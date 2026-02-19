from tkinter import *
import random

from cloudinit.util import center
print()
from v2 import history
history = []

class menu():
    """menu class"""
    def __init__(self):
        """the menu of the game"""
        self.frame = Frame(padx=10, pady=10)
        self.frame.grid(row=0, column=0)
        # frame
        intro_string = ("In each round you invinted to choose a colour your goal is to beat the target score"
                        "and win the round (and keep your points)")
        # intro string
        choose_string = ("how many rounds do you want to play?")
        # instrictons
        labels_list = [
            ["Colour Quest", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12"), None],
            [choose_string, ("Arial", "12","bold"), None, "#009900"],
        ]
        # list of labels
        start_label_ref = []
        for count, item in enumerate(labels_list):
            make_label = Label(self.frame, text=item[0],font=item[1],
                               fg=item[2],wraplength=350,justify="left",padx=20,pady=10)
            make_label.grid(row=count)
            start_label_ref.append(make_label)
        # label makers

        self.choose_label = start_label_ref[2]

        self.entry = Entry(self.frame, font=("arial", 14))
        self.entry.grid(row=3, column=0,padx=10,pady=10)
        # input for rounds
        self.start_button = Button(self.frame, text="Play", font=("arial", 16,"bold"),
                                   fg="#FFFFFF", bg="#0057D8",width=10,command=self.check_rounds)
        self.start_button.grid(row=4, column=0)

    def check_rounds(self):
        """Checks users have entered 1 or more rounds"""
        rounds_wanted = self.entry.get()
        self.choose_label.config(fg="#009900", font=("arial", 12,"bold"))
        self.entry.config(bg="#FFFFFF")

        error = ("please choose a number bigger than zero and less than 10000")
        # this code has no effect it is useless like my life
        haserrors = "no"
        # preset the errors to none
        try:
            rounds_wanted = int(rounds_wanted)
            if 10000 > int(rounds_wanted) >= 1:
                self.playgame_goto(rounds_wanted)
            else:
                haserrors = "yes"
        except ValueError:
            haserrors = "yes"

        if haserrors == "yes":
            self.choose_label.config(fg="#990000", font=("arial", 10,"bold"),)
            self.entry.config(bg="#F4CCCC")
            self.entry.delete(0, "end")
    def playgame_goto(self,rounds_wanted):
        self.frame.destroy()
        playgame(rounds_wanted,0)


class playgame():
    """the game"""
    def __init__(self, how_many,n):
        """the game
        gottem"""

        hexes = "ABCDEF0123456789"
        # all hex chaharters
        score = []
        # list of scores in a round
        q = []
        # where we store our hex codes
        for pp in range(4):
            # number of buttons
            temp_text = ""
            for item in range(6):
                # number of wzexrctfvygbhunjimko, in a colour hex
                temp_text += hexes[random.randint(0,15)]
                print(temp_text)
            q.append("#"+temp_text)
            # for the colour
            R,G,B = (tuple(int(temp_text[i:i + 2], 16) for i in (0, 2, 4)))
            score.append( 0.2126 * R + 0.7152 * G + 0.0722 * B)
            # magic to measure brightness
        # print(score)
        reqscore = sum(score)/4
        # print(reqscore)
        # if you want to cheat here are the tools also l you suck if you need to cheat
        global history
        # the history of the world
        self.game_frame = Frame(padx=10, pady=10)
        self.game_frame.grid(padx=10,pady=10)
        self.other_frame = Frame(self.game_frame)
        self.other_frame.grid(row=7)
        # frame setup
        self.game_heading_label = Label(self.game_frame, text=f"round {n} of {how_many}", font=("arial", 16,"bold"))
        self.game_heading_label.grid(row=0)
        # headding
        self.required_score = Label(self.game_frame, text=f"must beat: {reqscore}", font=("arial", 16,"bold"))
        self.required_score.grid(row=1)
        # required score
        self.responce = Label(self.game_frame, text="choose your colour", font=("arial", 16,"bold"))
        self.responce.grid(row=5)
        # suggested input
        self.buttons(q,NORMAL,score,reqscore)
        # this is cool its just maped to buttons though
        self.next_round = (Button(self.game_frame, text="next round", font=("arial", 16, "bold"),bg="#FC00C9",
                                 command=lambda: self.playgame_goto(n+1,how_many),width=24))
        # now this reloads the page with the buttons enabled but is disabled to prevent hacks
        self.next_round.grid(row=6)
        self.next_round.config(state=DISABLED)
        # this prevents round skipping
        self.hints = Button(
            self.other_frame, text="hints", font=("arial", 16, "bold"),command=lambda: hell(),width=10)
        # to be unbitched in the next patch
        self.hints.grid(row=7, column=0, padx=6, pady=5)
        self.stats = Button(self.other_frame, text="stats", font=("arial", 16, "bold"),command=lambda: stats(),width=10)
        self.stats.grid(row=7, column=1, padx=6, pady=5)
        # stats page for stats and stats


        self.suicide_switch = Button(self.game_frame, text="end game", font=("arial", 16,"bold"),
                                     fg="#FFFFFF",bg="#990000" ,command=self.end,width=24)
        self.suicide_switch.grid(row=8)
        # ends your life (by that i mean the games)

    def end(self):
        """ends self (in minecraft)"""
        root.deiconify()
        self.game_frame.destroy()
        menu()
    def answer(self, input,correct_answer,q,reqscore,score):
        """the answer"""
        print(history)
        if correct_answer >= reqscore:
            self.responce.config(text="your answer is correct")
            history.append(1)
        else:
            self.responce.config(text="your answer is incorrect")
            history.append(0)
        self.button_frame.destroy()
        self.buttons(q,DISABLED,score,reqscore)
        self.next_round.config(state=NORMAL)
    def buttons(self,q,state,score,reqscore):
        """buttons"""
        self.button_frame = Frame(self.game_frame)
        self.button_frame.grid(row=4)
        for item in [
            [lambda : self.answer(q[0],score[0],q,reqscore,score), q[0],1,2,0],
            [lambda : self.answer(q[1],score[1],q,reqscore,score), q[1],2,2,1],
            [lambda : self.answer(q[2],score[2],q,reqscore,score), q[2], 3,3,0],
            [lambda : self.answer(q[3],score[3],q,reqscore,score), q[3],4,3,1]
        ]:
            self.make_button = Button(self.button_frame,
                                     text=q[-1+item[2]], bg=item[1],
                                     fg="#FFFFFF", font=("Arial", 12, "bold"),
                                     width=12, command= item[0],state=state)
            self.make_button.grid(row=item[3], column=item[4], padx=5, pady=5)


    def playgame_goto(self,n,x):
        """nexts the round """
        if x >= n:
            self.game_frame.destroy()
            playgame(x,n)

class hell():
    """the most usless help page ever"""
    def __init__(self):
        self.frame = Toplevel()
        # i think this makes a new window
        self.grid = Frame(self.frame,padx=10,pady=10)
        self.help = Label(self.frame, text="i get it you suck at colours use a colour picker or google", font=("arial", 16,"bold"))
        self.help.grid(row=0)
class stats():
    """sure displays some stats"""
    def __init__(self):
        self.frame = Toplevel()
        # i think this makes a new window
        self.grid = Frame(self.frame,padx=10,pady=10)
        self.stats_title = Label(self.frame, text="your stats:", font=("arial", 16, "bold"))
        self.stats_title.grid(row=0,padx=200)
        if len(history)>0:
            winrate =round( history.count(1)/len(history) *100)
            self.stats_title.grid(row=0)
            l = ''
            if winrate < 50:
                l = 'we reccomend the help section'
                # rude much
            self.stats = Label(self.frame, text=f"Correct answer percentage: {winrate}%\n"
                                               f"Number of correct answers: {history.count(1)}\n"
                                               f"{l}", font=("arial", 16,"bold"))
            self.stats.grid(row=1)
        else:
            self.stats = Label(self.frame, text="no stats yet play the game", font=("arial", 16,"bold"))
            self.stats.grid(row=1)






# the fun part
# https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
# h = input('Enter hex: ').lstrip('#')
# print('RGB =', tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))
# print('#{:06x}'.format(random.randint(0, 0xFFFFFF)))
if __name__ == '__main__':
    """who knows what this does"""
    root = Tk()
    root.title("Colour Quest")
    menu()
    root.mainloop()
# while True:
#
#
#     boss_attack = ('#{:06x}'.format(random.randint(0, 0xFFFFFF)))
#     user_attack  = input()


