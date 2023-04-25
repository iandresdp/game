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
RED =  (255,0, 0)
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

# Calcular las coordenadas x e y en la pantalla que corresponden a la celda del laberinto donde se encuentra la puerta de entrada
entry_x = entry_col * CELL_SIZE + CELL_SIZE // 2
entry_y = entry_row * CELL_SIZE + CELL_SIZE // 2

# Definir posición inicial del jugador
player_x = entry_x
player_y = entry_y

# Definir tamaño del jugador
player_size = CELL_SIZE

# Definir velocidad del jugador
player_speed = CELL_SIZE + CELL_MARGIN

# Generar coordenadas iniciales aleatorias para el enemigo 1
x1 = random.randint(20, 620)
y1 = random.randint(20, 620)

# Generar coordenadas iniciales aleatorias para el enemigo 2
x2 = random.randint(20, 620)
y2 = random.randint(20, 620)

print(f'Coordenadas iniciales del enemigo 1: ({x1}, {y1})')
print(f'Coordenadas iniciales del enemigo 2: ({x2}, {y2})')

# Definir enemigo
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = CELL_SIZE
        self.speed = CELL_SIZE + CELL_MARGIN
        self.lives = 3

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

# Definir número inicial de vidas
player_lives = 3

# Definir fuente para el texto
font = pygame.font.Font(None, 36)

# Definir tamaño del jugador
player_size_x = CELL_SIZE
player_size_y = CELL_SIZE

# Definir estado del jugador (0 = normal, 1 = defensa)
player_state = 0

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
                player_direction = 'left'
            elif event.key == pygame.K_RIGHT and player_x < SCREEN_WIDTH - player_size_x:
                player_x += player_speed
                player_direction = 'right'
            elif event.key == pygame.K_UP and player_y > 0:
                player_y -= player_speed
                player_direction = 'up'
            elif event.key == pygame.K_DOWN and player_y < SCREEN_HEIGHT - player_size_y:
                player_y += player_speed
                player_direction = 'down'
            elif event.key == pygame.K_SPACE:
                if player_state == 0:
                    # Cambiar a estado de defensa
                    player_state = 1
                    # Aumentar el tamaño del jugador en la dirección que está mirando
                    if player_direction == 'left':
                        player_size_x *= 2
                        player_x -= CELL_SIZE
                    elif player_direction == 'right':
                        player_size_x *= 2
                    elif player_direction == 'up':
                        player_size_y *= 2
                        player_y -= CELL_SIZE
                    elif player_direction == 'down':
                        player_size_y *= 2
                else:
                    # Cambiar a estado normal
                    player_state = 0
                    # Restablecer el tamaño del jugador
                    if player_direction in ['left', 'right']:
                        player_size_x = CELL_SIZE
                        if player_direction == 'left':
                            player_x += CELL_SIZE
                    else:
                        player_size_y = CELL_SIZE
                        if player_direction == 'up':
                            player_y += CELL_SIZE
    # Cargar una imagen como textura
    texture = pygame.image.load('texture.jpg')
    
    # Dibujar el laberinto
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if maze[row][col] == 1:
                # Crear un rectángulo con la textura
                rect = pygame.Rect((CELL_MARGIN + CELL_SIZE) * col + CELL_MARGIN,
                                   (CELL_MARGIN + CELL_SIZE) * row + CELL_MARGIN,
                                   CELL_SIZE,
                                   CELL_SIZE)
                screen.blit(texture, rect)
            elif row == entry_row and col == entry_col:
                color = GREEN # color de la entrada
                pygame.draw.rect(screen, color,
                                 [(CELL_MARGIN + CELL_SIZE) * col + CELL_MARGIN,
                                  (CELL_MARGIN + CELL_SIZE) * row + CELL_MARGIN,
                                  CELL_SIZE,
                                  CELL_SIZE])
            elif row == exit_row and col == exit_col:
                color = YELLOW # color de la salida
                pygame.draw.rect(screen, color,
                                 [(CELL_MARGIN + CELL_SIZE) * col + CELL_MARGIN,
                                  (CELL_MARGIN + CELL_SIZE) * row + CELL_MARGIN,
                                  CELL_SIZE,
                                  CELL_SIZE])
            else:
                color = WHITE
                pygame.draw.rect(screen, color,
                                 [(CELL_MARGIN + CELL_SIZE) * col + CELL_MARGIN,
                                  (CELL_MARGIN + CELL_SIZE) * row + CELL_MARGIN,
                                  CELL_SIZE,
                                  CELL_SIZE])
    # Dibujar el jugador
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_size, player_size))

    # Mover y dibujar los enemigos
    for enemy in enemies:
            pygame.time.delay(125)
            enemy.draw()
            enemy.move()

    # Actualizar la ventana
    pygame.display.update()

    # Verificar si algún enemigo ha tocado al jugador
    for enemy in enemies:
        if (player_x < enemy.x + enemy.size and
            player_x + player_size > enemy.x and
            player_y < enemy.y + enemy.size and
            player_y + player_size > enemy.y):
            # Restar una vida al jugador
            player_lives -= 1
            print(f'¡Perdiste una vida! Vidas restantes: {player_lives}')
            # Verificar si el jugador aún tiene vidas restantes
            if player_lives == 0:
                running = False
                # Crear superficie con el texto de derrota
                text = font.render("¡Perdiste!", True, (255, 0, 0))
                # Calcular posición del texto en la pantalla
                text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
                text_y = SCREEN_HEIGHT // 2 - text.get_height() // 2
                # Dibujar un rectángulo detrás del texto
                pygame.draw.rect(screen, (0, 0, 0), (text_x - 10, text_y - 10,
                                                     text.get_width() + 20,
                                                     text.get_height() + 20))
                # Dibujar el texto en la pantalla
                screen.blit(text, (text_x, text_y))
                # Actualizar la ventana
                pygame.display.update()
                # Esperar antes de salir del juego
                pygame.time.wait(3000)
                print("¡Perdiste!")
                
    # Verificar si algún enemigo ha tocado al jugador mientras está en estado de defensa
    if player_state == 1:
        for enemy in enemies[:]:
            if (player_x < enemy.x + enemy.size and
                player_x + player_size_x > enemy.x and
                player_y < enemy.y + enemy.size and
                player_y + player_size_y > enemy.y):
                # Restar una vida al enemigo
                enemy.lives -= 1
                print(f'¡Le quitaste una vida al enemigo! Vidas restantes: {enemy.lives}')
                # Verificar si el enemigo aún tiene vidas restantes
                if enemy.lives == 0:
                    enemies.remove(enemy)
                    print('¡Eliminaste a un enemigo!')
    # Verificar si el jugador llegó a la salida
    if player_x // (CELL_SIZE + CELL_MARGIN) == exit_col and player_y // (CELL_SIZE + CELL_MARGIN) == exit_row:
        running = False
        # Crear superficie con el texto de victoria
        text = font.render("¡Ganaste!", True, (0, 255, 0))
        # Calcular posición del texto en la pantalla
        text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
        text_y = SCREEN_HEIGHT // 2 - text.get_height() // 2
        # Dibujar un rectángulo detrás del texto
        pygame.draw.rect(screen, (0, 0, 0), (text_x - 10, text_y - 10,
                                             text.get_width() + 20,
                                             text.get_height() + 20))
        # Dibujar el texto en la pantalla
        screen.blit(text, (text_x, text_y))
        # Actualizar la ventana
        pygame.display.update()
        # Esperar antes de salir del juego
        pygame.time.wait(3000)
        print("¡Ganaste!")

    # Crear superficie con el texto de las vidas del jugador
    text = font.render(f'Vidas: {player_lives}', True, (255, 255, 255))
    # Dibujar un rectángulo detrás del texto
    pygame.draw.rect(screen, (0, 0, 0), (10 - 5, 10 - 5,
                                         text.get_width() + 10,
                                         text.get_height() + 10))
    # Dibujar el texto en la pantalla
    screen.blit(text, (10, 10))
    pygame.display.update()
# Salir de Pygame
pygame.quit()
