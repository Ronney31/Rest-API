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

#
# class scrollTxtArea:
#     def __init__(self, root):
#         frame = Frame(root)
#         frame.pack()
#         self.textPad(frame)
#         return
#
#     def textPad(self, frame):
#         # add a frame and put a text area into it
#         textPad = Frame(frame)
#         self.text = Text(textPad, height=50, width=90)
#
#         # add a vertical scroll bar to the text area
#         scroll = Scrollbar(textPad)
#         self.text.configure(yscrollcommand=scroll.set)
#
#         # pack everything
#         self.text.pack(side=LEFT)
#         scroll.pack(side=RIGHT, fill=Y)
#         textPad.pack(side=TOP)
#         return
#
#
# def main():
#     root = Tk()
#     foo = scrollTxtArea(root)
#     root.title('TextPad With a Vertical Scroll Bar')
#     root.mainloop()
#
#
# main()

#
# class SampleApp(Tk):
#     def __init__(self, *args, **kwargs):
#         Tk.__init__(self, *args, **kwargs)
#         lb = Listbox(self)
#         lb.insert("end", "one")
#         lb.insert("end", "two")
#         lb.insert("end", "three")
#         lb.bind("<Double-Button-1>", self.OnDouble)
#         lb.pack(side="top", fill="both", expand=True)
#
#     def OnDouble(self, event):
#         widget = event.widget
#         selection=widget.curselection()
#         value = widget.get(selection[0])
#         print ("selection:", selection, ": '%s'" % value)
#
# if __name__ == "__main__":
#     app = SampleApp()
#     app.mainloop()