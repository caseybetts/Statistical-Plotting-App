# This script will process data from a birth stats .csv and produce graphics
# By Casey Betts March 2023

import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

### Global Variables ###

# .csv file location
file_location = "Pop Stats - Numeric Data.csv"

# Create list for ages and birth orders
ages = ['All ages', 'Under 15', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54']
orders = ['Total', '1st Born', '2nd Born', '3rd Born', '4th Born', '5th Born', '6th Born', '7th Born', '8th child and over', 'Not Stated']
birth_plots = ['age', 'order']


### Main Class ### 

class InteractivePlotter(Tk):
    # This is a child of a tkinter object class

    def __init__(self):
        super().__init__()

        # Define window attributes
        self.title("Birth Stats Plotter")   # Window title
        self.geometry("1100x1000")          # Window size
        self.gridWidth = 22                 # Number of columns
        self.gridHeight = 22                # Number of rows
        self.fig_height = 4                 # Figure height
        self.fig_width = 5                  # Figure width
        self.dpi = 100                      # Dots per inch on the figures

        # Define widget properties
        self.age_graph_toggles = []     # A list of Radio buttons for changing age range displayed on figure a
        self.order_graph_toggles = []   # A list of Radio buttons for changing birth order displayed on figure b
        self.age_plot_toggles = []      # A list of check buttons for changing plotted age ranges
        self.order_plot_toggles = []    # A list of check buttons for changing plotted birth orders
        self.plot_span = 10             # Number of columns the graph should span
        self.age_radio_var = IntVar()   # Varable for the age range radio buttons
        self.order_radio_var = IntVar() # Variable for the order radio buttons
        

        # Define rows and columns
        self.title_start_row = 0
        self.section1a_start_row = 1     # Options
        self.section2a_start_row = 2     # Age Radio Buttons
        self.section3a_start_row = 3     # Start of Graph and Checkboxes
        self.section4a_start_row = 15    # Order Radio Buttons
        self.section5a_start_row = 16    # Start of Graph and Checkboxes
        self.title_start_rowb = 17
        self.section1b_start_row = 18     # Options
        self.section2b_start_row = 19     # age Radio Buttons
        self.section3b_start_row = 20     # Start of Graph and Checkboxes
        self.section4b_start_row = 21    # Order Radio Buttons
        self.section5b_start_row = 22    # Start of Graph and Checkboxes

        self.left_side_column = 0           # Checkboxes 
        self.plot_start_column = 1          # Graphs
        self.start_date_label_column = 2    # Start Date Label
        self.start_date_column = 3          # Start Date Text Box
        self.end_date_label_column = 4      # End Date Label
        self.end_date_column = 5            # End Date Text Box

            

        # Creating the checkbuttons
        for order in orders:
            # Checkbuttons for each birth order
            temp_button = ttk.Checkbutton(self, text=order, command = self.update_plot_a)
            temp_button.state(['!alternate'])
            self.age_plot_toggles.append(temp_button)

        for age_range in ages:
            # Checkbuttons for each age range
            temp_button = ttk.Checkbutton(self, text=age_range, command = self.update_plot_b)
            temp_button.state(['!alternate'])
            self.order_plot_toggles.append(temp_button)

        # Checkbutton for the y-zoom option
        self.bottom_at_zero = ttk.Checkbutton(self, text="zoom y-axix", command = self.update_plot_a)
        self.bottom_at_zero.state(['!alternate'])

        # Creating the radiobuttons
        for index, age_range in enumerate(ages):
            # Radiobutton for each age range
            temp_button = ttk.Radiobutton(self, text=age_range, command=self.update_plot_a, variable= self.age_radio_var, value= index)
            self.age_graph_toggles.append(temp_button)

        for index, order in enumerate(orders):
            # Radiobutton for each birth order
            temp_button = ttk.Radiobutton(self, text=order, command=self.update_plot_b, variable= self.order_radio_var, value= index)
            self.order_graph_toggles.append(temp_button)

        # Create text entry boxes for date range input
        self.start_date = ttk.Entry(self, width = 19)
        self.end_date = ttk.Entry(self, width = 19)

        # Create labels for the date range text entry boxes
        self.start_date_label = ttk.Label(text= 'Start Date')
        self.end_date_label = ttk.Label(text= 'End Date')
            

    def update_plot_a(self):
        # This function will update the top chart to include the active plots

        # This variable is based on the currently selected age radio button
        current_age = ages[self.age_radio_var.get()]
        
        # Clear the figure
        self.figure_a.clf()

        # Update the figure canvas
        self.chart_a = FigureCanvasTkAgg(self.figure_a,self)
        self.chart_a.get_tk_widget().grid(column=self.plot_start_column, row=self.section3a_start_row, columnspan=self.plot_span, rowspan=self.plot_span)
        
        # Update the axis with a subplot
        self.ax_a = self.figure_a.add_subplot(111)
        
        # Create the ax properties
        self.legend_list_a = []

        # Plot data if the checkbox is selected
        for index, toggle in enumerate(self.age_plot_toggles):
            
            if 'selected' in toggle.state():
                self.all_data[index][self.age_radio_var.get()].plot('Year', 'Births', kind='line', legend=True, ax=self.ax_a) 
                self.legend_list_a.append(orders[index])
                self.ax_a.legend(self.legend_list_a)

                if 'selected' not in self.bottom_at_zero.state():
                    self.ax_a.set_ylim(bottom=0)

    def update_plot_b(self):
        # This function will update the bottom chart to include the active plots

        # This variable is based on the currently selected order radio button
        current_order = orders[self.order_radio_var.get()]
        
        # Clear the figure
        self.figure_b.clf()

        # Update the figure canvas
        self.chart_b = FigureCanvasTkAgg(self.figure_b,self)
        self.chart_b.get_tk_widget().grid(column=self.plot_start_column, row=self.section3b_start_row, columnspan=self.plot_span, rowspan=self.plot_span)
        
        # Update the axis with a subplot
        self.ax_b = self.figure_b.add_subplot(111)
        
        # Create the ax properties
        self.legend_list_b = []

        # Plot data if the checkbox is selected
        for index, toggle in enumerate(self.order_plot_toggles):
            
            if 'selected' in toggle.state():
                self.all_data[self.order_radio_var.get()][index].plot('Year', 'Births', kind='line', legend=True, ax=self.ax_b) 
                self.legend_list_b.append(ages[index])
                self.ax_b.legend(self.legend_list_b)

                if 'selected' not in self.bottom_at_zero.state():
                    self.ax_b.set_ylim(bottom=0)

    def make_window(self):
        # Create the structure of widgets inside the main window
        print("running make_window")
        
        # Placing the graph toggle radio button in the window
        i = 0
        for radiobutton in self.age_graph_toggles: # Age range toggles
            radiobutton.grid(column= self.left_side_column + i, row= self.section2a_start_row)
            i+=1

        i = 0
        for radiobutton in self.order_graph_toggles: # Birth order toggles
            radiobutton.grid(column= self.left_side_column + i, row= self.section2b_start_row)
            i+=1

        # Placing the plot toggle check buttons in the window
        i = 0
        for checkbutton in self.age_plot_toggles: # Age range toggles
            checkbutton.grid(column=self.left_side_column, row= self.section3a_start_row+i)
            i+=1

        i = 0
        for checkbutton in self.order_plot_toggles: # Birth order toggles
            checkbutton.grid(column=self.left_side_column, row= self.section3b_start_row+i)
            i+=1

        # Placing the bottom-at-zero checkbox
        self.bottom_at_zero.grid(column = self.left_side_column, row=self.section1a_start_row)

        # Create the space for the top plots
        self.figure_a = plt.Figure(figsize=(self.fig_width,self.fig_height), dpi=self.dpi)
        self.ax_a = self.figure_a.add_subplot(111)
        self.ax_a.set_title('Births per Year by Age Range')
        self.chart_a = FigureCanvasTkAgg(self.figure_a,self)
        self.chart_a.get_tk_widget().grid(column=self.plot_start_column, row=self.section3a_start_row, columnspan=self.plot_span, rowspan=self.plot_span)

       # Create the space for the bottom plots
        self.figure_b = plt.Figure(figsize=(self.fig_width,self.fig_height), dpi=self.dpi)
        self.ax_b = self.figure_b.add_subplot(111)
        self.ax_b.set_title('Births per Year by Order')
        self.chart_b = FigureCanvasTkAgg(self.figure_b,self)
        self.chart_b.get_tk_widget().grid(column=self.plot_start_column, row=self.section3b_start_row, columnspan=self.plot_span, rowspan=self.plot_span)

        # Place the date range text boxes
        self.start_date.grid(column= self.start_date_column, row= self.section1a_start_row)
        self.end_date.grid(column= self.end_date_column, row= self.section1a_start_row)

        # Place the date range labels
        self.start_date_label.grid(column= self.start_date_label_column, row= self.section1a_start_row)
        self.end_date_label.grid(column= self.end_date_label_column, row= self.section1a_start_row)


    def make_plot_data(self, birth_df):

        self.all_data = []

        for order in orders:
            temp_list = []
            for age_range in ages:
                temp_list.append(birth_df[(birth_df['Birth Order'] == order) & (birth_df['Age Group'] == age_range)])
            self.all_data.append(temp_list)
    

    def load_data(self, file_loc):
        # Read in the .csv data
        return pd.read_csv(file_loc)

    def create_dataframe(self):
        # Melt the age columns into rows
        Births = pd.melt(self.load_data(file_location), 
                                id_vars=['Year', 'Birth Order'],
                                value_vars=['All ages','Under 15', '15-19', '15-17', '18-19', '15', '16', '17', '18', '19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54'],
                                var_name='Age Group',
                                value_name='str_Births')

        # Change Births data type to int
        Births['Births'] = pd.to_numeric(Births.str_Births, downcast="integer")

        # Remove the str_Births column
        Births.drop(labels=['str_Births'], axis=1, inplace=True)


        return Births


if __name__ == "__main__":

    print("runing main")

    window = InteractivePlotter()
    print("main after make_window")
    window.make_window()
    window.make_plot_data(window.create_dataframe())


    window.mainloop()