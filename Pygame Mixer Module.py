from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pygame import mixer
from PIL import Image,ImageTk

def songpause(x,y):
    mixer.music.pause()
    x['state']="disabled"
    y['state']='active'

def songplay(x,y):
    mixer.music.unpause()
    x['state']='disabled'
    y['state']='active'


class Marquee(Canvas):
    def __init__(self, parent, text, margin=2, borderwidth=1, relief='flat', fps=30,width=80):
        Canvas.__init__(self, parent, borderwidth=borderwidth, relief=relief)
        self.fps = fps

        # start by drawing the text off screen, then asking the canvas
        # how much space we need. Use that to compute the initial size
        # of the canvas. 
        text = self.create_text(0, -1000, text=text, anchor="w", tags=("text",),font=('BentonSans Comp Regular',12))
        (x0, y0, x1, y1) = self.bbox("text")
        width = (x1 - x0) + (2*margin) + (2*borderwidth)
        height = (y1 - y0) + (2*margin) + (2*borderwidth)
        self.configure(width=width, height=height)

        # start the animation
        self.animate()

    def animate(self):
        (x0, y0, x1, y1) = self.bbox("text")
        if x1 < 0 or y0 < 0:
            # everything is off the screen; reset the X
            # to be just past the right margin
            x0 = self.winfo_width()
            y0 = int(self.winfo_height()/2)
            self.coords("text", x0, y0)
        else:
            self.move("text", -1, 0)

        # do again in a few milliseconds
        self.after_id = self.after(int(1000/self.fps), self.animate)

def volumecontrol(event):
    global slider
    x=slider.get()
    print(x)
    x=x/100
    mixer.music.set_volume(x)
    
    
    
def songchoose(z):
    global marquee
    a=filedialog.askopenfilename(defaultextension='.mp3',filetypes=[("MP3", '.mp3'),("WAV", '.wav')])
    if a!='':
        x=a.split("/")
        x=x[-1]
        y=x.split('.')
        y=y[0]
        marquee.destroy()
        marquee = Marquee(root, text=y, borderwidth=1, relief="sunken")
        marquee.place(x=20,y=10)
        mixer.init()
        mixer.music.load(a)
        mixer.music.play()
        slider['state']='active'
        slider.set(100)

root = Tk()
root.geometry('200x130+550+300')
root.title('SongPlayer')
root.resizable(False,False)
root.iconbitmap('icon.ico')
x= Image.open('playbutton.jpg')
x = x.resize((25,25))
x = ImageTk.PhotoImage(x)
y= Image.open('pausebutton.png')
y = y.resize((25,25))
y = ImageTk.PhotoImage(y)
marquee = Marquee(root, text="Choose a Song", borderwidth=1, relief="sunken")
marquee.place(x=55,y=10)
a=Button(root,text="Choose Song To Play",font=('American Captain',10))
a.place(x=50,y=57)
b=Button(root,image=x, state='disabled')
b.place(x=10,y=53)
c=Button(root,image=y)
c.place(x=160,y=53)
slider = ttk.Scale(root,from_=0,to=100,orient='horizontal',command = volumecontrol,state='disabled')
slider.place(x=55,y=90)
a.config(command=lambda:songchoose(a))
b.config(command=lambda:songplay(b,c))
c.config(command=lambda:songpause(c,b))

root.mainloop()
