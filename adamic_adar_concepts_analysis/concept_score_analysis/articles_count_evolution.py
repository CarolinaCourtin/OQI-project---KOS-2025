import csv
import matplotlib.pyplot as plt
from collections import Counter
import os

def plot_article_count_by_year(csv_path="quantum_subtree.csv"):
    year_counter = Counter()

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            year = row.get("publication_year")
            if year and year.isdigit():
                year_counter[int(year)] += 1

    if not year_counter:
        print("Aucune année valide trouvée dans le fichier.")
        return

    # Ordonner par année croissante
    sorted_years = sorted(year_counter.items())
    years, counts = zip(*sorted_years)

    plt.figure(figsize=(10, 5))
    plt.plot(years, counts, marker='o', linestyle='-', color='tab:green')
    plt.title("Nombre d'articles par année")
    plt.xlabel("Année")
    plt.ylabel("Nombre d'articles")
    plt.grid(True)

    # Afficher seulement une année sur 5 pour éviter la surcharge
    xtick_years = [y for y in years if y % 5 == 0]
    plt.xticks(xtick_years, rotation=45)

    plt.tight_layout()

    output_dir = "plots"
    os.makedirs(output_dir, exist_ok=True)
    plot_file = os.path.join(output_dir, f"count_articles_evolution.png")
    plt.savefig(plot_file, dpi=300)

    plt.show()

plot_article_count_by_year()
