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
    pygame.display.set_caption("Level 2 - Schwarzschild’s Singularity Core")

    # Colors
    BLACK = (0, 0, 30)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    # Font
    font = pygame.font.Font(None, 36)
    speech_font = pygame.font.Font(None, 28)

    # Load Schwarzschild image
    schwarzschild_img = pygame.image.load("schwarzschild.png")  # Ensure image exists
    schwarzschild_img = pygame.transform.scale(schwarzschild_img, (100, 100))

    # Introduction dialogue
    intro_dialogue = [
        "Karl Schwarzschild: Welcome, traveler! You are about to uncover the secrets of black holes!",
        "Using Einstein’s equations, I derived the Schwarzschild radius—the boundary of a black hole, also known as the event horizon.",
        "If an object's mass is compressed within this critical radius, not even light can escape!",
        "Understanding this concept is key to grasping how black holes form.",
        "Let’s calculate the Schwarzschild radius for a given mass and explore its implications!"
    ]
    intro_index = 0
    show_question = False
    show_result = False
    show_completion = False
    completion_index = 0

    # Math question generation
    def generate_question():
        mass = random.randint(5, 50)  # Solar masses
        radius = mass * 3  # Schwarzschild radius approximation in km
        return f"A black hole of {mass} solar masses has a radius of?", str(radius), mass, radius
    
    question, correct_answer, mass, radius = generate_question()
    user_input = ""
    answer_correct = None

    completion_dialogue = [
        "Karl Schwarzschild: Excellent work! You have successfully determined the Schwarzschild radius!",
        "This radius defines the event horizon—the point of no return for anything falling into a black hole.",
        "Your calculations mirror the foundation of modern black hole physics!",
        "With this knowledge, you are now equipped to explore the mysteries of spacetime.",
        "Press ENTER to return to the main menu."
    ]

    
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
                if not show_question:
                    if event.key == pygame.K_RETURN:
                        intro_index += 1
                        if intro_index >= len(intro_dialogue):
                            show_question = True
                elif show_question and not show_result:
                    if event.key == pygame.K_RETURN:
                        if user_input == correct_answer:
                            answer_correct = True
                            show_result = True
                        else:
                            answer_correct = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit():
                        user_input += event.unicode
                elif show_result and not show_completion:
                    if event.key == pygame.K_RETURN:
                        show_completion = True
                        completion_index = 0  # Reset index for dialogue
                elif show_completion and event.key == pygame.K_RETURN:
                    completion_index += 1
                    if completion_index >= len(completion_dialogue):
                        return  # Instead of quitting, return to main menu
        
        # Display Schwarzschild image and speech bubble
        screen.blit(schwarzschild_img, (50, HEIGHT - 200))
        speech_bubble = pygame.Rect(170, HEIGHT - 200, 500, 100)
        pygame.draw.rect(screen, WHITE, speech_bubble, border_radius=10)
        
        if not show_question:
            lines = wrap_text(intro_dialogue[intro_index], speech_font, 480)
            for i, line in enumerate(lines):
                text_surface = speech_font.render(line, True, BLACK)
                screen.blit(text_surface, (180, HEIGHT - 190 + i * 25))
            instruction_surface = font.render("Press ENTER to continue", True, WHITE)
            screen.blit(instruction_surface, (WIDTH // 2 - 100, HEIGHT - 50))
        elif not show_result:
            # Show question and input box
            lines = wrap_text(question, speech_font, 480)
            for i, line in enumerate(lines):
                question_surface = speech_font.render(line, True, BLACK)
                screen.blit(question_surface, (180, HEIGHT - 190 + i * 25))
            
            # Display formula for Schwarzschild radius
            formula_surface = speech_font.render("Formula: R = 3 * M (km)", True, WHITE)
            screen.blit(formula_surface, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
            
            input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 40)
            pygame.draw.rect(screen, WHITE, input_box, 2)
            input_surface = font.render(user_input, True, WHITE)
            screen.blit(input_surface, (input_box.x + 10, input_box.y + 5))
            
            if answer_correct is not None:
                result_text = "Correct!" if answer_correct else "Incorrect! Try again."
                result_color = GREEN if answer_correct else RED
                result_surface = font.render(result_text, True, result_color)
                screen.blit(result_surface, (WIDTH // 2 - 60, HEIGHT // 2 + 50))
        elif show_completion:
            lines = wrap_text(completion_dialogue[completion_index], speech_font, 480)
            for i, line in enumerate(lines):
                text_surface = speech_font.render(line, True, BLACK)
                screen.blit(text_surface, (180, HEIGHT - 190 + i * 25))
            instruction_surface = font.render("Press ENTER to continue", True, WHITE)
            screen.blit(instruction_surface, (WIDTH // 2 - 100, HEIGHT - 50))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    run_level()
