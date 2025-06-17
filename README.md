# PnLCalib API

> API REST pour la calibration de caméras à partir de lignes de terrain de football

## À propos de ce projet

Cette API est basée sur le travail de recherche original de **SoccerNet Camera Calibration Challenge**. Elle transforme les algorithmes de calibration existants en une API REST accessible et facile à utiliser.

### Travail original
📍 **Repository source** : [SoccerNet Camera Calibration](https://github.com/SoccerNet/sn-calibration)  [Marc Gutiérrez-Pérez](https://github.com/mguti97/PnLCalib)
📖 **Paper** : SoccerNet Camera Calibration Challenge  
👥 **Auteurs** : Équipe SoccerNet

## Fonctionnalités

✅ Calibration automatique de caméras à partir d'images de terrain de football  
✅ API REST avec FastAPI  
✅ Support des formats d'image : JPG, PNG  

## Installation locale

```bash
# Cloner le repository
git clone https://github.com/2nzi/PnLCalib.git
cd PnLCalib

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'API
python run_api.py
```

L'API sera accessible sur : http://localhost:8000

## Utilisation

### Endpoint principal : `/calibrate`

**POST** `/calibrate` - Calibrer une caméra à partir d'une image et de lignes du terrain

**Paramètres :**
- `image` : Fichier image (multipart/form-data)
- `lines_data` : JSON des lignes du terrain (string)

### Exemple d'utilisation

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

const response = await fetch('http://localhost:8000/calibrate', {
    method: 'POST',
    body: formData
});

const result = await response.json();
console.log('Paramètres de calibration:', result.camera_parameters);
```

#### Avec curl
```bash
curl -X POST "http://localhost:8000/calibrate" \
  -F "image=@terrain.jpg" \
  -F 'lines_data={"Big rect. right top":[{"x":1342.88,"y":1076.99}]}'
```

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

Une fois l'API lancée, accédez à la documentation interactive :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## Health Check

```bash
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
