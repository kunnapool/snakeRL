from game import SnakeGame, Direction
from time import sleep

snake_commands = [Direction.UP for i in range(20)]
snake_commands[2] = Direction.LEFT
snake_commands[3] = Direction.DOWN


game = SnakeGame()

for move in snake_commands:
    
    over, _ = game.play_step(move)
    if over:
        break

    sleep(2)
