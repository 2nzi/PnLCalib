from utils.utils_keypoints import KeypointsDB
from utils.utils_lines import LineKeypointsDB
from utils.utils_calib import FramebyFrameCalib
from utils.utils_heatmap import complete_keypoints
from PIL import Image
import torch
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D



cam1_line_dict = {
    "Side line top": [
        {"x": 0, "y": 205.35510086780727},
        {"x": 226.69196710942427, "y": 218.52089231566922},
        {"x": 609.2346616065778, "y": 235.73769651671947},
        {"x": 1072.7387729285256, "y": 248.90348796458142},
        {"x": 1642.5047438330162, "y": 257.005513470958},
        {"x": 1918.7855787476271, "y": 257.005513470958}
    ],
    "Big rect. right top": [
        {"x": 1918.6823296329553, "y": 327.02322511812105},
        {"x": 1761.8195845349164, "y": 327.02322511812105}
    ],
    "Big rect. right main": [
        {"x": 1761.8195845349164, "y": 327.02322511812105},
        {"x": 1774.5760335197388, "y": 409.7284234765342},
        {"x": 1790.8194197631253, "y": 526.9377258021154},
        {"x": 1809.8670388107444, "y": 671.5805829449724}
    ],
    "Big rect. right bottom": [
        {"x": 1809.8670388107444, "y": 671.5805829449724},
        {"x": 1917.4300640208282, "y": 677.1868952373312}
    ],
    "Circle right": [
        {"x": 1774.5760335197388, "y": 409.7284234765342},
        {"x": 1709.2165563955555, "y": 410.6005164997901},
        {"x": 1629.0422644565579, "y": 423.6819118486273},
        {"x": 1576.7546827572116, "y": 442.8679583602552},
        {"x": 1568.0400858073206, "y": 459.43772580211566},
        {"x": 1592.4409572670156, "y": 482.11214440676673},
        {"x": 1698.7590400556867, "y": 511.7633071974644},
        {"x": 1790.8194197631253, "y": 526.9377258021154}
    ],
    "Middle line": [
        {"x": 0, "y": 308.65587267083185},
        {"x": 226.69196710942427, "y": 218.52089231566922}
    ],
    "Circle central": [
        {"x": 0, "y": 340.8997444495873},
        {"x": 122.94647588765228, "y": 351.0820197481417},
        {"x": 234.87016428192882, "y": 366.3554326959732},
        {"x": 305.2464228934815, "y": 390.1140750592667},
        {"x": 309.48595654477987, "y": 413.8727174225603},
        {"x": 228.08691043985144, "y": 441.0254515520386},
        {"x": 71.22416534181235, "y": 463.08704803223975},
        {"x": 4.239533651298354, "y": 468.1781856815169}
    ],
    "Side line bottom": [
        {"x": 1.3071895424836595, "y": 814.522819727929},
        {"x": 636.6013071895421, "y": 827.6042150767662},
        {"x": 1286.2745098039209, "y": 852.458866239557},
        {"x": 1918.954248366012, "y": 889.086773216301}
    ]
}

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
    
    Args:
        line_dict (dict): Dictionary containing line coordinates
        width (int): Image width
        height (int): Image height
        
    Returns:
        dict: Dictionary with normalized coordinates
    """
    transformed = {}
    
    for line_name, points in line_dict.items():
        transformed[line_name] = []
        for point in points:
            # Normalize coordinates by dividing by image dimensions
            transformed[line_name].append({
                "x": point["x"] / width,
                "y": point["y"] / height
            })
            
    return transformed



def plot_camera_position(cam_params, keypoints_dict=None, lines_dict=None):
    """
    Plot the camera position, orientation and points relative to the football field.
    
    Args:
        cam_params (dict): Dictionary containing camera parameters
        keypoints_dict (dict, optional): Dictionary containing keypoints in image coordinates
        lines_dict (dict, optional): Dictionary containing lines in image coordinates
    """
    # Field dimensions in meters
    field_length = 105
    field_width = 68
    
    # Get camera parameters
    camera_pos = np.array(cam_params["cam_params"]["position_meters"])
    R = np.array(cam_params["cam_params"]["rotation_matrix"])
    
    # Create 3D figure
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Draw main field
    field_corners = np.array([
        [-field_length/2, -field_width/2, 0],
        [field_length/2, -field_width/2, 0],
        [field_length/2, field_width/2, 0],
        [-field_length/2, field_width/2, 0],
        [-field_length/2, -field_width/2, 0]
    ])
    ax.plot(field_corners[:, 0], field_corners[:, 1], field_corners[:, 2], 'g-', label='Field')
    
    # Add midline
    ax.plot([0, 0], [-field_width/2, field_width/2], [0, 0], 'w--', label='Midline')
    
    # Add penalty areas
    # Left penalty area
    penalty_line, = ax.plot([-field_length/2, -field_length/2+16.5], [-20.16, -20.16], [0, 0], 'r-', linewidth=2, label='Penalty areas')
    ax.plot([-field_length/2, -field_length/2+16.5], [20.16, 20.16], [0, 0], 'r-', linewidth=2)
    ax.plot([-field_length/2+16.5, -field_length/2+16.5], [-20.16, 20.16], [0, 0], 'r-', linewidth=2)
    
    # Right penalty area
    ax.plot([field_length/2, field_length/2-16.5], [-20.16, -20.16], [0, 0], 'r-', linewidth=2)
    ax.plot([field_length/2, field_length/2-16.5], [20.16, 20.16], [0, 0], 'r-', linewidth=2)
    ax.plot([field_length/2-16.5, field_length/2-16.5], [-20.16, 20.16], [0, 0], 'r-', linewidth=2)
    
    # Add center circle
    circle_points = 100
    theta = np.linspace(0, 2*np.pi, circle_points)
    radius = 9.15
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = np.zeros_like(theta)
    ax.plot(x, y, z, 'y-', label='Center circle')
    
    # Plot camera position
    ax.scatter(camera_pos[0], camera_pos[1], camera_pos[2], color='red', s=100, label='Camera')
    
    # Draw image plane
    rect_width = 16     
    rect_height = 9
    corners_cam = np.array([
        [-rect_width/2, -rect_height/2, 2],
        [rect_width/2, -rect_height/2, 2],
        [rect_width/2, rect_height/2, 2],
        [-rect_width/2, rect_height/2, 2],
        [-rect_width/2, -rect_height/2, 2]
    ])
    corners_world = np.array([camera_pos + R.T @ corner for corner in corners_cam])
    ax.plot(corners_world[:, 0], corners_world[:, 1], corners_world[:, 2], 
            'magenta', linewidth=2, label='Image plane')
    
    # Draw lines from camera to image plane corners
    for corner in corners_world[:-1]:
        ax.plot([camera_pos[0], corner[0]], 
                [camera_pos[1], corner[1]], 
                [camera_pos[2], corner[2]], 
                'y--', alpha=0.5)
    
    # Draw view direction
    direction = R[2] * 10
    ax.quiver(camera_pos[0], camera_pos[1], camera_pos[2],
              direction[0], direction[1], direction[2],
              color='blue', label='View direction')
    
    # Set labels and title
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_zlabel('Z (meters)')
    ax.set_title('Camera position relative to field')
    
    # Set axis limits with equal aspect ratio
    ax.set_xlim([-field_length/2, field_length/2])
    ax.set_ylim([-field_width/2, field_width/2])
    ax.set_zlim([-30, 10])
    ax.set_box_aspect([field_length, field_width, 40])  # Aspect ratio is 1:1:1
    
    # Add grid
    ax.grid(True)
    
    # Add goal annotations
    ax.text(-field_length/2, 0, 0, 'Left Goal', color='black')
    ax.text(field_length/2, 0, 0, 'Right Goal', color='black')
    
    # Calculate and display Euler angles
    euler_angles = np.array([
        np.arctan2(R[2,1], R[2,2]),  # roll
        np.arctan2(-R[2,0], np.sqrt(R[2,1]**2 + R[2,2]**2)),  # pitch
        np.arctan2(R[1,0], R[0,0])   # yaw
    ]) * 180 / np.pi
    
    # Add camera information text
    plt.figtext(0.02, 0.02, 
                f'Position: {camera_pos}\n'
                f'Focal length X: {cam_params["cam_params"]["x_focal_length"]:.2f}\n'
                f'Focal length Y: {cam_params["cam_params"]["y_focal_length"]:.2f}\n'
                f'Rotation (deg):\n'
                f'Roll: {euler_angles[0]:.1f}°\n'
                f'Pitch: {euler_angles[1]:.1f}°\n'
                f'Yaw: {euler_angles[2]:.1f}°', 
                bbox=dict(facecolor='white', alpha=0.8))
    
    # Create custom legend
    legend_elements = [
        Line2D([0], [0], color='g', label='Field'),
        Line2D([0], [0], color='w', linestyle='--', label='Midline'),
        Line2D([0], [0], color='y', label='Center circle'),
        Line2D([0], [0], color='r', label='Penalty areas'),
        Line2D([0], [0], color='magenta', label='Image plane'),
        Line2D([0], [0], color='blue', label='View direction'),
        Line2D([0], [0], color='y', linestyle='--', label='Projection rays'),
        plt.scatter([0], [0], color='red', s=100, label='Camera'),
    ]

    # Add keypoints and lines to legend if they exist
    if keypoints_dict is not None:
        legend_elements.append(plt.scatter([0], [0], color='cyan', s=50, label='Keypoints'))
    
    if lines_dict is not None:
        legend_elements.append(plt.scatter([0], [0], color='magenta', s=50, label='Line points'))
        legend_elements.append(Line2D([0], [0], color='m', alpha=0.5, label='Lines'))

    # Add the legend with all elements
    ax.legend(handles=legend_elements, loc='upper right')

    # Add this function to convert image points to 3D world coordinates
    def image_to_world(point_2d, cam_params):
        # Create projection matrix P
        K = np.array([
            [cam_params["cam_params"]["x_focal_length"], 0, cam_params["cam_params"]["principal_point"][0]],
            [0, cam_params["cam_params"]["y_focal_length"], cam_params["cam_params"]["principal_point"][1]],
            [0, 0, 1]
        ])
        R = np.array(cam_params["cam_params"]["rotation_matrix"])
        t = -R @ np.array(cam_params["cam_params"]["position_meters"])
        P = K @ np.hstack((R, t.reshape(-1,1)))
        
        # Create point on image plane in homogeneous coordinates
        point_2d_h = np.array([point_2d[0], point_2d[1], 1])
        
        # Back-project ray from camera
        ray = np.linalg.inv(K) @ point_2d_h
        ray = R.T @ ray
        
        # Find intersection with Z=0 plane
        camera_pos = np.array(cam_params["cam_params"]["position_meters"])
        t = -camera_pos[2] / ray[2]
        world_point = camera_pos + t * ray
        
        return world_point[:2]  # Return only X,Y coordinates since Z=0

    # Plot keypoints if provided
    if keypoints_dict is not None:
        for kp_key, kp_value in keypoints_dict.items():
            point_2d = np.array([kp_value['x'], kp_value['y']])
            point_3d = image_to_world(point_2d, cam_params)
            
            # Plot point
            ax.scatter(point_3d[0], point_3d[1], 0, color='cyan', s=50, label='Keypoints' if kp_key == 1 else "")
            # Add keypoint number as text
            ax.text(point_3d[0], point_3d[1], 0.1, str(kp_key), 
                   color='black', fontsize=8, ha='center', va='bottom')

    # Plot lines if provided
    if lines_dict is not None:
        for line_key, line_value in lines_dict.items():
            # Convert start point
            start_2d = np.array([line_value['x_1'], line_value['y_1']])
            start_3d = image_to_world(start_2d, cam_params)
            
            # Convert end point
            end_2d = np.array([line_value['x_2'], line_value['y_2']])
            end_3d = image_to_world(end_2d, cam_params)
            
            # Plot points and line
            ax.scatter(start_3d[0], start_3d[1], 0, color='magenta', s=50)
            ax.scatter(end_3d[0], end_3d[1], 0, color='magenta', s=50, 
                      label='Line points' if line_key == list(lines_dict.keys())[0] else "")
            ax.plot([start_3d[0], end_3d[0]], 
                   [start_3d[1], end_3d[1]], 
                   [0, 0], 'm-', alpha=0.5)

    plt.show()


def plot_2d_points(image_path, keypoints_dict=None, lines_dict=None):
    """
    Plot keypoints and lines on the original 2D image.
    
    Args:
        image_path (str): Path to the original image
        keypoints_dict (dict, optional): Dictionary containing keypoints in image coordinates
        lines_dict (dict, optional): Dictionary containing lines in image coordinates
    """
    # Load and display the image
    image = plt.imread(image_path)
    plt.figure(figsize=(15, 8))
    plt.imshow(image)
    
    # Plot keypoints if provided
    if keypoints_dict is not None:
        for kp_key, kp_value in keypoints_dict.items():
            x, y = kp_value['x'], kp_value['y']
            plt.scatter(x, y, color='cyan', s=100)
            plt.text(x+10, y+10, str(kp_key), color='white', fontsize=8,
                    bbox=dict(facecolor='black', alpha=0.7))
    
    # Plot lines if provided
    if lines_dict is not None:
        for line_key, line_value in lines_dict.items():
            x1, y1 = line_value['x_1'], line_value['y_1']
            x2, y2 = line_value['x_2'], line_value['y_2']
            plt.scatter([x1, x2], [y1, y2], color='magenta', s=100)
            plt.plot([x1, x2], [y1, y2], 'magenta', alpha=0.5)
    
    plt.title('2D Points and Lines on Original Image')
    plt.axis('off')
    plt.show()


def main():
    # Load image
    image = Image.open("examples/input/cam1.jpg")
    # Convert PIL Image to tensor format expected by utils
    image_tensor = torch.FloatTensor(np.array(image)).permute(2, 0, 1)
    
    # Get actual image dimensions
    img_width, img_height = image.size
    
    # Transform data using actual image dimensions
    # trans_data1 = transform_data(cam1_line_dict, img_width, img_height)
    trans_data1 = transform_data(cam3_line_dict, img_width, img_height)

    # Print transformed data
    # print("\n=== Transformed Data ===")
    # for line_name, points in trans_data1.items():
    #     print(f"{line_name}: {points}")
    
    # Initialize databases with transformed data and tensor image
    kp_db = KeypointsDB(trans_data1, image_tensor)
    ln_db = LineKeypointsDB(trans_data1, image_tensor)
    
    # Get keypoints and lines
    kp_db.get_full_keypoints()
    ln_db.get_lines()

    kp_dict = kp_db.keypoints_final
    ln_dict = ln_db.lines

    # Print number of keypoints and lines before completion
    print("\n=== Before Completion ===")
    print(f"Number of keypoints: {len(kp_dict)}")

    # Complete keypoints using actual image dimensions
    kp_dict, ln_dict = complete_keypoints(kp_dict, ln_dict, img_width, img_height)

    # Print number of keypoints and lines after completion
    print("\n=== After Completion ===")
    print(f"Number of keypoints: {len(kp_dict)}")

    # Print new keypoints
    print("\n=== New Keypoints ===")
    for kp_key, kp_value in kp_dict.items():
        print(f"{kp_key}: {kp_value}")
    
    # Initialize calibration with actual image dimensions
    cam = FramebyFrameCalib(img_width, img_height)
    cam.update(kp_dict, ln_dict)
    cam_params = cam.heuristic_voting(refine_lines=True)
    
    print(cam)
    print(cam_params)

    # Plot camera position and line points
    plot_camera_position(cam_params, kp_dict, ln_dict)
    
    # Plot 2D points
    plot_2d_points("examples/input/cam3.jpg", kp_dict, ln_dict)

if __name__ == "__main__":
    main()