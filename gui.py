from Tkinter import *
import activities
import activity
import sqlite3 as lite
import tkMessageBox

actv = activities.Activities()


def notImplemented():
    print 'Not implemented yet, sorry!'


def about():
    tkMessageBox.showinfo('O programie.. ', 'Habit Tracker v0.1\n\nDawid Swidurski\ngithub.com/swidur')


class popupWindow(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        top.minsize(height=75, width=150)
        top.attributes("-toolwindow", 1)
        top.title('Add activity')
        top.grab_set()

        self.name_l = Label(top, text="Activity name: ")
        self.name_l.grid(row=0, column=0, sticky=E)

        self.actv_name = Entry(top)
        self.actv_name.grid(row=0, column=1)

        self.dur_l = Label(top, text="Activity duration: ")
        self.dur_l.grid(row=1, column=0, sticky=E)

        self.actv_dura = Entry(top)
        self.actv_dura.grid(row=1, column=1)

        self.ok_button = Button(top, text='Ok', command=self.cleanup)
        self.ok_button.grid(row=2, column=0, columnspan=2)

    def cleanup(self):
        if self.actv_name.get() != '' and self.actv_dura.get() != '':
            actv.add_act(activity.Activity(self.actv_name.get(), self.actv_dura.get()))
        self.top.destroy()
        self.top.grab_release()


class mainWindow(object):
    def __init__(self, master):
        root.minsize(height=300, width=300)
        root.maxsize(height=99999999, width=300)
        master.title('Habit Tracker')

        self.main_menu = MainMenu(root)
        self.toolbar = Toolbar(root)
        self.master = master
        # self.b2=Button(master,text="print value",command=lambda: sys.stdout.write(self.entryValue()+'\n'))
        # self.b2.pack()

        #  ************** STATUS BAR **************

        status = Label(root, text='Preparing to do nothing', bd=1, relief=SUNKEN, anchor=W)
        status.pack(side=BOTTOM, fill=X)

    def entryValue(self):
        return self.w.value


class MainMenu:
    #  ************** MENU **************
    def __init__(self, master):
        self.menu = Menu(master)
        master.config(menu=self.menu)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Plik', menu=self.file_menu)
        self.file_menu.add_command(label='Otworz..', command=notImplemented)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Zamknij', command=root.quit)
        self.help_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Pomoc', menu=self.help_menu)
        self.help_menu.add_command(label='O programie..', command=about)


class Toolbar:
    def __init__(self, master):
        #  ************** TOOLBAR **************

        self.toolbar = Frame(master, bg='red')
        self.add_butt = Button(self.toolbar, text='Add', command=self.popup)
        self.add_butt.config(width=13)
        self.add_butt.pack(side=LEFT)
        self.view_butt = Button(self.toolbar, text='View', command=notImplemented)
        self.view_butt.config(width=13)
        self.view_butt.pack(side=LEFT)
        self.del_butt = Button(self.toolbar, text='Delete', command=notImplemented)
        self.del_butt.config(width=13)
        self.del_butt.pack(side=LEFT)
        self.toolbar.pack(side=TOP, fill=X)

    def popup(self):
        self.w = popupWindow(self.toolbar)
        self.add_butt["state"] = "disabled"
        self.toolbar.wait_window(self.w.top)
        self.add_butt["state"] = "normal"


if __name__ == "__main__":
    root = Tk()
    m = mainWindow(root)
    root.mainloop()
