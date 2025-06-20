# Predicting Breakthroughs in Quantum Computing Using Concept Co-Occurrence Networks

## Overview

This project explores the prediction of scientific breakthroughs in the field of **quantum computing** by analyzing how **concepts co-occur in scientific literature** over time. The goal is to detect patterns in the appearance and convergence of concepts by building and analyzing conceptual networks.

We use the **Adamic-Adar Index**, a common link prediction metric, to estimate the likelihood that two scientific concepts (which have not yet appeared together in any article) will co-occur in the near future.

## Methodology

### Data and Graph Construction

- We process a curated subset of articles relevant to quantum computing.
- For each article, we extract all associated concepts.
- For a given time window (yearly or quarterly), we build a graph:
  - **Nodes** = concepts.
  - **Edges** = two concepts appearing in the same paper.

We then identify **non-linked pairs of concepts** (concepts that have never co-occurred) and compute the **Adamic-Adar index** for each such pair:

AA(x, y) = ∑ (1 / log(|Γ(z)|)) for all z ∈ Γ(x) ∩ Γ(y)


Where:
- `Γ(x)` is the set of neighbors (co-occurring concepts) of node `x`.
- `z` is a common neighbor of both `x` and `y`.

### Temporal Analyses

Two types of temporal analyses were conducted:

1. **Quarterly Analysis**
   - Graphs are created for each **season** across several years.
   - Stored in the `quarterly_analysis/` directory.

2. **Yearly Analysis**
   - Graphs are created for each **year**.
   - Stored in the `yearly_analysis/` directory.

For both, CSV files contain the Adamic-Adar scores for each pair of concepts over time.

### Tracking Concept Pair Evolution

Using the `temporal_analysis()` function, we track the evolution of a selected number of top concept pairs across time. These results are visualized as line plots showing how the Adamic-Adar score of each pair changes.

### Key Insight

We observed a recurring pattern:

> For most tracked concept pairs, the Adamic-Adar score increases over time and eventually stabilizes or drops. This change coincides with the two concepts finally appearing together in the same article — a possible sign of a **scientific breakthrough or emerging research direction**.

This suggests the **Adamic-Adar score can serve as an early indicator of concept convergence**, and potentially, innovation.

## Usage

Befiore running any scripts, make sure that ou have all the necessary dependencies.
From the root of this part (`/adamic_adar_concepts_analysis`), run :

```python
pip install -r requirements.txt
```

To run and customize the analysis:
1. Go to the `yearly_analysis/adamic_adar_score.py` script.
2. Modify the following lines:
   - Line **188**: set the range of years for analysis.
   - Line **195**: adjust the number of concept pairs to track (`track_amount`).
3. Run the script to generate plots saved in the `plots/` folder.

> **Note**: All yearly Adamic-Adar score files have already been precomputed and are stored in the `adamic_scores_by_year/` directory.

We limited our analysis to **level 4 and 5 concepts**, based on prior work by Thomas Maillard and Thibaut Chataing, who found these levels to be the most meaningful and informative for predicting research trends.

## Visualizing Concept Predictions

To explore concept link predictions visually, you can run the following function that is also sotred in the `adamic_adar_score.py` script

```python
visualiser_top_adamic_from_file(csv_file, top_n)
```
This function:

- Takes a result CSV file for a specific time frame.

- Displays a graph of the top n concept pairs with the highest Adamic-Adar scores.

- Nodes are unlinked concepts; edges represent the probability of future linkage.

Notes on Quarterly Analysis : 

In the quarterly_analysis/, a similar method is applied.

All concept levels are used (not just level 4–5).

Despite this difference, trends in concept convergence remain consistent with those found in the yearly analysis.

# Interpretation and Exploration of the Dynamics Behind the Adamic-Adar Index

## Overview

This section of the project focuses on analyzing the evolution of the Adamic-Adar (AA) index over time, with the goal of understanding the dynamics that might underlie conceptual emergence in scientific literature.

Following our initial findings showing recurring patterns in the AA index — typically a steady increase followed by a plateau or sudden drop — we performed further analyses to explore the potential causes of these trends.

---

## First Hypothesis: Correlation with Article Frequency

We hypothesized that the evolution of the Adamic-Adar index might be correlated with how often the associated concepts are mentioned in scientific articles over time.

To investigate this, we performed a correlation analysis between the **cumulative article frequency** of each concept and its corresponding **AA score**.

### Implementation

- The core code for this analysis is located in the `concept_article_count_analysis` folder.
- Main script: `count_correlations.py`. In this script, we plot for each tracked pair of concepts, the correlation between the AA index evolution, the amount of articles written using the Concept A and the amount of articles writtend using the Concept B.
- The script `concepts_in_articles_evolution_count.py` allows you to plot the evolution of the count of papers written over the years relationg to the first, the second and the two concepts together. 
- The resulting plot is already saved in the `plots/` directory under the filename `correlations.png`.  
  > ⚠️ Running the script again may take some time, but is not necessary unless you're making changes.

---

###  Results and Observations

From the graph, several key trends emerge:

- **Positive correlation**: In many concept pairs, an increase in the number of articles citing either concept is mirrored by a rise in the AA index. This supports the idea that rising visibility in the literature contributes to a higher likelihood of conceptual linkage.
  
- **Negative correlation**: In some cases, when article frequency decreases, the AA score also declines. This suggests that when interest in a concept wanes, it may have less opportunity to co-occur with others.
  
- **Latent conceptual links**: A few concept pairs show rising AA scores even when article mentions stagnate or slightly decline. This could reflect **delayed or hidden conceptual convergence**, such as interdisciplinary emergence not immediately reflected in article counts.

---

### Conclusion: Predicting Conceptual Emergence

These findings support the potential for using the Adamic-Adar index in combination with article frequency trends as **early indicators of conceptual emergence**.

- A sustained rise in AA scores — especially when coupled with increasing article counts — may signal a **future co-occurrence** of concepts.
- This could highlight **emerging research directions or breakthroughs**, particularly useful in fast-evolving domains like **quantum computing**.

While further validation is needed, this approach could inform predictive models for **scientific innovation** and **interdisciplinary linkage forecasting**.

---

## Second Hypothesis: Concept Relevance as a Driver of AA Index

This analysis explores a second hypothesis to explain the observed patterns in the evolution of the Adamic-Adar (AA) index over time. While our first hypothesis focused on article frequency, this second investigation examines whether **concept weights**—that is, their relevance within articles—could be influencing the evolution of AA scores.

The hypothesis is as follows:  
> *The evolution of the Adamic-Adar index may be influenced by the relevance (or weight) of concepts in the articles where they appear.*

In OpenAlex data, each concept assigned to an article comes with a **weight**. This weight reflects the importance or relevance of the concept in the context of the article. A high weight likely means the concept is central to the article’s subject.

If two concepts are frequently *central* to papers (i.e., have high weights), it may suggest a stronger thematic link—and possibly a higher AA score when these concepts appear in related contexts.

---

### Implementation

To explore this hypothesis, we implemented the analysis in the script:

- The core code for this analysis is located in the `concept_score_analysis` folder.

- **Main script:** `average_concept_scores.py`

This script computes the **average weight of each tracked concept** (those already observed in AA score evolution) for every year in the dataset.

### Example Output

An example output graph, generated for the **top 10 most tracked concepts**, is available under the `plots/` directory:

plots/average_top_10_concepts_score-evolution_GRAPH.png


To generate graphs for a different number of concepts, modify the relevant parameter (e.g., the number of concepts to track) in **line 22** of the script.

---

### Results and Insights

Unfortunately, this analysis did **not reveal a clear correlation** between concept weights and the evolution of the Adamic-Adar index.

However, we did make an interesting observation:

- **From the year 2000 onwards**, the average weights of the tracked concepts become **notably more stable** over time.

This trend may be due to a shift in OpenAlex coverage: a significant increase in the number of indexed articles around the early 2000s likely smoothed out fluctuations in concept relevance. This stabilization effect might be relevant in understanding how large-scale data availability influences concept metrics.
To show this increase of pusblished articles in OpenAlex, we added a few other codes and plots : 

- The `count_articles_both_concepts.py` script shows the amount of articles occuring over the year with the two concepts of the tracked pairs of concepts.

- The `articles_count_evolution.py` script shows the amount of articles occuring over the years.

In both analysis, we can clearly see that the amount of articles significantly increases over the year, which might be the reason behind the overall concepts weights stabilizing at some point. 

---

## Conclusion

This study provided valuable insights into how we might anticipate future breakthroughs in the field of quantum computing through the analysis of concept networks.

The most promising outcome was the use of the Adamic-Adar (AA) index, a metric designed to estimate the likelihood of future links between concepts based on their shared neighbors in a graph. When applied to scientific concepts extracted from articles over time, the AA index exhibited a distinctive and interpretable pattern: it often increases steadily, then plateaus or drops—a dynamic that appears to coincide with the actual co-occurrence of the concepts in future publications. This suggests the potential of the AA metric as an early signal of emerging conceptual connections, and by extension, of future scientific innovation.

### Future Work
While the AA metric showed promising results, several avenues for future investigation remain:

- Further studies could explore additional metrics to determine whether they correlate with or explain the dynamics of the AA index. Combining multiple signals might lead to more robust predictive models.

- Understanding why the AA index behaves the way it does (e.g., what drives its rise and sudden drop) could offer deeper insight into the dynamics of concept emergence. This could involve analyzing the role of funding trends, institutional collaborations, or publication venues.

- While this study focused on quantum computing, applying the same methodology to other domains (e.g., AI, biomedical research) could validate the generalizability of the AA-based predictive approach.

---
