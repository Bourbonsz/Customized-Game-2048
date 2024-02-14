"""Customized Game 2048
Function description:
1. Game size: Customize the game board size with an integer between 2 and 10,
e.g., inputting 3 will create a game grid of size 3x3.
2. Color theme: Choose from six color themes, including Classic, Ocean, Forest, Sunset, Space, Royal, and Lime.
3. Word theme: Select from four default themes, which include Numbers, Emojis, Crypto, Harry Potter,
or create a custom word theme by entering a string of 10 characters separated by English commas.
4. Timer: Input a positive integer to initiate a countdown timer, e.g., entering 60 will start a 60-second countdown;
inputting 0 will start a regular timer. The game ends if the countdown timer reaches zero.
"""
from datetime import datetime, timedelta
from tkinter import Frame, Label, Tk, messagebox, Entry, Button, StringVar, OptionMenu
from PIL import ImageTk, Image
import logic
import constants as c

# Game grid interface
class GameGrid():
    def __init__(self, column: int = None, theme: str = None, word_theme: dict = None, time_limit: int = None):
        if column is None:
            column, theme, word_theme, time_limit = self.get_custom_settings()
        self.init_setting(column, theme)
        self.word_dict = word_theme
        self.time_limit = time_limit
        self.start_time = datetime.now()
        self.data = logic.Matrix2048(column)
        self.root = self.init_root()
        self.t = 0  # To check game over

        self.main()

    def init_setting(self, column, theme):

        # Game grid size
        self.column = column

        # Spacing between grid cells in pixels
        self.space_size = c.GRID_PADDING

        # Size of each grid cell in pixels
        self.cell_size = c.CELL_SIZE

        # Store tkinter.Label objects
        self.emts = []

        # Store game style information such as background color, font color, font size
        self.style = c.THEME_COLORS[theme]

    # Initialize the root window
    def init_root(self):
        column = self.column
        space_size = self.space_size
        cell_size = self.cell_size

        # Initialize the main window
        root = Tk()
        root.title('2048')

        window_w = column * (space_size + cell_size) + space_size
        window_h = window_w + cell_size + space_size * 2
        root.geometry(f'{window_w}x{window_h}')

        # header
        header_h = cell_size + space_size * 2
        header = Frame(root, height=header_h, width=window_w)
        self.init_header(header)

        # game grid
        table = Frame(root, height=window_w, width=window_w)
        self.init_table(table)

        return root

    # Initialize the header
    def init_header(self, master):
        master['bg'] = self.style['page']['bg']
        # Score
        emt_score = Label(master, bd=0)
        emt_score['fg'] = '#707070'
        emt_score['bg'] = self.style['page']['bg']
        emt_score['font'] = ("Verdana", 22, "bold")
        img = Image.new('RGB', (self.cell_size, self.cell_size),
                        self.style['page']['bg'])
        img = ImageTk.PhotoImage(img)
        emt_score.configure(image=img)
        emt_score['image'] = img

        emt_score['text'] = 'Score:' + str(self.data.score)
        emt_score['compound'] = 'center'
        self.emt_score = emt_score
        emt_score.place(x=15, y=15)

        # Timer
        timer_label = Label(master, bd=0)
        timer_label["fg"] = "#707070"
        timer_label["bg"] = self.style["page"]["bg"]
        timer_label["font"] = ("Verdana", 22, "bold")
        timer_label.place(x=15, y=6)
        self.timer_label = timer_label

        master.pack()

    # Initialize the game grid
    def init_table(self, master):
        column = self.column
        cell_size = self.cell_size
        space_size = self.space_size

        master['bg'] = self.style['page']['bg']

        # Create grid elements
        emts = [[0 for x in range(column)] for y in range(column)]
        for row in range(column):
            for col in range(column):
                emt = Label(master, bd=0)
                emt['width'] = self.cell_size
                emt['height'] = self.cell_size
                emt['text'] = ''
                emt['compound'] = 'center'

                y = space_size + (cell_size + space_size) * row
                x = space_size + (cell_size + space_size) * col

                emt.place(x=x, y=y)
                emts[row][col] = emt
        self.emts = emts
        master.pack()

    # Update UI (Score, Timer and matrix)
    def update_score(self):
        img = Image.new("RGB", (self.cell_size, self.cell_size), self.style["page"]["bg"])
        img = ImageTk.PhotoImage(img)
        self.emt_score.configure(image=img)
        self.emt_score["image"] = img

        self.emt_score["text"] = "Score:" + str(self.data.score)
    def update_timer(self):
        # Input 0 to display a positive timer
        if self.time_limit == 0:
            elapsed_time = datetime.now() - self.start_time
            self.timer_label.configure(text="Time: " + str(elapsed_time)[:-3])
        # Input other integer to display a negative timer
        elif self.time_limit > 0:
            remaining_time = (
                self.time_limit - (datetime.now() - self.start_time).total_seconds()
            )
            if remaining_time > 0:
                self.timer_label.configure(
                    text="Time: " + str(timedelta(seconds=int(remaining_time)))
                )
            else:
                self.reset_game()
        self.timer = self.root.after(1000, self.update_timer)

    # Update the ui after each operation
    def update_ui(self):
        self.update_score()
        self.update_timer()
        matrix = self.data.matrix
        for row in range(self.column):
            for col in range(self.column):
                num = matrix[row][col]

                emt = self.emts[row][col]
                img = Image.new(
                    'RGB', (self.cell_size, self.cell_size), self.style[num]['bg'])
                img = ImageTk.PhotoImage(img)
                emt.configure(image=img)
                emt['fg'] = self.style[num]['fg']
                emt['bg'] = self.style[num]['bg']
                emt['image'] = img
                emt['font'] = ("Verdana", self.style[num]['fz'], "bold")
                emt['text'] = self.word_dict.get(num, "") if num != 0 else ''

    # Event loop
    def key_event(self, event):
        print(event)
        # print(f"keyboard input:{ event.keysym }, ASCII:{ event.keycode }")
        if event.keysym in ['Up', 'w', 'Down', 's', 'Left', 'a', 'Right', 'd']:
            if event.keysym in ['Up', 'w']:    # Up
                self.data.matrix_move('U')
            elif event.keysym in ['Down', 's']:  # Down
                self.data.matrix_move('D')
            elif event.keysym in ['Left', 'a']:  # Left
                self.data.matrix_move('L')
            elif event.keysym in ['Right', 'd']:  # Right
                self.data.matrix_move('R')
            self.data.generate_number()

        # Press z to return to last step
        if event.keysym == 'z':
            if self.data.history != []:
                self.data.prev_step()
        self.update_ui()

        if self.data.gameover() is True:
            if self.t == 0:
                self.t = 1
            else:
                self.reset_game()

    # Restart the game
    def reset_game(self):
        res = messagebox.askyesno(
            title="2048", message="Game Over!\nRestart or not?")
        if res is True:
            self.t = 0
            self.root.destroy()
            GameGrid()
        else:
            self.root.quit()

    # Get the settings from SelectionWindow class
    def get_custom_settings(self):
        selection_window = SelectionWindow()
        return selection_window.get_settings()

    def main(self):
        self.update_ui()
        self.root.bind('<Key>', self.key_event)

        self.root.mainloop()

# Game setting interface
class SelectionWindow:
    def __init__(self):
        self.root = Tk()
        self.root.title("2048 Settings")
        self.column = None
        self.theme = None
        self.word_theme = None
        self.time_limit = None
        self.create_widgets()

    def create_widgets(self):
        # Get the grid size
        label = Label(self.root, text="Customize your game size\nplease enter an integer between 2 and 10: ")
        label.pack(pady=10)

        self.size_entry = Entry(self.root)
        self.size_entry.pack()

        theme_label = Label(self.root, text="Select Color Theme:")
        theme_label.pack(pady=5)

        # Create an option menu to select themes
        self.theme_var = StringVar(self.root)
        self.theme_var.set(list(c.THEME_COLORS.keys())[0])  # default theme
        theme_menu = OptionMenu(self.root, self.theme_var, *list(c.THEME_COLORS.keys()))
        theme_menu.pack()

        word_theme_label = Label(self.root, text="Select Word Theme:")
        word_theme_label.pack(pady=5)

        # Create an option menu to select word themes
        self.word_theme_var = StringVar(self.root)
        self.word_theme_var.set("Numbers")
        word_theme_menu = OptionMenu(self.root, self.word_theme_var, "Numbers", "Emojis", "Crypto", "Harry Potter", "Custom")
        word_theme_menu.pack()

        self.custom_word_theme_entry = Entry(self.root)
        self.custom_word_theme_entry.pack()
        self.custom_word_theme_entry.config(state="disabled")

        # Get the time limit number
        time_limit_label = Label(self.root, text="Time limit (integer >= 0), enter 0 for positive timing: ")
        time_limit_label.pack(pady=10)
        self.time_limit_entry = Entry(self.root)
        self.time_limit_entry.pack()

        confirm_button = Button(self.root, text="Confirm", command=self.confirm_size_and_theme)
        confirm_button.pack(pady=10)

        self.word_theme_var.trace_add("write", self.toggle_custom_word_theme_entry)

    # Disable the text box when selecting four default word themes
    def toggle_custom_word_theme_entry(self, *args):
        if self.word_theme_var.get() == "Custom":
            self.custom_word_theme_entry.config(state="normal")
        else:
            self.custom_word_theme_entry.config(state="disabled")

    # Ensure the time entered is valid
    def validate_time_limit(self, time_limit):
        try:
            time_limit = int(time_limit)
            if time_limit < 0:
                raise ValueError()
        except ValueError:
            raise ValueError()
        return time_limit

    # Ensure the size and custom word theme entered are valid
    def confirm_size_and_theme(self):
        try:
            custom_column = int(self.size_entry.get())
            if custom_column < 2:
                messagebox.showerror("Invalid Input", "Size must be at least 2x2.")
            elif custom_column > 10:
                messagebox.showerror("Invalid Input", "Size must be at most 10x10.")
            else:
                self.column = custom_column
                self.theme = self.theme_var.get()
                self.time_limit = self.validate_time_limit(self.time_limit_entry.get())
                selected_word_theme = self.word_theme_var.get()
                if selected_word_theme == "Numbers":
                    self.word_theme = c.word_theme_1
                elif selected_word_theme == "Emojis":
                    self.word_theme = c.word_theme_2
                elif selected_word_theme == "Crypto":
                    self.word_theme = c.word_theme_3
                elif selected_word_theme == "Harry Potter":
                    self.word_theme = c.word_theme_4
                elif selected_word_theme == "Custom":
                    custom_word_theme = self.custom_word_theme_entry.get()
                    custom_word_theme = custom_word_theme.split(',')
                    if len(custom_word_theme) == 10:
                        self.word_theme = {2 ** (i+1): custom_word_theme[i] for i in range(10)}
                    else:
                        messagebox.showerror("Invalid Input", "Custom word theme must have 10 elements.")
                        return
                self.root.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer not less than 0.")

    def get_settings(self):
        self.root.mainloop()
        return self.column, self.theme, self.word_theme, self.time_limit

g = GameGrid()