from Tkinter import *
import activities
import activity
import sqlite3 as lite
import tkMessageBox
import create_db
import table
import Tkinter as tk



actv = activities.Activities()





def notImplemented():
    m.stat.set('Not implemented yet, sorry!')


def about():
    tkMessageBox.showinfo('O programie.. ', 'Habit Tracker v0.1\n\nDawid Swidurski\ngithub.com/swidur')


class popupWindow(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        top.geometry('230x75+295+290')
        top.resizable(width=False, height=False)
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
        self.f = Frame(top)
        self.f.grid(row=2, columnspan = 2)

        self.add_button = Button(self.f, text='Add', command=self.cleanup)
        self.add_button.grid(row=0, column=0, padx = 1)

        self.cancel_button = Button(self.f, text='Cancel', command=self.close)
        self.cancel_button.grid(row=0, column=1 , padx = 1)

    def cleanup(self):
        if self.actv_name.get() != '' and self.actv_dura.get() != '':
            m.stat.set('Added')
            actv.add_act(activity.Activity(self.actv_name.get(), self.actv_dura.get()))
        else:
            m.stat.set('Empty value not permitted. Canceled.')
        self.top.destroy()
        self.top.grab_release()

    def close(self):
        m.stat.set('Canceled')
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
    def __init__(self):
        self.length = len(actv.get_aggregated())
        self.t = table.SimpleTable(root, self.length, 3)
        for i in range(self.length):
            self.t.set(i, 0, actv.get_aggregated()[i][0])
            self.t.set(i, 1, actv.get_aggregated()[i][1])
            self.t.set(i, 2, actv.get_aggregated()[i][2])



class Toolbar:
    def __init__(self, master):
        #  ************** TOOLBAR **************
        self.var = StringVar()
        self.toolbar = Frame(master, bg='red')

        self.add_butt = Button(self.toolbar, text='Add', command=self.popup)
        self.add_butt.config(width=13)
        self.add_butt.pack(side=LEFT)

        self.view_butt = Button(self.toolbar, text='View', command=self.some)
        self.view_butt.config(width=13)
        self.view_butt.pack(side=LEFT)

        self.del_butt = Button(self.toolbar, text='Delete', command=notImplemented)
        self.del_butt.config(width=13)
        self.del_butt.pack(side=LEFT)

        self.toolbar.pack(side=TOP, fill=X)

        self.click_c = 0

    def some(self):
        inst = showActiv()
        if self.click_c == 0:
            # inst = showActiv()
            self.click_c += 1
            print self.click_c
        else:
            inst.t.hide()
            self.click_c = 0
            print 'update'

    def popup(self):
        m.stat.set('Pressed add')

        self.w = popupWindow(self.toolbar)
        self.add_butt["state"] = "disabled"
        self.toolbar.wait_window(self.w.top)
        self.add_butt["state"] = "normal"

    def get_actvities(self):
        self.var.set(actv.get_aggregated())


if __name__ == "__main__":
    root = Tk()
    m = mainWindow(root)
    root.mainloop()

