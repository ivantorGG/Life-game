import copy
import random
import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, (0, 255, 0), (
                        self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size, self.cell_size)
                                     )
                pygame.draw.rect(screen, (255, 255, 255), (
                    self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size, self.cell_size),
                                 1)

    def get_click(self, mouse_pos, screen):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell, screen)

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if x < len(self.board[0]) and y < len(self.board):
            return x, y
        return None

    def on_click(self, cell_coords, screen):
        if cell_coords is not None:
            cell = self.board[cell_coords[1]][cell_coords[0]]
            if cell == 0:  # если белая
                self.board[cell_coords[1]][cell_coords[0]] = 1
            elif cell == 1:
                self.board[cell_coords[1]][cell_coords[0]] = 0

            self.render(screen)


class Life(Board):
    def __init__(self, height, width):
        super().__init__(height, width)
        self.play = False

    def next_move(self):
        tmp_board = copy.deepcopy(self.board)
        for i in range(self.height):
            for j in range(self.width):
                alive_cells = 0
                if i != 0:
                    if self.board[i - 1][j]:
                        alive_cells += 1
                    if j != 0:
                        if self.board[i - 1][j - 1]:
                            alive_cells += 1
                    else:
                        if self.board[i - 1][self.width - 1]:
                            alive_cells += 1
                    if j != self.width - 1:
                        if self.board[i - 1][j + 1]:
                            alive_cells += 1
                    else:
                        if self.board[i - 1][0]:
                            alive_cells += 1
                else:
                    if self.board[self.height - 1][j]:
                        alive_cells += 1
                    if j != 0:
                        if self.board[self.height - 1][j - 1]:
                            alive_cells += 1
                    else:
                        if self.board[self.height - 1][self.width - 1]:
                            alive_cells += 1
                    if j != self.width - 1:
                        if self.board[self.height - 1][j + 1]:
                            alive_cells += 1
                    else:
                        if self.board[self.height - 1][0]:
                            alive_cells += 1
                if i != self.height - 1:
                    if self.board[i + 1][j]:
                        alive_cells += 1
                    if j != 0:
                        if self.board[i + 1][j - 1]:
                            alive_cells += 1
                    else:
                        if self.board[i + 1][self.width - 1]:
                            alive_cells += 1
                    if j != self.width - 1:
                        if self.board[i + 1][j + 1]:
                            alive_cells += 1
                    else:
                        if self.board[i + 1][0]:
                            alive_cells += 1
                else:
                    if self.board[0][j]:
                        alive_cells += 1
                    if j != 0:
                        if self.board[0][j - 1]:
                            alive_cells += 1
                    else:
                        if self.board[0][self.width - 1]:
                            alive_cells += 1
                    if j != self.width - 1:
                        if self.board[0][j + 1]:
                            alive_cells += 1
                    else:
                        if self.board[0][0]:
                            alive_cells += 1
                if j != 0:
                    if self.board[i][j - 1]:
                        alive_cells += 1
                else:
                    if self.board[i][self.width - 1]:
                        alive_cells += 1
                if j != self.width - 1:
                    if self.board[i][j + 1]:
                        alive_cells += 1
                else:
                    if self.board[i][0]:
                        alive_cells += 1

                if (alive_cells == 3 and not self.board[i][j]) or (alive_cells == 2 and
                                                                   self.board[i][j]) or (
                        alive_cells == 3 and self.board[i][j]):
                    tmp_board[i][j] = 1
                else:
                    tmp_board[i][j] = 0

        self.board = copy.deepcopy(tmp_board)


print('\n"r" - рандомно сгенерировать слетки')
print('"c" - очистить поле')
print('"ЛКМ" - оживить клетку')
print('"ПКМ/ПРОБЕЛ" - запустить/приостановить игру')
print('"Колёсико мыши вверх/вниз" - ускорить/замедлить игру')
print("""\nПравила:\n- мёртвая клетка становится живой, если рядом с ней находятся ровно три живые клетки;
- если живую клетку окружают две или три живые клетки, то эта клетка остаётся живой;
- в противном случае клетка становится мёртвой.\n""")
cell_size = int(input('Введи длину клетки - рекомендую то 10 до 20: '))
a = int(input('Введи длину стороны (в клетках) - рекомендую от 60 до 30: '))

pygame.init()
size = width, height = 700, 700
screen = pygame.display.set_mode(size)

speed = 300
GOLIFE = pygame.USEREVENT + 1
pygame.time.set_timer(GOLIFE, speed)

board = Life(a, a)
board.set_view(50, 50, cell_size)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not board.play:
                board.get_click(event.pos, screen)

            if event.button == 3:  # правая кнопка мыши
                board.play = False if board.play else True

            if event.button == 4:  # колёсико вверх
                pygame.time.set_timer(GOLIFE, speed := max(speed - 25, 20))

            if event.button == 5:  # колёсико вниз
                pygame.time.set_timer(GOLIFE, speed := min(speed + 25, 5000))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                board.play = False if board.play else True
            if event.key == pygame.K_c:
                board.board = [[0] * a for _ in range(a)]
            if event.key == pygame.K_r:
                board.board = [[random.choice([0, 1]) for _ in range(a)] for _ in range(a)]

        if event.type == GOLIFE:
            if board.play:
                board.next_move()

    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
