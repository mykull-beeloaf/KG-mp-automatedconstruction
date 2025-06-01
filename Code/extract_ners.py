import os
from ollama_model_generator import Model


def load_concepts(model_name, variant):
    """Load concepts from the generated ontology files"""
    concepts_file = f"../Ontology/{model_name}/Concepts_relations/concepts_relations_{variant}.txt"
    try:
        with open(concepts_file, 'r') as f:
            lines = f.readlines()
            # Extract concepts from first line
            concepts_line = lines[0].strip().replace("Concepts: ", "")
            return concepts_line.split(", ")
    except FileNotFoundError:
        print(f"Concepts file not found: {concepts_file}")
        return []


def read_pub_file(pub_number, model_name, variant):
    """Read the complete publication file with all CQs and answers"""
    file_path = f"../NER_prompts/{model_name}/{variant}/pub{pub_number}.txt"
    try:
        with open(file_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Publication file not found: {file_path}")
        return None


def generate_ner_prompt(concepts, pub_content, mp_instruction=""):
    """Generate the NER prompt with dynamic concepts and publication content"""
    if not concepts:
        return "Error: No concepts loaded"

    if not pub_content:
        return "Error: No publication content"

    prompt = """You extract named entities from the provided competency question (CQ) answers. Use the following provided concepts to understand which named entities to extract from competency answers (CA). Structure your answer to include all the relevant entities from answers in the concept category. \nConcepts: """
    prompt += ", ".join(concepts) + "\n\n"

    prompt += "CAs and CQs: \n"
    prompt += pub_content + "\n\n"

    if mp_instruction:
        prompt += mp_instruction + "\n\n"

    prompt += "Now provide the named entities in the required format and using the following concepts:"
    prompt += ", ".join(concepts) + "\n\n"
    prompt += "\nFor each provided Concept(Corresponding Named Entity,..), ... "
    prompt += """\n\nExample of the output with example concepts:
Named Entities: 
DataFormat(...)
Dataset(...)
DeepLearningModel(convolutional neural network (CNN))
Hyperparameter(number of units in the two FC layers, dropout rate)
RegularizationMethod(dropout)
Framework(TensorFlow, Keras)
PerformanceMetric(accuracy, multiclass recall rate, multiclass precision, F1-score)
ModelPurpose(family-level classification of below-ground bulk samples of Coleoptera) """

    return prompt


def perform_ner(model_name, variant, pub_numbers, mp_instruction=""):
    """Perform NER on publication files using specified model and variant"""
    concepts = load_concepts(model_name, variant)
    model = Model(model_name=model_name,
                  system_prompt='Your task is to do Named Entity Recognition. You extract named entities from the provided competency question answers. Use provided concepts to understand which named entities to extract from competency answers.')
    for pub in pub_numbers:
        pub_content = read_pub_file(pub, model_name, variant)
        if not pub_content:
            continue

        prompt = generate_ner_prompt(concepts, pub_content, mp_instruction if variant == "mp" else "")

        # Get NER results from model
        ner_results = model.chat(prompt)

        # Save results
        os.makedirs(f"../NER_output/{model_name}/{variant}", exist_ok=True)
        with open(f"../NER_output/{model_name}/{variant}/pub{pub}_ner.txt", 'w') as f:
            f.write(ner_results)


if __name__ == "__main__":
    mp_instruction = """As you perform this task follow the following steps:
1. Clarify your understanding of the questions.
2. Make a preliminary identification of the concepts, relationships, data properties and inverse properties in the questions.
3. Critically assess your preliminary analysis. If you feel unsure about your initial identification, try to reassess it.
4. Confirm your final match with your output"""

    models = ['llama3.2', 'gemma3']
    variants = ['mp', 'nomp']
    pub_numbers = [1, 3, 5, 7, 8, 9, 10]

    # Run NER for all combinations
    for model_name in models:
        for variant in variants:
            perform_ner(
                model_name=model_name,
                variant=variant,
                pub_numbers=pub_numbers,
                mp_instruction=mp_instruction
            )