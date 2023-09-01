import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from main import VisitorsAnalyticsUtils, DataLoader
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Visitors Analytics Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

def generate_report(data):
    pdf = PDF()
    pdf.add_page()

    pdf.set_font('Arial', '', 12)

    # add the data to the PDF
    region_choice = app.region_combobox.get()# get user selected region
    pdf.cell(0, 10, f'Region of vistors: {region_choice}', 0, 1)

    pdf.cell(0, 10, 'Number of visitors from top 3 countries within region:', 0, 1)
    for country, visitors in data.items():
        pdf.cell(0, 10, f'{country}: {visitors}', 0, 1)

    pdf.output('report.pdf')

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visitors Analytics")
        self.create_widgets()
        self.data_loader = DataLoader()
        self.utils = VisitorsAnalyticsUtils()
        self.fig = None
        self.root.protocol("WM_DELETE_WINDOW", self._quit)
    
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

        visualize_button = tk.Button(self.root, text="Visualize Data", command=self.visualize_data_and_execute)
        visualize_button.pack()

        export_graph_button = tk.Button(self.root, text="Download graph", command=self.export_graph)
        export_graph_button.pack()

        generate_report_button = tk.Button(self.root, text="Generate Report", command=self.generate_report)
        generate_report_button.pack()

        # Create a placeholder for the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(plt.figure(), master=self.root)
        self.canvas.get_tk_widget().pack()
        self.canvas.get_tk_widget().pack_forget()  # Hide the canvas initially until called and drawn

        self.output_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=180, height=30, state=tk.DISABLED)
        self.output_text.pack()

    def visualize_data_and_execute(self):
        self.visualize_data()
        self.execute_program()    

    def execute_program(self):
        year_choice = self.year_combobox.get()
        region_choice = self.region_combobox.get()

        if self.year_combobox.get() == "" or self.region_combobox.get() == "":
            tk.messagebox.showerror(title='Error', message='Please select a year period and region!')
            print("Error: Please select a year period and region!")
            return

        if year_choice and region_choice:
            year_mapping = {"1978-1987": 1, "1988-1997": 2, "1998-2007": 3, "2008-2017": 4}
            region_mapping = {"Asia": 1, "Europe": 2, "Others": 3}
            self.parsed_data = self.data_loader.parseData(year_mapping[year_choice], region_mapping[region_choice])

            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, self.parsed_data)
            self.output_text.config(state=tk.DISABLED)

            top_three_countries_checked = self.top_three_countries_checked.get()
            if top_three_countries_checked == 1:
                self.output_text.config(state=tk.NORMAL)
                self.top_countries = self.utils.getTop3Countries(self.parsed_data)
                self.output_text.insert(tk.END, '\n\n*** Top 3 Countries ***\n')
                self.output_text.insert(tk.END, self.top_countries)
                self.output_text.config(state=tk.DISABLED)

    def generate_report(self):
        if hasattr(self, 'top_countries'):
            generate_report(self.top_countries)
        else:
            tk.messagebox.showerror(title='Error', message='Please execute the program first to get the top 3 countries.')

    def visualize_data(self, parsed_data=None):
        if parsed_data is None:
            year_choice = self.year_combobox.get()
            region_choice = self.region_combobox.get()

            if year_choice and region_choice:
                year_mapping = {"1978-1987": 1, "1988-1997": 2, "1998-2007": 3, "2008-2017": 4}
                region_mapping = {"Asia": 1, "Europe": 2, "Others": 3}
                parsed_data = self.data_loader.parseData(year_mapping[year_choice], region_mapping[region_choice])

        if parsed_data is not None:
            parsed_data = parsed_data.drop_duplicates(subset=['year'], keep='first')
            transposed_data = parsed_data.set_index('year').T

            if self.fig is not None:
                plt.close(self.fig)
            self.fig = plt.figure(figsize=(12, 6))
            ax = transposed_data.plot(kind='bar', stacked=True, ax=self.fig.gca())
            plt.xlabel("Countries")
            plt.ylabel("Number of Visitors")
            plt.title(f"Visitor Trends by Country in the Selected Region")
            plt.xticks(rotation=45)

            ax.legend(loc='upper left', bbox_to_anchor=(1, 1), title = 'Years')
            plt.tight_layout()

            self.canvas.get_tk_widget().pack_forget()
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
            self.canvas.get_tk_widget().pack()
        else:
            tk.messagebox.showerror(title='Error', message='No data available for visualization.')
            print("Error: No data available for visualization.")

    def export_graph(self):
        if self.fig is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")])

            if file_path:
                self.fig.savefig(file_path)
        else:
            tk.messagebox.showerror(title='Error', message='No graph available to export.')
            print("Error: No graph available to export.")

    def _quit(self):
        self.root.quit()
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()
