import pandas as pd

data = {
    "amount": [110, 121, -102, 211],
    "month": [9, 9, 9, 10],
}

data = pd.DataFrame(data)

column_selection = data[["amount", "month"]]
uniq_months = list(column_selection["month"].unique())
# Values we will select for the graph
bar_graph_values = []

for month in uniq_months:
    # Select values in the data frame where the month is equal to the unique months
    values_in_certain_months = column_selection[column_selection["month"] == month]
    # Select the rows in the dataframe
    # Add certain values to the chart
    expensePerMonth = [0]
    revenuePerMonth = [0]
    for index, row in values_in_certain_months.iterrows():
        value = row["amount"]
        month_value = row["month"]

        if value >= 0:
            revenuePerMonth.append(value)
        else:
            value = abs(value)
            expensePerMonth.append(value)

    # Add up the sums
    sum_of_expenses = sum(expensePerMonth)
    sum_of_revenues = sum(revenuePerMonth)

    # Add to the bar graph values
    # First index equals the month, second one is income/revenue, third is expenses
    month_to_add = [month, sum_of_revenues, sum_of_expenses]
    bar_graph_values.append(month_to_add)

# Select Month values
x_months = []
y_income = []
y_expense = []

for item in bar_graph_values:
    x_months.append(item[0])
    y_income.append(item[1])
    y_expense.append(item[2])
