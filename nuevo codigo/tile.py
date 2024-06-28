# tile.py

class Tile:
    def __init__(self, surface, walkable=True):
        self.surface = surface
        self.walkable = walkable

    def __repr__(self):
        return f"Tile(walkable={self.walkable})"
