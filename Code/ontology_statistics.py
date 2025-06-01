import os
import csv
from pathlib import Path
from rdflib import Graph, Namespace, RDF, OWL

# Your models
models = ['llama3.2','gemma3', 'llama3.3']
ontology_folder = "../Ontology/"
output_csv = "../Statistics/ontology_statistics.csv"

# Ensure output folder exists
Path(os.path.dirname(output_csv)).mkdir(parents=True, exist_ok=True)


def count_axioms(ontology_file):
    g = Graph()
    g.parse(ontology_file, format="turtle")

    class_count = len(set(g.subjects(RDF.type, OWL.Class)))
    object_prop_count = len(set(g.subjects(RDF.type, OWL.ObjectProperty)))
    data_prop_count = len(set(g.subjects(RDF.type, OWL.DatatypeProperty)))
    subclassof_axioms = len(list(g.triples((None, RDF.type, OWL.Class))))
    total_axioms = len(g)

    return class_count, object_prop_count, data_prop_count, subclassof_axioms, total_axioms


def calculate_statistics_for_models(models):
    statistics = []

    for model in models:
        model_folder = os.path.join(ontology_folder, model, 'Ontology')
        if not os.path.isdir(model_folder):
            print(f"Ontology folder not found for {model}, skipping.")
            continue

        for file in os.listdir(model_folder):
            if file.endswith(".ttl"):
                file_path = os.path.join(model_folder, file)
                variant = file.replace("dlprov_", "").replace(".ttl", "")

                cls, obj_props, data_props, subclass_axioms, total = count_axioms(file_path)

                statistics.append({
                    'Model': model,
                    'Variant': variant,
                    'Classes': cls,
                    'Object_Properties': obj_props,
                    'Data_Properties': data_props,
                    'SubClassOf_Axioms': subclass_axioms,
                    'Total_Axioms': total
                })

    return statistics


def write_statistics_to_csv(statistics):
    fieldnames = ['Model', 'Variant', 'Classes', 'Object_Properties', 'Data_Properties', 'SubClassOf_Axioms',
                  'Total_Axioms']

    with open(output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(statistics)

    print(f"Ontology statistics saved to: {output_csv}")


# Run the script
if __name__ == "__main__":
    stats = calculate_statistics_for_models(models)
    write_statistics_to_csv(stats)
