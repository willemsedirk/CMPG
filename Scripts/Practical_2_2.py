# Name: Dirk Willemse Student Number: 56441045

# Gets user input for length and width
length = float(input('Input a length: '))
width = float(input('Input a width: '))

# geometry calcs
area = length * width
perimeter = 2 * (length + width) 
diagonal = (length ** 2 + width ** 2) ** 0.5

# Results, formated
print(f"The area of the rectagle is {area: .2f} square cm")
print(f"The perimeter of the rectagle is {perimeter: .1f} cm")
print(f"The diagonal of the rectangle is {diagonal: .3f} cm")
print('\n')

# prints the dimensions
print("**Rectangle dimensions:**")
print(f'length = {length: .1f} cm \t width = {width: .1f} cm')
