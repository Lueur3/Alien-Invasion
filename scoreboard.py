import pygame.font

class Scoreboard:
    """Класс для вывода игровой информации."""

    def __init__(self, ai_game):
        """Инициализирует атрибуты подсчёта очков"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Настройки шрифта для вывода счёта.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # Подготовка исходного изображения
        self.prep_score()
        self.prep_rows()

    def prep_score(self):
        """Преобразует текущий счёт в графическое изображение."""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)

        # Вывод счёта в правой верхней части экрана.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20



    def prep_rows(self):
        curr_row_str = str(self.settings.curr_rows - 1)
        self.curr_row_image = self.font.render(curr_row_str, True,
                                               self.text_color, self.settings.bg_color)

        self.curr_row_rect = self.curr_row_image.get_rect()
        self.curr_row_rect.right = self.screen_rect.right - 20
        self.curr_row_rect.top = 60

    def show_score(self):
        """Выводит счёт на экран."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.curr_row_image, self.curr_row_rect)