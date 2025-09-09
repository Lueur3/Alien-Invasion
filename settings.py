
class Settings:
    """Класс для хранение всех настроек игры"""
    def __init__(self):
        """Инициализирует настройки игры"""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Настройки корабля
        self.ship_speed = 2

        # Параметры снаряда
        self.bullet_speed = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60 ,60)

        # Настройки пришельце
        self.alien_speed = 1.0