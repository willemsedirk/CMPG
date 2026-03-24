# ---------- DECIMAL TO BINARY ----------
decimal_number = int(input("Enter a decimal number: "))

b1 = decimal_number // 512
r1 = decimal_number % 512

b2 = r1 // 256
r2 = r1 % 256

b3 = r2 // 128
r3 = r2 % 128

b4 = r3 // 64
r4 = r3 % 64

b5 = r4 // 32
r5 = r4 % 32

b6 = r5 // 16
r6 = r5 % 16

b7 = r6 // 8
r7 = r6 % 8

b8 = r7 // 4
r8 = r7 % 4

b9 = r8 // 2
b10 = r8 % 2

binary_number = (
    b1 * 1000000000 +
    b2 * 100000000 +
    b3 * 10000000 +
    b4 * 1000000 +
    b5 * 100000 +
    b6 * 10000 +
    b7 * 1000 +
    b8 * 100 +
    b9 * 10 +
    b10
)

print(f"Decimal {decimal_number} in binary is: {binary_number}")


# ---------- BINARY TO DECIMAL ----------
binary_input = int(input("Enter a binary number (up to 10 digits): "))

d1 = binary_input // 1000000000
r1 = binary_input % 1000000000

d2 = r1 // 100000000
r2 = r1 % 100000000

d3 = r2 // 10000000
r3 = r2 % 10000000

d4 = r3 // 1000000
r4 = r3 % 1000000

d5 = r4 // 100000
r5 = r4 % 100000

d6 = r5 // 10000
r6 = r5 % 10000

d7 = r6 // 1000
r7 = r6 % 1000

d8 = r7 // 100
r8 = r7 % 100

d9 = r8 // 10
d10 = r8 % 10

decimal_result = (
    d1 * 512 +
    d2 * 256 +
    d3 * 128 +
    d4 * 64 +
    d5 * 32 +
    d6 * 16 +
    d7 * 8 +
    d8 * 4 +
    d9 * 2 +
    d10
)

print(f"Binary {binary_input} in decimal is: {decimal_result}")