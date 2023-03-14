# This script will process data from a birth stats .csv and produce graphics
# By Casey Betts March 2023

import pandas as pd
import matplotlib.pyplot as plt

### Global Variables ###

# .csv file location
file_location = "Pop Stats - Numeric Data.csv"

# Create list for ages and birth orders
ages = ['Under 15', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54']
orders = ['Total', '1st Born', '2nd Born', '3rd Born', '4th Born', '5th Born', '6th Born', '7th Born', '8th child and over', 'Not Stated']
birth_plots = ['age', 'order']

### Functions ### 

def load_data(file_loc):
    # Read in the .csv data
    return pd.read_csv(file_loc)

def creat_dataframe():
    # Melt the age columns into rows
    Births = pd.melt(load_data(file_location), 
                            id_vars=['Year', 'Birth Order'],
                            value_vars=['All ages','Under 15', '15-19', '15-17', '18-19', '15', '16', '17', '18', '19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54'],
                            var_name='Age Group',
                            value_name='str_Births')

    # Change Births data type to int
    Births['Births'] = pd.to_numeric(Births.str_Births, downcast="integer")

    # Remove the str_Births column
    Births.drop(labels=['str_Births'], axis=1, inplace=True)

    return Births

def make_plot(Births):
    # Ask user for desired plot type
    plot_type = input("Enter plot type (age/order): ")

    if plot_type == 'age':
        # Ask user for desired age group
        age = int(input("For what age group would you like to see birth order statistics?\n 0 = All Ages\n 1 = Under 15\n 2 = 15-19\n 3 = 20-24\n 4 = 25-29\n 5 = 30-34\n 6 = 34-39\n 7 = 40-44\n 8 = 45-49\n 9 = 50-54\n "))

        print(ages[age])
        # Create sub-dataframes for separate age plots
        First = Births[(Births['Birth Order'] == '1st Born') & (Births['Age Group'] == ages[age])]
        Second = Births[(Births['Birth Order'] == '2nd Born') & (Births['Age Group'] == ages[age])]
        Third = Births[(Births['Birth Order'] == '3rd Born') & (Births['Age Group'] == ages[age])]
        Fourth = Births[(Births['Birth Order'] == '4th Born') & (Births['Age Group'] == ages[age])]
        Fifth = Births[(Births['Birth Order'] == '5th Born') & (Births['Age Group'] == ages[age])]
        Sixth = Births[(Births['Birth Order'] == '6th Born') & (Births['Age Group'] == ages[age])]

        # Plot separate age dataframes
        plt.figure(figsize=(15,8))
        plt.plot(First.Year, First.Births, '.:r')
        plt.plot(Second.Year, Second.Births, '.:b')
        plt.plot(Third.Year, Third.Births, '.:g')
        plt.plot(Fourth.Year, Fourth.Births, '.:y')
        plt.plot(Fifth.Year, Fifth.Births, '.:')
        plt.plot(Sixth.Year, Sixth.Births, '.:')
        plt.title("Births per Year by Birth Order")
        plt.xlabel("Year")
        plt.ylabel("Births")
        plt.grid()
        plt.show()

    elif plot_type == 'order':
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
    else:
        print("Please ensure 'birth_plot' is from 0 to 1")


if __name__ == "__main__":

    df = creat_dataframe()
    make_plot(df)