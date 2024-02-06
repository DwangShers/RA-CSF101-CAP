# https://www.youtube.com/watch?v=1zVlRXd8f7g
# https://opensource.com/article/20/1/add-scorekeeping-your-python-game
# https://chat.openai.com/

import pygame # This line imports the Pygame library which is a set of Python modules designed for writing games
import sys #The sys module provides access to some variables used or maintained by the Python interpreter
import random
import time
from pygame.math import Vector2

pygame.init() # Is a function call that initializes all the Pygame modules

title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)


GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

cell_size = 30
number_of_cells = 25

OFFSET = 75

# Create a Food
class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)

    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        screen.blit(food_surface, food_rect)

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells -1)
        y = random.randint(0, number_of_cells -1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body):
        
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()                    
        return position

class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)
        self.add_segment = False
        self.eat_sound = pygame.mixer.Sound("Sounds/Eating.mp3")
        self.wall_hit_sound = pygame.mixer.Sound("Sounds/Crash.mp3")

    def draw(self):
        for segment in self.body:
            segment_rect = (OFFSET + segment.x * cell_size, OFFSET + segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, DARK_GREEN, segment_rect, 0, 7)

    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1]

    def reset(self):    
        self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1, 0)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
        self.score = 0
        self.foods_since_last_wall =  0
        self.walls = [Wall(initial_position=False)] # Start with one wall

    def draw(self):
        self.food.draw()
        self.snake.draw()
        for wall in self.walls:
            wall.draw()

    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()
            self.check_collision_with_walls()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            self.score += 1
            self.snake.eat_sound.play()
            self.foods_since_last_wall +=  1
            if self.foods_since_last_wall >=  3:
                self.add_wall()
                self.foods_since_last_wall =  0

    def check_collision_with_edges(self):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()

    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "GAMEOVER"
        self.score = 0
        self.snake.wall_hit_sound.play()

    def restart(self):
        self.score =  0
        self.foods_since_last_wall =  0
        self.walls = [Wall(initial_position=False)]  # Reset walls
        self.snake.reset()  # Reset snake
        self.state = "RUNNING"

    def add_wall(self):
        # Add a new wall to the game
        self.walls.append(Wall())

    def check_collision_with_walls(self):
        for wall in self.walls:
            if wall.check_collision(self.snake):
                self.game_over()

    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()

    


class Wall:
    def __init__(self, initial_position=True):
        self.shape = self.generate_random_shape()
        self.last_move_time = time.time()
        if initial_position:
            self.ensure_not_in_front_of_snake()

    def generate_random_shape(self):
        # Define a set of possible wall shapes
        shapes = [
            [(0,   0), (1,   0), (2,   0)],  # Horizontal line
            [(0,   0), (0,   1), (0,   2)],  # Vertical line
            [(0,   0), (1,   1), (2,   2)],  # Diagonal line
            [(0,   2), (1,   1), (2,   0)],  # Backward diagonal line
            [(0,   0), (1,   0), (2,   0), (2,   1), (2,   2)],  # Column
            [(0,   0), (0,   1), (0,   2), (1,   2), (2,   2)],  # Row
            [(0,   0), (1,   0), (2,   0), (2,   1), (2,   2), (1,   2)],  # Square
            [(0,   0), (1,   0), (2,   0), (2,   1), (2,   2), (1,   1)],  # L-shape
            [(0,   0), (1,   0), (2,   0), (2,   1), (2,   2), (1,   0)],  # T-shape
            [(0,   0), (1,   0), (2,   0), (2,   1), (2,   2), (0,   1)],  # Z-shape
            [(0,   0), (1,   0), (2,   0), (2,   1), (2,   2), (0,   2)]   # S-shape
        ]
        # Select a random shape
        return random.choice(shapes)

    def move(self):
        current_time = time.time()
        if current_time - self.last_move_time >=   7:
            # Generate a new random position for the wall
            x = random.randint(0, number_of_cells -  3)  # Subtract  3 to account for the wall's size
            y = random.randint(0, number_of_cells -  3)  # Subtract  3 to account for the wall's size
            self.shape = [[pos[0] + x, pos[1] + y] for pos in self.generate_random_shape()]
            self.last_move_time = current_time

    def ensure_not_in_front_of_snake(self):
        # Ensure the wall does not spawn in front of the snake
        while self.is_in_front_of_snake():
            self.move()

    def is_in_front_of_snake(self):
        head = game.snake.body[0]
        for pos in self.shape:
            if (pos[0] == head.x and abs(pos[1] - head.y) <=   1) or \
               (pos[1] == head.y and abs(pos[0] - head.x) <=   1):
                return True
        return False

    def draw(self):
        for pos in self.shape:
            wall_rect = pygame.Rect(OFFSET + pos[0] * cell_size, OFFSET + pos[1] * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, DARK_GREEN, wall_rect)  # Dark green color for walls

    def check_collision(self, snake):
        return any(pos in self.shape for pos in snake.body)




screen = pygame.display.set_mode((2*OFFSET + cell_size*number_of_cells, 2*OFFSET + cell_size*number_of_cells)) # is used to create the game window surface (or screen) with a specified size based on the number of cells and the size of each cell

pygame.display.set_caption("Twist and Turn Snake") # it is used to set the title or caption of the game window

clock = pygame.time.Clock() # it is used to create a Clock object, which is essential for controlling the frame rate of your game

game = Game()
food_surface = pygame.image.load("Graphics/food.png")

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)

wall = Wall()

#game loop
while True:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            if game.state == "RUNNING":
                game.update()
                for wall in game.walls:
                    wall.move()
                    if wall.check_collision(game.snake):
                        game.game_over()  # Assuming you have a game_over method in your Game class
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game.state == "GAMEOVER":
                game.restart()
                game.state = "RUNNING"
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)
    
    #Drawing 
    screen.fill(GREEN)
    pygame.draw.rect(screen, DARK_GREEN, (OFFSET-5, OFFSET-5, cell_size*number_of_cells+10, cell_size*number_of_cells+10), 5)
    game.draw()
    title_surface = title_font.render("Twist and Trun Sanke", True, DARK_GREEN)
    score_surface = score_font.render(str(game.score), True, DARK_GREEN)
    screen.blit(title_surface, (OFFSET-5, 20))
    screen.blit(score_surface, (OFFSET-5, OFFSET + cell_size*number_of_cells +10))

    pygame.display.update() # is used to update the entire display surface 
    clock.tick(60) #  is used to control the frame rate of your game loop