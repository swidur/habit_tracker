import Tkinter as tk


class SimpleTable(object):
    def __init__(self, parent, rows, columns):
        # use black background so it "peeks through" to
        # form grid lines

        self.frame = tk.Frame(parent, background="black")
        self.frame.pack(side = tk.TOP, fill = tk.X)
        self.frame._widgets = []
        self.b = tk.Button(self.frame, text='aaaaa', command=self.hide)
        self.b.grid(row=20)
        for row in range(rows):
            current_row = []

            for column in range(columns):
                label = tk.Label(self.frame, text="%s/%s" % (row, column),
                                 borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self.frame._widgets.append(current_row)

        for column in range(columns):
            self.frame.grid_columnconfigure(column, weight=1)

    def hide(self):
        tk.Frame.destroy(self.frame)
        print ('hide run')

    def set(self, row, column, value):
        widget = self.frame._widgets[row][column]
        widget.configure(text=value)


