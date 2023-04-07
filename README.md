# Statistical-Plotting-App

## Purpose
This script will read in a .csv data table with specific column names and open a gui to toggle plots using the data. The target data for this app is US birth data where the mother's age and the birth order are primary data within the table. 

## CSV Specifics
The .csv file should be formatted as the one contained in this reposetory. The field names are hard coded within the scrip so any deviation of field names will need to be changed in the code. These are the required fields:

- Year - The year the birth data is from
- Birth Order - Order the child was born in (ie. first born child, second born child, etc.)
- All ages - Number of births regardless of the age of the mother

And these age range fields which break down the total (All ages) number of births by age of the mother in five year increments:

- Under 15
- 15-19
- 20-24
- 25-29
- 30-34
- 35-39
- 40-44
- 45-49
- 50-54


The given .csv file also contains the following fields, however, these are optional and are not used in this tool: 15-17, 18-19, 15, 16, 17, 18, 19

## App Interface
![Screenshot]()
