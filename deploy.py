#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de déploiement pour l'application de filtrage de vidéos
"""

import os
import sys
import subprocess

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    print("[VERIFICATION] Verification des dependances...")
    
    required_packages = ['flask', 'pandas', 'werkzeug']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"[OK] {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"[MANQUANT] {package}")
    
    if missing_packages:
        print(f"\n[INSTALLATION] Installation des packages manquants: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("[OK] Installation terminee")
        except subprocess.CalledProcessError:
            print("[ERREUR] Erreur lors de l'installation")
            return False
    
    return True

def create_directories():
    """Crée les répertoires nécessaires"""
    print("[REPERTOIRES] Creation des repertoires...")
    
    directories = ['uploads', 'templates']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"[OK] Cree: {directory}")
        else:
            print(f"[INFO] Existe deja: {directory}")

def check_files():
    """Vérifie que tous les fichiers nécessaires sont présents"""
    print("[FICHIERS] Verification des fichiers...")
    
    required_files = [
        'app.py',
        'run_app.py',
        'templates/base.html',
        'templates/index.html',
        'templates/result.html',
        'requirements.txt'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"[OK] {file_path}")
        else:
            missing_files.append(file_path)
            print(f"[MANQUANT] {file_path}")
    
    if missing_files:
        print(f"\n[ATTENTION] Fichiers manquants: {', '.join(missing_files)}")
        return False
    
    return True

def main():
    """Fonction principale de déploiement"""
    print("=" * 60)
    print("DEPLOIEMENT DE L'APPLICATION DE FILTRAGE DE VIDEOS")
    print("=" * 60)
    
    # Vérifications
    if not check_dependencies():
        print("[ERREUR] Echec de la verification des dependances")
        return False
    
    create_directories()
    
    if not check_files():
        print("[ERREUR] Fichiers manquants detectes")
        return False
    
    print("\n[SUCCES] Deploiement termine avec succes !")
    print("\n[INFO] Pour demarrer l'application:")
    print("   python run_app.py")
    print("\n[INFO] Puis ouvrez votre navigateur sur:")
    print("   http://localhost:5000")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
