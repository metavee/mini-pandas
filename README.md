# mini-pandas

I like the syntax of [Pandas](https://pandas.pydata.org/) for many numerical tasks.
It's fun to imagine: if I were trapped on a desert island (with a Python 3.9 interpreter), could I re-implement some of its core functionality in pure Python?

This project explores that idea.

Toy project.

## Project objectives

- implement a DataFrame that can be indexed and sliced by row, column, or bitmask
- try to add a handful of Pandas functions that I commonly use
- avoid dependencies
- don't worry about efficiency
- don't aim for ultimate feature parity

## Demo

```python
from mini_pandas.df import DF

# create a dataframe based on our grocery list
groceries = DF({"Item": ["Red onion", "Carrots", "Paprika", "Cheese", "Potatoes", "Milk"], "Category": ["Vegetables", "Vegetables", "Spices", "Dairy", "Vegetables", "Dairy"], "Price": [1.08, 2.32, 1.55, 4.89, 3.40, 2.99]})
print(groceries)
# | Item      | Category   | Price |
# | --------- | ---------- | ----- |
# | Red onion | Vegetables | 1.08  |
# | Carrots   | Vegetables | 2.32  |
# | Paprika   | Spices     | 1.55  |
# | Cheese    | Dairy      | 4.89  |
# | Potatoes  | Vegetables | 3.4   |
# | Milk      | Dairy      | 2.99  |

# slice a column using its name
print(groceries["Price"])
# Vec([1.08, 2.32, 1.55, 4.89, 3.4, 2.99])

# slice a row using its number
print(groceries[1])
# Vec(['Carrots', 'Vegetables', 2.32])

# slice a set of rows that match a certain criteria
print(groceries[groceries["Category"] == "Vegetables"])
# | Item      | Category   | Price |
# | --------- | ---------- | ----- |
# | Red onion | Vegetables | 1.08  |
# | Carrots   | Vegetables | 2.32  |
# | Potatoes  | Vegetables | 3.4   |

# analyze the number of items in each category, and the price subtotal for each category
print(groceries.groupby("Category").count().sum("Price").agg())
# | Category   | count(*) | sum(Price) |
# | ---------- | -------- | ---------- |
# | Dairy      | 2        | 7.88       |
# | Spices     | 1        | 1.55       |
# | Vegetables | 3        | 6.8        |
```