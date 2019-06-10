from tkinter import *


class EntryWithPlaceholder(Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", width=5, sv=NONE, color='black'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.placeholder_width = width
        self.default_fg_color = self['fg']
        self.sv = sv

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()
        self.data = self.get()

    def put_placeholder(self):
        # self.placeholder = "\n".join([self.placeholder[i:i+28] for i in range(0, len(self.placeholder), 28)])
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color
        self['width'] = self.placeholder_width
        self['justify'] = CENTER
        self['textvariable'] = self.sv

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

    def entryValue(self):
        print (self.data)
