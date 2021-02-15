from game import SnakeGame, Direction
from time import sleep

snake_commands = [Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.LEFT]

game = SnakeGame()

for move in snake_commands:
    game.play_step(move)
    sleep(1)
