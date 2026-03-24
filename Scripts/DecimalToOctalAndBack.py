# DECIMAL TO OCTAL
decimal_number = int(input("Enter a decimal number: "))

# Break decimal into octal digits manually
octal_digit1 = decimal_number // 64
remainder1 = decimal_number % 64

print(octal_digit1)
print(remainder1)

octal_digit2 = remainder1 // 8
octal_digit3 = remainder1 % 8

octal_number = octal_digit1 * 100 + octal_digit2 * 10 + octal_digit3

print(f"Decimal {decimal_number} in octal is: {octal_number}")

# OCTAL TO DECIMAL
octal_input = int(input("Enter a octal number: "))

# Extract each octal digit manually
digit1 = octal_input // 100
remainder2 = octal_input % 100

digit2 = remainder2 // 10
digit3 = remainder2 % 10

decimal_result = digit1 * 64 + digit2 * 8 + digit3

print(f"Octal {octal_input} in decimal is: {decimal_result}")