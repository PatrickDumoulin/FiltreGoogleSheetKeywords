# 📖 Guide d'Utilisation - Filtreur de Vidéos par Mots-Clés

## 🎯 Vue d'ensemble

Cette application vous permet de filtrer des vidéos en fonction de mots-clés spécifiques. Elle est disponible en deux versions :
- **Interface Web** : Interface moderne avec drag & drop
- **Ligne de Commande** : Pour l'automatisation

## 🚀 Installation Rapide

### Méthode 1 : Script de Déploiement (Recommandée)
```bash
python deploy.py
```

### Méthode 2 : Installation Manuelle
```bash
pip install -r requirements.txt
```

## 🌐 Utilisation de l'Interface Web

### 1. Démarrage
```bash
python run_app.py
```

### 2. Accès
Ouvrez votre navigateur sur : `http://localhost:5000`

### 3. Upload des Fichiers
- **Glissez-déposez** vos fichiers CSV dans les zones prévues
- **Ou cliquez** pour sélectionner les fichiers
- **Data.csv** : Vos données de vidéos
- **keywords.csv** : Liste des mots-clés

### 4. Filtrage
- Cliquez sur "Filtrer les Vidéos"
- Attendez le traitement (barre de progression)
- Consultez les statistiques

### 5. Téléchargement
- Cliquez sur "Télécharger videos_filtrees.csv"
- Le fichier contient toutes les données + colonne "decision"

## 💻 Utilisation en Ligne de Commande

### 1. Préparation
Placez vos fichiers dans le répertoire :
- `Data.csv`
- `keywords.csv`

### 2. Exécution
```bash
python filtre_videos.py
```

### 3. Résultat
Le fichier `videos_filtrees.csv` est généré automatiquement.

## 📋 Format des Fichiers

### Data.csv
Colonnes requises :
```
title,id,url,viewcount,date,channelName,channelUrl,numberOfSubscribers,duration
```

### keywords.csv
Colonnes requises :
```
keyword
```

## 🔧 Fonctionnalités Avancées

### Interface Web
- **Drag & Drop** : Glissez-déposez vos fichiers
- **Validation** : Vérification automatique des formats
- **Statistiques** : Graphiques et compteurs en temps réel
- **Responsive** : Compatible mobile et desktop
- **Sécurité** : Validation des types de fichiers

### Ligne de Commande
- **Automatisation** : Intégration dans des scripts
- **Logs détaillés** : Informations de traitement
- **Gestion d'erreurs** : Messages d'erreur clairs

## 📊 Exemple de Résultats

```
Vidéos analysées : 1000
Vidéos gardées : 250
Vidéos rejetées : 750
Taux de conservation : 25%
Mots-clés utilisés : 15
```

## 🛠️ Dépannage

### Problèmes Courants

#### 1. Erreur "Module not found"
```bash
pip install -r requirements.txt
```

#### 2. Port 5000 occupé
Modifiez le port dans `run_app.py` :
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

#### 3. Fichiers CSV invalides
- Vérifiez les noms des colonnes
- Assurez-vous que les fichiers sont au format CSV
- Vérifiez l'encodage (UTF-8 recommandé)

#### 4. Aucune vidéo gardée
- Vérifiez vos mots-clés
- Assurez-vous qu'ils correspondent aux titres/chaînes
- La recherche est insensible à la casse

### Logs et Debug
- **Interface Web** : Messages dans la console
- **Ligne de Commande** : Affichage détaillé des étapes

## 🔒 Sécurité

- Validation des types de fichiers
- Noms de fichiers sécurisés
- Nettoyage automatique des fichiers temporaires
- Limitation de la taille des fichiers (16MB)

## 📁 Structure du Projet

```
FiltreGoogleSheetKeywords/
├── app.py                 # Application Flask
├── run_app.py            # Script de démarrage
├── filtre_videos.py      # Version ligne de commande
├── deploy.py             # Script de déploiement
├── test_interface.py     # Tests
├── config.py             # Configuration
├── requirements.txt      # Dépendances
├── templates/            # Templates HTML
│   ├── base.html
│   ├── index.html
│   └── result.html
├── uploads/              # Fichiers temporaires
└── README.md             # Documentation
```

## 🆘 Support

En cas de problème :
1. Consultez ce guide
2. Vérifiez les logs d'erreur
3. Testez avec les fichiers d'exemple fournis
4. Redémarrez l'application

## 📈 Améliorations Futures

- Support de plus de formats de fichiers
- Filtrage par critères multiples
- Export vers différents formats
- Interface d'administration
- API REST

