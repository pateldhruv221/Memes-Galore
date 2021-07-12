
# imports
from praw import Reddit
from requests import get
from cv2 import imdecode, imwrite, IMREAD_COLOR
import numpy as np
from random import randint
from tkinter import *
from PIL import Image, ImageTk

# initial tkinter setup
root = Tk()
root.title("Memes Galore")
root.geometry("450x700")
root.configure(background="white")
# root.state("zoomed")

# access info for Reddit API
creds = {
    "client_id": "ZmS20ZTchg2LJA",
    "client_secret": "fH0yRW0VI8MBNEwUANSkw8J_jttAsA",
    "user_agent": "MyAPI/0.0.1",
    "username": "No-Wallaby-3076",
    "password": "yBG3e2bNU?Gfgu5"
}

reddit = Reddit(client_id=creds['client_id'],
                    client_secret=creds['client_secret'],
                    user_agent=creds['user_agent'],
                    username=creds['username'],
                    password=creds['password'])

# accessing Reddit API and wholesomememes subreddit
subreddit = reddit.subreddit("wholesomememes")

posts = []
for post in subreddit.hot():
    if "jpg" in post.url.lower() or "png" in post.url.lower():
        posts.append(post)

# getting an initial random post
random_post_number = randint(0, len(posts)-1)
random_post = posts[random_post_number]

# extracting its image into a separate png file
resp = get(random_post.url.lower(), stream=True).raw
image = np.asarray(bytearray(resp.read()), dtype="uint8")
image = imdecode(image, IMREAD_COLOR)
imwrite(f"./random_pic.png", image)

# populating GUI with necessary widgets
main_frame = Frame(root,bg="white")
title_label = Label(main_frame,text="MEMES GALORE",font=("Gothic", 36),bg="white")

random_image = Image.open("./random_pic.png")
random_image = random_image.resize((364,412),Image.ANTIALIAS) # set to 68%, 100% = 536x607
temp_img = ImageTk.PhotoImage(random_image)
random_image_label = Label(main_frame,image=temp_img,borderwidth=0,highlightthickness=0,bg="white")

# placing the widgets in their appropriate locations
main_frame.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.9)
title_label.place(relx=0,rely=0,relwidth=1,relheight=0.1)
random_image_label.place(relx=0,rely=0.1,relwidth=1,relheight=0.8)

# action to execute when button is pressed
def get_new_image():
    global random_post_number, random_post, resp, image, random_image, new_img, random_image_label

    random_post_number = randint(0, len(posts)-1)
    random_post = posts[random_post_number]

    resp = get(random_post.url.lower(), stream=True).raw
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = imdecode(image, IMREAD_COLOR)
    imwrite(f"./random_pic.png", image)

    random_image = Image.open("./random_pic.png")
    random_image = random_image.resize((364,412),Image.ANTIALIAS) # set to 68%, 100% = 536x607
    new_img = ImageTk.PhotoImage(random_image)

    random_image_label.configure(image=new_img)
    random_image_label.image = new_img

# creating and placing button widget
button = Button(main_frame, text="Get a new meme!",command=get_new_image)
button.place(relx=0,rely=0.9,relwidth=1,relheight=0.1)

# running GUI
root.mainloop()
