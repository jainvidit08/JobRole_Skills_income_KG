import pickle

with open("knowledge_graph.pkl", "rb") as f:
    kg = pickle.load(f)
    
# Verify weight is there
for u, v, data in kg.edges(data=True):
    print(f"Edge {u} -> {v} has weight: {data['weight']}")