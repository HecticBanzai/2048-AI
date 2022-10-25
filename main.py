from game import Game, translate
from getkey import getkey, keys
import random
import os

grid = [0 for i in range(16)]

while grid.count(0) != 14:
        
  random_index = random.randint(0, 15)
  random_tile = random.choice([2, 4])
        
  if grid[random_index] == 0:
    grid[random_index] = random_tile

new_game = Game(grid, 0)

manual_or_ai = int(input("Enter 0 if you want to play 2048. Enter 1 if you want to see the AI play 2048. \n"))

if manual_or_ai == 0:
  print(new_game)
  
  while new_game.can_move():
    print("Use WASD keys to move the tiles \n")
    next_move = getkey()
    if new_game.valid_move(next_move):
      os.system('cls')

      if next_move == 'a':
        new_game = new_game.left() 
      
      elif next_move == 'd':
        new_game = new_game.right()
      
      elif next_move == 'w':
        new_game = new_game.up()
      
      elif next_move == 's':
        new_game = new_game.down()
  
      new_game = new_game.place_new_random()
  
    print(new_game)
elif manual_or_ai == 1:
  while new_game.can_move():
    print(new_game)
    
    next_move = new_game.minimax(2, 0)[1]
    print(translate[next_move])
    print(new_game)
  
    if new_game.valid_move(next_move):
      os.system('cls')
      
      if next_move == keys.LEFT:
        new_game = new_game.left() 
      
      elif next_move == keys.RIGHT:
        new_game = new_game.right()
      
      elif next_move == keys.UP:
        new_game = new_game.up()
      
      elif next_move == keys.DOWN:
        new_game = new_game.down()
  
      new_game = new_game.place_new_random()
  
    print(new_game)

print("Game Over!")
print(f"Your high score was {new_game.score}")
input("Press enter to exit")
