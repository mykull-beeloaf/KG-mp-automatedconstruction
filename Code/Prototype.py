from ollama import generate
from ollama import Client
import json


def communicate(prompt):
    response = generate('llama3.2', prompt)
    # response = generate('deepseek-r1', prompt)
    # response = generate('gemma3', prompt)
    return response['response']

# (Kojima et al., 2022)
# Addition to a basic query
def step_by_step():
    return "Let's think step by step."

# Zero-shot Plan-and-Solve (PS) prompting (Wang et al., 2023a)
# Adding to the end of the question
def plan_and_solve_prompt():
    return "Let’s first understand the problem and devise a plan to solve the problem. Then, let’s carry out the plan and solve the problem step by step."


def mp_template_ontology_prompt():
    return f"""As you perform this task, follow these steps (and comment on them): 
    1. Understand the context and the meanings between questions and answers, along with their 
    potential interactions.
    2. Make a preliminary identification of the relationships between entities and provide
    preliminary answer in this form (Example: DeepLearningModel(CNN, RNN, Transformer), Framework(TensorFlow, PyTorch), PerformanceMetric(Accuracy, mean IoU)).
    3. Critically assess your preliminary analysis. If you feel unsure about your initial 
    relationships, try to reassess it.
    4. Confirm your final answer and explain the reasoning behind your decisions."""

def mp_template_medical_prompt(sentence, item_1, item_2):
    return f"""Given the context sentence “{sentence}”, identify the relationship between 
    the pharmacological substances “{item_1}” and “{item_2}” within the sentence. Classify 
    the relationship under one of these categories: Advice, Effect, Mechanism, or Int. {plan_and_solve_prompt()} As you 
    perform this task, follow these steps: 
    1. Understand the context and the meanings of the two substances, along with their potential
     interactions.
    2. Make a preliminary identification of the relationship between two substances.
    3. Critically assess your preliminary analysis. If you feel unsure about your initial
    relationship, try to reassess it.
    4. Confirm your final answer and explain the reasoning behind your decision. 
    5. Evaluate your confidence (0-100%) in your analysis and provide an explanation for this 
    confidence level.
    6. Provide your final answer as one word among Advice, Effect, Mechanism, or Int.
"""

# {mp_template_ontology_prompt()}
def mp_ontology_extraction():
    return f"""Your task is to do Named Entity Recognition. You extract named entities from the provided competency question answers. 
Use provided concepts to understand which named entities to extract from competency answers. 
Concepts: Method, RawData, DataFormat, DataAnnotationTechnique, DataAugmentationTechnique, Dataset, PreprocessingStep, DataSplitCriteria, CodeRepository, DataRepository, CodeRepositoryLink, DataRepositoryLink, DeepLearningModel, Hyperparameter, HyperparameterOptimization, OptimizationTechnique, TrainingCompletionCriteria, RegularizationMethod, ModelPerformanceMonitoringStrategy, Framework, HardwareResource, PostprocessingStep, PerformanceMetric, GeneralizabilityMeasure, RandomnessStrategy, ModelPurpose, DataBiasTechnique, ModelDeploymentProcess, DeploymentPlatform.         
Example: DeepLearningModel(CNN, RNN, Transformer), Framework(TensorFlow, PyTorch), PerformanceMetric(Accuracy, mean IoU)
{plan_and_solve_prompt()} {mp_template_ontology_prompt()} Below are the competency questions and answers:

CQ: What data formats are used in the deep learning pipeline (e.g, image, audio, video, csv)?
Answer: The deep learning pipeline uses audio and image data formats. The audio data is presented as spectrograms, while the image data is presented as image crops around the object of interest, with contrast enhancement and consecutive frame differences.

CQ: What are the data augmentation techniques applied in the deep learning pipeline (e.g, Flipping, Rotating, Scaling)?
Answer: The provided context does not mention any specific data augmentation techniques applied in the deep learning pipeline. Therefore, I cannot provide a helpful answer to this query.

CQ: What are the datasets used in the deep learning pipeline (e.g, MNIST, CIFAR, ImageNet)?
Answer: The paper does not explicitly mention the use of any specific datasets such as MNIST, CIFAR, or ImageNet. However, it does mention that the deep learning pipeline uses large amounts of labeled data produced by analysts using the UI. This data is used to classify dozens of species signals and event types across ongoing projects. The paper also mentions the use of deep convolutional neural networks (CNNs) and deep feed forward neural networks (DNNs) to audio spectrogram and image data. This suggests that the datasets used in the deep learning pipeline are likely audio and image data related to biodiversity monitoring.

CQ: What preprocessing steps are involved before training a deep learning model (e.g., normalization, scaling, cleaning)?
Answer: The context does not provide specific information on the preprocessing steps involved before training a deep learning model. However, common preprocessing steps for deep learning models include normalization, scaling, cleaning, and augmentation of the data. Normalization and scaling help to bring the data to a similar scale, cleaning helps to remove any noise or irrelevant data, and augmentation helps to increase the size of the dataset.

CQ: What is the code repository link of the deep learning pipeline (e.g., Link to GitHub, GitLab, BitBucket)?
Answer: I'm sorry, the provided context does not include the code repository link of the deep learning pipeline.

CQ: What type of deep learning model is used in the pipeline (e.g., CNN, RNN, Transformer)?
Answer: The pipeline uses deep convolutional neural networks (CNNs) and deep feed forward neural networks (DNNs) to audio spectrogram and image data.

CQ: What are the hyperparameters used in the deep learning model (e.g., learning rate, optimizer)?
Answer: The paper does not provide information on the hyperparameters used in the deep learning model, such as learning rate or optimizer.

CQ: What optimization techniques are applied in the deep learning pipeline (e.g., SGD, Adam)?
Answer: The provided context does not mention any specific optimization techniques applied in the deep learning pipeline, such as SGD (Stochastic Gradient Descent) or Adam.

CQ: What are the regularization methods used to prevent overfitting  in the deep learning pipeline (e.g., dropout, L2 regularization)?
Answer: The provided context does not mention any specific regularization methods used to prevent overfitting in the deep learning pipeline.

CQ: Which frameworks are used to build the deep learning model (e.g., TensorFlow, PyTorch)?
Answer: The context does not provide information on the specific frameworks used to build the deep learning model.

CQ: Which hardware resources are used for training the deep learning model (e.g., GPUs, TPUs)?
Answer: The context does not provide information on the specific hardware resources used for training the deep learning model.

CQ: What metrics are used to evaluate the performance of the deep learning model (e.g., accuracy, precision, recall)?
Answer: The context does not provide information on the specific metrics used to evaluate the performance of the deep learning model.

CQ: What is the purpose of the deep learning model (e.g., classification, segmentation, detection)?
Answer: The purpose of the deep learning model is to classify the presence or absence and activity rates of a number of different endangered species, or in some cases, the sounds of birds colliding with energy infrastructure. In total, the model has the ability to classify dozens of species signals and event types across ongoing projects, and aims to scale this up to encompass whole communities.

Provide your answer as follows:
        Named Entities: For each provided Concept(Corresponding Named Entity,..), ..."""

def main():

    prompt_ontology = (mp_ontology_extraction())

    prompt_med = (mp_template_medical_prompt("""Impaired renal function has been 
    described in bone marrow transplant patients who were conditioned with high-dose 
    intravenous melphalan and who subsequently received cyclosporin to prevent 
    graft-versus-host disease.""", "melphalan", "cyclosporin"))

    prompt = prompt_ontology
    response = communicate(prompt)
    print("Prompt:", prompt)
    print("Model Response:", response)

main()