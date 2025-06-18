import requests
import json
from pathlib import Path

# Configuration
API_URL = "http://localhost:8000"
IMAGE_PATH = "examples/input/cam3.jpg"  # Adaptez selon votre structure
# IMAGE_PATH = "examples/input/FootDrone.jpg"  # Adaptez selon votre structure
VIDEO_PATH = "examples/input/FootDrone.mp4"  # Adaptez selon votre structure

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
    "Big rect. right bottom": [
        {"x": 32.736572890025556, "y": 397.21988189225624},
        {"x": 0.3753980224568448, "y": 407.0286292126068}
    ],
    "Small rect. right top": [
        {"x": 312.24913494809687, "y": 1075.6461846681693},
        {"x": 426.66666666666663, "y": 999.9279904137233}
    ],
    "Small rect. right main": [
        {"x": 426.66666666666663, "y": 999.9279904137233},
        {"x": 0, "y": 769.079837198949}
    ],
    "Circle right": [
        {"x": 828.6491513601493, "y": 668.8579000924583},
        {"x": 821.7759602949911, "y": 612.2830792373484},
        {"x": 782.8739995106773, "y": 564.5621490047902},
        {"x": 722.6387053930304, "y": 529.3993583071158},
        {"x": 623.5014504910696, "y": 503.02726528386006},
        {"x": 494.24654853028534, "y": 492.980753655953},
        {"x": 349.8767728435256, "y": 500.9610345717304}
    ],
    "Side line bottom": [
        {"x": 2.0193824656299317, "y": 266.2605192109321},
        {"x": 399.0443993689428, "y": 186.14824976426013},
        {"x": 645.5533017804819, "y": 132.93313314748357},
        {"x": 1001.1088573360372, "y": 53.39824942655338},
        {"x": 1208.1676808654488, "y": 7.351737798646435}
    ],
    "Middle line": [
        {"x": 645.5533017804819, "y": 132.93313314748357},
        {"x": 1106.0585089650835, "y": 200.22939899146556},
        {"x": 1580.7388158704541, "y": 269.8451725000601},
        {"x": 1917.6527118636336, "y": 318.9857185061268}
    ],
    "Circle central": [
        {"x": 1580.7388158704541, "y": 269.8451725000601},
        {"x": 1580.7388158704541, "y": 269.8451725000601},
        {"x": 1533.8366024891266, "y": 288.8643838246303},
        {"x": 1441.810458698277, "y": 302.46903498742097},
        {"x": 1316.3202626198458, "y": 304.5620582432349},
        {"x": 1219.0653606590615, "y": 292.0039187083512},
        {"x": 1135.4052299401073, "y": 274.2132210339326},
        {"x": 1069.522876998931, "y": 237.5853140571884},
        {"x": 1106.0585089650835, "y": 200.22939899146556},
        {"x": 1139.5882364760548, "y": 189.4457791734675},
        {"x": 1224.2941188289963, "y": 177.9341512664908},
        {"x": 1314.2287593518718, "y": 174.79461638276985},
        {"x": 1392.6601319008914, "y": 180.02717452230473},
        {"x": 1465.8627462799764, "y": 190.49229080137454},
        {"x": 1529.6535959531789, "y": 204.09694196416518},
        {"x": 1581.9411776525253, "y": 230.2597326618396},
        {"x": 1580.7388158704541, "y": 269.8451725000601}
    ],
    "Side line left": [
        {"x": 1208.1676808654488, "y": 7.351737798646435},
        {"x": 1401.9652021886754, "y": 20.565213248502545},
        {"x": 1582.3573590514204, "y": 30.37625976013045},
        {"x": 1679.416182580832, "y": 34.300678364781604},
        {"x": 1824.5142217965183, "y": 41.23091697692868},
        {"x": 1918.6318688553417, "y": 42.21202162809147}
    ],
    "Big rect. left bottom": [
        {"x": 1401.9652021886754, "y": 20.565213248502545},
        {"x": 1283.3377512082834, "y": 53.98527744204496}
    ],
    "Big rect. left main": [
        {"x": 1283.3377512082834, "y": 53.98527744204496},
        {"x": 1510.7887316004399, "y": 73.60737046530076},
        {"x": 1808.8279472867146, "y": 94.21056813971936},
        {"x": 1918.6318688553417, "y": 100.0971960466961}
    ],
    "Circle left": [
        {"x": 1510.7887316004399, "y": 73.60737046530076},
        {"x": 1548.0436335612244, "y": 86.36173093041702},
        {"x": 1620.5926531690673, "y": 95.19167279088215},
        {"x": 1681.3769668945574, "y": 97.15388209320773},
        {"x": 1746.0828492474989, "y": 100.0971960466961},
        {"x": 1808.8279472867146, "y": 94.21056813971936}
    ],
    "Small rect. left bottom": [
        {"x": 1550.9848100318127, "y": 42.21202162809147},
        {"x": 1582.3573590514204, "y": 30.37625976013045}
    ],
    "Small rect. left main": [
        {"x": 1550.9848100318127, "y": 42.21202162809147},
        {"x": 1918.418689198772, "y": 60.49417894940041}
    ]
}

def test_health():
    """Test du health check"""
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'API. Vérifiez qu'elle est démarrée.")
        return False
    except Exception as e:
        print(f"❌ Erreur health check: {e}")
        return False

def test_calibration():
    """Test de l'API de calibration avec lignes manuelles"""
    if not Path(IMAGE_PATH).exists():
        print(f"❌ Image non trouvée: {IMAGE_PATH}")
        print(f"   Chemin absolu: {Path(IMAGE_PATH).absolute()}")
        return
    
    print(f"📁 Test avec l'image: {IMAGE_PATH}")
    print(f"   Taille du fichier: {Path(IMAGE_PATH).stat().st_size} bytes")
    
    try:
        with open(IMAGE_PATH, 'rb') as image_file:
            files = {'image': (Path(IMAGE_PATH).name, image_file, 'image/jpeg')}
            data = {'lines_data': json.dumps(cam3_line_dict)}
            
            print("🚀 Envoi de la requête de calibration...")
            response = requests.post(
                f"{API_URL}/calibrate",
                files=files,
                data=data
            )
            
            print(f"📡 Réponse reçue: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Calibration réussie!")
                print("Paramètres de la caméra:")
                print(json.dumps(result['camera_parameters'], indent=2))
            else:
                print(f"❌ Erreur calibration: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"Détail de l'erreur: {error_detail}")
                except:
                    print(f"Réponse brute: {response.text}")
                    
    except Exception as e:
        print(f"❌ Exception lors du test de calibration: {e}")

def test_inference_image():
    """Test de l'inférence automatique sur image"""
    if not Path(IMAGE_PATH).exists():
        print(f"❌ Image non trouvée: {IMAGE_PATH}")
        print(f"   Chemin absolu: {Path(IMAGE_PATH).absolute()}")
        return
        
    print(f"📁 Test inférence avec l'image: {IMAGE_PATH}")
    print(f"   Taille du fichier: {Path(IMAGE_PATH).stat().st_size} bytes")
    
    try:
        with open(IMAGE_PATH, 'rb') as image_file:
            files = {'image': (Path(IMAGE_PATH).name, image_file, 'image/jpeg')}
            data = {
                'kp_threshold': 0.15,
                'line_threshold': 0.15
            }
            
            print("🚀 Envoi de la requête d'inférence image...")
            response = requests.post(
                f"{API_URL}/inference/image",
                files=files,
                data=data
            )
            
            print(f"📡 Réponse reçue: {response.status_code}")
            print(f"📡 Réponse reçue: {response.json()}")
            
            if response.status_code == 200 and response.json()['status'] == 'success':
                result = response.json()
                print("✅ Inférence image réussie!")
                print(f"Status: {result['status']}")
                print(f"Image info: {result['image_info']}")
                if result['camera_parameters']:
                    print("Paramètres de la caméra:")
                    cam_params = result['camera_parameters'].get('cam_params', {})
                    print(f"  Position: {cam_params.get('position_meters', 'N/A')}")
                    print(f"  Focale X: {cam_params.get('x_focal_length', 'N/A')}")
                    print(f"  Focale Y: {cam_params.get('y_focal_length', 'N/A')}")
            else:
                print(f"❌ Erreur inférence image: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"Détail de l'erreur: {error_detail}")
                except:
                    print(f"Réponse brute: {response.text}")
                    
    except Exception as e:
        print(f"❌ Exception lors du test d'inférence image: {e}")

def test_inference_video():
    """Test de l'inférence automatique sur vidéo"""
    if not Path(VIDEO_PATH).exists():
        print(f"❌ Vidéo non trouvée: {VIDEO_PATH}")
        print(f"   Chemin absolu: {Path(VIDEO_PATH).absolute()}")
        return
        
    print(f"📁 Test inférence avec la vidéo: {VIDEO_PATH}")
    print(f"   Taille du fichier: {Path(VIDEO_PATH).stat().st_size} bytes")
    print("🎬 Test inférence vidéo (peut prendre du temps...)") 
    
    try:
        with open(VIDEO_PATH, 'rb') as video_file:
            files = {'video': (Path(VIDEO_PATH).name, video_file, 'video/mp4')}
            data = {
                'kp_threshold': 0.15,
                'line_threshold': 0.15,
                'frame_step': 200  # Traiter 1 frame sur 10 pour le test
            }
            
            print("🚀 Envoi de la requête d'inférence vidéo...")
            response = requests.post(
                f"{API_URL}/inference/video",
                files=files,
                data=data
            )
            
            print(f"📡 Réponse reçue: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Inférence vidéo réussie!")
                print(f"Status: {result['status']}")
                print(f"Frames traitées: {result['frames_processed']}")
                print(f"Vidéo info: {result['video_info']}")
                
                if result['camera_parameters']:
                    print(f"\n=== Exemples de paramètres ===")
                    for i, params in enumerate(result['camera_parameters'][:3]):
                        frame_num = params.get('frame_number', i)
                        timestamp = params.get('timestamp_seconds', 0)
                        print(f"Frame {frame_num} (t={timestamp:.2f}s):")
                        if 'cam_params' in params:
                            cam_params = params['cam_params']
                            print(f"  Position: {cam_params.get('position_meters', 'N/A')}")
                            print(f"  Focales: X={cam_params.get('x_focal_length', 'N/A')}, Y={cam_params.get('y_focal_length', 'N/A')}")
                    
                    if len(result['camera_parameters']) > 3:
                        print(f"... et {len(result['camera_parameters']) - 3} autres frames")
            else:
                print(f"❌ Erreur inférence vidéo: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"Détail de l'erreur: {error_detail}")
                except:
                    print(f"Réponse brute: {response.text}")
                    
    except Exception as e:
        print(f"❌ Exception lors du test d'inférence vidéo: {e}")

def test_all():
    """Lance tous les tests"""
    print("=== TEST DE L'API FOOTBALL VISION ===\n")
    
    # Test 1: Health check
    # print("1. Test Health Check")
    # if not test_health():
    #     print("❌ API non accessible, arrêt des tests")
    #     return
    # print()
    
    # # Vérifier les chemins des fichiers
    # print("2. Vérification des fichiers")
    # print(f"   Image: {'✅' if Path(IMAGE_PATH).exists() else '❌'} {IMAGE_PATH}")
    # print(f"   Vidéo: {'✅' if Path(VIDEO_PATH).exists() else '❌'} {VIDEO_PATH}")
    # print()
    
    # # Test 2: Calibration avec lignes manuelles
    # print("3. Test Calibration (lignes manuelles)")
    # test_calibration()
    # print()
    
    # Test 3: Inférence image
    print("4. Test Inférence Image (automatique)")
    test_inference_image()
    print()
    
    # # Test 4: Inférence vidéo
    # print("5. Test Inférence Vidéo (automatique)")
    # test_inference_video()
    # print()

if __name__ == "__main__":
    test_all()