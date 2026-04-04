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
    Standard single-hop traversal. 
    Required for the multi-hop logic to function.
    """
    if not G.has_node(start_node):
        return []

    results = []
    edges = G.out_edges(start_node, data=True) if direction == "out" else G.in_edges(start_node, data=True)
    
    for u, v, data in edges:
        if data.get('label') == relation_label:
            neighbor = v if direction == "out" else u
            results.append((neighbor, data['weight']))
            
    return results

def multi_hop_income_query(G, category, exp_level):
    """
    Combines Category and Experience Level to predict the most likely Income Range.
    Logic: Finds the intersection of 'PAYS' and 'EARNS' relationships.
    """
    # 1. Get all income nodes connected to the Category (e.g., DevOps -> PAYS -> Range)
    cat_results = dict(single_hop_query(G, category, "PAYS", direction="out"))
    
    # 2. Get all income nodes connected to the Experience Level (e.g., Senior -> EARNS -> Range)
    exp_results = dict(single_hop_query(G, exp_level, "EARNS", direction="out"))
    
    # If both queries return nothing, we can't make a prediction
    if not cat_results and not exp_results:
        return "No data found for this combination."

    # 3. Combine weights for nodes that appear in both paths
    # We use a set union to ensure we check every potential income range found
    all_income_nodes = set(cat_results.keys()) | set(exp_results.keys())
    
    scores = {}
    for node in all_income_nodes:
        # We sum the weights. A node appearing in BOTH paths gets a much higher score.
        score = cat_results.get(node, 0) + exp_results.get(node, 0)
        scores[node] = score
        
    # 4. Return the income range with the highest total score (the strongest intersection)
    prediction = max(scores, key=scores.get)
    return prediction

if __name__ == "__main__":
    # Path to your saved brain
    PKL_PATH = os.path.join('..', 'model', 'knowledge_graph.pkl')
    
    try:
        kg = load_kg(PKL_PATH)
        print("KG loaded for Multi-Hop Query testing.\n")

        # --- Example Test Case ---
        test_cat = "AI/ML Engineering"
        test_exp = "senior"
        
        result = multi_hop_income_query(kg, test_cat, test_exp)
        
        print(f"Query: What is the expected income for a {test_exp} {test_cat}?")
        print(f"Prediction: {result}")

    except Exception as e:
        print(f"Error: {e}")