from utils.utils_keypoints import KeypointsDB
from utils.utils_lines import LineKeypointsDB
from utils.utils_calib import FramebyFrameCalib
from utils.utils_heatmap import complete_keypoints
from PIL import Image
import torch
import numpy as np

# Données de lignes pour cam3
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

def transform_data(line_dict, width, height):
    """
    Transform input line dictionary to normalized coordinates.
    """
    transformed = {}
    for line_name, points in line_dict.items():
        transformed[line_name] = []
        for point in points:
            transformed[line_name].append({
                "x": point["x"] / width,
                "y": point["y"] / height
            })
    return transformed

def get_camera_parameters(image_path, line_dict):
    """
    Extract camera parameters from image and line data.
    
    Args:
        image_path (str): Path to the image file
        line_dict (dict): Dictionary containing line coordinates
        
    Returns:
        dict: Camera parameters
    """
    # Load image
    image = Image.open(image_path)
    image_tensor = torch.FloatTensor(np.array(image)).permute(2, 0, 1)
    
    # Get image dimensions
    img_width, img_height = image.size
    
    # Transform data using actual image dimensions
    trans_data = transform_data(line_dict, img_width, img_height)
    
    # Initialize databases
    kp_db = KeypointsDB(trans_data, image_tensor)
    ln_db = LineKeypointsDB(trans_data, image_tensor)
    
    # Get keypoints and lines
    kp_db.get_full_keypoints()
    ln_db.get_lines()
    
    kp_dict = kp_db.keypoints_final
    ln_dict = ln_db.lines
    
    # Complete keypoints
    kp_dict, ln_dict = complete_keypoints(kp_dict, ln_dict, img_width, img_height)
    
    # Initialize calibration
    cam = FramebyFrameCalib(img_width, img_height)
    cam.update(kp_dict, ln_dict)
    cam_params = cam.heuristic_voting(refine_lines=True)
    
    return cam_params

def main():
    # Chemin vers votre image
    image_path = "examples/input/cam3.jpg"
    
    # Obtenir les paramètres de la caméra
    camera_params = get_camera_parameters(image_path, cam3_line_dict)
    
    # Afficher les paramètres
    print("=== PARAMÈTRES DE LA CAMÉRA ===")
    print(f"Position (mètres): {camera_params['cam_params']['position_meters']}")
    print(f"Distance focale X: {camera_params['cam_params']['x_focal_length']:.2f}")
    print(f"Distance focale Y: {camera_params['cam_params']['y_focal_length']:.2f}")
    print(f"Point principal: {camera_params['cam_params']['principal_point']}")
    print(f"Matrice de rotation:")
    rotation_matrix = np.array(camera_params['cam_params']['rotation_matrix'])
    print(rotation_matrix)
    
    # Calcul des angles d'Euler
    euler_angles = np.array([
        np.arctan2(rotation_matrix[2,1], rotation_matrix[2,2]),  # roll
        np.arctan2(-rotation_matrix[2,0], np.sqrt(rotation_matrix[2,1]**2 + rotation_matrix[2,2]**2)),  # pitch
        np.arctan2(rotation_matrix[1,0], rotation_matrix[0,0])   # yaw
    ]) * 180 / np.pi
    
    print(f"Angles d'Euler (degrés):")
    print(f"  Roll: {euler_angles[0]:.1f}°")
    print(f"  Pitch: {euler_angles[1]:.1f}°")
    print(f"  Yaw: {euler_angles[2]:.1f}°")

    # print(camera_params)
    
    return camera_params

if __name__ == "__main__":
    main() 