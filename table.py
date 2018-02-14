import Tkinter as tk


class SimpleTable(object):
    def __init__(self, parent, rows, columns):
        # use black background so it "peeks through" to
        # form grid lines

        self.frame = tk.Frame(parent)
        self.frame._widgets = []
        self.frame.pack(fill=tk.X)


        for row in range(rows):
            current_row = []

            for column in range(columns):
                if column == 0:

                        label = tk.Label(self.frame,
                                         borderwidth=1, width=6, relief=tk.SUNKEN)
                        label.grid(row=row, column=column, ipadx=1, ipady=1)

                        current_row.append(label)

                else:

                    if row == 0:
                        label = tk.Label(self.frame, fg='black', text="%s/%s" % (row, column),
                                         borderwidth=1, width=10,relief = tk.RIDGE)
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                        label.config(font=("Arial", 9, 'bold'))

                    elif row > 0:
                        label = tk.Label(self.frame, text="%s/%s" % (row, column),
                                 borderwidth=1, width=10, relief = tk.SUNKEN)
                        label.grid(row=row, column=column, sticky="nsew", ipadx=1, ipady=1)

                    current_row.append(label)
            self.frame._widgets.append(current_row)

        for column in range(columns):
            self.frame.grid_columnconfigure(column, weight=1)




    def set(self, row, column, value):
        widget = self.frame._widgets[row][column]
        widget.configure(text=value)
