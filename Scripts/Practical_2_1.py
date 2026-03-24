# Name: Dirk Willemse Student Number: 56441045

# heading for concatenated values
print("Concatenated values")

# user input propts for age, output will be strings
myAge = input("What is your age?: ")
friendAge = input("What age is your friend?: ")

# adds the 2 numbers as strings
cValues = myAge + friendAge

# prints the combined string
print(f"Result: {cValues}")

# prints the sum values
print("Sum values")

myAge = int(input("What is your age?: "))
friendAge = int(input("What age is your friend?: "))

# converts the input strings to ints
num1 = myAge
num2 = friendAge

# gets the sum between to values
sum = num1 + num2

print(type(sum))
# prints the sum
print(f"Result: {sum}")

# gets the num avg
avg = (num1 + num2) / 2

# prints the avg
print(f"Average age: {avg}")
