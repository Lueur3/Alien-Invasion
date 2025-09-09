import pygame


from settings import Settings

class Ship:
    """Класс для управления кораблём."""
    def __init__(self, ai_game):
        """Инициализирует корабль и задаёт его начальную позицию"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Загружает изображение корабля и получает прямоугольник
        self.image = pygame.image.load('images/ship.png')
        self.image = pygame.transform.smoothscale(self.image, (128, 128))
        self.rect = self.image.get_rect()
        # Каждый новый корабль появляется у нижнего края экрана.
        self.rect.midbottom = self.screen_rect.midbottom

        # Сохранение вещественной координаты центра коробля
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Флаг перемещения
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Обновляет позицию корабля с учётом флагов."""
        # Обновляем атрибут x, не rect
        if self.moving_right:
            self.x += self.settings.ship_speed
        if self.moving_left :
            self.x -= self.settings.ship_speed

        if self.moving_up:
            self.y -= self.settings.ship_speed
        if self.moving_down:
            self.y += self.settings.ship_speed

        # Проверка выхода за границы
        self._check_bounds()

        # Обновление атрибута rect на основании self.x и self.y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)


    def _check_bounds(self):
        """Проверка на выход за границы"""
        if self.x < 0:
            self.x = 0
        if self.x > self.settings.screen_width - self.rect.width:
            self.x = self.settings.screen_width - self.rect.width

        if self.y > self.settings.screen_height - self.rect.height:
           self.y = self.settings.screen_height - self.rect.height

        if self.y < self.settings.screen_height / 2 :
            self.y = self.settings.screen_height / 2

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Размещает корабль в центре нижней стороны"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)