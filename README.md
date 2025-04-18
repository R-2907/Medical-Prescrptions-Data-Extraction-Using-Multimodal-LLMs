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

This project uses a **field coverage-based evaluation**, which assesses how often the model successfully extracts a non-null value for each expected field across all images.

***Coverage(field) = (Number of non-null entries for the field / Total number of rows) × 100***

| Field                         | Coverage (%) |
|------------------------------|---------------|
| Age                          | 65.89%        |
| Gender                       | 65.89%        |
| Symptoms / Chief Complaints  | 68.99%        |
| Diagnosis                    | 68.22%        |
| Lab Tests / Investigations   | 40.31%        |
| Medicines                    | 68.99%        |

These fields were specifically chosen because of their relevance out of the **16 columns** available in `extracted_predictions.csv`.

### Data Analysis and Insights

Here are some insights and data analysis on few columns, which seemed relevant for future analysis.

#### Gender

![Gender](/photos/gender.png)

| Gender                         | Frequency and % |
|------------------------------|---------------|
| Male                          | 53 (41.09%)        |
| Female                       | 32 (24.81%)        |
| Null                       | 44 (35.48%)        |

#### Patient's Age Distribution

![Age](/photos/age.png)

| Age Distribution                         | Count |
|------------------------------|---------------|
| 0-20                          | 8        |
| 21-40                       | 58        |
| 41-60                       | 8        |
| 61-80                       | 10        |
| 81-100                       | 1        |

#### Symptoms/Chief Complaints Distribution

![Symptoms](/photos/symptoms.png)

| Symptoms Distribution (top 5)                         | Frequency and % |
|------------------------------|---------------|
| Fever                          | 25 (62.5%)        |
| Headache                       | 5 (12.5%)        |
| Fever, Cough, Soar Throat                       | 4 (10%)        |
| Cough                       | 3 (7.5%)        |
| Pain                       | 3 (7.5%)        |

Total unique symptoms recorded (among non-null values): **49**

#### Diagnosis Frequencies

| Diagnosis (top 20)                    | Count |
|-----------------------------|-------|
| Fever                       | 18    |
| Common Cold                 | 7     |
| Migraine                    | 5     |
| Asthma                      | 4     |
| Flu                         | 4     |
| Common cold                 | 3     |
| Influenza                   | 2     |
| Anxiety                     | 2     |
| Lipoma                      | 2     |
| Dyspnea                     | 1     |
| Liposomal Amphotericin B    | 1     |
| Appendicitis                | 1     |
| MBC                         | 1     |
| Phosphate deficiency        | 1     |
| Myocardial infarction       | 1     |
| Temporal bone fracture      | 1     |
| Pain abdomen                | 1     |
| Cocaine addiction           | 1     |
| Angina                      | 1     |
| Hypertension                | 1     |

Total unique diagnosis recorded (among non-null values): **50**

#### Lab Tests/Investigations Frequencies

| Lab Test / Investigation   | Count |
|----------------------------|-------|
| Blood test                 | 19    |
| Blood Culture              | 3     |
| Blood tests                | 3     |
| EKG                        | 2     |
| MRI                        | 2     |
| Blood Test                 | 2     |
| Chest X-ray                | 2     |
| X-ray                      | 1     |
| Ultrasound                 | 1     |
| EKG, Chest X-ray           | 1     |

Total unique lab tests recorded (among non-null values): **26**

#### Top 10 Medicines (based on frequencies in the dataset):

| Medicine Name   | Frequency |
|-----------------|-----------|
| Paracetamol     | 11        |
| Amoxicillin     | 10        |
| Aspirin         | 4         |
| Cetirizine      | 3         |
| Caffeine        | 2         |
| Crocin          | 2         |
| Ibuprofen       | 2         |
| Rosuvastatin    | 2         |
| Lipitor         | 2         |
| Tylenol         | 2         |

#### Top Modes of medication:

| Medication Method  |  Count  |
|--------------------|---------|
| Oral  |  85  |
| po  |  2  |
| injection  |  2  |
| iv  |  1  |
| intravenous  |  1  |


If we use **OCR engines (like Tesseract)** along with **Multimodal LLMs or Vision LLMs** (basically a hybrid approach), the output can be significantly more accurate as compared to solely relying on Multimodal LLMs.
