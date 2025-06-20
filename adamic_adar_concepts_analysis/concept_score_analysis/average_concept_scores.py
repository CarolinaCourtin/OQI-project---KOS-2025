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
    track_amount = 10  # You can change the amount of pairs of concepts to track here 
    missing_data = []
    previous_concepts = set()
    tracked_pairs = set()
    pair_scores = {}
    first_year_track = 0
    years_graph_x = []
    top_concepts_scores = None
    concepts_to_track = set()
    pair_labels = {}

    for year in range(1965, 2024):
        subfolder = "adamic_scores_by_year"
        filename = os.path.join(subfolder, f"{year}_adamic_scores.csv")

        if os.path.exists(filename):
            first_year_track += 1

            if first_year_track == 1:
                top_concepts_scores = get_top_adamic_scores(filename, track_amount)
                tracked_pairs = {
                    tuple(sorted(((c1_id, c1_name), (c2_id, c2_name))))
                    for (c1_id, c1_name), (c2_id, c2_name), _ in top_concepts_scores
                }
                pair_scores = {pair: [] for pair in tracked_pairs}

                for (c1_id, c1_name), (c2_id, c2_name), _ in top_concepts_scores:
                    concepts_to_track.add((c1_id, c1_name))
                    concepts_to_track.add((c2_id, c2_name))

                    label = f"{c1_name} - {c2_name}"
                    pair = tuple(sorted(((c1_id, c1_name), (c2_id, c2_name))))
                    pair_labels[pair] = label

            years_graph_x.append(str(year))
            current_scores = {}
            current_concepts = set()
            missing_tracked_concepts = []

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

            previous_concepts = current_concepts

        else:
            missing_data.append(filename)

    # --- Analyse des concepts individuels dans quantum_subtree.csv ---
    concept_year_scores = defaultdict(lambda: defaultdict(list))

    with open('quantum_subtree.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                year = int(row["publication_year"])
            except ValueError:
                continue
            if year < 1965 or year > 2023:
                continue

            raw_concepts = row["concepts"]
            for concept_score_str in raw_concepts.strip().split(';'):
                try:
                    parts = concept_score_str.strip().split('|')
                    if len(parts) == 3:
                        concept_id = parts[0].split('/')[-1]
                        concept_name = parts[1]
                        score = float(parts[2])
                        if (concept_id, concept_name) in concepts_to_track:
                            concept_year_scores[concept_name][year].append(score)
                except ValueError:
                    continue

    # --- Graphe sans légende : évolution des scores moyens des concepts ---

    plt.figure(figsize=(12, 6))
    concept_lines = []
    for concept_name, year_scores in concept_year_scores.items():
        years = sorted(year_scores.keys())
        avg_scores = [np.mean(year_scores[y]) if year_scores[y] else float('nan') for y in years]
        line, = plt.plot(years, avg_scores, marker='o', label=concept_name)
        concept_lines.append((line, concept_name))

    plt.xlabel("Année")
    plt.ylabel("Score moyen du concept (quantum_subtree)")
    plt.title(f"Évolution des scores moyens des concepts liés aux top {track_amount} paires Adamic-Adar")
    plt.grid(True)
    plt.tight_layout()
    

    output_dir = "plots"
    os.makedirs(output_dir, exist_ok=True)
    plot_file = os.path.join(output_dir, f"average_top_{track_amount}_concepts_scores_evolution_GRAPH.png")
    plt.savefig(plot_file, dpi=300)

    plt.show()

    plt.close()

    # --- Figure séparée pour la légende des concepts ---

    fig_concept_legend = plt.figure(figsize=(6, max(2, len(concept_lines) * 0.25)))
    ax2 = fig_concept_legend.add_subplot(111)
    ax2.axis('off')
    concept_legend_lines = [l[0] for l in concept_lines]
    concept_legend_labels = [l[1] for l in concept_lines]

    legend2 = ax2.legend(concept_legend_lines, concept_legend_labels, loc='center', frameon=True)
    legend2.get_frame().set_edgecolor('black')
    legend2.get_frame().set_linewidth(0.5)
    plt.tight_layout()

    output_dir = "plots"
    os.makedirs(output_dir, exist_ok=True)
    plot_file = os.path.join(output_dir, f"average_top_{track_amount}_concepts_scores_evolution_LEGEND.png")
    plt.savefig(plot_file, dpi=300)

    plt.show()

    plt.close()

if __name__ == "__main__":
    temporal_analysis()
