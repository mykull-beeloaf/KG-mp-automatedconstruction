import os
import re
import rdflib
import csv
from urllib.parse import unquote
from pathlib import Path

stats_folder = "../Statistics/"
cq_answers_folder = "../CQ_answers/answers_processed"
kg_root = "../KG/"
cq_kg_file = '../CQs/CQs_KG.txt'
models = ['gemma3', 'llama3.2', 'llama3.3']
prompt_types = ['mp', 'nomp']
all_publications = set()

# Create output directory
Path(stats_folder).mkdir(parents=True, exist_ok=True)

def load_cq_answers():
    """Load CQ answers from processed files"""
    cq_data = {}
    for filename in os.listdir(cq_answers_folder):
        match = re.match(r"Publication(\d+)_CQ(\d+)\.txt", filename)

        if match:
            pub_num = match.group(1)
            cq_num = match.group(2)
            all_publications.add(pub_num)
            with open(os.path.join(cq_answers_folder, filename)) as f:
                content = f.read().lower().strip()
                if pub_num not in cq_data:
                    cq_data[pub_num] = {}
                cq_data[pub_num][cq_num] = content
    print(cq_data)
    return cq_data


def get_relevant_cqs():
    """Get list of relevant CQ numbers from KG file"""
    relevant_cqs = []
    with open(cq_kg_file) as f:
        for line in f:
            if line.strip() and ":" in line:
                cq_num = line.split(":")[0][2:]
                relevant_cqs.append(cq_num)
    return relevant_cqs


def extract_kg_instances(kg_file):
    """Extract instances from KG file"""
    g = rdflib.Graph()
    g.parse(kg_file, format="turtle")
    instances = set()

    for s in g.subjects():
        if "#" in s:
            instance = unquote(s.split("#")[-1]).replace("_", " ").lower()
            instances.add(instance)
    return instances


def evaluate_models(cq_data, relevant_cqs):
    """Main evaluation function"""
    results = {}

    # Initialize results structure
    for pub in all_publications:
        results[pub] = {}
        for model in models:
            for pt in prompt_types:
                results[pub][f"{model}_{pt}"] = {"correct": 0, "total": 0}

    # Process each model and prompt type
    for model in models:
        for pt in prompt_types:
            model_dir = os.path.join(kg_root, model, pt)
            if not os.path.exists(model_dir):
                continue

            for kg_file in os.listdir(model_dir):
                if kg_file.endswith(".ttl"):
                    pub_num = re.search(r"pub(\d+)", kg_file).group(1)
                    if pub_num not in cq_data:
                        continue

                    # Get combined CQ answers
                    combined_answers = " ".join(
                        cq_data[pub_num][cq]
                        for cq in relevant_cqs
                        if cq in cq_data[pub_num]
                    )

                    # Extract KG instances
                    kg_path = os.path.join(model_dir, kg_file)
                    kg_instances = extract_kg_instances(kg_path)

                    # Calculate matches
                    correct = sum(1 for inst in kg_instances if inst in combined_answers)
                    total = len(kg_instances)

                    # Store results
                    key = f"{model}_{pt}"
                    results[pub_num][key]["correct"] = correct
                    results[pub_num][key]["total"] = total

    return results


def save_results(results):
    """Save results to CSV with proper publication ordering"""
    output_path = os.path.join(stats_folder, "kg_cq_evaluation_results.csv")
    columns = ["Publication"] + [f"{m}_{pt}" for m in models for pt in prompt_types]

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)

        # Sort publications numerically
        sorted_pubs = sorted(results.keys(), key=lambda x: int(x))

        # Write publication rows
        for pub in sorted_pubs:
            row = [pub]
            for model_pt in columns[1:]:
                res = results[pub][model_pt]
                perc = (res["correct"] / res["total"] * 100) if res["total"] > 0 else 0
                row.append(f"{res['correct']}/{res['total']} ({perc:.2f}%)")
            writer.writerow(row)

        # Add total row
        totals = {model_pt: {"correct": 0, "total": 0}
                  for model_pt in columns[1:]}
        for pub in results.values():
            for model_pt, vals in pub.items():
                totals[model_pt]["correct"] += vals["correct"]
                totals[model_pt]["total"] += vals["total"]

        total_row = ["Total"]
        for model_pt in columns[1:]:
            t = totals[model_pt]
            perc = (t["correct"] / t["total"] * 100) if t["total"] > 0 else 0
            total_row.append(f"{t['correct']}/{t['total']} ({perc:.2f}%)")
        writer.writerow(total_row)


if __name__ == "__main__":
    print("Loading CQ answers...")
    cq_data = load_cq_answers()

    print("Identifying relevant CQs...")
    relevant_cqs = get_relevant_cqs()

    print("Evaluating knowledge graphs...")
    evaluation_results = evaluate_models(cq_data, relevant_cqs)

    print("Saving results...")
    save_results(evaluation_results)

    print("Evaluation complete! Results saved to kg_cq_evaluation_results.csv")