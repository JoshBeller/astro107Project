import pygame
import sys

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

def run_ending():
    pygame.init()
    
    # Screen settings
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Final Reflection")
    
    # Colors
    BLACK = (0, 0, 30)
    WHITE = (255, 255, 255)
    
    # Font
    font = pygame.font.Font(None, 36)
    speech_font = pygame.font.Font(None, 28)
    
    # Load scientist images
    scientists = [
        ("einstein.png", "Albert Einstein", "The fabric of space and time is more than what we see. The pursuit of knowledge is endless."),
        ("schwarzschild.png", "Karl Schwarzschild", "Through mathematics, we defined the event horizon. The true mystery still lies within."),
        ("hawking.png", "Stephen Hawking", "Even the darkest places in the universe emit light. Never stop searching for the unknown."),
        ("ghez.png", "Andrea Ghez", "The stars have guided us to the heart of the Milky Way. Keep exploring, for the universe is vast and full of wonder."),
        ("thorne.png", "Kip Thorne", "Wormholes, time travel, and black holes are no longer fiction. Science brings us closer to the impossible."),
        ("penrose.png", "Roger Penrose", "Singularities may be the key to new physics. What lies beyond them is up to the next generation of explorers.")
    ]
    
    scientist_index = 0
    show_message = True
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        screen.fill(BLACK)
        
        # Load and display scientist
        image_path, name, quote = scientists[scientist_index]
        scientist_img = pygame.image.load(image_path)
        scientist_img = pygame.transform.scale(scientist_img, (100, 100))
        screen.blit(scientist_img, (WIDTH // 2 - 50, HEIGHT // 2 - 150))
        
        # Display name
        name_surface = font.render(name, True, WHITE)
        name_rect = name_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        screen.blit(name_surface, name_rect)
        
        # Display quote in speech bubble
        speech_bubble = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 100)
        pygame.draw.rect(screen, WHITE, speech_bubble, border_radius=10)
        
        lines = wrap_text(quote, speech_font, WIDTH // 2 - 20)
        for i, line in enumerate(lines):
            text_surface = speech_font.render(line, True, BLACK)
            screen.blit(text_surface, (WIDTH // 4 + 10, HEIGHT // 2 + 10 + i * 25))
        
        instruction_surface = font.render("Press ENTER to continue", True, WHITE)
        screen.blit(instruction_surface, (WIDTH // 2 - 100, HEIGHT - 50))
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    scientist_index += 1
                    if scientist_index >= len(scientists):
                        show_message = False
                        running = False  # End the sequence
        
        pygame.display.flip()
        clock.tick(60)
    
    # Final message screen
    final_message = [
        "The universe is infinite, and so is curiosity.",
        "Keep exploring!",
        "Thank you for playing!"
    ]
    
    running = True
    while running:
        screen.fill(BLACK)
        
        for i, line in enumerate(final_message):
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20 + i * 40))
            screen.blit(text_surface, text_rect)
        
        instruction_surface = font.render("Press ENTER to return to main menu", True, WHITE)
        screen.blit(instruction_surface, (WIDTH // 2 - 150, HEIGHT - 50))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                    return "ending_complete"
        
        pygame.display.flip()
        clock.tick(60)
    
if __name__ == "__main__":
    run_ending()