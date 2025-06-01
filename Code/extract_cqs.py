from ollama_model_generator import Model

mp = """As you perform this task, follow these steps:
1. Clarify your understanding of the questions.
2. Make a preliminary identification of the concepts, relationships, data properties and inverse properties in the questions.
3. Critically assess your preliminary analysis. If you feel unsure about your initial identification, try to reassess it.
4. Confirm your final answer and explain the reasoning behind your choice.
5. Evaluate your confidence (0-100%) in your analysis and provide an explanation for this confidence level.
"""

prompt_ms = ['', mp]
models = ['llama3.2', 'gemma3']

# Function that provides a set up for the model to know its task, as well as to pass the prompt
def extract_ontology(model_name, prompt_modifier):
    # Step 1: Instantiate the models, provide the system task
    system_prompt = """You are an ontology extraction system. Your task is to analyze competency questions (CQs) and identify all the concepts, relationships, data properties, and inverse properties between concepts mentioned in the text. 
These elements will be used to build ontology for describing the provenance of a Deep Learning Pipeline. If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Don't provide anything other than the results in a comma separated list. Do not reply using a complete sentence. Only give the answer in the following format.
    
Example of provided CQs:
CQ1: What hyperparameters are used in the model?
CQ2: What data formats are used in the deep learning pipeline?
CQ3: What are the sources of input data for the deep learning pipeline?
CQ4: Who are the authors of the deep learning model?
CQ5: When was the model trained?
CQ6: What is the accuracy of the model?
    
Example of your response:
Concepts: Hyperparameter, Model, Data, DataFormat, DeepLearningPipeline, Source, InputData, Author, TrainingDate, Accuracy
Relationships: hasHyperparameter, hasModel, hasData, hasDataFormat, hasSource, hasInputData, hasAuthor, hasTrainingDate, hasAccuracy
DataProperties: authorName, trainingDate, modelAccuracy
InverseProperties: isHyperparameterOf, isModelOf, isDataOf, isDataFormatOf, isSourceOf, isInputDataOf, isAuthorOf, isTrainingDateOf, isAccuracyOf
    """

    model = Model(model_name=model_name, system_prompt=system_prompt)

    # Step 2: Creating 4 ontologies (LLM1+MP, LLM1+NoMp, LLM2+MP, LLM2+NoMP)

    cq_prompt = f"""Analyze the following competency questions and identify all the concepts, relationships, 
data properties, and inverse properties between concepts mentioned in the text: 
    
CQ1:What data formats are used in the deep learning pipeline?
CQ2:What are the data augmentation techniques applied in the deep learning pipeline?
CQ3:What are the datasets used in the deep learning pipeline?
CQ4:What preprocessing steps are involved before training a deep learning model?
CQ5:What is the code repository link of the deep learning pipeline?
CQ6:What type of deep learning model is used in the pipeline?
CQ7:What are the hyperparameters used in the deep learning model?
CQ8:What optimization techniques are applied in the deep learning pipeline?
CQ9:What are the regularization methods used to prevent overfitting  in the deep learning pipeline?
CQ10:Which frameworks are used to build the deep learning model?
CQ11:Which hardware resources are used for training the deep learning model?
CQ12:What metrics are used to evaluate the performance of the deep learning model?
CQ13:What is the purpose of the deep learning model? {prompt_modifier}

Please provide your final response as:
    
Concepts: (concepts in comma separated list)
Relationships: (relationships in comma separated list)
DataProperties: (data properties in comma separated list)
InverseProperties: (inverse properties in comma separated list).
"""

    return model.chat(cq_prompt)

if __name__ == "__main__":

    # Iterating over 2 models x MP/NoMP approach
    for model_name in models:
        for prompt_modifier in prompt_ms:
            response = extract_ontology(model_name, prompt_modifier)
            if prompt_modifier == prompt_ms[1]:
                print(f"Output by {model_name} with MP:\n", response)
            else:
                print(f"Output by {model_name} without MP:\n", response)

