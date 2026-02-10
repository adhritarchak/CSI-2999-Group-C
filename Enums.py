from enum import Enum

class CardTypes(Enum):
    Typeless = 0
    Buff = 1
    Debuff = 2
    Effect = 3
    Power = 4
    Misc = 5