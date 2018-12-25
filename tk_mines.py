import tkinter as tk
from tkinter import messagebox as tkmb
import traceback
from mines import *

class TkGame(Game):
    def lclick(self,e):
        self.select(e.y//self.h, e.x//self.w)

    def rclick(self,e):
        self.mark(e.y//self.h, e.x//self.w)  
        
    def __init__(self,rows,cols,n_mines):
        self.root = tk.Tk()
        # import images
        self.tiles = {x : tk.PhotoImage(file = "20x20/"+str(x)+".png") for x in range(9) }
        self.tiles[9] = tk.PhotoImage(file = "20x20/mine.png")
        for name in ['normal', 'flag', 'wrong', 'explode']:
            self.tiles[name] = tk.PhotoImage(file = "20x20/"+name+".png")
        self.w = self.tiles[0].width()
        self.h = self.tiles[0].height()

        self.canvas = tk.Canvas(self.root, height=self.h*rows, width=self.w*cols, highlightthickness=0)
        self.canvas.pack()

        menubar = tk.Menu(self.root)
        menubar.add_command(label="New", command=lambda: self.init(self.rows,self.cols,self.n_mines))
        menubar.add_command(label="Quit", command=self.root.destroy)
        self.root.config(menu=menubar)

        self.root.title("Mine Sweeper")

        self.root.report_callback_exception = self.report_callback_exception
        self.canvas.bind('<Button-1>', lambda event: self.lclick(event))
        self.canvas.bind('<Button-3>', lambda event: self.rclick(event))

        self.init_board(rows,cols,n_mines)
        
    def init_board(self,rows,cols,n_mines):
        super().init_board(rows,cols,n_mines)
        for i in range(rows):
            for j in range(cols):
                self.canvas.create_image(i*self.w, j*self.h, image=self.tiles['normal'], anchor=tk.NW)


    def update(self,i,j,cell):
        if cell.state == 1:
            self.canvas.create_image(j*self.w, i*self.h, image=self.tiles[cell.value], anchor=tk.NW)
        elif cell.state ==2:
            self.canvas.create_image(j*self.w, i*self.h, image=self.tiles['flag'], anchor=tk.NW)
        elif cell.state == 3:
            if cell.value == 9:
                self.canvas.create_image(j*self.w, i*self.h, image=self.tiles['explode'], anchor=tk.NW)
            else:
                self.canvas.create_image(j*self.w, i*self.h, image=self.tiles['wrong'], anchor=tk.NW)
        else:
            self.canvas.create_image(j*self.w, i*self.h, image=self.tiles['normal'], anchor=tk.NW)


    def report_callback_exception(self, *args):
        if args[0]==GameLost:
            self.show_board()
            tkmb.showinfo("Game Result","You lost!")
        elif args[0]==GameWon:
            self.show_board()
            tkmb.showinfo("Game Result","You won!")
        else:
            err = traceback.format_exception(*args)
            tkmb.showerror('Exception', err)

    def play(self):
        self.root.mainloop()

game = TkGame(20,20,40)
game.play()