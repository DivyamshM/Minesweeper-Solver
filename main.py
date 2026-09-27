import time
import pyautogui
import numpy as np
from vision import VisionAgent
from bridge import get_moves_from_cpp

def play_game():
    vision = VisionAgent(cell_size=20) 
    pyautogui.PAUSE = 0.05
    is_valid = True
    is_start = True
    
    # 1. Identify Board and Dimensions once at startup
    screen = vision.capture_screen()
    start_x, start_y, rows, cols = vision.find_board(screen)
    print(f"Board detected! Dimensions: {rows} rows x {cols} cols.")
    
    total_mines = 99 
    
    while True:
        screen = vision.capture_screen()
        current_mines = 0 
        grid_2d = vision.parse_grid(screen, start_x, start_y, rows, cols)
        
        moves, is_valid, is_start = get_moves_from_cpp(
            grid_2d, total_mines, current_mines, is_valid, is_start
        )
        
        if not is_valid:
            print("Invalid state. Stopping.")
            break
            
        # --- THE HUMAN HANDOFF TRIGGER ---
        if not moves or (len(moves) == 1 and moves[0]['row'] >= rows):
            print("Solver stuck! Pausing for human assistance...")
            print("Make a guess. The bot will resume when the board changes.")
            
            # Enter a waiting loop to poll the screen
            while True:
                time.sleep(0.5)
                wait_screen = vision.capture_screen()
                wait_grid = vision.parse_grid(wait_screen, start_x, start_y, rows, cols)
                
                # If the human clicked something, the grids will no longer be identical
                if not np.array_equal(grid_2d, wait_grid):
                    print("Human move detected! Taking back control...")
                    break 
            continue 
            
        # Execute Clicks
        for move in moves:
            r, c = move['row'], move['col']
            
            # FIXED: Hard safety check to completely prevent FailSafe exceptions
            if r < 0 or c < 0 or r >= rows or c >= cols:
                print(f"Ignored invalid coordinate from solver: Row {r}, Col {c}")
                continue
                
            click_x = start_x + (c * vision.cell_size) + (vision.cell_size // 2)
            click_y = start_y + (r * vision.cell_size) + (vision.cell_size // 2)
            
            if move['action'] == 'OPEN':
                pyautogui.click(click_x, click_y, button='left')
            elif move['action'] == 'FLAG':
                pyautogui.click(click_x, click_y, button='right')
                
        time.sleep(0.1)

if __name__ == "__main__":
    print("Starting bot in 5 seconds. Switch to the Minesweeper Window!")
    time.sleep(5)
    play_game()