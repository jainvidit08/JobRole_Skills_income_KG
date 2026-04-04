import pickle
import os

def load_kg(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Pickle file not found at {file_path}")
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def single_hop_query(G, start_node, relation_label, direction="out"):
    """Core engine for traversing one step in the graph."""
    if not G.has_node(start_node):
        return []
    results = []
    edges = G.out_edges(start_node, data=True) if direction == "out" else G.in_edges(start_node, data=True)
    for u, v, data in edges:
        if data.get('label') == relation_label:
            neighbor = v if direction == "out" else u
            results.append((neighbor, data['weight']))
    return results

def dynamic_multi_hop(G, node1, rel1, node2, rel2):
    """
    Finds the strongest intersection between two different paths.
    """
    # Get neighbors for both starting points
    res1 = dict(single_hop_query(G, node1, rel1, direction="out"))
    res2 = dict(single_hop_query(G, node2, rel2, direction="out"))
    
    if not res1 and not res2:
        return "No common data found for this combination."

    # Combine weights of shared destination nodes
    common_nodes = set(res1.keys()) | set(res2.keys())
    scores = {node: res1.get(node, 0) + res2.get(node, 0) for node in common_nodes}
    
    # The winner is the node with the highest combined weight
    prediction = max(scores, key=scores.get)
    return f"{prediction} (Confidence Score: {scores[prediction]})"

def main():
    PKL_PATH = os.path.join('..', 'model', 'knowledge_graph.pkl')
    try:
        kg = load_kg(PKL_PATH)
        print("--- Dynamic KG Recommendation Engine ---")
        
        while True:
            print("\nChoose a Prediction Type:")
            print("1. Income Prediction (Category + Experience)")
            print("2. Income Prediction (Skill + Education)")
            print("3. Job Recommendation (Skill + Education)")
            print("4. Custom Intersection (Manual Input)")
            print("Type 'exit' to quit.")

            choice = input("\nSelect (1-4): ").strip()
            if choice.lower() == 'exit': break

            if choice == '1':
                n1 = input("Enter Category: ")
                n2 = input("Enter Experience Level: ")
                print(f"\nPredicted Income: {dynamic_multi_hop(kg, n1, 'PAYS', n2, 'EARNS')}")

            elif choice == '2':
                n1 = input("Enter Skill: ")
                n2 = input("Enter Education: ")
                print(f"\nPredicted Income: {dynamic_multi_hop(kg, n1, 'PAYS_DIRECT', n2, 'RESULT_IN')}")

            elif choice == '3':
                n1 = input("Enter Skill: ")
                n2 = input("Enter Education: ")
                print(f"\nSuggested Category: {dynamic_multi_hop(kg, n1, 'PART_OF', n2, 'QUALIFIES_FOR')}")

            elif choice == '4':
                print("\nAvailable Relations: PART_OF, PAYS, EARNS, PAYS_DIRECT, RESULT_IN, QUALIFIES_FOR")
                n1 = input("Enter First Node: ")
                r1 = input("Enter Relation for First Node: ")
                n2 = input("Enter Second Node: ")
                r2 = input("Enter Relation for Second Node: ")
                print(f"\nResult: {dynamic_multi_hop(kg, n1, r1, n2, r2)}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()