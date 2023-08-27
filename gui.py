import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import sys
from main import VisitorsAnalyticsUtils

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visitors Analytics")
        self.create_widgets()
        self.utils = VisitorsAnalyticsUtils()

    def create_widgets(self):
        year_label = tk.Label(self.root, text="Select Year Period:")
        year_label.pack()
        self.year_combobox = ttk.Combobox(self.root, values=["1978-1987", "1988-1997", "1998-2007", "2008-2017"])
        self.year_combobox.pack()

        region_label = tk.Label(self.root, text="Select Region:")
        region_label.pack()
        self.region_combobox = ttk.Combobox(self.root, values=["Asia", "Europe", "Others"])
        self.region_combobox.pack()

        execute_button = tk.Button(self.root, text="Execute", command=self.execute_program)
        execute_button.pack()

        self.output_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=130, height=10)
        self.output_text.pack()

    def execute_program(self):
        year_choice = self.year_combobox.get()
        region_choice = self.region_combobox.get()

        if year_choice and region_choice:
            # Capture the output of the analysis in a variable
            year_mapping = {"1978-1987": 1, "1988-1997": 2, "1998-2007": 3, "2008-2017": 4}
            region_mapping = {"Asia": 1, "Europe": 2, "Others": 3}
            output = self.utils.parseData(year_mapping[year_choice], region_mapping[region_choice])
            
            # Clear the ScrolledText widget and insert the captured output
            self.output_text.delete(1.0, tk.END)  # Clear the existing content
            self.output_text.insert(tk.END, output)

            # Reset sys.stdout to the original stdout
            sys.stdout = sys.__stdout__


if __name__ == '__main__':
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()
