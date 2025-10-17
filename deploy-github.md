# 🚀 Guide de Déploiement sur Vercel via GitHub

## 📋 Étapes de Déploiement

### 1. Préparer le Repository GitHub

#### A. Créer un nouveau repository sur GitHub
1. Allez sur [GitHub.com](https://github.com)
2. Cliquez sur "New repository"
3. Nom : `FiltreGoogleSheetKeywords`
4. Description : "Filtreur de vidéos par mots-clés avec interface web"
5. Cochez "Public" ou "Private" selon vos préférences
6. **Ne cochez PAS** "Initialize with README" (nous avons déjà nos fichiers)
7. Cliquez sur "Create repository"

#### B. Initialiser Git localement
```bash
# Dans le dossier de votre projet
git init
git add .
git commit -m "Initial commit: Filtreur de vidéos par mots-clés"
```

#### C. Connecter au repository GitHub
```bash
# Remplacez VOTRE-USERNAME par votre nom d'utilisateur GitHub
git remote add origin https://github.com/VOTRE-USERNAME/FiltreGoogleSheetKeywords.git
git branch -M main
git push -u origin main
```

### 2. Déployer sur Vercel

#### A. Créer un compte Vercel
1. Allez sur [Vercel.com](https://vercel.com)
2. Cliquez sur "Sign Up"
3. Choisissez "Continue with GitHub"
4. Autorisez Vercel à accéder à vos repositories

#### B. Importer le projet
1. Dans le dashboard Vercel, cliquez sur "New Project"
2. Sélectionnez votre repository `FiltreGoogleSheetKeywords`
3. Vercel détectera automatiquement que c'est un projet Python
4. Cliquez sur "Deploy"

#### C. Configuration automatique
Vercel va automatiquement :
- Détecter le fichier `vercel.json`
- Installer les dépendances depuis `requirements-vercel.txt`
- Déployer l'API serverless dans `/api/index.py`

### 3. Vérifier le Déploiement

#### A. Accéder à votre application
1. Une fois le déploiement terminé, Vercel vous donnera une URL
2. Exemple : `https://filtre-google-sheet-keywords.vercel.app`
3. Ouvrez cette URL dans votre navigateur

#### B. Tester l'interface
1. Glissez-déposez vos fichiers CSV
2. Testez le filtrage
3. Vérifiez le téléchargement

## 🔧 Configuration Avancée

### Variables d'Environnement (si nécessaire)
Dans le dashboard Vercel :
1. Allez dans "Settings" > "Environment Variables"
2. Ajoutez les variables si nécessaire :
   - `SECRET_KEY` : Clé secrète pour Flask
   - `MAX_FILE_SIZE` : Taille maximale des fichiers

### Domaine Personnalisé
1. Dans "Settings" > "Domains"
2. Ajoutez votre domaine personnalisé
3. Configurez les DNS selon les instructions Vercel

## 📊 Monitoring et Logs

### Vercel Analytics
- Accédez aux métriques dans le dashboard Vercel
- Surveillez les performances et l'utilisation

### Logs de Débogage
- Allez dans "Functions" > "View Function Logs"
- Consultez les logs en temps réel

## 🚨 Dépannage

### Problèmes Courants

#### 1. Erreur de Build
```bash
# Vérifiez que requirements-vercel.txt contient les bonnes versions
Flask==3.1.2
pandas==2.3.3
Werkzeug==3.1.3
```

#### 2. Erreur 500
- Vérifiez les logs dans Vercel
- Assurez-vous que l'API fonctionne localement

#### 3. Timeout
- Vercel a une limite de 30 secondes pour les fonctions
- Pour des fichiers très volumineux, considérez une approche différente

### Redéploiement
```bash
# Après modification du code
git add .
git commit -m "Update: description des changements"
git push origin main
# Vercel redéploiera automatiquement
```

## 📈 Optimisations

### Performance
- Les fichiers sont traités en mémoire (pas de stockage permanent)
- Utilisez des fichiers CSV de taille raisonnable (< 10MB)

### Coûts
- Vercel offre un plan gratuit généreux
- Payez seulement si vous dépassez les limites

## 🔒 Sécurité

### Bonnes Pratiques
- Ne stockez pas de données sensibles dans le code
- Utilisez des variables d'environnement pour les secrets
- Validez toujours les fichiers uploadés

### Limites Vercel
- Taille maximale des fichiers : 50MB
- Timeout des fonctions : 30 secondes
- Requêtes simultanées : 1000/minute

## 📞 Support

### Vercel
- [Documentation Vercel](https://vercel.com/docs)
- [Support Vercel](https://vercel.com/support)

### GitHub
- [Documentation GitHub](https://docs.github.com)
- [GitHub Support](https://support.github.com)

---

## 🎉 Félicitations !

Votre application est maintenant déployée sur Vercel et accessible depuis n'importe où dans le monde ! 🌍

**URL de votre application :** `https://votre-projet.vercel.app`
