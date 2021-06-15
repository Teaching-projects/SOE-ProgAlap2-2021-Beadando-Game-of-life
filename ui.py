from tkinter import *
from gameoflife import *


class GameFrame(Frame):

    def __init__(self, parent, size):
        super().__init__(parent)
        self.size = size
        self.buttons = []
        self.game = Board(self.size)
        self.make_frame()

    def make_frame(self):
        self.buttons = []
        
        for row in range(self.size):
            self.buttons.append([])
            for col in range(self.size):
                button = Button(self, width = 2, height = 1, bg = "black", command = lambda row = row, col = col: self.clicked(row, col))
                self.buttons[-1].append(button)
                self.buttons[row][col].grid(row = row, column = col)

    def clicked(self, row, col):
        if self.game.board[row][col].is_alive(): self.game.board[row][col].set_dead()
        else: self.game.board[row][col].set_alive()
        self.update_buttons()

    def simulate_game(self):
        self.game.update()
        self.update_buttons()

        if self.game.generate_next: self.after(300, self.simulate_game)

    def stop(self):
        self.game.generate_next = False
        
    def reset(self):
        self.game.generate_next = True
        self.game.reset()
        self.make_frame()

    def update_buttons(self):
        for row in range(len(self.buttons)):
            for col in range(len(self.buttons)):
                if self.game.board[row][col].is_alive(): self.buttons[row][col].config(bg = "white")
                else: self.buttons[row][col].config(bg = "black")


class GameView(Tk):

    def __init__(self, size):
        super().__init__()
        self.title("Game of Life")

        self.game = GameFrame(self, size) 
        self.game.grid(row = 1, column = 0, columnspan = 3) 

        self.start_button = Button(self, text = "Start", command = self.start)
        self.start_button.grid(row = 0, column = 0, sticky = E)

        self.stop_button = Button(self, text = "Stop", command = self.stop)
        self.stop_button.grid(row = 0, column = 1)

        self.reset_button = Button(self, text = "Reset", state = "normal", command = self.reset)
        self.reset_button.grid(row = 0 , column = 2, sticky = W)

    def start(self):
        self.game.game.generate_next = True
        self.disable_buttons()
        self.game.simulate_game()
    
    def stop(self):
        self.enable_buttons()
        self.game.stop()

    def reset(self):
        self.game.reset()

    def disable_buttons(self):
        self.stop_button.config(state = "normal")
        self.start_button.config(state = "disabled")

    def enable_buttons(self):
        self.stop_button.config(state = "disabled")
        self.start_button.config(state = "normal")