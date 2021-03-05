import numpy as np
import time

start = time.time()

class sudoku_puzzle():
    def __init__(self, sudoku):
        self.sudoku = np.copy(sudoku)
        self.num_rows = 9
        self.num_cols = 9
        
    def get_row_cells(self,i):
        if 0 <= i < self.num_rows:
            row_cells = np.array(self.sudoku[i])
            return row_cells
        else:
            raise ValueError("Row index out of bounds!")
    
    def get_col_cells(self,j):
        if 0 <= j < self.num_cols:
            col_cells = np.array([self.sudoku[i][j] for i in range(self.num_rows)])
            to_return = col_cells.reshape(9,1)
            return to_return
        else:
            raise ValueError("Column index out of bounds!")
            
    def get_square_cells(self,row,col):
        square = []
        
        square_x = col // 3
        square_y = row // 3
        
        min_range_x = square_x * 3
        min_range_y = square_y * 3
        
        max_range_x = min_range_x + 3
        max_range_y = min_range_y + 3
        
        for i in range(min_range_y, max_range_y):
            for j in range(min_range_x, max_range_x):
                square.append(self.get_cell(i,j))
                
        square = np.array(square)
        square = square.reshape(3,3)
        
        return square
        
    def get_cell(self,row,col):
        if (0 <= row < self.num_rows) and (0<= col < self.num_cols):
            num = self.sudoku[row][col]
            return num
        else:
            raise ValueError("Index out of bounds!")
    
    def set_cell(self,row,col,value):
        if (0 <= value < 10) and (0 <= row < self.num_rows) and (0<= col < self.num_cols):
            self.sudoku[row][col] = value
        else:
            raise ValueError("Value or index out of bounds!")
            
    def has_valid_start_state(self):  
        for i in range(1,10): 
            #Check rows.
            for row in range(self.num_rows):
                count_row = np.count_nonzero(self.get_row_cells(row) == i)
                if count_row > 1:
                    return False  
                
            #Check columns.   
            for col in range(self.num_cols):
                count_col = np.count_nonzero(self.get_col_cells(col) == i)
                if count_col > 1:
                    return False   
            
            #Check local 3x3 squares.
            #We use the list square_index in order to avoid checking the same squares multiple times.
            square_index = [0,3,7]
            for row in square_index:
                for col in square_index:
                    count_square = np.count_nonzero(self.get_square_cells(row,col) == i)
                    if count_square > 1:
                        return False
            
        return True  
    
    def get_empty_cells(self):
        empty_cells = []
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.get_cell(i,j) == 0:
                    empty_cells.append((i,j))
    
        return empty_cells
    
    def get_remaining_valid_values(self,row,col):
        available_values = [1,2,3,4,5,6,7,8,9]
        valid_values = [1,2,3,4,5,6,7,8,9]
        
        local_row = self.get_row_cells(row)
        local_col = self.get_col_cells(col)
        local_square = self.get_square_cells(row,col)
        
        for i in range(len(available_values)):
            if available_values[i] in local_row:             
                valid_values.remove(available_values[i])
            elif available_values[i] in local_col: 
                valid_values.remove(available_values[i])
            elif available_values[i] in local_square:
                valid_values.remove(available_values[i])   
        return valid_values
    
    def select_MRV(self,empty_cells):
        remaining_values = []
        #empty_cells = self.get_empty_cells()
        for row,col in empty_cells:
                remaining_values.append(self.get_remaining_valid_values(row,col))
         
        avail_sizes = [len(j) for j in remaining_values]
        index = np.argmin(avail_sizes)
        
        return [empty_cells[index],remaining_values[index]]
    
    def solve_sudoku(self):
        empty_cells = self.get_empty_cells()
        
        if empty_cells == []:
            return True
        else:
            pos,candidate_values = self.select_MRV(empty_cells)
            row = pos[0]
            col = pos[1]
        
        for i in candidate_values:                       
            self.set_cell(row,col,i)
            print("Candidate value: ",i," in row: ",row," column: ",col)
            print(self.sudoku)
            solved = self.solve_sudoku()
            if solved:
                return True
            else:
                # Reset the current cell for backtracking
                self.set_cell(row,col,0)
                
        #print("busted")
        #print(self.sudoku)
        return False
                                
    def return_unsolvable_sudoku(self):
        solution = np.full((9,9),-1)
        return solution           
        
    def return_sudoku(self):
        return self.sudoku
            
    def to_print(self):
        print("\n",self.sudoku,"\n")
    
def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    
    puzzle = sudoku_puzzle(sudoku)
    
    if puzzle.has_valid_start_state():
        if puzzle.solve_sudoku():
            return puzzle.return_sudoku()
        else:
            return puzzle.return_unsolvable_sudoku()
    else:
        return puzzle.return_unsolvable_sudoku()



#***********************************************DEBUGGING-CODE*********************************************************#

test_sudoku1 =np.array([
 [0, 8, 0, 4, 3, 0, 0, 0, 0],
 [0, 0, 5, 0, 0, 9, 0, 0, 0],
 [6, 0, 0, 0, 8, 0, 0, 7, 0],
 [0, 0, 0, 0, 9, 0, 0, 0, 3],
 [0, 0, 0, 8, 0, 7, 0, 0, 0],
 [9, 0, 0, 0, 0, 0, 0, 5, 4],
 [0, 6, 0, 0, 0, 0, 0, 0, 5],
 [0, 0, 8, 0, 0, 0, 4, 0, 0],
 [0, 4, 0, 0, 0, 6, 0, 1, 0]])

test_sudoku2 = np.array([
 [0, 8, 5, 0, 1, 3, 0, 0, 9],
 [6, 3, 4, 0, 0, 2, 1, 7, 5,],
 [0, 2, 0, 5, 7, 4, 0, 3, 0,],
 [2, 4, 8, 3, 6, 7, 9, 5, 1,],
 [9, 6, 0, 4, 5, 8, 0, 2, 3,],
 [3, 5, 7, 2, 0, 0, 4, 8, 0,],
 [5, 7, 3, 1, 0, 0, 8, 9, 2,],
 [4, 9, 6, 0, 2, 5, 3, 1, 0,],
 [8, 1, 2, 0, 3, 9, 5, 6, 4]])

hardest_sudoku = np.array([
    [8,0,0,0,0,0,0,0,0],
    [0,0,3,6,0,0,0,0,0],
    [0,7,0,0,9,0,2,0,0],
    [0,5,0,0,0,7,0,0,0],
    [0,0,0,0,4,5,7,0,0],
    [0,0,0,1,0,0,0,3,0],
    [0,0,1,0,0,0,0,6,8],
    [0,0,8,5,0,0,0,1,0],
    [0,9,0,0,0,0,4,0,0]])

k = hardest_sudoku
test_puzzle = sudoku_puzzle(k)
test_puzzle.get_empty_cells()
test_puzzle.to_print()
print("\n",sudoku_solver(k),"\n")

print( "solved in {} seconds".format( time.time() - start ) )