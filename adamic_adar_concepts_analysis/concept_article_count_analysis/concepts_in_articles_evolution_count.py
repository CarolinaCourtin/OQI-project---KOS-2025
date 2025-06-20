import csv
import matplotlib.pyplot as plt
from collections import defaultdict

def cumulative_article_counts(concept_id1, concept_id2, filename='quantum_subtree.csv'):
    """
    Affiche uniquement le comptage cumulatif du nombre d'articles contenant :
    - concept_id1 seul
    - concept_id2 seul
    - les deux concepts
    Les poids (weights) ne sont pas traités ici.
    """
    yearly_counts = defaultdict(lambda: {'c1_only': 0, 'c2_only': 0, 'both': 0})

    with open(filename, newline='', encoding='utf-8') as csvfile:
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

    years = sorted(yearly_counts.keys())
    c1_only_counts = []
    c2_only_counts = []
    both_counts = []

    cum_c1_only = cum_c2_only = cum_both = 0

    for year in years:
        cum_c1_only += yearly_counts[year]['c1_only']
        cum_c2_only += yearly_counts[year]['c2_only']
        cum_both += yearly_counts[year]['both']

        c1_only_counts.append(cum_c1_only)
        c2_only_counts.append(cum_c2_only)
        both_counts.append(cum_both)

    # Création du graphique
    plt.figure(figsize=(10, 6))
    plt.plot(years, c1_only_counts, label=f'{concept_id1} seul (cumulé)', color='blue', marker='o')
    plt.plot(years, c2_only_counts, label=f'{concept_id2} seul (cumulé)', color='red', marker='o')
    plt.plot(years, both_counts, label=f'{concept_id1} et {concept_id2} (cumulé)', color='green', marker='o')

    plt.xlabel('Année')
    plt.ylabel('Nombre cumulatif d\'articles')
    plt.title(f'Évolution cumulative des articles citant {concept_id1} et/ou {concept_id2}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

cumulative_article_counts('C186468114', 'C51003876', filename='quantum_subtree.csv')
