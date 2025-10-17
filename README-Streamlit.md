# 🎬 Filtreur de Vidéos par Mots-Clés - Version Streamlit

Application Streamlit pour filtrer des vidéos en fonction de mots-clés spécifiques.

## 🚀 Déploiement sur Streamlit Cloud

### Méthode 1 : Déploiement Direct
1. Allez sur [share.streamlit.io](https://share.streamlit.io)
2. Connectez votre compte GitHub
3. Sélectionnez ce repository
4. Fichier principal : `streamlit_app.py`
5. Déployez !

### Méthode 2 : Déploiement Local
```bash
# Installer les dépendances
pip install -r requirements-streamlit.txt

# Lancer l'application
streamlit run streamlit_app.py
```

## 📋 Utilisation

1. **Uploadez Data.csv** : Fichier contenant vos données de vidéos
2. **Uploadez keywords.csv** : Fichier contenant la liste des mots-clés
3. **Cliquez sur "Filtrer les Vidéos"**
4. **Téléchargez le résultat** : Fichier CSV filtré

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

## ✨ Fonctionnalités

- 🌐 **Interface intuitive** avec drag & drop
- 📊 **Statistiques visuelles** en temps réel
- 🔍 **Filtres avancés** par décision
- 📥 **Téléchargement multiple** (tous, gardés, rejetés)
- 📱 **Design responsive** (mobile/desktop)
- 🎨 **Thème personnalisé** Streamlit

## 🛠️ Technologies

- **Streamlit** : Interface utilisateur
- **Pandas** : Traitement des données CSV
- **Python 3.8+** : Langage principal

## 📊 Exemple de Résultats

```
📊 Total : 1000 vidéos
✅ Gardées : 250 vidéos (25.0%)
❌ Rejetées : 750 vidéos (75.0%)
🔑 Mots-clés : 15 utilisés
```

## 🔧 Configuration

Le fichier `.streamlit/config.toml` contient :
- Thème personnalisé
- Configuration serveur
- Paramètres de sécurité

## 🆘 Support

En cas de problème :
1. Vérifiez le format de vos fichiers CSV
2. Assurez-vous que les colonnes attendues sont présentes
3. Consultez les logs Streamlit Cloud

---

**🎉 Déployez facilement sur Streamlit Cloud !** 🚀
