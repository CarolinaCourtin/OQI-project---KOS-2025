import csv 
import os
import requests
import networkx as nx
from networkx.algorithms.link_prediction import adamic_adar_index
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

'''
This python file contains the code that was used to generate the AA scores for unconnected pairs of concepts nodes of level 4 and 5.
Although the following function did not yield results during this phase of the project, it has been retained for future work. 

'''


def get_season_label(date):

    year = date.year
    month = date.month
    if month in [1, 2, 3]:
        season = 'winter'
    elif month in [4, 5, 6]:
        season = 'spring'
    elif month in [7, 8, 9]:
        season = 'summer'
    else:
        season = 'fall'
    return f"{season}_{year}"



def generate_adamic_adar_scores_levels_4_5():
    output_dir = "adamic_scores_levels_4_5"
    os.makedirs(output_dir, exist_ok=True)

    print("📥 Chargement des concepts niveau 4 et 5...")
    levels_df = pd.read_csv("concepts_levels.csv")
    levels_df['concept_id'] = levels_df['concept_id'].str.strip()
    allowed_concepts = set(levels_df[levels_df['level'].isin([4, 5])]['concept_id'].str.strip().apply(lambda x: x.split("/")[-1]))
    concept_level_dict = {
        cid.strip().split("/")[-1]: level
        for cid, level in zip(levels_df['concept_id'], levels_df['level'])
        }
    print(f"✅ {len(allowed_concepts)} concepts de niveau 4 et 5 chargés.")

    df = pd.read_csv("quantum_networks_log_papers.csv")
    df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')
    df = df.dropna(subset=['publication_date'])
    df['season_label'] = df['publication_date'].apply(get_season_label)

    season_order = {'winter': 1, 'spring': 2, 'summer': 3, 'fall': 4}
    df['season'] = df['season_label'].str.extract(r'(\w+)_\d+')[0]
    df['year'] = df['season_label'].str.extract(r'_(\d+)')[0].astype(int)
    df['season_rank'] = df['season'].map(season_order)
    grouped = df.groupby(['year', 'season_rank', 'season_label'])['paper_id'].apply(list)
    grouped = grouped.sort_index()

    cumulative_articles = set()
    season_articles_cumulative = {}

    for (_, _, label), paper_ids in grouped.items():
        cumulative_articles.update(paper_ids)
        season_articles_cumulative[label] = sorted(cumulative_articles)

    print(f"🗂 {len(season_articles_cumulative)} saisons détectées.")

    print("📄 Chargement des données d'articles...")
    with open("quantum_networks_log_papers.csv", newline='', encoding='utf-8') as fichier_csv:
        lecteur = csv.DictReader(fichier_csv)
        article_data = {ligne['paper_id']: ligne for ligne in lecteur}
    print(f"📚 {len(article_data)} articles chargés.")

    print("\n🧪 Exemple de concepts autorisés (niveaux 4/5) :")
    for i, cid in enumerate(list(allowed_concepts)[:5]):
        print(f" - {cid}")

    sample_article = article_data[list(article_data.keys())[0]]
    print("\n🧪 Concepts d’un article (brut) :")
    print(sample_article["concepts"])

    for season, list_article in season_articles_cumulative.items():
        print(f"\n🔄 Traitement de la saison : {season} ({len(list_article)} articles cumulés)")

        G = nx.Graph()
        article_counter = 0
        valid_article_counter = 0
        total_concepts = 0
        filtered_concepts = 0
        level_counter = {}  # 🔄 AJOUT

        for article_id in list_article:
            article_counter += 1
            article = article_data.get(article_id)
            if not article:
                continue

            concept_all = article.get("concepts", "").split(";")
            total_concepts += len(concept_all)
            concept_sliced = [i.split("|") for i in concept_all if len(i.split("|")) == 2]

            concept_filtered = []
            for item in concept_sliced:
                cid = item[0].strip().split("/")[-1]
                if cid in allowed_concepts:
                    concept_filtered.append(item)
                    level = concept_level_dict.get(cid, "unknown")  # 🔄 AJOUT
                    level_counter[level] = level_counter.get(level, 0) + 1  # 🔄 AJOUT
                    print(f"✅ Found concept level 4/5: {cid}")

            filtered_concepts += len(concept_filtered)
            if not concept_filtered:
                continue

            valid_article_counter += 1

            for concept_link, concept_name in concept_filtered:
                concept_id = concept_link.split("/")[-1]
                if concept_id not in G:
                    G.add_node(concept_id, Concept_name=concept_name, Concept_link=concept_link)

            for i in range(len(concept_filtered)):
                for j in range(i + 1, len(concept_filtered)):
                    concept1 = concept_filtered[i][0].split("/")[-1]
                    concept2 = concept_filtered[j][0].split("/")[-1]
                    if not G.has_edge(concept1, concept2):
                        G.add_edge(concept1, concept2)

        print(f"🧾 Articles traités : {article_counter}")
        print(f"✅ Articles avec concepts niveau 4/5 : {valid_article_counter}")
        print(f"🔢 Concepts totaux : {total_concepts} / concepts filtrés : {filtered_concepts}")
        print(f"📊 Graphe : {G.number_of_nodes()} noeuds, {G.number_of_edges()} arêtes")
        print("📈 Répartition des niveaux :")  # 🔄 AJOUT
        for lvl, count in sorted(level_counter.items()):
            print(f"   - Niveau {lvl}: {count} concepts")  # 🔄 AJOUT

        if G.number_of_nodes() < 2:
            print(f"⚠️ Graphe trop petit pour {season}, Adamic-Adar ignoré.")
            continue

        non_edges_list = list(nx.non_edges(G))
        print(f"🔍 {len(non_edges_list)} couples non connectés à évaluer")

        adamic_preds = list(adamic_adar_index(G, tqdm(non_edges_list)))

        output_path = os.path.join(output_dir, f"{season}_adamic_scores.csv")
        with open(output_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "Concept1_ID", "Concept1_Name",
                "Concept2_ID", "Concept2_Name",
                "AdamicAdarScore"
            ])
            for u, v, score in adamic_preds:
                name_u = G.nodes[u].get('Concept_name', 'Unknown')
                name_v = G.nodes[v].get('Concept_name', 'Unknown')
                writer.writerow([u, name_u, v, name_v, score])

        print(f"✅ Fichier sauvegardé : {output_path}")

    print("🎉 Fin de l’analyse par saison pour niveaux 4 et 5.")

# generate_adamic_adar_scores_levels_4_5()
