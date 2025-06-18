import sys
import os
import cv2
import torch
import numpy as np
import torchvision.transforms as T
import torchvision.transforms.functional as f
from PIL import Image
import yaml
from tqdm import tqdm
import json

from model.cls_hrnet import get_cls_net
from model.cls_hrnet_l import get_cls_net as get_cls_net_l
from utils.utils_calib import FramebyFrameCalib
from utils.utils_heatmap import get_keypoints_from_heatmap_batch_maxpool, get_keypoints_from_heatmap_batch_maxpool_l, complete_keypoints, coords_to_dict

# Paramètres par défaut inspirés du config.yaml
WEIGHTS_KP = "models/SV_FT_TSWC_kp"
WEIGHTS_LINE = "models/SV_FT_TSWC_lines"
DEVICE = "cuda:0"
INPUT_PATH = "examples/input/"
OUTPUT_PATH = "examples/output/"
KP_THRESHOLD = 0.15
LINE_THRESHOLD = 0.15
PNL_REFINE = True
FRAME_STEP = 5  # Pour les vidéos : traiter 1 frame sur 5

# Extensions supportées
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']

def load_models():
    """Charge les modèles de keypoints et lignes"""
    device = torch.device(DEVICE if torch.cuda.is_available() else 'cpu')
    
    # Charger les configurations
    cfg = yaml.safe_load(open("config/hrnetv2_w48.yaml", 'r'))
    cfg_l = yaml.safe_load(open("config/hrnetv2_w48_l.yaml", 'r'))
    
    # Modèle keypoints
    model = get_cls_net(cfg)
    model.load_state_dict(torch.load(WEIGHTS_KP, map_location=device))
    model.to(device)
    model.eval()
    
    # Modèle lignes
    model_l = get_cls_net_l(cfg_l)
    model_l.load_state_dict(torch.load(WEIGHTS_LINE, map_location=device))
    model_l.to(device)
    model_l.eval()
    
    return model, model_l, device

def process_frame(frame, model, model_l, device, frame_width, frame_height):
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

def detect_file_type(filename):
    """Détecte si le fichier est une image ou une vidéo"""
    ext = os.path.splitext(filename.lower())[1]
    if ext in IMAGE_EXTENSIONS:
        return 'image'
    elif ext in VIDEO_EXTENSIONS:
        return 'video'
    else:
        return 'unknown'

def process_image(filename):
    """Traite une image et retourne les paramètres de caméra"""
    print(f"=== TRAITEMENT IMAGE ===")
    print(f"Fichier: {filename}")
    
    # Charger les modèles
    model, model_l, device = load_models()
    
    # Lire l'image
    image_path = INPUT_PATH + filename
    frame = cv2.imread(image_path)
    if frame is None:
        raise ValueError(f"Impossible de lire l'image: {image_path}")
    
    frame_height, frame_width = frame.shape[:2]
    print(f"Résolution: {frame_width}x{frame_height}")
    
    # Traitement
    print("Inférence en cours...")
    params = process_frame(frame, model, model_l, device, frame_width, frame_height)
    
    if params is not None:
        print("✅ Paramètres extraits avec succès!")
        
        # Afficher les paramètres principaux
        if 'cam_params' in params:
            cam_params = params['cam_params']
            print(f"Position (mètres): {cam_params.get('position_meters', 'N/A')}")
            print(f"Focale X: {cam_params.get('x_focal_length', 'N/A'):.2f}")
            print(f"Focale Y: {cam_params.get('y_focal_length', 'N/A'):.2f}")
            print(f"Point principal: {cam_params.get('principal_point', 'N/A')}")
        
        return params
    else:
        print("❌ Échec de l'extraction des paramètres")
        return None

def process_video(filename):
    """Traite une vidéo et retourne la liste des paramètres de caméra"""
    print(f"=== TRAITEMENT VIDÉO ===")
    print(f"Fichier: {filename}")
    
    # Charger les modèles
    model, model_l, device = load_models()
    
    # Ouvrir la vidéo
    video_path = INPUT_PATH + filename
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Impossible d'ouvrir la vidéo: {video_path}")
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    print(f"Résolution: {frame_width}x{frame_height}")
    print(f"Total frames: {total_frames}, FPS: {fps}")
    print(f"Traitement: 1 frame sur {FRAME_STEP}")
    
    all_params = []
    frame_count = 0
    processed_count = 0
    
    pbar = tqdm(total=total_frames//FRAME_STEP, desc="Traitement vidéo")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Traiter seulement 1 frame sur FRAME_STEP
        if frame_count % FRAME_STEP != 0:
            frame_count += 1
            continue
        
        # Traitement
        params = process_frame(frame, model, model_l, device, frame_width, frame_height)
        
        if params is not None:
            params['frame_number'] = frame_count
            params['timestamp_seconds'] = frame_count / fps
            all_params.append(params)
            processed_count += 1
        
        frame_count += 1
        pbar.update(1)
    
    cap.release()
    pbar.close()
    
    print(f"✅ Traitement terminé: {processed_count} frames avec paramètres extraits")
    
    if all_params:
        # Sauvegarder automatiquement les résultats
        output_file = save_video_params(all_params, filename)
        
        # Afficher quelques exemples
        print(f"\n=== EXEMPLES ===")
        for i, params in enumerate(all_params[:3]):
            print(f"\n--- Frame {params.get('frame_number', i)} (t={params.get('timestamp_seconds', 0):.2f}s) ---")
            if 'cam_params' in params:
                cam_params = params['cam_params']
                print(f"Position: {cam_params.get('position_meters', 'N/A')}")
                print(f"Focales: X={cam_params.get('x_focal_length', 'N/A'):.2f}, Y={cam_params.get('y_focal_length', 'N/A'):.2f}")
        
        if len(all_params) > 3:
            print(f"\n... et {len(all_params) - 3} autres frames")
    
    return all_params

def save_video_params(params_list, video_filename):
    """Sauvegarde les paramètres vidéo dans un fichier JSON"""
    base_name = os.path.splitext(video_filename)[0]
    output_file = OUTPUT_PATH + f"camera_params_{base_name}.json"
    
    # Convertir les numpy arrays en listes pour la sérialisation JSON
    serializable_params = []
    for params in params_list:
        serializable = {}
        for key, value in params.items():
            if isinstance(value, np.ndarray):
                serializable[key] = value.tolist()
            elif isinstance(value, dict):
                serializable[key] = {}
                for k, v in value.items():
                    serializable[key][k] = v.tolist() if isinstance(v, np.ndarray) else v
            else:
                serializable[key] = value
        serializable_params.append(serializable)
    
    with open(output_file, 'w') as f:
        json.dump(serializable_params, f, indent=2)
    
    print(f"Paramètres sauvegardés dans: {output_file}")
    return output_file

def get_camera_params(filename):
    """
    Fonction principale : traite automatiquement une image ou vidéo
    
    Args:
        filename: nom du fichier dans INPUT_PATH
        
    Returns:
        dict ou list: paramètres de caméra
    """
    file_type = detect_file_type(filename)
    
    if file_type == 'image':
        return process_image(filename)
    elif file_type == 'video':
        return process_video(filename)
    else:
        raise ValueError(f"Type de fichier non supporté: {filename}")

if __name__ == "__main__":
    # Nom du fichier à traiter (changez ici selon vos besoins)
    filename = "FootDrone.mp4"  # Changez pour .jpg pour une image
    filename = "FootDrone.jpg"  # Changez pour .jpg pour une image
    
    try:
        print(f"=== EXTRACTION PARAMÈTRES CAMÉRA ===")
        print(f"Fichier: {filename}")
        print(f"Seuils: KP={KP_THRESHOLD}, LINE={LINE_THRESHOLD}")
        print(f"Device: {DEVICE}")
        
        # Détection automatique et traitement
        file_type = detect_file_type(filename)
        print(f"Type détecté: {file_type}")
        
        if file_type == 'unknown':
            print(f"❌ Type de fichier non supporté: {filename}")
            print(f"Extensions supportées:")
            print(f"  Images: {', '.join(IMAGE_EXTENSIONS)}")
            print(f"  Vidéos: {', '.join(VIDEO_EXTENSIONS)}")
        else:
            params = get_camera_params(filename)
            
            if params is not None:
                print(f"\n=== SUCCÈS ===")
                if file_type == 'image':
                    print("Paramètres de caméra extraits de l'image!")
                    print(f"Paramètres complets: {params}")
                else:
                    print(f"Paramètres de caméra extraits de {len(params)} frames de la vidéo!")
            else:
                print("❌ Aucun paramètre extrait")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")