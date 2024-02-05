import json
import os

from stability_ai import text_to_image
from add_text import add_text_to_panel
from fastapi import FastAPI
from fastapi.testclient import TestClient
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

STYLE = "manga, uncolored"

app = FastAPI()

model_name = 'tuner007/pegasus_paraphrase'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)

@app.post("/")
async def receive_post_data(json_data: dict):
    # Access values from the parsed JSON data
    panelNum = json_data.get("panel", "")
    description = json_data.get("description", "")
    text = json_data.get("text", "")
    paraphaseOrNot = json_data.get("paraphase", "")

    panel_prompt = description + ", cartoon box, " + STYLE
    panel_image = text_to_image(panel_prompt)

    if paraphaseOrNot == 0:
        panel_image_with_text = add_text_to_panel(text, panel_image)
    else:
        batch = tokenizer.prepare_seq2seq_batch(str(text), truncation=True, padding='longest', max_length=60,
                                                return_tensors="pt").to(torch_device)
        translated = model.generate(**batch, max_length=60, num_beams=10, num_return_sequences=1)
        paraphrased_text = tokenizer.batch_decode(translated, skip_special_tokens=True)

        panel_image_with_text = add_text_to_panel(paraphrased_text[0], panel_image)

    panel_image_with_text.save(f"output/panel-{panelNum}.png")

    return {"message": "Operation successful"}

# Testing the FastAPI endpoint
client = TestClient(app)

def test_receive_post_data():
  test_data = {
    "panel": 3,
    "description": "A girl and guy looking at each other shyly",
    "text": "I think love you dear yes.",
    "paraphase": 0
  }
  response = client.post("/", json=test_data)
  assert response.status_code == 200
  assert response.json() == {"message": "Operation successful"}

    # return {"description": description, "text": text}

# print(f"Generate panels with style '{STYLE}' for this scenario: \n {SCENARIO}")
# os.environ['OPENAI_API_KEY'] = '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'
# SCENARIO = "haha"
# panels = generate_panels(SCENARIO)

# with open('output/panels.json', 'w') as outfile:
#   json.dump(panels, outfile)

# with open('output/panels.json') as json_file:
#   panels = json.load(json_file)

# panel_images = []

# for panel in panels:
#   panel_prompt = panel["description"] + ", cartoon box, " + STYLE
#   print(f"Generate panel {panel['number']} with prompt: {panel_prompt}")
#   panel_image = text_to_image(panel_prompt)
#   panel_image_with_text = add_text_to_panel(panel["text"], panel_image)
#   panel_image_with_text.save(f"output/panel-{panel['number']}.png")
#   panel_images.append(panel_image_with_text)

# create_strip(panel_images).save("output/strip.png")
