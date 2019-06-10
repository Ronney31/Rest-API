from tkinter import *
import requests, json
from view.placeholder import EntryWithPlaceholder as placeholder

class frontEnd():
    __radius = 135
    __ls = "That which you are GOOD at?"
    __rs = "That which the world need?"
    __ts = "That which you love?"
    __bs = "That which can be paid for?"

    def __init__(self, root, q1=NONE, q2=NONE, q3=NONE, q4=NONE, username=NONE):
        self.lQues = q1
        self.rQues = q2
        self.tQues = q3
        self.bQues = q4
        self.userName = username
        self.userData = {}
        self.root = root
        self.frame = Frame(self.root)
        self.myCanvas = Canvas(self.root, width="600", height="500", bg="white")

        self.leftQues = placeholder(self.myCanvas, frontEnd.__ls, 20, frontEnd.__ls, "orange")
        self.rightQues = placeholder(self.myCanvas, frontEnd.__rs, 20, frontEnd.__rs, "green")
        self.topQues = placeholder(self.myCanvas, frontEnd.__ts, 28, frontEnd.__ts, "blue")
        self.bottomQues = placeholder(self.myCanvas, frontEnd.__bs, 28, frontEnd.__bs, "red")
        self.entry_userName = placeholder(self.root, "Enter Username",20)
        self.scroll_userList = Scrollbar(self.frame)
        self.listbox = Listbox(self.frame, yscrollcommand=self.scroll_userList.set, height=10)
        self.status = Label(self.root, fg="red", font='Helvetica 19 bold')

    def create_circle(self, radius, canvasName):  # center coordinates, radius
        canvasName.create_oval(200 - radius, 250 - radius, 200 + radius, 250 + radius, width=2, outline="orange")
        canvasName.create_oval(400 - radius, 250 - radius, 400 + radius, 250 + radius, width=2, outline="green")
        canvasName.create_oval(300 - radius, 360 - radius, 300 + radius, 360 + radius, width=2, outline="red")
        canvasName.create_oval(300 - radius, 145 - radius, 300 + radius, 145 + radius, width=2, outline="blue")

    def popupmsg(self, msg):
        popup = Tk()
        popup.wm_title("!")
        label = Label(popup, text=msg, font=("Verdana", 12))
        label.pack(side="top", fill="x", pady=10)
        B1 = Button(popup, text="Okay", command=popup.destroy)
        B1.pack()
        popup.mainloop()

    def userList(self):
        self.userData.clear()
        self.listbox.delete(0, 'end')
        try:
            req = requests.get('http://127.0.0.1:5010/ikis/users/')
            if req.status_code == 200 :
                req_data = req.json()
                for key in req_data['users ']:
                    __uName = key['userName']
                    del key['userName']
                    self.userData[__uName] = key
                for __userName in self.userData:
                    self.listbox.insert(END, str(__userName))
            else:
                self.status['text'] = "Something Went Wrong "
        except Exception as e:
            self.status['text'] = " 404 :: Server Not Found "

    def onClickListItem(self, event):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        __user = self.userData[value]
        self.clearEntry()
        self.entry_userName.insert(0,value)
        self.leftQues.insert(0, __user['Answer 1'])
        self.rightQues.insert(0, __user['Answer 2'])
        self.topQues.insert(0, __user['Answer 3'])
        self.bottomQues.insert(0, __user['Answer 4'])

    def clearEntry(self):
        self.entry_userName.delete('0', 'end')
        self.leftQues.delete('0', 'end')
        self.rightQues.delete('0', 'end')
        self.topQues.delete('0', 'end')
        self.bottomQues.delete('0', 'end')

    def addUserData(self):
        __userName = self.entry_userName.get()
        __leftQues = self.leftQues.get()
        __rightQues = self.rightQues.get()
        __topQues = self.topQues.get()
        __bottomQues = self.bottomQues.get()

        try:
            __url = "http://127.0.0.1:5010/iki/"+__userName
            __data = {"q1": __leftQues, "q2": __rightQues, "q3": __topQues, "q4": __rightQues}
            r = requests.post(__url, data=__data)
            if r.status_code != 201:
                self.status['text'] = r.json()['Message']
                return
            self.status['text'] = "Record Successfully Added"
        except Exception as e:
            self.status['text'] = "An Error Occur While Adding Record."
        self.userList()

    def updateUserData(self):
        __userName = self.entry_userName.get()
        __leftQues = self.leftQues.get()
        __rightQues = self.rightQues.get()
        __topQues = self.topQues.get()
        __bottomQues = self.bottomQues.get()

        if __userName not in self.userData:
            self.status['text'] = "Record Not Found"
            return
        try:
            __url = "http://127.0.0.1:5010/iki/" + __userName
            __data = {"q1": __leftQues, "q2": __rightQues, "q3": __topQues, "q4": __rightQues}
            r = requests.put(__url, data=__data)
            if r.status_code != 200:
                msg = "Something went wrong"
                raise msg
            self.status['text'] = "Record Successfully Updated."
        except Exception as e:
            self.status['text'] = "An Error Occur While Updating Record."
        self.userList()

    def deleteUserData(self):
        __userName = self.entry_userName.get()
        if __userName not in self.userData:
            self.status['text'] = "Record Not Found"
            return
        try:
            __url = "http://127.0.0.1:5010/iki/" + __userName
            r = requests.delete(__url)
            if r.status_code != 200:
                msg = "Something went wrong"
                raise msg
            self.status['text'] = "Record Successfully Deleted."
            self.clearEntry()
        except Exception as e:
            self.status['text'] = "An Error Occur While Deleting Record."
        self.userList()

    def main(self):
        self.create_circle(frontEnd.__radius, self.myCanvas)
        header = Label(self.root, text='IKIGAI APPLICATION', fg='BLACK', bg='YELLOW', font=("Cambria", 22, "bold"))
        header.pack()
        iki_quote = Label(self.myCanvas, text="IKIGAI", bg="white", font=("Georgia", 14))
        iki_quote.pack()
        self.myCanvas.pack()
        self.myCanvas.place(x=200, y=80)
        self.leftQues.pack()
        self.rightQues.pack()
        self.topQues.pack()
        self.bottomQues.pack()

        self.myCanvas.create_window(130, 250, window=self.leftQues)
        self.myCanvas.create_window(470, 250, window=self.rightQues)
        self.myCanvas.create_window(300, 75, window=self.topQues)
        self.myCanvas.create_window(300, 425, window=self.bottomQues)
        self.myCanvas.create_window(300, 250, window=iki_quote)

        Label_ques = Label(self.root, text="User Answers (view only)")
        Label_leftQues = Label(self.root, textvariable=frontEnd.__ls, fg="orange")
        Label_rightQues = Label(self.root, textvariable=frontEnd.__rs, fg="green")
        Label_topQues = Label(self.root, textvariable=frontEnd.__ts, fg="blue")
        Label_bottomQues = Label(self.root, textvariable=frontEnd.__bs, fg="red")

        Label_ques.pack()
        Label_leftQues.pack()
        Label_rightQues.pack()
        Label_topQues.pack()
        Label_bottomQues.pack()
        Label_ques.place(x=20, y=580)
        Label_leftQues.place(x=20, y=600)
        Label_rightQues.place(x=20, y=620)
        Label_topQues.place(x=20, y=640)
        Label_bottomQues.place(x=20, y=660)

        # status
        self.status['justify'] = CENTER
        self.status.pack()
        self.status.place(x=300, y=710)

        # userList
        userNameHeader = Label(self.root, text="User Name")
        userNameHeader.pack()
        self.listbox.bind("<Double-Button-1>", self.onClickListItem)
        self.listbox.pack(side=LEFT, fill=BOTH)
        self.scroll_userList.pack(side=RIGHT, fill=Y)
        self.scroll_userList.config(command=self.listbox.yview)
        userNameHeader.place(x=20, y=150)
        self.userList()
        self.frame.pack()
        self.frame.place(x=20, y=172)

        lable_userName = Label(self.root, text="Enter Username")
        lable_userName.pack()
        self.entry_userName.pack()
        lable_userName.place(x=835, y=150)
        self.entry_userName.place(x=820, y=172)

        # buttons
        add_button = Button(self.root, text="Add Record", command=self.addUserData)
        update_button = Button(self.root, text="Update Record", command=self.updateUserData)
        delete_button = Button(self.root, text="Delete Record", command=self.deleteUserData)
        add_button.pack()
        update_button.pack()
        delete_button.pack()
        add_button.place(x=850, y=280)
        update_button.place(x=842, y=315)
        delete_button.place(x=845, y=350)

        # one time
        left_lab = Label(self.myCanvas, text="That which you\nare GOOD at?", fg="orange")
        right_lab = Label(self.myCanvas, text="That which the\nworld need?", fg="green")
        top_lab = Label(self.myCanvas, text="That which you love?", fg="blue")
        bottom_lab = Label(self.myCanvas, text="That which can be paid for?", fg="red")

        left_lab.pack()
        right_lab.pack()
        top_lab.pack()
        bottom_lab.pack()

        left_lab.place(x=83, y=195)
        right_lab.place(x=430, y=195)
        top_lab.place(x=235, y=35)
        bottom_lab.place(x=220, y=385)


if __name__ == "__main__":
    __root = Tk()

    FE = frontEnd(__root)
    FE.main()
    
    __root.title("IKIGAI Python Application")
    __root.geometry("1000x900")
    __root.mainloop()






