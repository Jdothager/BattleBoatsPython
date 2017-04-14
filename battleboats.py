from tkinter import Tk, Frame, Label, Button, Menu
from random import randrange
from sys import exit


class MyGUI:
    def __init__(self, master):
        self.master = master
        master.title('Battleship')
        # variables
        self.turn = ''
        self.difficulty = 'easy'
        self.top_squares_list = []
        self.top_button_list = []
        self.bottom_squares_list = []
        self.bottom_button_list = []
        self.top_spacer = Label(self.master, text=' ', height=1)
        self.middle_spacer = Label(self.master, text=' ', height=2)
        self.center_window()
        self.init_menu()
        self.create_buttons()
        self.reset()

    def init_menu(self):
        """ setup the menus"""
        bar_menu = Menu(self.master)
        self.master.config(menu=bar_menu)
        # add a file button to the menu
        file_menu = Menu(bar_menu, tearoff=0)
        file_menu.add_command(label='Reset', command=self.reset)
        file_menu.add_command(label='Exit', command=exit)
        # set all menus to the top bar menu
        bar_menu.add_cascade(label='File', menu=file_menu)

    def create_buttons(self):
        self.master.grid_columnconfigure(index=0, pad=75)
        self.top_spacer.grid(column=0, row=0, columnspan=11)
        # top button layout
        col = 0
        row = 1
        index = 0
        for i in range(10):  # row
            for j in range(10):  # column
                self.top_squares_list.append([0, False])
                self.top_button_list.append(Button(self.master, width=2, height=1, bg='blue',
                                                   command=lambda x=index: self.button_action(x)))
                if col == 0:
                    self.top_button_list[index].grid(column=col, row=row, sticky='e')
                else:
                    self.top_button_list[index].grid(column=col, row=row)
                col += 1
                index += 1
            col = 0
            row += 1
        # middle spacer layout
        row += 1
        self.middle_spacer.grid(column=0, row=row, columnspan=11)
        # bottom button layout
        row += 1
        col = 0
        index = 0
        for i in range(10):  # row
            for j in range(10):  # column
                self.bottom_squares_list.append([0, False])
                self.bottom_button_list.append(Button(self.master, width=2, height=1, bg='blue'))
                if col == 0:
                    self.bottom_button_list[index].grid(column=col, row=row, sticky='e')
                else:
                    self.bottom_button_list[index].grid(column=col, row=row)
                col += 1
                index += 1
            col = 0
            row += 1

    def button_action(self, index):
        if self.turn == 'player' and not self.game_is_won() and not self.top_squares_list[index][1]:
            if self.top_squares_list[index][0] == 0:
                self.top_squares_list[index] = [3, True]
                self.top_button_list[index].config(bg='white')
                self.turn = 'comp'
                self.comp_turn()
            else:
                self.top_squares_list[index] = [2, True]
                self.top_button_list[index].config(bg='red')
                self.turn = 'comp'
                self.comp_turn()

    def center_window(self):
        """ set the size of the window and center it"""
        width = 400
        height = 600
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - width) / 2
        y = (screen_height - height) / 2
        self.master.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def deploy_ships(self):
        fleet = [5, 4, 3, 3, 2]
        # top
        for ship in fleet:
            thinking = True
            while thinking:
                col = randrange(10)
                row = randrange(10)
                direction = randrange(4)
                if direction == 0:  # up
                    if row - ship < 0:
                        continue
                    elif self.open_spots((col, row), direction, ship, 'top'):
                        for i in range(ship):
                            index = (row * 10) + col
                            self.top_squares_list[index][-2] = 1
                            row -= 1
                        thinking = False
                if direction == 1:  # right
                    if col + ship > 10:
                        continue
                    elif self.open_spots((col, row), direction, ship, 'top'):
                        for i in range(ship):
                            index = (row * 10) + col
                            self.top_squares_list[index][-2] = 1
                            col += 1
                        thinking = False
                if direction == 2:  # down
                    if row + ship > 10:
                        continue
                    elif self.open_spots((col, row), direction, ship, 'top'):
                        for i in range(ship):
                            index = (row * 10) + col
                            self.top_squares_list[index][-2] = 1
                            row += 1
                        thinking = False
                if direction == 3:  # left
                    if col - ship < 0:
                        continue
                    elif self.open_spots((col, row), direction, ship, 'top'):
                        for i in range(ship):
                            index = (row * 10) + col
                            self.top_squares_list[index][-2] = 1
                            col -= 1
                        thinking = False
        # bottom
        for ship in fleet:
            thinking = True
            while thinking:
                col = randrange(10)
                row = randrange(10)
                direction = randrange(4)
                if direction == 0:  # up
                    if row - ship < 0:
                        continue
                    elif self.open_spots((col, row), direction, ship, 'bottom'):
                            for i in range(ship):
                                index = (row * 10) + col
                                self.bottom_squares_list[index][-2] = 1
                                self.bottom_button_list[index].config(bg='grey')
                                row -= 1
                            thinking = False
                elif direction == 1:  # right
                    if col + ship > 10:
                        continue
                    elif self.open_spots((col, row), direction, ship, 'bottom'):
                            for i in range(ship):
                                index = (row * 10) + col
                                self.bottom_squares_list[index][-2] = 1
                                self.bottom_button_list[index].config(bg='grey')
                                col += 1
                            thinking = False
                elif direction == 2:  # down
                    if row + ship > 10:
                        continue
                    elif self.open_spots((col, row), direction, ship, 'bottom'):
                            for i in range(ship):
                                index = (row * 10) + col
                                self.bottom_squares_list[index][-2] = 1
                                self.bottom_button_list[index].config(bg='grey')
                                row += 1
                            thinking = False
                elif direction == 3:  # left
                    if col - ship < 0:
                        continue
                    elif self.open_spots((col, row), direction, ship, 'bottom'):
                        for i in range(ship):
                            index = (row * 10) + col
                            self.bottom_squares_list[index][-2] = 1
                            self.bottom_button_list[index].config(bg='grey')
                            col -= 1
                        thinking = False

    def open_spots(self, col_row_pos, direction, ship, frame):
        """ This is a helper to self.deploy_ships, checks if it's clear to assign a ship without overlapping
            returns a bool """
        # determine which frame we working with, top or bottom
        if frame == 'bottom':
            frame = self.bottom_squares_list
        else:
            frame = self.top_squares_list
        # check if any of the squares are already set to state 1
        col = col_row_pos[0]
        row = col_row_pos[1]
        for i in range(ship):
            index = (row * 10) + col
            if frame[index][0] == 1:
                return False
            if direction == 0:
                row -= 1
            if direction == 1:
                col += 1
            if direction == 2:
                row += 1
            if direction == 3:
                col -= 1
        return True

    def reset(self):
        for index in range(100):
            self.top_button_list[index].config(bg='blue')
            self.bottom_button_list[index].config(bg='blue')
            self.top_squares_list[index] = [0, False]
            self.bottom_squares_list[index] = [0, False]
        self.deploy_ships()
        order = randrange(2)
        if order == 1:
            self.turn = 'player'
        else:
            self.turn = 'comp'
            self.comp_turn()

    def game_is_won(self):
        top_count = 0
        bottom_count = 0
        for index in range(100):
            if self.top_squares_list[index][0] == 1:
                top_count += 1
            if self.bottom_squares_list[index][0] == 1:
                bottom_count += 1
        if top_count == 0 or bottom_count == 0:
            return True
        return False

    def comp_turn(self):
        if self.turn == 'comp' and not self.game_is_won():
            thinking = True
            while thinking:
                if self.difficulty == 'easy':
                    target = randrange(100)
                    if not self.bottom_squares_list[target][1]:
                        if self.bottom_squares_list[target][0] == 0:
                            self.bottom_squares_list[target] = [3, True]
                            self.bottom_button_list[target].config(bg='white')
                            thinking = False
                            self.turn = 'player'
                        else:
                            self.bottom_squares_list[target] = [2, True]
                            self.bottom_button_list[target].config(bg='red')
                            thinking = False
                            self.turn = 'player'


def main():
    root = Tk()
    my_gui = MyGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
