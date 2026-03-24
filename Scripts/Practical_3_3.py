# User Inputs

stick1 = float(input('Enter the length of stick #1: '))
stick2 = float(input('Enter the length of stick #2: '))
stick3 = float(input('Enter the length of stick #3: '))

# triangle inequality theorem
if stick1 + stick2 > stick3 and stick1 + stick3 > stick2 and stick2 + stick3 > stick1:
    print("Triangle possible")
    if stick1 == stick2 == stick3:
        print("Equilateral triangle possible")
    elif stick1 == stick2 or stick1 == stick3 or stick2 == stick3:
        print("Isosceles triangle possible")
    else:
        print("Scalene triangle possible")    
else:
    print("No triangle possible")