import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.stats import pearsonr
import networkx as nx


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


def compute_and_plot_correlations(pair_scores, years, csv_file='quantum_subtree.csv'):
    correlations = {}

    def get_cumulative_counts(concept_id1, concept_id2):
        yearly_counts = defaultdict(lambda: {'c1_only': 0, 'c2_only': 0, 'both': 0})

        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    year = int(row['publication_year'])
                except:
                    continue
                concepts = row['concepts'].split(';')
                found_c1 = any(concept_id1 in c for c in concepts)
                found_c2 = any(concept_id2 in c for c in concepts)

                if found_c1 and not found_c2:
                    yearly_counts[year]['c1_only'] += 1
                elif found_c2 and not found_c1:
                    yearly_counts[year]['c2_only'] += 1
                elif found_c1 and found_c2:
                    yearly_counts[year]['both'] += 1

        sorted_years = sorted(years)
        c1_only_cum, c2_only_cum, both_cum = [], [], []
        c1_sum = c2_sum = both_sum = 0

        for y in sorted_years:
            c1_sum += yearly_counts[y]['c1_only']
            c2_sum += yearly_counts[y]['c2_only']
            both_sum += yearly_counts[y]['both']
            c1_only_cum.append(c1_sum)
            c2_only_cum.append(c2_sum)
            both_cum.append(both_sum)

        return c1_only_cum, c2_only_cum, both_cum

    for pair, aa_scores in pair_scores.items():
        (id1, name1), (id2, name2) = pair
        label = f"{name1} - {name2}"

        valid_indices = ~np.isnan(aa_scores)
        if np.sum(valid_indices) < 3:
            correlations[label] = {'c1_only': np.nan, 'c2_only': np.nan, 'both': np.nan}
            continue

        valid_years = [int(y) for i, y in enumerate(years) if valid_indices[i]]
        aa_values = np.array([s for i, s in enumerate(aa_scores) if valid_indices[i]])

        c1_cum, c2_cum, both_cum = get_cumulative_counts(id1, id2)
        c1_cum = np.array([v for i, v in enumerate(c1_cum) if valid_indices[i]])
        c2_cum = np.array([v for i, v in enumerate(c2_cum) if valid_indices[i]])
        both_cum = np.array([v for i, v in enumerate(both_cum) if valid_indices[i]])

        try:
            corr_c1 = pearsonr(aa_values, c1_cum)[0]
        except:
            corr_c1 = np.nan
        try:
            corr_c2 = pearsonr(aa_values, c2_cum)[0]
        except:
            corr_c2 = np.nan
        try:
            corr_both = pearsonr(aa_values, both_cum)[0]
        except:
            corr_both = np.nan

        correlations[label] = {
            'c1_only': corr_c1,
            'c2_only': corr_c2,
            'both': corr_both
        }

    labels = list(correlations.keys())
    c1_vals = [correlations[l]['c1_only'] for l in labels]
    c2_vals = [correlations[l]['c2_only'] for l in labels]
    both_vals = [correlations[l]['both'] for l in labels]

    x = np.arange(len(labels))
    width = 0.25

    plt.figure(figsize=(15, 7))
    plt.bar(x - width, c1_vals, width=width, label='C1 seul', color='blue')
    plt.bar(x, c2_vals, width=width, label='C2 seul', color='red')
    plt.bar(x + width, both_vals, width=width, label='Les deux', color='green')

    plt.xticks(x, labels, rotation=45, ha='right', fontsize=9)
    plt.ylabel('Corrélation de Pearson')
    plt.title("Corrélation entre Adamic-Adar et fréquence cumulée des concepts")
    plt.legend()
    plt.tight_layout()
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    output_dir = "plots"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "correlation_adamic_vs_freq.png")
    plt.savefig(output_file, dpi=300)

    plt.show()


def temporal_analysis():
    track_amount = 60
    years_graph_x = []
    top_concepts_scores = None
    pair_scores = {}
    tracked_pairs = set()
    previous_concepts = set()

    for year in range(1965, 2024):
        subfolder = "adamic_scores_by_year"
        filename = os.path.join(subfolder, f"{year}_adamic_scores.csv")
        if not os.path.exists(filename):
            continue

        years_graph_x.append(str(year))
        current_scores = {}
        current_concepts = set()

        if top_concepts_scores is None:
            top_concepts_scores = get_top_adamic_scores(filename, track_amount)
            tracked_pairs = {
                tuple(sorted(((c1_id, c1_name), (c2_id, c2_name))))
                for (c1_id, c1_name), (c2_id, c2_name), _ in top_concepts_scores
            }
            pair_scores = {pair: [] for pair in tracked_pairs}

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
            pair_scores[pair].append(current_scores.get(pair, float("nan")))

        previous_concepts = current_concepts

    return pair_scores, years_graph_x


# ====== Lancement global ======
pair_scores, years_graph_x = temporal_analysis()
compute_and_plot_correlations(pair_scores, [int(y) for y in years_graph_x], csv_file='quantum_subtree.csv')
