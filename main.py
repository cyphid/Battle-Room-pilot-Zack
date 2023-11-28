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
                "head": "gamer",  # TODO: Choose head
                "tail": "coffee",  # TODO: Choose tail
        }


def start(game_state: typing.Dict):
        """start is called when your Battlesnake begins a game"""
        print("GAME START")


def end(game_state: typing.Dict):
        """end is called when your Battlesnake finishes a game"""
        print("GAME OVER\n")


def is_cell_occupied(x: int, y: int, game_state: typing.Dict) -> bool:
        """Check if a cell is occupied by a hazard, your snake, or enemy snakes."""
        board = game_state['board']
        # Check hazards
        if any(cell['x'] == x and cell['y'] == y for cell in board['hazards']):
                return True
        
        # Check for all snakes (including your own)
        for snake in board['snakes']:
                for segment in snake['body']:
                        if segment['x'] == x and segment['y'] == y and not(segment == snake['body'][-1]):
                                return True
                          
        # Avoid head-to-head
        for snake in board['snakes']:
            snake_head = snake['body'][0]
            #print(snake['length'], game_state['you']['length'])
            if not (snake['id'] == game_state['you']['id'] and len(snake['body']) >= len(game_state['you']['body'])):
                if (snake_head['x'] - 1, snake_head['y']) == (x, y) or (snake_head['x'] + 1, snake_head['y']) == (x, y) or (snake_head['x'], snake_head['y'] + 1) == (x, y) or (snake_head['x'], snake_head['y'] - 1) == (x, y):
                  return True
        
        return False
    
def move_towards_food_x(snake_pos, food_pos):
    dx = food_pos["x"] - snake_pos["x"]
    if dx > 0 :
        return "right"
    else:
        return "left"
              
def move_towards_food_y(snake_pos, food_pos):
    dy = food_pos["y"] - snake_pos["y"]
    if dy < 0 :
        return "down"
    else:
        return "up"
  
def calculate_distance_to_food(my_head, food_position):
    x_distance = abs(my_head['x'] - food_position['x'])
    y_distance = abs(my_head['y'] - food_position['y'])
    return x_distance + y_distance

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

        is_move_safe = {"up": True, "down": True, "left": True, "right": True}

        my_head = game_state["you"]["body"][0]  # Coordinates of your head

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

    
        # Don't hit other snakes and own body
        for move, isSafe in is_move_safe.items():
                if isSafe:
                        if move == "up":
                                if is_cell_occupied(my_head['x'], my_head['y'] + 1, game_state):
                                        is_move_safe['up'] = False
                        elif move == "down":
                                if is_cell_occupied(my_head['x'], my_head['y'] - 1, game_state):
                                        is_move_safe['down'] = False
                        elif move == "left":
                                if is_cell_occupied(my_head['x'] - 1, my_head['y'], game_state):
                                        is_move_safe['left'] = False
                        elif move == "right":
                                if is_cell_occupied(my_head['x'] + 1, my_head['y'], game_state):
                                        is_move_safe['right'] = False
        
        
        # Are there any safe moves left?
        safe_moves = []
        for move, isSafe in is_move_safe.items():
                if isSafe:
                        safe_moves.append(move)

        if len(safe_moves) == 0:
                print(f"MOVE {game_state['turn']}: No safe moves detected! Moving up :(")
                return {"move": "up"}


        # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
        food = game_state['board']['food']
        
        smallest_distance = 10000
        correct_food = None
        for food_item in food:
            distance = calculate_distance_to_food(my_head, food_item)
            if distance < smallest_distance:
                smallest_distance = distance
                correct_food = food_item

        x_direction = move_towards_food_x(my_head, correct_food)
        y_direction = move_towards_food_y(my_head, correct_food)
        if is_move_safe[x_direction]:
            next_move = x_direction
        elif is_move_safe[y_direction]:
            next_move = y_direction
        else:
            next_move = random.choice(safe_moves)

        print(f"MOVE {game_state['turn']}: {next_move}")
        return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
        from server import run_server

        run_server({"info": info, "start": start, "move": move, "end": end})