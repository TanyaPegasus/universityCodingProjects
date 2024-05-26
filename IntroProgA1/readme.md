# Codetown Burger Co

A Python program for taking customer orders at Codetown Burger Co.

Implemented for COSC110 Assignment 1 for Trimester 1, 2024.


## Usage
Run the following command in the terminal from within the directory containing the burger.py file:

```
python3 burger.py
```

## Example Interaction

```
Welcome to Codetown Burger Co!

How many burgers would you like to order?
               Please enter a number between 1 and 10: 2

     Details for burger 1:
          What bun type should be included for burger 1?
               Please type 'milk' or 'gluten free': milk
          What sauce should be included on Burger 1?
               Please type 'tomato', 'barbecue' or 'none': tomato
          How many patties should be included on burger number 1:
               Please enter a number between 0 and 3: 2
          How many cheese slices should be included on burger number 1:
               Please enter a number between 0 and 3: 3
          Would you like tomato on burger number 1?
               Please type 'yes' or 'no': yes
          Would you like lettuce on burger number 1?
               Please type 'yes' or 'no': yes
          Would you like onion on burger number 1?
               Please type 'yes' or 'no': no

     Details for burger 2:
          What bun type should be included for burger 2?
               Please type 'milk' or 'gluten free': gf
               Please enter a valid choice
               Please type 'milk' or 'gluten free': gluten free
          What sauce should be included on Burger 2?
               Please type 'tomato', 'barbecue' or 'none': none
          How many patties should be included on burger number 2:
               Please enter a number between 0 and 3: 5
               Number must be between 0 and 3:
               Please enter a number between 0 and 3: hello
               That was not a number
               Please enter a number between 0 and 3: 2
          How many cheese slices should be included on burger number 2:
               Please enter a number between 0 and 3: 2
          Would you like tomato on burger number 2?
               Please type 'yes' or 'no': y
               Please enter a valid choice
               Please type 'yes' or 'no': yes
          Would you like lettuce on burger number 2?
               Please type 'yes' or 'no': yes
          Would you like onion on burger number 2?
               Please type 'yes' or 'no': no


The total cost for all burgers is $22
     Thank you for visiting Codetown Burger Co!
```