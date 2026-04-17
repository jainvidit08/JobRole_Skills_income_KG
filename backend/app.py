from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import os
import pickle

app = FastAPI()

# Enable CORS so our Frontend can talk to our Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

PKL_PATH = os.path.join('..', 'src','model', 'knowledge_graph.pkl')
kg = load_kg(PKL_PATH)

@app.get("/query")
async def get_recommendation(node: str, relation: str, direction: str = "out"):
    """
    Endpoint to fetch KG data. 
    Example: /query?node=DevOps&relation=PART_OF&direction=in
    """
    results = single_hop_query(kg, node, relation, direction)
    if isinstance(results, list):
        # Format for easier frontend mapping
        return [{"name": item, "weight": weight} for item, weight in results]
    return {"error": "No data found"}

@app.get("/metadata")
async def get_metadata():
    """
    Scans the Knowledge Graph to extract unique values for each node type.
    This provides the list for frontend autocomplete suggestions.
    """
    categories = set()
    skills = set()
    experience = set()
    education = set()
    income_ranges = set()

    # Iterate through all edges to identify node types by their relationship labels
    for u, v, data in kg.edges(data=True):
        label = data.get('label')

        # 1. Extract Categories and Skills
        if label == 'PART_OF':
            skills.add(u)
            categories.add(v)
        
        # 2. Extract Experience Levels
        elif label == 'EARNS':
            experience.add(u)
            income_ranges.add(v) # The target of EARNS is an income node
        
        # 3. Extract Education Levels
        elif label == 'RESULT_IN':
            education.add(u)
            income_ranges.add(v) # The target of RESULT_IN is an income node

        # 4. Handle other paths leading to income
        elif label in ['PAYS', 'PAYS_DIRECT']:
            income_ranges.add(v)

    # Return as a structured dictionary
    return {
        "categories": sorted(list(categories)),
        "skills": sorted(list(skills)),
        "experience": sorted(list(experience)),
        "education": sorted(list(education)),
        "income": sorted(list(income_ranges)) # <--- New Key added here
    }
def dynamic_multi_hop(G, node1, rel1, node2, rel2):
    res1 = dict(single_hop_query(G, node1, rel1, direction="out"))
    res2 = dict(single_hop_query(G, node2, rel2, direction="out"))
    if not res1 and not res2:
        return None
    common_nodes = set(res1.keys()) | set(res2.keys())
    scores = {node: res1.get(node, 0) + res2.get(node, 0) for node in common_nodes}
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

@app.get("/multihop")
async def get_multihop(node1: str, rel1: str, node2: str, rel2: str):
    results = dynamic_multi_hop(kg, node1, rel1, node2, rel2)
    if not results:
        return {"error": "No data found"}
    return [{"name": item, "weight": weight} for item, weight in results]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)