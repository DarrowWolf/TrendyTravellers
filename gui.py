import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from main import VisitorsAnalyticsUtils

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visitors Analytics")
        self.create_widgets()
        self.utils = VisitorsAnalyticsUtils()
        self.fig = None
        self.root.protocol("WM_DELETE_WINDOW", self._quit)
    
    # This function is called when the user clicks the "Visualize Data" button to visualize the data and execute the program
    def visualize_data_and_execute(self):
        self.visualize_data()
        self.execute_program()
        
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

        # Create a placeholder for the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(plt.figure(), master=self.root)
        self.canvas.get_tk_widget().pack()
        self.canvas.get_tk_widget().pack_forget()  # Hide the canvas initially until called and drawn

        self.output_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=180, height=40, state=tk.DISABLED)
        self.output_text.pack()

    def execute_program(self):
        year_choice = self.year_combobox.get()
        region_choice = self.region_combobox.get()

        # checks if year_choice and region_choice is not empty
        if self.year_combobox.get() == "" or self.region_combobox.get() == "":
            tk.messagebox.showerror(title='Error', message='Please select a year period and region!')
            print("Error: Please select a year period and region!")
            return

        if year_choice and region_choice:
            # Take the output of the analysis in a variable
            year_mapping = {"1978-1987": 1, "1988-1997": 2, "1998-2007": 3, "2008-2017": 4}
            region_mapping = {"Asia": 1, "Europe": 2, "Others": 3}
            parsed_data = self.utils.parseData(year_mapping[year_choice], region_mapping[region_choice])

            # Clear the scrolled text widget and insert the captured output
            self.output_text.config(state=tk.NORMAL) # tk.NORMAL allows users to type into the text box, also need to set it to NORMAL or else it won't insert.
            self.output_text.delete(1.0, tk.END)  # Clear the existing content
            self.output_text.insert(tk.END, parsed_data)
            self.output_text.config(state=tk.DISABLED) # tk.DISABLE doesn't allow users to type into text box. .insert won't work if set to disable

            # Get top 3 countries if the checkbox is checked
            top_three_countries_checked = self.top_three_countries_checked.get()
            if top_three_countries_checked == 1: # if the checkbox is checked, it will go to this line
                self.output_text.config(state=tk.NORMAL)
                output = self.utils.getTop3Countries(parsed_data)
                self.output_text.insert(tk.END, '\n\n*** Top 3 Countries ***\n')
                self.output_text.insert(tk.END, output)
                self.output_text.config(state=tk.DISABLED)


            

    def visualize_data(self, parsed_data=None):
        if parsed_data is None:
            # If parsed_data is not provided, try to fetch it from the execute_program function
            year_choice = self.year_combobox.get()
            region_choice = self.region_combobox.get()

            if year_choice and region_choice:
                year_mapping = {"1978-1987": 1, "1988-1997": 2, "1998-2007": 3, "2008-2017": 4}
                region_mapping = {"Asia": 1, "Europe": 2, "Others": 3}
                parsed_data = self.utils.parseData(year_mapping[year_choice], region_mapping[region_choice])

        if parsed_data is not None:
            # Remove duplicate years before plotting
            parsed_data = parsed_data.drop_duplicates(subset=['year'], keep='first')

            # Transpose the data for plotting
            transposed_data = parsed_data.set_index('year').T

            # Create a stacked bar chart
            if self.fig is not None:
                plt.close(self.fig)  # Close the previous figure to avoid overlapping
            self.fig = plt.figure(figsize=(12, 6))  # Set the size of the plot
            ax = transposed_data.plot(kind='bar', stacked=True, ax=self.fig.gca())
            plt.xlabel("Countries")
            plt.ylabel("Number of Visitors")
            plt.title(f"Visitor Trends by Country in the Selected Region")
            plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

            # place the year legend outside the plot area to the right
            ax.legend(loc='upper left', bbox_to_anchor=(1, 1), title = 'Years')
            plt.tight_layout()

            # update the graph figure on the canvas
            self.canvas.get_tk_widget().pack_forget()  # hide the previous canvas
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
            self.canvas.get_tk_widget().pack()  # show the new canvas
        else:
            # error handling if parsed_data is not available
            tk.messagebox.showerror(title='Error', message='No data available for visualization.')
            print("Error: No data available for visualization.")

    def export_graph(self):
        # check if figure is available to export
        # if available, it opens a file dialog to save the graph
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