import cv2
import os

IMAGE_PATH = 'screenshot.png'
SAVE_DIR = 'templates'
# Make sure to set this to whatever CELL_SIZE worked for you before!
CELL_SIZE = 20

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

img = cv2.imread(IMAGE_PATH)
if img is None:
    print(f"Error: Could not load {IMAGE_PATH}")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
clone = img.copy()

board_origin = None
selected_cell = None

def mouse_click(event, x, y, flags, param):
    global board_origin, clone, selected_cell
    
    # 1. Set Anchor
    if event == cv2.EVENT_LBUTTONDOWN and board_origin is None:
        board_origin = (x, y)
        print(f"Anchor set at {board_origin}")
        for r in range(16):
            for c in range(30):
                cx = board_origin[0] + (c * CELL_SIZE)
                cy = board_origin[1] + (r * CELL_SIZE)
                cv2.rectangle(clone, (cx, cy), (cx + CELL_SIZE, cy + CELL_SIZE), (0, 255, 0), 1)
        cv2.imshow("Extractor", clone)
        print("Grid aligned. Now click any cell, then type the label directly on your keyboard.")

    # 2. Select Cell
    elif event == cv2.EVENT_LBUTTONDOWN and board_origin is not None:
        col = (x - board_origin[0]) // CELL_SIZE
        row = (y - board_origin[1]) // CELL_SIZE
        
        start_x = board_origin[0] + (col * CELL_SIZE)
        start_y = board_origin[1] + (row * CELL_SIZE)
        
        selected_cell = gray[start_y:start_y+CELL_SIZE, start_x:start_x+CELL_SIZE]
        
        # Draw a red box around the selected cell
        display_img = clone.copy()
        cv2.rectangle(display_img, (start_x, start_y), (start_x + CELL_SIZE, start_y + CELL_SIZE), (0, 0, 255), 2)
        cv2.imshow("Extractor", display_img)
        print("Cell highlighted. Press 0-8, 'u', or 'f' to save it.")

cv2.imshow("Extractor", clone)
cv2.setMouseCallback("Extractor", mouse_click)

print("1. Click top-left pixel to set anchor.")
print("2. Press 'q' to quit.")

# Main loop captures keyboard input natively
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
        
    # If a cell is highlighted and a valid key is pressed
    if selected_cell is not None:
        char = chr(key).lower()
        if char in '012345678':
            cv2.imwrite(os.path.join(SAVE_DIR, f"{char}.png"), selected_cell)
            print(f"Saved {char}.png")
            selected_cell = None
        elif char == 'u':
            cv2.imwrite(os.path.join(SAVE_DIR, "unopened.png"), selected_cell)
            print("Saved unopened.png")
            selected_cell = None
        elif char == 'f':
            cv2.imwrite(os.path.join(SAVE_DIR, "flag.png"), selected_cell)
            print("Saved flag.png")
            selected_cell = None

cv2.destroyAllWindows()