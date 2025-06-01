import os
from ollama_model_generator import Model

models = ['llama3.2', 'gemma3']
variants = ['mp', 'nomp']
base_path = '../Ontology/'

mp_instruction = """As you perform this task, follow these steps:
1. Clarify your understanding of the provided concepts, relationships, properties and inverse relationships.
2. Make a preliminary ontology in the specified format.
3. Critically assess your preliminary analysis. If you feel unsure about your initial identification, try to reassess it.
4. Confirm your final answer and explain the reasoning behind your choice.
5. Evaluate your confidence (0-100%) in your analysis and provide an explanation for this confidence level.
"""

system_prompt = """You are an ontology construction system. Build an ontology with classes, object properties, data properties, and axioms in Turtle (TTL) format for describing the provenance of Deep Learning Pipeline using the competency questions.

Key requirements:
1. Use the base IRI: <https://w3id.org/dlprovenance/>
2. Reuse PROV-O ontology classes and properties (prefix prov: <http://www.w3.org/ns/prov#>)
3. Include proper prefixes for all standard vocabularies
4. Structure the ontology with:
   - Class definitions (subclass of prov:Entity where appropriate)
   - Object properties with domains and ranges
   - Data properties
   - Inverse properties where specified
   - Axioms as needed

Format requirements:
- Must be valid Turtle syntax
- Include all required prefixes
- Each class/property on a new line
- Proper indentation
- Include rdfs:label for all elements

Example output format:

@prefix dlprov: <https://w3id.org/dlprov#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

dlprov:CodeRepository a owl:Class ;
    rdfs:label "CodeRepository"^^xsd:string ;
    rdfs:subClassOf prov:Entity .

dlprov:DataAugmentationTechnique a owl:Class ;
    rdfs:label "DataAugmentationTechnique"^^xsd:string ;
    rdfs:subClassOf prov:Entity .

dlprov:DataFormat a owl:Class ;
    rdfs:label "DataFormat"^^xsd:string ;
    rdfs:subClassOf prov:Entity .

dlprov:Dataset a owl:Class ;
    rdfs:label "Dataset"^^xsd:string ;
    rdfs:subClassOf prov:Entity .

dlprov:DeepLearningModel a owl:Class ;
    rdfs:label "DeepLearningModel"^^xsd:string ;
    rdfs:subClassOf prov:Entity .

dlprov:DeepLearningPipeline a owl:Class ;
    rdfs:label "DeepLearningPipeline"^^xsd:string ;
    rdfs:subClassOf prov:Entity .
"""


def load_concept_file(filepath):
    data = {}
    with open(filepath, 'r') as f:
        lines = f.readlines()
    current = None
    for line in lines:
        line = line.strip()
        if not line: continue
        if ':' in line:
            key, values = line.split(':', 1)
            current = key.strip()
            data[current] = values.strip()
        elif current:
            data[current] += ', ' + line.strip()
    return data


def validate_ttl(content):
    """Basic validation of TTL content"""
    required_prefixes = [
        '@prefix dlprov:',
        '@prefix owl:',
        '@prefix rdfs:'
    ]
    return all(prefix in content for prefix in required_prefixes)


def extract_ontology(model_name, variant):
    rel_path = os.path.join(base_path, model_name, "Concepts_relations", f"concepts_relations_{variant}.txt")
    if not os.path.exists(rel_path):
        print(f"Missing file: {rel_path}")
        return None

    sections = load_concept_file(rel_path)
    modifier = mp_instruction + "\n\n" if variant == "mp" else ""

    # Format structured prompt
    concepts = f"Concepts: {sections.get('Concepts', '')}"
    relations = f"Relationships: {sections.get('Relationships', '')}"
    data_props = f"DataProperties: {sections.get('DataProperties', '')}"
    inverse_props = f"InverseProperties: {sections.get('InverseProperties', '')}"

    user_prompt = (
        f"Generate a complete PROV-O based ontology in Turtle (TTL) format using these elements:\n"
        f"{concepts}\n{relations}\n{data_props}\n{inverse_props}\n\n"
        f"{modifier}"
        "Important: Only respond with the valid Turtle syntax ontology, no additional commentary or explanation."
    )

    # Send to model
    model = Model(model_name=model_name, system_prompt=system_prompt)
    output = model.chat(user_prompt)

    # Validate and clean output
    if '```' in output:  # Remove markdown code blocks if present
        output = output.split('```')[1].strip()
        if output.startswith('ttl'):
            output = output[3:].strip()

    if not validate_ttl(output):
        print(f"Warning: Generated ontology may not be valid TTL for {model_name}-{variant}")

    # Save output to .ttl file
    save_folder = os.path.join(base_path, model_name, "Ontology")
    os.makedirs(save_folder, exist_ok=True)
    filename = f"llm_generated_{variant}.ttl"  # Changed to .ttl
    save_path = os.path.join(save_folder, filename)

    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"Saved ontology to {save_path}")
    return output


if __name__ == "__main__":
    for model in models:
        for variant in variants:
            print(f"\nPrompting {model} ({variant.upper()})")
            extract_ontology(model, variant)