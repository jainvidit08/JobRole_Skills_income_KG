Answer Job related Queries using Knowledge Graph (KG) based Recommendation System


Install dependencies:
pip install fastapi uvicorn networkx pandas pyvis


Usage Steps
Step 1: Build the Knowledge Graph

Generate the graph model from your raw dataset (runs once).
python3 src/build_kg.py
(No need right now as pkl file is already provided in src/model)
This generates the knowledge_graph.pkl file.


Step 2: Run Graph Analysis

Evaluate the structural health and density of the graph.
python3 src/analyze_graph.py
This will output the Node Count, Edge Count, and Graph Density metrics.


Step 3: Start the Backend API

Launch the FastAPI server to allow the frontend to communicate with the graph.(/backend)
uvicorn src.app:app --reload --port 8000


Step 4: Access the Frontend

Open the index_single.html/index_multi.html file in your preferred web browser to interact with the Recommendation Engine.(/frontend)
open index_single.html
open index_multi.html

for visualising knowledge graph(/src/model)
open freelancer_kg.html


for preprocessing there are several of preprocessing file in src/preprocessing to make this preprocessing step by step process. File name "final_preprocessing.py" is the final script which do all the process in one go
(/src/preprocessing)
python3 src/model/final_preprocessing.py