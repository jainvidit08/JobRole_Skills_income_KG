import pandas as pd
import networkx as nx
from pyvis.network import Network
import os

def create_knowledge_graph(file_path):
    # Load the cleaned data
    df = pd.read_csv(file_path)
    
    # Initialize a Directed Graph
    G = nx.DiGraph()

    for _, row in df.iterrows():
        # 1. Get row values
        cat = str(row['category'])
        exp_lvl = str(row['experience_level'])
        edu = str(row['education'])
        inc_range = str(row['annual_income_range'])
        
        # Handle skills (assuming they are stored as a string representation of a list)
        # We use eval() or strip/split to get the actual list
        skills = eval(row['primary_skills']) if isinstance(row['primary_skills'], str) else row['primary_skills']

        # 2. Build Relationships (Edges)
        # Relationship: Skill -> Category
        for skill in skills:
            if G.has_edge(skill, cat):
                G[skill][cat]['weight'] += 1
            else:
                G.add_node(skill, type='skill')
                G.add_node(cat, type='category')    
                G.add_edge(skill, cat, weight=1, label='PART_OF')
        
        # Skill -> Income Range
        # This helps answer: "How much does knowing Python actually pay?"
        for skill in skills:
            if G.has_edge(skill, inc_range):
                G[skill][inc_range]['weight'] += 1
            else:
                G.add_node(skill, type='skill')
                G.add_node(inc_range, type='income')
                G.add_edge(skill, inc_range, weight=1, label='PAYS_DIRECT')

        # Education -> Income Range 
        # This helps answer: "Does a Master's degree lead to the 125k+ tier?"
        if G.has_edge(edu, inc_range):
            G[edu][inc_range]['weight'] += 1
        else:
            G.add_node(edu, type='education')
            G.add_node(inc_range, type='income')
            G.add_edge(edu, inc_range, weight=1, label='RESULT_IN')

        # Education -> Category 
        # This helps answer: "Which degree is most common for AI/ML Engineering?"
        if G.has_edge(edu, cat):
            G[edu][cat]['weight'] += 1
        else:
            G.add_node(edu, type='education')
            G.add_node(cat, type='category')
            G.add_edge(edu, cat, weight=1, label='QUALIFIES_FOR')

        # Relationship: Category -> Income Range
        if G.has_edge(cat, inc_range):
            G[cat][inc_range]['weight'] += 1
        else:
            G.add_node(inc_range, type='income')
            G.add_node(cat, type='category')
            G.add_edge(cat, inc_range, weight=1, label='PAYS')

        # Relationship: Experience Level -> Income Range
        if G.has_edge(exp_lvl, inc_range):
            G[exp_lvl][inc_range]['weight'] += 1
        else:
            G.add_node(inc_range, type='income')
            G.add_node(exp_lvl, type='exp')
            G.add_edge(exp_lvl, inc_range, weight=1, label='EARNS')

    return G

def visualize_graph(G, output_file):
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)

    # Color mapping
    color_map = {
        'skill': 'orange',
        'category': 'blue',
        'education': 'green',
        'income': 'red',
        'experience': 'purple'
    }

    # Add nodes manually with colors
    for node, data in G.nodes(data=True):
        node_type = data.get('type', 'default')
        color = color_map.get(node_type, 'gray')
        
        net.add_node(node, label=node, color=color)

    # Add edges
    for source, target, data in G.edges(data=True):
        net.add_edge(source, target, value=data.get('weight', 1), title=data.get('label', ''))

    net.toggle_physics(True)
    net.show(output_file, notebook=False)

    print(f"Graph visualization saved to {output_file}")

if __name__ == "__main__":
    INPUT_FILE = os.path.join('..','..', 'data','processed', 'cleaned_dataset.csv')
    OUTPUT_HTML = "freelancer_kg.html"
    
    if os.path.exists(INPUT_FILE):
        kg = create_knowledge_graph(INPUT_FILE)
        visualize_graph(kg, OUTPUT_HTML)
    else:
        print("Cleaned dataset not found.")