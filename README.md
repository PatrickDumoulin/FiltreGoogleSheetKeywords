# Filtreur de Vidéos par Mots-Clés

Ce programme filtre les vidéos d'un fichier CSV en fonction de mots-clés spécifiés dans un autre fichier CSV. Il est disponible en version ligne de commande et avec une interface web moderne.

## Fonctionnalités

- **Interface Web Moderne** : Upload de fichiers par glisser-déposer
- **Filtrage Intelligent** : Analyse du titre et du nom de la chaîne
- **Statistiques Détaillées** : Taux de conservation et compteurs
- **Téléchargement Direct** : Fichier CSV filtré prêt à utiliser
- **Version Ligne de Commande** : Pour l'automatisation

## Installation

1. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### 🌐 Interface Web (Recommandée)

1. Démarrez l'application web :
```bash
python run_app.py
```

2. Ouvrez votre navigateur sur `http://localhost:5000`

3. Glissez-déposez vos fichiers `Data.csv` et `keywords.csv`

4. Cliquez sur "Filtrer les Vidéos"

5. Téléchargez le fichier `videos_filtrees.csv` généré

### 💻 Version Ligne de Commande

1. Placez vos fichiers `Data.csv` et `keywords.csv` dans le même répertoire
2. Exécutez le programme :
```bash
python filtre_videos.py
```

## Format des fichiers

### Data.csv
Le fichier doit contenir les colonnes suivantes :
- title : Titre de la vidéo
- id : Identifiant de la vidéo
- url : URL de la vidéo
- viewcount : Nombre de vues
- date : Date de publication
- channelName : Nom de la chaîne
- channelUrl : URL de la chaîne
- numberOfSubscribers : Nombre d'abonnés
- duration : Durée en secondes

### keywords.csv
Le fichier doit contenir une colonne `keyword` avec les mots-clés à rechercher.

## Résultat

Le programme génère un fichier `videos_filtrees.csv` contenant toutes les données originales plus une colonne `decision` indiquant si la vidéo doit être gardée ou rejetée.

## Exemple

Avec les fichiers d'exemple fournis, le programme identifiera les vidéos liées à la programmation et au développement web comme "Gardé" et les autres comme "Rejeté".
