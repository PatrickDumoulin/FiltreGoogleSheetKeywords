# 🎬 Démonstration - Interface Web de Filtrage de Vidéos

## 🚀 Démarrage Rapide

1. **Démarrez l'application** :
   ```bash
   python run_app.py
   ```

2. **Ouvrez votre navigateur** sur : `http://localhost:5000`

## 📋 Étapes d'utilisation

### 1. Page d'Accueil
- Interface moderne avec drag & drop
- Deux zones d'upload pour vos fichiers CSV
- Instructions détaillées

### 2. Upload des Fichiers
- **Data.csv** : Vos données de vidéos
- **keywords.csv** : Liste des mots-clés
- Glissez-déposez ou cliquez pour sélectionner

### 3. Traitement
- Filtrage automatique en arrière-plan
- Barre de progression
- Messages d'état

### 4. Résultats
- **Statistiques visuelles** :
  - Nombre total de vidéos
  - Vidéos gardées (vert)
  - Vidéos rejetées (orange)
  - Taux de conservation (bleu)
- **Téléchargement direct** du fichier filtré

## 🎯 Fonctionnalités Avancées

### Interface Responsive
- Design adaptatif pour mobile/desktop
- Navigation intuitive
- Feedback visuel en temps réel

### Gestion des Erreurs
- Messages d'erreur clairs
- Validation des fichiers
- Nettoyage automatique

### Sécurité
- Validation des types de fichiers
- Noms de fichiers sécurisés
- Nettoyage des fichiers temporaires

## 📊 Exemple de Résultats

```
Vidéos analysées : 1000
Vidéos gardées : 250
Vidéos rejetées : 750
Taux de conservation : 25%
Mots-clés utilisés : 15
```

## 🔧 Personnalisation

L'interface peut être facilement personnalisée en modifiant :
- `templates/base.html` : Design général
- `templates/index.html` : Page d'accueil
- `templates/result.html` : Page de résultats
- `app.py` : Logique métier

## 🆘 Support

En cas de problème :
1. Vérifiez que les fichiers CSV sont au bon format
2. Assurez-vous que les colonnes attendues sont présentes
3. Consultez les messages d'erreur dans l'interface
4. Redémarrez l'application si nécessaire

