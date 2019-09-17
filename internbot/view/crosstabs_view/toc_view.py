## outside modules
import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView, FileChooserIconView

import os
import io
from contextlib import redirect_stdout


class TOCView(BoxLayout):

    def __init__(self, **kwargs):
        super(TOCView, self).__init__(**kwargs)

        self.open_file_path = ''
        self.navigated_path = os.path.expanduser("~")
        self.save_file_path = ''

        self.open_file_prompt = self.create_open_file_prompt()
        self.open_file_dialog = self.create_open_file_dialog()
        self.save_file_prompt = self.create_save_file_prompt()
        self.save_file_dialog = self.create_save_file_dialog()

    def create_open_file_prompt(self):
        label = Label(text="Choose Qualtrics survey file (.qsf) for project")
        label.font_family= "Y2"

        popup = Popup(title="Select survey file",
        content=label,
        size_hint=(.7, .5), pos_hint={'center_x': 0.5, 'center_y': 0.5},
        on_dismiss=self.open_file_prompt_to_dialog)

        return popup

    def create_open_file_dialog(self):
        chooser = BoxLayout()
        container = BoxLayout(orientation='vertical')

        def open_file(path, filename):
            try:
                filepath = os.path.join(path, filename[0])
                path, ext = os.path.splitext(filepath)
                if ext != ".qsf":
                    self.error_message("Please pick a survey (.qsf) file")
                else:
                    self.open_file_path = filepath
                    self.navigated_path = path
                    self.open_file_dialog_to_prompt()
            except IndexError:
                self.error_message("Please pick a survey (.qsf) file")

        filechooser = FileChooserListView()
        filechooser.path = os.path.expanduser("~")
        filechooser.bind(on_selection=lambda x: filechooser.selection)
        filechooser.show_hidden = False

        open_btn = Button(text='open', size_hint=(.2,.1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        open_btn.bind(on_release=lambda x: open_file(filechooser.path, filechooser.selection))

        container.add_widget(filechooser)
        container.add_widget(open_btn)
        chooser.add_widget(container)

        file_chooser = Popup(title='Open file',
        content=chooser,
        size_hint=(.9, .7 ), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        return file_chooser 

    def create_save_file_prompt(self):
        label = Label(text="Choose a file location and name for QResearch table of contents file.")
        label.font_family= "Y2"

        popup = Popup(title="Select save file location",
        content=label,
        size_hint=(.7, .5), pos_hint={'center_x': 0.5, 'center_y': 0.5},
        on_dismiss=self.save_file_prompt_to_dialog)

        return popup

    def create_save_file_dialog(self):
        chooser = BoxLayout()
        container = BoxLayout(orientation='vertical')

        filechooser = FileChooserIconView()
        filechooser.path = self.navigated_path
        filechooser.show_hidden = False

        container.add_widget(filechooser)

        def save_file(path, filename):
            self.save_file_path = os.path.join(path, filename)
            self.finish()

        button_layout = BoxLayout()
        button_layout.size_hint = (1, .1)
        file_name = TextInput(text="File name.xlsx")
        button_layout.add_widget(file_name)

        save_btn = Button(text='save', size_hint=(.2,1))
        save_btn.bind(on_release=lambda x: save_file(filechooser.path, file_name.text))

        button_layout.add_widget(save_btn)
        container.add_widget(button_layout)
        chooser.add_widget(container)

        file_chooser = Popup(title='Save TOC file',
        content=chooser,
        size_hint=(.9, .7 ), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        return file_chooser

    def run(self, survey_builder, toc_builder):
        self.survey_builder = survey_builder
        self.toc_builder = toc_builder
        self.open_file_prompt.open()

    def open_file_prompt_to_dialog(self, instance):
        self.open_file_dialog.open()

    def open_file_dialog_to_prompt(self):
        self.open_file_dialog.dismiss()
        self.save_file_prompt.open()

    def save_file_prompt_to_dialog(self, instance):
        self.save_file_dialog.open()

    def finish(self):
        self.save_file_dialog.dismiss()

        self.terminal_popup = Popup(title = "Compiling table of contents", auto_dismiss=False)
        self.terminal_popup.size_hint=(.7, .5)
        self.terminal_popup.pos_hint={'center_x': 0.5, 'center_y': 0.5}

        content_box = BoxLayout(orientation ='vertical')

        terminal_verbatim = Label()
        content_box.add_widget(terminal_verbatim)
        
        button_layout = BoxLayout()
        save_btn = Button(text='Save terminal log', size_hint=(.2, .1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        save_btn.bind(on_press=lambda x: self.save_log(terminal_verbatim.text))
        close_btn = Button(text = 'Close', size_hint=(.2, .1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        close_btn.bind(on_press=self.close_terminal)

        button_layout.add_widget(save_btn)
        button_layout.add_widget(close_btn)

        self.terminal_popup.add_widget(button_layout)

        self.terminal_popup.open()

        f = io.StringIO()
        with redirect_stdout(f):
            self.build_toc()

        terminal_verbatim.text=f.getvalue()

    def error_message(self, error):
        label = Label(text=error)
        label.font_family= "Y2"

        popup = Popup(title="Something Went Wrong",
        content=label,
        size_hint=(.5, .8), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        popup.open()

    def build_toc(self):
        survey = self.survey_builder.compile(self.open_file_path)
        self.toc_builder.compile_toc(survey, self.save_file_path)

    def save_log(self, log_text):
        pass

    def close_terminal(self, instance):
        self.terminal_popup.dismiss()
