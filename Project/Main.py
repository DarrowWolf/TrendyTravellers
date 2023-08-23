import pandas as pd

# cars = pd.reaad_csv(mtcars.csv)
intMonthlyVisitor = pd.read_csv('c:/Users/cynth/Downloads/Int_Monthly_Visitor.csv')


yearPeriod = input("Enter year period (1: 1978-1987, 2: 1988-1997, 3: 1998-2007, 4: 2008-2017): ")

if yearPeriod.lower() == '1' or yearPeriod.lower() == '2' or yearPeriod.lower() == '3' or yearPeriod.lower() == '4':
        region = input("Enter region (1: Asia, 2: Europe, 3: Others): ")
    
else:
    print("Invalid Input")

if region.lower() == '1' or region.lower() == '2' or region.lower() == '3':
      print("Yay")

else:
      print("Invalid Input")