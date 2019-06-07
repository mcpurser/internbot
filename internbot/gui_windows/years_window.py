import base
import crosstabs
import topline
import rnc_automation
import tkinter
import os, subprocess, platform
import csv
from collections import OrderedDict


class YearsWindow(object):

    def __init__ (self, main_window, root, round):
        self.round=round
        self.__window = main_window
        self.year_window = root
        self.entry_list = []

    def packing_years(self, year_frame):
        if self.round >= 10:
            self.pack_ten_years(year_frame)
            print("Trended Topline Report will have 10 years")
        elif self.round == 9:
            self.pack_nine_years(year_frame)
            print("Trended Topline Report will have 9 years")
        elif self.round == 8:
            self.pack_eight_years(year_frame)
            print("Trended Topline Report will have 8 years")
        elif self.round == 7:
            self.pack_seven_years(year_frame)
            print("Trended Topline Report will have 7 years")
        elif self.round == 6:
            self.pack_six_years(year_frame)
            print("Trended Topline Report will have 6 years")
        elif self.round == 5:
            self.pack_five_years(year_frame)
            print("Trended Topline Report will have 5 years")
        elif self.round == 4:
            self.pack_four_years(year_frame)
            print("Trended Topline Report will have 4 years")
        elif self.round == 3:
            self.pack_three_years(year_frame)
            print("Trended Topline Report will have 3 years")
        elif self.round == 2:
            self.pack_two_years(year_frame)
            print("Trended Topline Report will have 2 years")

        self.focus_index = 0

        def down_pressed(event):
            if self.focus_index < self.round -1:
                self.focus_index+=1
                self.entry_list[self.focus_index].focus_set()

        def up_pressed(event):
            if self.focus_index > 0:
                self.focus_index-=1
                self.entry_list[self.focus_index].focus_set()

        def mouse_clicked(event):
            focus_item = self.year_window.focus_get()
            for item in range(0, int(self.round)):
                if focus_item == self.entry_list[item]:
                    self.focus_index = item
                    break

        self.year_window.bind("<Down>", down_pressed)
        self.year_window.bind("<Up>", up_pressed)
        self.year_window.bind("<Button-1>", mouse_clicked)

    def pack_two_years(self, year_frame):
        year_one_frame = tkinter.Frame(year_frame)
        year_one_label = tkinter.Label(year_one_frame, text="1st year name:")
        year_one_label.pack(side=tkinter.LEFT, expand=True)
        self.year_one_entry = tkinter.Entry(year_one_frame)
        self.year_one_entry.pack(side=tkinter.RIGHT, expand=True)
        year_one_frame.pack(side=tkinter.TOP, expand=True)
        self.entry_list.append(self.year_one_entry)
        self.year_one_entry.focus_set()

        year_two_frame = tkinter.Frame(year_frame)
        year_two_label = tkinter.Label(year_two_frame, text="2nd year name:")
        year_two_label.pack(side=tkinter.LEFT, expand=True)
        self.year_two_entry = tkinter.Entry(year_two_frame)
        self.year_two_entry.pack(side=tkinter.RIGHT, expand=True)
        year_two_frame.pack(side=tkinter.TOP, expand=True)
        self.entry_list.append(self.year_two_entry)

    def pack_three_years(self, year_frame):
        self.pack_two_years(year_frame)
        year_three_frame = tkinter.Frame(year_frame)
        year_three_label = tkinter.Label(year_three_frame, text="3rd year name:")
        year_three_label.pack(side=tkinter.LEFT, expand=True)
        self.year_three_entry = tkinter.Entry(year_three_frame)
        self.year_three_entry.pack(side=tkinter.RIGHT, expand=True)
        year_three_frame.pack(side=tkinter.TOP, expand=True)
        self.entry_list.append(self.year_three_entry)

    def pack_four_years(self, year_frame):
        self.pack_three_years(year_frame)
        year_four_frame = tkinter.Frame(year_frame)
        year_four_label = tkinter.Label(year_four_frame, text="4th year name:")
        year_four_label.pack(side=tkinter.LEFT, expand=True)
        self.year_four_entry = tkinter.Entry(year_four_frame)
        self.year_four_entry.pack(side=tkinter.RIGHT, expand=True)
        year_four_frame.pack(side=tkinter.TOP, expand=True)
        self.entry_list.append(self.year_four_entry)

    def pack_five_years(self, year_frame):
        self.pack_four_years(year_frame)
        year_five_frame = tkinter.Frame(year_frame)
        year_five_label = tkinter.Label(year_five_frame, text="5th year name:")
        year_five_label.pack(side=tkinter.LEFT, expand=True)
        self.year_five_entry = tkinter.Entry(year_five_frame)
        self.year_five_entry.pack(side=tkinter.RIGHT, expand=True)
        year_five_frame.pack(side=tkinter.TOP, expand=True)
        self.entry_list.append(self.year_five_entry)

    def pack_six_years(self, year_frame):
        self.pack_five_years(year_frame)
        year_six_frame = tkinter.Frame(year_frame)
        year_six_label = tkinter.Label(year_six_frame, text="6th year name:")
        year_six_label.pack(side=tkinter.LEFT, expand=True)
        self.year_six_entry = tkinter.Entry(year_six_frame)
        self.year_six_entry.pack(side=tkinter.RIGHT, expand=True)
        year_six_frame.pack(side=tkinter.TOP, expand=True)
        self.entry_list.append(self.year_six_entry)

    def pack_seven_years(self, year_frame):
        self.pack_six_years(year_frame)
        year_seven_frame = tkinter.Frame(year_frame)
        year_seven_label = tkinter.Label(year_seven_frame, text="7th year name:")
        year_seven_label.pack(side=tkinter.LEFT, expand=True)
        self.year_seven_entry = tkinter.Entry(year_seven_frame)
        self.year_seven_entry.pack(side=tkinter.RIGHT, expand=True)
        year_seven_frame.pack(side=tkinter.TOP, expand=True)
        self.entry_list.append(self.year_seven_entry)

    def pack_eight_years(self, year_frame):
        self.pack_seven_years(year_frame)
        year_eight_frame = tkinter.Frame(year_frame)
        year_eight_label = tkinter.Label(year_eight_frame, text="8th year name:")
        year_eight_label.pack(side=tkinter.LEFT, expand=True)
        self.year_eight_entry = tkinter.Entry(year_eight_frame)
        self.year_eight_entry.pack(side=tkinter.RIGHT, expand=True)
        year_eight_frame.pack(side=tkinter.TOP, expand=True)
        self.entry_list.append(self.year_eight_entry)

    def pack_nine_years(self, year_frame):
        self.pack_eight_years(year_frame)
        year_nine_frame = tkinter.Frame(year_frame)
        year_nine_label = tkinter.Label(year_nine_frame, text="9th year name:")
        year_nine_label.pack(side=tkinter.LEFT, expand=True)
        self.year_nine_entry = tkinter.Entry(year_nine_frame)
        self.year_nine_entry.pack(side=tkinter.RIGHT, expand=True)
        year_nine_frame.pack(side=tkinter.TOP, expand=True)
        self.entry_list.append(self.year_nine_entry)

    def pack_ten_years(self, year_frame):
        self.pack_nine_years(year_frame)
        year_ten_frame = tkinter.Frame(year_frame)
        year_ten_label = tkinter.Label(year_ten_frame, text="10th year name:")
        year_ten_label.pack(side=tkinter.LEFT, expand=True)
        self.year_ten_entry = tkinter.Entry(year_ten_frame)
        self.year_ten_entry.pack(side=tkinter.RIGHT, expand=True)
        year_ten_frame.pack(side=tkinter.TOP, expand=True)
        self.entry_list.append(self.year_ten_entry)

    def read_years(self):
        years = []
        if (self.round >= 10):
            self.pull_ten_years(years)
        elif (self.round == 9):
            self.pull_nine_years(years)
        elif (self.round == 8):
            self.pull_eight_years(years)
        elif (self.round == 7):
            self.pull_seven_years(years)
        elif (self.round == 6):
            self.pull_six_years(years)
        elif (self.round == 5):
            self.pull_five_years(years)
        elif (self.round == 4):
            self.pull_four_years(years)
        elif (self.round == 3):
            self.pull_three_years(years)
        elif (self.round == 2):
            self.pull_two_years(years)
        self.year_window.destroy()
        return years

    def pull_ten_years(self, years):
        years.append(self.year_ten_entry.get())
        self.pull_nine_years(years)

    def pull_nine_years(self, years):
        years.append(self.year_nine_entry.get())
        self.pull_eight_years(years)

    def pull_eight_years(self, years):
        years.append(self.year_eight_entry.get())
        self.pull_seven_years(years)

    def pull_seven_years(self, years):
        years.append(self.year_seven_entry.get())
        self.pull_six_years(years)

    def pull_six_years(self, years):
        years.append(self.year_six_entry.get())
        self.pull_five_years(years)

    def pull_five_years(self, years):
        years.append(self.year_five_entry.get())
        self.pull_four_years(years)

    def pull_four_years(self, years):
        years.append(self.year_four_entry.get())
        self.pull_three_years(years)

    def pull_three_years(self, years):
        years.append(self.year_three_entry.get())
        self.pull_two_years(years)

    def pull_two_years(self, years):
        years.append(self.year_two_entry.get())
        years.append(self.year_one_entry.get())