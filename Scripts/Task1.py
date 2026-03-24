decimal_number_input = input("Enter a decimal number: ")
decimal_number = int(decimal_number_input)

# Each digit: shift right to target position, isolate with % 8
d1  = decimal_number // 8**9  % 8
d2  = decimal_number // 8**8  % 8
d3  = decimal_number // 8**7  % 8
d4  = decimal_number // 8**6  % 8
d5  = decimal_number // 8**5  % 8
d6  = decimal_number // 8**4  % 8
d7  = decimal_number // 8**3  % 8
d8  = decimal_number // 8**2  % 8
d9  = decimal_number // 8**1  % 8
d10 = decimal_number // 8**0  % 8

octal_number = f"{d1}{d2}{d3}{d4}{d5}{d6}{d7}{d8}{d9}{d10}"

print(f"Decimal {decimal_number} in octal is: {octal_number}")