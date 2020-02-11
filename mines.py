import random, enum

class CellValue(enum.IntEnum):
    Empty = 0
    Mine = 9

class CellState(enum.IntEnum):
    Closed = 0
    Open = 1
    Marked = 2
    WrongMarked = 3


class Cell:
    def __init__(self):
        self.value = CellValue.Empty
        self.state = CellState.Closed

class GameExit(Exception): pass
class GameWon(GameExit): pass
class GameLost(GameExit): pass

class Game:
    def init_board(self,n_rows,n_cols,n_mines):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_mines = n_mines
        self.n_inactive = n_rows*n_cols
        self.board = [ [Cell() for _ in range(n_cols)] for _ in range(n_rows) ]
        for pos in random.sample(range(n_rows*n_cols), n_mines):
            i = pos // n_rows
            j = pos % n_rows
            self.board[i][j].value = CellValue.Mine
            for ii in range(max(i-1,0),min(i+2,n_rows)):
                for jj in range(max(j-1,0),min(j+2,n_cols)):
                    if self.board[ii][jj].value != 9:
                        self.board[ii][jj].value += 1

    def select(self,i,j):
        cell = self.board[i][j]
        if cell.state == CellState.Open: # already open
            return

        if cell.value == CellValue.Mine: # mine exploded!
            cell.state = CellState.WrongMarked
            self.update(i,j,cell) 
            raise GameLost()

        if cell.value == 0: # no mines around, then recurively open all neighbouring cells
            todo = [(i,j)]
            while True:
                try:
                    i,j = todo.pop()
                except IndexError:
                    break
                for ii in range(max(i-1,0),min(i+2,self.n_rows)):
                    for jj in range(max(j-1,0),min(j+2,self.n_cols)):
                        scell = self.board[ii][jj]
                        if scell.state == CellState.Open:
                            continue
                        scell.state = CellState.Open
                        self.update(ii,jj,scell)
                        self.n_inactive -= 1
                        if scell.value == CellValue.Empty:
                            todo.append((ii,jj))
        else: # open the cell and display the mine count
            cell.state = CellState.Open
            self.update(i,j,cell)
            self.n_inactive -= 1
        if self.n_inactive == self.n_mines: # if all but mine cells opened, then you won!
            raise GameWon()

    def mark(self,i,j): # flag/unflag a cell for mines
        cell = self.board[i][j]
        if cell.state == CellState.Closed: # mark a closed cell
            cell.state = CellState.Marked
            self.update(i,j,cell)
        elif cell.state == CellState.Marked: # unmark a flagged cell
            cell.state = CellState.Closed
            self.update(i,j,cell)

    def show_board(self): # open mines and wrong-flagged cells
        for i,row in enumerate(self.board):
            for j,column in enumerate(row):
                cell = self.board[i][j]
                if cell.value == CellValue.Mine and cell.state == CellState.Closed: # open all mines
                    cell.state = CellState.Open
                    self.update(i,j,cell)
                elif cell.value != CellValue.Mine and cell.state == CellState.Marked: # mark wrong-flagged cells
                    cell.state = CellState.WrongMarked
                    self.update(i,j,cell)
