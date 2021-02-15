from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import random
from enum import Enum, IntEnum
from collections import namedtuple
import torch


class Direction(IntEnum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3

class State(IntEnum):
    FOOD_UP = 0
    FOOD_RIGHT = 1
    FOOD_LEFT = 2
    FOOD_DOWN = 3

    COLLISION_UP = 4
    COLLISION_RIGHT = 5
    COLLISION_LEFT = 6
    COLLISION_DOWN = 7

    DIRECTION_UP = 8
    DIRECTION_RIGHT = 9
    DIRECTION_LEFT = 10
    DIRECTION_DOWN = 11

Point = namedtuple('Point', 'x, y')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)


BLOCK_SIZE = 20
SPEED = 100

pygame.init()
font = pygame.font.SysFont('arial', 25)

class SnakeGame:

    def __init__(self, w=640, h=480):

        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('snakeRL')
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT

        # start snake in the middle of the screen
        self.head = Point(self.w/2, self.h/2)

        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - 2*BLOCK_SIZE, self.head.y),
                      Point(self.head.x - 4*BLOCK_SIZE, self.head.y)]


        self.score = 0
        self.food = None
        self._place_food()


    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE

        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food()

    def _is_collision(self):

        # wall collision
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        
        # self collision
        if self.head in self.snake[1:]:
            return True
        
        return False

    def play_step(self, move):
        """
        Play one step - one move only
        """

            # Don't allow 180 turns
        if move == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        elif move == Direction.DOWN and self.direction != Direction.UP:
            self.direction = Direction.DOWN
        elif move == Direction.UP and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        elif move == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT


        self._move(self.direction)
        self.snake.insert(0, self.head)
        
        if self._is_collision():
            return True, None, -10 # negative reward for game over
        
        self.update_state()
        # print(self.snake)
        # print("\n\n")

        if self.head == self.food:
            self.score += 1
            self._place_food()

            self._update_ui()
            self.clock.tick(SPEED)

            # print("ATE FOOD")

            return False, tuple(self.state), 1
        else:
            # makes the snake "move" - tail leaves the current block
            self.snake.pop()

            self._update_ui()
            self.clock.tick(SPEED)

            return False, tuple(self.state), -1

    def _update_food_state(self, h, f):
        # food is towards right
        if h.x < f.x:
            self.state[State.FOOD_RIGHT] = 1
        # food is towards left
        elif h.x > f.x:
            self.state[State.FOOD_LEFT] = 1
        
        # food is down
        if h.y < f.y:
            self.state[State.FOOD_DOWN] = 1
        # food is up
        elif h.y > f.y:
            self.state[State.FOOD_UP] = 1

    def _update_collision_state(self):

        # wall is right or self collision is right
        if self.head.x + BLOCK_SIZE == self.w or ( (self.head.x + BLOCK_SIZE) in [s.x for s in self.snake[1:] if self.head.y == s.y] and self.direction != Direction.LEFT):
            self.state[State.COLLISION_RIGHT] = 1
            # print("COLLISION RIGHT")

        # wall is left or self collision is left
        if self.head.x == 0 or ( (self.head.x - BLOCK_SIZE) in [s.x for s in self.snake[1:] if self.head.y == s.y] and self.direction != Direction.RIGHT):
            self.state[State.COLLISION_LEFT] = 1
            # print("COLLISION LEFT")

        # wall is down or self collision is down
        if self.head.y + BLOCK_SIZE == self.h or ( (self.head.y + BLOCK_SIZE) in [s.y for s in self.snake[1:] if self.head.x == s.x] and self.direction != Direction.UP):
            self.state[State.COLLISION_DOWN] = 1
            # print("COLLISION DOWN")

        # wall is up or self collision is up
        if self.head.y == 0 or ( (self.head.x - BLOCK_SIZE) in [s.x for s in self.snake[1:] if self.head.y == s.y] and self.direction != Direction.DOWN):
            self.state[State.COLLISION_UP] = 1
            # print("COLLISION UP")

    def _update_direction_state(self):
        if self.direction == Direction.RIGHT:
            self.state[State.DIRECTION_RIGHT] = 1
        elif self.direction == Direction.UP:
            self.state[State.DIRECTION_UP] = 1
        elif self.direction == Direction.LEFT:
            self.state[State.DIRECTION_LEFT] = 1
        elif self.direction == Direction.DOWN:
            self.state[State.DIRECTION_DOWN] = 1

    def update_state(self):
        """
        f: food
        c: collision

        [fu, fr, fl, fd,
         cu, cr, cl, cd]
        """ 

        self.state = [0 for i in range(12)]

        h = self.head
        f = self.food

        self._update_food_state(h, f)
        
        self._update_collision_state()

        self._update_direction_state()
        

    def _move(self, direction):
        """
        Move one block in "direction" direction
        """

        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

    def _update_ui(self):
        """
        Update UI/game board
        """

        self.display.fill(BLACK)

        # draw snake
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        # draw food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip() # ????

