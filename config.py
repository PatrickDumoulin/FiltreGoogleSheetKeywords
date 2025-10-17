#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration pour l'application de filtrage de vidéos
"""

import os

class Config:
    """Configuration de base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre_cle_secrete_changez_moi'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    ALLOWED_EXTENSIONS = {'csv'}
    
    # Configuration de l'application
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True
    
    # Messages
    MESSAGES = {
        'upload_success': 'Fichiers uploadés avec succès !',
        'filter_success': 'Filtrage terminé avec succès !',
        'file_not_found': 'Fichier non trouvé',
        'invalid_file': 'Seuls les fichiers CSV sont autorisés',
        'missing_files': 'Veuillez sélectionner les deux fichiers CSV',
        'processing_error': 'Erreur lors du traitement des fichiers'
    }

class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cle_secrete_production_changez_moi'

class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True

# Configuration par défaut
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

