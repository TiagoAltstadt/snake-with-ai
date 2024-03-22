import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    RIGHT= 1
    Left = 2
    UP= 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# Game Variables
BLOCK_SIZE = 20
SPEED = 10

## Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)

class SnakeGame:

    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

        # init the display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake by Goia')
        self.clock = pygame.time.Clock()

        #init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head, 
                      Point(self.head.x - BLOCK_SIZE, self.head.y), 
                      Point(self.head.x - (2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.height-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)
        if(self.food in self.snake):
            self._place_food()

    def play_step(self):

        # collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.Left
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # move
        self._move(self.direction) # updating head
        self.snake.insert(0, self.head) # updating body

        # check if came over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # place new food or just move snake

        if self.head == self.food:
            self.score += 1
            self._place_food()
        else: 
            self.snake.pop()

        # update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        #return game over and score
        return game_over, self.score

    def _is_collision(self):
        if self.head.x > self.width - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.height - BLOCK_SIZE or self.head.y < 0:
            return True
        if self.head in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE)) # Head
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12)) # Body

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: "+str(self.score), True, WHITE)

        self.display.blit(text, [0,0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.Left:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        self.head = Point(x, y)

if __name__ == '__main__':
    game = SnakeGame()

    # game loop
    while True: 
        game_over, score = game.play_step()
        if game_over == True:
            break
    print('Final Score', score)

    pygame.quit()