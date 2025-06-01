import os
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, XSD

# Models to process
models = ['llama3.3']
ontology_folder = "../Ontology/"
concept_relations_folder = "Concepts_relations"

# Namespaces
DLPROV = Namespace("https://w3id.org/dlprov#")
PROV = Namespace("http://www.w3.org/ns/prov#")

# Load concept relations from a file
def load_concept_relations(filepath):
    sections = {'Concepts': [], 'Relationships': [], 'DataProperties': [], 'InverseProperties': []}
    current = None

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue

            if ':' in line and line.split(':')[0] in sections:
                current = line.split(':')[0]
                items = line.split(':')[1].strip().split(', ')
                sections[current].extend(items)
            elif current:
                sections[current].extend(line.split(', '))

    return sections['Concepts'], sections['Relationships'], sections['DataProperties'], sections['InverseProperties']

# Create RDF ontology and save
def create_ontology(model_name, variant, concepts, relationships, data_props, inverse_props):
    g = Graph()
    g.bind("dlprov", DLPROV)
    g.bind("prov", PROV)

    for concept in concepts:
        uri = DLPROV[concept]
        g.add((uri, RDF.type, OWL.Class))
        g.add((uri, RDFS.subClassOf, PROV.Entity))
        g.add((uri, RDFS.label, Literal(concept, datatype=XSD.string)))

    for rel in relationships:
        uri = DLPROV[rel]
        g.add((uri, RDF.type, OWL.ObjectProperty))
        g.add((uri, RDFS.label, Literal(rel, datatype=XSD.string)))

    for dp in data_props:
        uri = DLPROV[dp]
        g.add((uri, RDF.type, OWL.DatatypeProperty))
        g.add((uri, RDFS.label, Literal(dp, datatype=XSD.string)))

    for ip in inverse_props:
        uri = DLPROV[ip]
        g.add((uri, RDF.type, OWL.ObjectProperty))
        g.add((uri, OWL.inverseOf, uri))  # Placeholder; could be customized
        g.add((uri, RDFS.label, Literal(ip, datatype=XSD.string)))

    # Save ontology to disk
    save_path = os.path.join(ontology_folder, model_name, 'Ontology')
    os.makedirs(save_path, exist_ok=True)

    file_name = f"dlprov_{variant}.ttl"
    g.serialize(destination=os.path.join(save_path, file_name), format='turtle')
    print(f"Saved ontology: {os.path.join(save_path, file_name)}")

# Main execution
if __name__ == "__main__":
    variants = ['mp', 'nomp']

    for model in models:
        for variant in variants:
            filename = f"concepts_relations_{variant}.txt"
            rel_path = os.path.join(ontology_folder, model,concept_relations_folder, filename)

            if not os.path.exists(rel_path):
                print(f"Missing: {rel_path}")
                continue

            concepts, relationships, data_props, inverse_props = load_concept_relations(rel_path)
            create_ontology(model, variant, concepts, relationships, data_props, inverse_props)
