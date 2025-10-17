#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour l'interface web de filtrage de vidéos
"""

import requests
import time
import os

def test_interface():
    """Test de l'interface web"""
    print("[TEST] Test de l'interface web...")
    
    # Attendre que l'application démarre
    time.sleep(2)
    
    try:
        # Test de la page d'accueil
        response = requests.get('http://localhost:5000', timeout=10)
        if response.status_code == 200:
            print("[OK] Page d'accueil accessible")
        else:
            print(f"[ERREUR] Page d'accueil: {response.status_code}")
            return False
        
        # Test de la page de résultats (sans fichier)
        response = requests.get('http://localhost:5000/result', timeout=10)
        if response.status_code == 200:
            print("[OK] Page de resultats accessible")
        else:
            print(f"[ATTENTION] Page de resultats: {response.status_code}")
        
        print("[SUCCES] Interface web fonctionnelle !")
        print("[INFO] Ouvrez http://localhost:5000 dans votre navigateur")
        return True
        
    except requests.exceptions.ConnectionError:
        print("[ERREUR] Impossible de se connecter a l'application")
        print("   Assurez-vous que l'application est demarree avec: python run_app.py")
        return False
    except Exception as e:
        print(f"[ERREUR] Lors du test: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("TEST DE L'INTERFACE WEB")
    print("=" * 50)
    test_interface()
