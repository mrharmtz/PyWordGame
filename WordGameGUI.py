import tkinter as tk
import tkinter.font
import time

import WordGame as wg


class WordGameFrame(tk.Frame):

    SCORE_TEXT = 'Score: %d'
    TIME_TEXT = 'Time: %lf'
    AVERAGE_TEXT = 'Average Time: %lf'
    START_DIFFICULTY = [3,4]

    def __init__(self, parent, cnf: dict = {}, word_count=3, **kwargs):
        super().__init__(parent, cnf, **kwargs)

        self.__word_game_core = wg.WordGame()

        self.__displayed_words = []
        self.__difficulty = self.START_DIFFICULTY

        for i in range(word_count):
            self.__displayed_words.append(tk.StringVar())
            self.__displayed_words[i].set(self.__word_game_core.generate(difficulty=self.__difficulty))

        self.__typed_word = tk.StringVar()
        self.__typed_word.set('')

        self.__score = tk.StringVar()
        self.__score.set(self.SCORE_TEXT % self.__word_game_core.score)

        self.__average = tk.StringVar()
        self.__average.set(self.AVERAGE_TEXT % self.__word_game_core.average_time)
        self.__time = tk.StringVar()
        self.__update_time()

        fontstyle = tk.font.Font(family='Lucida Grande', size=28)

        row = 0

        self.__score_display = tk.Label(self, textvariable=self.__score)
        self.__score_display.grid(row=row, column=0)

        self.__time_display = tk.Label(self, textvariable=self.__time)
        self.__time_display.grid(row=row, column=1)

        self.__average_display = tk.Label(self, textvariable=self.__average)
        self.__average_display.grid(row=row, column=2)

        self.__word_displays = []

        for i in range(word_count):
            row += 1
            self.__word_displays.append(tk.Label(self, textvariable=self.__displayed_words[i], font=fontstyle))
            self.__word_displays[i].grid(row=row, column=0, columnspan=3)

        row += 1
        self.__word_entry = tk.Entry(self, textvariable=self.__typed_word, font=fontstyle)
        self.__word_entry.grid(row=row, column=0, columnspan=3)
        self.__word_entry.bind('<Return>', self.__return_pushed)

    def __update_time(self):
        self.__time.set(self.TIME_TEXT % (time.time() - self.__word_game_core.start_time))
        self.after(100, self.__update_time)

    def __return_pushed(self, event=None):
        try:
            index = [value.get() for value in self.__displayed_words].index(self.__typed_word.get())
            self.__word_game_core.point(self.__typed_word.get())

            if self.__word_game_core.score >= (len(self.__difficulty) - 1) * 100:
                self.__difficulty.append(max(self.__difficulty) + 1)

            self.__displayed_words[index].set(self.__word_game_core.generate(difficulty=self.__difficulty))
            self.__average.set(self.AVERAGE_TEXT % self.__word_game_core.average_time)
        except ValueError:
            pass

        self.__typed_word.set('')
        self.__score.set(self.SCORE_TEXT % self.__word_game_core.score)


def main():

    root = tk.Tk()
    root.title('word game')

    word_game_frame = WordGameFrame(root)
    word_game_frame.pack()

    root.mainloop()


if __name__ == '__main__':
    main()