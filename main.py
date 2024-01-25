from tkinter import *

timer = None
text = "hello there"
position = 0
chars = 0
correct_chars = 0


def start_timer():
    start_btn.pack_forget()
    text_widget.pack()
    user_input.pack()
    countdown(60)


def countdown(count):
    global timer
    timer_label.config(text=count)
    if count > 0:
        timer = window.after(1000, countdown, count - 1)
    else:
        end_test()


def on_user_input(event):
    global position
    global chars
    global timer
    global correct_chars

    if event.keysym == 'space':
        user_input.delete(0, END)
        position = position + 1
    else:
        chars = chars + 1
        letter = event.char
        if letter == text[position]:
            correct_chars = correct_chars + 1
            if text_widget.tag_names(f"1.{position}"):
                text_widget.tag_add("correct", f"1.{position}", f"1.{position + 1}")
                text_widget.tag_config("correct", background="green")
            position = position + 1
        else:
            text_widget.tag_add("incorrect", f"1.{position}", f"1.{position + 1}")
            text_widget.tag_config("incorrect", background="red")

    if position > len(text) - 1:
        end_test()


def end_test():
    global timer
    window.after_cancel(timer)
    user_input.pack_forget()
    chars_minute = correct_chars / (60 - int(timer_label["text"])) * 60
    accuracy = correct_chars / chars * 100
    speed_label.config(text=f"chars per minute: {'{:.2f}'.format(chars_minute)}")
    accuracy_label.config(text=f"your accuracy is: {'{:.2f}%'.format(accuracy)}")
    speed_label.pack()
    accuracy_label.pack()

# UI
window = Tk()
window.title("Type speed test")
window.config(padx=50, pady=50)

timer_label = Label(text="60")
timer_label.pack()

text_widget = Text()
text_widget.insert(INSERT, text)

user_input = Entry()
user_input.bind('<KeyRelease>', on_user_input)

start_btn = Button(text="Start", command=start_timer)
start_btn.pack()

speed_label = Label(text="")
accuracy_label = Label(text="")

window.mainloop()