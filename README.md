# 📊 DBLP Co-Authorship Network Analysis

## 📌 Project Overview
This project performs a **Social Network Analysis (SNA)** on the **DBLP co-authorship dataset** to study collaboration patterns among computer science researchers. Authors are modeled as nodes and co-authorship relationships as edges to analyze network structure, identify influential researchers, detect research communities, and observe information diffusion.

---

## 📂 Dataset
- **Name:** DBLP Co-Authorship Network  
- **Source:** Stanford Network Analysis Project (SNAP)  
- **Graph Type:** Undirected  
- **Nodes:** Authors  
- **Edges:** Co-authored publications  

Due to the large dataset size (~317K nodes), a **degree-based subgraph of the top 5000 authors** was used for detailed analysis and visualization.

---

## 🛠 Tools & Technologies
- **Programming Language:** Python  
- **Libraries & Frameworks:**  
  - NetworkX  
  - python-louvain  
  - Matplotlib  
- **Visualization Tool:** Gephi  

---

## 🔍 Methodology
### 1. Data Preprocessing
- Removed comment lines from raw dataset  
- Converted edge list into NetworkX graph  
- Extracted the largest connected component  
- Built a high-degree subgraph for efficient computation  

### 2. Network Structure Analysis
- Number of nodes and edges  
- Network density  
- Average degree  
- Approximate diameter  
- Clustering coefficient  
- Degree assortativity  

### 3. Centrality Measures
- Degree Centrality  
- PageRank  
- Eigenvector Centrality  
- Betweenness Centrality (approximate)  
- Closeness Centrality  

### 4. Community Detection
- Louvain algorithm  
- Modularity score evaluation  

### 5. Information Diffusion
- SI (Susceptible–Infected) diffusion model  
- Initiated from influential (high PageRank) authors  

### 6. Visualization
- Exported network as `.gexf` for Gephi  
- Applied ForceAtlas2 layout  
- Colored nodes by community  
- Sized nodes by influence (PageRank / degree)  

---

## 📈 Key Results
- The DBLP network is **sparse but highly connected**, showing **small-world characteristics**.  
- A small set of authors act as **highly influential hubs**.  
- Louvain community detection revealed **distinct research clusters** with high modularity.  
- Information diffusion spreads efficiently through central authors.  
- Visualizations clearly highlight community structure and author influence.

---

## 🖼 Visualizations
This project includes:
- Community-colored co-authorship network  
- Influence-based (PageRank) node sizing  
- Filtered visualizations of major communities  

(All visualizations generated using **Gephi**)

---

## 📁 Repository Structure
project_files:
  - main.py
  - subgraph_5000.gexf
  - nodes_metrics.csv
  - README.md


---

## ▶️ How to Run the Project
1. Clone this repository  
2. Install required libraries:
```bash
pip install networkx python-louvain matplotlib
```
3. Place the dataset file inside a data/ directory
Run the analysis:
```bash
python main.py
```



