# Base file
import pygame
import json
# # Window Constants
def main():
    # config = {
    #     'Window': {
    #         'Width': 1000,
    #         'Height': 600,
    #         'FPS': 60,
    #         'Caption': "Supreme Pong",
    #         'font': ("timesnewroman", 36)
    #     },
    #     'Table Layout': {
    #         'Table_Margin': 80,
    #         'Table_Border': 5,
    #         'Net_Thickness': 4,
    #         'Midline_Thickness': 3
    #     },
    #     'Paddle Physics': {
    #         'Paddle_Boost': 1.4,
    #         'Paddle_Width': 20,
    #         'Paddle_Height': 80,
    #         'BasePaddleSpeed': 5,
    #         'SmashPaddle1Speed': 1.5,       #BasePaddleSpeed * 0.3
    #         'SmashPaddle2Speed': 1.5,       #BasePaddleSpeed * 0.3
    #         'SmashChargeSpeed': 1.5,
    #         'Smash_start_time': 0,
    #         'Smash1_hold_time': 0,
    #         'Smash1_hit': False,
    #         'Smash1_hit_time': 0,
    #         'Smash1_active': False,
    #         'Smash2_hold_time': 0,
    #         'Smash2_active': False,
    #         'Smash_duration': 3000,
    #         'Smash2_hit': False,
    #         'Smash2_hit_time': 0
    #     },
    #     'Ball Physics': {
    #         'Radius': 10,
    #         'Max_Height': 25,
    #         'Gravity': 0.35,
    #         'BounceSpeedLost': 0.85,
    #         'Max_Speed': 10,
    #         'Bounce_MinZ': 8,
    #         'paddle_hit_boost': 1,
    #         'init_x': 500,      #Width // 2
    #         'init_y': 300,      #Height // 2
    #         'init_height': 0,
    #         'init_vel_x': 1,
    #         'init_vel_y': 0.8,
    #         'init_vel_z': 0
    #     },
    #     'colors': {
    #         'White': (255, 255, 255),
    #         'Black': (0, 0, 0),
    #         'Red Table': (170, 40, 40),
    #         'Light Brown': (200, 170, 130),
    #         'Orange': (255, 165, 0),
    #         'Shadow': (0, 50, 0, 100),
    #         'Paddle 1': (255, 100, 100),
    #         'Paddle 2': (100, 100, 255)
    #         }
    # }
    # with open('config.json', 'w') as c:
    #     json.dump(config, c)
    config: dict = None
    with open('config.json', 'r') as c:
        config = json.load(c)
    print(config)

if __name__ == "__main__":
    main()

