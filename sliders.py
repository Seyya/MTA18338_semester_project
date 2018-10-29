import tkinter as gui

master = gui.Tk()


def givevalueplz(value, value1):
    print(value, value1)
    return value, value1


scale1 = gui.Scale(master, from_=0, to=42)
scale1.pack()
scale2 = gui.Scale(master, from_=0, to=255, orient=gui.HORIZONTAL)
scale2.pack()
btn = gui.Button(master, text='Show', command=lambda: givevalueplz(scale1.get(), scale2.get()))
btn.pack()

master.mainloop()
