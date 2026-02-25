import json
from pet.pet import VirtualPet
import os

# Automatically resolve the data path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "pets.json")

def save_pets(pets):
    data = [pet.to_dict() for pet in pets]

    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

def load_pets():
    if not os.path.exists(DATA_PATH) or os.path.getsize(DATA_PATH) == 0:
        print("[WARN] pets.json missing or empty. Returning empty list.")
        return []

    try:
        with open(DATA_PATH, "r") as f:
            pet_dicts = json.load(f)
    except json.JSONDecodeError:
        print("[ERROR] pets.json is corrupted or invalid JSON. Returning empty list.")
        return []

    pets = []
    for pd in pet_dicts:
        pet = VirtualPet(
            pd["name"],
            pd["species"],
            pd["personality"],
            pd["sprite_name"],
            pd.get("hunger", 50),
            pd.get("happiness", 50),
            pd.get("energy", 50),
            pd.get("relationships", {}),
            pd.get("sleeping", False),
            pd.get("state", "idle")
        )
        pets.append(pet)
    return pets

