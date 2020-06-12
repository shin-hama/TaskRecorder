import datetime

import tkinter as tk
import tkinter.ttk as ttk

STATUS_TEXT = ['waiting..', 'processing']


class TaskRecorder(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        # columns name
        task_name = 'Task'
        start_time = 'Start'
        end_time = 'End'
        elapsed_time = 'Total'
        self.columns = (task_name, start_time, end_time, elapsed_time)

        # set widget
        self.task_name = tk.StringVar()
        self.task_name.set('resting')
        self.current_task = ttk.Label(master, textvariable=self.task_name)
        self.current_task.grid(row=0, column=0)
        self.text_box = tk.Entry()
        self.text_box.grid(row=1, column=0, columnspan=2)

        self.task_list = TaskList(master, self.columns)
        self.task_list.table_widget.grid(row=0, column=2, rowspan=4)

        start_button = tk.Button(master, text='start', command=self.start_task)
        start_button.grid(row=2, column=0)

        end_button = tk.Button(master, text='end', command=self.end_task)
        end_button.grid(row=2, column=1)
        delete_button = tk.Button(master, text='delete',
                                  command=self.delete_task)

        delete_button.grid(row=3)

    def start_task(self):
        """ Add task data in text box to Treeview
        """
        text = self.text_box.get()
        # Ignore empty text for not adding empty row.
        if text == '' or text.startswith(' '):
            self.text_box.delete(0, tk.END)
            return

        self.task_name.set(text)
        self.task_list.insert(text)

        # Clear text box because make next usage to easier
        self.text_box.delete(0, tk.END)

    def end_task(self):
        pass

    def delete_task(self):
        index = self.Tasklist.curselection()
        if index == ():
            print('test')
            return
        self.task_list.delete(index)


class TaskList(tk.Frame):

    class Task(object):
        """ Class for task data
        """

        def __init__(self, columns, **kwargs):
            self.task_info = {column: None for column in columns}
            if len(kwargs) > 0:
                self.set_info(**kwargs)

        def set_info(self, **kwargs):
            """ Set values corresponding to the column name.

            Parameters
            ----------
            **kwargs : dict
                Set values to task_info when key is same as columns name
                If key is difference, ignore the value.
            """

            for key, value in kwargs.items():
                if key in self.task_info:
                    self.task_info[key] = value
                else:
                    print('{} is not supportted.'.format(key))

        def get_info(self):
            """ Get task_info values as list
            """
            return [value for value in self.task_info.values()]

    def __init__(self, master=None, columns=None):

        self.columns = columns

        self.create_widget(master)

    def create_widget(self, master):
        self.table_widget = ttk.Treeview(master)
        self.table_widget['show'] = 'headings'
        self._set_columns()

    def _set_columns(self):
        """ Set columns name of Treeview
        """
        self.table_widget['columns'] = self.columns
        # Set each columns width that is splitted by the number of columns
        width = 300 // len(self.columns)
        for col in self.columns:
            self.table_widget.heading(col, text=col)
            self.table_widget.column(col, width=width)

    def insert(self, task_name):
        """ Insert task info at end of Treeview
        """
        now = datetime.datetime.now().strftime('%H:%M')
        task = self.Task(self.columns, Task=task_name, Start=now)
        iid = self.table_widget.insert('', index='end', values=task.get_info())
        print(iid)


def main():

    root = tk.Tk()
    root.title('Hello World!')
    # window size + window position
    root.geometry('400x300+1000+10')

    task_list = TaskRecorder(master=root)

    root.mainloop()


if __name__ == "__main__":
    main()
