import pygame
import sys
import random

def wrap_text(text, font, max_width):
    """Splits text into multiple lines if it exceeds max_width."""
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    
    lines.append(current_line)
    return lines

def run_level():
    pygame.init()

    # Screen settings
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Level 1 - Einstein’s Spacetime Lens")

    # Colors
    BLACK = (0, 0, 30)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)
    LIGHT_BLUE = (173, 216, 230)
    GREEN = (0, 255, 0)

    # Font
    font = pygame.font.Font(None, 36)
    speech_font = pygame.font.Font(None, 28)

    # Load Einstein image
    einstein_img = pygame.image.load("einstein.png")  # Ensure the image exists in the directory
    einstein_img = pygame.transform.scale(einstein_img, (100, 100))

    # Dialogue
    dialogue = [
        "Albert Einstein: Welcome, traveler!",
        "I will teach you about gravitational lensing.",
        "Light bends around massive objects like black holes.",
        "Use the arrow keys to move left and right.",
        "Press ENTER to start the minigame!"
    ]
    dialogue_index = 0
    
    completion_dialogue = [
        "Congratulations! You have reconstructed the Spacetime Lens!",
        "Einstein’s work on General Relativity showed that gravity bends light.",
        "This effect, called gravitational lensing, allows us to see galaxies hidden behind black holes.",
        "Press ENTER to return to the main menu."
    ]
    completion_index = 0
    
    show_minigame = False
    show_completion_dialogue = False
    collected = 0
    target_collect = 10
    game_completed = False

    # Player settings
    player = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 60, 40, 40)
    player_speed = 7

    # Light fragments (collectibles)
    fragments = []
    fragment_speed = 4
    spawn_rate = 30  # Frames per spawn
    spawn_timer = 0

    clock = pygame.time.Clock()
    running = True
    
    while running:
        screen.fill(BLACK)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not show_minigame:
                    if event.key == pygame.K_RETURN:
                        dialogue_index += 1
                        if dialogue_index >= len(dialogue):
                            show_minigame = True
                elif game_completed and not show_completion_dialogue:
                    show_completion_dialogue = True
                elif show_completion_dialogue and event.key == pygame.K_RETURN:
                    completion_index += 1
                    if completion_index >= len(completion_dialogue):
                        return  # Return instead of quitting
        
        # Display dialogue with Einstein
        if not show_minigame:
            screen.blit(einstein_img, (50, HEIGHT - 200))  # Display Einstein image
            speech_bubble = pygame.Rect(170, HEIGHT - 200, 500, 100)
            pygame.draw.rect(screen, WHITE, speech_bubble, border_radius=10)
            
            lines = wrap_text(dialogue[dialogue_index], speech_font, 480)
            for i, line in enumerate(lines):
                text_surface = speech_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(topleft=(180, HEIGHT - 190 + i * 25))
                screen.blit(text_surface, text_rect)
            
            instruction_surface = font.render("Press ENTER to continue", True, WHITE)
            instruction_rect = instruction_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(instruction_surface, instruction_rect)
        elif not game_completed:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x > 0:
                player.x -= player_speed
            if keys[pygame.K_RIGHT] and player.x < WIDTH - player.width:
                player.x += player_speed
            
            # Spawn light fragments
            spawn_timer += 1
            if spawn_timer >= spawn_rate:
                fragments.append(pygame.Rect(random.randint(20, WIDTH - 20), 0, 20, 20))
                spawn_timer = 0
            
            # Move fragments
            for fragment in fragments:
                fragment.y += fragment_speed
            
            # Check for collisions
            for fragment in fragments[:]:
                if player.colliderect(fragment):
                    fragments.remove(fragment)
                    collected += 1
            
            # Check win condition
            if collected >= target_collect:
                game_completed = True
            
            # Draw player
            pygame.draw.rect(screen, BLUE, player)
            
            # Draw fragments
            for fragment in fragments:
                pygame.draw.rect(screen, LIGHT_BLUE, fragment)
            
            # Display score
            score_text = font.render(f"Collected: {collected}/{target_collect}", True, WHITE)
            screen.blit(score_text, (20, 20))
        elif show_completion_dialogue:
            # Display completion message with Einstein
            screen.blit(einstein_img, (50, HEIGHT - 200))  # Display Einstein image
            speech_bubble = pygame.Rect(170, HEIGHT - 220, 550, 120)
            pygame.draw.rect(screen, WHITE, speech_bubble, border_radius=10)
            
            lines = wrap_text(completion_dialogue[completion_index], speech_font, 530)
            for i, line in enumerate(lines):
                text_surface = speech_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(topleft=(180, HEIGHT - 210 + i * 25))
                screen.blit(text_surface, text_rect)
            
            instruction_surface = font.render("Press ENTER to continue", True, WHITE)
            instruction_rect = instruction_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(instruction_surface, instruction_rect)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    run_level()
