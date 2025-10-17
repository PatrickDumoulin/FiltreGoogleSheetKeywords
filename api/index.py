#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API serverless ultra-simple pour Vercel - Test de base
"""

import json

def handler(request):
    """Handler principal pour Vercel - Version de test"""
    try:
        # Headers CORS
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'application/json'
        }
        
        # Gestion des requêtes OPTIONS (CORS preflight)
        if request.method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        # Route principale - Page d'accueil
        if request.path == '/' or request.path == '':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'text/html'},
                'body': get_homepage_html()
            }
        
        # Route API de test
        elif request.path == '/api/test':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'success': True,
                    'message': 'API fonctionne correctement !',
                    'path': request.path,
                    'method': request.method
                })
            }
        
        # Route par défaut
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Not found'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': f'Internal server error: {str(e)}'})
        }

def get_homepage_html():
    """Retourne le HTML de la page d'accueil"""
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Filtreur de Vidéos - Test Vercel</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .hero {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 4rem 0;
            }
        </style>
    </head>
    <body>
        <div class="hero">
            <div class="container text-center">
                <h1 class="display-4 mb-4">
                    <i class="fas fa-video me-3"></i>
                    Filtreur de Vidéos
                </h1>
                <p class="lead mb-4">Test de déploiement Vercel</p>
                <button class="btn btn-light btn-lg" onclick="testAPI()">
                    Tester l'API
                </button>
            </div>
        </div>
        
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">Test de l'API</h5>
                        </div>
                        <div class="card-body">
                            <div id="result" class="alert alert-info" style="display: none;">
                                <strong>Résultat :</strong> <span id="resultText"></span>
                            </div>
                            <p>Cliquez sur le bouton "Tester l'API" pour vérifier que l'API fonctionne.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            async function testAPI() {
                try {
                    const response = await fetch('/api/test');
                    const data = await response.json();
                    
                    document.getElementById('resultText').textContent = JSON.stringify(data, null, 2);
                    document.getElementById('result').style.display = 'block';
                } catch (error) {
                    document.getElementById('resultText').textContent = 'Erreur: ' + error.message;
                    document.getElementById('result').style.display = 'block';
                }
            }
        </script>
    </body>
    </html>
    """