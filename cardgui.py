import pygame as pg



def card_ui(screen, font, inventory, player_num, x_offset, y_offset):
    card_width = 80
    card_height = 40
    spacing = 5
    transparency = 200
    
    for i, card in enumerate(inventory.cards):
        x = x_offset + i * (card_width + spacing)
        y = y_offset
        
        # Create card surface
        card_surface = pg.Surface((card_width, card_height), pg.SRCALPHA)
        
        # Determine color based on card status
        if card.is_Passive:
            color = (100, 100, 200, transparency)  # Blue for passive 
        elif card.rounds_left_on_cooldown > 0:
            color = (0, 0, 0, transparency)  # Black for on cooldown
        else:
            color = (200, 50, 50, transparency)  # Red for ready to use
        
        pg.draw.rect(card_surface, color, card_surface.get_rect(), border_radius=5)
        pg.draw.rect(card_surface, (255, 255, 255, 100), card_surface.get_rect(), 2, border_radius=5)
        
        name_text = card.name
        if len(name_text) > 10:
            name_text = name_text[:8] + ".."
        
        small_font = pg.font.SysFont('timesnewroman', 15)
        text_surface = small_font.render(name_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(card_width // 2, card_height // 2 - 5))
        card_surface.blit(text_surface, text_rect)
        
        if not card.is_Passive and card.rounds_left_on_cooldown > 0:
            cooldown_text = small_font.render(f"{card.rounds_left_on_cooldown}", True, (255, 200, 100))
            cooldown_rect = cooldown_text.get_rect(center=(card_width // 2, card_height - 12))
            card_surface.blit(cooldown_text, cooldown_rect)
        
        slot_text = small_font.render(f"[{i+1}]", True, (200, 200, 200))
        slot_rect = slot_text.get_rect(topleft=(2, 2))
        card_surface.blit(slot_text, slot_rect)
        
        screen.blit(card_surface, (x, y))
        
        if player_num == 1:
            key_hint = small_font.render(f"Press {i+1}", True, (255, 255, 255))
            hint_rect = key_hint.get_rect(center=(x + card_width // 2, y + card_height + 8))
            screen.blit(key_hint, hint_rect)
        else:
            keys = ['I', 'O', 'P', 'K', 'L']
            if i < len(keys):
                key_hint = small_font.render(f"Press {keys[i]}", True, (255, 255, 255))
                hint_rect = key_hint.get_rect(center=(x + card_width // 2, y + card_height + 8))
                screen.blit(key_hint, hint_rect)


def card_legend(screen, font):
    legend_x = 10
    legend_y = screen.get_height() - 200
    
    legend_font = pg.font.SysFont('timesnewroman', 10)
    
    # Red box
    pg.draw.rect(screen, (200, 50, 50), (legend_x, legend_y, 12, 12))
    red_text = legend_font.render("= Ready", True, (255, 255, 255))
    screen.blit(red_text, (legend_x + 15, legend_y))
    
    # Black box
    pg.draw.rect(screen, (0, 0, 0), (legend_x, legend_y + 15, 12, 12))
    black_text = legend_font.render("= Cooldown", True, (255, 255, 255))
    screen.blit(black_text, (legend_x + 15, legend_y + 15))
    
    # Blue box
    pg.draw.rect(screen, (100, 100, 200), (legend_x, legend_y + 30, 12, 12))
    blue_text = legend_font.render("= Passive", True, (255, 255, 255))
    screen.blit(blue_text, (legend_x + 15, legend_y + 30))