from tkinter import *
from tkinter import ttk
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
        self.game.rules()
        self.game.update()
        self.update_buttons()

        if self.game.generate_next: self.after(300, self.simulate_game)

    def stop(self):
        self.game.generate_next = False
        
    def reset(self, size):
        self.size = size
        self.game.reset(size)
        self.make_frame()

    def update_buttons(self):
        for row in range(len(self.buttons)):
            for col in range(len(self.buttons)):
                if self.game.board[row][col].is_alive(): self.buttons[row][col].config(bg = "white")
                else: self.buttons[row][col].config(bg = "black")


class GameView(Tk):

    def __init__(self):
        super().__init__()
        self.title("Game of Life")

        self.game = GameFrame(self, 10) 
        self.game.grid(row = 1, column = 0, columnspan = 3, padx = 20, pady = 20)
        
        self.start_button = Button(self, text = "Start", command = self.start)
        self.start_button.grid(row = 0, column = 0, sticky = "we")
        self.next_button = Button(self, text = "Next", command = self.next)
        self.next_button.grid(row = 0, column = 1, sticky = "we")
        self.stop_button = Button(self, text = "Stop", state = "disabled", command = self.stop)
        self.stop_button.grid(row = 0, column = 2, sticky = "we")

        self.shapes = ttk.Combobox(self, postcommand = self.change)
        self.shapes.grid(row = 2, column = 0, sticky = "we", columnspan = 2)
        self.load_button = Button(self, text = "Go", command = self.load_shape)
        self.load_button.grid(row = 2, column = 2, sticky = "we")
        
        self.entry = Entry(self, textvariable = StringVar())
        self.entry.grid(row = 3, column = 0, sticky = "we", columnspan = 2)
        self.save_button = Button(self, text = "Save", command = self.save)
        self.save_button.grid(row = 3, column = 2, sticky = "we")

        self.spinbox = Spinbox(self, from_ = 10, to = 15, width = 5)
        self.spinbox.grid(row = 4, column = 0, sticky = "we", columnspan = 2)
        self.reset_button = Button(self, text = "Reset", command = self.reset)
        self.reset_button.grid(row = 4, column = 2, sticky = "we")

    def start(self):
        self.game.game.generate_next = True
        self.disable_buttons()
        self.game.simulate_game()

    def next(self):
        self.game.game.generate_next = False
        self.game.simulate_game()
    
    def stop(self):
        self.enable_buttons()
        self.game.stop()

    def reset_size(self, size):
        self.game.grid_forget()
        self.game = GameFrame(self, size)
        self.game.grid(row = 1, column = 0, columnspan = 3, padx = 20, pady = 20)

    def reset(self):
        size = int(self.spinbox.get())
        self.reset_size(size)

    def disable_buttons(self):
        self.stop_button.config(state = "normal")
        self.start_button.config(state = "disabled")
        self.next_button.config(state = "disabled")

    def enable_buttons(self):
        self.stop_button.config(state = "disabled")
        self.start_button.config(state = "normal")
        self.next_button.config(state = "normal")

    def change(self):
        values = []
        
        with open("shapes.json", "r") as file:
            data = json.load(file)
            for shape in data: values.append(shape)
            file.close()
        self.shapes["values"] = values

    def load_shape(self):
        shape = str(self.shapes.get())

        with open ("shapes.json", "r") as file:
            data = json.load(file)
            file.close()

        self.reset_size(len(data[shape]))
        self.game.game.states = data[shape]
        self.next()

    def save(self):
        name = str(self.entry.get())
        self.game.game.save(name)