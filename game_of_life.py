import pygame
import numpy as np
import os

# Initialize Pygame
pygame.init()

# Screen size
width, height = 800, 800
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Conway's Game of Life")

# Initial cell size
initial_cell_size = 10
cell_size = initial_cell_size
cols, rows = width // cell_size, height // cell_size

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BG_COLOR = (30, 30, 30)
SHADOW_COLOR = (50, 50, 50)

# Load Sounds
def load_sound(file):
    if os.path.exists(file):
        return pygame.mixer.Sound(file)
    else:
        print(f"Warning: Sound file {file} not found.")
        return None

click_sound = load_sound('sounds/click.wav')
toggle_sound = load_sound('sounds/toggle.wav')

# Create a grid
grid = np.zeros((rows, cols))

# Initialize a random grid
def random_grid():
    return np.random.choice([0, 1], size=(rows, cols))

# Update the grid
def update_grid(grid):
    new_grid = np.copy(grid)
    for row in range(rows):
        for col in range(cols):
            # Count alive neighbors
            alive_neighbors = np.sum(grid[max(0, row-1):min(rows, row+2), max(0, col-1):min(cols, col+2)]) - grid[row, col]
            # Apply the rules of the game
            if grid[row, col] == 1 and (alive_neighbors < 2 or alive_neighbors > 3):
                new_grid[row, col] = 0
            elif grid[row, col] == 0 and alive_neighbors == 3:
                new_grid[row, col] = 1
    return new_grid

# Draw the grid
def draw_grid(grid, cell_size, pan_x, pan_y):
    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == 1:
                color = (255 - (row * 5) % 256, 255 - (col * 5) % 256, (row * col) % 256)
            else:
                color = BG_COLOR
            pygame.draw.rect(screen, color, (col * cell_size + pan_x, row * cell_size + pan_y, cell_size, cell_size))
            pygame.draw.rect(screen, SHADOW_COLOR, (col * cell_size + pan_x, row * cell_size + pan_y, cell_size, cell_size), 1)

# Draw UI elements
def draw_ui(paused, speed, generations, population):
    font = pygame.font.SysFont('Arial', 24, bold=True)
    pause_text = font.render('Paused' if paused else 'Running', True, WHITE)
    speed_text = font.render(f'Speed: {speed}', True, WHITE)
    gen_text = font.render(f'Generations: {generations}', True, WHITE)
    pop_text = font.render(f'Population: {population}', True, WHITE)
    
    # Draw shadows
    shadow_offset = 2
    screen.blit(pause_text, (12 + shadow_offset, 12 + shadow_offset), special_flags=pygame.BLEND_RGB_SUB)
    screen.blit(speed_text, (12 + shadow_offset, 42 + shadow_offset), special_flags=pygame.BLEND_RGB_SUB)
    screen.blit(gen_text, (12 + shadow_offset, 72 + shadow_offset), special_flags=pygame.BLEND_RGB_SUB)
    screen.blit(pop_text, (12 + shadow_offset, 102 + shadow_offset), special_flags=pygame.BLEND_RGB_SUB)

    # Draw background for text
    pygame.draw.rect(screen, BLACK, (10, 10, 220, 140))
    
    screen.blit(pause_text, (10, 10))
    screen.blit(speed_text, (10, 40))
    screen.blit(gen_text, (10, 70))
    screen.blit(pop_text, (10, 100))

# Draw control panel with circular edges
def draw_control_panel(height):
    font = pygame.font.SysFont('Arial', 20, bold=True)
    button_texts = ['Start', 'Pause', 'Reset', 'Save', 'Load']
    button_colors = [GREEN, RED, BLUE, YELLOW, WHITE]
    button_rects = []
    for i, text in enumerate(button_texts):
        color = button_colors[i]
        rect = pygame.Rect(10 + i*90, height - 50, 80, 40)
        pygame.draw.rect(screen, color, rect, border_radius=20)
        button_text = font.render(text, True, BLACK)
        screen.blit(button_text, (rect.x + 10, rect.y + 10))
        button_rects.append(rect)
    return button_rects

def handle_button_click(pos, button_rects, paused, generations):
    global grid
    if button_rects[0].collidepoint(pos):
        paused = False
        if toggle_sound:
            toggle_sound.play()
    elif button_rects[1].collidepoint(pos):
        paused = True
        if toggle_sound:
            toggle_sound.play()
    elif button_rects[2].collidepoint(pos):
        grid = random_grid()
        generations = 0
        if click_sound:
            click_sound.play()
    elif button_rects[3].collidepoint(pos):
        np.save("saved_grid.npy", grid)
        if click_sound:
            click_sound.play()
    elif button_rects[4].collidepoint(pos):
        grid = np.load("saved_grid.npy")
        if click_sound:
            click_sound.play()
    return paused, generations

def resize_grid(grid, new_rows, new_cols):
    new_grid = np.zeros((new_rows, new_cols))
    min_rows = min(grid.shape[0], new_rows)
    min_cols = min(grid.shape[1], new_cols)
    new_grid[:min_rows, :min_cols] = grid[:min_rows, :min_cols]
    return new_grid

# Main loop
def main():
    global screen, cols, rows, grid, cell_size, width, height
    clock = pygame.time.Clock()
    grid = random_grid()
    paused = False
    speed = 10
    zoom_factor = 1.0
    generations = 0
    running = True
    pan_x, pan_y = 0, 0

    while running:
        population = np.sum(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    if toggle_sound:
                        toggle_sound.play()
                elif event.key == pygame.K_r:
                    grid = random_grid()
                    generations = 0
                    if click_sound:
                        click_sound.play()
                elif event.key == pygame.K_s:
                    np.save("saved_grid.npy", grid)
                    if click_sound:
                        click_sound.play()
                elif event.key == pygame.K_l:
                    grid = np.load("saved_grid.npy")
                    if click_sound:
                        click_sound.play()
                elif event.key == pygame.K_UP:
                    speed = min(speed + 1, 60)
                elif event.key == pygame.K_DOWN:
                    speed = max(speed - 1, 1)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    zoom_factor = min(zoom_factor + 0.1, 5.0)
                    cell_size = int(initial_cell_size * zoom_factor)
                    new_cols, new_rows = width // cell_size, height // cell_size
                    grid = resize_grid(grid, new_rows, new_cols)
                    cols, rows = new_cols, new_rows
                elif event.key == pygame.K_MINUS:
                    zoom_factor = max(zoom_factor - 0.1, 1.0)
                    cell_size = int(initial_cell_size * zoom_factor)
                    new_cols, new_rows = width // cell_size, height // cell_size
                    grid = resize_grid(grid, new_rows, new_cols)
                    cols, rows = new_cols, new_rows
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y >= height - 50:
                    paused, generations = handle_button_click((x, y), button_rects, paused, generations)
                else:
                    col, row = (x - pan_x) // cell_size, (y - pan_y) // cell_size
                    if event.button == 1:  # Left click
                        grid[row, col] = 1
                    elif event.button == 3:  # Right click
                        grid[row, col] = 0
                    if click_sound:
                        click_sound.play()
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.size
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                new_cols, new_rows = width // cell_size, height // cell_size
                grid = resize_grid(grid, new_rows, new_cols)
                cols, rows = new_cols, new_rows
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[1]:  # Middle mouse button for panning
                    pan_x += event.rel[0]
                    pan_y += event.rel[1]

        if not paused:
            grid = update_grid(grid)
            generations += 1

        screen.fill(BG_COLOR)
        draw_grid(grid, cell_size, pan_x, pan_y)
        draw_ui(paused, speed, generations, population)
        button_rects = draw_control_panel(height)
        pygame.display.flip()

        clock.tick(speed)

    pygame.quit()

if __name__ == "__main__":
    main()
