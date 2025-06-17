# # Utiliser une image Miniconda avec Python 3.9
# FROM continuumio/miniconda3:latest

# # Définir un répertoire de travail
# WORKDIR /app

# # Copier le fichier environment.yml dans le conteneur
# COPY PnLCalib.yml .

# # Installer l'environnement conda
# RUN conda env create -f PnLCalib.yml

# # Activer l'environnement par défaut et définir la commande d'entrée
# SHELL ["conda", "run", "-n", "PnLCalib", "/bin/bash", "-c"]

# # Définir le point d'entrée du conteneur (changer si besoin)
# CMD ["python"]

# # Utiliser une image Miniconda avec Python 3.9
# FROM continuumio/miniconda3:latest

# # Définir un répertoire de travail
# WORKDIR /app

# # Copier le fichier environment.yml dans le conteneur
# COPY PnLCalib.yml .

# # Copier le script Python et les fichiers nécessaires dans le conteneur
# COPY inference.py .
# COPY examples/messi_sample.png .

# # Installer l'environnement conda
# RUN conda env create -f PnLCalib.yml

# # Activer l'environnement par défaut et définir la commande d'entrée
# SHELL ["conda", "run", "-n", "PnLCalib", "/bin/bash", "-c"]

# # Définir le point d'entrée du conteneur pour exécuter le script Python
# CMD ["python", "inference.py", "--weights_kp", "SV_kp", "--weights_line", "SV_lines", "--pnl_refine", "--input_path", "examples/messi_sample.png", "--input_type", "image", "--save_path", "examples/messi_results.png"]








# # Utiliser une image de base Python
# FROM python:3.9-slim

# # Définir un répertoire de travail
# WORKDIR /app

# # Copier le fichier requirements.txt dans le conteneur
# COPY requirements.txt .

# # Copier le script Python et les fichiers nécessaires dans le conteneur
# COPY inference.py .
# COPY examples/messi_sample.png .

# # Installer les dépendances
# RUN pip install --no-cache-dir -r requirements.txt

# # Définir le point d'entrée du conteneur pour exécuter le script Python
# CMD ["python", "inference.py", "--weights_kp", "SV_kp", "--weights_line", "SV_lines", "--pnl_refine", "--input_path", "examples/messi_sample.png", "--input_type", "image", "--save_path", "examples/messi_results.png"]





FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the entire project into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define the entry point
CMD ["python", "inference.py", "--weights_kp", "SV_kp", "--weights_line", "SV_lines", "--pnl_refine", "--input_path", "examples/messi_sample.png", "--input_type", "image", "--save_path", "examples/messi_results.png"]