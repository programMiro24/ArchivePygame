import tkinter as tk
import angry_birds
import snake_game
import score_manager
import scoreboard
from PIL import Image, ImageTk

def player_game():
    player_name = entry_name.get()
    if player_name == "":
        player_name = "Player"
    return {
        "name": player_name,
        "score_angry_birds": player["score_angry_birds"],
        "score_snake": player["score_snake"]
    }

def start_snake():
    player_data = player_game()
    player_data["score_snake"] = snake_game.run(player_data)
    score_manager.update_score(player_data['name'], "snake", player_data["score_snake"])
    label_points_snake.config(text=player_data["score_snake"])

def start_angry_birds():
    player_data = player_game()
    player_data["score_angry_birds"] = angry_birds.run(player_data)
    score_manager.update_score(player_data['name'], "angry_birds", player_data["score_angry_birds"])
    label_points_angry.config(text=player_data["score_angry_birds"])

root = tk.Tk()
root.title("Game Center")
root.geometry("1200x650")
root.configure(bg="white")

root.columnconfigure(1, weight=3)
root.columnconfigure(2, weight=2)
root.rowconfigure(1, weight=1)

score_canvas = tk.Canvas(root, width=80, bg="#4a76bd", highlightthickness=0)
score_canvas.grid(row=0, column=0, rowspan=3, sticky="ns")
score_canvas.create_text(
    40, 325,
    text="Scoreboard",
    angle=90,
    font=("Arial", 15, "bold")
)
score_canvas.bind("<Button-1>", lambda e: scoreboard.show_scoreboard())

title = tk.Label(
    root,
    text="GAME CENTER",
    bg="red",
    fg="black",
    font=("Arial", 24, "bold")
)
title.grid(row=0, column=1, columnspan=2, sticky="ew")

image_frame = tk.Frame(root, bg="yellow")
image_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

def resize_image(event):
    img = Image.open("New_image.png")
    img = img.resize((event.width, event.height), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    image_label.config(image = photo)
    image_label.image = photo

image_label = tk.Label(image_frame, bg="yellow")
image_label.pack(fill="both", expand=True)
image_frame.bind("<Configure>", resize_image)

right_frame = tk.Frame(root, bg="white")
right_frame.grid(row=1, column=2, sticky="n", padx=10)

tk.Label(
    right_frame,
    text="Въведи име",
    bg="#2f7d32",
    font=("Arial", 14, "bold"),
    width=20,
    height=2
).grid(row=0, column=0, padx=5, pady=15)

entry_name = tk.Entry(
    right_frame,
    bg="#9be29b",
    font=("Arial", 14),
    width=22
)
entry_name.grid(row=0, column=1, padx=5, pady=15)

player = {"name": "Player", "score_angry_birds": 0, "score_snake": 0}

games_frame = tk.Frame(right_frame, bg="white")
games_frame.grid(row=1, column=0, columnspan=2, pady=40)

snake_img = ImageTk.PhotoImage(Image.open("snake_icon.png").resize((90, 90)))
angry_img = ImageTk.PhotoImage(Image.open("angry_icon.png").resize((90, 90)))

tk.Label(games_frame, image=snake_img, bg="white").grid(row=0, column=0, pady=5)
btn_snake = tk.Button(
    games_frame,
    text="Snake",
    bg="#4fc3f7",
    font=("Arial", 14, "bold"),
    width=18,
    height=2,
    command=start_snake
)
btn_snake.grid(row=1, column=0, padx=10)

label_points_snake = tk.Label(games_frame, text="0", font=("Arial", 14))
label_points_snake.grid(row=2, column=0, pady=5)

tk.Label(games_frame, image = angry_img, bg="white").grid(row=0, column=1, pady=5)
btn_bird = tk.Button(
    games_frame,
    text="Angry Birds",
    bg="#4fc3f7",
    font=("Arial", 14, "bold"),
    width=18,
    height=2,
    command=start_angry_birds
)
btn_bird.grid(row=1, column=1, padx=10)

label_points_angry = tk.Label(games_frame, text="0", font=("Arial", 14))
label_points_angry.grid(row=2, column=1, pady=5)

btn_exit = tk.Button(
    root,
    text="EXIT",
    bg="#f1b400",
    font=("Arial", 14, "bold"),
    width=12,
    height=2,
    command=root.quit
)
btn_exit.grid(row=2, column=2, sticky="se", padx=15, pady=15)

root.mainloop()
