import pygame
from settings import Settings

class Ship:
    """Класс для управления кораблём."""
    def __init__(self, ai_game):
        """Инициализирует корабль и задаёт его начальную позицию"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Загружает изображение корабля и получает прямоугольник
        self.image = pygame.image.load('images/ship.png')
        self.image = pygame.transform.smoothscale(self.image, (128, 128))
        self.rect = self.image.get_rect()
        # Каждый новый корабль появляется у нижнего края экрана.
        self.rect.midbottom = self.screen_rect.midbottom

        # Флаг перемещения
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Обновляет позицию корабля с учётом флага."""
        if self.moving_right and self.rect.x < 1065:
            self.rect.x += 1
        if self.moving_left and self.rect.x > 0:
            self.rect.x -= 1

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)
