import cv2
import numpy as np
import mss
import os

class VisionAgent:
    def __init__(self, cell_size=20):
        self.sct = mss.mss()
        self.cell_size = cell_size
        self.templates = {}
        
        template_files = {
            -2: 'unopened.png',
            -1: 'flag.png',
             0: '0.png',
             1: '1.png', 
             2: '2.png', 
             3: '3.png',
             4: '4.png', 
             5: '5.png', 
             6: '6.png',
        }
        
        for val, filename in template_files.items():
            path = os.path.join('templates', filename)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE) 
            
            if img is None:
                print(f"WARNING: Could not find or load {path}")
            else:
                self.templates[val] = img
                
        if -2 not in self.templates:
            raise FileNotFoundError("CRITICAL ERROR: templates/unopened.png is missing! The bot cannot find the board without it.")
            
    def capture_screen(self):
        """Grabs the primary monitor screen."""
        monitor = self.sct.monitors[1]
        screenshot = self.sct.grab(monitor)

        img = np.array(screenshot)
        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        return gray

    def find_board(self, screen_gray):
        """Automatically finds the top-left corner and calculates board dimensions."""
        unopened_template = self.templates[-2] 
        res = cv2.matchTemplate(screen_gray, unopened_template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.95)
        
        if len(loc[0]) == 0:
            raise ValueError("Could not find the Minesweeper board. Is it visible?")
            
        matches = list(zip(*loc[::-1]))
        matches.sort(key=lambda pt: (pt[1], pt[0])) 
        
        start_x, start_y = matches[0]
        
        cols = 0
        while True:
            x = start_x + (cols * self.cell_size)
            if x + self.cell_size > screen_gray.shape[1]: 
                break
                
            cell_img = screen_gray[start_y:start_y+self.cell_size, x:x+self.cell_size]
            if self._classify_cell(cell_img) == -99:
                break
            cols += 1
            
        rows = 0
        while True:
            y = start_y + (rows * self.cell_size)
            if y + self.cell_size > screen_gray.shape[0]: 
                break
                
            cell_img = screen_gray[y:y+self.cell_size, start_x:start_x+self.cell_size]
            if self._classify_cell(cell_img) == -99:
                break
            rows += 1
            
        return start_x, start_y, rows, cols
    
    def parse_grid(self, screen_gray, start_x, start_y, rows, cols):
        """Slices the grid into cells and classifies each one."""
        grid = np.zeros((rows, cols), dtype=np.int32)
        for r in range(rows):
            for c in range(cols):
                x = start_x + (c * self.cell_size)
                y = start_y + (r * self.cell_size)
                cell_img = screen_gray[y:y+self.cell_size, x:x+self.cell_size]
                grid[r][c] = self._classify_cell(cell_img)
        return grid
    
    def _classify_cell(self, cell_img):
        """Compares the cell_img against loaded templates."""
        best_score = -1.0
        best_match_val = -99 

        for val, template in self.templates.items():
            res = cv2.matchTemplate(cell_img, template, cv2.TM_CCOEFF_NORMED)
            score = res[0][0]
            if score > best_score:
                best_score = score
                best_match_val = val
        
        if best_score < 0.85:
            return -99
        
        return best_match_val