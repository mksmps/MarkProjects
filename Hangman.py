# window interface
import tkinter
import tkinter as tk
from tkinter import *
# regular expressions
import re

# this class holds all window objects and does all window updates
class WordWindow:
    # initializing all window objects, but not placing them in the window just yet
    def __init__(self):
        self.window = Tk()
        self.window.geometry('600x600')
        self.window.resizable(False, False)
        self.window.title("Mark Sampias's Hangman")
        self.mw = tk.StringVar()
        self.row_length = 130
        self.mws_label_1 = Label(self.window, text="Enter the words for the person to pick: ", font=('bold', 20))
        self.mws_label_2 = Label(self.window, text="", fg='red', font=('bold', 22))
        self.mws_entry_1 = Entry(self.window, textvariable=self.mw, width=20, justify=CENTER, font=('normal', 20))
        self.mws_button_1 = Button(self.window, text="Play", command=lambda: check_word(self.mw.get().upper()), font=('normal', 20))
        self.gs_label_1 = Label(self.window, text="Hangman", font=('bold', 25))
        self.gs_label_2 = Label(self.window, text='', font=('bold', 25))
        self.gs_label_3 = Label(self.window, text='', font=('bold', 25))
        self.gs_button_1 = Button(self.window, text='Play Again?', command=lambda: self.play_again())
        self.button = []
        self.canvas = Canvas(master=self.window, height=300, width=210, bg='white')
        self.game_screen_active = False
        # this is the list of virtual keys in the window
        self.button_labels = [
            "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P",
            "A", "S", "D", "F", "G", "H", "J", "K", "L",
            "Z", "X", "C", "V", "B", "N", "M"]

    # puts the objects in the window to receive the mystery word
    def create_mystery_word_screen(self):

        self.mws_label_1.grid(row=0, column=0, padx=self.row_length, pady=50)
        self.mws_entry_1.grid(row=2, column=0, padx=self.row_length, pady=0)
        self.mws_button_1.grid(row=4, column=0, padx=self.row_length, pady=50)
        # makes it so the entry has the cursor already in it
        self.mws_entry_1.focus_set()
        self.window.update()

    # resets and hides the game objects in the window, then sets up to
    # receive a new mystery word
    def play_again(self):

        # deletes the text in the entry box
        self.mws_entry_1.delete(0, 'end')
        # deletes the hangman on the canvas
        self.canvas.delete('all')
        self.canvas.place_forget()

        self.gs_label_1.place_forget()
        self.gs_label_2.place_forget()
        self.gs_label_3.place_forget()
        self.gs_button_1.place_forget()

        for label in self.button_labels:
            # resets and re-enables keys on the virtual keyboard
            self.button[self.button_labels.index(label)].configure(highlightbackground='systemWindowBackgroundColor', state=NORMAL)
            self.button[self.button_labels.index(label)].place_forget()

        # sets this so the key listeners know that we are choosing a
        # mystery word
        self.game_screen_active = False
        self.create_mystery_word_screen()

    # puts the game objects on the screen to guess the word
    def create_game_screen(self, mystery_word_redacted):
        self.gs_label_1.place(relx=0.5, rely=0.03, anchor='n')
        self.canvas.place(relx=0.5, rely=0.35, anchor=CENTER)

        # shows the redacted mystery word on screen
        self.gs_label_2.configure(text=mystery_word_redacted)
        self.gs_label_2.place(relx=0.5, rely=0.66, anchor='n')

        # here we use loops and conditionals to put the virtual keys on the screen exactly
        # where we need them
        letter_column = 0
        letter_row = 0
        extra_push = 0
        letter_index = 0

        for label in self.button_labels:
            self.button.append(
                tk.Button(self.window, text=label, width=2, disabledforeground='black'))
            # label=label is necessary for it to retain the variable information.
            # without it, all members of the list will use the label from the last
            # iteration, which would be the 26th letter, M
            self.button[letter_index].configure(command=lambda label=label: letter_chosen(label))

            if letter_column == 10 and letter_row == 0:
                letter_column = 0
                letter_row = 1
                extra_push = 0.045
            elif letter_column == 9 and letter_row == 1:
                letter_column = 0
                letter_row = 2
                extra_push = 0.09

            self.button[letter_index].place(relx=0.05 + extra_push + (letter_column * 0.09), rely=0.83 + (letter_row * 0.05), anchor='w')
            letter_column += 1
            letter_index += 1

        # this makes the program update the window to show progress
        self.window.update()
        # setting this so the key listeners know that we are playing the game
        self.game_screen_active = True

    # draws part of the "hangman" based on how many tries they have left
    def draw_part(self, incorrect_tries):

        x1 = 50
        y1 = 50

        if incorrect_tries == 6:
            self.canvas.create_line((120 + x1, 217 + y1), (140 + x1, 232 + y1), fill="black", width=3)
            self.canvas.create_line((130 + x1, 0 + y1), (130 + x1, 225 + y1), fill="black", width=2)
            self.canvas.create_line((130 + x1, 0 + y1), (30 + x1, 0 + y1), fill="black", width=2)
            self.canvas.create_line((30 + x1, 0 + y1), (30 + x1, 20 + y1), fill="black", width=2)
        elif incorrect_tries == 5:
            self.canvas.create_oval((0 + x1, 20 + y1), (60 + x1, 100 + y1), outline="black", fill="white", width=2)
        elif incorrect_tries == 4:
            self.canvas.create_line((30 + x1, 100 + y1), (30 + x1, 175 + y1), fill="black", width=2)
        elif incorrect_tries == 3:
            self.canvas.create_line((30 + x1, 120 + y1), (50 + x1, 135 + y1), fill="black", width=2)
        elif incorrect_tries == 2:
            self.canvas.create_line((30 + x1, 120 + y1), (10 + x1, 135 + y1), fill="black", width=2)
        elif incorrect_tries == 1:
            self.canvas.create_line((30 + x1, 175 + y1), (50 + x1, 190 + y1), fill="black", width=2)
        else:
            self.canvas.create_line((30 + x1, 175 + y1), (10 + x1, 190 + y1), fill="black", width=2)
            self.canvas.create_text((30 + x1, 60 + y1), text='DEAD', fill='red')

    # this gets called to change the virtual key based on whether it was found or not
    def letter_button_used(self, button_label, letter_found):
        if letter_found:
            key_color = 'green'
        else:
            key_color = 'red'
        self.button[self.button_labels.index(button_label)].configure(highlightbackground=key_color, state=DISABLED)

    # updates the label in the window after the letter is chosen and was found
    # in the mystery word
    def update_mystery_word_redacted(self, mystery_word_redacted):
        self.gs_label_2.configure(text=mystery_word_redacted)

    # ends the game and allows the user a button to play again
    def game_over(self, win):
        if win:
            self.gs_label_3.configure(foreground='green', text='You Win!')
        else:
            self.gs_label_3.configure(foreground='red', text='You Lose')

        self.gs_label_3.place(relx=0.5, rely=0.73, anchor='n')
        self.gs_button_1.place(relx=0.5, rely=0.61, anchor='n')
# End class WordWindow

# this class mostly just initializes and holds variables that are then changed
# each time a letter is chosen
class MysteryWordTries:
    def __init__(self):
        self.allowed_incorrect_tries = 0
        self.mystery_word = ""

        self.incorrect_tries = 0
        # we need lists that we can iterate through to find and place letters
        self.mystery_word_list = []
        self.mystery_word_split = []
        self.mystery_word_redacted = ""
        self.mystery_word_redacted_list = []

        # we need to be able to check if the letter was already hit
        self.incorrect_letters = []

        # once they've either won or lost, this will be set to true to stop the checks
        self.game_over = False

    # this takes the mystery word and puts it into different variables that will
    # allow us to play the game
    def play_game(self, total_tries, mystery_word):
        self.game_over = False
        self.allowed_incorrect_tries = total_tries
        self.mystery_word = mystery_word

        self.incorrect_tries = self.allowed_incorrect_tries

        # we need lists that we can iterate through to find and place letters
        self.mystery_word_list = list(self.mystery_word)
        self.mystery_word_split = re.split('\\s', self.mystery_word)
        self.mystery_word_redacted = ""

        for segment in self.mystery_word_split:
            self.mystery_word_redacted = self.mystery_word_redacted + '-' * len(segment) + ' '
        self.mystery_word_redacted = self.mystery_word_redacted.rstrip()
        self.mystery_word_redacted_list = list(self.mystery_word_redacted)
# End Class MysteryWordTries

# method check_word makes sure the word entered in the text box is valid: only contains letters
# or spaces, and is not empty or more than 30 characters
def check_word(mystery_word):

    if re.search('[^A-Z\\s]+', str(mystery_word)) is not None:
        word_window.mws_label_2.configure(text="Bad character entered!\nOnly use A-Z and space!")
        word_window.mws_label_2.grid(row=6, column=0, padx=word_window.row_length, pady=50)
        return
    elif len(mystery_word) > 30:
        word_window.mws_label_2.configure(text="Words should be 30\ncharacters or less")
        word_window.mws_label_2.grid(row=6, column=0, padx=word_window.row_length, pady=50)
        return
    elif len(mystery_word) == 0:
        return
    # if it passes all the tests, set the MysteryWordTries variables, create the game
    # screen, and remove the mystery word screen objects
    else:
        word_window.mws_label_1.grid_remove()
        word_window.mws_label_2.grid_remove()
        word_window.mws_entry_1.grid_remove()
        word_window.mws_button_1.grid_remove()
        mystery_word_tries.play_game(7, mystery_word)
        word_window.create_game_screen(mystery_word_tries.mystery_word_redacted)

# gets called when a letter is typed or pushed on the virtual keyboard
def letter_chosen(button_label):
    if mystery_word_tries.game_over is False:

        input_letter = button_label
        index = 0
        letter_found = False

        # go through the word, and if the input letter is found,
        # note that it was found, rewrite the redacted word to include
        # the found letters
        for letter in mystery_word_tries.mystery_word_list:
            if input_letter == letter:
                mystery_word_tries.mystery_word_redacted_list[index] = letter
                letter_found = True
                word_window.letter_button_used (input_letter, letter_found)
            index += 1

        # once you've updated the redacted word, use the list to create it as a string
        mystery_word_tries.mystery_word_redacted = ''.join(mystery_word_tries.mystery_word_redacted_list)

        # if the letter wasn't found in the word and isn't a repeat, we add to the list
        # of incorrect letters, they have one fewer try, and we draw a part of the "hangman"
        if letter_found is False:
            if input_letter not in mystery_word_tries.incorrect_letters:
                mystery_word_tries.incorrect_letters.append(input_letter)
                mystery_word_tries.incorrect_letters = list(set(mystery_word_tries.incorrect_letters))
                word_window.letter_button_used (input_letter, letter_found)
                mystery_word_tries.incorrect_tries -= 1
                word_window.draw_part(mystery_word_tries.incorrect_tries)

        # if the full word has not yet been found and they have more tries, just re-show the redacted word
        # if they do not have more tries, they lose
        if re.search("[-]", mystery_word_tries.mystery_word_redacted) is not None:
            if mystery_word_tries.incorrect_tries > 0:
                word_window.update_mystery_word_redacted(mystery_word_tries.mystery_word_redacted)
            else:
                word_window.update_mystery_word_redacted(mystery_word_tries.mystery_word)
                mystery_word_tries.game_over = True
                word_window.game_over(False)
        # if there are no more dashes in the redacted word, they won!
        else:
            word_window.update_mystery_word_redacted(mystery_word_tries.mystery_word)
            mystery_word_tries.game_over = True
            word_window.game_over(True)

# whenever a key is pressed on the physical keyboard, this function decides what to do
# or whether to do anything at all
def keydown(event):
    if word_window.game_screen_active == True and 'A' <= event.char.upper() <= 'Z':
        letter_chosen(event.char.upper())
    elif event.keysym == 'Return':
        if word_window.game_screen_active is False:
            check_word(word_window.mw.get().upper())
        else:
            if mystery_word_tries.game_over is True:
                word_window.play_again()


# main program here and below, just initializing the classes and binding
# keypress to our keydown function
word_window = WordWindow()
word_window.create_mystery_word_screen()
mystery_word_tries = MysteryWordTries()

# this is what tells the method to listen for keystrokes
word_window.window.bind("<KeyPress>", keydown)

word_window.window.mainloop()
