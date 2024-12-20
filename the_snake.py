"""
Модуль игры "Змейка".

Содержит классы и функции для реализации игры, включая управление змейкой,
отображение яблока, обработку столкновений и основную игровую логику.
"""

from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)
# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Скорость движения змейки:
SPEED = 5

# Константы для индексов координат
X_IDX = 0
Y_IDX = 1

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)


class GameObject:
    """Базовый класс для объектов игры, таких как змейка и яблоко."""

    def __init__(self):
        """Центральная точка экрана это старт."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None  # переопределяется в эпл и снэйк

        # Настройка игрового окна:
        self.direction = None
        self.apple_position = None

    def draw(self):
        """
        Метод для отрисовки объектов.

        Метод переопределяется в дочерних.
        """
        raise NotImplementedError(
            'Метод draw() должен быть переопределён в дочернем классе'
        )


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self, occupied_positions=None):
        """
        Инициализирует объект класса Apple.

        Устанавливает цвет яблока, задаёт начальное положение
        с помощью метода randomize_position().
        """
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = None
        # Если occupied_positions не передан, создаем пустое множество
        if occupied_positions is None:
            occupied_positions = set()

        self.randomize_position(occupied_positions)  # начальная позиция

    def randomize_position(self, occupied_positions):
        """Генерируем случайную позицию для яблока."""
        while True:

            random_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            random_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (random_x, random_y)
            if new_position not in occupied_positions:
                self.position = new_position
                break

    def draw(self):
        """Отрисовываем яблоко на поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        """
        Инициализирует змейку с начальными параметрами.

        Длина = 1, начальная позиция = центр экрана, направление = вправо.
        """
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None  # Для затирания хвоста

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Движение змейки."""
        head_x, head_y = self.get_head_position()
        new_head_x = ((head_x + self.direction[X_IDX] * GRID_SIZE)
                      % SCREEN_WIDTH)
        new_head_y = ((head_y + self.direction[Y_IDX] * GRID_SIZE)
                      % SCREEN_HEIGHT)
        # Обновляем позицию головы
        new_pos = (new_head_x, new_head_y)
        # Добаляем новую позицию в список позиций
        self.positions.insert(0, new_pos)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self):
        """Обновление направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Сбрасывает состояние змейки к начальному значению."""
        self.length = 1
        # Сброс к начальной позиции, центр игрового поля
        self.positions = [self.position]
        # Рандомное направление движения
        directions = (UP, DOWN, LEFT, RIGHT)
        self.direction = choice(directions)
        self.last = None

    def draw(self):
        """Отрисовка змейки."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Используем get_head_position для отрисовки головы
        head_position = self.get_head_position()
        head_rect = pygame.Rect(head_position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Удаляем хвост
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обрабатывает нажатие клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit('Выход из игры')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция."""
    # Инициализация PyGame:
    pygame.init()

    # Создание объектов игры:
    snake = Snake()
    apple = Apple(occupied_positions=set(snake.positions))

    # Первичная генерация позиции яблока
    apple.randomize_position(set(snake.positions))

    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        # Обновление направления движения
        snake.update_direction()

        # Перемещение змейки
        snake.move()

        # Проверка столкновений
        if snake.get_head_position() == apple.position:
            # Увеличение длины змейки
            snake.length += 1
            # Генерация новой позиции яблока
            apple.randomize_position(set(snake.positions))

        # Проверка на столкновение с собой
        if snake.get_head_position() in snake.positions[1:]:
            # Сброс игры в случае столкновения
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(set(snake.positions))
        # Отрисовка объектов
        snake.draw()
        apple.draw()

        # Обновление экрана
        pygame.display.update()


if __name__ == '__main__':
    main()
