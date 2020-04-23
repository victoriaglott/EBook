import pandas as pd

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import pandas as pd
import time
import Tkinter as tk
import ttk
from Tkinter import *
import os
import pandas as pd
import matplotlib.pyplot as plt
import os.path
import sys
import numpy as np
from PIL import ImageTk,Image


LARGE_FONT= ("Verdana", 50)


class App(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "E-Book")

        self.frames = {}

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames["MainPage"] = MainPage(parent=container, controller=self)
        self.show_frame("MainPage")

    def show_frame(self, page_name):
        #frame = StartPage(self, container, csv_file)
        frame = self.frames[page_name]
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()


class MainPage(tk.Frame):


    def display_consequence_page(self, Alt):
        self.textBox.delete('1.0', tk.END)
        self.textBox.insert(tk.END, self.consequence)
        i = self.cons_df['Image'][self.cons_df['PositiveCons'] == self.consequence].values
        if i.size != 0:
            i = Image.open(self.PATH + str(i[0]))
            i = i.resize((400, 300))
            self.img = ImageTk.PhotoImage(i)
            self.panel.config(image = self.img)
        if Alt == 1:
            self.Alt1Btn.config(text='Next')
            self.Alt2Btn.pack_forget()
        else:
            self.Alt2Btn.config(text='Next')
            self.Alt1Btn.pack_forget()
        #self.Alt2Btn.config(text='Next')
        del self.cons_queue[self.consequence]

    def display_main_page(self):
        print(self.curr_box_index)
        self.curr_box_index = int(self.curr_box_index)
        self.alt1Text = self.df['Alt1'][self.curr_box_index]
        self.alt2Text = self.df['Alt2'][self.curr_box_index]
        self.Text = self.df['Text'][self.curr_box_index]
        self.Alt1Btn.config(text=self.alt1Text)
        self.Alt2Btn.config(text=self.alt2Text)
        self.textBox.delete('1.0', tk.END)
        self.textBox.tag_configure("center", justify='center')
        self.textBox.insert(tk.END, self.Text)
        self.textBox.tag_add("center", "1.0", "end")
        if self.df['Image'][self.curr_box_index] is not np.nan:
            i = Image.open(self.PATH + str(self.df['Image'][self.curr_box_index]))
            i = i.resize((400, 300))
            self.img = ImageTk.PhotoImage(i)
            self.panel.config(image = self.img)

    def finished(self):
        self.destroy()

    def alt1Btn(self, event):
        self.add_consequence(1)
        #print(self.curr_box_index)
        if self.display_consequence():
            self.display_consequence_page(1)
        else:
            self.increment_consequence()
            self.Alt2Btn.pack(side = 'right', fill = X, expand = 1)
            self.curr_box_index = self.df['Alt1_Index'][self.curr_box_index]
            if self.curr_box_index == 'Finish':
                print('Finish')
                self.finished()
            else:
                self.display_main_page()


    def alt2Btn(self, event):

        self.add_consequence(2)
        print(self.curr_box_index)
        if self.display_consequence():
            self.display_consequence_page(2)
        else:
            self.increment_consequence()
            self.Alt1Btn.pack(side = 'left', fill = X, expand = 1)
            self.curr_box_index = self.df['Alt2_Index'][self.curr_box_index]
            if self.curr_box_index == 'Finish':
                print('Finish')
                self.finished()
            else:
                self.display_main_page()

    def increment_consequence(self):
        for key, values in self.cons_queue.items():
            self.cons_queue[key] -= 1

    def display_consequence(self):
        for key, values in self.cons_queue.items():
            if values == 0:
                self.consequence = key
                return True
        return False

    def add_consequence(self, Alt):
        if np.isnan(self.df['Cons1'][self.curr_box_index]) == False:
            Cons_idx = int(self.df['Cons' + str(Alt)][self.curr_box_index])
            probAlt1 = self.df['ConsProb1'][self.curr_box_index]
            probAlt2 = self.df['ConsProb2'][self.curr_box_index]
            Resulting_Cons = np.random.choice(np.arange(0, 2), p=[probAlt1, probAlt2])
            if Resulting_Cons == 0:
                self.cons_queue[self.cons_df['PositiveCons'][Cons_idx]] = 2
            else:
                self.cons_queue[self.cons_df['NegativeCons'][Cons_idx]] = 2





    def __init__(self, parent, controller):

        self.PATH = "/Users/eier/Documents/PraktiskProsjektledelse/"

        self.df = pd.read_csv(self.PATH + 'History.csv')
        self.cons_df = pd.read_csv(self.PATH + 'Konsekvenser.csv')
        self.curr_box_index = 0
        self.cons_queue = {}
        self.controller = controller
        self.alt1Text = self.df['Alt1'][self.curr_box_index]
        self.alt2Text = self.df['Alt2'][self.curr_box_index]
        self.Text = self.df['Text'][self.curr_box_index]

        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text="")
        self.label.pack(pady=10,padx=10)

        self.textBox = tk.Text(self, height = 10, width = 500)
        self.textBox.tag_configure("center", justify='center')
        self.textBox.insert(tk.END, self.Text)
        self.textBox.tag_add("center", "1.0", "end")
        self.textBox.pack()

        i = Image.open(self.PATH + str(self.df['Image'][self.curr_box_index]))
        i = i.resize((400, 300))
        self.img = ImageTk.PhotoImage(i)

        self.panel = tk.Label(self, image = self.img)
        self.panel.pack(side = 'top', fill = X, expand = True)

        self.Alt1Btn = ttk.Button(self, text=self.alt1Text,
                                  command=lambda: self.controller.show_frame('MainPage'))

        self.Alt1Btn.pack(side = 'left', fill = X, expand = 1)
        self.Alt1Btn.bind("<Button-1>", self.alt1Btn)

        self.Alt2Btn = ttk.Button(self, text=self.alt2Text,
                                  command=lambda: self.controller.show_frame('MainPage'))
        self.Alt2Btn.pack(side = 'right', fill = X, expand = 1)
        self.Alt2Btn.bind("<Button-1>", self.alt2Btn)

app = App()
app.geometry('900x600')
app.mainloop()
