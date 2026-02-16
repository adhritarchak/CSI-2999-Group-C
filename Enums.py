from enum import Enum, auto

class GameStages(Enum):
    StartScreen = auto()
    MainMenu = auto()
    CharSelect = auto()
    Playing = auto()
    BetweenRounds = auto()
    PostMatch = auto()

class CardTypes(Enum):
    Typeless = auto()
    Buff = auto()
    Debuff = auto()
    Effect = auto()
    Power = auto()
    Misc = auto()

# These constants are used to index into the position and velocity tuples for the ball and paddles
X = 0
Y = 1
HEIGHT = 2

# These constants are used to reference the sides of the screen for the ball or paddles
TOP = 0
BOTTOM = 1
LEFT = 2
RIGHT = 3