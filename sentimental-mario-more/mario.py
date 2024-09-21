while True:
    try:
        height = int(input("Height: Type a number between 1 and 8: "))
        if 1 <= height <= 8:
            break
    except ValueError:
        print("Please enter a valid number.")

# Print the pyramid shape (height - row)
for row in range(1, height + 1):
si
    print(" " * (height - row), end="")

    print("#" * row, end="")

    print("  ", end="")

    print("#" * row)
