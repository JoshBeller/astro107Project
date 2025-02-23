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
    pygame.display.set_caption("Level 3 - Hawking’s Radiation Storm")
    
    # Colors
    BLACK = (0, 0, 30)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    
    # Font
    font = pygame.font.Font(None, 36)
    speech_font = pygame.font.Font(None, 28)
    
    # Load Stephen Hawking image
    hawking_img = pygame.image.load("hawking.png")  # Ensure the image exists
    hawking_img = pygame.transform.scale(hawking_img, (100, 100))
    
    # Introduction dialogue
    intro_dialogue = [
        "Stephen Hawking: Welcome, traveler!",
        "Black holes are not entirely black! They emit radiation.",
        "This effect, called Hawking Radiation, slowly evaporates black holes.",
        "Use arrow keys to move the radiation channel.",
        "Balance the energy flow to stabilize the Radiation Converter!"
    ]
    intro_index = 0
    show_puzzle = False
    show_end_dialogue = False
    game_completed = False
    end_dialogue_index = 0
    
    display_completion_message = False
    hide_player_controls = False

    # End dialogue
    end_dialogue = [
        "Well done! You have stabilized the Radiation Converter!",
        "This balance of energy mirrors how black holes evaporate over time.",
        "Hawking Radiation plays a crucial role in our understanding of the universe.",
        "Press ENTER to return to the main menu."
    ]
    
    # Radiation Channel (Player-Controlled)
    channel = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 100, 50, 10)
    channel_speed = 7
    
    # Radiation Particles
    particles = []
    particle_speed = 4
    particle_spawn_rate = 30  # Faster spawn rate
    spawn_timer = 0
    
    # Circuit Board
    circuits = [pygame.Rect(250, 250, 50, 50), pygame.Rect(500, 250, 50, 50)]
    circuit_status = [0, 0]  # 0 = neutral, 1 = blue (cool), 2 = red (hot)
    circuit_counts = [0, 0]  # Track how many particles have hit
    required_particles = 5  # Each circuit needs exactly 5 particles to stabilize
    
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
                if not show_puzzle:
                    if event.key == pygame.K_RETURN:
                        intro_index += 1
                        if intro_index >= len(intro_dialogue):
                            show_puzzle = True
                elif display_completion_message and not show_end_dialogue:
                    show_end_dialogue = True
                    hide_player_controls = True
                elif show_end_dialogue and event.key == pygame.K_RETURN:
                    end_dialogue_index += 1
                    if end_dialogue_index >= len(end_dialogue):
                        return  # Return to main menu
        
        if not show_puzzle:
            screen.blit(hawking_img, (50, HEIGHT - 200))
            speech_bubble = pygame.Rect(170, HEIGHT - 200, 500, 100)
            pygame.draw.rect(screen, WHITE, speech_bubble, border_radius=10)
            
            lines = wrap_text(intro_dialogue[intro_index], speech_font, 480)
            for i, line in enumerate(lines):
                text_surface = speech_font.render(line, True, BLACK)
                screen.blit(text_surface, (180, HEIGHT - 180 + i * 25))
            instruction_surface = font.render("Press ENTER to continue", True, WHITE)
            screen.blit(instruction_surface, (WIDTH // 2 - 100, HEIGHT - 50))
        elif not game_completed and not hide_player_controls:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and channel.x > 0:
                channel.x -= channel_speed
            if keys[pygame.K_RIGHT] and channel.x < WIDTH - channel.width:
                channel.x += channel_speed
            
            # Spawn particles
            spawn_timer += 1
            if spawn_timer >= particle_spawn_rate:
                x_position = channel.x + channel.width // 2 - 10
                color = random.choice([BLUE, RED])
                particles.append((pygame.Rect(x_position, channel.y - 10, 15, 15), color))
                spawn_timer = 0
            
            # Move particles
            for particle in particles[:]:
                particle[0].y -= particle_speed
                for i, circuit in enumerate(circuits):
                    if particle[0].colliderect(circuit):
                        if circuit_counts[i] < required_particles:
                            circuit_counts[i] += 1
                            circuit_status[i] = 1 if particle[1] == BLUE else 2
                        particles.remove(particle)
                        break
            
            # Draw circuits with required amount indicators
            for i, circuit in enumerate(circuits):
                pygame.draw.rect(screen, WHITE, circuit, 2)
                if circuit_status[i] == 1:
                    pygame.draw.rect(screen, BLUE, circuit)
                elif circuit_status[i] == 2:
                    pygame.draw.rect(screen, RED, circuit)
                count_text = font.render(f"{circuit_counts[i]}/{required_particles}", True, YELLOW)
                screen.blit(count_text, (circuit.x + 10, circuit.y - 30))
            
            # Draw particles
            for particle in particles:
                pygame.draw.rect(screen, particle[1], particle[0])
            
            # Draw player-controlled channel
            pygame.draw.rect(screen, GREEN, channel)
            
            # Check for completion
            if circuit_counts == [required_particles, required_particles]:
                display_completion_message = True
                hide_player_controls = True
            
        if show_end_dialogue:
            screen.blit(hawking_img, (50, HEIGHT - 200))
            speech_bubble = pygame.Rect(170, HEIGHT - 200, 500, 100)
            pygame.draw.rect(screen, WHITE, speech_bubble, border_radius=10)
            
            lines = wrap_text(end_dialogue[end_dialogue_index], speech_font, 480)
            for i, line in enumerate(lines):
                text_surface = speech_font.render(line, True, BLACK)
                screen.blit(text_surface, (180, HEIGHT - 180 + i * 25))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    run_level()
