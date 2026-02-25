import pytest

from pet.pet import VirtualPet


def test_adjust_stat_clamps_between_0_and_100():
    cat = VirtualPet("Mochi", "cat", "affectionate", "AllCats")

    cat.adjust_stat("hunger", +1000)
    assert cat.hunger == 100

    cat.adjust_stat("hunger", -1000)
    assert cat.hunger == 0


@pytest.mark.parametrize(
    "hunger, energy, happiness, expected",
    [
        (90, 50, 50, "Hungry"),
        (50, 10, 50, "Tired"),
        (50, 50, 10, "Sad"),
        (10, 80, 80, "Happy"),
    ],
)
def test_mood_logic(hunger, energy, happiness, expected):
    cat = VirtualPet(
        "Mochi",
        "cat",
        "affectionate",
        "AllCats",
        hunger=hunger,
        happiness=happiness,
        energy=energy,
    )

    assert cat.mood() == expected
