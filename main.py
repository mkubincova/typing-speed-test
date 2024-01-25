from tkinter import *
from text import sentences
import random


class TypingSpeedTest:
    def __init__(self, window, heading):
        self.timer = None
        random.shuffle(sentences)
        self.text = " ".join(sentences)
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
        self.start_btn = Button(text="Start", command=self.start_test, font=("Arial", 20), padx=10, pady=7)
        self.timer_label = Label(text="60", font=("Arial", 25), pady=10)
        self.text_widget = Text(font=("Arial", 20), width=1, height=1, spacing2=10, wrap=WORD)
        self.text_widget.insert(END, self.text)
        self.user_input = Entry()
        self.user_input.bind('<KeyPress>', self.on_user_input)
        self.speed_label = Label(text="", font=("Arial", 20))
        self.accuracy_label = Label(text="", font=("Arial", 20))

        # Display initial UI
        self.heading_label.pack()
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
        self.start_btn.pack_forget()
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
        self.text_widget.tag_config('current', underline=True, underlinefg='yellow')

    def set_incorrect_char(self):
        self.text_widget.tag_add("incorrect", f"1.{self.position}", f"1.{self.position + 1}")
        self.text_widget.tag_config("incorrect", background="red")

    def set_corrected_char(self):
        self.text_widget.tag_remove("incorrect", f"1.{self.position}", f"1.{self.position + 1}")
        self.text_widget.tag_add("correct", f"1.{self.position}", f"1.{self.position + 1}")
        self.text_widget.tag_config("correct", background="blue")

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
