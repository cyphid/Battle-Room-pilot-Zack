# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
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
        "author": "shxrpy",  # TODO: Your Battlesnake Username
        "color": "#0fd6d6",  # TODO: Choose color
        "head": "replit-mark",  # TODO: Choose head
        "tail": "replit-notmark",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


def is_cell_occupied(x: int, y: int, board: typing.Dict) -> bool:
    """Check if a cell is occupied by a hazard, your snake, or enemy snakes."""
    # Check hazards
    if any(cell['x'] == x and cell['y'] == y for cell in board['hazards']):
        return True
    
    # Check for all snakes (including your own)
    for snake in board['snakes']:
        for segment in snake['body']:
            if segment['x'] == x and segment['y'] == y:
                return True
    
    return False
  
def move_towards_food(snake_pos, food_pos):
  dx = food_pos[0] - snake_pos[0]
  dy = food_pos[1] - snake_pos[1]
  
  if abs(dx) > abs(dy):
      if dx > 0 :
          return "right"
      else:
          return "left"
  else:
      if dy > 0 :
          return "down"
      else:
          return "up"


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

    if my_head['x'] == 0:  # Head is at the left boundary, don't move left
        is_move_safe['left'] = False
    
    elif my_head['x'] == board_width - 1:  # Head is at the right boundary, don't move right
        is_move_safe['right'] = False
    
    if my_head['y'] == 0:  # Head is at the top boundary, don't move up
        is_move_safe['down'] = False
    
    elif my_head['y'] == board_height - 1:  # Head is at the bottom boundary, don't move down
        is_move_safe['up'] = False
    
    
    for move, isSafe in is_move_safe.items():
        if isSafe:
            if move == "up":
                if is_cell_occupied(my_head['x'], my_head['y'] + 1, game_state['board']):
                    is_move_safe['up'] = False
            elif move == "down":
                if is_cell_occupied(my_head['x'], my_head['y'] - 1, game_state['board']):
                    is_move_safe['down'] = False
            elif move == "left":
                if is_cell_occupied(my_head['x'] - 1, my_head['y'], game_state['board']):
                    is_move_safe['left'] = False
            elif move == "right":
                if is_cell_occupied(my_head['x'] + 1, my_head['y'], game_state['board']):
                    is_move_safe['right'] = False
    
    
    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']
    
  
    # for food_item in food:
    #   food_pos = []
      
    #   dx = food_pos[0] - snake_pos[0]
    #   dy = food_pos[1] - snake_pos[1]
    

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})