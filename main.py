import networkx as nx
import community.community_louvain as community_louvain
import matplotlib.pyplot as plt
import csv

file_path = "data/com-dblp.ungraph.txt"

print("Loading graph...")

# -----------------------------
# STEP 1 — Load Graph
# -----------------------------
G = nx.Graph()

with open(file_path, "r") as file:
    for line in file:
        if line.startswith("#"):
            continue
        u, v = map(int, line.split())
        G.add_edge(u, v)

print("Graph loaded successfully!")
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())

# -----------------------------
# STEP 2 — Basic Network Stats
# -----------------------------
density = nx.density(G)
print("Density:", density)

avg_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()
print("Average Degree:", avg_degree)

largest_cc = max(nx.connected_components(G), key=len)
G_lcc = G.subgraph(largest_cc).copy()
print("Largest Connected Component size:", G_lcc.number_of_nodes())

# -----------------------------
# STEP 3 — Approximate Diameter
# -----------------------------
from networkx.algorithms.approximation import diameter as approx_diameter

try:
    dia = approx_diameter(G_lcc)
    print("Approx Diameter:", dia)
except:
    print("Approx Diameter: Could not compute.")

# -----------------------------
# STEP 4 — Degree Centrality
# -----------------------------
deg_cent = nx.degree_centrality(G)
top_degree = sorted(deg_cent.items(), key=lambda x: x[1], reverse=True)[:10]

print("\nTop 10 by Degree Centrality:")
for node, score in top_degree:
    print(node, score)

# -----------------------------
# STEP 5 — PageRank (Scipy NOT needed)
# -----------------------------
pagerank = nx.pagerank(G, alpha=0.85, max_iter=200)
top_pr = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]

print("\nTop 10 PageRank:")
for node, score in top_pr:
    print(node, score)

# -----------------------------
# STEP 6 — Create Top-5000 Subgraph
# -----------------------------
deg = dict(G.degree())
top_nodes = sorted(deg, key=deg.get, reverse=True)[:5000]
subG = G.subgraph(top_nodes).copy()

print("\nSubgraph size:", subG.number_of_nodes(), subG.number_of_edges())

# -----------------------------
# STEP 6.5 — Additional Network Structure Metrics (Stage 3)
# -----------------------------
print("\nComputing additional network structure metrics (subgraph)...")

# Average clustering coefficient
avg_clustering = nx.average_clustering(subG)
print("Average Clustering Coefficient:", avg_clustering)

# Degree assortativity
assortativity = nx.degree_assortativity_coefficient(subG)
print("Degree Assortativity:", assortativity)

# Approximate average shortest path length
try:
    avg_path_length = nx.average_shortest_path_length(subG)
    print("Average Shortest Path Length:", avg_path_length)
except:
    print("Average Shortest Path Length: skipped (graph too large)")


# -----------------------------
# STEP 7 — Closeness & Betweenness (approx)
# -----------------------------
closeness = nx.closeness_centrality(subG)

betweenness = nx.betweenness_centrality(subG, k=300, normalized=True)

# -----------------------------
# STEP 8 — Eigenvector Centrality (on subgraph)
# -----------------------------
print("Computing Eigenvector Centrality (subgraph)...")
eigenvector = nx.eigenvector_centrality(subG, max_iter=200, tol=1e-06)

top_eig = sorted(eigenvector.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 Eigenvector Centrality:")
for node, score in top_eig:
    print(node, score)

# -----------------------------
# STEP 9 — Louvain Communities
# -----------------------------
partition = community_louvain.best_partition(subG)
num_communities = len(set(partition.values()))
print("\nNumber of communities detected:", num_communities)

# -----------------------------
# STEP 9A — Modularity Score
# -----------------------------
modularity = community_louvain.modularity(partition, subG)
print("Modularity Score:", modularity)


# -----------------------------
# STEP 10 — Export for GEPHI
# -----------------------------
print("\nExporting files for Gephi...")

# Add community attribute to graph
for node, comm in partition.items():
    subG.nodes[node]["community"] = comm

# Add PageRank
for node, pr in pagerank.items():
    if node in subG.nodes():
        subG.nodes[node]["pagerank"] = pr

# Add eigenvector centrality  (FIXED HERE)
for node, ev in eigenvector.items():
    if node in subG.nodes():
        subG.nodes[node]["eigenvector"] = ev

# 1) Export GEXF graph
nx.write_gexf(subG, "subgraph_5000.gexf")

# 2) Export CSV with metrics
with open("nodes_metrics.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["node", "degree", "pagerank", "eigenvector", "community"])
    for node in subG.nodes():
        writer.writerow([
            node,
            deg[node],
            pagerank[node],
            eigenvector[node],
            partition[node]
        ])

print("Gephi export completed!")


# -----------------------------
# STEP 11 — Information Diffusion (SI Model)
# -----------------------------
import random

def simulate_si(graph, seed_nodes, steps=10):
    infected = set(seed_nodes)
    for _ in range(steps):
        new_infected = set(infected)
        for node in infected:
            for nbr in graph.neighbors(node):
                if nbr not in infected and random.random() < 0.05:
                    new_infected.add(nbr)
        infected = new_infected
    return infected

# Start diffusion from top PageRank author
seed = [top_pr[0][0]]
infected_nodes = simulate_si(subG, seed)

print("Diffusion reached nodes:", len(infected_nodes))


print("\nAnalysis completed successfully!")