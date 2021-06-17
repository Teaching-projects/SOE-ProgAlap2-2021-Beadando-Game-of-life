import json

class Cell:

    def __init__(self):
        self.state = "dead"

    def set_dead(self):
        self.state = "dead"
        
    def set_alive(self):
        self.state = "alive"

    def is_alive(self) -> bool:
        return self.state == "alive"


class Board:

    def __init__(self, size):
        self.size = size
        self.board = [[Cell() for cell in range(self.size)] for cell in range(self.size)]
        self.states = [[None for state in range(self.size)] for state in range(self.size)]
        self.generate_next = True

    def rules(self):

        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col].is_alive():
                    if self.neighbors(row, col) == 2 or self.neighbors(row, col) == 3: self.states[row][col] = "alive"
                    # tuleli, ha ket vagy harom szomszedja van
                    else: self.states[row][col] = "dead"
                    # elpusztul, ha kettonel kevesebb vagy haromnal tobb szomszedja van 
                else:
                    if self.neighbors(row, col) == 3: self.states[row][col] = "alive"
                    # uj szuletik, ha kornyezeteben pontosan 3 szomszedja van

    def neighbors(self, row, col):

        neighbors = 0
        for i in range(max(0, row-1), min(len(self.board)-1, row+1)+1):
            for j in range(max(0, col-1), min(len(self.board)-1, col+1)+1):
                if i == row and j == col: continue
                if self.board[i][j].is_alive(): neighbors += 1
        return neighbors

    def update(self):

        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.states[row][col] == "alive": self.board[row][col].set_alive()
                if self.states[row][col] == "dead": self.board[row][col].set_dead()

    def reset(self):
        
        self.board = [[Cell() for cell in range(self.size)] for cell in range(self.size)]
        self.states = [[None for state in range(self.size)] for state in range(self.size)]

    def save(self, filename):
        board_states = []

        for i in range(len(self.board)):
            board_states.append([])
            for j in range(len(self.board)):
                board_states[-1].append(self.board[i][j].state)

        with open("shapes.json", "r") as file:
            data = json.load(file)
            data[filename] = board_states
            
        with open("shapes.json", "w") as file:
            data[filename] = board_states
            json.dump(data, file)
            file.close