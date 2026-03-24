# User Inputs
num = float(input('Enter a real value: '))
runningTotal = 0

# Logic
while num >= 0:
    runningTotal += num
    num = float(input('Enter a real value: '))

print(runningTotal)