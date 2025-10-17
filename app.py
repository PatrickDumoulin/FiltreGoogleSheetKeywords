#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface web pour le filtreur de vidéos par mots-clés
"""

from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import pandas as pd
import os
import tempfile
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_ici'  # Changez cette clé en production

# Configuration pour les fichiers uploadés
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

# Créer le dossier uploads s'il n'existe pas
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Vérifie si le fichier a une extension autorisée"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def charger_mots_cles(fichier_keywords):
    """Charge les mots-clés depuis le fichier CSV"""
    try:
        df_keywords = pd.read_csv(fichier_keywords)
        
        # Extraire tous les mots-clés
        if 'keyword' in df_keywords.columns:
            mots_cles = df_keywords['keyword'].tolist()
        else:
            mots_cles = df_keywords.iloc[:, 0].tolist()
        
        # Nettoyer et convertir en minuscules
        mots_cles_clean = set()
        for mot in mots_cles:
            if pd.notna(mot):
                mot_clean = str(mot).strip().lower()
                if mot_clean:
                    mots_cles_clean.add(mot_clean)
        
        return mots_cles_clean
        
    except Exception as e:
        print(f"Erreur lors du chargement des mots-clés: {e}")
        return set()

def contient_mots_cles(texte, mots_cles):
    """Vérifie si un texte contient au moins un des mots-clés"""
    if pd.isna(texte) or not isinstance(texte, str):
        return False
    
    texte_clean = str(texte).lower()
    
    for mot_cle in mots_cles:
        if mot_cle in texte_clean:
            return True
    
    return False

def filtrer_videos(fichier_data, fichier_keywords):
    """Filtre les vidéos en fonction des mots-clés"""
    # Charger les mots-clés
    mots_cles = charger_mots_cles(fichier_keywords)
    if not mots_cles:
        return None, "Aucun mot-clé valide trouvé dans le fichier keywords.csv"
    
    # Charger les données des vidéos
    try:
        df_data = pd.read_csv(fichier_data)
    except Exception as e:
        return None, f"Erreur lors du chargement des données: {e}"
    
    # Créer une copie du DataFrame
    df_resultat = df_data.copy()
    df_resultat['decision'] = 'Rejeté'  # Par défaut, toutes les vidéos sont rejetées
    
    # Compter les vidéos gardées et rejetées
    gardees = 0
    rejetees = 0
    
    # Analyser chaque vidéo
    for index, row in df_data.iterrows():
        titre = row.get('title', '')
        channel_name = row.get('channelName', '')
        
        # Combiner titre et nom de chaîne pour l'analyse
        texte_analyse = f"{titre} {channel_name}"
        
        if contient_mots_cles(texte_analyse, mots_cles):
            df_resultat.at[index, 'decision'] = 'Gardé'
            gardees += 1
        else:
            rejetees += 1
    
    return df_resultat, {
        'gardees': gardees,
        'rejetees': rejetees,
        'total': len(df_data),
        'mots_cles': len(mots_cles)
    }

@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """Traite l'upload des fichiers et effectue le filtrage"""
    if 'data_file' not in request.files or 'keywords_file' not in request.files:
        flash('Veuillez sélectionner les deux fichiers CSV', 'error')
        return redirect(url_for('index'))
    
    data_file = request.files['data_file']
    keywords_file = request.files['keywords_file']
    
    if data_file.filename == '' or keywords_file.filename == '':
        flash('Veuillez sélectionner les deux fichiers CSV', 'error')
        return redirect(url_for('index'))
    
    if not (allowed_file(data_file.filename) and allowed_file(keywords_file.filename)):
        flash('Seuls les fichiers CSV sont autorisés', 'error')
        return redirect(url_for('index'))
    
    try:
        # Sauvegarder les fichiers temporairement
        data_filename = secure_filename(data_file.filename)
        keywords_filename = secure_filename(keywords_file.filename)
        
        data_path = os.path.join(UPLOAD_FOLDER, data_filename)
        keywords_path = os.path.join(UPLOAD_FOLDER, keywords_filename)
        
        data_file.save(data_path)
        keywords_file.save(keywords_path)
        
        # Effectuer le filtrage
        resultat, stats = filtrer_videos(data_path, keywords_path)
        
        if resultat is None:
            flash(f"Erreur lors du filtrage: {stats}", 'error')
            return redirect(url_for('index'))
        
        # Sauvegarder le résultat
        output_filename = 'videos_filtrees.csv'
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        resultat.to_csv(output_path, index=False, encoding='utf-8')
        
        # Nettoyer les fichiers temporaires
        os.remove(data_path)
        os.remove(keywords_path)
        
        # Stocker les statistiques dans la session
        session_stats = {
            'gardees': stats['gardees'],
            'rejetees': stats['rejetees'],
            'total': stats['total'],
            'mots_cles': stats['mots_cles'],
            'taux_conservation': round((stats['gardees'] / stats['total'] * 100), 1) if stats['total'] > 0 else 0
        }
        
        flash('Filtrage terminé avec succès !', 'success')
        return render_template('result.html', stats=session_stats, output_file=output_filename)
        
    except Exception as e:
        flash(f'Erreur lors du traitement: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    """Télécharge le fichier filtré"""
    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            flash('Fichier non trouvé', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Erreur lors du téléchargement: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/cleanup')
def cleanup():
    """Nettoie les fichiers temporaires"""
    try:
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        flash('Fichiers temporaires nettoyés', 'info')
    except Exception as e:
        flash(f'Erreur lors du nettoyage: {str(e)}', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

