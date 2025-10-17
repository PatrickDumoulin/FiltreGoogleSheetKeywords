# 🎬 Filtreur de Vidéos par Mots-Clés

Une application web moderne pour filtrer des vidéos en fonction de mots-clés spécifiques. Disponible en version locale et déployable sur Vercel.

## ✨ Fonctionnalités

- 🌐 **Interface Web Moderne** avec drag & drop
- 📊 **Statistiques Visuelles** en temps réel
- 💻 **Version Ligne de Commande** pour l'automatisation
- 🚀 **Déploiement Vercel** prêt à l'emploi
- 📱 **Design Responsive** (mobile/desktop)

## 🚀 Déploiement Rapide sur Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/VOTRE-USERNAME/FiltreGoogleSheetKeywords)

### Étapes de Déploiement

1. **Fork ce repository** sur GitHub
2. **Connectez votre compte Vercel** à GitHub
3. **Importez le projet** depuis GitHub
4. **Déployez** en un clic !

## 🛠️ Installation Locale

### Prérequis
- Python 3.8+
- pip

### Installation
```bash
# Cloner le repository
git clone https://github.com/VOTRE-USERNAME/FiltreGoogleSheetKeywords.git
cd FiltreGoogleSheetKeywords

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python run_app.py
```

### Accès
Ouvrez votre navigateur sur : `http://localhost:5000`

## 📋 Utilisation

### Interface Web
1. **Glissez-déposez** vos fichiers CSV :
   - `Data.csv` : Données de vos vidéos
   - `keywords.csv` : Liste des mots-clés
2. **Cliquez** sur "Filtrer les Vidéos"
3. **Téléchargez** le fichier filtré

### Ligne de Commande
```bash
python filtre_videos.py
```

## 📁 Format des Fichiers

### Data.csv
```csv
title,id,url,viewcount,date,channelName,channelUrl,numberOfSubscribers,duration
"Titre de la vidéo",vid001,https://...,15000,2024-01-15,Chaîne,https://...,50000,1200
```

### keywords.csv
```csv
keyword
programming
tutoriel
javascript
python
```

## 🏗️ Structure du Projet

```
FiltreGoogleSheetKeywords/
├── api/
│   └── index.py              # API Vercel (serverless)
├── templates/                # Templates HTML
├── app.py                    # Application Flask locale
├── filtre_videos.py          # Version ligne de commande
├── run_app.py               # Script de démarrage
├── vercel.json              # Configuration Vercel
├── requirements.txt         # Dépendances locales
├── requirements-vercel.txt  # Dépendances Vercel
└── README.md               # Documentation
```

## 🔧 Configuration

### Variables d'Environnement (Vercel)
Aucune configuration supplémentaire requise !

### Configuration Locale
Modifiez `config.py` pour personnaliser :
- Port d'écoute
- Taille maximale des fichiers
- Messages d'interface

## 📊 Exemple de Résultats

```
Vidéos analysées : 1000
Vidéos gardées : 250
Vidéos rejetées : 750
Taux de conservation : 25%
Mots-clés utilisés : 15
```

## 🛡️ Sécurité

- ✅ Validation des types de fichiers
- ✅ Noms de fichiers sécurisés
- ✅ Limitation de taille (16MB)
- ✅ Nettoyage automatique des fichiers temporaires

## 🚀 Technologies

- **Backend** : Python, Flask, Pandas
- **Frontend** : HTML5, CSS3, JavaScript, Bootstrap 5
- **Déploiement** : Vercel (serverless)
- **Version Control** : Git, GitHub

## 📈 Performance

- **Traitement rapide** des fichiers CSV
- **Interface réactive** avec feedback en temps réel
- **Serverless** : Mise à l'échelle automatique
- **CDN global** : Chargement rapide partout

## 🤝 Contribution

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

- 📧 **Email** : votre-email@example.com
- 🐛 **Issues** : [GitHub Issues](https://github.com/VOTRE-USERNAME/FiltreGoogleSheetKeywords/issues)
- 📖 **Documentation** : [Wiki](https://github.com/VOTRE-USERNAME/FiltreGoogleSheetKeywords/wiki)

## 🙏 Remerciements

- [Flask](https://flask.palletsprojects.com/) - Framework web
- [Pandas](https://pandas.pydata.org/) - Manipulation de données
- [Bootstrap](https://getbootstrap.com/) - Framework CSS
- [Vercel](https://vercel.com/) - Plateforme de déploiement

---

⭐ **N'oubliez pas de donner une étoile si ce projet vous a aidé !** ⭐
