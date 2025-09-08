import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создаёт игровые ресуры"""
        pygame.init()
        self.settings = Settings()

        self.icon = pygame.image.load('images/icon.png')
        pygame.display.set_icon(self.icon)

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.last_shot_time = 0
        self.bullet_allowed = 4

    @staticmethod
    def quit_game():
        pygame.quit()
        sys.exit()

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True

        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        elif event.key == pygame.K_q:
            AlienInvasion.quit_game()

    def _check_keyup_events(self, event):
        """Реагирует на опускание клавиш."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 200:
            if len(self.bullets) < self.bullet_allowed:
                new_bullet = Bullet(self)
                self.bullets.add(new_bullet)
                self.last_shot_time = current_time

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                AlienInvasion.quit_game()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)



    def _update_screen(self):
        """Обновляет изображение на экране и отображает на новый экран."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        pygame.display.flip()

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events() # проверка событий
            self.ship.update() #  Обновление движения корабля
            self.bullets.update() # Обновление движения пули

            # Удаление снарядов, вышедших за край
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

            self._update_screen() # обновление экрана



if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
