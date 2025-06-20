from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import json
import tempfile
import os
from PIL import Image
import numpy as np
import cv2
import torch
import torchvision.transforms as T
import torchvision.transforms.functional as f
import yaml
from tqdm import tqdm
from huggingface_hub import hf_hub_download

from get_camera_params import get_camera_parameters

# Imports pour l'inférence automatique
from model.cls_hrnet import get_cls_net
from model.cls_hrnet_l import get_cls_net as get_cls_net_l
from utils.utils_calib import FramebyFrameCalib
from utils.utils_heatmap import get_keypoints_from_heatmap_batch_maxpool, get_keypoints_from_heatmap_batch_maxpool_l, complete_keypoints, coords_to_dict

app = FastAPI(
    title="Football Vision Calibration API",
    description="API pour la calibration de caméras à partir de lignes de terrain de football",
    version="1.0.0"
)

# Configuration CORS pour autoriser les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifiez les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paramètres par défaut pour l'inférence
WEIGHTS_KP = "models/SV_FT_TSWC_kp"
WEIGHTS_LINE = "models/SV_FT_TSWC_lines"
# DEVICE = "cuda:0"
DEVICE = "cpu"
KP_THRESHOLD = 0.15
LINE_THRESHOLD = 0.15
PNL_REFINE = True
FRAME_STEP = 5

# Cache pour les modèles (éviter de les recharger à chaque requête)
_models_cache = None

# Paramètres pour HF Hub
HF_MODEL_REPO = "2nzi/SV_FT_TSWC_kp"  # Remplacez par votre repo
WEIGHTS_KP_FILE = "SV_FT_TSWC_kp"  # Nom du fichier dans le repo
WEIGHTS_LINE_FILE = "SV_FT_TSWC_lines"  # Nom du fichier dans le repo

def load_inference_models():
    """Charge les modèles d'inférence depuis Hugging Face Hub"""
    global _models_cache
    
    if _models_cache is not None:
        return _models_cache
    
    try:
        # Device detection
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {device}")
        
        # Télécharger les modèles depuis HF Hub
        print("Téléchargement des modèles depuis Hugging Face Hub...")
        
        weights_kp_path = hf_hub_download(
            repo_id=HF_MODEL_REPO,
            filename=WEIGHTS_KP_FILE,
            cache_dir="./hf_cache"
        )
        
        weights_line_path = hf_hub_download(
            repo_id=HF_MODEL_REPO, 
            filename=WEIGHTS_LINE_FILE,
            cache_dir="./hf_cache"
        )
        
        print(f"Modèles téléchargés:")
        print(f"  - Keypoints: {weights_kp_path}")
        print(f"  - Lines: {weights_line_path}")
        
        # Vérifier l'existence des fichiers de configuration
        config_files = ["config/hrnetv2_w48.yaml", "config/hrnetv2_w48_l.yaml"]
        for config_file in config_files:
            if not os.path.exists(config_file):
                raise FileNotFoundError(f"Fichier de configuration manquant: {config_file}")
        
        # Charger les configurations
        with open("config/hrnetv2_w48.yaml", 'r') as f:
            cfg = yaml.safe_load(f)
        with open("config/hrnetv2_w48_l.yaml", 'r') as f:
            cfg_l = yaml.safe_load(f)
        
        # Modèle keypoints
        model = get_cls_net(cfg)
        model.load_state_dict(torch.load(weights_kp_path, map_location=device))
        model.to(device)
        model.eval()
        
        # Modèle lignes
        model_l = get_cls_net_l(cfg_l)
        model_l.load_state_dict(torch.load(weights_line_path, map_location=device))
        model_l.to(device)
        model_l.eval()
        
        _models_cache = (model, model_l, device)
        print("✅ Modèles chargés avec succès depuis HF Hub!")
        return _models_cache
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement des modèles: {e}")
        raise HTTPException(
            status_code=503, 
            detail=f"Modèles non disponibles: {str(e)}. Veuillez réessayer plus tard."
        )

def process_frame_inference(frame, model, model_l, device, frame_width, frame_height):
    """Traite une frame et retourne les paramètres de caméra"""
    transform = T.Resize((540, 960))
    
    # Préparer la frame pour l'inférence
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_pil = Image.fromarray(frame_rgb)
    frame_tensor = f.to_tensor(frame_pil).float().unsqueeze(0)
    
    if frame_tensor.size()[-1] != 960:
        frame_tensor = transform(frame_tensor)
    
    frame_tensor = frame_tensor.to(device)
    b, c, h, w = frame_tensor.size()
    
    # Inférence
    with torch.no_grad():
        heatmaps = model(frame_tensor)
        heatmaps_l = model_l(frame_tensor)
    
    # Extraire les keypoints et lignes
    kp_coords = get_keypoints_from_heatmap_batch_maxpool(heatmaps[:,:-1,:,:])
    line_coords = get_keypoints_from_heatmap_batch_maxpool_l(heatmaps_l[:,:-1,:,:])
    kp_dict = coords_to_dict(kp_coords, threshold=KP_THRESHOLD)
    lines_dict = coords_to_dict(line_coords, threshold=LINE_THRESHOLD)
    kp_dict, lines_dict = complete_keypoints(kp_dict[0], lines_dict[0], w=w, h=h, normalize=True)
    
    # Calibration
    cam = FramebyFrameCalib(iwidth=frame_width, iheight=frame_height, denormalize=True)
    cam.update(kp_dict, lines_dict)
    final_params_dict = cam.heuristic_voting(refine_lines=PNL_REFINE)
    
    return final_params_dict

# Modèles Pydantic pour la validation des données
class Point(BaseModel):
    x: float
    y: float

class LinePolygon(BaseModel):
    points: List[Point]

class CalibrationRequest(BaseModel):
    lines: Dict[str, List[Point]]

class CalibrationResponse(BaseModel):
    status: str
    camera_parameters: Dict[str, Any]
    input_lines: Dict[str, List[Point]]
    message: str

class InferenceImageResponse(BaseModel):
    status: str
    camera_parameters: Optional[Dict[str, Any]]
    image_info: Dict[str, Any]
    message: str

class InferenceVideoResponse(BaseModel):
    status: str
    camera_parameters: List[Dict[str, Any]]
    video_info: Dict[str, Any]
    frames_processed: int
    message: str

@app.get("/")
async def root():
    return {
        "message": "Football Vision Calibration API", 
        "version": "1.0.0",
        "endpoints": {
            "/calibrate": "POST - Calibrer une caméra à partir d'une image et de lignes",
            "/inference/image": "POST - Extraire les paramètres de caméra d'une image automatiquement",
            "/inference/video": "POST - Extraire les paramètres de caméra d'une vidéo automatiquement",
            "/health": "GET - Vérifier l'état de l'API"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.post("/calibrate", response_model=CalibrationResponse)
async def calibrate_camera(
    image: UploadFile = File(..., description="Image du terrain de football"),
    lines_data: str = Form(..., description="JSON des lignes du terrain")
):
    """
    Calibrer une caméra à partir d'une image et des lignes du terrain.
    
    Args:
        image: Image du terrain de football (formats: jpg, jpeg, png)
        lines_data: JSON contenant les lignes du terrain au format:
                   {"nom_ligne": [{"x": float, "y": float}, ...], ...}
    
    Returns:
        Paramètres de calibration de la caméra et lignes d'entrée
    """
    try:
        # Validation du format d'image - version robuste
        content_type = getattr(image, 'content_type', None) or ""
        filename = getattr(image, 'filename', "") or ""
        
        # Vérifier le type MIME ou l'extension du fichier
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
        is_image_content = content_type.startswith('image/') if content_type else False
        is_image_extension = any(filename.lower().endswith(ext) for ext in image_extensions)
        
        if not is_image_content and not is_image_extension:
            raise HTTPException(
                status_code=400, 
                detail=f"Le fichier doit être une image. Type détecté: {content_type}, Fichier: {filename}"
            )
        
        # Parse des données de lignes
        try:
            lines_dict = json.loads(lines_data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Format JSON invalide pour les lignes")
        
        # Validation de la structure des lignes
        validated_lines = {}
        for line_name, points in lines_dict.items():
            if not isinstance(points, list):
                raise HTTPException(
                    status_code=400, 
                    detail=f"Les points de la ligne '{line_name}' doivent être une liste"
                )
            
            validated_points = []
            for i, point in enumerate(points):
                if not isinstance(point, dict) or 'x' not in point or 'y' not in point:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Point {i} de la ligne '{line_name}' doit avoir les clés 'x' et 'y'"
                    )
                try:
                    validated_points.append({
                        "x": float(point['x']),
                        "y": float(point['y'])
                    })
                except (ValueError, TypeError):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Coordonnées invalides pour le point {i} de la ligne '{line_name}'"
                    )
            
            validated_lines[line_name] = validated_points
        
        # Sauvegarde temporaire de l'image
        file_extension = os.path.splitext(filename)[1] if filename else '.jpg'
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            content = await image.read()
            temp_file.write(content)
            temp_image_path = temp_file.name
        
        try:
            # Validation de l'image
            pil_image = Image.open(temp_image_path)
            pil_image.verify()  # Vérification de l'intégrité de l'image
            
            # Calibration de la caméra
            camera_params = get_camera_parameters(temp_image_path, validated_lines)
            
            # Formatage de la réponse
            response = CalibrationResponse(
                status="success",
                camera_parameters=camera_params,
                input_lines=validated_lines,
                message="Calibration réussie"
            )
            
            return response
            
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Erreur lors de la calibration: {str(e)}"
            )
        
        finally:
            # Nettoyage du fichier temporaire
            if os.path.exists(temp_image_path):
                os.unlink(temp_image_path)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@app.post("/inference/image", response_model=InferenceImageResponse)
async def inference_image(
    image: UploadFile = File(..., description="Image du terrain de football"),
    kp_threshold: float = Form(KP_THRESHOLD, description="Seuil pour les keypoints"),
    line_threshold: float = Form(LINE_THRESHOLD, description="Seuil pour les lignes")
):
    """
    Extraire automatiquement les paramètres de caméra à partir d'une image.
    
    Args:
        image: Image du terrain de football (formats: jpg, jpeg, png)
        kp_threshold: Seuil pour la détection des keypoints (défaut: 0.15)
        line_threshold: Seuil pour la détection des lignes (défaut: 0.15)
    
    Returns:
        Paramètres de calibration de la caméra extraits automatiquement
    """
    params = None  # Initialiser params
    try:
        # Validation du format d'image - version robuste
        content_type = getattr(image, 'content_type', None) or ""
        filename = getattr(image, 'filename', "") or ""
        
        # Vérifier le type MIME ou l'extension du fichier
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
        is_image_content = content_type.startswith('image/') if content_type else False
        is_image_extension = any(filename.lower().endswith(ext) for ext in image_extensions)
        
        if not is_image_content and not is_image_extension:
            raise HTTPException(
                status_code=400, 
                detail=f"Le fichier doit être une image. Type détecté: {content_type}, Fichier: {filename}"
            )
        
        # Sauvegarde temporaire de l'image
        file_extension = os.path.splitext(filename)[1] if filename else '.jpg'
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            content = await image.read()
            temp_file.write(content)
            temp_image_path = temp_file.name
        
        try:
            # Charger les modèles
            model, model_l, device = load_inference_models()
            
            # Lire l'image
            frame = cv2.imread(temp_image_path)
            if frame is None:
                raise HTTPException(status_code=400, detail="Impossible de lire l'image")
            
            frame_height, frame_width = frame.shape[:2]
            
            # Mettre à jour les seuils globaux
            global KP_THRESHOLD, LINE_THRESHOLD
            KP_THRESHOLD = kp_threshold
            LINE_THRESHOLD = line_threshold
            
            # Traitement
            params = process_frame_inference(frame, model, model_l, device, frame_width, frame_height)
            
            # Formatage de la réponse
            response = InferenceImageResponse(
                status="success" if params is not None else "failed",
                camera_parameters=params,
                image_info={
                    "filename": filename,
                    "width": frame_width,
                    "height": frame_height,
                    "kp_threshold": kp_threshold,
                    "line_threshold": line_threshold
                },
                message="Paramètres extraits avec succès" if params is not None else "Échec de l'extraction des paramètres"
            )
            
            return response
            
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Erreur lors de l'inférence: {str(e)}"
            )
        
        finally:
            # Nettoyage du fichier temporaire
            if os.path.exists(temp_image_path):
                os.unlink(temp_image_path)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@app.post("/inference/video", response_model=InferenceVideoResponse)
async def inference_video(
    video: UploadFile = File(..., description="Vidéo du terrain de football"),
    kp_threshold: float = Form(KP_THRESHOLD, description="Seuil pour les keypoints"),
    line_threshold: float = Form(LINE_THRESHOLD, description="Seuil pour les lignes"),
    frame_step: int = Form(FRAME_STEP, description="Traiter 1 frame sur N")
):
    """
    Extraire automatiquement les paramètres de caméra à partir d'une vidéo.
    
    Args:
        video: Vidéo du terrain de football (formats: mp4, avi, mov, etc.)
        kp_threshold: Seuil pour la détection des keypoints (défaut: 0.15)
        line_threshold: Seuil pour la détection des lignes (défaut: 0.15)
        frame_step: Traiter 1 frame sur N pour accélérer le traitement (défaut: 5)
    
    Returns:
        Liste des paramètres de calibration de la caméra pour chaque frame traitée
    """
    try:
        # Validation du format vidéo - version robuste
        content_type = getattr(video, 'content_type', None) or ""
        filename = getattr(video, 'filename', "") or ""
        
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
        is_video_content = content_type.startswith('video/') if content_type else False
        is_video_extension = any(filename.lower().endswith(ext) for ext in video_extensions)
        
        if not is_video_content and not is_video_extension:
            raise HTTPException(
                status_code=400, 
                detail=f"Le fichier doit être une vidéo. Type détecté: {content_type}, Fichier: {filename}"
            )
        
        # Sauvegarde temporaire de la vidéo
        file_extension = os.path.splitext(filename)[1] if filename else '.mp4'
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            content = await video.read()
            temp_file.write(content)
            temp_video_path = temp_file.name
        
        try:
            # Charger les modèles
            model, model_l, device = load_inference_models()
            
            # Ouvrir la vidéo
            cap = cv2.VideoCapture(temp_video_path)
            if not cap.isOpened():
                raise HTTPException(status_code=400, detail="Impossible d'ouvrir la vidéo")
            
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            
            # Mettre à jour les seuils globaux
            global KP_THRESHOLD, LINE_THRESHOLD
            KP_THRESHOLD = kp_threshold
            LINE_THRESHOLD = line_threshold
            
            all_params = []
            frame_count = 0
            processed_count = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                    
                # Traiter seulement 1 frame sur frame_step
                if frame_count % frame_step != 0:
                    frame_count += 1
                    continue
                
                # Traitement
                params = process_frame_inference(frame, model, model_l, device, frame_width, frame_height)
                
                if params is not None:
                    params['frame_number'] = frame_count
                    params['timestamp_seconds'] = frame_count / fps
                    all_params.append(params)
                    processed_count += 1
                
                frame_count += 1
            
            cap.release()
            
            # Formatage de la réponse
            response = InferenceVideoResponse(
                status="success" if all_params else "failed",
                camera_parameters=all_params,
                video_info={
                    "filename": filename,
                    "width": frame_width,
                    "height": frame_height,
                    "total_frames": total_frames,
                    "fps": fps,
                    "duration_seconds": total_frames / fps,
                    "kp_threshold": kp_threshold,
                    "line_threshold": line_threshold,
                    "frame_step": frame_step
                },
                frames_processed=processed_count,
                message=f"Paramètres extraits de {processed_count} frames" if all_params else "Aucun paramètre extrait"
            )
            
            return response
            
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Erreur lors de l'inférence vidéo: {str(e)}"
            )
        
        finally:
            # Nettoyage du fichier temporaire
            if os.path.exists(temp_video_path):
                os.unlink(temp_video_path)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

app_instance = app