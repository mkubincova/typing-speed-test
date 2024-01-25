from tkinter import *
from text import sentences
import random

random.shuffle(sentences)
text = " ".join(sentences)
timer = None
position = 0
chars = 0
correct_chars = 0


def start_timer():
    start_btn.pack_forget()
    timer_label.pack()
    text_widget.pack(side='top',fill='both',expand=True)
    user_input.pack()
    user_input.focus()
    countdown(60)


def countdown(count):
    global timer
    timer_label.config(text=count)
    if count > 0:
        timer = window.after(1000, countdown, count - 1)
    else:
        end_test()


def update_current_char(pos):
    text_widget.tag_remove('current', f"1.0", "end")
    text_widget.tag_add('current', f"1.{pos}", f"1.{pos + 1}")
    text_widget.tag_config('current', underline=True, underlinefg='yellow')


def set_incorrect_char(pos):
    text_widget.tag_add("incorrect", f"1.{pos}", f"1.{pos + 1}")
    text_widget.tag_config("incorrect", background="red")


def set_corrected_char(pos):
    text_widget.tag_remove("incorrect", f"1.{pos}", f"1.{pos + 1}")
    text_widget.tag_add("correct", f"1.{pos}", f"1.{pos + 1}")
    text_widget.tag_config("correct", background="blue")


def on_user_input(event):
    global position
    global chars
    global correct_chars
    global text

    if event.keysym == 'space':
        user_input.delete(0, END)
    if event.char:
        chars = chars + 1
        letter = event.char
        if letter == text[position]:
            correct_chars = correct_chars + 1
            if "incorrect" in text_widget.tag_names(f"1.{position}"):
                set_corrected_char(position)
            position = position + 1
        else:
            set_incorrect_char(position)

    update_current_char(position)

    if position == len(text) - 1:
        end_test()


def end_test():
    global timer
    window.after_cancel(timer)
    user_input.pack_forget()
    chars_minute = correct_chars / (60 - int(timer_label["text"])) * 60
    accuracy = correct_chars / chars * 100 if chars else 0
    speed_label.config(text=f"Characters per minute: {'{:.2f}'.format(chars_minute)}")
    accuracy_label.config(text=f"Accuracy: {'{:.2f}%'.format(accuracy)}")
    speed_label.pack()
    accuracy_label.pack()


def center_window():
    window_height = 800
    window_width = 800
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_cor = int((screen_width / 2) - (window_width / 2))
    y_cor = int((screen_height / 2) - (window_height / 2))
    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cor, y_cor))


# UI
window = Tk()
window.title("Type speed test")
window.config(padx=50, pady=50)
center_window()

heading_label = Label(text="Typing speed test", font=("Arial", 40), pady=20)
heading_label.pack()

timer_label = Label(text="60", font=("Arial", 25), pady=10)

text_widget = Text(font=("Arial", 20), width=1, height=1, spacing2=10, wrap=WORD)
text_widget.insert(END, text)
text_widget.tag_add('current', f"1.{position}", f"1.{position + 1}")
text_widget.tag_config('current', underline=True, underlinefg='yellow')

user_input = Entry()
user_input.bind('<KeyPress>', on_user_input)

start_btn = Button(text="Start", command=start_timer, font=("Arial", 20), padx=10, pady=7)
start_btn.pack()

speed_label = Label(text="", font=("Arial", 20))
accuracy_label = Label(text="", font=("Arial", 20))

window.mainloop()