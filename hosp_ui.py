from tkinter import *
import new

class ticket:
	def __init__(self,root):
		self.f = Frame(root,height=500,width=500)
		self.f.propagate(0)
		self.f.pack()
		root.title("Finding Hospital Near You")
		self.l = Label(self.f,text="Enter the Hospital speciality:")
		self.s = StringVar()
		self.e = Entry(self.f,textvariable=self.s,width=15)
		self.e.pack()
		self.l1 = Label(self.f,text="Enter the Hospital Type:")
		self.s1 = StringVar()
		self.e1 = Entry(self.f,textvariable=self.s1,width=15)
		self.e1.pack()
		self.l2 = Label(self.f,text="Enter your Location:")
		self.l.place(x=50,y=100)
		self.e.place(x=250,y=100)
		self.l1.place(x=50,y=150)
		self.e1.place(x=250,y=150)
		self.l2.place(x=50,y=200)
		self.submitButton = Button(self.f, text="Locate Me!!")
		self.submitButton.place(x=250,y=200)
		# creating a button instance
		self.saveButton = Button(self.f, text="Save")
		# placing the button on my window
		self.saveButton.place(x=150,y=250)


root = Tk()
t = ticket(root)
root.mainloop()
