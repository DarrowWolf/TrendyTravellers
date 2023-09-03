import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from main import VisitorsAnalyticsUtils, DataLoader
from fpdf import FPDF


class GUIApp:
    def __init__(self, root):
        self.root = root  # root is the main window
        self.root.title("Visitors Analytics")  # set the title of the window
        self.create_widgets()  # call the create_widgets function
        self.data_loader = DataLoader()  # create an instance of the DataLoader class
        self.utils = VisitorsAnalyticsUtils()  # create an instance of the VisitorsAnalyticsUtils class
        self.fig = None  # create a placeholder for the Matplotlib figure
        self.original_fig_size = (12, 6)  # Store the original size of the graph
        self.root.protocol("WM_DELETE_WINDOW", self._quit)  # handle the closing of the window
    
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

        help_button = tk.Button(self.root, text="Help", command=self.show_help)
        help_button.pack()


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
        if self.fig is not None:
            self.visualize_data(self.parsed_data)

    def generate_report(self):
        if hasattr(self, 'top_countries'):
            generate_report(self.top_countries, self.fig, self.original_fig_size)
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
            self.fig = plt.figure(figsize=self.original_fig_size)  # Use the original size of the graph
            ax = transposed_data.plot(kind='bar', stacked=True, ax=self.fig.gca())
            plt.xlabel("Countries")
            plt.ylabel("Number of Visitors")
            plt.title(f"Visitor Trends by Country in the Selected Region")
            plt.xticks(rotation=45)

            ax.legend(loc='upper left', bbox_to_anchor=(1, 1), title='Years')
            plt.tight_layout()

            self.canvas.get_tk_widget().pack_forget()
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
            self.canvas.get_tk_widget().pack()
        else:
            tk.messagebox.showerror(title='Error', message='No data available for visualization.')
            print("Error: No data available for visualization.")

    def export_graph(self):
        if self.fig is not None:
            file_path = filedialog.asksaveasfilename(initialfile="graph", defaultextension=".png",filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")])

            if file_path:

                self.fig.set_size_inches(12, 6)
                self.fig.savefig(file_path)

                # Display a success message
                tk.messagebox.showinfo(title='Success', message='Graph downloaded successfully.')
        else:
            tk.messagebox.showerror(title='Error', message='No graph available to export.')


    def show_help(self):
        try:
            with open('help_doc.txt', 'r') as help_file:
                help_text = help_file.read()

            help_window = tk.Toplevel(self.root)
            help_window.title("Help Documentation")
            
            help_text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, width=80, height=30)
            help_text_widget.pack(expand=True, fill='both')
            help_text_widget.insert(tk.END, help_text)
            help_text_widget.config(state=tk.DISABLED)

        except FileNotFoundError:
            tk.messagebox.showerror(title='Error', message='Help documentation not found.')

    def _quit(self):
        self.root.quit()
        self.root.destroy()

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Visitors Analytics Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

def generate_report(data, fig, original_fig_size):
    if not data.empty and fig is not None:
        pdf = PDF()
        pdf.add_page()

        pdf.set_font('Arial', '', 12)

        # Add the data to the PDF 
        region_choice = app.region_combobox.get()  # Get user-selected region
        pdf.cell(0, 10, f'Region of visitors: {region_choice}', 0, 1)

        # Save the original size of the graph to a temporary file
        original_fig_file_path = 'graph.png'
        fig.set_size_inches(original_fig_size)
        fig.savefig(original_fig_file_path)

        # Add the original size graph from the image file to the PDF
        pdf.image(original_fig_file_path, x=10, y=pdf.get_y() + 10, w=190)
        pdf.ln(110)

        # Add the top 3 countries data to the PDF
        pdf.cell(0, 10, 'Number of visitors from top 3 countries within region:', 0, 1)
        for country, visitors in data.items():
            pdf.cell(0, 10, f'{country}: {visitors}', 0, 1)

        # Output the PDF
        pdf.output('report.pdf', 'F')

        # Clear the Matplotlib figure after saving it as an image
        plt.close(fig)

    else:
        tk.messagebox.showerror(title='Error', message='No graph or top 3 countries data available to generate a report.')



if __name__ == '__main__':
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()