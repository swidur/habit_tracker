from Tkinter import *
import activities
import activity
import tkMessageBox
import create_db
import table
import logging

logging.basicConfig(filename='debug.log', format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='/%d-%m-%Y %H:%M:%S/', level=logging.DEBUG)

actv = activities.Activities()


def notImplemented():
    info = 'Not yet implemented, sorry!'
    m.stat.set(info)
    logging.warning(info)


def about():
    tkMessageBox.showinfo('About.. ', 'Habit Tracker v0.1\n\nDawid Swidurski\ngithub.com/swidur')
    info = 'About displayed'
    m.stat.set(info)
    logging.debug(info)


class addPopup(object):
    def __init__(self, master):
        self.top = self.top = Toplevel(master)
        self.top.geometry("+%d+%d" % (master.winfo_rootx() + 50, master.winfo_rooty() + 50))
        self.top.resizable(width=False, height=False)
        self.top.attributes("-toolwindow", 1)
        self.top.title('Add activity')
        self.top.grab_set()
        info = "'addPopup' created"
        logging.debug(info)

        self.top.bind("<Escape>", self.closeEsc)
        self.top.protocol("WM_DELETE_WINDOW", self.closeX)

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

        self.add_button = Button(self.f, text='Add', command=self.submit)
        self.add_button.grid(row=0, column=0, padx=1)
        self.add_button.bind("<Return>", self.submit)

        self.cancel_button = Button(self.f, text='Cancel', command=self.close)
        self.cancel_button.grid(row=0, column=1, padx=1)

        # reassigned in cleanup method
        self.name = ''
        self.duration = ''

    def focus_on_dur(self, *args):
        self.top.bind("<Return>", self.actv_dura.focus())
        info = 'Add popup: focus on activity duration entry field'
        logging.debug(info)

    def focus_on_ok(self, *args):
        self.top.bind("<Return>", self.add_button.focus())
        info = 'Add popup: focus on add activity button'
        logging.debug(info)


    def submit(self, *args):
        # cast entry fields variables into correct types. Display error to status bar.
        try:
            try:
                if self.actv_dura.get() != '':
                    self.duration = float(self.actv_dura.get())
            except (TypeError, ValueError):
                info = 'Expected number, got {} instead.'.format(type(self.actv_dura.get()))
                m.stat.set(info)
                logging.warning(info)
                raise TypeError

            try:
                self.name = str(self.actv_name.get())
            except (TypeError, ValueError):
                info = 'Expected string, got {} instead.'.format(type(self.actv_name.get()))
                m.stat.set(info)
                logging.warning(info)
                raise TypeError

        except TypeError:
            logging.warning('TypeError raised, did not submit any data')
            self.top.destroy()
            self.top.grab_release()

        else:
            self.send()

    def send(self):
        if self.name != '' and self.duration != '':
            info = 'Added: {}, {} hrs'.format(self.name, self.duration)
            m.stat.set(info)
            logging.debug(info)
            actv.add_act(activity.Activity(self.name, self.duration))
        else:
            info = 'Empty value not permitted. Aborted'
            m.stat.set(info)
            logging.debug(info)
        self.top.destroy()
        self.top.grab_release()

    def close(self, *args):
        info = "Closed 'Add activities' via 'Cancel' button"
        m.stat.set(info)
        logging.debug(info)
        self.top.destroy()

    def closeX(self, *args):
        info = "Closed 'Add activities' via X button"
        m.stat.set(info)
        logging.debug(info)
        self.top.destroy()

    def closeEsc(self, *args):
        info = "Closed 'Add activities' via escape"
        m.stat.set(info)
        logging.debug(info)
        self.top.destroy()


class viewPopup(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        top.minsize(height=250, width=225)
        self.top.geometry("+%d+%d" % (master.winfo_rootx() + 80, master.winfo_rooty() - 20))
        top.resizable(width=False, height=1)
        top.attributes("-toolwindow", 1)
        top.title('Activities')
        self.top.protocol("WM_DELETE_WINDOW", self.closeX)
        top.grab_set()
        info = "'viewPopup' created"
        logging.debug(info)

        self.inst = showActiv(top)

        self.f = Frame(top)
        self.f.pack(fill=X)

        self.cancel_button = Button(self.f, text='OK', command=self.close)
        self.cancel_button.pack()
        self.cancel_button.focus()
        self.cancel_button.bind("<Return>", self.close)
        top.bind("<Escape>", self.closeEsc)

    def close(self, *args):
        info = "View activities closed via 'OK' button"
        m.stat.set(info)
        logging.debug(info)
        self.top.destroy()

    def closeEsc(self, *args):
        info = "View activities closed via escape"
        m.stat.set(info)
        logging.debug(info)
        self.top.destroy()

    def closeX(self, *args):
        info = 'View activities closed via X button'
        m.stat.set(info)
        logging.debug(info)
        self.top.destroy()


class delPopup(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        top.minsize(height=250, width=225)
        self.top.geometry("+%d+%d" % (master.winfo_rootx() + 80, master.winfo_rooty() - 20))
        top.resizable(width=False, height=1)
        top.attributes("-toolwindow", 1)
        top.title('Delete activity')
        self.top.protocol("WM_DELETE_WINDOW", self.closex)
        top.grab_set()

        self.inst = showDelEntryBox(top)

        self.f = Frame(top)
        self.f.pack()

        self.e_val = StringVar()

        self.e = Entry(self.f)
        self.e.insert(0, "Enter activity name..")
        self.e.bind("<Button-1>", self.clear_e)
        self.e.grid(row=0, columnspan=2, pady=5)

        self.sf = Frame(top)
        self.sf.pack()

        self.add_button = Button(self.sf, text='Delete', command=self.delete)
        self.add_button.grid(row=1, column=0, padx=2, pady=7)

        self.cancel_button = Button(self.sf, text='Cancel', command=self.close)
        self.cancel_button.grid(row=1, column=1)
        self.cancel_button.bind("<Return>", self.closeesc)
        self.cancel_button.focus()

        top.bind("<Escape>", self.close)

    def close(self, *args):
        info = "'Delete activities' closed via 'Cancel' button"
        m.stat.set(info)
        logging.debug(info)
        self.top.destroy()

    def closeesc(self, *args):
        info = "'Delete activities' closed via esc"
        m.stat.set(info)
        logging.debug(info)
        self.top.destroy()

    def closex(self, *args):
        info = "'Delete activities' closed via X button"
        m.stat.set(info)
        logging.debug(info)
        self.top.destroy()

    def delete(self, *args):
        self.e_val = self.e.get()
        if self.e_val != '':
            actv.del_by_name(self.e_val)
            info = actv.info
            m.stat.set(info)
            logging.debug(info)
            self.clear_e()
        else:
            info = 'Blank space is not valid activity name'
            m.stat.set(info)
            logging.warning(info)
        print self.e_val
        self.close()
        m.toolbar.del_popup()

    def clear_e(self, *args):
        self.e.delete(0, END)
        info = 'Cleared delete entry widget'
        logging.debug(info)


class mainWindow(object):
    def __init__(self, master):
        self.stat = StringVar()
        root.minsize(height=300, width=300)
        root.geometry('300x300+150+100')
        root.maxsize(height=99999999, width=300)
        self.master = master
        master.title('Habit Tracker')
        master.protocol("WM_DELETE_WINDOW", self.closeX)

        info = 'Main window opened'
        self.stat.set(info)
        logging.warning(info)

        self.main_menu = MainMenu(root)
        self.toolbar = Toolbar(root)

        # self.master = master
        # self.b2=Button(master,text="print value",command=lambda: sys.stdout.write(self.entryValue()+'\n'))
        # self.b2.pack()

        #  ************** STATUS BAR **************

        status = Label(root, textvariable=self.stat, bd=1, relief=SUNKEN, anchor=W)
        status.pack(side=BOTTOM, fill=X)


    def closeX(self):
        self.master.destroy()
        info = 'Main window closed via X button'
        logging.warning(info)


class MainMenu:
    #  ************** MENU **************
    def __init__(self, master):
        self.menu = Menu(master)
        self.master = master
        master.config(menu=self.menu)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='File', menu=self.file_menu)

        self.file_menu.add_command(label='Open..', command=self.open_db)

        self.file_menu.add_separator()

        self.file_menu.add_command(label='Close', command=self.close)

        self.help_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Help', menu=self.help_menu)
        self.help_menu.add_command(label='About..', command=about)

    def open_db(self, *args):
        info = "'Open' menu called"
        m.stat.set(info)
        logging.debug(info)
        notImplemented()

    def close(self, *args):
        info = "Main window closed via menu button 'Close'"
        m.stat.set(info)
        logging.warning(info)
        self.master.destroy()



class showActiv():
    def __init__(self, master):
        self.length = len(actv.get_aggregated())
        self.master = master
        self.t = table.SimpleTable(self.master, self.length + 1, 3, 15)

        self.t.set(0, 0, 'Name')
        self.t.set(0, 1, 'Time')
        self.t.set(0, 2, 'Count')

        for i in range(self.length):
            self.t.set(i + 1, 0, actv.get_aggregated()[i][0])
            self.t.set(i + 1, 1, actv.get_aggregated()[i][1])
            self.t.set(i + 1, 2, actv.get_aggregated()[i][2])


# class showDelCheckbox():
#     def __init__(self, master):
#         self.length = len(actv.get_aggregated())
#         self.master = master
#         self.t = table.SimpleTable(self.master, self.length + 1, 4, 6)
#
#         self.t.set(0, 0, '')
#         self.t.set(0, 1, 'Name')
#         self.t.set(0, 2, 'Time')
#         self.t.set(0, 3, 'Count')
#
#         for i in range(self.length):
#             self.t.set(i + 1, 1, actv.get_aggregated()[i][0])
#             self.t.set(i + 1, 2, actv.get_aggregated()[i][1])
#             self.t.set(i + 1, 3, actv.get_aggregated()[i][2])
#             self.t.set(i + 1, 0, Checkbutton(self.t.frame, pady=0, padx=0, borderwidth=0, command = notImplemented).grid(row=i + 1, column=0))


class showDelEntryBox():
    def __init__(self, master):
        self.length = len(actv.get_aggregated())
        self.master = master
        self.t = table.SimpleTable(self.master, self.length + 1, 3, 15)

        self.t.set(0, 0, 'Name')
        self.t.set(0, 1, 'Time')
        self.t.set(0, 2, 'Count')

        for i in range(self.length):
            self.t.set(i + 1, 0, actv.get_aggregated()[i][0])
            self.t.set(i + 1, 1, actv.get_aggregated()[i][1])
            self.t.set(i + 1, 2, actv.get_aggregated()[i][2])


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
        info = 'Add activity'
        m.stat.set(info)
        logging.debug(info)

        self.ap = addPopup(self.toolbar)
        self.add_butt["state"] = "disabled"
        self.toolbar.wait_window(self.ap.top)
        self.add_butt["state"] = "normal"

    def view_popup(self):
        info = 'View activities'
        m.stat.set(info)
        logging.debug(info)

        self.vp = viewPopup(self.toolbar)
        self.view_butt["state"] = "disabled"
        self.toolbar.wait_window(self.vp.top)
        self.view_butt["state"] = "normal"

    def del_popup(self):
        info = 'Delete activities'
        m.stat.set(info)
        logging.debug(info)

        self.dp = delPopup(self.toolbar)
        self.del_butt["state"] = "disabled"
        self.toolbar.wait_window(self.dp.top)
        self.del_butt["state"] = "normal"


if __name__ == "__main__":
    root = Tk()
    m = mainWindow(root)
    root.mainloop()
