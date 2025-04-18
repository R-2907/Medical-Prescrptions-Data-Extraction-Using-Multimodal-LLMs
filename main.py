import os
import json
from PIL import Image
from tqdm import tqdm
import pandas as pd
from transformers import AutoProcessor, LlavaForConditionalGeneration
import torch

def extract_json_from_llava_output(response):
    try:
        json_start = response.find("{")
        json_end = response.rfind("}") + 1
        json_str = response[json_start:json_end].strip()
        return json.loads(json_str)
    except Exception as e:
        return {}

def main(data_folder="data", output_folder="extracted"):
    os.makedirs(output_folder, exist_ok=True)
    image_files = sorted([f for f in os.listdir(data_folder) if f.endswith(".jpg")])

    # Load model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_id = "llava-hf/llava-1.5-7b-hf"

    processor = AutoProcessor.from_pretrained(model_id)
    model = LlavaForConditionalGeneration.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    ).to(device)

    prompt = """
    You are a medical assistant AI. Given the following prescription image:

    <image>

    Extract ALL the following fields and return in **valid JSON** format:

    {
      "Patient Name": "...",
      "Age": "...",
      "Gender": "...",
      "Date of appointment": "...",
      "Doctor's Name": "...",
      "Doctor's Qualification": "...",
      "Doctor's Registration Number": "...",
      "Hospital/Clinic Name": "...",
      "Hospital/Clinic Address": "...",
      "Hospital Phone Number": "...",
      "Symptoms / Chief Complaints": "...",
      "Diagnosis": "...",
      "Medicines": [
        {"name": "...", "dosage": "...", "frequency": "...", "route": "..."}
      ],
      "Lab Tests / Investigations": "...",
      "Special Instructions": "..."
    }

    If any field is missing or not visible, use null.
    """

    fields = [
        "Patient Name", "Age", "Gender", "Date of appointment",
        "Doctor's Name", "Doctor's Qualification", "Doctor's Registration Number",
        "Hospital/Clinic Name", "Hospital/Clinic Address", "Hospital Phone Number",
        "Symptoms / Chief Complaints", "Diagnosis",
        "Medicines", "Lab Tests / Investigations", "Special Instructions"
    ]

    records = []
    for filename in tqdm(image_files):
        img_path = os.path.join(data_folder, filename)
        img = Image.open(img_path).convert("RGB")

        inputs = processor(text=prompt, images=img, return_tensors="pt").to(device)
        outputs = model.generate(**inputs, max_new_tokens=1024)
        response = processor.batch_decode(outputs, skip_special_tokens=True)[0]
        response = response[response.index('If any field is missing or not visible, use null.'):]
        parsed = extract_json_from_llava_output(response)

        # Save individual JSON
        json_path = os.path.join(output_folder, filename.replace(".jpg", ".json"))
        with open(json_path, "w") as f:
            json.dump(parsed, f, indent=2)

        # Read back JSON and collect structured row
        if not os.path.exists(json_path):
            continue

        with open(json_path, "r") as f:
            parsed = json.load(f)

        row = {"filename": filename}
        for field in fields:
            value = parsed.get(field, "null")
            if isinstance(value, (list, dict)):
                value = json.dumps(value)
            row[field] = value if value != "" else "null"

        records.append(row)

        del inputs, outputs, img
        torch.cuda.empty_cache()

    df = pd.DataFrame(records)
    df.to_csv("extracted_prescriptions.csv", index=False)
    print("Extraction complete. Files saved: JSON and CSV.")

if __name__ == "__main__":
    data_folder = "data"
    output_folder = "extracted"
    main(data_folder, output_folder)