"""Contains all the extra functions and etc that'll be used in our main application"""

information = {
    "titleText": "#355040",
    "thirdOfFrame": 0.3 * 500,
}

FONTTEXTCOLOR = "#355040"

random_money_quotes = [
    "“The bitterness of poor quality remains long after the sweetness of low price is forgotten.” – Benjamin Frankin",
    "“Empty pockets never held anyone back. Only empty heads and empty hearts can do that.” – Norman Vincent Peale ",
    "“Saving must become a priority, not just a thought. Pay yourself first.” – Dave Ramsey",
    "“Money is only a tool. It will take you wherever you wish, but it will not replace you as the driver.” – Ayn Rand",
    "“There is a gigantic difference between earning a great deal of money and being rich.” – Marlene Dietrich",
    "“Enough is better than too much.” Dutch Proverb ",
    "“Never spend your money before you have it.” – Thomas Jefferson",
    "“Saving is the gap between your ego and your income. ― Morgan Housel, The Psychology of Money",
    "The price of anything is the amount of life you exchange for it. – Henry David Thoreau",
    "Always the first step to save money is to always record your expenses.",
    "Set savings goals.",
]

exp_income = ("Income", "Expense")
type_of_trans = (
    "Retail",
    "Food",
    "Transport",
    "Gift",
    "Medical",
    "School",
    "Work",
    "Other",
)


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"
