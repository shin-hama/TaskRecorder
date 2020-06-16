import datetime

import tkinter as tk
import tkinter.ttk as ttk

STATUS_TEXT = ['waiting..', 'processing']


class TaskRecorder(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master, height=400, width=300)
        self.master.title('Hello World!')

        # columns name
        task_name = 'task'
        start_time = 'start'
        end_time = 'end'
        elapsed_time = 'total'
        self.columns = (task_name, start_time, end_time, elapsed_time)

        self.task = None
        self.create_widget()

    def create_widget(self):
        """ Design layout of ui
        """
        self.current_task = CurrentTask(self)
        self.current_task.grid(row=0, column=0)

        self.task_list = TaskList(self, self.columns)
        self.task_list.table_widget.grid(row=0, column=2, rowspan=4)

        self.text_box = tk.Entry(self)
        self.text_box.grid(row=1, column=0, columnspan=2)

        start_button = tk.Button(self, text='start', command=self.start_task)
        start_button.grid(row=2, column=0)

        end_button = tk.Button(self, text='end', command=self.end_task)
        end_button.grid(row=2, column=1)

        delete_button = tk.Button(self, text='delete',
                                  command=self.delete_task)
        delete_button.grid(row=3, column=0)

        cancel_button = tk.Button(self, text='cancel', command=self.cancel_task)
        cancel_button.grid(row=3, column=1)

    def start_task(self):
        """ Add task data in text box to Treeview
        """
        text = self.text_box.get()
        # Ignore empty text for not adding empty row.
        if text == '' or text.startswith(' '):
            self.text_box.delete(0, tk.END)
            return

        self.create_task(text)
        self.current_task.set_param(self.task)

        # Clear text box because make next usage to easier
        self.text_box.delete(0, tk.END)

    def create_task(self, task_name):
        """ Create task with name is inputted in text box
        """
        now = datetime.datetime.now()
        self.task = Task(self.columns, task=task_name, start=now)

    def end_task(self):
        """ Insert current task to task table and reset task
        """
        if self.task:
            self.task_list.insert(self.task)
            self.task = None
            self.current_task.set_param()

    def delete_task(self):
        """ Delete selected task from task list
        """
        self.task_list.delete_selected_items()

    def cancel_task(self):
        """ Reset current task
        """
        if self.task:
            self.task = None
            self.current_task.set_param()


class Task(object):
    """ Class for task data
    """

    def __init__(self, columns, **kwargs):
        # TODO: make to singletone
        self.info = {column: None for column in columns}
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
            if key in self.info:
                self.info[key] = value
            else:
                print('{} is not supportted.'.format(key))

    def get_all_info(self):
        """ Get task_info values as list
        """

        # Convert datetime to str since datetime is not readable.
        values = [value.strftime('%H:%M')
                  if isinstance(value, datetime.datetime) else value
                  for value in self.info.values()]

        return values


class CurrentTask(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.task_name = tk.StringVar()
        self.start = tk.StringVar()
        self.timer = tk.StringVar()

        self.task = None

        self.create_widget()

    def create_widget(self):
        self.set_param()
        task_label = tk.Label(self, textvariable=self.task_name)
        task_label.grid(row=0, column=0, columnspan=2)

        start_time = tk.Label(self, textvariable=self.start)
        start_time.grid(row=1, column=0)

        timer = tk.Label(self, textvariable=self.timer)
        timer.grid(row=1, column=1)

    def set_param(self, task=None):

        if task:
            self.task_name.set(task.info['task'])
            self.start.set(task.info['start'].strftime('%H:%M'))
            self.started_time = task.info['start']
            self.update_timer()
        else:
            self.task_name.set('resting')

            now = datetime.datetime.now().strftime('%H:%M')
            self.start.set(now)

            self.timer.set('sample')

    def update_timer(self):
        """ Display elapsed time from started task.
        """
        now = datetime.datetime.now()
        delta = now - self.started_time
        # remove micro seconds from timedelta object
        self.timer.set(str(delta).split('.')[0])
        # update timer text for each one second
        self.after(1000, self.update_timer)


class TaskList(tk.Frame):

    def __init__(self, master=None, columns=None):
        super().__init__(master)

        self.columns = columns

        # List of finished Task()
        self.task_list = []

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
            self.table_widget.heading(col, text=col.capitalize())
            self.table_widget.column(col, width=width)

    def insert(self, task):
        """ Insert task info at end of Treeview
        """
        now = datetime.datetime.now()
        delta = now - task.info['start']
        task.set_info(end=now)
        task.set_info(total=str(delta).split('.')[0])
        self.table_widget.insert('', index='end', values=task.get_all_info())

    def delete_selected_items(self):

        # Get id of selected rows will be deleted.
        items = self.table_widget.selection()
        for item in items:
            self.table_widget.delete(item)


def main():

    task_list = TaskRecorder()
    task_list.grid()
    task_list.mainloop()


if __name__ == "__main__":
    main()
