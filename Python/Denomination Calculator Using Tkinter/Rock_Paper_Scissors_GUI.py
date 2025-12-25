import tkinter as tk
import random as ran


window = tk.Tk()
window.title("Rock, Paper, Scissors")


result_label = tk.Label(window, text="Make Your Choice!")
result_label.pack(fill="x", padx= 50, pady=10)


def play(user_choice):

    computer_choice = ran.choice(["Rock", "Paper", "Scissors"])

    if user_choice == computer_choice:
        result = "It's a Tie!"
    
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Paper" and computer_choice == "Rock") or \
         (user_choice == "Scissors" and computer_choice == "Paper"):
        result = "You Win!"

    else:
        result = "You Lose!"

    result_label.config(text=f"Computer chose {computer_choice} | You chose {user_choice} | Result: {result}")
    

rock_button = tk.Button(window, text="Rock", command=lambda: play("Rock"))
rock_button.pack(side="left", padx=20, pady=20)

paper_button = tk.Button(window, text="Paper", command=lambda: play("Paper"))
paper_button.pack(side="top", pady=20)

scissors_button = tk.Button(window, text="Scissors", command=lambda: play("Scissors"))
scissors_button.pack(side="right", padx=20, pady=20)

window.mainloop()





