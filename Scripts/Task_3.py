# Main menu
# Display options

print("=========================================")
print("\t CMPG 111 PRACTICE MENU \t")
print("=========================================")
print("1. FINANCIAL DECISIONS")
print("2. GENERAL CONDITION CHECKING")
print("3. TEXT / COMPARISON TASKS")
print("4. ACADEMIC TASKS")
print("=========================================")

# User Input
nav = input('Enter your choice (1-4): ')

# Nav logic 1
if nav == '1':
    print('a. Determining Sales Bonuses')
    print('b. Checking Payment Status')
    print('c. Salary Comparison')
    print('d. Loan Qualification Assessment')
    print('e. Special Offer Eligibility')

    # Sub Navi (a-e)
    choice = input('Enter your choice (a-e): ')

    # a logic and for bonus calc
    if choice == 'a':
        sales = float(input('Please enter your sales: '))
        if sales >= 5000:
            bonus = 500.0
            print('Your bonus: ', bonus)
            print('Your sales:', sales)

        else:
            print('Your sales:', sales)

    # b logic and calcs for sufficient payments
    elif choice == 'b':
        bal = float(input('Please enter your balance: '))
        payment = float(input('Please enter the payment amount: '))

        if bal == 0:
            print('Insufficient Funds')
            print('You did not pay enough')

        elif bal >= payment:
            print("You have paid enough")

        else:
            print('You did not pay enough')

    # c logic for determining if you have big or small salary
    elif choice == 'c':
        salary = float(input('Please enter your salary: '))

        if salary <= 20000:
            print('Small Salary')
        else:
            print('Big Salary')

    # d logic for loan qualification
    elif choice == 'd':
        salary2 = float(input('Please enter your Salary: '))
        timeE = float(input('Please enter your years on job: '))

        if salary2 >= 30000 and timeE >= 2:
            print('You qualify for a loan')
        
        elif salary2 < 30000 and timeE < 2:
            print('You must earn at least 30k to qualify')
            print('You must have been on your current job for 2 years')

        elif salary2 < 30000:
            print('You must earn at least 30k to qualify')
        
        elif timeE < 2:
            print('You must have been on your current job for 2 years')

    # e logic for determining if you qualify for a discount
    elif choice == 'e':
        age = int(input('Enter your age: '))
        student = input('Are you a student? (yes/no): ')

        if age >= 60 or student == 'yes':
            print('You get the special')
        
        else:
            print('You do not get the special')

    else:
        print('Invalid sub-menu choice.')

# Nav logic 2
elif nav == '2':
    print('a. Weather Temperature Evaluation')
    print('b. Lego Age Restriction')
    print('c. Even Number Checker')
    choice2 = input('Enter your choice (a-c): ')

    # a logic for weather report
    if choice2 == 'a':
        temp = float(input('Please enter the temperature: '))

        if temp < 40:
            print("A little cold, isn't it?")
        
        else:
            print("Nice weather we're having.")

    # b logic to see if you can play with lego
    elif choice2 == 'b':
        age = int(input('Please enter your age: '))

        if age >= 4 and age <= 94:
            print('You can play Lego')
        
        else:
            print('You cannot play Lego')

    # c logic to determine if a number is odd or even
    elif choice2 == 'c':
        num1 = int(input('Please enter a number: '))

        if num1 % 2 == 0:
            print('Even Number!')

        else:
            print('Uneven Number!')
    else:
        print('Invalid sub-menu choice.')

# Nav logic 3
elif nav == '3':
    print('a. Comparing Usernames')
    choice3 = input('Enter your choice (a): ')

    # a logic to compare to users by ASCII values
    if choice3 == 'a':
        user1 = input('Enter the first User 1: ')
        user2 = input('Enter the second User 2: ')

        # Compares left-to-right using character codes (ASCII for normal letters/spaces)
        if user1 > user2:
            print(user1,">", user2 )
        elif user1 < user2:
            print(user1, '<', user2)
        else:
            print(user1, '=', user2)

    else:
        print('Invalid sub-menu choice.')

# Nav logic 4
elif nav == "4":
    print('a. Academic Grading')
    choice3 = input('Enter your choice (a): ')

    # a logic to determine your grade symbol
    if choice3 == 'a':
        grade = float(input('Enter your score: '))

        if grade >= 90:
            print('Your grade is A')

        elif grade >= 80:
            print('Your grade is B')

        elif grade >= 70:
            print('Your grade is C')
        
        elif grade >= 60:
            print('Your grade is D')

        else:
            print('Your grade is F')

    else:
        print('Invalid sub-menu choice.')
        
else:
    print('Invalid main menu choice.')

