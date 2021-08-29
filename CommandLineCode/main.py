balance = "21"

try:
    if balance != ".":
        balance += ".00"
        balance = float(balance)

        print(f"{balance}")
    else:
        balance1 = float(balance)
        balance = round(balance1, 2)
except ValueError:
    print("Error")
