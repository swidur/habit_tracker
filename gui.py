from Tkinter import *
import activities
import activity
import sqlite3 as lite
import tkMessageBox
import create_db
import table
import Tkinter as tk
import time

actv = activities.Activities()


def notImplemented():
    m.stat.set('Not implemented yet, sorry!')


def about():
    tkMessageBox.showinfo('O programie.. ', 'Habit Tracker v0.1\n\nDawid Swidurski\ngithub.com/swidur')


class addPopup(object):
    def __init__(self, master):
        self.top = self.top = Toplevel(master)
        self.top.geometry('230x75+295+290')
        self.top.resizable(width=False, height=False)
        self.top.attributes("-toolwindow", 1)
        self.top.title('Add activity')
        self.top.grab_set()


        self.top.bind("<Escape>", self.close)


        self.name_l = Label(self.top, text="Activity name: ")
        self.name_l.grid(row=0, column=0, sticky=E)

        self.actv_name = Entry(self.top)
        self.actv_name.grid(row=0, column=1)
        self.actv_name.focus()
        self.actv_name.bind("<Return>", self.focus_on_dur)

        self.dur_l = Label(self.top, text="Activity duration: ")
        self.dur_l.grid(row=1, column=0, sticky=E)

        self.actv_dura = Entry(self.top)
        self.actv_dura.grid(row=1, column=1)
        self.actv_dura.bind("<Return>", self.focus_on_ok)

        self.f = Frame(self.top)
        self.f.grid(row=2, columnspan=2)

        self.add_button = Button(self.f, text='Add')
        self.add_button.grid(row=0, column=0, padx=1)
        self.add_button.bind("<Button-1>", self.submit)
        self.add_button.bind("<Return>", self.submit)

        self.cancel_button = Button(self.f, text='Cancel')
        self.cancel_button.grid(row=0, column=1, padx=1)
        self.cancel_button.bind("<Button-1>", self.close)

        # reassigned in cleanup method
        self.name = None
        self.duration = None


    def focus_on_dur(self, event):
        self.top.bind("<Return>", self.actv_dura.focus())

    def focus_on_ok(self, event):
        self.top.bind("<Return>", self.add_button.focus())

    def submit(self, event):
        # cast entry fields variables into correct types. Display error to status bar.
        try:
            try:
                self.duration = float(self.actv_dura.get())
            except (TypeError, ValueError):
                m.stat.set('Expected number, got {} instead.'.format(type(self.actv_dura.get())))
                raise TypeError

            try:
                self.name = str(self.actv_name.get())
            except (TypeError, ValueError):
                m.stat.set('Expected string, got {} instead.'.format(type(self.actv_name.get())))
                raise TypeError

        except TypeError:
            self.top.destroy()
            self.top.grab_release()

        else:
            self.send()

    def send(self):
        if self.name != '' and self.duration != '':
            m.stat.set('Added')
            actv.add_act(activity.Activity(self.name, self.duration))
        else:
            m.stat.set('Empty value not permitted. Aborted.')
        self.top.destroy()
        self.top.grab_release()

    def close(self, event):
        m.stat.set('Canceled')
        self.top.destroy()


class viewPopup(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        top.minsize(height=250, width=225)
        # top.geometry('0x0+295+290')
        top.resizable(width=False, height=1)
        top.attributes("-toolwindow", 1)
        top.title('Add activity')
        top.grab_set()

        self.inst = showActiv(top)

        self.f = Frame(top)
        self.f.pack(fill=X)

        self.cancel_button = Button(self.f, text='OK', command=self.close)
        self.cancel_button.pack()
        self.cancel_button.focus()

    def close(self):
        m.stat.set('Closed')
        self.top.destroy()


class delPopup(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        top.minsize(height=250, width=225)
        # top.geometry('0x0+295+290')
        top.resizable(width=False, height=1)
        top.attributes("-toolwindow", 1)
        top.title('Add activity')
        top.grab_set()
        top.focus()

        self.inst = showDel(top)

        self.f = Frame(top)
        self.f.pack(fill=X)

        self.cancel_button = Button(self.f, text='OK', command=self.close)
        self.cancel_button.pack()

        # top.bind("<Return>", self.ok)
        top.bind("<Escape>", self.close)

    def close(self, event):
        m.stat.set('Closed')
        self.top.destroy()


class mainWindow(object):
    def __init__(self, master):
        root.minsize(height=300, width=300)
        root.geometry('300x300+250+200')
        root.maxsize(height=99999999, width=300)
        master.title('Habit Tracker')
        self.stat = StringVar()

        self.main_menu = MainMenu(root)
        self.toolbar = Toolbar(root)

        # self.master = master
        # self.b2=Button(master,text="print value",command=lambda: sys.stdout.write(self.entryValue()+'\n'))
        # self.b2.pack()

        #  ************** STATUS BAR **************

        status = Label(root, textvariable=self.stat, bd=1, relief=SUNKEN, anchor=W)
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


class showActiv():
    def __init__(self, master):
        self.length = len(actv.get_aggregated())
        self.master = master
        self.t = table.SimpleTable(self.master, self.length + 1, 3)

        self.t.set(0, 0, 'Name')
        self.t.set(0, 1, 'Time')
        self.t.set(0, 2, 'Count')

        for i in range(self.length):
            self.t.set(i + 1, 0, actv.get_aggregated()[i][0])
            self.t.set(i + 1, 1, actv.get_aggregated()[i][1])
            self.t.set(i + 1, 2, actv.get_aggregated()[i][2])


class showDel():
    def __init__(self, master):
        self.length = len(actv.get_aggregated())
        self.master = master
        self.t = table.SimpleTable(self.master, self.length + 1, 4)

        self.t.set(0, 1, 'Name')
        self.t.set(0, 2, 'Time')
        self.t.set(0, 3, 'Count')

        for i in range(self.length):
            self.t.set(i + 1, 1, actv.get_aggregated()[i][0])
            self.t.set(i + 1, 2, actv.get_aggregated()[i][1])
            self.t.set(i + 1, 3, actv.get_aggregated()[i][2])
            self.t.set(i + 1, 0, Checkbutton(self.t.frame, pady=0, padx=0, borderwidth=0).grid(row=i + 1, column=0))


class Toolbar:
    def __init__(self, master):
        #  ************** TOOLBAR **************
        self.var = StringVar()
        self.toolbar = Frame(master, bg='red')

        self.add_butt = Button(self.toolbar, text='Add', command=self.add_popup)
        self.add_butt.config(width=13)
        self.add_butt.pack(side=LEFT)

        self.view_butt = Button(self.toolbar, text='View', command=self.view_popup)
        self.view_butt.config(width=13)
        self.view_butt.pack(side=LEFT)
        # self.view_butt.bind("<Button-1>", show)
        # self.view_butt.bind("<Button-3>", some2)

        self.del_butt = Button(self.toolbar, text='Delete', command=self.del_popup)
        self.del_butt.config(width=13)
        self.del_butt.pack(side=LEFT)

        self.toolbar.pack(side=TOP, fill=X)

    def add_popup(self):
        m.stat.set('Add')

        self.ap = addPopup(self.toolbar)
        self.add_butt["state"] = "disabled"
        self.toolbar.wait_window(self.ap.top)
        self.add_butt["state"] = "normal"

    def view_popup(self):
        m.stat.set('View')

        self.vp = viewPopup(self.toolbar)
        self.view_butt["state"] = "disabled"
        self.toolbar.wait_window(self.vp.top)
        self.view_butt["state"] = "normal"

    def del_popup(self):
        m.stat.set('Delete')

        self.dp = delPopup(self.toolbar)
        self.del_butt["state"] = "disabled"
        self.toolbar.wait_window(self.dp.top)
        self.del_butt["state"] = "normal"


if __name__ == "__main__":
    root = Tk()
    m = mainWindow(root)
    root.mainloop()
