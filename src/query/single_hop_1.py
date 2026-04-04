import pickle
import os

def load_kg(file_path):
    """Loads the saved Knowledge Graph object."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Pickle file not found at {file_path}")
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def single_hop_query(G, start_node, relation_label, direction="out"):
    """
    Finds direct connections for a node based on a relationship label.
    direction='out': Nodes that the start_node points TO.
    direction='in': Nodes that point TO the start_node.
    """
    if not G.has_node(start_node):
        return f"Node '{start_node}' not found in the Knowledge Graph."

    results = []
    
    # Get edges based on direction
    if direction == "out":
        edges = G.out_edges(start_node, data=True)
    else:
        edges = G.in_edges(start_node, data=True)
    
    for u, v, data in edges:
        if data.get('label') == relation_label:
            # If 'out', the answer is the target (v). If 'in', the answer is the source (u).
            neighbor = v if direction == "out" else u
            results.append((neighbor, data['weight']))
            
    # Sort by weight (highest frequency/strength first)
    return sorted(results, key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
    # Path to your saved brain
    PKL_PATH = os.path.join('..', 'model', 'knowledge_graph.pkl')
    
    try:
        # Load the graph once
        kg = load_kg(PKL_PATH)
        print("KG loaded successfully!\n")

        # --- Example 1: Skills for a Category (In-Hop) ---
        target_cat = "DevOps"
        skills = single_hop_query(kg, target_cat, "PART_OF", direction="in")
        print(f"Top Skills for {target_cat}:")
        for skill, weight in skills[:5]:
            print(f"- {skill} (Strength: {weight})")

        # --- Example 2: Income for a Skill (Out-Hop) ---
        target_skill = "Python"
        incomes = single_hop_query(kg, target_skill, "PAYS_DIRECT", direction="out")
        print(f"\nIncome Distribution for {target_skill}:")
        for inc, weight in incomes:
            print(f"- {inc}: {weight} freelancers")

    except Exception as e:
        print(f"Error: {e}")