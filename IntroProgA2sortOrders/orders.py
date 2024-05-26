"""
A program which reads in burger orders from a file, and determines how often each order was made.

The program asks the user how many of the top orders they would like to view,
and prints that number to the console along with the order's frequency and 
price. 
Each order must be on a new line in the file, and contain 7 elements. An example of a single line in
the correct format is:
milk,tomato,2,1,yes,no,no

Author: Tanya
Trimester 1, 2024
"""

from operator import itemgetter

ORDERS_FILENAME = "orders.txt"

AVAILABLE_BUNS = ["milk", "gluten free"]
AVAILABLE_SAUCES = ["tomato", "barbecue", "none"]

PRICES = {
    "base" : 5,  # Includes milk bun, sauce, up to 1 patty, 1 cheese slice, and 1 salad item.
    "gluten_free" : 1,  # Additional cost.
    "patty" : 3,  # 1 included. Price per additional patty.
    "cheese" : 1,  # 1 included, Price per additional cheese slice.
    "salad" : 1  # tomato, lettuce or onion included in base price. Price per additional salad item. 
}

# Initialise an empty dictionary for storing frequency of each order.
order_frequency = {}

def check_valid_choice(choice, available_choices, choice_type):
    """Checks if the choice is in the list of availahle choices.

    Checks against the available_buns or available_sauces lists. 
    Called by the convert_to_tuple() function.
    
    Arguments:
    choice -- String to check against the list
    available_choices -- The list to check against
    choice_type -- String for use in print statement

    Returns:
    String -- if valid choice, returns choice
    None -- if choice is not in list, returns None
    """
    if choice in available_choices:
        return choice
    else:
        print(f"The {choice_type} choice isn't an available option")
        return None
    
def convert_to_int(choice, choice_type):
    """Convert choice to int and check it's in range.

    Called by the convert_to_tuple() function.

    Arguments:
    choice -- String to convert to int
    choice_type -- String for use in print statement

    Returns:
    int -- If choice can be converted and is between 0 and 3
    None -- If choice can't be converted or not in range
    """
    try:
        choice = int(choice)
        if choice >= 0 and choice <= 3:
            return choice
        else:
            print(f"Given Amount for {choice_type} not in range")
            return None
    except ValueError:
        print(f"Can't convert given value for {choice_type} to int")
        return None

def convert_to_bool(choice, choice_type):
    """Converts a String to boolean if the String is "yes" or "no".
    
    Only converts "yes" or "no" to boolean. All other values are
    invalid. Called by the convert_to_tuple() function.
    
    Arguments:
    choice -- String to convert to boolean
    choice_type -- String for use in print statement

    Returns:
    bool -- If choice is "yes" or "no"
    None -- If choice is invalid
    """
    if choice == "yes":
        return True
    elif choice == "no":
        return False
    else:
        print(f"This {choice_type} choice not valid. Must be 'yes' or 'no'.")
        return None

def convert_to_tuple(order):
    """Takes order String and converts to a tuple containing the correct types.

    First converts to a list and checks if the list is the correct length. Calls 
    check_valid_choice(), convert_to_int() and convert_to_bool() functions 
    to process the list elements, before converting the final list to 
    a tuple.
    
    Arguments:
    order -- String representing a single burger order

    Returns:
    tuple -- The current order converted to a tuple
    None -- If list length is incorrect, or any converted items returned None
    """
    order = order.strip().split(",")
    if len(order) != 7:
        print("Order must include bun choice, sauce choice, 2 numbers, and 3 instances of \"yes\" or \"no\"")
        return None 
        # The tuple is not the correct length. Exit the function early.
    
    order[0] = check_valid_choice(order[0], AVAILABLE_BUNS, "bun")
    order[1] = check_valid_choice(order[1], AVAILABLE_SAUCES, "sauce")
    order[2] = convert_to_int(order[2], "patties")
    order[3] = convert_to_int(order[3], "cheese slices")
    order[4] = convert_to_bool(order[4], "tomato")
    order[5] = convert_to_bool(order[5], "lettuce")
    order[6] = convert_to_bool(order[6], "onion")

    for i in range(len(order)):
        if order[i] == None:
            return None
         
    return(tuple(order))

def read_file_and_process(filename):
    """Reads each line of file and adds converted tuple to order_frequency dictionary.

    Adds the orders if not already present or increments the value for 
    that order.
    If convert_to_tuple() returns None for any lines, or the file can't
    be read, prints an error message and exits the program.

    Arguments:
    filename -- The file to read orders from
    """
    line_number = 0

    try:
        with open(filename) as file:
            for order in file:
                line_number += 1
                order = convert_to_tuple(order)

                if order == None:
                    print(f"The error occurred in line {line_number} of the text file")
                    exit()

                else: # Add order to dictionary, or increment by one if already present
                    order_frequency[order] = order_frequency.get(order, 0) + 1

    except PermissionError:
        print("You don't have permission to open this text file")
        exit()
    except FileNotFoundError:
        print("Text file can't be found")
        exit()

def process_user_input():
    """Asks users how many top orders to display.

    Checks that the user input can be converted to an integer. If the 
    user requests more orders than are available, prints a message informing
    them, and returns the maximum number of burgers instead. Called by 
    display_top_burgers().

    Returns:
    int -- Either the requested number, or the maximum number
    """
    requested_number = 0

    try:
        requested_number = int(input("How many of the top burger orders would you like to see?: "))
        if requested_number <= 0:
            print("That number is too low. Please enter a positive number: ")
            process_user_input()
    except ValueError:
        print("Input not valid. Please enter a positive number: ")
        process_user_input()
    
    max = len(order_frequency)
    if requested_number > max:
        print(f"There are only {max} different burgers recorded.")
        return max
    else:
        return requested_number
    
def get_cost(burger_order):
    """Calculate the cost of individual burgers.

    Called by the display_top_burgers() function to calculate the
    cost of the requested number of top orders only.
    
    Arguments:
    burger_order -- tuple containing details of the current burger

    Returns:
    int -- The price of the burger as an integer 
    """
    burger_price = PRICES["base"]
    
    if burger_order[0] == "gluten free":
        burger_price += PRICES["gluten_free"]
    if burger_order[2] > 1:
        burger_price += PRICES["patty"] * (burger_order[2] - 1)
    if burger_order[3] > 1:
        burger_price += PRICES["cheese"] * (burger_order[3] - 1)

    salad_number = 0

    for salad_type in burger_order[4], burger_order[5], burger_order[6]:
        if salad_type:
            salad_number += 1

    if salad_number > 1:
        burger_price += PRICES["salad"] * (salad_number - 1)

    return burger_price

def display_top_burgers():
    """Print fillings, order frequency and price for requested top orders.

    Sorts the order_frequency dictionary by its values, and reverses the 
    order to find those ordered most often. Calls process_user_input() to
    determine how many to display, and get_cost() to calculate the prices
    of those burgers.
    """
    sorted_orders = sorted(order_frequency.items(), key=itemgetter(1,0))
    sorted_orders.reverse()

    requested_number = process_user_input()

    top_number = {}
    for i in range(requested_number):
        burger = sorted_orders[i]
        top_number[burger[0]] = burger[1]

    if requested_number == 1:
        print("The top burger was:\n")
    else:
        print(f"The top {requested_number} burgers were:\n")

    for key, value in top_number.items():
        price = get_cost(key)
        print(f"{key}\t{value}\t${price}\n")


if __name__ == "__main__":
    # First create the order_frequency dictionary by reading in
    #  all orders from the file.
    read_file_and_process(ORDERS_FILENAME)

    # Next sort the orders, ask for user input, and display the 
    #  requested number.
    display_top_burgers()
