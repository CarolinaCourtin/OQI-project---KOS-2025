import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def get_top_adamic_scores(csv_file, top_n):
    scores = []

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            concept1_id = row["Concept1_ID"]
            concept2_id = row["Concept2_ID"]
            concept1_name = row["Concept1_Name"]
            concept2_name = row["Concept2_Name"]
            score = float(row["AdamicAdarScore"])
            scores.append(((concept1_id, concept1_name), (concept2_id, concept2_name), score))

    top_scores = sorted(scores, key=lambda x: x[2], reverse=True)[:top_n]
    return top_scores


def temporal_analysis():
    track_amount = None
    missing_data = []
    previous_concepts = set()
    tracked_pairs = set()
    pair_scores = {}
    first_year_track = 0
    years_graph_x = []
    top_concepts_scores = None

    for year in range(1965, 2024): 
        subfolder = f"adamic_scores_by_year"  
        filename = os.path.join(subfolder, f"{year}_adamic_scores.csv")

        if os.path.exists(filename):
            first_year_track += 1

            if first_year_track == 1:
                track_amount = 60
                top_concepts_scores = get_top_adamic_scores(filename, track_amount)
                print(f"Top concept scores : ", top_concepts_scores)

                tracked_pairs = {
                    tuple(sorted(((c1_id, c1_name), (c2_id, c2_name))))
                    for (c1_id, c1_name), (c2_id, c2_name), _ in top_concepts_scores
                }
                pair_scores = {pair: [] for pair in tracked_pairs}

            years_graph_x.append(str(year))
            current_scores = {}
            current_concepts = set()
            missing_tracked_concepts = []

            print(f"Traitement fichier {filename}")

            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    c1_id, c1_name = row["Concept1_ID"], row["Concept1_Name"]
                    c2_id, c2_name = row["Concept2_ID"], row["Concept2_Name"]
                    score = float(row["AdamicAdarScore"])
                    pair = tuple(sorted(((c1_id, c1_name), (c2_id, c2_name))))
                    current_scores[pair] = score
                    current_concepts.add(pair)

            for pair in tracked_pairs:
                if pair in current_scores:
                    pair_scores[pair].append(current_scores[pair])
                else:
                    pair_scores[pair].append(float("nan"))
                    missing_tracked_concepts.append(pair)

            if previous_concepts:
                common = current_concepts & previous_concepts
                added = current_concepts - previous_concepts
                removed = previous_concepts - current_concepts

                print(f"Comparaison avec l'année précédente :")
                print(f"   ➕ Nouveaux liens : {len(added)}")
                print(f"   ➖ Liens disparus : {len(removed)}")
                print(f"   ✅ Liens communs  : {len(common)}")

            previous_concepts = current_concepts
            print(f"Missing pairs in {year} : {missing_tracked_concepts}")

        else:
            missing_data.append(filename)

    return pair_scores, years_graph_x


def count_articles_with_both_concepts(pair, quantum_file='quantum_subtree.csv'):
    (id1, name1), (id2, name2) = pair
    yearly_counts = defaultdict(int)

    with open(quantum_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                year = int(row['publication_year'])
            except:
                continue
            concepts = row['concepts'].split(';')
            found_c1 = any(id1 in c for c in concepts)
            found_c2 = any(id2 in c for c in concepts)

            if found_c1 and found_c2:
                yearly_counts[year] += 1

    years = sorted(yearly_counts.keys())
    counts = [yearly_counts[y] for y in years]

    return years, counts


def plot_article_counts_for_pairs(pair_scores, quantum_file='quantum_subtree.csv'):
    # Figure principale (graphe)
    plt.figure(figsize=(14, 8))

    for pair in pair_scores.keys():
        years, counts = count_articles_with_both_concepts(pair, quantum_file)
        (_, name1), (_, name2) = pair
        label = f"{name1} & {name2}"

        plt.plot(years, counts, marker='o', label=label)

    plt.xlabel("Année")
    plt.ylabel("Nombre d'articles avec les deux concepts")
    plt.title("Nombre annuel d'articles contenant chaque paire de concepts")
    plt.grid(True)
    plt.tight_layout(rect=[0, 0, 0.85, 1])  # espace à droite pour la légende

    output_dir = "plots"
    os.makedirs(output_dir, exist_ok=True)
    graph_path = os.path.join(output_dir, "count_articles_evolution_citing_concepts_pairs.png")
    plt.savefig(graph_path, dpi=300, bbox_inches='tight')

    plt.show()
    plt.close()

    # Figure pour la légende seule
    fig_legend = plt.figure(figsize=(6, max(2, len(pair_scores)*0.3)))
    ax = fig_legend.add_subplot(111)
    ax.axis('off')

    lines = []
    labels = []
    for pair in pair_scores.keys():
        (_, name1), (_, name2) = pair
        label = f"{name1} & {name2}"
        line, = ax.plot([], [], marker='o')
        lines.append(line)
        labels.append(label)

    legend = ax.legend(lines, labels, loc='center')
    legend.get_frame().set_edgecolor('black')
    legend.get_frame().set_linewidth(0.5)

    plt.tight_layout()
    legend_path = os.path.join(output_dir, "count_articles_evolution_citing_concepts_pairs_LEGEND.png")
    plt.savefig(legend_path, dpi=300, bbox_inches='tight')


    plt.show()
    plt.close()



if __name__ == "__main__":
    pair_scores, years = temporal_analysis()
    plot_article_counts_for_pairs(pair_scores, quantum_file='quantum_subtree.csv')
