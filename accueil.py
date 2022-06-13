from tkinter import *
import tkinter as tk, threading
import imageio
from PIL import Image, ImageTk

video_name = "skull.mp4" #This is your video file path
video = imageio.get_reader(video_name)

def stream(label):

    for image in video.iter_data():
        frame_image = ImageTk.PhotoImage(Image.fromarray(image).resize((1100,1050)))
        label.config(image=frame_image)
        label.image = frame_image

if __name__ == "__main__":

    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.config(background = 'black')

    welcometitle = Label(root, bg = "black", text = "Are you ready to be hanged ?", font = ("goudy stout", 46),  fg = "yellow",  height = 2)
    welcometitle.pack(side = TOP, fill = "both", expand = True)


    frame_menu = Frame(root, borderwidth=0, bg="black")
    frame_menu.pack(side = LEFT, fill = "both", padx = 200)

    my_label = tk.Label(root, borderwidth=0, highlightthickness = 0)
    my_label.pack(side = LEFT)

    butplay = Button(frame_menu, bg = 'black',font = ("goudy stout", 12), fg = "yellow", text = "PLAY", height = 5, width = 10)
    butplay.pack(pady = 40)

    butlevel = Button(frame_menu,bg = 'black',font = ("goudy stout", 12), fg = "green", text = "LEVEL", height = 5, width = 10)
    butlevel.pack(pady = 40)

    butrules = Button(frame_menu, bg = 'black',font = ("goudy stout", 12), text = "RULES", fg = "red", height = 5, width = 10)
    butrules.pack(pady = 40)

    butquit = Button(frame_menu, bg = 'black',font = ("goudy stout", 12), text = "EXIT", fg = "orange", height = 5, width = 10)
    butquit.pack(pady = 40)

    thread = threading.Thread(target=stream, args=(my_label,))
    thread.daemon = 1
    thread.start()

root.mainloop()