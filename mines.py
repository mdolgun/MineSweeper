import random

class Cell:
    def __init__(self):
        self.value = 0
        self.state = 0

class GameExit(Exception): pass
class GameWon(GameExit): pass
class GameLost(GameExit): pass

class Game:
    def init_board(self,rows,cols,n_mines):
        self.rows = rows
        self.cols = cols
        self.n_mines = n_mines
        self.n_inactive = rows*cols
        self.board = [ [Cell() for _ in range(cols)] for _ in range(rows) ]
        for pos in random.sample(range(rows*cols), n_mines):
            i = pos // rows
            j = pos % rows
            self.board[i][j].value = 9
            for ii in range(max(i-1,0),min(i+2,rows)):
                for jj in range(max(j-1,0),min(j+2,cols)):
                    if self.board[ii][jj].value != 9:
                        self.board[ii][jj].value += 1

    def select(self,i,j):
        cell = self.board[i][j]
        if cell.state == 1: # already open
            return

        if cell.value == 9: # mine exploded!
            cell.state = 3
            self.update(i,j,cell) 
            raise GameLost()

        if cell.value == 0: # no mines around, then recurively open all neighbouring cells
            todo = [(i,j)]
            while True:
                try:
                    i,j = todo.pop()
                except IndexError:
                    break
                for ii in range(max(i-1,0),min(i+2,self.rows)):
                    for jj in range(max(j-1,0),min(j+2,self.cols)):
                        scell = self.board[ii][jj]
                        if scell.state==1:
                            continue                
                        scell.state = 1
                        self.update(ii,jj,scell)
                        self.n_inactive -= 1
                        if scell.value == 0:
                            todo.append((ii,jj))
        else: # open the cell and display the mine count
            cell.state = 1
            self.update(i,j,cell)
            self.n_inactive -= 1
        if self.n_inactive == self.n_mines: # if all but mine cells opened, then you won!
            raise GameWon()

    def mark(self,i,j): # flag/unflag a cell for mines
        cell = self.board[i][j]
        if cell.state == 0: # mark a closed cell
            cell.state = 2
            self.update(i,j,cell)
        elif cell.state == 2: # unmark a flagged cell
            cell.state = 0
            self.update(i,j,cell)

    def show_board(self): # open mines and wrong-flagged cells
        for i,row in enumerate(self.board):
            for j,column in enumerate(row):
                cell = self.board[i][j]
                if cell.value == 9 and cell.state == 0: # open all mines
                    cell.state = 1
                    self.update(i,j,cell)
                elif cell.value != 9 and cell.state == 2: # mark wrong-flagged cells
                    cell.state = 3
                    self.update(i,j,cell)
