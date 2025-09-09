import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Класс представляющий одного пришельца."""

    def __init__(self, ai_game):
        """Инициализирует пришельца и задаёт его начальую позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Загрузка изоббражения пришельца и назначение атрибута rect.
        self.image = pygame.image.load('images/alien.png')
        self.image = pygame.transform.smoothscale(self.image, (128, 128))
        self.rect = self.image.get_rect()

        # Каждый новый пришелец появляется в левом верхнем углу экрана.
        self.rect.x = self.rect.width - 70
        self.rect.y = self.rect.height - 120

        # Сохранение точной горизонтальной позиции пришельца.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True


    def update(self):
        """Перемещение пришельца вправо или влево."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x