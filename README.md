# Medical-Prescrptions-Data-Extraction-Using-Multimodal-LLMs
ICMR ASSIGNMENT-Medical Prescriptions Image Data Extraction using Multimodal LLMs (LLaVa 1.5-7B Model)

## Table of Contents

- [Objective](#objective)
- [Extraction Pipeline](#extraction-pipeline)
- [Evaluation Metrics](#evaluation-metrics)
- [Data Analysis and Insights](#data-analysis-and-insights)

### Objective
The goal of this project is to take a dataset containing hardwritten medical prescriptions collected from various sources and extracting as much useful information as possible from them using Multimodal LLMs.

The dataset used in this project is present here: [Medical Prescriptions Image Dataset](https://www.kaggle.com/datasets/mehaksingal/illegible-medical-prescription-images-dataset)

The model used in the code here: [LLaVa 1.5-7B](https://huggingface.co/llava-hf/llava-1.5-7b-hf)

Other models suitable for this task
- BLIP-2
- MiniGPT-4
- PaliGemma 2 Mix (Developed by Google, excels in OCR, visual question answering, image captioning and object detection)
- BioMistral (Excels in medical question-answering tasks, supports multilingual evaluations, pretrained on PubMed Central)
- OpenBioLLM-70B

### Extraction Pipeline

![Extraction Pipeline](/photos/pipeline.png)

As you can clearly see, the above extraction pipeline will execute for each and every image available in the dataset. 

Steps are as follows:
- Single image is taken from the dataset
- Prompt is created (using prompt engineering where the output structure is specified, i.e. structured json for future use along with the <image> token, because that's how LLaVa Model expects its input)
- Response is parsed to extract the output JSON which is stored in `/extracted` folder for each image
- JSON is parsed and relevant data is stored in CSV file (`extracted_predictions.csv`)

### Evaluation Metrics


### Data Analysis and Insights
