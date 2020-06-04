import tkinter as tk
import tkinter.ttk as ttk

STATUS_TEXT = ['waiting..', 'processing']


class TaskRecorder(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        task_name = 'Task name'
        start_time = 'Start time'
        end_time = 'End time'
        elapsed_time = 'Elapsed time'
        self.columns = (task_name, start_time, end_time, elapsed_time)
        self.task_list = TaskList(master, self.columns)

        self.text_box = tk.Entry()
        self.text_box.pack()

        button = tk.Button(master, text='add', command=self.add_task)
        button.pack()

        button = tk.Button(master, text='delete', command=self.delete_task)
        button.pack()

    def add_task(self):
        text = self.text_box.get()
        if text == '' or text.startswith(' '):
            self.text_box.delete(0, tk.END)
            return

        self.Tasklist.insert('end', {text: 2})
        self.text_box.delete(0, tk.END)

    def delete_task(self):
        index = self.Tasklist.curselection()
        if index == ():
            print('test')
            return
        self.Tasklist.delete(index)


class TaskList(tk.Frame):

    def __init__(self, master=None, columns=None):

        self.columns = columns
        self.task_list = ttk.Treeview(master)
        self.task_list['show'] = 'headings'
        self._set_columns()

        self.task_list.pack()

    def _set_columns(self):
        self.task_list['columns'] = self.columns
        width = 300 // len(self.columns)
        for col in self.columns:
            self.task_list.heading(col, text=col)
            self.task_list.column(col, width=width)


def main():

    root = tk.Tk()
    root.title('Hello World!')
    # window size + window position
    root.geometry('400x300+1000+10')

    task_list = TaskRecorder(master=root)

    root.mainloop()


if __name__ == "__main__":
    main()
