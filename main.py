from tkinter import *
from text import text_easy, text_medium, text_hard
import random

DIFFICULTY = {
    1: text_easy,
    2: text_medium,
    3: text_hard
}

class TypingSpeedTest:
    def __init__(self, window, heading):
        self.timer = None
        self.text = ""
        self.position = 0
        self.chars = 0
        self.correct_chars = 0
        self.counter = 60

        # UI
        self.window = window
        self.window.title("Typing speed test")
        self.window.config(padx=50, pady=50)
        self.center_window()

        self.heading_label = Label(text=heading, font=("Arial", 40), pady=20)
        self.difficulty = IntVar(value=1)
        self.frame_1 = Frame(self.window)
        self.easy_radio = Radiobutton(self.frame_1, text="Easy", variable=self.difficulty, value=1, pady=20,  font=("Arial", 18))
        self.medium_radio = Radiobutton(self.frame_1, text="Medium", variable=self.difficulty, value=2, pady=20, font=("Arial", 18))
        self.hard_radio = Radiobutton(self.frame_1, text="Hard", variable=self.difficulty, value=3, pady=20, font=("Arial", 18))
        self.start_btn = Button(text="Start", command=self.start_test, font=("Arial", 20), padx=10, pady=7)

        self.timer_label = Label(text="60", font=("Arial", 25), pady=10)
        self.text_widget = Text(font=("Arial", 20), width=1, height=1, spacing2=10, wrap=WORD, background="#332941", foreground="white")
        self.user_input = Entry(font=("Arial", 20))
        self.user_input.bind('<KeyPress>', self.on_user_input)
        self.speed_label = Label(text="", font=("Arial", 20))
        self.accuracy_label = Label(text="", font=("Arial", 20))

        # Starting UI
        self.heading_label.pack()
        self.frame_1.pack()
        self.easy_radio.pack(side='left')
        self.medium_radio.pack(side='left')
        self.hard_radio.pack(side='left')
        self.start_btn.pack()

    def center_window(self):
        window_height = 800
        window_width = 800
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_cor = int((screen_width / 2) - (window_width / 2))
        y_cor = int((screen_height / 2) - (window_height / 2))
        self.window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cor, y_cor))

    def start_test(self):
        # Set text
        text_list = DIFFICULTY[self.difficulty.get()]
        random.shuffle(text_list)
        self.text = " ".join(text_list)
        self.text_widget.insert(END, self.text)

        # Remove starting UI
        self.frame_1.destroy()
        self.start_btn.destroy()

        # Add test UI & start countdown
        self.timer_label.pack()
        self.text_widget.pack(side='top', fill='both', expand=True)
        self.update_current_char()
        self.user_input.pack()
        self.user_input.focus()
        self.countdown()

    def countdown(self):
        self.timer_label.config(text=self.counter)
        if self.counter > 0:
            self.counter = self.counter - 1
            self.timer = self.window.after(1000, self.countdown)
        else:
            self.end_test()

    def update_current_char(self):
        self.text_widget.tag_remove('current', f"1.0", "end")
        self.text_widget.tag_add('current', f"1.{self.position}", f"1.{self.position + 1}")
        self.text_widget.tag_config('current', underline=True, underlinefg='#FFBE00')

    def set_incorrect_char(self):
        self.text_widget.tag_add("incorrect", f"1.{self.position}", f"1.{self.position + 1}")
        self.text_widget.tag_config("incorrect", background="#DC0000")

    def set_corrected_char(self):
        self.text_widget.tag_remove("incorrect", f"1.{self.position}", f"1.{self.position + 1}")
        self.text_widget.tag_add("correct", f"1.{self.position}", f"1.{self.position + 1}")
        self.text_widget.tag_config("correct", background="#2E99B0")

    def on_user_input(self, event):
        if event.keysym == 'space':
            self.user_input.delete(0, END)

        if event.char:
            self.chars = self.chars + 1
            letter = event.char
            if letter == self.text[self.position]:
                self.correct_chars = self.correct_chars + 1
                if "incorrect" in self.text_widget.tag_names(f"1.{self.position}"):
                    self.set_corrected_char()
                self.position = self.position + 1
            else:
                self.set_incorrect_char()

        self.update_current_char()

        if self.position == len(self.text) - 1:
            self.end_test()

    def end_test(self):
        self.window.after_cancel(self.timer)
        self.user_input.config(state="disabled")
        self.user_input.pack_forget()

        chars_minute = self.correct_chars / (60 - int(self.timer_label["text"])) * 60
        accuracy = self.correct_chars / self.chars * 100 if self.chars else 0
        self.speed_label.config(text=f"Characters per minute: {'{:.2f}'.format(chars_minute)}")
        self.accuracy_label.config(text=f"Accuracy: {'{:.2f}%'.format(accuracy)}")
        self.speed_label.pack()
        self.accuracy_label.pack()


if __name__ == "__main__":
    root = Tk()
    app = TypingSpeedTest(window=root, heading="Welcome to the Typing speed test!")
    root.mainloop()
