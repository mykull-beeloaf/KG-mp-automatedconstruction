import os
import re
import rdflib
from rdflib import Graph, Namespace, Literal, RDF, RDFS, OWL
from urllib.parse import quote

# Define the folders and files paths
ner_root = '../NER_output/'
kg_root = '../KG/'

# Define namespaces
DLPROV = Namespace("https://w3id.org/dlprov#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")


# Function to read named entities from a publication file
def read_named_entities(file_path):
    named_entities = {}
    exclude_phrases = ["Not Specified", "not mentioned", "Not mentioned", "Not Mentioned", "None", "None mentioned",
                       "Not Provided", "Not explicitly stated", "N/A", "none", "not provided", "not explicitly stated",
                       "not explicitly mentioned", "not specified", ]
    try:
        with open(file_path, 'r') as f:
            content = f.read().strip()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return named_entities

    # Split into lines and process
    lines = [line.strip() for line in content.split('\n') if line.strip()]

    for line in lines:
        # Skip header lines
        if line.lower().startswith("Named Entities:"):
            continue

        # Handle both concept(entity, entity) and concept: entity, entity formats
        if '(' in line:
            parts = re.split(r'[\(\)]', line)
            if len(parts) >= 2:
                concept_part = parts[0].strip()
                entities_part = parts[1]
            else:
                continue
        elif ':' in line:
            concept_part, entities_part = line.split(':', 1)
        else:
            continue  # Skip malformed lines

        concept = concept_part.strip()
        entities = [e.strip() for e in entities_part.split(',') if e.strip()]

        # Filter excluded phrases and empty entities
        filtered_entities = [
            entity for entity in entities
            if entity.lower() not in [phrase.lower() for phrase in exclude_phrases]
               and entity != ''
        ]

        if filtered_entities:
            named_entities[concept] = filtered_entities

    return named_entities


def clean_and_encode(entity_name):
    # Remove special characters and normalize
    cleaned = re.sub(r'[\(\)\{\}\<\>]', '', entity_name)
    cleaned = cleaned.replace(' ', '_').replace('/', '_')
    return quote(cleaned)


def create_kg(named_entities):
    g = Graph()
    g.bind("dlprov", DLPROV)
    g.bind("rdfs", RDFS)
    g.bind("owl", OWL)

    for concept, entities in named_entities.items():
        concept_uri = DLPROV[clean_and_encode(concept)]

        # Add concept as both a class and a concept instance
        g.add((concept_uri, RDF.type, OWL.Class))
        g.add((concept_uri, RDF.type, DLPROV.Concept))

        for entity in entities:
            # Handle abbreviations in parentheses
            entity_parts = re.split(r'\s*\(\s*', entity, 1)
            entity_name = entity_parts[0].strip()

            if not entity_name:
                continue

            entity_uri = DLPROV[clean_and_encode(entity_name)]

            # Add entity instance and link to concept
            g.add((entity_uri, RDF.type, concept_uri))
            g.add((entity_uri, RDFS.label, Literal(entity_name)))

            # Handle abbreviations if present
            if len(entity_parts) > 1:
                abbr = entity_parts[1].rstrip(')').strip()
                if abbr:
                    abbr_uri = DLPROV[clean_and_encode(abbr)]
                    g.add((abbr_uri, RDF.type, concept_uri))
                    g.add((abbr_uri, RDFS.label, Literal(abbr)))
                    g.add((entity_uri, DLPROV.hasAbbreviation, abbr_uri))

    return g


def write_kg_to_file(kg, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    kg.serialize(destination=output_file, format='turtle')


def main():
    models = ['llama3.2', 'gemma3', 'llama3.3']
    prompting_types = ['mp', 'nomp']

    for model in models:
        for pt in prompting_types:
            input_dir = os.path.join(ner_root, model, pt)
            output_dir = os.path.join(kg_root, model, pt)

            if not os.path.exists(input_dir):
                print(f"Input directory not found: {input_dir}")
                continue

            for pub_file in os.listdir(input_dir):
                if pub_file.endswith('_ner.txt'):
                    pub_path = os.path.join(input_dir, pub_file)
                    pub_id = pub_file.split('_')[0]  # Extract publication ID

                    print(f"Processing {pub_path}...")
                    entities = read_named_entities(pub_path)

                    if not entities:
                        print(f"No valid entities found in {pub_path}")
                        continue

                    kg = create_kg(entities)

                    # Save KG
                    output_file = os.path.join(output_dir, f"{pub_id}_KG.ttl")
                    write_kg_to_file(kg, output_file)
                    print(f"Created KG: {output_file}")


if __name__ == "__main__":
    main()