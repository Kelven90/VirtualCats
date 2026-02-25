class VirtualPet:
    def __init__(self, name, species, personality, sprite_name, hunger=50, happiness=50, energy=50, 
                 relationships=None, sleeping=False, state="idle"):
        self.name = name
        self.species = species
        self.personality = personality
        self.sprite_name = sprite_name
        self.hunger = hunger
        self.happiness = happiness
        self.energy = energy
        self.relationships = relationships if relationships else {}
        self.sleeping = sleeping
        self.state = state
        self._current_animation_key = None
        self._last_state = state


    def feed(self):
        self.adjust_stat("hunger", -10)

    def play(self):
        self.adjust_stat("happiness", +10)
        self.adjust_stat("energy", -5)

    def rest(self):
        self.adjust_stat("energy", +10)

    def mood(self):
        if self.hunger > 80:
            return "Hungry"
        elif self.energy < 20:
            return "Tired"
        elif self.happiness < 30:
            return "Sad"
        else:
            return "Happy"

    def adjust_stat(self, stat_name, delta):
        value = getattr(self, stat_name)
        new_value = max(0, min(100, value + delta))
        setattr(self, stat_name, new_value)

    def to_dict(self):
        return {
            "name": self.name,
            "species": self.species,
            "personality": self.personality,
            "sprite_name": self.sprite_name,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "relationships": self.relationships,
            "sleeping": self.sleeping,
            "state": self.state
        }
