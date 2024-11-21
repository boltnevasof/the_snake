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
SPEED = 11

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)


class GameObject:
    """Базовый класс для объектов игры, таких как змейка и яблоко"""

    def __init__(self):
        # центральная точка экрана это старт
        self.position = ((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.body_color = None  # переопределяется в эпл и снэйк

        # Настройка игрового окна:

        self.direction = None
        self.apple_position = None
    # Метод рисования у объекта есть цвет и позиция

    def draw(self):
        """Метод для отрисовки объектов, который переопределяется в дочерних"""
        pass


class Apple(GameObject):
    """Класс для яблока"""

    def __init__(self):
        super().__init__()

        # определяем цвет яблока
        self.body_color = APPLE_COLOR
        # Генерация случайных координат яблока
        self.randomize_position()

    def randomize_position(self):
        """Генерируем случайную позицию для яблока"""
        random_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        random_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        position = (random_x, random_y)
        self.position = position
        self.apple_position = self.position

    def draw(self):
        """Отрисовываем яблоко на поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки"""

    # Начальное состояние змейки
    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        # Атрибут для хранения позиции последнего сегмента
        self.last = None

    def update_direction(self):
        """Обновление направление движения змейки"""
        # Обновление направления движения змейки
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple_position):
        """Обновляет позиции змейки, обрабатывает столкновения"""
        # получили голову
        head = self.get_head_position()

        new_head_x = (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_head_x, new_head_y)

        self.positions.insert(0, new_head)

        if new_head == apple_position:
            self.length += 1

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        # проверка на столкновение с самим собой
        if new_head in self.positions[1:]:
            self.reset()

    def reset(self):
        """Сбрасывает состояние змейки к начальному значению"""
        # Сброс к начальному значению
        self.length = 1
        # Сброс к начальной позиции, центр игрового поля
        self.positions = [self.position]
        # Рандомное направление движения
        directions = [UP, DOWN, LEFT, RIGHT]
        self.direction = choice(directions)

    # Возвращает текущую позицию змейки
    def get_head_position(self):
        """Возвращает текущую позицию головы змейки"""
        return self.positions[0]

    # Метод draw класса Snake
    def draw(self):
        """Отрисовывает змейку"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


# Обрабатывает нажатие клавиш
def handle_keys(game_object):
    """Обрабатывает нажатие клавиш для управления змейкой"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
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
    """Главная функция"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        # нажатие клавиш
        handle_keys(snake)
        # обновление направления и движения
        snake.update_direction()
        snake.move(apple.position)
        pygame.display.update()
        # Тут опишите основную логику игры.
        # если съела яблоко
        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            snake.length += 1
            pygame.display.update()

        # отрисовка яблока и змейки
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
