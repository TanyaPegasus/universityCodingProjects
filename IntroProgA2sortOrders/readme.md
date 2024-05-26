# Orders

A program to read in burger orders from a file and determine
how often each order was made. 

Users request a number of top orders to display and it prints those orders to the console, along with each order's frequency and price.

Developed to fulfill the requirements of Programming Task 2 for COSC110, T1 2024.

## Usage

Ensure that the "orders.txt" file is located within the same directory as "orders.py".

For files in alternate locations, or with alternate names, ORDERS_FILENAME in "orders.py" will need to be updated with the correct name and path.

```bash
python3 burger.py
```

## Example file contents and interactions

```
milk,tomato,2,1,yes,no,no
milk,barbecue,3,3,yes,yes,yes
gluten free,barbecue,1,0,no,yes,no
milk,barbecue,3,3,yes,yes,yes
gluten free,barbecue,1,0,no,yes,no
milk,barbecue,3,3,yes,yes,yes
milk,barbecue,3,3,yes,yes,yes
milk,tomato,2,1,yes,no,no
----

How many of the top burger orders would you like to see?: 5
There are only 3 different burgers recorded.
The top 3 burgers were:

('milk', 'barbecue', 3, 3, True, True, True)    7       $15

('milk', 'barbecue', 2, 3, True, True, True)    7       $12

('gluten free', 'barbecue', 1, 0, False, True, False)   6       $6

```

```
milk,tomato,2,1,yes,no,no
milk,bbq,3,3,yes,yes,yes
----

The sauce choice isn't an available option
The error occurred in line 2 of the text file
```

## Author

TanyaPegasus