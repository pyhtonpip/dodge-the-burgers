import pygame
import random
import os

# Constants for the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
LIGHT_RED = (255, 128, 128)
DARK_RED = (128, 0, 0)
RED = (255, 0, 0)

# Game class
class DodgeBurgersGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("DodgeTheBurgers")
        self.clock = pygame.time.Clock()

        # Game state variables
        self.player_y = SCREEN_HEIGHT // 2
        self.burgers = []
        self.score = 0
        self.highscore = {"Easy": 0, "Medium": 0, "Hard": 0, "Impossible": 0}
        self.running = True
        self.difficulty_selected = False

        # Default speeds
        self.player_speed = 0
        self.burger_speed = 0

        # Load sprites and scale them
        self.character_sprite = pygame.image.load("sprites/character.png").convert_alpha()
        self.character_sprite = pygame.transform.scale(self.character_sprite, (50, 50))  # Scale character
        self.burger_sprite = pygame.image.load("sprites/burger.png").convert_alpha()
        self.burger_sprite = pygame.transform.scale(self.burger_sprite, (50, 50))  # Scale burger

        self.load_highscores()
        self.show_difficulty_selection()

    def load_highscores(self):
        """ Load high scores from a file. """
        if os.path.exists("highscore.txt"):
            try:
                with open("highscore.txt", "r") as file:
                    for line in file:
                        difficulty, score = line.strip().split(": ")
                        self.highscore[difficulty] = int(score)
            except Exception as e:
                print(f"Error loading high scores: {e}")
                # Reset high scores on error
                self.highscore = {"Easy": 0, "Medium": 0, "Hard": 0, "Impossible": 0}

    def save_highscores(self):
        """ Save high scores to a file. """
        try:
            with open("highscore.txt", "w") as file:
                for difficulty, score in self.highscore.items():
                    file.write(f"{difficulty}: {score}\n")
        except Exception as e:
            print(f"Error saving high scores: {e}")

    def show_difficulty_selection(self):
        while not self.difficulty_selected:
            self.screen.fill(WHITE)
            font = pygame.font.Font(None, 74)
            text = font.render("Select Difficulty", True, BLACK)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 4))

            easy_text = font.render("Press 1 for Easy", True, GREEN)
            medium_text = font.render("Press 2 for Medium", True, YELLOW)
            hard_text = font.render("Press 3 for Hard", True, LIGHT_RED)
            impossible_text = font.render("Press 4 for Impossible", True, DARK_RED)
            self.screen.blit(easy_text, (SCREEN_WIDTH // 2 - easy_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(medium_text, (SCREEN_WIDTH // 2 - medium_text.get_width() // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(hard_text, (SCREEN_WIDTH // 2 - hard_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(impossible_text, (SCREEN_WIDTH // 2 - impossible_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:  # Easy mode
                        self.set_difficulty(easy=True, medium=False, hard=False, impossible=False)
                    elif event.key == pygame.K_2:  # Medium mode
                        self.set_difficulty(easy=False, medium=True, hard=False, impossible=False)
                    elif event.key == pygame.K_3:  # Hard mode
                        self.set_difficulty(easy=False, medium=False, hard=True, impossible=False)
                    elif event.key == pygame.K_4:  # Impossible mode
                        self.set_difficulty(easy=False, medium=False, hard=False, impossible=True)

    def set_difficulty(self, easy, medium, hard, impossible):
        if easy:
            self.player_speed = 2
            self.burger_speed = 5
            self.current_difficulty = "Easy"
        elif medium:
            self.player_speed = 3
            self.burger_speed = 13
            self.current_difficulty = "Medium"
        elif hard:
            self.player_speed = 5
            self.burger_speed = 20
            self.current_difficulty = "Hard"
        elif impossible:
            self.player_speed = 999999
            self.burger_speed = 999999
            self.current_difficulty = "Impossible"
        
        self.difficulty_selected = True
        self.run_game()

    def run_game(self):
        self.score = 0  # Reset score on game start
        self.burgers = []  # Reset burgers on game start
        self.player_y = SCREEN_HEIGHT // 2  # Reset player position

        while self.running:
            self.handle_events()
            self.update_burgers()
            self.draw()
            self.clock.tick(60)

        self.show_game_over()

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player_y -= self.player_speed
            if self.player_speed >= 999999:  # If difficulty is impossible
                self.running = False  # Immediately end the game

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player_y += self.player_speed
            if self.player_speed >= 999999:  # If difficulty is impossible
                self.running = False  # Immediately end the game

        # Ensure the player stays within bounds
        if self.player_y < 0:
            self.player_y = 0
        if self.player_y > SCREEN_HEIGHT - self.character_sprite.get_height():
            self.player_y = SCREEN_HEIGHT - self.character_sprite.get_height()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update_burgers(self):
        # Burger logic (spawning and moving)
        if random.random() < 0.02:  # Spawn a burger occasionally
            self.burgers.append({'x': SCREEN_WIDTH, 'y': random.randint(0, SCREEN_HEIGHT - self.burger_sprite.get_height())})

        for burger in self.burgers[:]:  # Iterate over a copy of the list
            burger['x'] -= self.burger_speed
            if burger['x'] < 0:
                self.burgers.remove(burger)
                self.score += 1

            # Check for collision
            if (100 < burger['x'] < 100 + self.character_sprite.get_width() and
                self.player_y < burger['y'] + self.burger_sprite.get_height() and
                self.player_y + self.character_sprite.get_height() > burger['y']):
                self.running = False  # End game on collision

    def draw(self):
        self.screen.fill(WHITE)
        # Draw player
        self.screen.blit(self.character_sprite, (100, self.player_y))
        # Draw burgers
        for burger in self.burgers:
            self.screen.blit(self.burger_sprite, (burger['x'], burger['y']))

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        highscore_text = font.render(f"High Score: {self.highscore[self.current_difficulty]}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(highscore_text, (10, 40))

        pygame.display.flip()

    def show_game_over(self):
        # Update high score if necessary
        if self.score > self.highscore[self.current_difficulty]:
            self.highscore[self.current_difficulty] = self.score
            self.save_highscores()

        while not self.running:
            self.screen.fill(WHITE)
            font = pygame.font.Font(None, 74)
            game_over_text = font.render("Game Over", True, RED)  # Change color to red
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 4))

            restart_text = font.render("Press R to Restart", True, BLACK)
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart the game
                        self.running = True
                        self.difficulty_selected = False  # Go back to difficulty selection
                        self.show_difficulty_selection()  # Show difficulty selection

# Main function to start the game
if __name__ == "__main__":
    DodgeBurgersGame()
