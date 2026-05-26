from collections import defaultdict
from constants import WORLDS_SCALE_FACTOR
import random


class World:
    width: int = 0
    height: int = 0
    fuel_chance: float = 0.0
    engine_part_chance: float = 0.0
    armor_part_chance: float = 0.0
    storm_interval: int = 0
    storm_chance: float = 0.0
    oasis_chance: float = 0.0
    map_fragment_chance: float = 0.0

    def __init__(self):
        self.artifact_x = random.randint(
            -self.width // WORLDS_SCALE_FACTOR, self.width // WORLDS_SCALE_FACTOR
        )
        self.artifact_y = random.randint(
            -self.height // WORLDS_SCALE_FACTOR, self.height // WORLDS_SCALE_FACTOR
        )
        self.dug_positions = defaultdict(int)

    def is_out_of_bounds(self, x: int, y: int) -> bool:
        half_x = self.width // WORLDS_SCALE_FACTOR
        half_y = self.height // WORLDS_SCALE_FACTOR

        return x < -half_x or x > half_x or y < -half_y or y > half_y


class EasyWorld(World):
    width = 200
    height = 200
    fuel_chance = 0.20
    engine_part_chance = 0.20
    armor_part_chance = 0.10
    storm_interval = 20
    storm_chance = 0.25
    oasis_chance = 0.05
    map_fragment_chance = 0.10


class MediumWorld(World):
    width = 300
    height = 300
    fuel_chance = 0.15
    engine_part_chance = 0.10
    armor_part_chance = 0.10
    storm_interval = 15
    storm_chance = 0.25
    map_fragment_chance = 0.08
    oasis_chance = 0.05


class HardWorld(World):
    width = 400
    height = 400
    fuel_chance = 0.10
    engine_part_chance = 0.10
    armor_part_chance = 0.10
    storm_interval = 10
    storm_chance = 0.25
    map_fragment_chance = 0.05
    oasis_chance = 0.05


class ExtremeWorld(World):
    width = 500
    height = 500
    fuel_chance = 0.05
    engine_part_chance = 0.10
    armor_part_chance = 0.10
    storm_interval = 5
    storm_chance = 0.25
    map_fragment_chance = 0.02
    oasis_chance = 0.05


def create_world(difficulty: str) -> World:
    match difficulty:
        case "easy":
            return EasyWorld()
        case "medium":
            return MediumWorld()
        case "hard":
            return HardWorld()
        case "extreme":
            return ExtremeWorld()
        case _:
            raise ValueError("Nieznany poziom trudności")
