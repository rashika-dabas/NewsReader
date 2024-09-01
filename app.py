import requests
import io
import webbrowser

from tkinter import *
from urllib.request import urlopen
from PIL import ImageTk, Image


def open_link(url):
    webbrowser.open(url)


class NewsApp:

    def __init__(self):
        self.root = Tk()

        # Fetch data
        self.data = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=d297edec26b4432d9dd992854334ca9b').json()

        # Load GUI
        self.load_gui()
        self.root.title('News Reader')

        # Add favicon
        self.root.iconbitmap('favicon.ico')

        # Load news
        self.load_news_item(0)

    def load_gui(self):
        self.root.geometry('350x500')
        self.root.resizable(True, True)
        self.root.configure(background='black')

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def load_news_item(self, index):
        self.clear()

        # Image
        try:
            img_url = self.data['articles'][index]['urlToImage']
            raw = urlopen(img_url).read()
            img = Image.open(io.BytesIO(raw)).resize((350, 200))
            photo = ImageTk.PhotoImage(img)

        except:
            img = Image.open('news.jpg')
            img_size = img.resize((100, 100))
            photo = ImageTk.PhotoImage(img_size)

        label = Label(self.root, image=photo)
        label.pack()

        # Heading
        heading = Label(self.root, text=self.data['articles'][index]['title'], bg='black', fg='white', justify='center', wraplength=350)
        heading.pack(pady=(10, 20))
        heading.config(font=('verdana', 15))

        # Description
        desc = Label(self.root, text=self.data['articles'][index]['description'], bg='black', fg='white', justify='center', wraplength=350)
        desc.pack(pady=(3, 20))
        desc.config(font=('verdana', 10))

        # Buttons
        frame = Frame(self.root, bg='black')
        frame.pack(expand=True, fill=BOTH)
        if index != 0:
            prev = Button(frame, text='Previous', width=16, height=3, command=lambda: self.load_news_item(index - 1))
            prev.pack(side=LEFT)

        read = Button(frame, text='Read More', width=16, height=3, command=lambda: open_link(self.data['articles'][index]['url']))
        read.pack(side=LEFT)

        if index != 19:
            nxt = Button(frame, text='Next', width=16, height=3, command=lambda: self.load_news_item(index + 1))
            nxt.pack(side=RIGHT)

        self.root.mainloop()


obj = NewsApp()
