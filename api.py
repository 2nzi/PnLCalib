from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any
import json
import tempfile
import os
from PIL import Image
import numpy as np

from get_camera_params import get_camera_parameters

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

@app.get("/")
async def root():
    return {
        "message": "Football Vision Calibration API", 
        "version": "1.0.0",
        "endpoints": {
            "/calibrate": "POST - Calibrer une caméra à partir d'une image et de lignes",
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
        # Validation du format d'image
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Le fichier doit être une image")
        
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
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{image.filename.split('.')[-1]}") as temp_file:
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

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# Ajoutez ceci à la place :
# Point d'entrée pour Vercel
app_instance = app