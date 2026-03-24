# Name: Dirk Willemse Student Number: 56441045

weight = int(input('Enter your weight in kilograms (kg): '))
height = int(input('Enter your height in centimeters (cm): '))

# cm => meter
meter = height / 100

# calcs bmi
bmi = weight / (meter ** 2)
print(f'BMI: {bmi: .3f}')
