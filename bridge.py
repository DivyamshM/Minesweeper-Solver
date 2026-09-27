import ctypes
import numpy as np

# 1. Define the Python equivalent of your C++ possibleMoves struct
class PossibleMoves(ctypes.Structure):
    _fields_ = [
        ("cellrow", ctypes.c_int),
        ("cellcol", ctypes.c_int),
        ("flag", ctypes.c_int)
    ]

# 2. Load the compiled library (Change to solver.dll if on Windows)
solver_lib = ctypes.CDLL('./libsolver.so')

# 3. Define the argument types for safety
solver_lib.get_next_moves_c.argtypes = [
    np.ctypeslib.ndpointer(dtype=np.int32, ndim=1, flags='C_CONTIGUOUS'), # flat_grid
    ctypes.c_int,  # rows
    ctypes.c_int,  # cols
    ctypes.c_int,  # totMines
    ctypes.c_int,  # curMines
    ctypes.POINTER(ctypes.c_bool),  # isValidFlag
    ctypes.POINTER(ctypes.c_bool),  # isBoardStart
    ctypes.POINTER(PossibleMoves),  # out_moves
    ctypes.c_int   # max_out_size
]
solver_lib.get_next_moves_c.restype = ctypes.c_int

def get_moves_from_cpp(grid_2d: np.ndarray, tot_mines: int, cur_mines: int, is_valid: bool, is_start: bool):
    rows, cols = grid_2d.shape
    flat_grid = grid_2d.astype(np.int32).flatten()
    
    # Create C-compatible boolean pointers
    c_is_valid = ctypes.c_bool(is_valid)
    c_is_start = ctypes.c_bool(is_start)
    
    # Allocate a buffer to hold up to 100 moves
    max_moves = 100
    move_buffer = (PossibleMoves * max_moves)()
    
    # Call the C++ function
    num_moves = solver_lib.get_next_moves_c(
        flat_grid, rows, cols, tot_mines, cur_mines,
        ctypes.byref(c_is_valid), ctypes.byref(c_is_start),
        move_buffer, max_moves
    )
    
    # Extract the results back into a clean Python list
    results = []
    for i in range(num_moves):
        results.append({
            'row': move_buffer[i].cellrow,
            'col': move_buffer[i].cellcol,
            'action': 'FLAG' if move_buffer[i].flag == 1 else 'OPEN'
        })
        
    return results, c_is_valid.value, c_is_start.value

# --- QUICK TEST ---
if __name__ == "__main__":
    # Simulate an empty 9x9 beginner board (-2 means unopened)
    test_board = np.full((9, 9), -2, dtype=np.int32)
    
    moves, is_valid, is_start = get_moves_from_cpp(test_board, 10, 0, True, True)
    
    print(f"Board Valid: {is_valid} | Is Start: {is_start}")
    for m in moves:
        print(f"Move: {m}")