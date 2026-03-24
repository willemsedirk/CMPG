# User Inputs
age = int(input("Enter your age: "))

# logic

if age == 0:
    exit()

else:
    while 0 < age < 18:
        print("You may NOT vote")
        age = int(input("Enter your age: "))


print("You are eligible to vote")
