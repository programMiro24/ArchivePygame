import tkinter as tk
import score_manager

def show_scoreboard():
    window = tk.Toplevel()
    window.title("Scoreboard")
    window.geometry("450x500")
    window.configure(padx=20, pady=20)

    lbl_title = tk.Label(window, text="SCOREBOARD", font=("Arial", 20, "bold"), pady=10)
    lbl_title.grid(row=0,column=0,columnspan=4,pady=(0,20))

    headers =["Place", "Player", "Snake", "Angry Birds"]
    for i, text in enumerate(headers):
        header_lbl = tk.Label(window, text=text, font=("Arial", 12, "bold"))
        header_lbl.grid(row=1, column=i, padx=10, pady=5, sticky="W")

    separator = tk.Frame(window, height=20, bd=1, relief="sunken", bg="black")
    separator.grid(row=2, column=0, columnspan=4, sticky="EW", pady=5)

    players = score_manager.load_scores()

    for p in players:
        p["total"] = p.get("score_snake", 0) + p.get("score_angry_birds", 0)

    sorted_players = sorted(players, key=lambda p: p["total"], reverse=True)
    for index, player in enumerate(sorted_players):
        row_inx = index + 3
        color = "black"
        if index == 0:color="gold" # Gold
        elif index == 1:color="gray" # Silver
        elif index == 2:color="brown" # Bronze
        tk.Label(window, text=f"{index + 1}.", font=("Arial",11,"bold"),fg=color).grid(row=row_inx, column=0,
        padx=10,pady=5, sticky="W")
        tk.Label(window, text=player.get("name", "Player"), font=("Arial",11),fg=color).grid(row=row_inx, column=1,
        padx=10,pady=5, sticky="W")
        tk.Label(window, text=player.get("score_snake", 0), font=("Arial",11),fg=color).grid(row=row_inx, column=2,
        padx=10,pady=5, sticky="WE")
        tk.Label(window, text=player.get("score_angry_birds", 0), font=("Arial",11),fg=color).grid(row=row_inx, column=3,
        padx=10,pady=5, sticky="WE")

    btn_close = tk.Button(window, text="Close", command=window.destroy, bg="red", fg="white", font=("Arial", 10, "bold"))
    btn_close.grid(row=len(sorted_players)+4, column=0, columnspan=4, pady=5, sticky="W")
