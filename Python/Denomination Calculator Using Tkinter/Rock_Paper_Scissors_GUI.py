import tkinter as tk
import random as ran

window = tk.Tk()
window.title("Rock, Paper, Scissors")


result_label = tk.Label(window, text="Make Your Choice!")
result_label.pack(fill="x", padx= 50, pady=10)

def play_rock():
    computer_choice = ran.choice(["Rock", "Paper", "Scissors"])
    user_choice = "Rock"


    if computer_choice == "Scissors":
        result_label.config(text=f"Computer chose {computer_choice} | You chose {user_choice} | Rock smashes Scissors | Result: You win")
    
    elif computer_choice == "Rock":
        result_label.config(text=f"Computer chose {computer_choice} | You chose {user_choice} | Rock and Rock | Result: Draw!")

    else:
        result_label.config(text=f"Computer chose {computer_choice} | You chose {user_choice} | Paper covers Rock | Result: You lose!")
       

rock_button = tk.Button(window, text="Rock", command= play_rock)
rock_button.pack(side="left", padx=20, pady=20)

def play_paper():
    computer_choice = ran.choice(["Rock", "Paper", "Scissors"])
    user_choice = "Paper"

    if computer_choice == "Rock":
        result_label.config(text=f"Computer chose {computer_choice} | You chose {user_choice} | Paper covers Rock | Result: You win")

    elif computer_choice == "Paper":
        result_label.config(text=f"Computer chose {computer_choice} | You chose {user_choice} | Paper and Paper | Result: Draw!")

    else:
        result_label.config(text=f"Computer chose {computer_choice} | You chose {user_choice} | Scissors cuts Paper | Result: You lose!")



paper_button = tk.Button(window, text="Paper", command= play_paper)
paper_button.pack(side="top", pady=20)


def play_scissors():
    computer_choice = ran.choice(["Rock", "Paper", "Scissors"])
    user_choice = "Scissors"

    if computer_choice == "Paper":
        result_label.config(text=f"Computer chose {computer_choice} | You chose {user_choice} | Scissors cuts Paper | Result: You win!")

    elif computer_choice == "Scissors":
        result_label.config(text=f"Computer chose {computer_choice} | You chose {user_choice} | Scissors and Scissors | Result: Draw!")

    else:
        result_label.config(text=f"Computer chose {computer_choice} | You chose {user_choice} | Rock smashes Scissors | Result: You lose!")


scissors_button = tk.Button(window, text="Scissors", command=play_scissors)
scissors_button.pack(side="right", padx=20, pady=20)

window.mainloop()





