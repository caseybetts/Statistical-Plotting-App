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
ages = ['Under 15', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54']
orders = ['Total', '1st Born', '2nd Born', '3rd Born', '4th Born', '5th Born', '6th Born', '7th Born', '8th child and over', 'Not Stated']
birth_plots = ['age', 'order']


### Main Class ### 

class InteractivePlotter(Tk):
    # This is a child of a tkinter object class

    def __init__(self):
        super().__init__()

        # Define window attributes
        self.title("Birth Stats Plotter")
        self.geometry("1000x600")
        self.gridWidth = 11
        self.gridHeight = 11

        # Define widget properties
        self.age_plot_toggles = [] # A list of radio buttons
        self.orders = ['Total', '1st Born', '2nd Born', '3rd Born', '4th Born', '5th Born', '6th Born', '7th Born', '8th child and over', 'Not Stated']
        self.order_vars = []
        self.age_toggle_top_row = 2
        self.toggle_column = 0
        self.age_plot_row = self.toggle_column + 1
        self.age_plot_column = self.age_toggle_top_row
        self.plot_span = 10
            

        # Creating the checkbuttons
        for i in range(len(self.orders)):
            self.order_vars.append(IntVar())
            temp_button = ttk.Checkbutton(self, text=self.orders[i], command = self.update_plot, variable = self.order_vars[i])
            self.age_plot_toggles.append(temp_button)


    def update_plot(self):
        # This function will update the chart to include the active plots
        print("updating plot")
        
        # Clear the figure
        self.figure.clf()

        # Update the figure canvas
        self.chart = FigureCanvasTkAgg(self.figure,self)
        self.chart.get_tk_widget().grid(column=self.age_plot_column, row=self.age_plot_row, columnspan=self.plot_span, rowspan=self.plot_span)
        
        # Update the axis with a subplot
        self.ax1 = self.figure.add_subplot(111)
        
        # Create the ax properties
        self.legend_list = []

        # Plot data if the checkbox is selected
        for i in range(len(self.age_plot_toggles)):
            
            if 'selected' in self.age_plot_toggles[i].state():
                self.all_data[i].plot('Year', 'Births', kind='line', legend=True, ax=self.ax1) 
                self.legend_list.append(self.orders[i])
                self.ax1.legend(self.legend_list)
                


    def make_window(self):
        # Create the structure of widgets inside the main window
        print("running make_window")
        
        # Placing the plot toggle radio buttons in the window
        i = self.age_toggle_top_row
        for radiobutton in self.age_plot_toggles:
            radiobutton.grid(column=0, row=i)
            i+=1

        # Create the space for the plots
        self.figure = plt.Figure(figsize=(6,5), dpi=100)
        self.ax1 = self.figure.add_subplot(111)
        self.ax1.set_title('Births per Year')
        self.chart = FigureCanvasTkAgg(self.figure,self)
        self.chart.get_tk_widget().grid(column=self.age_plot_column, row=self.age_plot_row, columnspan=self.plot_span, rowspan=self.plot_span)


        # Create a button to insert plot (temporary)
        # self.test_button = Button(self, text="Test", command = self.insert_plot)
        # print("Button is created")
        # test_colomn = self.age_plot_column + self.plot_span + 1
        # test_row = self.age_plot_row + self.plot_span + 1
        # self.test_button.grid(column = test_colomn, row = test_row)

    def make_plot_data(self, birth_df):

        self.all_data = []

        for i in range(len(self.orders)):
            self.all_data.append(birth_df[(birth_df['Birth Order'] == self.orders[i]) & (birth_df['Age Group'] == 'All ages')])


        # Create sub-dataframes for separate age plots
        # First = Births[(Births['Birth Order'] == '1st Born') & (Births['Age Group'] == ages[age])]
        # Second = Births[(Births['Birth Order'] == '2nd Born') & (Births['Age Group'] == ages[age])]
        # Third = Births[(Births['Birth Order'] == '3rd Born') & (Births['Age Group'] == ages[age])]
        # Fourth = Births[(Births['Birth Order'] == '4th Born') & (Births['Age Group'] == ages[age])]
        # Fifth = Births[(Births['Birth Order'] == '5th Born') & (Births['Age Group'] == ages[age])]
        # Sixth = Births[(Births['Birth Order'] == '6th Born') & (Births['Age Group'] == ages[age])]

        if False:
            # Ask user for desired birth order
            order = int(input("What birth order would you like to plot?\n 0 = Total\n 1 = 1st Born\n 2 = 2nd Born\n 3 = 3rd Born\n 4 = 4th Born\n 5 = 5th Born\n 6 = 6th Born\n 7 = 7th Born\n 8 = 8th child and over\n 9 = Not Stated\n Enter the cooresponding number (0-9)\n "))

            # Create sub-dataframes for separate birth order plots

            Under_fifteen = Births[(Births['Birth Order'] == orders[order]) & (Births['Age Group'] == 'Under 15')]
            Late_teens = Births[(Births['Birth Order'] == orders[order]) & (Births['Age Group'] == '15-19')]
            Early_twenties = Births[(Births['Birth Order'] == orders[order]) & (Births['Age Group'] == '20-24')]
            Late_twenties = Births[(Births['Birth Order'] == orders[order]) & (Births['Age Group'] == '25-29')]
            Early_thirties = Births[(Births['Birth Order'] == orders[order]) & (Births['Age Group'] == '30-34')]
            Late_thirties = Births[(Births['Birth Order'] == orders[order]) & (Births['Age Group'] == '35-39')]

            # Plot separate birth orders dataframes
            plt.figure(figsize=(15,8))
            plt.plot(Under_fifteen.Year, Under_fifteen.Births, '.:r')
            plt.plot(Late_teens.Year, Late_teens.Births, '.:b')
            plt.plot(Early_twenties.Year, Early_twenties.Births, '.:g')
            plt.plot(Late_twenties.Year, Late_twenties.Births, '.:y')
            plt.plot(Early_thirties.Year, Early_thirties.Births, '.:')
            plt.plot(Late_thirties.Year, Late_thirties.Births, '.:')
            plt.title("Births per Year by Age Group")
            plt.xlabel("Year")
            plt.ylabel("Births")
            plt.grid()
            plt.show()

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

    # def insert_plot(self):
    #     print("inserting plot")
    #     # for now, insert a random plot on the frame
    #     data1 = {'country': ['A', 'B', 'C', 'D', 'E'],
    #      'gdp_per_capita': [45000, 42000, 52000, 49000, 47000]
    #      }
    #     df1 = pd.DataFrame(data1)
    #     chart = FigureCanvasTkAgg(self.figure,self)
    #     chart.get_tk_widget().grid(column=self.age_plot_column, row=self.age_plot_row, columnspan=self.plot_span, rowspan=self.plot_span)
    #     df1 = df1[['country', 'gdp_per_capita']].groupby('country').sum()
    #     df1.plot(kind='bar', legend=True, ax=self.ax1)


if __name__ == "__main__":

    print("runing main")

    window = InteractivePlotter()
    print("main after make_window")
    window.make_window()
    window.make_plot_data(window.create_dataframe())


    window.mainloop()