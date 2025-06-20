# OQI-project---KOS-2025




<details>
<summary>
Clément's Contribution => Automatic KG generation with NLP
</summary>

## Automatic Knowledge Graph Generation with NLP and Ontology Alignment

This part of the project aims to generate a **Knowledge Graph (KG)** from a collection of quantum computing research paper abstracts. Using Natural Language Processing (NLP) and ontology alignment, we extract structured information in the form of (subject, predicate, object) triples and attempt to align them with a formal **Physics Ontology**. This explores the instanciation of the following research article : "**Generating knowledge graphs by employing NaturalLanguage Processing and Machine Learning techniques within the scholarly domain** " by Dessi and al (availaible in the directory /KG_generation_NLP).

---

### Work Accomplished

- **Entity Extraction**: Named Entity Recognition using SpaCy (`en_core_web_sm`) was successful in annotating abstracts with key entities.
- **Triple Extraction**: Dependency-based extraction of SVO (Subject-Verb-Object) triples worked as expected.
- **Ontology Loading**: The Physics ontology was successfully parsed using `rdflib` in RDF, OWL, and TTL formats.
- **Triple Mapping (Partially)**: Some triples were mapped to ontology terms using exact or partial string matching.

---

### Ontology Description

The physics ontology (`PhySci.ttl`, `physci.rdf`) is a semantic knowledge model of physical science concepts, including:

- **Classes**: `Quantum_Entanglement`, `Black_Hole`, `Quantum_State`, etc.
- **Properties**: `hasName`, `hasDescription`, `partOf`, etc.
- **Instances**: Named examples or cases of phenomena.

We use it to validate or enhance extracted triples. For example, if a triple `(entanglement, affect, state)` is extracted and the ontology has `entanglement` and `state` as classes, this triple gains semantic grounding.

---

### 📁 File Structure

| File / Folder                            | Description                                                        |
| ---------------------------------------- | ------------------------------------------------------------------ |
| `quantum_computing_subtree_papers.csv`   | Source dataset containing abstracts and metadata of papers         |
| `PhySci.ttl`, `physci.rdf`, `physci.owl` | Physics ontology provided in various serialization formats         |
| `[OQI]_Automatic_KG_gen_NLP.ipynb`       | Main notebook for entity/triple extraction and ontology mapping    |
| `Dessì et al. - 2021 - ... .pdf`         | Reference paper for the triple extraction and KG generation method |


---

### ⚙️ How to Run

#### Setup Environment
```bash
pip install pandas spacy rdflib
python -m spacy download en_core_web_sm
``` 
Run the notebook
Open and run [OQI]_Automatic_KG_gen_NLP.ipynb step-by-step.

It will :
-   Loads abstracts
-   Extracts triples
-   Loads the ontology
-   Maps extracted triples to ontology concepts
-   Saves results to CSV
-   Review enhanced_triples.csv. This file contains both raw and ontology-aligned triples.

### Limitations & Future Work
Due to time constraints, several key features of this project remain either partially implemented or left as future improvements. These include:

#### Concept-Based Triple Filtering
We initially attempted to filter and validate extracted triples against the concept lists provided in the paper metadata. However, this approach was unreliable due to:

Surface form mismatches (e.g., "quantum entanglement" vs. "entangled states"),

Synonyms and lexical variations not accounted for.
Future work could include string normalization or embedding-based matching to improve alignment.

#### Date Literal Conversion
Parsing of ontology data using RDFLib triggered repeated errors for non-ISO date formats like '01-07-2019'.
Although some formats were manually fixed or bypassed during parsing, the warnings persist and may affect downstream ontology operations.
Future work: implement a preprocessing step to normalize all date literals before ontology loading.

####  Triple–Ontology Mapping
Triple-to-ontology mapping was only partially realized:

Many triples extracted via NLP did not match ontology terms exactly.

The lack of semantic understanding in string comparison (e.g., "uses" vs. "applies") limited recall.
Future work could leverage:
-   Named entity linking (NEL),
-   Sentence embedding models (e.g., BERT, SBERT),
-   Ontology alignment libraries like LOV, ELK, or OntoPortal.


</details>

<details>
<summary>
Mervat's Contribution => Citation Netwok KG
</summary>

# Brief Overview

This part of the project explores citation patterns in the domain of **quantum networks** by constructing yearly knowledge graphs where nodes represent papers and edges represent citations. The aim is to:

- Go beyond OpenAlex's `counts_by_year` (limited to post-2013) to track citations year by year using the actual citing paper's date.
- Use citation counts as a proxy for relevance and create weighted graphs where highly cited papers gain more importance.
- Analyze concept relationships by tracing citations between papers to infer semantic links and their evolution over time (e.g., using co-occurrence or the Jaccard index).

---

# Work Accomplished

- **Data Collection:** Retrieved papers related to the *quantum networks* focal concept and saved them in `quantum_networks_subtree_papers_dates.csv`.
- **Node Selection:** Selected a subset of **20–50 papers** based on title, date, and ID, stored in `nodes.csv`.
- **Graph Construction:**
  - Created `knowledge_graph.ttl` with up to 250 citations per paper, including their URLs.
  - Filtered to intra-pool citations (within the 20–50 selected papers) to create `filtered_citations.ttl`.
- **Visualization:**
  - Built citation graphs with papers as nodes and citations as directed edges.
  - Produced a time-based series of visualizations showing citation evolution (e.g., 1985 alone, then 1985–1995, etc.).
  - Saved outputs in `visualisation/` (for 20 papers) and `visualisation2/` (for 50 papers).
- **Concept Analysis:**  
  - Explored concept relationships via citation paths, including experiments with Jaccard index and co-occurrence metrics.
  - Generated cumulative scores for top concept pairs over time (`top_pairs_over_time.png`).

---

# Key Insights

- **Beyond API Limits:** OpenAlex's `counts_by_year` only goes back to 2013. By using citation metadata and publication dates, this approach allows reconstructing yearly citation graphs further into the past.
- **Citation Weighting:** Citations offer a useful proxy for a paper’s impact; using them as weights in the graph allows identifying key nodes (i.e., foundational papers).
- **Semantic Inference:** Citation links between concept-containing papers help infer evolving relationships between concepts (e.g., A cites B implies a link from concept_A to concept_B).

---

# Limitations & Future Work

- **API Constraints:** The OpenAlex API has rate and time window limitations, which makes large-scale or repeated queries time-consuming.
- **Citation Date Precision:** Using only total citation counts would misrepresent temporal dynamics. For accurate time-aware analysis, the citing paper's publication date is essential.
- **Subset-Based Analysis:** The current prototype works on a small subset (20–50 papers). Scaling to thousands will require optimized processing and storage.
- **Concept Hierarchy Limitations:** OpenAlex's concept ontology sometimes lacks granularity or coherence. Integrating alternative ontologies or manual curation might yield better concept pair tracking.


</details>

<details>
<summary>
Mervat's Contribution => Citation and Weight comparaison
</summary>

# Brief Overview

This part of the project tried to understand the links and trends between the number of citations and the number of papers (weights) for pairs of concepts, that are found in the same paper in a yealy manner.


---

# Work Accomplished

- **Analysis:** Construction of yearly concept co-occurrence graphs, calculation of citation-enriched edge lists, and extraction of metrics such as growth rates, newcomers, and productivity patterns.
- **Visualization:** Generation of figures illustrating key relationships (e.g., superlinear scaling between co-occurrence and citations), citations per article, and time evolution for selected concept pairs.

---

# Results (Key Findings)

- **Superlinear Scaling:** The number of citations for a concept pair increases slightly more than proportionally with the number of co-mentioning articles (slope ≈ 1.10 in log-log regression), indicating a superlinear relationship.
- **No Critical Mass Effect:** Average citations per article remain nearly constant regardless of the pair's total article count, suggesting increased total citations arise from accumulation rather than increased per-paper impact.
- **Growth & Emergence:** The pipeline identifies rapidly growing and "newcomer" concept pairs, highlighting emerging areas of research and shifts in topic prominence within the field.
- **Temporal Proximity:** The Adamic-Adar index enables tracking of how closely related two concepts become over time, providing insights into evolving topic relationships.

---

# Limitations & Future Work

- **API Constraints:** The OpenAlex API imposes rate limits, meaning full-scale data acquisition can be time-consuming, yet it is to have all the details of the dataset you work on to correctly produce the edges files.
- **Limited data:** The OpenAlex API request "counts_by_year", which gives the detailed citation number per year of a paper is limited as it only goes back to maximum 2013. Without it, the analysis wouldn't be correct, since only using the "final" citation count of a paper, wouldn't make us able to compare it fairly with the weight of a pair of concepts in 2010 and 2015 for instance, since the citation count would be from 2025.
- **Subset Analysis:** The current workflow is based on a subset (~26,000 papers); scaling up to the entire field will require a lot more run time.
- **Concept Hierarchy:** The analysis depends on the granularity and quality of the OpenAlex concept hierarchy; refining concept selection or integrating other ontologies could improve result as the current one's aren't always the soundest.
- **Further Metrics:** Future work may include more advanced network metrics, machine learning for trend prediction, or even analysis of triples instead of pairs.

---

# References & Acknowledgements

**Codebase Inspiration** based on the work of David Dosu from the Quantum Institute of CERN, and the work of Thomas Maillart and Thibault Chataing [wazaahhh/breakthroughs](https://github.com/wazaahhh/breakthroughs/).

---


</details>
