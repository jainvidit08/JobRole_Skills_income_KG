import networkx as nx
import pickle
import os

def analyze_kg(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # Load the graph
    with open(file_path, 'rb') as f:
        G = pickle.load(f)

    # 1. Basic Counts
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()

    # 2. Graph Density
    # NetworkX calculates density automatically based on whether 
    # the graph is directed or undirected.
    density = nx.density(G)

    print("--- Knowledge Graph Analysis ---")
    print(f"Total Nodes (Entities): {num_nodes}")
    print(f"Total Edges (Relationships): {num_edges}")
    print(f"Graph Density: {density:.6f}")
    
    # Interpretation
    print("\n--- Insight ---")
    if density > 0.05:
        print("Your graph is 'Dense'—most entities have relationships with many others.")
    else:
        print("Your graph is 'Sparse'—relationships are very specific/niche.")

if __name__ == "__main__":
    # Point to your model file
    PKL_PATH = os.path.join('.', 'model', 'knowledge_graph.pkl')
    analyze_kg(PKL_PATH)