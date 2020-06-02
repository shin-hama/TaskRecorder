import tkinter as Tk


STATUS_TEXT = ['waiting..', 'processing']


class Button(Tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

        self.status_text = Tk.StringVar()
        self.status_text.set(STATUS_TEXT[0])
        self.status = Tk.Label(master, textvariable=self.status_text,
                               borderwidth=2, relief='groove')
        self.status.pack(side=Tk.BOTTOM, fill=Tk.X)

    def create_widgets(self):
        self.hi_there = Tk.Button(self)
        self.hi_there['text'] = 'test'
        self.hi_there['command'] = self.process
        self.hi_there.pack(side='top')

    def process(self):
        for text in STATUS_TEXT:
            if not self.status_text.get() == text:
                self.status_text.set(text)
                break


def main():

    root = Tk.Tk()
    root.title('Hello World!')
    # window size + window position
    root.geometry('400x300+1000+10')

    button = Button(master=root)

    button.mainloop()


if __name__ == "__main__":
    main()
