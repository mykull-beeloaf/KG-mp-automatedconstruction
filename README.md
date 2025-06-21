# Improving the LLM assisted KG construction
This is an implementation of my Bachelor's Thesis on the topic "Does Metacognitive Prompting Improve the Accuracy of Semi-Automated Construction of Knowledge Graphs?"

This repository contains code, data, prompts and results related to the (semi-)automatic pipeline of Ontology and Knowledge Graph Construction with three different Large Language Models (LLMs): Llama3.2-4B, Llama3.3-70B-Instruct, Gemma3-4B

## Overview
This project and code is largely an inspired and re-imlemented version of [LLM assisted KG construction Repository](https://github.com/fusion-jena/automatic-KG-creation-with-LLM/tree/master)
In this project, we are exploring the potential of improving the utilization Large Language Models (LLMs) to generate Knowledge Graphs (KGs) with Metacognitive Prompting (MP). This work explores the (semi-)automatic construction of KGs facilitated by different Open-source LLMs. This pipeline involves formulating competency questions (CQs), developing an ontology (TBox) based on these CQs, constructing KGs using the developed ontology, and evaluating the resultant KG with minimal to no involvement of human experts. The results of our research did not show any MP effect on the pipeline.

## Contents
* CQs/: Contains the competency questions from the previous research
* Code/: Contains code files for data preprocessing, competency questions, ontology and KG generation, and evaluation of KGs for our LLMs, modified from the previous research
* Data/: Contains the selected publication pdfs and their metadata from the previous research
* Evaluation/: Contains human evaluations of RAG-generated CQ answers from the previous research
* KG/: Contains individual KG for 7 publications for 3 LLMs with/out MP prompting variant
* NER/: Contains NERs for all the competency answers for 3 LLMs with/out MP prompting variant
* NER_prompt/: Contains the prompts for all the selected publications, which have the instructions that are passed to different LLMs to extract named entities, modified from the previous research
* Ontology/: Contains generated ontologies from three SOTA LLMs with/out MP prompting variant
* RAG_CQ_Ans/: Contains the RAG-generated answers for 13 queries (selected publication)  modified from the previous research
* Stats/: Contains all the stats generated for this publication (ontology stats, KG individual counts and others as described in manuscript)
