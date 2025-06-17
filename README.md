# PnLCalib API

> API REST pour la calibration de caméras à partir de lignes de terrain de football

## 🌐 API en ligne

L'API est disponible directement en ligne sans installation :
**🔗 https://2nzi-pnlcalib.hf.space/**

Vous pouvez l'utiliser immédiatement dans vos applications !

## À propos de ce projet

Cette API est basée sur le travail de recherche original de **SoccerNet Camera Calibration Challenge**. Elle transforme les algorithmes de calibration existants en une API REST accessible et facile à utiliser.

### Travail original
📍 **Repository source** : [SoccerNet Camera Calibration](https://github.com/SoccerNet/sn-calibration)  [Marc Gutiérrez-Pérez](https://github.com/mguti97/PnLCalib)
📖 **Paper** : SoccerNet Camera Calibration Challenge  
👥 **Auteurs** : Équipe SoccerNet

### 🎯 Principe de fonctionnement

![Interface de calibration](https://github.com/2nzi/PnLCalib/blob/main/ressources/interface.png?raw=true)
*Interface permettant de définir les lignes du terrain de football*


## Fonctionnalités

✅ Calibration automatique de caméras à partir d'images de terrain de football  
✅ API REST avec FastAPI  
✅ Support des formats d'image : JPG, PNG  
✅ API hébergée disponible en ligne  
✅ Installation locale possible (pip ou Docker)

## Installation locale

### Option 1 : Installation avec pip

```bash
# Cloner le repository
git clone https://github.com/2nzi/PnLCalib.git
cd PnLCalib

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'API
python run_api.py
```

### Option 2 : Installation avec Docker

```bash
# Cloner le repository
git clone https://github.com/2nzi/PnLCalib.git
cd PnLCalib

# Construire l'image Docker
docker build -t pnlcalib-api .

# Lancer le conteneur
docker run -p 8000:8000 pnlcalib-api
```

**L'API sera accessible sur :** http://localhost:8000

## Utilisation

### 🌐 Utilisation avec l'API en ligne

#### Avec JavaScript/Fetch
```javascript
const formData = new FormData();
formData.append('image', imageFile);
formData.append('lines_data', JSON.stringify({
    "Big rect. right top": [
        {"x": 1342.88, "y": 1076.99},
        {"x": 1484.74, "y": 906.37}
    ],
    "Big rect. right main": [
        {"x": 1484.74, "y": 906.37},
        {"x": 1049.62, "y": 748.02}
    ],
    "Circle central": [
        {"x": 1580.73, "y": 269.84},
        {"x": 1533.83, "y": 288.86}
    ]
    // ... autres lignes
}));

const response = await fetch('https://2nzi-pnlcalib.hf.space/calibrate', {
    method: 'POST',
    body: formData
});

const result = await response.json();
console.log('Paramètres de calibration:', result.camera_parameters);
```

#### Avec curl
```bash
# API en ligne
curl -X POST "https://2nzi-pnlcalib.hf.space/calibrate" \
  -F "image=@terrain.jpg" \
  -F 'lines_data={"Big rect. right top":[{"x":1342.88,"y":1076.99}]}'

# API locale (si installée)
curl -X POST "http://localhost:8000/calibrate" \
  -F "image=@terrain.jpg" \
  -F 'lines_data={"Big rect. right top":[{"x":1342.88,"y":1076.99}]}'
```

<details>
<summary>📋 <strong>Exemple complet avec cam3.jpg</strong> (cliquer pour développer)</summary>

### Exemple pratique avec l'image cam3.jpg

Cet exemple utilise l'image `resources/cam3.jpg` du projet avec toutes les lignes détectées.

![Image d'exemple cam3.jpg](https://github.com/2nzi/PnLCalib/blob/main/ressources/cam3.jpg?raw=true)
*Image de terrain de football utilisée pour la calibration - cam3.jpg*

![Transformation de calibration](https://github.com/2nzi/PnLCalib/blob/main/ressources/transformation.png?raw=true)  
*Processus de transformation et de calibration de la caméra*

#### Avec curl

```bash
# API en ligne
curl -X POST "https://2nzi-pnlcalib.hf.space/calibrate" \
  -F "image=@resources/cam3.jpg" \
  -F 'lines_data={
    "Big rect. right top": [
        {"x": 12.8861505076343, "y": 1076.997434976179},
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
}'
```

#### Avec JavaScript/Fetch

```javascript
// Charger l'image (exemple avec input file)
const fileInput = document.getElementById('imageInput');
const imageFile = fileInput.files[0]; // ou charger resources/cam3.jpg

const linesData = {
    "Big rect. right top": [
        {"x": 12.8861505076343, "y": 1076.997434976179},
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
};

const formData = new FormData();
formData.append('image', imageFile); // ou charge resources/cam3.jpg
formData.append('lines_data', JSON.stringify(linesData));

try {
    const response = await fetch('https://2nzi-pnlcalib.hf.space/calibrate', {
        method: 'POST',
        body: formData
    });
    
    const result = await response.json();
    
    if (result.status === 'success') {
        console.log('🎯 Calibration réussie!');
        console.log('📐 Paramètres de la caméra:', result.camera_parameters);
        
        // Exemple de résultat attendu :
        // {
        //   "pan_degrees": -15.2,
        //   "tilt_degrees": 8.7,
        //   "roll_degrees": 0.3,
        //   "position_meters": [25.4, 35.1, 12.8],
        //   "x_focal_length": 1450.2,
        //   "y_focal_length": 1448.9,
        //   "principal_point": [960, 540]
        // }
    } else {
        console.error('❌ Erreur de calibration:', result.message);
    }
} catch (error) {
    console.error('❌ Erreur réseau:', error);
}
```

#### Avec Python

```python
import requests

# Préparer les données
files = {'image': open('resources/cam3.jpg', 'rb')}
data = {
    'lines_data': '''{
        "Big rect. right top": [
            {"x": 12.8861505076343, "y": 1076.997434976179},
            {"x": 1484.7446330310781, "y": 906.3705391217808}
        ],
        "Big rect. right main": [
            {"x": 1484.7446330310781, "y": 906.3705391217808},
            {"x": 1049.6210183678218, "y": 748.0287797688992},
            {"x": 828.6491513601493, "y": 668.8579000924583},
            {"x": 349.8767728435256, "y": 500.9610345717304},
            {"x": 32.736572890025556, "y": 397.21988189225624}
        ],
        "Circle central": [
            {"x": 1580.7388158704541, "y": 269.8451725000601},
            {"x": 1533.8366024891266, "y": 288.8643838246303}
        ]
    }'''
}

# Appel API
response = requests.post(
    'https://2nzi-pnlcalib.hf.space/calibrate',
    files=files,
    data=data
)

result = response.json()
print("📐 Paramètres de calibration:", result['camera_parameters'])
```

</details>

### Endpoint principal : `/calibrate`

**POST** `/calibrate` - Calibrer une caméra à partir d'une image et de lignes du terrain

**Paramètres :**
- `image` : Fichier image (multipart/form-data)
- `lines_data` : JSON des lignes du terrain (string)

### Format de réponse

```json
{
  "status": "success",
  "camera_parameters": {
    "pan_degrees": -45.2,
    "tilt_degrees": 12.8,
    "roll_degrees": 1.2,
    "position_meters": [10.5, 20.3, 5.8],
    "x_focal_length": 1200.5,
    "y_focal_length": 1201.2,
    "principal_point": [960, 540]
  },
  "input_lines": { /* lignes validées */ },
  "message": "Calibration réussie"
}
```

## Documentation

### API en ligne
- **API Info** : https://2nzi-pnlcalib.hf.space/
- **Swagger UI** : https://2nzi-pnlcalib.hf.space/docs
- **ReDoc** : https://2nzi-pnlcalib.hf.space/redoc

### API locale (si installée)
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## Health Check

```bash
# API en ligne
curl https://2nzi-pnlcalib.hf.space/health

# API locale
curl http://localhost:8000/health
```

## Support des lignes de terrain

L'API accepte ces types de lignes de terrain :
- `Big rect. right/left top/main/bottom`
- `Small rect. right/left top/main`
- `Circle right/left/central`
- `Side line bottom/left`
- `Middle line`
...

Chaque ligne est définie par une liste de points avec coordonnées `x` et `y`.

## Crédits

Basé sur le travail original de l'équipe SoccerNet pour le Camera Calibration Challenge [Marc Gutiérrez-Pérez](https://github.com/mguti97/PnLCalib).  
Transformé en API REST par [2nzi](https://github.com/2nzi).

## Licence

Voir [LICENSE](LICENSE) - Basé sur la licence du projet original SoccerNet.
