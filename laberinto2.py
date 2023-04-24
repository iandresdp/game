import pygame
import random
from queue import PriorityQueue
import numpy as np

# Inicializar Pygame
pygame.init()

# Definir las dimensiones de la ventana
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640

# Crear la ventana
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Laberinto")

# Definir colores
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED =  (255,255, 0)
GREEN = (0, 255, 0)

# Definir tamaño de celda y margen
CELL_SIZE = 20
CELL_MARGIN = 2

# Calcular número de filas y columnas de celdas
NUM_ROWS = (SCREEN_HEIGHT - CELL_MARGIN) // (CELL_SIZE + CELL_MARGIN)
NUM_COLS = (SCREEN_WIDTH - CELL_MARGIN) // (CELL_SIZE + CELL_MARGIN)

# Crear el laberinto
maze = []
for row in range(NUM_ROWS):
    maze.append([])
    for col in range(NUM_COLS):
        maze[row].append(1)

# Definir la posición de entrada y salida
entry_row = random.randint(0, NUM_ROWS - 1)
entry_col = 0
exit_row = random.randint(0, NUM_ROWS - 1)
exit_col = NUM_COLS - 1

# Asegurarse de que la entrada y la salida no estén en la misma fila
while entry_row == exit_row:
    exit_row = random.randint(0, NUM_ROWS - 1)

# Asegurarse de que la entrada y la salida no estén en la misma columna
while entry_col == exit_col:
    exit_col = random.randint(0, NUM_COLS - 1)

# Abrir la entrada y la salida del laberinto
maze[entry_row][entry_col] = 0
maze[exit_row][exit_col] = 0

# Crear el laberinto
for row in range(1, NUM_ROWS - 1):
    for col in range(1, NUM_COLS - 1):
        if random.randint(0, 100) < 40:
            maze[row][col] = 0
        else:
            if (maze[row][col-1] == 0 or maze[row][col+1] == 0 or
                maze[row-1][col] == 0 or maze[row+1][col] == 0):
                maze[row][col] = 0

# Definir posición inicial del jugador
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2

# Definir tamaño del jugador
player_size = CELL_SIZE

# Definir velocidad del jugador
player_speed = CELL_SIZE + CELL_MARGIN

# Definir coordenadas iniciales del enemigo
x1 = 100
y1 = 50
x2 = 200
y2 = 100

# Definir enemigo
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = CELL_SIZE
        self.speed = CELL_SIZE + CELL_MARGIN

    def move(self):
        row = self.y // (CELL_SIZE + CELL_MARGIN)
        col = self.x // (CELL_SIZE + CELL_MARGIN)
        directions = []
        if row > 0 and maze[row-1][col] == 0:
            directions.append((-1, 0))
        if row < NUM_ROWS-1 and maze[row+1][col] == 0:
            directions.append((1, 0))
        if col > 0 and maze[row][col-1] == 0:
            directions.append((0, -1))
        if col < NUM_COLS-1 and maze[row][col+1] == 0:
            directions.append((0, 1))
        if directions:
            d_row, d_col = random.choice(directions)
            self.y += d_row * (CELL_SIZE + CELL_MARGIN)
            self.x += d_col * (CELL_SIZE + CELL_MARGIN)

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.size, self.size))

# Inicializar lista de enemigos
enemies = []

# Agregar enemigos a la lista
enemy1 = Enemy(x1, y1)
enemies.append(enemy1)
enemy2 = Enemy(x2, y2)
enemies.append(enemy2)

# Bucle principal
running = True
while running:
    # Manejar eventos de Pygame
    for event in pygame.event.get():
        pygame.time.delay(0)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player_x > 0:
                player_x -= player_speed
            elif event.key == pygame.K_RIGHT and player_x < SCREEN_WIDTH - player_size:
                player_x += player_speed
            elif event.key == pygame.K_UP and player_y > 0:
                player_y -= player_speed
            elif event.key == pygame.K_DOWN and player_y < SCREEN_HEIGHT - player_size:
                player_y += player_speed      

    # Dibujar el laberinto
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if maze[row][col] == 1:
                color = GREY
            elif row == entry_row and col == entry_col:
                color = GREEN # color de la entrada
            elif row == exit_row and col == exit_col:
                color = RED # color de la salida
            else:
                color = WHITE
            pygame.draw.rect(screen, color, [(CELL_MARGIN + CELL_SIZE) * col + CELL_MARGIN,
                                             (CELL_MARGIN + CELL_SIZE) * row + CELL_MARGIN,
                                             CELL_SIZE, CELL_SIZE])
    # Dibujar el jugador
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_size, player_size))

    # Mover y dibujar los enemigos
    for enemy in enemies:
            pygame.time.delay(125)
            enemy.draw()
            enemy.move()

    # Actualizar la ventana
    pygame.display.update()

    # Verificar si el jugador llegó a la salida
    if player_x // (CELL_SIZE + CELL_MARGIN) == exit_col and player_y // (CELL_SIZE + CELL_MARGIN) == exit_row:
        running = False
        print("¡Ganaste!")

# Salir de Pygame
pygame.quit()
