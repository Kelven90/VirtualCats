import random


def process_interaction(pet1, pet2):
    """Handles cat-cat interactions based on personality and relationship."""
    if pet1.species != "cat" or pet2.species != "cat":
        return ""

    personalities = {pet1.personality, pet2.personality}
    message = ""

    # Affectionate behavior
    if "affectionate" in personalities:
        pet1.adjust_stat("happiness", +5)
        pet2.adjust_stat("happiness", +5)
        message = (
            f"{pet1.name} cuddled up next to {pet2.name}. So warm and fuzzy. 🐱💞🐱"
        )

    # Playful + Playful
    elif pet1.personality == "playful" and pet2.personality == "playful":
        pet1.adjust_stat("energy", -5)
        pet2.adjust_stat("energy", -5)
        pet1.adjust_stat("happiness", +8)
        pet2.adjust_stat("happiness", +8)
        message = (
            f"{pet1.name} and {pet2.name} pounced and tumbled around playfully! 🐱🎾🐱"
        )

    # Playful + Shy
    elif "playful" in personalities and "shy" in personalities:
        playful = pet1 if pet1.personality == "playful" else pet2
        shy = pet2 if pet1 == playful else pet1
        playful.adjust_stat("happiness", -2)
        shy.adjust_stat("happiness", -2)
        message = f"{playful.name} tried to play, but {shy.name} shied away... 😿"

    # Lazy + Lazy or Shy + Shy or Lazy + Shy
    elif {"lazy", "shy"}.intersection(personalities) and random.random() < 0.8:
        pet1.adjust_stat("energy", +5)
        pet2.adjust_stat("energy", +5)
        message = f"{pet1.name} and {pet2.name} quietly enjoyed a lazy nap together. 💤"

    # Curious + Any
    elif "curious" in personalities:
        pet1.adjust_stat("happiness", +3)
        pet2.adjust_stat("happiness", +3)
        message = f"{pet1.name} and {pet2.name} observed each other curiously, tails twitching. 🐾👀"

    else:
        pet1.adjust_stat("hunger", +3)
        pet2.adjust_stat("hunger", +3)
        message = (
            f"{pet1.name} looked at {pet2.name}... then started licking their paw. 🐱✨"
        )

    # Relationship impact
    for a, b in [(pet1, pet2), (pet2, pet1)]:
        prev = a.relationships.get(b.name, 0)
        if "pounced" in message or "cuddled" in message:
            a.relationships[b.name] = min(100, prev + 10)
        elif "shied away" in message:
            a.relationships[b.name] = max(0, prev - 5)
        else:
            a.relationships[b.name] = min(100, prev + 2)

    return message
