from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

# Load geologist brain - sees crystals, layers, texture
print("Loading geologist brain...")
model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)
print("Brain loaded!")

# How a real geologist describes rocks
ROCK_PROMPTS = {
    "GRANITE": "a close up photo of granite rock with speckled black and white crystals, coarse grained, hard igneous rock",
    "BASALT": "dark black basalt volcanic rock, very fine grained, heavy, smooth",
    "DOLERITE": "dolerite dark igneous rock with medium speckled crystals",
    "SANDSTONE": "sandstone layered sedimentary rock, sandy grains, brown layered",
    "LIMESTONE": "light limestone sedimentary rock, smooth, white gray",
    "LATERITE": "red laterite iron rock, reddish brown, porous, Ghana laterite",
    "BAUXITE": "bauxite reddish brown aluminum ore rock",
    "SHALE": "shale dark layered flat sedimentary rock, thin layers",
    "GNEISS": "gneiss metamorphic banded rock with black white bands",
    "QUARTZITE": "quartzite light hard quartz rock, glassy sparkle",
    "MARBLE": "marble white smooth metamorphic rock",
    "GOLD QUARTZ": "quartz rock with gold yellow metallic vein, shiny gold metallic",
    "HEMATITE": "hematite dark red metallic iron ore rock",
    "SCHIST": "schist shiny flaky metamorphic rock with mica sparkle"
}

def classify(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
        
        texts = list(ROCK_PROMPTS.values())
        names = list(ROCK_PROMPTS.keys())
        
        inputs = processor(text=texts, images=img, return_tensors="pt", padding=True)
        
        with torch.no_grad():
            outputs = model(**inputs)
            probs = outputs.logits_per_image.softmax(dim=1)
        
        values, indices = torch.topk(probs[0], 3)
        
        top_name = names[indices[0]]
        top_prob = values[0].item() * 100
        
        second = f"{names[indices[1]]} ({values[1].item()*100:.0f}%)"
        third = f"{names[indices[2]]} ({values[2].item()*100:.0f}%)"
        
        crystal_note = ""
        if "GRANITE" in top_name:
            crystal_note = "\n🔬 Crystals: Visible black/white crystals, coarse = Slow cooling igneous"
        elif "BASALT" in top_name:
            crystal_note = "\n🔬 Crystals: Too small to see = Fast cooling lava"
        elif "SANDSTONE" in top_name or "SHALE" in top_name:
            crystal_note = "\n🔬 Layers: Sedimentary bedding = Deposited by water/wind"
        elif "GNEISS" in top_name or "SCHIST" in top_name:
            crystal_note = "\n🔬 Bands: Metamorphic banded = High pressure deep underground"
        elif "GOLD" in top_name:
            crystal_note = "\n💰 Gold Alert: Yellow metallic luster! Do hardness test!"
        
        return f"""✅ GEOLOGIST AI BRAIN:

Primary: {top_name} - {top_prob:.0f}% confidence
Other guesses: {second}, {third}
{crystal_note}

🧠 This brain sees CRYSTALS + LAYERS + TEXTURE + COLOR like real geologist
📚 Trained on millions of images
"""
    except Exception as e:
        return f"Error: {e}\nMake sure you installed transformers"