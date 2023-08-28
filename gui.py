import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
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

        self.top_three_countries_checked = tk.IntVar()
        self.top_three_countries = ttk.Checkbutton(self.root, text='Get top 3 countries', onvalue=1, offvalue=0, variable=self.top_three_countries_checked)
        self.top_three_countries.pack()

        execute_button = tk.Button(self.root, text="Execute", command=self.execute_program)
        execute_button.pack()

        self.output_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=180, height=50)
        self.output_text.pack()

    def execute_program(self):
        year_choice = self.year_combobox.get()
        region_choice = self.region_combobox.get()
        top_three_countries_checked = self.top_three_countries_checked.get()

        if year_choice and region_choice:
            # take the output of the analysis in a variable
            year_mapping = {"1978-1987": 1, "1988-1997": 2, "1998-2007": 3, "2008-2017": 4}
            region_mapping = {"Asia": 1, "Europe": 2, "Others": 3}
            parsed_data = self.utils.parseData(year_mapping[year_choice], region_mapping[region_choice])

            # clear the scrolled text widget and insert the captured output
            self.output_text.delete(1.0, tk.END)  # clear the existing content
            self.output_text.insert(tk.END, parsed_data)

            if top_three_countries_checked == 1:
                output = self.utils.getTop3Countries(parsed_data)
                self.output_text.insert(tk.END, '\n\n*** Top 3 Countries ***\n')
                self.output_text.insert(tk.END, output)




if __name__ == '__main__':
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()
