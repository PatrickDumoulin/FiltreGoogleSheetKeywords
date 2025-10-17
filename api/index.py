#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API serverless pour Vercel - Filtreur de vidéos par mots-clés
"""

from flask import Flask, request, jsonify
import pandas as pd
import tempfile
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration pour Vercel
UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    """Vérifie si le fichier a une extension autorisée"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def charger_mots_cles(fichier_keywords):
    """Charge les mots-clés depuis le fichier CSV"""
    try:
        df_keywords = pd.read_csv(fichier_keywords)
        
        if 'keyword' in df_keywords.columns:
            mots_cles = df_keywords['keyword'].tolist()
        else:
            mots_cles = df_keywords.iloc[:, 0].tolist()
        
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

def filtrer_videos(data_content, keywords_content):
    """Filtre les vidéos en fonction des mots-clés"""
    try:
        # Charger les mots-clés
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(keywords_content)
            keywords_path = f.name
        
        mots_cles = charger_mots_cles(keywords_path)
        os.unlink(keywords_path)
        
        if not mots_cles:
            return None, "Aucun mot-clé valide trouvé"
        
        # Charger les données des vidéos
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(data_content)
            data_path = f.name
        
        df_data = pd.read_csv(data_path)
        os.unlink(data_path)
        
        # Créer une copie du DataFrame
        df_resultat = df_data.copy()
        df_resultat['decision'] = 'Rejeté'
        
        gardees = 0
        rejetees = 0
        
        # Analyser chaque vidéo
        for index, row in df_data.iterrows():
            titre = row.get('title', '')
            channel_name = row.get('channelName', '')
            
            texte_analyse = f"{titre} {channel_name}"
            
            if contient_mots_cles(texte_analyse, mots_cles):
                df_resultat.at[index, 'decision'] = 'Gardé'
                gardees += 1
            else:
                rejetees += 1
        
        # Convertir en CSV
        csv_result = df_resultat.to_csv(index=False, encoding='utf-8')
        
        return csv_result, {
            'gardees': gardees,
            'rejetees': rejetees,
            'total': len(df_data),
            'mots_cles': len(mots_cles)
        }
        
    except Exception as e:
        return None, f"Erreur lors du filtrage: {str(e)}"

@app.route('/')
def index():
    """Page d'accueil - redirige vers l'interface statique"""
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Filtreur de Vidéos par Mots-Clés</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            .upload-area {
                border: 2px dashed #dee2e6;
                border-radius: 10px;
                padding: 2rem;
                text-align: center;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            .upload-area:hover {
                border-color: #0d6efd;
                background-color: #f8f9fa;
            }
            .upload-area.dragover {
                border-color: #0d6efd;
                background-color: #e7f1ff;
            }
            .file-info {
                background-color: #f8f9fa;
                border-radius: 5px;
                padding: 0.5rem;
                margin-top: 0.5rem;
            }
            .stats-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 15px;
            }
            .btn-custom {
                background: linear-gradient(45deg, #667eea, #764ba2);
                border: none;
                color: white;
                transition: transform 0.2s;
            }
            .btn-custom:hover {
                transform: translateY(-2px);
                color: white;
            }
        </style>
    </head>
    <body class="bg-light">
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand" href="/">
                    <i class="fas fa-video me-2"></i>
                    Filtreur de Vidéos
                </a>
            </div>
        </nav>

        <div class="container mt-4">
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <div class="card shadow">
                        <div class="card-header bg-primary text-white">
                            <h2 class="card-title mb-0">
                                <i class="fas fa-upload me-2"></i>
                                Import de Fichiers CSV
                            </h2>
                        </div>
                        <div class="card-body p-4">
                            <form id="uploadForm" enctype="multipart/form-data">
                                <div class="row">
                                    <div class="col-md-6 mb-4">
                                        <label class="form-label fw-bold">
                                            <i class="fas fa-database me-2 text-primary"></i>
                                            Fichier Data.csv
                                        </label>
                                        <div class="upload-area" id="dataUploadArea">
                                            <i class="fas fa-cloud-upload-alt fa-3x text-muted mb-3"></i>
                                            <p class="mb-2">Glissez-déposez votre fichier Data.csv ici</p>
                                            <p class="text-muted small">ou cliquez pour sélectionner</p>
                                            <input type="file" name="data_file" class="d-none" accept=".csv" required>
                                            <div class="file-info" style="display: none;"></div>
                                        </div>
                                    </div>

                                    <div class="col-md-6 mb-4">
                                        <label class="form-label fw-bold">
                                            <i class="fas fa-key me-2 text-success"></i>
                                            Fichier keywords.csv
                                        </label>
                                        <div class="upload-area" id="keywordsUploadArea">
                                            <i class="fas fa-cloud-upload-alt fa-3x text-muted mb-3"></i>
                                            <p class="mb-2">Glissez-déposez votre fichier keywords.csv ici</p>
                                            <p class="text-muted small">ou cliquez pour sélectionner</p>
                                            <input type="file" name="keywords_file" class="d-none" accept=".csv" required>
                                            <div class="file-info" style="display: none;"></div>
                                        </div>
                                    </div>
                                </div>

                                <div class="text-center">
                                    <button type="submit" class="btn btn-custom btn-lg px-5" id="submitBtn">
                                        <i class="fas fa-magic me-2"></i>
                                        Filtrer les Vidéos
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>

                    <div id="results" class="mt-4" style="display: none;">
                        <div class="card stats-card">
                            <div class="card-body text-center">
                                <h2 class="card-title mb-4">
                                    <i class="fas fa-chart-bar me-2"></i>
                                    Résultats du Filtrage
                                </h2>
                                <div class="row">
                                    <div class="col-md-3">
                                        <div class="mb-3">
                                            <h3 class="display-4 fw-bold" id="total">0</h3>
                                            <p class="mb-0">Vidéos analysées</p>
                                        </div>
                                    </div>
                                    <div class="col-md-3">
                                        <div class="mb-3">
                                            <h3 class="display-4 fw-bold text-success" id="gardees">0</h3>
                                            <p class="mb-0">Vidéos gardées</p>
                                        </div>
                                    </div>
                                    <div class="col-md-3">
                                        <div class="mb-3">
                                            <h3 class="display-4 fw-bold text-warning" id="rejetees">0</h3>
                                            <p class="mb-0">Vidéos rejetées</p>
                                        </div>
                                    </div>
                                    <div class="col-md-3">
                                        <div class="mb-3">
                                            <h3 class="display-4 fw-bold text-info" id="taux">0%</h3>
                                            <p class="mb-0">Taux de conservation</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="card mt-4">
                            <div class="card-body text-center">
                                <h4 class="card-title mb-4">
                                    <i class="fas fa-download me-2"></i>
                                    Télécharger le Fichier Filtré
                                </h4>
                                <button class="btn btn-success btn-lg px-5" id="downloadBtn">
                                    <i class="fas fa-download me-2"></i>
                                    Télécharger videos_filtrees.csv
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            let csvData = null;
            
            // Gestion du drag & drop
            const uploadAreas = document.querySelectorAll('.upload-area');
            
            uploadAreas.forEach(area => {
                area.addEventListener('dragover', (e) => {
                    e.preventDefault();
                    area.classList.add('dragover');
                });
                
                area.addEventListener('dragleave', () => {
                    area.classList.remove('dragover');
                });
                
                area.addEventListener('drop', (e) => {
                    e.preventDefault();
                    area.classList.remove('dragover');
                    
                    const files = e.dataTransfer.files;
                    const input = area.querySelector('input[type="file"]');
                    if (input && files.length > 0) {
                        input.files = files;
                        updateFileInfo(input);
                    }
                });
                
                area.addEventListener('click', () => {
                    const input = area.querySelector('input[type="file"]');
                    if (input) input.click();
                });
            });
            
            function updateFileInfo(input) {
                const fileInfo = input.parentNode.querySelector('.file-info');
                if (input.files.length > 0) {
                    const file = input.files[0];
                    fileInfo.innerHTML = `
                        <i class="fas fa-file-csv text-success me-2"></i>
                        <strong>${file.name}</strong> (${(file.size / 1024).toFixed(1)} KB)
                    `;
                    fileInfo.style.display = 'block';
                } else {
                    fileInfo.style.display = 'none';
                }
            }
            
            document.querySelectorAll('input[type="file"]').forEach(input => {
                input.addEventListener('change', () => updateFileInfo(input));
            });
            
            // Gestion du formulaire
            document.getElementById('uploadForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const submitBtn = document.getElementById('submitBtn');
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Traitement en cours...';
                submitBtn.disabled = true;
                
                const formData = new FormData();
                const dataFile = document.querySelector('input[name="data_file"]').files[0];
                const keywordsFile = document.querySelector('input[name="keywords_file"]').files[0];
                
                if (!dataFile || !keywordsFile) {
                    alert('Veuillez sélectionner les deux fichiers CSV');
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                    return;
                }
                
                formData.append('data_file', dataFile);
                formData.append('keywords_file', keywordsFile);
                
                try {
                    const response = await fetch('/api/filter', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        csvData = result.csv_data;
                        showResults(result.stats);
                    } else {
                        alert('Erreur: ' + result.error);
                    }
                } catch (error) {
                    alert('Erreur lors du traitement: ' + error.message);
                }
                
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            });
            
            function showResults(stats) {
                document.getElementById('total').textContent = stats.total;
                document.getElementById('gardees').textContent = stats.gardees;
                document.getElementById('rejetees').textContent = stats.rejetees;
                document.getElementById('taux').textContent = stats.taux_conservation + '%';
                
                document.getElementById('results').style.display = 'block';
                document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
            }
            
            // Téléchargement
            document.getElementById('downloadBtn').addEventListener('click', () => {
                if (csvData) {
                    const blob = new Blob([csvData], { type: 'text/csv' });
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'videos_filtrees.csv';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);
                }
            });
        </script>
    </body>
    </html>
    """

@app.route('/api/filter', methods=['POST'])
def filter_videos():
    """API endpoint pour filtrer les vidéos"""
    try:
        if 'data_file' not in request.files or 'keywords_file' not in request.files:
            return jsonify({'success': False, 'error': 'Veuillez sélectionner les deux fichiers CSV'})
        
        data_file = request.files['data_file']
        keywords_file = request.files['keywords_file']
        
        if data_file.filename == '' or keywords_file.filename == '':
            return jsonify({'success': False, 'error': 'Veuillez sélectionner les deux fichiers CSV'})
        
        if not (allowed_file(data_file.filename) and allowed_file(keywords_file.filename)):
            return jsonify({'success': False, 'error': 'Seuls les fichiers CSV sont autorisés'})
        
        # Lire le contenu des fichiers
        data_content = data_file.read().decode('utf-8')
        keywords_content = keywords_file.read().decode('utf-8')
        
        # Effectuer le filtrage
        csv_result, stats = filtrer_videos(data_content, keywords_content)
        
        if csv_result is None:
            return jsonify({'success': False, 'error': stats})
        
        # Calculer le taux de conservation
        taux_conservation = round((stats['gardees'] / stats['total'] * 100), 1) if stats['total'] > 0 else 0
        
        return jsonify({
            'success': True,
            'csv_data': csv_result,
            'stats': {
                'total': stats['total'],
                'gardees': stats['gardees'],
                'rejetees': stats['rejetees'],
                'mots_cles': stats['mots_cles'],
                'taux_conservation': taux_conservation
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erreur lors du traitement: {str(e)}'})

# Handler pour Vercel
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    app.run(debug=True)
