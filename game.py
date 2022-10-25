import random
import copy
import math
from getkey import keys

INDEXES_ROTATED_RIGHT = [12, 8, 4, 0,
                        13, 9, 5, 1,
                        14, 10, 6, 2,
                        15, 11, 7, 3]
INDEXES_ROTATED_LEFT = [3, 7, 11, 15,
                        2, 6, 10, 14,
                        1, 5, 9, 13,
                        0, 4, 8, 12]
ALL_DIRECTIONS = [keys.LEFT, keys.RIGHT, keys.UP,keys.DOWN]
BEST_CASE_SNAKE = [2**1, 2**2, 2**3, 2**4,
                  2**8, 2**7, 2**6, 2**5,
                  2**9, 2**10, 2**11, 2**12,
                  2**16, 2**15, 2**14, 2**13]
SCORE_FROM_NUM_TILES = [2**(x+4) for x in range(1,17)]
CORNER_PRIORITY = [2**7, 2**5, 2**3, 2**1,
                   2**9, 2**7, 2**5, 2**3,
                   2**11, 2**9, 2**7, 2**5,
                   2**13, 2**11, 2**9, 2**7]
translate = {
  keys.LEFT : "left",
  keys.RIGHT : "right",
  keys.UP : "up",
  keys.DOWN : "down"
}

class Game:
  def __init__(self, grid, score):
    self.grid = grid
    self.score = score

  def __str__(self):
    grid = "------------\n"
    
    for i in range(0, 13, 4):
      for k in range(4):
        grid += f"|{self.grid[i + k]}|"
        
      grid += "\n------------\n"

    print(f"SCORE : {self.score}")

    return grid

  def indexes_of_tiles(self, grid):
    indexes = []
    
    for index in range(16):
      if grid[index] != 0:
        indexes.append(index)

    return indexes

  def score_corner_priority(game_grid):
    sum = 0
    for i in range(len(game_grid)):
      if game_grid[i] == 0:
        continue
      else:
        sum += game_grid[i] * CORNER_PRIORITY[i]

    return sum

  def score_moving_largest(game_grid):
    if game_grid[12] == max(game_grid):
      return max(game_grid) * 2**5
      
    return -(max(game_grid) * 2**10)

  def score_tile_count(game_grid):
    zero_count = game_grid.count(0)

    return SCORE_FROM_NUM_TILES[zero_count]

  def score_adding_tiles(current_score, original_score):
    return (current_score - original_score) * 2**4

  # def score_row_order(game_grid):
  #   score = 0
  #   for i in range(0, 16, 4):
  #     current_row = game_grid[i : i+4]

  #     for k in range(len(current_row) - 2):
  #       next = 1
  #       while current_row[k + next] == 0 and k + next < 3:
  #         next += 1
        
  #       if current_row[k] >= current_row[k + next]:
  #         score += 2 ** 6
  #       else:
  #         break

  #   for i in range(4):
  #     current_column = [game_grid[i + (4 * k)] for k in range(4)]
      

  #     for l in range(len(current_column) - 2):
  #       next = 1
  #       while current_column[l + next] == 0 and l + next < 3:
  #         next += 1
          
  #       if current_column[l] >= current_column[l + next]:
  #         score += 2 ** 6
  #       else:
  #         break
          
  #   return score

  def score_adding_opportunity(game_grid):
    score = 0
    for i in range(0, 16, 4):
      current_row = game_grid[i : i+4]

      for k in range(len(current_row) - 2):
        next = 1
        while current_row[k + next] == 0 and k + next < 3:
          next += 1
        
        if current_row[k] == current_row[k + next]:
          score += 2 ** 6
        else:
          break

      for i in range(4):
        current_column = [game_grid[i + (4 * k)] for k in range(4)]

        for l in range(len(current_column) - 2):
          next = 1
          while current_column[l + next] == 0 and l + next < 3:
            next += 1
          
          if current_column[l] == current_column[l + next]:
            score += 2 ** 6
          else:
            break
          
    return score
  
  def create_sim_game(self):
    sim_grid = copy.deepcopy(self.grid)
    sim_score = copy.deepcopy(self.score)

    return Game(sim_grid, sim_score)

  def input_to_move(self, input):
    if input == keys.LEFT:
      return self.left()
    elif input == keys.RIGHT:
      return self.right()
    elif input == keys.UP:
      return self.up()
    else: 
      return self.down()

  def place_new_random(self):
    new_grid = copy.deepcopy(self.grid)
    
    amount_of_zeros = new_grid.count(0)
    random_tile = random.choice([2, 4])
    
    while new_grid.count(0) == amount_of_zeros:
      random_pos = random.randint(0, 15)
      
      if new_grid[random_pos] != 0:
        continue
      else:
        new_grid[random_pos] = random_tile

    return Game(new_grid, self.score)

  def valid_move(self, move):
    sim_game = self.create_sim_game()
    sim_game = sim_game.input_to_move(move)

    if sim_game.grid == self.grid:
      return False

    return True

  def can_move(self):
    for direction in ALL_DIRECTIONS:
      sim_game = self.create_sim_game()

      if sim_game.input_to_move(direction).grid != self.grid:
        return True
      else:
        continue

    return False

  def add_together(self, grid, score):
    grid_with_sums = copy.deepcopy(grid)
    
    for i in range(0, 13, 4):
      used_indexes = []
      current_row = grid_with_sums[i : i +4]

      for k in range(3):
        if current_row[k] != 0 and k not in used_indexes:
          start_index = k
          end_index = 0

          for m in range(k + 1, 4):
            if current_row[m] == 0:
              continue
            elif current_row[m] != current_row[start_index]:
              break
            else:
              end_index = m
              break
              
          if end_index != 0 and end_index > start_index:
            row_with_sum = [current_row[start_index] + current_row[end_index]] + [0 for l in range(end_index - start_index)]
            
            grid_with_sums[start_index+i : end_index + i + 1] = row_with_sum

            score += current_row[start_index] + current_row[end_index]
          
            used_indexes.append(start_index)
            used_indexes.append(end_index)

    return grid_with_sums, score

  def slide_to_left(self, grid, tile_indexes, score):
    grid, new_score = self.add_together(grid, score)[0], self.add_together(grid, score)[1]
    
    for i in range(0, 13, 4):
      current_row = grid[i : i+4]
      indexes = [index for index in tile_indexes if index >= i and index < i + 4]

      if 0 in current_row:
        for index in indexes:
          leftmost_zero = current_row.index(0) + i

          if leftmost_zero < index:
            grid[leftmost_zero] = grid[index]
            grid[index] = 0
          
            current_row = grid[i : i + 4]

    return grid, new_score

  def rotate_90_right(self, grid):
    rotated_grid = [grid[i] for i in INDEXES_ROTATED_RIGHT]
    
    return rotated_grid

  def rotate_90_left(self, grid):
    rotated_grid = [grid[i] for i in INDEXES_ROTATED_LEFT]
    
    return rotated_grid

  def left(self):
    tile_indexes = self.indexes_of_tiles(self.grid)
    new_grid = copy.deepcopy(self.grid)
    new_score = copy.deepcopy(self.score)

    new_grid, new_score = self.slide_to_left(new_grid, tile_indexes, new_score)
    
    return Game(new_grid, new_score)

  def right(self):
    new_grid = copy.deepcopy(self.grid)
    new_score = copy.deepcopy(self.score)

    for i in range(2):
      new_grid = self.rotate_90_right(new_grid)

    tile_indexes = self.indexes_of_tiles(new_grid)
    new_grid, new_score = self.slide_to_left(new_grid, tile_indexes, new_score)

    for i in range(2):
      new_grid = self.rotate_90_left(new_grid)

    return Game(new_grid, new_score)

  def up(self):
    new_grid = copy.deepcopy(self.grid)
    new_score = copy.deepcopy(self.score)

    for i in range(3):
      new_grid = self.rotate_90_right(new_grid)

    tile_indexes = self.indexes_of_tiles(new_grid)
    new_grid, new_score = self.slide_to_left(new_grid, tile_indexes, new_score)

    for i in range(3):
      new_grid = self.rotate_90_left(new_grid)
    
    return Game(new_grid, new_score)

  def down(self):
    new_grid = copy.deepcopy(self.grid)
    new_score = copy.deepcopy(self.score)

    new_grid = self.rotate_90_right(new_grid)

    tile_indexes = self.indexes_of_tiles(new_grid)
    new_grid, new_score = self.slide_to_left(new_grid, tile_indexes, new_score)

    new_grid = self.rotate_90_left(new_grid)

    return Game(new_grid, new_score)

  def heuristic(self, previous_score):
    heuristic = 0

    heuristic += Game.score_corner_priority(self.grid)
    heuristic += Game.score_moving_largest(self.grid)
    heuristic += Game.score_tile_count(self.grid)
    heuristic += Game.score_adding_tiles(self.score, previous_score)
    heuristic += Game.score_adding_opportunity(self.grid)

    return heuristic

  def minimax(self, max_depth, current_depth, original_score = None, direction = None):  
    if max_depth == current_depth:
      return self.heuristic(original_score), direction

    if current_depth % 2 == 0:
      score, move = -math.inf, None

      for direction in ALL_DIRECTIONS:
        if not self.valid_move(direction):
          continue
        else:
          sim_game = self.create_sim_game()

          sim_game = self.input_to_move(direction)
          new_score, new_move = sim_game.minimax(max_depth, current_depth + 1, sim_game.score, direction)
          
          if new_score > score:
            score = new_score
            move = new_move

    else:
      score, move = math.inf, direction
      
      for i in range(16):
        if self.grid[i] == 0:
          sim_grid = copy.deepcopy(self.grid)
          sim_grid[i] = 2
          sim_score = copy.deepcopy(self.score)
          sim_game = Game(sim_grid, sim_score)

          new_score, new_move = sim_game.minimax(max_depth, current_depth + 1, sim_game.score, direction)

          if new_score < score:
            score = new_score
            move = new_move

        if self.grid[i] == 0:
          sim_grid = copy.deepcopy(self.grid)
          sim_grid[i] = 4
          sim_score = copy.deepcopy(self.score)
          sim_game = Game(sim_grid, sim_score)

          new_score, new_move = sim_game.minimax(max_depth, current_depth + 1, sim_game.score, direction)

          if new_score < score:
            score = new_score
            move = new_move

    return score, move