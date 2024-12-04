import gradio as gr
import numpy as np
import heapq
import random

# Configurações do grid
GRID_SIZE = 10
START_COLOR = "green"
OBSTACLE_COLOR = "black"
EMPTY_COLOR = "white"

# Função para gerar o grid inicial
def generate_grid():
    grid = [[EMPTY_COLOR for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    start_pos = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    grid[start_pos[0]][start_pos[1]] = START_COLOR
    
    # Adicionando obstáculos aleatórios
    for _ in range(random.randint(5, 15)):  # Ajuste o número de obstáculos
        obs_pos = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        if grid[obs_pos[0]][obs_pos[1]] == EMPTY_COLOR:  # Não sobrepor ao pixel inicial
            grid[obs_pos[0]][obs_pos[1]] = OBSTACLE_COLOR
            
    return grid, start_pos

# Função heurística para o A*
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Algoritmo A*
def a_star(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    obstacles = {tuple((i, j)) for i in range(rows) for j in range(cols) if grid[i][j] == OBSTACLE_COLOR}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruir o caminho
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Vizinhos 4-direcionais
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and neighbor not in obstacles:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # Sem caminho disponível

# Atualizar grid com o caminho
def update_grid_with_path(grid, path):
    for pos in path:
        grid[pos[0]][pos[1]] = "blue"
    return grid

# Função principal para interatividade
def process_click(grid, start_pos, x, y):
    if grid[x][y] == OBSTACLE_COLOR or grid[x][y] == START_COLOR:
        return grid  # Ignore cliques em obstáculos ou no pixel inicial

    goal_pos = (x, y)
    path = a_star(grid, start_pos, goal_pos)

    if path:
        updated_grid = [row[:] for row in grid]
        updated_grid = update_grid_with_path(updated_grid, path)
        return updated_grid
    return grid  # Sem caminho encontrado, retorna grid original

# Função para reiniciar
def reset():
    grid, start_pos = generate_grid()
    return grid, start_pos

# Variáveis globais para o estado do grid
grid, start_pos = generate_grid()

# Interface Gradio
def interactive_grid(x=-1, y=-1):
    global grid, start_pos
    if x != -1 and y != -1:
        grid = process_click(grid, start_pos, x, y)
    return grid

# Função de reinicialização
def reset_callback():
    global grid, start_pos
    grid, start_pos = reset()
    return grid

with gr.Blocks() as demo:
    output = gr.Grid(update=lambda: interactive_grid())
    btn_reset = gr.Button("Reset")
    btn_reset.click(reset_callback, outputs=output)
    gr.Interface(fn=interactive_grid, 
                   inputs=["click"],
                 ).launch()
