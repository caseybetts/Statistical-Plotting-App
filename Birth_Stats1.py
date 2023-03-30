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
        self.geometry("1100x600")           # Window size
        self.gridWidth = 11                 # Number of columns
        self.gridHeight = 11                # Number of rows

        # Define widget properties
        self.age_graph_toggles = []     # A list of Radio buttons for changing age of the graph
        self.age_plot_toggles = []      # A list of check buttons for changing plotted data
        self.plot_span = 10             # Number of columns the graph should span
        self.age_radio_var = IntVar()   # Varable for the age range radio buttons
        

        # Define rows and columns
        self.title_start_row = 0
        self.section1_start_row = 1     # Options
        self.section2_start_row = 2     # Age Radio Buttons
        self.section3_start_row = 3     # Start of Graph and Checkboxes
        self.section4_start_row = 15    # Order Radio Buttons
        self.section5_start_row = 16    # Start of Graph and Checkboxes

        self.left_side_column = 0       # Checkboxes 
        self.plot_start_column = 1      # Graphs
        self.start_date_label_column = 2       # Start Date Label
        self.start_date_column = 3      # Start Date Text Box
        self.end_date_label_column = 4         # End Date Label
        self.end_date_column = 5        # End Date Text Box

            

        # Creating the checkbuttons
        for i in range(len(orders)):
            # Checkbuttons for each birth order
            temp_button = ttk.Checkbutton(self, text=orders[i], command = self.update_plot)
            temp_button.state(['!alternate'])
            self.age_plot_toggles.append(temp_button)

        # Checkbutton for the y-zoom option
        self.bottom_at_zero = ttk.Checkbutton(self, text="zoom y-axix", command = self.update_plot)
        self.bottom_at_zero.state(['!alternate'])

        # Creating the radiobuttons
        for i in range(len(ages)):
            # Radiobutton for each age range
            temp_button = ttk.Radiobutton(self, text=ages[i], command=self.update_plot, variable= self.age_radio_var, value= i)
            self.age_graph_toggles.append(temp_button)

        # Create text entry boxes for date range input
        self.start_date = ttk.Entry(self, width = 19)
        self.end_date = ttk.Entry(self, width = 19)

        # Create labels for the date range text entry boxes
        self.start_date_label = ttk.Label(text= 'Start Date')
        self.end_date_label = ttk.Label(text= 'End Date')
            

    def update_plot(self):
        # This function will update the chart to include the active plots

        # This variable is based on the currently selected age radio button
        current_age = ages[self.age_radio_var.get()]
        
        # Clear the figure
        self.figure.clf()

        # Update the figure canvas
        self.chart = FigureCanvasTkAgg(self.figure,self)
        self.chart.get_tk_widget().grid(column=self.plot_start_column, row=self.section3_start_row, columnspan=self.plot_span, rowspan=self.plot_span)
        
        # Update the axis with a subplot
        self.ax1 = self.figure.add_subplot(111)
        
        # Create the ax properties
        self.legend_list = []

        # Plot data if the checkbox is selected
        for i in range(len(self.age_plot_toggles)):
            
            if 'selected' in self.age_plot_toggles[i].state():
                self.all_data[i][self.age_radio_var.get()].plot('Year', 'Births', kind='line', legend=True, ax=self.ax1) 
                self.legend_list.append(orders[i])
                self.ax1.legend(self.legend_list)

                if 'selected' not in self.bottom_at_zero.state():
                    self.ax1.set_ylim(bottom=0)

    def make_window(self):
        # Create the structure of widgets inside the main window
        print("running make_window")
        
        # Placing the graph toggle radio button in the window
        i = 0
        for radiobutton in self.age_graph_toggles:
            radiobutton.grid(column= self.left_side_column + i, row= self.section2_start_row)
            i+=1

        # Placing the plot toggle check buttons in the window
        i = 0
        for checkbutton in self.age_plot_toggles:
            checkbutton.grid(column=self.left_side_column, row= self.section3_start_row+i)
            i+=1

        # Placing the bottom-at-zero checkbox
        self.bottom_at_zero.grid(column = self.left_side_column, row=self.section1_start_row)

        # Create the space for the plots
        self.figure = plt.Figure(figsize=(8,5), dpi=100)
        self.ax1 = self.figure.add_subplot(111)
        self.ax1.set_title('Births per Year')
        self.chart = FigureCanvasTkAgg(self.figure,self)
        self.chart.get_tk_widget().grid(column=self.plot_start_column, row=self.section3_start_row, columnspan=self.plot_span, rowspan=self.plot_span)

        # Place the date range text boxes
        self.start_date.grid(column= self.start_date_column, row= self.section1_start_row)
        self.end_date.grid(column= self.end_date_column, row= self.section1_start_row)

        # Place the date range labels
        self.start_date_label.grid(column= self.start_date_label_column, row= self.section1_start_row)
        self.end_date_label.grid(column= self.end_date_label_column, row= self.section1_start_row)


    def make_plot_data(self, birth_df):

        self.all_data = []

        for i in range(len(orders)):
            temp_list = []
            for j in range(len(ages)):
                temp_list.append(birth_df[(birth_df['Birth Order'] == orders[i]) & (birth_df['Age Group'] == ages[j])])
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