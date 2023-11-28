# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
  print("INFO")

  return {
    "apiversion": "1",
    "author": "Shxrpy",  # TODO: Your Battlesnake Username
    "color": "#779980",  # TODO: Choose color
    "head": "crystal-power",  # TODO: Choose head
    "tail": "coffee",  # TODO: Choose tail
  }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
  print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
  print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
  is_move_safe = {"up": True, "down": True, "left": True, "right": True}
  # We've included code to prevent your Battlesnake from moving backwards
  my_head = game_state["you"]["body"][0]  # Coordinates of your head
  my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

  if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
    is_move_safe["left"] = False

  elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
    is_move_safe["right"] = False

  elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
    is_move_safe["down"] = False

  elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
    is_move_safe["up"] = False

  # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
  board_width = game_state['board']['width']
  board_height = game_state['board']['height']

  if my_head["x"] <= 0:  # Head is at left edge of board, don't move left
    is_move_safe["left"] = False

  elif my_head[
      "x"] >= board_width - 1:  # Head is at right edge of board, don't move right
    is_move_safe["right"] = False

  if my_head["y"] <= 0:  # Head is at bottom edge of board, don't move down
    is_move_safe["down"] = False

  elif my_head[
      "y"] >= board_height - 1:  # Head is at top edge of board, don't move up
    is_move_safe["up"] = False

  # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
  # Get the coordinates of your snake's body
  directions = ["up", "down", "left", "right"]
  my_body = game_state['you']['body']
  # Check each direction in order of preference
  for direction in directions:
    if is_move_safe[direction]:
      # Make a hypothetical move in that direction by creating a new head
      new_head = my_head.copy()
      if direction == "up":
        new_head["y"] += 1
      elif direction == "down":
        new_head["y"] -= 1
      elif direction == "left":
        new_head["x"] -= 1
      elif direction == "right":
        new_head["x"] += 1
      # Check if the hypothetical move causes the snake to collide with itself
      if new_head in my_body:
        is_move_safe[direction] = False

  # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
  opponents = game_state['board']['snakes']
  for opponent in opponents:
    for segment in opponent["body"]:
      if my_head["x"] == segment["x"] and my_head["y"] == segment["y"] + 1:
        is_move_safe["down"] = False

      elif my_head["x"] == segment["x"] and my_head["y"] == segment["y"] - 1:
        is_move_safe["up"] = False

      elif my_head["y"] == segment["y"] and my_head["x"] == segment["x"] + 1:
        is_move_safe["left"] = False

      elif my_head["y"] == segment["y"] and my_head["x"] == segment["x"] - 1:
        is_move_safe["right"] = False

  # Are there any safe moves left?
  safe_moves = [
    direction for direction, is_safe in is_move_safe.items() if is_safe
  ]

  if len(safe_moves) == 0:
    print(f"MOVE {game_state['turn']}: No safe moves detected!")
    # No safe moves so choose randomly from among all moves
    next_move = random.choice(directions)
  else:
    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

  # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
  food = game_state['board']['food']
  if food:
    # Calculate the Manhattan distance between the head and each food
    distances = [
      abs(my_head['x'] - food['x']) + abs(my_head['y'] - food['y'])
      for food in food
    ]
  # Find the index of the closest food
  closest_food_index = distances.index(min(distances))
  closest_food = food[closest_food_index]

  # Determine the available safe moves towards the closest food
  safe_moves_towards_food = []
  if closest_food['x'] < my_head['x'] and is_move_safe['left']:
    safe_moves_towards_food.append('left')
  if closest_food['x'] > my_head['x'] and is_move_safe['right']:
    safe_moves_towards_food.append('right')
  if closest_food['y'] < my_head['y'] and is_move_safe['down']:
    safe_moves_towards_food.append('down')
  if closest_food['y'] > my_head['y'] and is_move_safe['up']:
    safe_moves_towards_food.append('up')

  if safe_moves_towards_food:
    next_move = random.choice(safe_moves_towards_food)

  if not next_move:
    next_move = random.choice(safe_moves)

#     print(f"MOVE {game_state['turn']}: Moving towards food {closest_food}                    ({safe_moves_towards_food})")
#     return {"move": next_move}

# # Get the coordinates of all food on the board
# food = game_state['board']['food']

# # Find the closest food
# closest_food = None
# min_dist = 9999
# for f in food:
#     dist = abs(f["x"] - my_head["x"]) + abs(f["y"] - my_head["y"])
#     if dist < min_dist:
#         min_dist = dist
#         closest_food = f

# if closest_food:
#     # Move towards the closest food if possible
#     if my_head["x"] < closest_food["x"]:
#         if "right" in safe_moves:
#             next_move = "right"
#     elif my_head["x"] > closest_food["x"]:
#         if "left" in safe_moves:
#             next_move = "left"
#     elif my_head["y"] < closest_food["y"]:
#         if "up" in safe_moves:
#             next_move = "up"
#     elif my_head["y"] > closest_food["y"]:
#         if "down" in safe_moves:
#             next_move = "down"

# If moving towards food is not possible, choose a random safe move

  print(f"MOVE {game_state['turn']}: {next_move} ({safe_moves})")
  return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
  from server import run_server

  run_server({"info": info, "start": start, "move": move, "end": end})
