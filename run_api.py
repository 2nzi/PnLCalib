import uvicorn

if __name__ == "__main__":
    print("🚀 Démarrage de l'API Football Vision Calibration...")
    print("📍 API accessible sur: http://localhost:8000")
    print("📖 Documentation: http://localhost:8000/docs")
    
    uvicorn.run(
        "api:app",  # ← Changement ici : string au lieu d'objet
        host="0.0.0.0", 
        port=8000,
        reload=True  # Rechargement automatique en développement
    )