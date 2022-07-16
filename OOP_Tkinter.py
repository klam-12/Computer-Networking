import tkinter as tk
from tkinter.constants import *
from tkinter import *
import os
from typing import Container
from PIL import ImageTk, Image

LARGE_FONT = ("Verdana", 12)

class SignInPage(tk.Frame):
    def __init__(self,parent,controller,bg=None, fg=None):
        tk.Frame.__init__(self,parent, bg=bg, fg=fg)

        label_title = tk.Label(self,text= "Welcome to Ruki Food Store",bg="#9FD996", font=("Roman", 30))
        label_user = tk.Label(self,text="Please enter your name",bg="#9FD996", font=("Verdana", 15))
        label_notice = tk.Label(self,text="",bg="#9FD996", font=("Verdana", 10))

        self.entry_user = tk.Entry(self,width=20,text="",bg="white")

        button_go = tk.Button(self,text="GO",command=lambda: controller.SignIn(self))
        button_go.config(width=10,bg="green")

        label_title.place(relx= 0.5,rely=0.3,anchor=CENTER)
        label_user.place(relx=0.5,rely=0.4,anchor=CENTER)
        self.entry_user.place(relx=0.5,rely=0.45,anchor=CENTER)
        label_notice.place(relx=0.5,rely=0.5,anchor=CENTER)
        button_go.place(relx=0.5,rely=0.6,anchor=CENTER)


class programStart(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        self.geometry("600x500")

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (SignInPage, StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self, bg='#9FD996')

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(SignInPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        # os.system("pause")
    def SignIn(self, curFrame):
        try:
            nickname = curFrame.entry_user.get()
            if nickname == "":
                curFrame.label_notice['text'] = "Name can not be empty"
                return
            else:
                self.show_frame(StartPage)
        except:
            print("error")


class StartPage(tk.Frame):

    def __init__(self, parent, controller, bg=None, fg=None):
        tk.Frame.__init__(self, parent, bg=bg, fg=fg)

        # Label
        name = tk.Label(self, text="Ruki Food Store",
                        bg="#9FD996", font=("Roman", 32))
        name.place(relx=0.5, rely=0.2, anchor=CENTER)

        # Button
        # Order button
        order_button = tk.Button(
            self,
            command=lambda: controller.show_frame(PageOne),
            height=3,
            width=10,
            font=28,
            text="Order",
            bg="#808080",
            fg="white"
        )
        order_button.place(relx=0.5, rely=0.4, anchor=CENTER)
        # Payment button
        payment_button = tk.Button(
            self,
            command=lambda: controller.show_frame(PageTwo),
            height=3,
            width=10,
            font=28,
            text="Payment",
            bg="#0080FF",
            fg="white"
        )
        payment_button.place(relx=0.5, rely=0.57, anchor=CENTER)

        # Exit button
        exit_button = tk.Button(
            self,
            command=exit_program,
            height=3,
            width=10,
            font=28,
            text="Exit",
            bg="#FF6666",
            fg="white"
        )
        exit_button.place(relx=0.5, rely=0.74, anchor=CENTER)


class Checkbar(tk.Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        tk.Frame.__init__(self, parent)
        self.vars = []

        # label
        label = tk.Label(self, text="List Foods",
                         bg="#FFFFFF")
        label.pack(side="top", fill='both', anchor="w")

        for row, pick in enumerate(picks):
            var = IntVar()
            chk = Checkbutton(self, bg='#FFFFFF',
                              anchor="w",
                              height=2,
                              width=15,
                              text=pick, variable=var)
            chk.pack(side="top", fill='y', anchor="w")
            # chk.place(x=100, y=0+x)
            self.vars.append(var)
            # x += 50

    def state(self):
        return map((lambda var: var.get()), self.vars)


class CheckQuantity(tk.Frame):
    def __init__(self, parent=None, num=0, side=LEFT, anchor=W):
        tk.Frame.__init__(self, parent)
        self.vars = []

        # label
        label = tk.Label(self, text="Quantity",
                         bg="#FFFFFF")
        label.pack(side="top", fill='both', anchor="w")

        for _ in range(num):
            var = IntVar()
            e = tk.Spinbox(self,
                           from_=0,
                           to=999,
                           bd=2,
                           bg="#FFFFFF"
                           )
            e.pack(side="top", fill='y', padx=0, pady=10)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)


class AddShowImageButton(tk.Frame):
    def __init__(self, parent=None, num=0, side=LEFT, anchor=W):
        tk.Frame.__init__(self, parent)
        self.vars = []

        # label
        label = tk.Label(self, text="Show image",
                         bg="#FFFFFF")
        label.pack(side="top", fill='both', anchor="w")

        for _ in range(num):
            var = IntVar()
            e = tk.Button(self,
                          height=1,
                          text='+',
                          command=open,
                          bd=1,
                          bg="#FFFFFF"
                          )
            e.pack(side="top", fill='y', padx=0, pady=8)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)

# Order page
class PageOne(tk.Frame):

    def __init__(self, parent, controller, bg=None, fg=None):
        tk.Frame.__init__(self, parent, bg=bg, fg=fg)
        # label
        label = tk.Label(self, text="Order Page",
                         bg="#9FD996", font=("Roman", 32))
        label.place(relx=0.5, rely=0.15, anchor=CENTER)

        # Back home button
        back_button = tk.Button(
            self,
            command=lambda: controller.show_frame(StartPage),
            height=3,
            width=10,
            text="Back to home",
            bg="#FF6666",
            fg="white"
        )
        back_button.place(relx=0.1, rely=0.9, anchor=CENTER)

        # Internal Frame
        internal_frame = Frame(self, bg="#FFFFFF", width=300, height=200)
        internal_frame.place(relx=0.22, rely=0.25)

        # Food frame
        food_frame = Frame(internal_frame, bg="#FFFFFF", width=300, height=200)
        food_frame.grid(row=0, column=1)
        # Create list to choice
        lst_food = ['Com Suon', 'Banh Canh', 'Hu Tieu', 'Coca', 'Pepsi']
        lng = Checkbar(food_frame, lst_food)
        lng.pack(padx=0, pady=0)

        # Quantity Frame
        quantity_frame = Frame(internal_frame, bg="#FFFFFF",
                               width=300, height=200)
        quantity_frame.grid(row=0, column=2)
        quantity = CheckQuantity(quantity_frame, len(lst_food))
        quantity.pack(padx=0, pady=0)

        # Show image frame
        show_image_frame = Frame(
            internal_frame, bg="#FFFFFF", width=300, height=200)
        show_image_frame.grid(row=0, column=3)
        quantity = AddShowImageButton(show_image_frame, len(lst_food))
        quantity.pack(padx=5, pady=5)

        # Submit button
        back_button = tk.Button(
            self,
            # command=lambda: controller.show_frame(StartPage),
            height=2,
            width=10,
            text="Add to cart",
            bg="#0080FF",
            fg="white"
        )
        back_button.place(relx=0.5, rely=0.8, anchor=CENTER)

# Payment Page
class PageTwo(tk.Frame):

    def __init__(self, parent, controller, bg=None, fg=None):
        tk.Frame.__init__(self, parent, bg=bg, fg=fg)
        # label
        label = tk.Label(self, text="Payment Page",
                         bg="#9FD996", font=("Roman", 32))
        label.place(relx=0.5, rely=0.2, anchor=CENTER)

        # Back home button
        back_button = tk.Button(
            self,
            command=lambda: controller.show_frame(StartPage),
            height=3,
            width=10,
            text="Back to home",
            bg="#FF6666",
            fg="white"
        )
        back_button.place(relx=0.1, rely=0.9, anchor=CENTER)

        # Cash payment
        pay_up_button = tk.Button(
            self,
            # command=lambda: controller.show_frame(StartPage),
            height=4,
            width=20,
            font=32,
            text="Cash payment",
            bg="#0080FF",
            fg="white"
        )
        pay_up_button.place(relx=0.5, rely=0.4, anchor=CENTER)

        # Charge Card Payment
        pay_up_button = tk.Button(
            self,
            # command=lambda: controller.show_frame(StartPage),
            height=4,
            width=20,
            font=32,
            text="Charge Card Payment",
            bg="#FF9933",
            fg="white"
        )
        pay_up_button.place(relx=0.5, rely=0.6, anchor=CENTER)


def exit_program():
    os.sys.exit()


def open():
    global my_img
    top = Toplevel()
    top.title('My Second Window')

    img = Image.open('camcui.jpg')
    img = img.resize((450, 350))
    # Resize image
    #my_img = my_img.resize((600, 350))
    my_img = ImageTk.PhotoImage(img)
    my_label = Label(top, image=my_img).pack()
    btn2 = Button(top, text="close window", command=top.destroy).pack()

# Exit page
class PageThree(tk.Frame):

    def __init__(self, parent, controller, bg=None, fg=None):
        tk.Frame.__init__(self, parent, bg=bg, fg=fg)

        # label
        label = tk.Label(self, text="Exit Page",
                         bg="#9FD996", font=("Roman", 32))
        label.place(relx=0.5, rely=0.2, anchor=CENTER)

        # Back home button
        back_button = tk.Button(
            self,
            # command=lambda: controller.show_frame(StartPage),
            height=3,
            width=10,
            text="Back to home",
            bg="#FF6666",
            fg="white"
        )
        back_button.place(relx=0.1, rely=0.9, anchor=CENTER)


app = programStart()
app.mainloop()
