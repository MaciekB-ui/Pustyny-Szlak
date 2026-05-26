import math


class Rover:
    def __init__(
        self, name: str, x: int, y: int, angle: int, fuel: int, armor_durability: int
    ):
        self.name = name
        self.armor_durability = armor_durability
        self.x = x
        self.y = y
        self.angle = angle
        self.fuel = fuel
        self.fuel_consumption = 4
        self.engine_level = 1
        self.max_dig_level = 1
        self.engine_parts = 0
        self.armor_parts = 0

    @property
    def has_fuel(self) -> bool:
        return self.fuel > 0

    @property
    def has_armor(self) -> bool:
        return self.armor_durability > 0

    def rotate(self, rotation: int) -> None:
        self.angle = (self.angle + rotation) % 360

    def move_forward(self, distance: int) -> tuple[int, int]:
        radians = math.radians(self.angle)

        self.x += round(distance * math.cos(radians))
        self.y += round(distance * math.sin(radians))
        self.fuel -= self.fuel_consumption

        return self.x, self.y

    def upgrade_engine(self) -> bool:
        was_upgraded = False
        required = self.engine_level
        self.engine_parts += 1

        if self.engine_parts >= required:
            self.engine_parts -= required
            self.fuel_consumption = max(1, 4 - (self.engine_level))
            self.engine_level += 1
            was_upgraded = True

        return was_upgraded
