import random
from settings import *

def create_initial_map():
    map_colors = [[(random.randint(100, 255), 0, 0) for _ in range(CHUNKS_HORIZONTAL)] for _ in range(CHUNKS_VERTICAL)]
    game_map = []
    for y in range(CHUNKS_VERTICAL * CHUNK_SIZE):
        row = []
        for x in range(CHUNKS_HORIZONTAL * CHUNK_SIZE):
            chunk_x = x // CHUNK_SIZE
            chunk_y = y // CHUNK_SIZE
            row.append(map_colors[chunk_y][chunk_x])
        game_map.append(row)
    return game_map

def expand_map(game_map, direction):
    if direction == 'right':
        for row in game_map:
            new_color = (random.randint(100, 255), 0, 0)
            row.extend([new_color] * CHUNK_SIZE)
    elif direction == 'left':
        for row in game_map:
            new_color = (random.randint(100, 255), 0, 0)
            row[0:0] = [new_color] * CHUNK_SIZE
    elif direction == 'up':
        new_row = [(random.randint(100, 255), 0, 0) for _ in range(len(game_map[0]))]
        for _ in range(CHUNK_SIZE):
            game_map.insert(0, new_row[:])
    elif direction == 'down':
        new_row = [(random.randint(100, 255), 0, 0) for _ in range(len(game_map[0]))]
        for _ in range(CHUNK_SIZE):
            game_map.append(new_row[:])
