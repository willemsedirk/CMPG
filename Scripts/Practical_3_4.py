# User inputs
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

div_remainder = num1 % num2

# Division check
if div_remainder != 0:
    print(num1, "is not divisible by", num2)
else:
    print(num1, "is divisible by", num2)
