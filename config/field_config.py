"""
Configuration file for football field elements (lines and keypoints)
All measurements are in meters
Field dimensions: 105m x 68m
Origin (0,0) is at top-left corner
"""

# Lines configuration
LINES = {
    1: {"name": "Big rect. left bottom", "description": "Surface de réparation gauche - ligne basse"},
    2: {"name": "Big rect. left main", "description": "Surface de réparation gauche - ligne parallèle"},
    3: {"name": "Big rect. left top", "description": "Surface de réparation gauche - ligne haute"},
    4: {"name": "Big rect. right bottom", "description": "Surface de réparation droite - ligne basse"},
    5: {"name": "Big rect. right main", "description": "Surface de réparation droite - ligne parallèle"},
    6: {"name": "Big rect. right top", "description": "Surface de réparation droite - ligne haute"},
    7: {"name": "Goal left crossbar", "description": "Barre transversale but gauche"},
    8: {"name": "Goal left post left", "description": "Poteau gauche but gauche"},
    9: {"name": "Goal left post right", "description": "Poteau droit but gauche"},
    10: {"name": "Goal right crossbar", "description": "Barre transversale but droit"},
    11: {"name": "Goal right post left", "description": "Poteau gauche but droit"},
    12: {"name": "Goal right post right", "description": "Poteau droit but droit"},
    13: {"name": "Middle line", "description": "Ligne médiane"},
    14: {"name": "Side line bottom", "description": "Ligne de but"},
    15: {"name": "Side line left", "description": "Ligne de touche gauche"},
    16: {"name": "Side line right", "description": "Ligne de touche droite"},
    17: {"name": "Side line top", "description": "Ligne de but opposée"},
    18: {"name": "Small rect. left bottom", "description": "Petite surface gauche - ligne basse"},
    19: {"name": "Small rect. left main", "description": "Petite surface gauche - ligne parallèle"},
    20: {"name": "Small rect. left top", "description": "Petite surface gauche - ligne haute"},
    21: {"name": "Small rect. right bottom", "description": "Petite surface droite - ligne basse"},
    22: {"name": "Small rect. right main", "description": "Petite surface droite - ligne parallèle"},
    23: {"name": "Small rect. right top", "description": "Petite surface droite - ligne haute"}
}

# Keypoints configuration
KEYPOINTS = {
    # Points principaux (1-30)
    1: {"name": "Top Left Corner", "coords": [0.0, 0.0], "description": "Coin supérieur gauche"},
    2: {"name": "Top Middle", "coords": [52.5, 0.0], "description": "Milieu ligne du haut"},
    3: {"name": "Top Right Corner", "coords": [105.0, 0.0], "description": "Coin supérieur droit"},
    4: {"name": "Left Big Box Top", "coords": [0.0, 16.5], "description": "Surface gauche haut"},
    5: {"name": "Left Big Box Main", "coords": [16.5, 16.5], "description": "Surface gauche principale"},
    6: {"name": "Right Big Box Main", "coords": [88.5, 16.5], "description": "Surface droite principale"},
    7: {"name": "Right Big Box Top", "coords": [105.0, 16.5], "description": "Surface droite haut"},
    8: {"name": "Left Small Box Top", "coords": [0.0, 5.5], "description": "Petite surface gauche haut"},
    9: {"name": "Left Small Box Main", "coords": [5.5, 5.5], "description": "Petite surface gauche principale"},
    10: {"name": "Right Small Box Main", "coords": [99.5, 5.5], "description": "Petite surface droite principale"},
    11: {"name": "Right Small Box Top", "coords": [105.0, 5.5], "description": "Petite surface droite haut"},
    12: {"name": "Left Goal Crossbar Right", "coords": [3.66, 0.0], "description": "Barre transversale gauche - droite"},
    13: {"name": "Left Goal Post Right", "coords": [3.66, 2.44], "description": "Poteau droit but gauche"},
    14: {"name": "Right Goal Post Left", "coords": [101.34, 2.44], "description": "Poteau gauche but droit"},
    15: {"name": "Right Goal Crossbar Left", "coords": [101.34, 0.0], "description": "Barre transversale droite - gauche"},
    16: {"name": "Left Goal Crossbar Left", "coords": [0.0, 0.0], "description": "Barre transversale gauche - gauche"},
    17: {"name": "Left Goal Post Left", "coords": [0.0, 2.44], "description": "Poteau gauche but gauche"},
    18: {"name": "Right Goal Post Right", "coords": [105.0, 2.44], "description": "Poteau droit but droit"},
    19: {"name": "Right Goal Crossbar Right", "coords": [105.0, 0.0], "description": "Barre transversale droite - droite"},
    20: {"name": "Left Small Box Bottom", "coords": [0.0, 0.0], "description": "Petite surface gauche bas"},
    21: {"name": "Left Small Box Bottom Main", "coords": [5.5, 0.0], "description": "Petite surface gauche bas principale"},
    22: {"name": "Right Small Box Bottom Main", "coords": [99.5, 0.0], "description": "Petite surface droite bas principale"},
    23: {"name": "Right Small Box Bottom", "coords": [105.0, 0.0], "description": "Petite surface droite bas"},
    24: {"name": "Left Big Box Bottom", "coords": [0.0, 0.0], "description": "Surface gauche bas"},
    25: {"name": "Bottom Middle", "coords": [52.5, 0.0], "description": "Milieu ligne du bas"},
    26: {"name": "Right Big Box Bottom", "coords": [105.0, 0.0], "description": "Surface droite bas"},
    27: {"name": "Left Big Box Bottom Main", "coords": [16.5, 0.0], "description": "Surface gauche bas principale"},
    28: {"name": "Bottom Middle Top", "coords": [52.5, 68.0], "description": "Milieu ligne opposée"},
    29: {"name": "Right Big Box Bottom Main", "coords": [88.5, 0.0], "description": "Surface droite bas principale"},
    30: {"name": "Left Penalty Spot", "coords": [11.0, 34.0], "description": "Point de penalty gauche"},

    # Points auxiliaires (31-57)
    31: {"name": "Left Box Aux 1", "coords": [16.5, 20.0], "description": "Point auxiliaire surface gauche 1"},
    32: {"name": "Center Circle Left", "coords": [43.35, 34.0], "description": "Rond central gauche"},
    33: {"name": "Center Circle Right", "coords": [61.65, 34.0], "description": "Rond central droit"},
    34: {"name": "Right Box Aux 1", "coords": [88.5, 20.0], "description": "Point auxiliaire surface droite 1"},
    35: {"name": "Left Box Aux 2", "coords": [16.5, 48.0], "description": "Point auxiliaire surface gauche 2"},
    36: {"name": "Right Box Aux 2", "coords": [88.5, 48.0], "description": "Point auxiliaire surface droite 2"},
    37: {"name": "Center Circle Top Left", "coords": [43.35, 24.85], "description": "Rond central haut gauche"},
    38: {"name": "Center Circle Top Right", "coords": [61.65, 24.85], "description": "Rond central haut droit"},
    39: {"name": "Center Circle Bottom Left", "coords": [43.35, 43.15], "description": "Rond central bas gauche"},
    40: {"name": "Center Circle Bottom Right", "coords": [61.65, 43.15], "description": "Rond central bas droit"},
    41: {"name": "Center Circle Left Inner", "coords": [46.03, 34.0], "description": "Rond central intérieur gauche"},
    42: {"name": "Center Circle Right Inner", "coords": [58.97, 34.0], "description": "Rond central intérieur droit"},
    43: {"name": "Center Circle Top Inner", "coords": [52.5, 27.53], "description": "Rond central intérieur haut"},
    44: {"name": "Center Circle Bottom Inner", "coords": [52.5, 40.47], "description": "Rond central intérieur bas"},
    45: {"name": "Left Penalty Arc Left", "coords": [19.99, 32.29], "description": "Arc penalty gauche - point gauche"},
    46: {"name": "Left Penalty Arc Right", "coords": [19.99, 35.71], "description": "Arc penalty gauche - point droit"},
    47: {"name": "Right Penalty Arc Left", "coords": [85.01, 32.29], "description": "Arc penalty droit - point gauche"},
    48: {"name": "Right Penalty Arc Right", "coords": [85.01, 35.71], "description": "Arc penalty droit - point droit"},
    49: {"name": "Left Penalty Arc Top", "coords": [16.5, 34.0], "description": "Arc penalty gauche - point haut"},
    50: {"name": "Right Penalty Arc Top", "coords": [88.5, 34.0], "description": "Arc penalty droit - point haut"},
    51: {"name": "Left Penalty Area Center", "coords": [16.5, 34.0], "description": "Centre surface de réparation gauche"},
    52: {"name": "Right Penalty Area Center", "coords": [88.5, 34.0], "description": "Centre surface de réparation droite"},
    53: {"name": "Right Penalty Spot", "coords": [94.0, 34.0], "description": "Point de penalty droit"},
    54: {"name": "Center Spot", "coords": [52.5, 34.0], "description": "Point central"},
    55: {"name": "Left Box Center", "coords": [16.5, 34.0], "description": "Centre surface gauche"},
    56: {"name": "Right Box Center", "coords": [88.5, 34.0], "description": "Centre surface droite"},
    57: {"name": "Center Circle Center", "coords": [52.5, 34.0], "description": "Centre rond central"}
}

# Field dimensions
FIELD_DIMENSIONS = {
    "length": 105.0,  # meters
    "width": 68.0,    # meters
    "center_circle_radius": 9.15,
    "penalty_area_length": 16.5,
    "penalty_area_width": 40.32,
    "goal_area_length": 5.5,
    "goal_area_width": 18.32,
    "penalty_spot_dist": 11.0,
    "goal_height": 2.44,
    "goal_width": 7.32
}

# Line intersections that form keypoints
KEYPOINT_LINE_PAIRS = [
    ["Side line top", "Side line left"],
    ["Side line top", "Middle line"],
    ["Side line right", "Side line top"],
    ["Side line left", "Big rect. left top"],
    ["Big rect. left top", "Big rect. left main"],
    ["Big rect. right top", "Big rect. right main"],
    ["Side line right", "Big rect. right top"],
    ["Side line left", "Small rect. left top"],
    ["Small rect. left top", "Small rect. left main"],
    ["Small rect. right top", "Small rect. right main"],
    ["Side line right", "Small rect. right top"],
    ["Goal left crossbar", "Goal left post right"],
    ["Side line left", "Goal left post right"],
    ["Side line right", "Goal right post left"],
    ["Goal right crossbar", "Goal right post left"],
    ["Goal left crossbar", "Goal left post left"],
    ["Side line left", "Goal left post left"],
    ["Side line right", "Goal right post right"],
    ["Goal right crossbar", "Goal right post right"],
    ["Side line left", "Small rect. left bottom"],
    ["Small rect. left bottom", "Small rect. left main"],
    ["Small rect. right bottom", "Small rect. right main"],
    ["Side line right", "Small rect. right bottom"],
    ["Side line left", "Big rect. left bottom"],
    ["Big rect. left bottom", "Big rect. left main"],
    ["Big rect. right bottom", "Big rect. right main"],
    ["Side line right", "Big rect. right bottom"],
    ["Side line left", "Side line bottom"],
    ["Side line right", "Side line bottom"]
]

# Auxiliary keypoint pairs
KEYPOINT_AUX_PAIRS = [
    ["Small rect. left main", "Side line top"],
    ["Big rect. left main", "Side line top"],
    ["Big rect. right main", "Side line top"],
    ["Small rect. right main", "Side line top"],
    ["Small rect. left main", "Big rect. left top"],
    ["Big rect. right top", "Small rect. right main"],
    ["Small rect. left top", "Big rect. left main"],
    ["Small rect. right top", "Big rect. right main"],
    ["Small rect. left bottom", "Big rect. left main"],
    ["Small rect. right bottom", "Big rect. right main"],
    ["Small rect. left main", "Big rect. left bottom"],
    ["Small rect. right main", "Big rect. right bottom"],
    ["Small rect. left main", "Side line bottom"],
    ["Big rect. left main", "Side line bottom"],
    ["Big rect. right main", "Side line bottom"],
    ["Small rect. right main", "Side line bottom"]
] 