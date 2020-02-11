import conio, sys
from mines import *

amap = { # attribute map for tiles
    0: conio.yellow,
    1: conio.bright+conio.blue,
    2: conio.bright+conio.green,
    3: conio.bright+conio.magenta,
    4: conio.bright+conio.cyan,
    5: conio.blue,
    6: conio.magenta,
    7: conio.green,
    8: conio.yellow,
    9: conio.bright+conio.red,
}
cmap = { # character map for tiles
    0: '.', # empty
    1: '1',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '*'  # mine
}

class ConGame(Game):
    def __init__(self,n_rows,n_cols,n_mines):
        self.init_board(n_rows,n_cols,n_mines)

    def update(self,i,j,cell):
        if cell.state == CellState.Open:
            conio.write(i+1, j+1, cmap[cell.value], fg=amap[cell.value])
        elif cell.state == CellState.Marked:
            conio.write(i+1, j+1, '!', fg=conio.bright+conio.red)
        elif cell.state == CellState.WrongMarked:
            if cell.value == CellValue.Mine:
                conio.write(i+1, j+1, '*', fg=conio.bright+conio.red, reverse=True)
            else:
                conio.write(i+1, j+1, '!', fg=conio.bright+conio.red, reverse=True)
        else:
            conio.write(i+1, j+1, '#', fg=conio.white)

    def init_board(self, n_rows, n_cols, n_mines):
        super().init_board(n_rows, n_cols, n_mines)
        conio.clr_scr();
        border = "+" +  '-'*self.n_cols + '+'
        content = '|' + '#'*self.n_cols +'|'
        conio.write(0, 0, text=border)
        for i in range(self.n_rows):
            conio.write(1+i, 0, text=content)
        conio.write(self.n_rows+1, 0, text=border)
        conio.write(self.n_rows+2, 0, text="<arrow keys>:Move <space>:Select m:Mark n:New game q:Quit ", fg=conio.white)

    def play(self):
        with conio.conio(): 
            while True:
                self.init_board(self.n_rows, self.n_cols, self.n_mines)
                curx = 0
                cury = 0
                try:
                    while True:
                        conio.write(cury+1,curx+1)
                        c = conio.getch()
                        if c=='q':
                            conio.write(self.n_rows+2, 0, text="You quit!", fg=conio.white, erase=conio.erase_eol)
                            return
                        elif c == 'left':
                            if curx > 0:
                                curx -= 1
                        elif c == 'right':
                            if curx < self.n_cols-1:
                                curx += 1
                        elif c == 'up':
                            if cury > 0:
                                cury -= 1
                        elif c == 'down':
                            if cury < self.n_rows-1:
                                cury += 1 
                        elif c == ' ':
                            self.select(cury,curx)
                        elif c == 'm':
                            self.mark(cury,curx)
                        elif c == 'n':
                            break
                except GameWon:
                    self.show_board()
                    conio.write(self.n_rows+2, 0, text="You won! Press any key to continue or q to quit", fg=conio.white, erase=conio.erase_eol)
                    if conio.getch()=='q':
                        return;
                except GameLost:
                    self.show_board()
                    conio.write(self.n_rows+2, 0, text="You lost! Press any key to continue or q to quit", fg=conio.white, erase=conio.erase_eol)
                    if conio.getch()=='q':
                        return;

game = ConGame(20,20,40)
game.play()