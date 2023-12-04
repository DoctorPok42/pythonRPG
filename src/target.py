from healthbar import Healthbar

class Target:
    def __init__(self, name: str, max_health: int, health: int) -> None:
        self._name = name
        self._max_health = max_health
        self._health = health
        self._healthbar = Healthbar(self._name, self._max_health, self._health)
        self._healthbar.create_healthbar()
        self._attack: str = ""

    def get_name(self):
        return self._name

    def get_max_health(self):
        return self._max_health

    def get_health(self):
        return self._health

    def change_name(self, name: str):
        self._name = name
        self._healthbar.update_name(name)

    def change_health(self, health: int):
        self._health = health
        if (self._health > self._max_health):
            self._health = self._max_health
        self._healthbar.update_health(health)

    def change_max_health(self, max_health: int):
        self._max_health = max_health
        self._healthbar.update_maxHealth(max_health)

    def show_healthbar(self):
        self._healthbar.update_health(self._health)
        self._healthbar.display_healthbar()
