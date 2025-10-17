#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application Streamlit - Filtreur de vidéos par mots-clés
"""

import streamlit as st
import pandas as pd
import io
from typing import Set

# Configuration de la page
st.set_page_config(
    page_title="Filtreur de Vidéos par Mots-Clés",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def charger_mots_cles(keywords_content: str) -> Set[str]:
    """Charge les mots-clés depuis le contenu CSV"""
    try:
        df_keywords = pd.read_csv(io.StringIO(keywords_content))
        
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
        st.error(f"Erreur lors du chargement des mots-clés: {e}")
        return set()

def contient_mots_cles(texte: str, mots_cles: Set[str]) -> bool:
    """Vérifie si un texte contient au moins un des mots-clés"""
    if pd.isna(texte) or not isinstance(texte, str):
        return False
    
    texte_clean = str(texte).lower()
    
    for mot_cle in mots_cles:
        if mot_cle in texte_clean:
            return True
    
    return False

def filtrer_videos(df_data: pd.DataFrame, mots_cles: Set[str]) -> pd.DataFrame:
    """Filtre les vidéos en fonction des mots-clés"""
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
    
    return df_resultat, gardees, rejetees

def main():
    """Fonction principale de l'application Streamlit"""
    
    # En-tête
    st.title("🎬 Filtreur de Vidéos par Mots-Clés")
    st.markdown("---")
    
    # Sidebar avec instructions
    with st.sidebar:
        st.header("📋 Instructions")
        st.markdown("""
        **Étapes :**
        1. **Uploadez** votre fichier `Data.csv`
        2. **Uploadez** votre fichier `keywords.csv`
        3. **Cliquez** sur "Filtrer les Vidéos"
        4. **Téléchargez** le résultat
        
        **Format des fichiers :**
        - **Data.csv** : title, id, url, viewcount, date, channelName, channelUrl, numberOfSubscribers, duration
        - **keywords.csv** : keyword (liste des mots-clés)
        """)
        
        st.markdown("---")
        st.markdown("**💡 Astuce :** Le programme analyse le titre et le nom de la chaîne de chaque vidéo.")
    
    # Zone principale
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📁 Fichier Data.csv")
        data_file = st.file_uploader(
            "Sélectionnez votre fichier de données vidéos",
            type=['csv'],
            key="data_file",
            help="Fichier contenant les données de vos vidéos"
        )
    
    with col2:
        st.header("🔑 Fichier keywords.csv")
        keywords_file = st.file_uploader(
            "Sélectionnez votre fichier de mots-clés",
            type=['csv'],
            key="keywords_file",
            help="Fichier contenant la liste des mots-clés"
        )
    
    # Bouton de filtrage
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🚀 Filtrer les Vidéos", type="primary", use_container_width=True):
            if data_file is not None and keywords_file is not None:
                try:
                    # Charger les données
                    with st.spinner("Chargement des fichiers..."):
                        df_data = pd.read_csv(data_file)
                        keywords_content = keywords_file.read().decode('utf-8')
                        mots_cles = charger_mots_cles(keywords_content)
                    
                    if not mots_cles:
                        st.error("❌ Aucun mot-clé valide trouvé dans le fichier keywords.csv")
                        return
                    
                    # Filtrer les vidéos
                    with st.spinner("Filtrage en cours..."):
                        df_resultat, gardees, rejetees = filtrer_videos(df_data, mots_cles)
                    
                    # Afficher les résultats
                    st.success("✅ Filtrage terminé avec succès !")
                    
                    # Statistiques
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("📊 Total", df_data.shape[0])
                    
                    with col2:
                        st.metric("✅ Gardées", gardees, delta=f"{(gardees/df_data.shape[0]*100):.1f}%")
                    
                    with col3:
                        st.metric("❌ Rejetées", rejetees, delta=f"{(rejetees/df_data.shape[0]*100):.1f}%")
                    
                    with col4:
                        st.metric("🔑 Mots-clés", len(mots_cles))
                    
                    # Afficher un aperçu des données
                    st.subheader("📋 Aperçu des données filtrées")
                    st.dataframe(df_resultat.head(10), use_container_width=True)
                    
                    # Bouton de téléchargement
                    csv_result = df_resultat.to_csv(index=False, encoding='utf-8')
                    st.download_button(
                        label="📥 Télécharger videos_filtrees.csv",
                        data=csv_result,
                        file_name="videos_filtrees.csv",
                        mime="text/csv",
                        type="primary",
                        use_container_width=True
                    )
                    
                    # Stocker les résultats dans la session
                    st.session_state.df_resultat = df_resultat
                    st.session_state.stats = {
                        'total': df_data.shape[0],
                        'gardees': gardees,
                        'rejetees': rejetees,
                        'mots_cles': len(mots_cles)
                    }
                    
                except Exception as e:
                    st.error(f"❌ Erreur lors du traitement: {str(e)}")
            else:
                st.warning("⚠️ Veuillez sélectionner les deux fichiers CSV")
    
    # Afficher les résultats stockés si disponibles
    if 'df_resultat' in st.session_state:
        st.markdown("---")
        st.subheader("📊 Résultats détaillés")
        
        # Filtres
        col1, col2 = st.columns(2)
        
        with col1:
            decision_filter = st.selectbox(
                "Filtrer par décision",
                ["Tous", "Gardé", "Rejeté"],
                key="decision_filter"
            )
        
        with col2:
            if decision_filter != "Tous":
                df_filtered = st.session_state.df_resultat[
                    st.session_state.df_resultat['decision'] == decision_filter
                ]
            else:
                df_filtered = st.session_state.df_resultat
            
            st.info(f"📈 {len(df_filtered)} vidéos affichées")
        
        # Tableau des résultats
        st.dataframe(df_filtered, use_container_width=True)
        
        # Bouton de téléchargement des résultats filtrés
        if decision_filter != "Tous":
            csv_filtered = df_filtered.to_csv(index=False, encoding='utf-8')
            st.download_button(
                label=f"📥 Télécharger vidéos {decision_filter.lower()}s",
                data=csv_filtered,
                file_name=f"videos_{decision_filter.lower()}s.csv",
                mime="text/csv",
                use_container_width=True
            )

if __name__ == "__main__":
    main()
