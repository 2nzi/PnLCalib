import requests
import json
from pathlib import Path

# Configuration
API_URL = "http://localhost:8000"
IMAGE_PATH = "examples/input/cam3.jpg"  # Adaptez selon votre structure

# Données d'exemple (votre cam3_line_dict)
cam3_line_dict = {
    "Big rect. right top": [
        {"x": 1342.8861505076343, "y": 1076.997434976179},
        {"x": 1484.7446330310781, "y": 906.3705391217808}
    ],
    "Big rect. right main": [
        {"x": 1484.7446330310781, "y": 906.3705391217808},
        {"x": 1049.6210183678218, "y": 748.0287797688992},
        {"x": 828.6491513601493, "y": 668.8579000924583},
        {"x": 349.8767728435256, "y": 500.9610345717304},
        {"x": 32.736572890025556, "y": 397.21988189225624}
    ],
    # ... ajoutez les autres lignes si nécessaire
}

def test_api():
    """Test de l'API de calibration"""
    
    # Test du health check
    response = requests.get(f"{API_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
    
    # Test de calibration
    if Path(IMAGE_PATH).exists():
        with open(IMAGE_PATH, 'rb') as image_file:
            files = {'image': image_file}
            data = {'lines_data': json.dumps(cam3_line_dict)}
            
            response = requests.post(
                f"{API_URL}/calibrate",
                files=files,
                data=data
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Calibration réussie!")
                print("Paramètres de la caméra:")
                print(json.dumps(result['camera_parameters'], indent=2))
            else:
                print(f"❌ Erreur: {response.status_code}")
                print(response.json())
    else:
        print(f"❌ Image non trouvée: {IMAGE_PATH}")

if __name__ == "__main__":
    test_api()