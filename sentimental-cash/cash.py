import cs50

def get_positive_float(prompt):
    while True:
        change_owed = cs50.get_float(prompt)
        if change_owed >= 0:
            return change_owed
        print("Change owed must be non-negative.")

def calculate_coins(change_owed):
    num_coins = 0
    coin_values = [25, 10, 5, 1]

    for coin_value in coin_values:
        while change_owed >= coin_value:
            change_owed -= coin_value
            num_coins += 1

    return num_coins

change_owed_cents = int(get_positive_float("Change owed: ") * 100)
num_coins = calculate_coins(change_owed_cents)
print(num_coins)

