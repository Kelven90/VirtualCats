from pathlib import Path

from pet.pet import VirtualPet
import pet.persistence as persistence


def test_save_and_load_pets_round_trip(tmp_path: Path, monkeypatch):
    # Redirect DATA_PATH to a temporary file so we don't touch real data/pets.json
    temp_file = tmp_path / "pets.json"
    monkeypatch.setattr(persistence, "DATA_PATH", str(temp_file))

    original = [
        VirtualPet(
            "Mochi",
            "cat",
            "affectionate",
            "AllCats",
            hunger=40,
            happiness=80,
            energy=70,
        ),
        VirtualPet(
            "Kumo",
            "cat",
            "lazy",
            "AllCatsGrey",
            hunger=60,
            happiness=50,
            energy=40,
        ),
    ]

    persistence.save_pets(original)
    loaded = persistence.load_pets()

    assert len(loaded) == len(original)
    for original_cat, loaded_cat in zip(original, loaded):
        assert loaded_cat.name == original_cat.name
        assert loaded_cat.species == original_cat.species
        assert loaded_cat.personality == original_cat.personality
        assert loaded_cat.sprite_name == original_cat.sprite_name
        assert loaded_cat.hunger == original_cat.hunger
        assert loaded_cat.happiness == original_cat.happiness
        assert loaded_cat.energy == original_cat.energy
