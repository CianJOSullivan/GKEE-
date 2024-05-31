# GKEE-
 - I dont know why there is a - at the end
 - add all valve logic into the logic.py file


 def draw_valve_buttons():
    # Draw valve control buttons
    x, y = 50, 100
    spacing = 60  # Increased spacing between rows
    

    for row, valve_name in enumerate(locations):
        # Draw valve name with smaller font
        draw_text(valve_name, NAME_FONT, BLACK,  x, y + row * spacing)

        # Draw Green box
        pygame.draw.rect(win, GREEN if selected_states[valve_name] else BLACK, (x + 120, y + row * spacing, 80, 40))

        # Draw cylinder
        pygame.draw.rect(win, GREEN, (x + 220, y + row * spacing, 40, 40))

        # Draw options 1, 2, and 3
        for i in range(3):
            pygame.draw.rect(win, GREEN, (x + 280 + i * 60, y + row * spacing, 40, 40))
            draw_text(str(i + 1), STAT_FONT, BLACK, x + 295 + i * 60, y + row * spacing)