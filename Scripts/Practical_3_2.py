# User Input

temp = float(input("Enter the temperature in Celsius: "))

if temp <= 0:
    print("the tempertature is freezing cold")

elif temp > 0 and temp <= 10:
    print("the tempertature is cold")

elif temp >= 11 and temp <= 20:
    print("the tempertature is cool")

elif temp >= 21 and temp <= 30:
    print("the tempertature is warm")

else:
    print("the tempertature is scorching hot")

# sal nie onder die boundry gaan van die boonste grens nie =
# sal nie onder die vorige range gaan nie