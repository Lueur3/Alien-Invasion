import sys
import pygame

from math import ceil
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats

class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создаёт игровые ресурcы."""
        pygame.init()
        self.settings = Settings()

        self.icon = pygame.image.load('images/icon.png')
        pygame.display.set_icon(self.icon)

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')

        # Создание экземпляра для хранения игровой статистики
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.last_shot_time = 0
        self.bullet_allowed = 4

        self._create_fleet()

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

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.width // 1.5 + 10, alien.rect.height
        alien.x = alien_width + 2 * alien_width * alien_number - 35
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 1.5 *  alien.rect.height * row_number - 400
        self.aliens.add(alien)

    def _create_fleet(self):
        """Создание флота вторжения."""
        # Создание пришельца и вычисление количества пришельцев в ряду.
        # Интервал между соседними пришельцами равен ширине пришельца.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.width // 1.5 + 10,  alien.rect.height
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = ceil(available_space_x / (2 * alien_width))

        """Определяет количество рядов, помещающихся на экране."""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (2 * alien_height) - ship_height)
        number_rows = ceil(available_space_y / (2 * alien_height))

        # Создание флота вторжения.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

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

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем"""
        # Уменьшение ships_left
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()

            # Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_bullet_alien_collisions(self):
        # Проверка попадания в пришельце.
        # При обнаружении попадания удалить снаряд и пришельца.
        collisions = pygame.sprite.groupcollide(self.bullets,
                                                self.aliens, True, True)

        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота.
            self.bullets.empty()
            self._create_fleet()


    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды"""
        # Обновление позиций снарядов.
        self.bullets.update()

        # Удаление снарядов, вышедших за край
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _update_aliens(self):
        """Проверяет, достиг ли флот края экрана,
        с последующим обновлением позиций всех пришельцев во флоте."""
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коллизии пришелец - корабль
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _update_screen(self):
        """Обновляет изображение на экране и отображает на новый экран."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events() # проверка событий
            if self.stats.game_active:
                self.ship.update() #  Обновление движения корабля
                self._update_bullets() # Обновление движения пуль
                self._update_aliens()

            else:
                print('Game over')
                AlienInvasion.quit_game()

            self._update_screen() # обновление экрана



if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
