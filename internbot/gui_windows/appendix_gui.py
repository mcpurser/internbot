import base
import crosstabs
import topline
import rnc_automation
import tkinter
from tkinter import messagebox
from tkinter import filedialog
import os, subprocess, platform
import csv
from collections import OrderedDict
import threading
import sys
import time

class AppendixView(object):

    def __init__(self, main_window, mov_x, mov_y, window_width, window_height, header_font, header_color, bot_render):
        self.__window = main_window
        self.mov_x = mov_x
        self.mov_y = mov_y
        self.window_width = window_width
        self.window_height = window_height
        self.header_font = header_font
        self.header_color = header_color
        self.fpath = os.path.join(os.path.expanduser("~"), "Desktop")
        self.__embedded_fields = []
        self.bot_render = bot_render

    def append_menu(self):
        """
        Function sets up Topline Appendix menu.
        :return: None
        """
        self.redirect_window=tkinter.Toplevel(self.__window)
        self.redirect_window.withdraw()
        width=200
        height=300

        self.redirect_window.geometry("%dx%d+%d+%d" % (width,height,self.mov_x + self.window_width / 2 - width / 2, self.mov_y + self.window_height / 2 - height / 2))
        self.redirect_window.title("Y2 Topline Appendix Report Automation")
        message = "Please open a .csv file \nwith open ended responses."
        tkinter.Label(self.redirect_window, text=message, font=self.header_font, fg=self.header_color).pack(expand=True, pady=5)
        btn_open = tkinter.Button(self.redirect_window, text="Open", command=self.append_type, height=3, width=20)
        btn_cancel = tkinter.Button(self.redirect_window, text="Cancel", command=self.redirect_window.destroy, height=3,
                                    width=20)
        btn_bot = tkinter.Button(self.redirect_window, image=self.bot_render, borderwidth=0,
                                 highlightthickness=0, relief=tkinter.FLAT, bg="white", height=65, width=158,
                                 command=self.appendix_help_window)
        btn_bot.pack(side=tkinter.TOP, padx=10, pady=5)
        btn_cancel.pack(side=tkinter.BOTTOM, padx=10, pady=5)
        btn_open.pack(side=tkinter.BOTTOM, padx=10, pady=5)

        self.redirect_window.deiconify()

    def appendix_help_window(self):
        """
        Funtion sets up help window to give the user info about round numbers.
        :return: None
        """
        help_window = tkinter.Toplevel(self.__window)
        help_window.withdraw()
        width = 250
        height = 400
        help_window.geometry("%dx%d+%d+%d" % (
            width, height, self.mov_x + self.window_width / 2 - width / 2,
            self.mov_y + self.window_height / 2 - height / 2))
        message = "\nAppendix Help"
        tkinter.Label(help_window, text=message, font=self.header_font, fg=self.header_color).pack(side=tkinter.TOP,
                                                                                                   padx=10)
        info_message = "Open a .csv file containing open ends\n" \
                       "Column names should include:\n"\
                       "variable = question name\n" \
                       "prompt = question asked\n" \
                       "label = response from user\n" \
                       "\nThen choose if you would like to\n" \
                       "create a .docx or .xlsx appendix\n" \
                       "(Most clients need .docx)"

        tkinter.Label(help_window, text=info_message, justify=tkinter.LEFT).pack(side=tkinter.TOP)
        btn_ok = tkinter.Button(help_window, text="Ok", command=help_window.destroy, height=3, width=20)
        btn_ok.pack(padx=5, pady=10, side=tkinter.TOP, expand=False)
        help_window.deiconify()

        def enter_pressed(event):
            help_window.destroy()

        help_window.bind("<Return>", enter_pressed)
        help_window.bind("<KP_Enter>", enter_pressed)

    def append_type(self):
        """
        Funtion asks the user if they would like to create a .docx or a .xlsx
        :return: None
        """
        self.choose_window = tkinter.Toplevel(self.__window)
        self.choose_window.withdraw()
        width = 250
        height = 250
        self.choose_window.geometry("%dx%d+%d+%d" % (
            width, height, self.mov_x + self.window_width / 2 - width / 2,
            self.mov_y + self.window_height / 2 - height / 2))
        message = "Choose the format of\nyour appendix report"
        tkinter.Label(self.choose_window, text=message, font=self.header_font, fg=self.header_color).pack(expand=True)
        btn_doc = tkinter.Button(self.choose_window, text="Word Appendix", command=self.doc_appendix,
                                     height=3, width=20)

        btn_excel = tkinter.Button(self.choose_window, text="Excel Appendix",
                                   command=self.excel_appendix, height=3, width=20)
        btn_cancel = tkinter.Button(self.choose_window, text="Cancel",
                                   command=self.choose_window.destroy, height=3, width=20)

        btn_cancel.pack(ipadx=5, side=tkinter.BOTTOM, expand=False)
        btn_excel.pack(ipadx=5, side=tkinter.BOTTOM, expand=False)
        btn_doc.pack(ipadx=5, side=tkinter.BOTTOM, expand=False)
        self.choose_window.deiconify()





    def doc_appendix(self):
        generator = topline.Appendix.AppendixGenerator()
        csvfilename = filedialog.askopenfilename(initialdir=self.fpath, title="Select open ends file",
                                                   filetypes=(("Comma separated files", "*csv"), ("all files", "*.*")))
        if csvfilename is not "":
            generator.parse_file(csvfilename)
            savedirectory = filedialog.asksaveasfilename(defaultextension='.docx', filetypes=[('word files', '.docx')])
            if savedirectory is not "":
                thread_worker = threading.Thread(target=self.doc_appendix_worker, args=(generator, savedirectory))
                thread_worker.start()
            self.redirect_window.destroy()

    def doc_appendix_worker(self, generator, savedirectory):
        """
        Funtion is called as worker thread to generate the report and open the finished file for the user.
        :param generator: topline.Appendix.AppendixGenerator
        :param savedirectory: string indicating the filename for the file from the user
        :return: None
        """
        generator.write_appendix(savedirectory, "/Library/internbot/1.0.0/templates_images/appendix_template.docx", False)
        self.open_file_for_user(savedirectory)

    def excel_appendix(self):
        generator = topline.Appendix.AppendixGenerator()
        csvfilename = filedialog.askopenfilename(initialdir=self.fpath, title="Select open ends file",
                                                   filetypes=(("Comma separated files", "*csv"), ("all files", "*.*")))
        if csvfilename is not "":
            is_y2 = messagebox.askquestion('Appendix Style','Is this a Y2 style appendix?')
            if is_y2 == 'yes':
                is_qualtrics =False
            else:
                is_qualtrics=True
            generator.parse_file(csvfilename, is_qualtrics)
            savedirectory = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[('excel files', '.xlsx')])
            if savedirectory is not "":
                thread_worker = threading.Thread(target=self.excel_appendix_worker, args=(generator, savedirectory))
                thread_worker.start()

            self.redirect_window.destroy()

    def excel_appendix_worker(self, generator, savedirectory):
        """
        Funtion is called as worker thread to generate the report and open the finished file for the user.
        :param generator: topline.Appendix.AppendixGenerator
        :param savedirectory: string indicating the filename for the file from the user
        :return: None
        """
        generator.write_appendix(savedirectory, '', True)
        self.open_file_for_user(savedirectory)



    def open_file_for_user(self, file_path):
        try:
            if os.path.exists(file_path):
                if platform.system() == 'Darwin':  # macOS
                    subprocess.call(('open', file_path))
                elif platform.system() == 'Windows':  # Windows
                    os.startfile(file_path)
            else:
                messagebox.showerror("Error", "Error: Could not open file for you \n"+file_path)
        except IOError:
            messagebox.showerror("Error", "Error: Could not open file for you \n" + file_path)
