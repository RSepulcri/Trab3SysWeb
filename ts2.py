import gradio as gr
import numpy as np
import random
import heapq

# Configurações do grid
GRID_SIZE = 10
START_COLOR = [0, 255, 0]  # Verde
OBSTACLE_COLOR = [0, 0, 0]  # Preto
EMPTY_COLOR = [255, 255, 255]  # Branco
PATH_COLOR = [0, 0, 255]  # Azul

# Função para gerar o grid inicial
def generate_grid():
    grid = np.full((GRID_SIZE, GRID_SIZE, 3), EMPTY_COLOR, dtype=np.uint8)
    start_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    grid[start_pos[0], start_pos[1]] = START_COLOR

    # Adicionar obstáculos aleatórios
    for _ in range(random.randint(5, 15)):
        obs_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if not np.array_equal(grid[obs_pos[0], obs_pos[1]], START_COLOR):
            grid[obs_pos[0], obs_pos[1]] = OBSTACLE_COLOR

    return grid, start_pos

# Função heurística para o A*
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Algoritmo A*
def a_star(grid, start, goal):
    rows, cols = grid.shape[0], grid.shape[1]
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    obstacles = {tuple((i, j)) for i in range(rows) for j in range(cols) if np.array_equal(grid[i, j], OBSTACLE_COLOR)}

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

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
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
        grid[pos[0], pos[1]] = PATH_COLOR
    return grid

# Função principal para interatividade
def process_click(image, start_pos, x, y):
    grid = np.array(image, dtype=np.uint8)
    if np.array_equal(grid[x, y], OBSTACLE_COLOR) or np.array_equal(grid[x, y], START_COLOR):
        return grid.tolist()  # Ignorar cliques em obstáculos ou no pixel inicial

    goal_pos = (x, y)
    path = a_star(grid, start_pos, goal_pos)

    if path:
        grid = update_grid_with_path(grid, path)
        return grid.tolist()
    return grid.tolist()  # Sem caminho encontrado, retorna grid original

# Função para reiniciar
def reset():
    grid, start_pos = generate_grid()
    return grid.tolist(), start_pos

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

# Interface Gradio
with gr.Blocks() as demo:
    grid_image = gr.Image(type="numpy", label="Clique em um pixel!")
    btn_reset = gr.Button("Resetar")
    grid_image.change(interactive_grid, inputs=["image"], outputs=grid_image)
    btn_reset.click(reset_callback, outputs=grid_image)

demo.launch()
