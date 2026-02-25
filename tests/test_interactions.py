from pet.pet import VirtualPet
from pet.interactions import process_interaction


def make_cat(name: str, personality: str) -> VirtualPet:
    return VirtualPet(name, "cat", personality, "AllCats")


def test_affectionate_increases_happiness_and_relationship():
    a = make_cat("A", "affectionate")
    b = make_cat("B", "lazy")

    msg = process_interaction(a, b)

    assert "cuddled" in msg
    assert a.happiness > 50
    assert b.happiness > 50
    assert a.relationships["B"] > 0
    assert b.relationships["A"] > 0


def test_playful_vs_shy_decreases_happiness():
    playful = make_cat("Playful", "playful")
    shy = make_cat("Shy", "shy")

    msg = process_interaction(playful, shy)

    assert "shied away" in msg
    assert playful.happiness < 50
    assert shy.happiness < 50


def test_non_cat_species_returns_empty_message():
    cat = VirtualPet("Cat", "cat", "affectionate", "AllCats")
    dog = VirtualPet("Dog", "dog", "lazy", "AllDogs")

    msg = process_interaction(cat, dog)

    assert msg == ""
    # make sure we did not accidentally create relationship entries
    assert dog.name not in cat.relationships
