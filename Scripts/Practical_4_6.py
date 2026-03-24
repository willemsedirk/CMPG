# User inputs
width = int(input('Enter rectangle width: '))
while width <= 0:
    width = int(input('Enter rectangle width: '))

length = int(input('Enter rectangle length: '))
while length <= 0:
    length = int(input('Enter rectangle length: '))

if width > 0 and length > 0:
    print('Here is your rectangle: ')
    for i in range(length):
        print('*' * width)
