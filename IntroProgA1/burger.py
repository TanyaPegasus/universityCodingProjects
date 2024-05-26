# Amounts used to calculate burger prices are initialised here.
# This allows them to be accessed from anywhere, and allows them to be changed easily in the futrure
# without need to look at the rest of the code.
prices = {
    "base" : 5,  # Includes milk bun, sauce, up to 1 patty, 1 cheese slice, and 1 salad item.
    "gluten_free" : 1,  # Additional cost
    "patty" : 3,  # 1 included. Price per additional patty
    "cheese" : 1,  # 1 included, Price per additional cheese slice
    "salad" : 1  # tomato, lettuce or onion included in base price. Price per additional salad item. 
}

# Variables used for formatting output seen by customer in the terminal. Adds readability.
indent_one = " " * 5
indent_two = " " * 10
indent_three = " " * 15

def customer_choice(choice_list, message):
    """Handle customer input for fillings with a list of valid choices.

    Arguements:
    choice_list -- list containing valid choices
    message -- String to display when requesting input
    
    Returns a String containing customers's choice
    """

    choice = ""

    while choice not in choice_list:
        try:
            choice = input(message).lower()  # Converting to lowercase ensures input is not case sensitive.
            if choice not in choice_list:
                raise ValueError
        except ValueError:
                print(f"{indent_three}Please enter a valid choice")

    return choice

def type_of_bun(burger_num): 
    """Asks customer to select a bun type.
    Calls the customer_choice function to ensure responses are valid.
    
    Arguements:
    burger_num -- which burger the current choice is for. Type: integer.
    
    Returns a String containing customers's choice
    """

    available_buns = ["milk", "gluten free"]

    print(f"{indent_two}What bun type should be included for burger {burger_num}?")
    
    bun_selection = customer_choice(
        choice_list = available_buns, 
        message = f"{indent_three}Please type 'milk' or 'gluten free': ")
    
    return bun_selection

def type_of_sauce(burger_num):
    """Asks customer to select a type of sauce.
    Calls the customer_choice function to ensure responses are valid.
    
    Arguements:
    burger_num -- which burger the current choice is for. Type: integer.
    
    Returns a String containing customers's choice
    """

    available_sauces = ["tomato", "barbecue", "none"]

    print(f"{indent_two}What sauce should be included on Burger {burger_num}?")

    sauce_selection = customer_choice(
        choice_list = available_sauces,
        message = f"{indent_three}Please type 'tomato', 'barbecue' or 'none': ")
    
    return sauce_selection 

def handle_numeric_input(min, max):
    """Handle customer input for choices where customers select an amount.
    Ensures that inputs can be converted to an integer, and that the integer is between the minimum 
    and maximum amounts.
    
    Arguements:
    min -- the minimum valid number
    max -- the maximum valid number

    Returns the chosen number as an integer
    """

    amount = min -1

    while amount < min or amount > max:
        try:
            amount = int(input(f"{indent_three}Please enter a number between {min} and {max}: "))
            if amount < min or amount > max:
                print(f"{indent_three}Number must be between {min} and {max}: ")
        except ValueError:
                print(f"{indent_three}That was not a number")

    return amount

def how_many(filling_type, burger_num, min, max):
    """Handle customer input for choices which require customers to select an amount.
    Calls the handle_numeric_input fuction to ensure responses are integers within the specified range.
    
    Arguements:
    filling_type -- String representing filling, for inclusion in print statement.
    burger_num -- which burger the current choice is for. Type: integer.
    min -- the minimum valid number
    max -- the maximum valid number

    Returns the chosen number as an integer
    """

    print(f"{indent_two}How many {filling_type} should be included on burger number {burger_num}: ")
    amount = handle_numeric_input(min, max)

    return amount
    
def salad(salad_type, burger_num):
    """Ask customer whether each burger should contain specific salad items.
    Calls the customer_choice function to ensure responses are valid.
    
    Arguements:
    salad_type -- String representing which salad is currently being chosen
    burger_num -- which burger the current choice is for. Type: integer
    
    Returns choice as a boolean value
    """

    print(f"{indent_two}Would you like {salad_type} on burger number {burger_num}?")

    with_salad = customer_choice(
        choice_list = ["yes", "no"], 
        message = f"{indent_three}Please type 'yes' or 'no': ")
    
    if with_salad == "yes":
        choice_as_bool = True
    elif with_salad == "no":
        choice_as_bool = False

    return choice_as_bool

def each_burger_cost(burger_order):
    """Calculate the cost of individual burgers.
    
    Arguements:
    burger_order -- dictionary containing details of the current burger

    Returns burger_order dictionary with updated price field
    """
    
    burger_price = prices["base"]

    if burger_order["bun"] == "gluten free":
        burger_price += prices["gluten_free"]
    if burger_order["patties"] > 1:
        burger_price += prices["patty"] * (burger_order["patties"] - 1)
    if burger_order["cheese"] > 1:
        burger_price += prices["cheese"] * (burger_order["cheese"] - 1)

    salad_number = 0

    for salad_type in burger_order["tomato"], burger_order["lettuce"], burger_order["onion"]:
        if salad_type:
            salad_number += 1

    if salad_number > 1:
        burger_price += prices["salad"] * (salad_number - 1)

    burger_order["price"] = burger_price
    return burger_order

def create_burger(bur_num):
    """Creates a dictionary containing details of the current burger.
    Calls relevent functions to fill each field.
    
    Arguements:
    bur_num -- which burger the current choice is for. Type: integer.

    Returns burger details as a dictionary
    """
    
    print("\n" + f"{indent_one}Details for burger {bur_num}:")
    new_burger = {
        "burger" : bur_num,
        "bun" : type_of_bun(bur_num),
        "sauce" : type_of_sauce(bur_num),
        "patties" : how_many(
            filling_type = "patties", 
            burger_num = bur_num, 
            min = 0, 
            max = 3),
        "cheese" : how_many(
            filling_type = "cheese slices", 
            burger_num = bur_num, 
            min = 0, 
            max = 3),
        "tomato" : salad(
            salad_type = "tomato",
            burger_num = bur_num),
        "lettuce" : salad(
            salad_type = "lettuce",
            burger_num = bur_num),
        "onion" : salad(
            salad_type = "onion",
            burger_num = bur_num), 
        "price" : 0
        }
    
    each_burger_cost(new_burger)  # Updates the price field above
    return new_burger

def total_cost(list_of_burgers):
    """Calculate the cost for all burgers combined
    
    Arguements:
    list_of_burgers -- a list of dictionaries containing information for individual burgers
    
    Returns total_cost as an integer
    """
    
    total_cost = 0 
    for burger in range(len(list_of_burgers)):
        total_cost += list_of_burgers[burger]["price"]

    return total_cost

def take_order_and_display_cost():
    """Main ordering function. 
    Takes user input to determine how many burgers are required, and calls create_burger function for each.
    Displays total cost to user and a message to end the interaction.
    """

    print("Welcome to Codetown Burger Co! \n")
    print("How many burgers would you like to order?")
    number_of_burgers = handle_numeric_input(min = 1, max = 10)

    burger_list = []  # Initialise an empty list to store the orders as a disctionary for each burger

    for burger in range(number_of_burgers):
        burger_number = burger + 1  # burger starts at index 0, but need burger_number needs to start from 1
        burger_list.append(create_burger(bur_num = burger_number))
    
    total = total_cost(list_of_burgers = burger_list)
    print("\n")
    print(f"The total cost for all burgers is ${total}")
    print(f"{indent_one}Thank you for visiting Codetown Burger Co!")

take_order_and_display_cost()