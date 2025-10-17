#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programme de filtrage de vidéos basé sur des mots-clés
Filtre les vidéos du fichier Data.csv en fonction des mots-clés du fichier keywords.csv
"""

import pandas as pd
import re
import os
from typing import List, Set

def charger_mots_cles(fichier_keywords: str) -> Set[str]:
    """
    Charge les mots-clés depuis le fichier CSV keywords.csv
    
    Args:
        fichier_keywords: Chemin vers le fichier keywords.csv
        
    Returns:
        Set des mots-clés en minuscules pour la comparaison
    """
    try:
        # Lire le fichier keywords.csv
        df_keywords = pd.read_csv(fichier_keywords)
        
        # Extraire tous les mots-clés (suppose qu'il y a une colonne 'keyword' ou la première colonne)
        if 'keyword' in df_keywords.columns:
            mots_cles = df_keywords['keyword'].tolist()
        else:
            # Utiliser la première colonne si pas de colonne 'keyword'
            mots_cles = df_keywords.iloc[:, 0].tolist()
        
        # Nettoyer et convertir en minuscules
        mots_cles_clean = set()
        for mot in mots_cles:
            if pd.notna(mot):  # Ignorer les valeurs NaN
                mot_clean = str(mot).strip().lower()
                if mot_clean:  # Ignorer les chaînes vides
                    mots_cles_clean.add(mot_clean)
        
        print(f"[OK] {len(mots_cles_clean)} mots-cles charges depuis {fichier_keywords}")
        return mots_cles_clean
        
    except FileNotFoundError:
        print(f"[ERREUR] Fichier {fichier_keywords} non trouve")
        return set()
    except Exception as e:
        print(f"[ERREUR] Lors du chargement des mots-cles: {e}")
        return set()

def contient_mots_cles(texte: str, mots_cles: Set[str]) -> bool:
    """
    Vérifie si un texte contient au moins un des mots-clés
    
    Args:
        texte: Texte à analyser
        mots_cles: Set des mots-clés à rechercher
        
    Returns:
        True si au moins un mot-clé est trouvé, False sinon
    """
    if pd.isna(texte) or not isinstance(texte, str):
        return False
    
    # Convertir en minuscules et nettoyer
    texte_clean = str(texte).lower()
    
    # Rechercher chaque mot-clé dans le texte
    for mot_cle in mots_cles:
        if mot_cle in texte_clean:
            return True
    
    return False

def filtrer_videos(fichier_data: str, fichier_keywords: str, fichier_sortie: str = "videos_filtrees.csv"):
    """
    Filtre les vidéos en fonction des mots-clés
    
    Args:
        fichier_data: Chemin vers le fichier Data.csv
        fichier_keywords: Chemin vers le fichier keywords.csv
        fichier_sortie: Nom du fichier de sortie
    """
    print("Demarrage du filtrage des videos...")
    
    # Charger les mots-clés
    mots_cles = charger_mots_cles(fichier_keywords)
    if not mots_cles:
        print("❌ Aucun mot-clé chargé. Arrêt du programme.")
        return
    
    # Charger les données des vidéos
    try:
        df_data = pd.read_csv(fichier_data)
        print(f"[OK] {len(df_data)} videos chargees depuis {fichier_data}")
    except FileNotFoundError:
        print(f"[ERREUR] Fichier {fichier_data} non trouve")
        return
    except Exception as e:
        print(f"[ERREUR] Lors du chargement des donnees: {e}")
        return
    
    # Vérifier que les colonnes attendues existent
    colonnes_attendues = ['title', 'id', 'url', 'viewcount', 'date', 'channelName', 'channelUrl', 'numberOfSubscribers', 'duration']
    colonnes_manquantes = [col for col in colonnes_attendues if col not in df_data.columns]
    
    if colonnes_manquantes:
        print(f"[ATTENTION] Colonnes manquantes: {colonnes_manquantes}")
        print(f"Colonnes disponibles: {list(df_data.columns)}")
    
    # Créer une copie du DataFrame pour éviter de modifier l'original
    df_resultat = df_data.copy()
    
    # Ajouter la colonne de décision
    df_resultat['decision'] = 'Rejeté'  # Par défaut, toutes les vidéos sont rejetées
    
    # Compter les vidéos gardées et rejetées
    gardees = 0
    rejetees = 0
    
    print("\nAnalyse des videos...")
    
    # Analyser chaque vidéo
    for index, row in df_data.iterrows():
        # Vérifier dans le titre et le nom de la chaîne
        titre = row.get('title', '')
        channel_name = row.get('channelName', '')
        
        # Combiner titre et nom de chaîne pour l'analyse
        texte_analyse = f"{titre} {channel_name}"
        
        if contient_mots_cles(texte_analyse, mots_cles):
            df_resultat.at[index, 'decision'] = 'Gardé'
            gardees += 1
        else:
            rejetees += 1
        
        # Afficher le progrès tous les 100 éléments
        if (index + 1) % 100 == 0:
            print(f"  Traite {index + 1}/{len(df_data)} videos...")
    
    # Sauvegarder le résultat
    try:
        df_resultat.to_csv(fichier_sortie, index=False, encoding='utf-8')
        print(f"\n[OK] Fichier sauvegarde: {fichier_sortie}")
        print(f"Resultats:")
        print(f"   - Videos gardees: {gardees}")
        print(f"   - Videos rejetees: {rejetees}")
        print(f"   - Total: {len(df_data)}")
        print(f"   - Taux de conservation: {(gardees/len(df_data)*100):.1f}%")
        
    except Exception as e:
        print(f"[ERREUR] Lors de la sauvegarde: {e}")

def main():
    """Fonction principale"""
    print("=" * 60)
    print("FILTREUR DE VIDEOS PAR MOTS-CLES")
    print("=" * 60)
    
    # Vérifier que les fichiers existent
    fichier_data = "Data.csv"
    fichier_keywords = "keywords.csv"
    
    if not os.path.exists(fichier_data):
        print(f"[ERREUR] Fichier {fichier_data} non trouve dans le repertoire courant")
        print("   Assurez-vous que le fichier Data.csv est present")
        return
    
    if not os.path.exists(fichier_keywords):
        print(f"[ERREUR] Fichier {fichier_keywords} non trouve dans le repertoire courant")
        print("   Assurez-vous que le fichier keywords.csv est present")
        return
    
    # Lancer le filtrage
    filtrer_videos(fichier_data, fichier_keywords)

if __name__ == "__main__":
    main()
