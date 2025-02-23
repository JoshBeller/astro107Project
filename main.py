import pygame
import levels.level1  # Import the first level
import levels.level2  # Import the second level
import levels.level3  # Import the third level
import levels.level4  # Import the fourth level
import levels.level5  # Import the fifth level
import levels.level6  # Import the secret final level
import levels.ending  # Import the ending sequence

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Black Hole Explorer")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Font
font = pygame.font.Font(None, 40)
title_font = pygame.font.Font(None, 50)

# Level completion tracking
levels_completed = [False, False, False, False, False]
secret_level_unlocked = False
final_sequence_triggered = False

# Level selection options
menu_options = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Exit"]
selected_index = 0

# Puzzle display settings
piece_size = 50
spacing = 20
puzzle_width = (piece_size * 5) + (spacing * 4)
start_x = (WIDTH - puzzle_width) // 2  # Centered horizontally
start_y = 100  # Positioned near the top
puzzle_pieces = [(start_x + i * (piece_size + spacing), start_y) for i in range(5)]

# Game loop
running = True
while running:
    screen.fill(BLACK)
    
    # Display title text
    title_text = title_font.render("Rebuild the Wormhole Generator!", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
    screen.blit(title_text, title_rect)
    
    # Display menu options
    for i, option in enumerate(menu_options):
        color = WHITE if i == selected_index else GRAY
        text_surface = font.render(option, True, color)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 300 + i * 50))
        screen.blit(text_surface, text_rect)
    
    # Display puzzle progress
    for i, pos in enumerate(puzzle_pieces):
        if levels_completed[i]:
            pygame.draw.rect(screen, GREEN, (*pos, piece_size, piece_size))  # Filled piece
        else:
            pygame.draw.rect(screen, BLUE, (*pos, piece_size, piece_size), 2)  # Empty slot
    
    # Unlock secret level if all levels are completed
    if all(levels_completed) and not secret_level_unlocked:
        secret_level_unlocked = True
        menu_options.insert(5, "Secret Level")  # Add Secret Level to menu
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_index = (selected_index - 1) % len(menu_options)
            if event.key == pygame.K_DOWN:
                selected_index = (selected_index + 1) % len(menu_options)
            if event.key == pygame.K_RETURN:
                if selected_index == 0:
                    levels.level1.run_level()
                    levels_completed[0] = True
                elif selected_index == 1:
                    levels.level2.run_level()
                    levels_completed[1] = True
                elif selected_index == 2:
                    levels.level3.run_level()
                    levels_completed[2] = True
                elif selected_index == 3:
                    levels.level4.run_level()
                    levels_completed[3] = True
                elif selected_index == 4:
                    levels.level5.run_level()
                    levels_completed[4] = True
                elif selected_index == 5 and secret_level_unlocked:
                    result = levels.level6.run_level()  # Secret level
                    if result == "game_completed" and not final_sequence_triggered:
                        final_sequence_triggered = True
                        levels.ending.run_ending()  # Trigger final scientist reflection
                elif selected_index == len(menu_options) - 1:
                    running = False

    # Update display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()