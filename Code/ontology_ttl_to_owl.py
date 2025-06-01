import os
from rdflib import Graph

# Models and folder
models = ['llama3.2', 'gemma3', 'llama3.3']
ontology_folder = "../Ontology/"

def convert_ttl_to_owl(model):
    ttl_folder = os.path.join(ontology_folder, model, 'Ontology')

    if not os.path.exists(ttl_folder):
        print(f"Folder not found: {ttl_folder}")
        return

    for file in os.listdir(ttl_folder):
        if file.endswith('.ttl'):
            ttl_path = os.path.join(ttl_folder, file)
            owl_path = os.path.join(ttl_folder, file.replace('.ttl', '.owl'))

            g = Graph()
            g.parse(ttl_path, format='turtle')
            g.serialize(destination=owl_path, format='pretty-xml')

            print(f"Converted {file} to {os.path.basename(owl_path)}")

# Main conversion
if __name__ == "__main__":
    for model in models:
        convert_ttl_to_owl(model)
