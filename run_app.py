#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de démarrage pour l'application web de filtrage de vidéos
"""

from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("FILTREUR DE VIDEOS - INTERFACE WEB")
    print("=" * 60)
    print("L'application va démarrer sur http://localhost:5000")
    print("Appuyez sur Ctrl+C pour arrêter l'application")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

