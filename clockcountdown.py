
#!/usr/bin/env python3
# Display a countdown clock
# Useful for workshops.
# Can be used as a live countdown clock with OBS for on-line events.
# Specify the number of minutes, as a command line argument.
# Tested on MS-Windows. Remove winsound if you want to use it on Mac or Linux OS. 
# (c) Rudiger Wolf 2020-11-09
# https://github.com/rnwolf/pyclockcountdown
# 

import sys
import tkinter as tk
import winsound

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle_arc = _create_circle_arc


class Count_down_App(tk.Tk):
    def __init__(self,seconds):
        tk.Tk.__init__(self)
        self.width = 800
        self.height = 350
        self.geometry("800x450") 
        self.resizable(False,False)
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.label_text = tk.StringVar()
        self.label_text.set("")
        self.label = tk.Label(self, text=self.label_text, width=10,anchor='sw')
        self.canvas.pack(fill="both",expand=False)
        self.label.pack()
        self.remaining = 0
        self.starting = seconds
        self.countdown(self.starting)

    def countdown(self, remaining = None):
        self.label.config(font=("Arial", 64))
        self.canvas.create_circle(self.width/3, self.height/4*2, (self.height/4*2), fill="blue", outline="#DDD", width=4)
        self.canvas.create_circle_arc(self.width/3, self.height/4*2, (self.height/4*2-4), 
                fill="red", 
                outline="", 
                start=(0+90), 
                end=(360/self.starting*(self.starting-self.remaining)+90))
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.canvas.create_circle(self.width/3,  self.height/4*2, (self.height/4*2), fill="red", outline="#DDD", width=4)
            self.label.configure(text="time's up!")
            # Probably play Windows default sound, if any is registered (because
            # "*" probably isn't the registered name of any sound).
            winsound.PlaySound("*", winsound.SND_ALIAS)
            #sys.stdout.write('\a')  # Make a beep in a cross platform way.
        else:
            mins,secs = divmod(self.remaining,60)
            #self.label_text.set("{min:2}:{secs:2}")
            labelstr=f"{mins:02d}:{secs:02d}"
            self.title("Countdown "+labelstr)     # Add a title
            self.label.configure(text=labelstr )  #"%d" % secs ) #self.remaining )
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("""
        Specify how many minutes to countdown for.
        Example:

        python clockcountdown.py 10

        Will start a 10 minute countdown timer.
        If no number is provided then 5 minutes is assumed to be the default.
        Minimize timer window to pause it.
        """)
    if len(sys.argv) == 2:
        minutes = int(sys.argv[1:][0])
    else:
        minutes = 5 # Default is 5 minutes if none is specified.
    seconds = minutes * 60
    app = Count_down_App(seconds)
    app.mainloop()
