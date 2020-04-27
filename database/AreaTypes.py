from enum import Enum

class AreaTypes(Enum):
    TOWN = 1
    WILDERNESS = 2
    DUNGEON = 3

print(type(AreaTypes.TOWN))