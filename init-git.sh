#!/bin/bash
# Script d'initialisation Git pour le déploiement Vercel

echo "🚀 Initialisation Git pour le déploiement Vercel"
echo "================================================"

# Vérifier si Git est installé
if ! command -v git &> /dev/null; then
    echo "❌ Git n'est pas installé. Veuillez installer Git d'abord."
    exit 1
fi

# Initialiser Git si ce n'est pas déjà fait
if [ ! -d ".git" ]; then
    echo "📁 Initialisation du repository Git..."
    git init
else
    echo "✅ Repository Git déjà initialisé"
fi

# Ajouter tous les fichiers
echo "📝 Ajout des fichiers..."
git add .

# Créer le commit initial
echo "💾 Création du commit initial..."
git commit -m "Initial commit: Filtreur de vidéos par mots-clés avec interface Vercel"

echo ""
echo "✅ Repository Git initialisé avec succès !"
echo ""
echo "📋 Prochaines étapes :"
echo "1. Créez un repository sur GitHub"
echo "2. Connectez votre repository local :"
echo "   git remote add origin https://github.com/VOTRE-USERNAME/FiltreGoogleSheetKeywords.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Déployez sur Vercel :"
echo "   - Allez sur vercel.com"
echo "   - Connectez votre compte GitHub"
echo "   - Importez le repository"
echo "   - Déployez !"
echo ""
echo "📖 Consultez deploy-github.md pour les instructions détaillées"
