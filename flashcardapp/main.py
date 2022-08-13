import random
from tkinter import *
from tkinter import messagebox
import pandas
BACKGROUND_COLOR = "#B1DDC6"

# imports the main data
try:
    with open(file="data/english_words.csv", encoding="utf-8") as data_file:
        df = pandas.DataFrame(pandas.read_csv(data_file))
        df_dict = df.to_dict(orient="records")
        index = random.choice(range(0, len(df_dict) + 1))
        word_tr = df_dict[index]["turkish"]
        word_en = df_dict[index]["english"]
except FileNotFoundError:
    messagebox.showerror(message="english_words.csv not found.")

# creates a copy of main data and remove known words in order not to see them again.
# main data still remains and code will be able to edit.
try:
    with open(file="data/english_words_personal.csv", encoding="utf-8", mode="r") as personal_data:
        pass
except FileNotFoundError:
    with open(file="data/english_words.csv", encoding="utf-8", mode="r") as data_file:
        data = data_file.read()
    with open(file="data/english_words_personal.csv", mode="w", encoding="utf-8") as personal_data:
        personal_data.write(data)


def wrong_button():
    global text, index, word_tr, word_en
    with open(file="data/unknown_words.csv", encoding="utf-8", mode="a") as save_file:
        save_file.write(f"{word_en},{word_tr}\n")

    with open(file="data/english_words_personal.csv", encoding="utf-8", mode="r") as data_file:
        df = pandas.DataFrame(pandas.read_csv(data_file))
        index = random.choice(range(1, len(df_dict) + 1))
        word_tr = df_dict[index]["turkish"]
        word_en = df_dict[index]["english"]
        canvas.delete(text)
        text = canvas.create_text(425, 275, text=f"{word_en}", anchor="center", width=500,
                                  font=("New Times Roman", 50, "bold"))
        canvas.update()


def right_button():
    with open(file="data/english_words_personal.csv", encoding="utf-8", mode="r") as data_file:
        global text, index, word_tr, word_en
        df_dict.remove(df_dict[index])
        df = pandas.DataFrame(pandas.read_csv(data_file))
        index = random.choice(range(1, len(df_dict) + 1))
        word_tr = df_dict[index]["turkish"]
        word_en = df_dict[index]["english"]
        canvas.delete(text)
        text = canvas.create_text(425, 275, text=f"{word_en}", anchor="center", width=500,
                                  font=("New Times Roman", 50, "bold"))


def hint():
    new_text = canvas.create_text(425, 325, text=f"{word_tr}", anchor="center", width=500,
                                  font=("New Times Roman", 30, "bold"))
    canvas.update()
    canvas.after(2000, func=canvas.delete(new_text))


# GUI PART BEGINS BELOW
# window
window = Tk()
window.configure(padx=35, pady=35, background=BACKGROUND_COLOR)
window.title("Flash Card App")

# image
card_back_img = PhotoImage(file="images/card_back.png")
card_front_img = PhotoImage(file="images/card_front.png")
wrong_img = PhotoImage(file="images/wrong.png")
right_img = PhotoImage(file="images/right.png")
answer_img = PhotoImage(file="images/hint_img.png")

# canvas
canvas = Canvas()
canvas.configure(background=BACKGROUND_COLOR, height=550, width=850, highlightthickness=0)
canvas.create_image(35, 25, image=card_front_img, anchor="nw")
canvas.grid(row=0, column=0, columnspan=3)

text = canvas.create_text(425, 275, text=f"{word_en}", width=500,
                          font=("New Times Roman", 50, "bold"))
# buttons
right_button = Button(image=right_img, highlightthickness=0, command=right_button)
right_button.grid(row=1, column=2)

wrong_button = Button(image=wrong_img, highlightthickness=0, command=wrong_button)
wrong_button.grid(row=1, column=0)

answer_button = Button(image=answer_img, highlightthickness=0, command=hint)
answer_button.grid(row=1, column=1)

window.mainloop()
