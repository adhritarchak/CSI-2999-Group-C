
import pygame as pg
import random

class Card:
    def __init__(self, name, effect_function):
        self.name = name
        self.effect_function = effect_function

    def activate_card(self):
        self.effect_function()


def arc_strike_effect():
        print("Arc Strike activated!")
        #if player.has_card("arc_strike"):
            #ball.speed_x *= 1.5
            #ball.speed_y *= 1.5
            #player.has_card("arc_strike") = False
        # Implement the effect of Arc Strike here


def bigger_is_better_effect():
        print("Bigger is better activated!")
        #if player.has_card("bigger_is_better"):
            #ball.radius *= 1.5
            #player.has_card("bigger_is_better") = False
        # Implement the effect of Bigger is better here

def bring_it_back_effect():
        print("Bring it back activated!")
        #if player.has_card("bring_it_back"):
            #ball.x, ball.y = player.initial_position()
            #player.has_card("bring_it_back") = False
        # Implement the effect of Bring it back here

def shadow_clone_effect():
        print("Shadow Clone activated!")
        # Implement the effect of Shadow Clone here

def low_impact_effect():
        print("Low impact activated!")
        # Implement the effect of Low impact here

def high_impact_effect():
        print("High impact activated!")
        # Implement the effect of High impact here
def shrink_effect():
        print("Shrink activated!")
        # Implement the effect of Shrink here

cards = [
        Card("Arc Strike", arc_strike_effect), #cards[0]
        Card("Bigger is better", bigger_is_better_effect), #cards[1]
        Card("Bring it back", bring_it_back_effect), #cards[2]
        Card("Shadow Clone", shadow_clone_effect), #cards[3]
        Card("Low impact", low_impact_effect), #cards[4]
        Card("High impact", high_impact_effect), #cards[5]
        Card("Shrink", shrink_effect) #cards[6]
        ]

card_count = 0


def draw_random_card(num = 3):
   selected_cards = random.sample(cards, num)
   global card_count
   print("These are your available cards!")
   for card in selected_cards:
        print(f"Drawn card: {card.name}")
   while card_count == 0:
        card_name_choice = input("Which card would you like: ")
        for card in selected_cards:
            if card.name.lower() == card_name_choice.lower():
                print(f"Selected card: {card.name}")
                card_count += 1
                return card
                break
        else:
            print("That card is not in the deck, please enter another one: ")
    
hand = draw_random_card()
