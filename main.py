import pandas as pd

year_choice = 0
region_choice = 0

class VistorsAnalyticsUtils:
    data = pd.read_csv('Int_Monthly_Visitor.csv') # Made data global variable within the class
    
    def loadDataFile(self):
        data = self.data
        return data
    def parseData(self, year_choice, region_choice):
        # Filter data based on year_choice and region_choice
        filtered_data = self.data[(self.data['Year_Period'] == year_choice) & (self.data['Region'] == region_choice)]
        
        # Parse the data to retain the necessary 10 years period
        if year_choice == 1:
            start_year = 1978
        elif year_choice == 2:
            start_year = 1988
        elif year_choice == 3:
            start_year = 1998
        elif year_choice == 4:
            start_year = 2008
        end_year = start_year + 9  # 10 years period
        
        filtered_data = filtered_data[(filtered_data['Year'] >= start_year) & (filtered_data['Year'] <= end_year)]
        
        # Split the critical information to different columns
        filtered_data['Year_Start'] = start_year
        filtered_data['Year_End'] = end_year
        
        # Retain necessary regions only
        if region_choice == 1:
            filtered_data = filtered_data.iloc[:, 1:19]  # Asia
        elif region_choice == 2:
            filtered_data = filtered_data.iloc[:, 19:30]  # Europe
        elif region_choice == 3:
            filtered_data = filtered_data.iloc[:, 30:]  # Others
        
        return filtered_data

def main():
    while True:
        try:
            year_choice = int(input("Enter year period (1: 1978-1987, 2: 1988-1997, 3: 1998-2007, 4: 2008-2017): "))
            if year_choice not in {1, 2, 3, 4}: # Checks if year_choice input is not 1, 2, 3, 4
                print("Invalid year choice, please choose the number representing the year period!")
                year_choice = 0 # Assign year_choice back to 0 because from the input amove it already assigns a value.
                continue
            elif year_choice in {1, 2, 3, 4}: # Checks if year_choice input is 1, 2, 3, 4
                region_choice = int(input("Enter region (1: Asia, 2: Europe, 3: Others): "))
                if region_choice not in {1, 2, 3}:  # If the year_choice input is 1, 2, 3, 4. It will go to this line to check if the input is not 1, 2, 3
                    print("Invalid region choice, please choose the number representing the region!")
                    region_choice = 0 # Does the same thing as above is it is not the right input
                    continue
                print(year_choice, region_choice) # Debugging to see if what you input in, is correct
                break

        except:
            print("Invalid input")
            continue

    
#Made it easier to read this way
loadDataFile = VistorsAnalyticsUtils().loadDataFile()
parsed_data = VistorsAnalyticsUtils().parseData(year_choice, region_choice)
    
print("Parsed Data:")
print(parsed_data)

if __name__ == '__main__':
    main()
    print(loadDataFile.head())
    ##print(loadDataFile.iloc[:,1:19]) #Asia
    ##print(loadDataFile.iloc[:,19:30]) #Europe
    ##print(loadDataFile.iloc[:, 30:]) #Others
    

