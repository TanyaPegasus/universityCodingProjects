"""
A program which creates a graphical user interface intended for displaying in
the fictional burger restaurant, "Codetown Burger Co".

The display cycles through each of the 4 named burgers every 5 seconds. 
Users can press the buttons along the bottom to view information for a 
specific burger, and the program will reset the cycle, displaying the 
next burger 5 seconds after the user selection.

The image files related to the program must be stored within the same 
directory as menu.py, or the file paths must be updated to reflect the
correct locations.

Additional Note:
This program was designed by a vision impaired developer using a system wide display 
setting of 175%. When resizing, no elements will be squashed, and elements will stay 
proportional, however the overall design but may seem a little smaller than expected 
when viewed on other systems, but could be adjusted to suit client specifications when 
provided.

Author: Tanya
Trimester 1, 2024
"""

from tkinter import *
from tkinter import ttk

root = Tk()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 750

CODE_STYLE_FONT = 'Lucida Console'

COLOURS = {
    "base" : "#1e1e2e",
    "mantle" : "#181825",
    "crust" : "#11111b",
    "mauve" : "#cba6f7",
    "cat_blue" : "#89b4fa",
    "cat_red" : "#f38ba8",
    "orange_peach" : "#fab387",
    "cat_white" : "#cdd6f4",
    "cat_green" : "#a6e3a1",
    "teal" : "#94e2d5",
    "cat_yellow": "#e5c890"
}

# large images displayed on the right
BYTE_IMAGE = "byte.png"
CAD_IMAGE = "cad.png"
DATA_CRUNCH_IMAGE = "dataCrunch.png"
CODE_CRUNCHER_IMAGE = "codeCruncher.png"

# Smalle images displayed on the buttons
BYTE_BUTTON_IMAGE = "byteButton.png"
CAD_BUTTON_IMAGE = "cadButton.png"
DC_BUTTON_IMAGE = "dataCrunchButton.png"
CC_BUTTON_IMAGE = "codeCruncherButton.png"

HEADER_IMAGE = "burgerHeader.png"

PRICES = {
    "base" : 5,  # Includes milk bun, sauce, up to 1 patty, 1 cheese slice, and 1 salad item.
    "gluten_free" : 1,  # Additional cost.
    "patty" : 3,  # 1 included. Price per additional patty.
    "cheese" : 1,  # 1 included, Price per additional cheese slice.
    "salad" : 1  # tomato, lettuce or onion included in base price. Price per additional salad item. 
}

next_burger_number = 0 # index number used by cycle_burgers()
current_after_task = None # ID used to ideantify tcl.after task currently running
burger_list = [] # initiated here and extended after Burger instances are created.


def create_photoimage(filename):
    """Creates tkinter PhotoImage widget.

    To display an image on another widget, a PhotoImage widget must be created first.
    When the widget can't be created, a TclError is raised. Function tries to create the widget or displays 
    a message informing the user about the error, then exits the program.

    Arguments:
    filename -- String representing the image filename includeing file extension eg "byte.png"

    Returns:
    PhotoImage widget -- for use within other widgets
    """
    try:
        photoimage = PhotoImage(file= filename)
        return photoimage
    except TclError:
        print(f"{filename} can't be found")
        exit()


class Burger:
    """Class to store information about available burgers

    Attributes:
    name -- String representing the burger name
    bun -- String representing the bun type as "milk" or "gluten free"
    sauce -- String representing the sauce type as "tomato", "barbeque" or "none"
    patty -- Int representing the number of patties between 0 and 3
    cheese -- Int representing the number of cheese slices between 0 and 3
    tomato -- Boolean representing whether the burger has tomato
    lettuce -- Boolean representing whether the burger has lettuce
    onion -- Boolean representing whether the burger has onion
    main_image -- String representing the image filename for display on the right of the window
    button_image -- String representing the image filename for display on the button
    
    Methods:
    get_cost() -- Calculate the cost of individual burgers
    display_ingredients_list() -- Format ingredients_list Text widget display
    create_button -- onfigure the frames and buttons along the bottom of the window
    """

    def __init__(self, name, bun, sauce, patty, cheese, tomato, lettuce, onion, main_image, button_image):
        """Initialise attributes of a burger

        Calls create_phoimage() to ensure filenames passed for main_image and button_image are valid, and
        then create their widget.
        """
        self.name = name
        self.bun = bun
        self.sauce = sauce
        self.patty = patty
        self.cheese = cheese
        self.tomato = tomato
        self.lettuce = lettuce
        self.onion = onion
        self.main_image = create_photoimage(main_image)
        self.button_image = create_photoimage(button_image)

    def get_cost(self):
        """Calculate the cost of individual burgers.
        
        Called by display_ingredients_list()

        Returns:
        int -- The price of the burger as an integer 
        """
        burger_price = PRICES["base"]
        
        if self.bun == "gluten free":
            burger_price += PRICES["gluten_free"]
        if self.patty > 1:
            burger_price += PRICES["patty"] * (self.patty - 1)
        if self.cheese > 1:
            burger_price += PRICES["cheese"] * (self.cheese - 1)

        salad_number = 0
        for salad_type in self.tomato, self.lettuce, self.onion:
            if salad_type:
                salad_number += 1

        if salad_number > 1:
            burger_price += PRICES["salad"] * (salad_number - 1)

        return burger_price
    
    def display_ingredients_list(self):
        """Format ingredients_list Text widget display
        
        Called by cycle_burgers()
        """
        ingredients_list = [
            # from codetown import the_best_burgers
            ("from ", "mauve"), ("codetown ", "cat_yellow"), ("import ", "mauve"), ("the_best_burgers\n\n", "cat_yellow"),
            # def create_burger():
            ("def ", "mauve"), ("create_burger", "cat_blue"), ("():\n", "cat_red"),
            # burger_name = name
            ("\tburger_name", "cat_white"), (" = ", "teal"), (f"'{self.name}'\n", "cat_green_bold"),
            # ingredients = [
            ("\tingredients", "cat_white"), (" = ", "teal"), ("[\n", "cat_red")
        ]

        ingredients_list.append((f"\t\t'{self.bun} bun',\n", "cat_green")),
        ingredients_list.append((f"\t\t'{self.sauce} sauce,'\n", "cat_green")),

        if self.patty == 0:
            num_patties = "\t\t'No Meat Patties',\n"
        elif self.patty == 1:
            num_patties = f"\t\t'{self.patty} Meat Patty',\n"
        elif self.patty > 1:
            num_patties = f"\t\t'{self.patty} Meat Patties',\n"
        ingredients_list.append((num_patties, "cat_green"))

        if self.cheese == 0:
            num_cheese = "\t\t'No Cheese',\n"
        elif self.cheese == 1:
            num_cheese = f"\t\t'{self.cheese} Slice of Cheese',\n"
        elif self.cheese > 1:
            num_cheese = f"\t\t'{self.cheese} Slices of Cheese',\n"
        ingredients_list.append((num_cheese, "cat_green"))
        
        if self.tomato:
            tomato_choice = "\t\t'Tomato',\n"
        else:
            tomato_choice = "\t\t'No Tomato',\n"
        ingredients_list.append((tomato_choice, "cat_green"))

        if self.lettuce:
            lettuce_choice = "\t\t'Lettuce',\n"
        else:
            lettuce_choice = "\t\t'No Lettuce',\n"
        ingredients_list.append((lettuce_choice, "cat_green"))

        if self.onion:
            onion_choice = "\t\t'Onion',\n"
        else:
            onion_choice = "\t\t'No Onion',\n"
        ingredients_list.append((onion_choice, "cat_green"))

        ingredients_list.append(("\t\t]\n", "cat_red"))
        ingredients_list.append(("\tprice", "cat_white"))
        ingredients_list.append((" = ", "teal")) 
        ingredients_list.append((f"'${self.get_cost()}'\n", "orange_peach"))

        # Allow the prgram to edit the ingredients_text widget
        ingredients_text.config(state= "normal")
        
        for i in range(len(ingredients_list)):
            ingredients_text.insert(END, ingredients_list[i][0], ingredients_list[i][1])
       
        # Prevent users from editing the text in the display
        ingredients_text.config(state= "disabled")
    
    def create_button(self, button_number):
        """Configure the frames and buttons along the bottom of the window.
        
        Called in a for loop for all Burger instances, after bottom_frame has
        been created.

        Arguments:
        button_number -- Int representing the index of the Burger in burger_list
        """
        this_frame = ttk.Frame(
            bottom_frame, 
            width= WINDOW_WIDTH/4,
            height= 150, 
            style= 'crust.TFrame')
        this_frame.grid(column= button_number, row= 0, sticky = (N, W, E, S))

        this_button = ttk.Button(
            this_frame, 
            # text= self.name, 
            image= self.button_image, 
            # compound= "bottom", 
            style= 'TButton', 
            command= lambda: skip_to_burger(button_number))
        this_button.grid(column= 0, row= 0)
        this_button.place(relx= 0.5, rely= 0.5, anchor= CENTER)


def skip_to_burger(index_number):
    """Skip to selected burger when user clicks a button.
    
    Changes the index of the next burger to display to the user's selection, and 
    cancels the current 5 second countdown. Calls cycle_burgers() to display the choice 
    and start a new countdown.

    Arguments:
    index_number -- index number of the selected burger in burger_list
    """
    global next_burger_number
    global current_after_task

    next_burger_number = index_number
    root.after_cancel(current_after_task)

    cycle_burgers()

def cycle_burgers():
    """Controls current burger to display, and sets up 5 second countdown
    
    Called once at the start of the program and sets up an 'after' task
    to call this function again after 5 seconds. If user selects a burger, the
    task is cancelled by skip_to_burger(), before this function is called again.
    """
    global next_burger_number
    global current_after_task

    next_burger = burger_list[next_burger_number]

    burger_pic.config(image= next_burger.main_image)
    ingredients_text.config(state="normal")
    ingredients_text.delete('1.0', END)
    next_burger.display_ingredients_list()
    current_after_task = root.after(5000, cycle_burgers)
    ingredients_text.config(state= "disabled")

    if next_burger_number >= 0 and next_burger_number < len(burger_list) -1:
        next_burger_number += 1
    else: next_burger_number = 0


# Create burger objects
byte_burger = Burger("Byte Burger", "milk", "tomato", 1, 0, False, True, False, BYTE_IMAGE, BYTE_BUTTON_IMAGE)
ctrl_alt_delicious = Burger("Ctrl-Alt-Delicious", "milk", "barbecue", 2, 2, True, True, True, CAD_IMAGE, CAD_BUTTON_IMAGE)
data_crunch = Burger("Data Crunch", "gluten free", "tomato", 0, 0, True, True, True, DATA_CRUNCH_IMAGE, DC_BUTTON_IMAGE)
code_cruncher = Burger("Code Cruncher", "milk", "tomato", 3, 3, True, True, True, CODE_CRUNCHER_IMAGE, CC_BUTTON_IMAGE)
burger_list.extend([byte_burger, ctrl_alt_delicious, data_crunch, code_cruncher])

# Set up style information used in ttk.Frame widgets
my_style = ttk.Style()
my_style.configure('base.TFrame', background = COLOURS["base"])
my_style.configure('mantle.TFrame', background = COLOURS["mantle"])
my_style.configure('crust.TFrame', background = COLOURS["crust"])
my_style.configure('TButton',  font = (CODE_STYLE_FONT, 15), background = COLOURS["crust"], foreground = COLOURS["crust"])

# Set up the root window
root.title("Codetown Burger Menu")
root.config(background= COLOURS["base"])
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}') # +30+30
root.minsize(WINDOW_WIDTH - 100, WINDOW_HEIGHT - 50)

# grid_propogate(False) prevents child widgets from autromatically resizing the grid 
#  to fit themselves.
root.grid_propagate(False) 
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight= 0)
root.rowconfigure(1, weight= 2)
root.rowconfigure(2, weight= 1, minsize= WINDOW_HEIGHT * 0.25)

# top_frame frame holds the header image
top_frame = ttk.Frame(root, width= WINDOW_WIDTH, height= WINDOW_HEIGHT * 0.15, style= 'crust.TFrame')
top_frame.grid(column= 0, row= 0, sticky = (N, W, E, S))
top_frame.grid_propagate(False)

burger_header_image = create_photoimage(HEADER_IMAGE)
title_label = ttk.Label(top_frame, image= burger_header_image)
title_label.config(font= (CODE_STYLE_FONT, 30), background= COLOURS["crust"])
title_label.grid(column= 0, row= 0, sticky = (N, W, S))

# centre_frame holds the ingredients list display, and the large burger image
centre_frame = ttk.Frame(root, width= WINDOW_WIDTH, height= WINDOW_HEIGHT * 0.6, style= 'base.TFrame')
centre_frame.grid(column= 0, row= 1, sticky = (N, W, E, S))
centre_frame.grid_propagate(False)
centre_frame.columnconfigure(0, weight = 3)
centre_frame.columnconfigure(1, weight = 2)
centre_frame.rowconfigure(0, weight= 1)

ingredients = ttk.Frame(centre_frame, style= 'mantle.TFrame')
ingredients.grid_propagate(False)
ingredients.grid(column= 0, row= 0, sticky = (N, W, E, S))
ingredients.columnconfigure(0, weight = 1)
ingredients.rowconfigure(0, weight= 1)

ingredients_text = Text(ingredients, bg= COLOURS["mantle"], bd= 0, wrap= 'none', selectbackground= COLOURS["mantle"])
ingredients_text.grid(column= 0, row= 0, sticky = (N, W, E, S))
ingredients_text.place(relx= 0.65, rely= 0.6, anchor= CENTER)

# Create the tags for the colours used to display the ingredients
for colour in COLOURS.items():
    ingredients_text.tag_config(tagName= colour[0], foreground= colour[1], font=(CODE_STYLE_FONT, 15))
ingredients_text.tag_config("cat_green_bold", foreground= COLOURS["cat_green"], font=(CODE_STYLE_FONT, 15, "bold"))

burger_frame = ttk.Frame(centre_frame, padding= 0, relief= FLAT, style= 'base.TFrame')
burger_frame.grid_propagate(False)
burger_frame.grid(column= 1, row= 0, sticky = (N, W, E, S))
burger_frame.columnconfigure(0, weight = 1)
burger_frame.rowconfigure(0, weight= 1)

burger_pic = Label(burger_frame, image= byte_burger.main_image, border= 0, relief= FLAT)
burger_pic.configure(background= COLOURS["base"])
burger_pic.grid(column= 0, row= 0, sticky = (N, W, E, S))

# bottom_frame holds the 4 buttons along the bottom
bottom_frame = ttk.Frame(root, width= WINDOW_WIDTH, height= WINDOW_HEIGHT * 0.25, style= 'mantle.TFrame')
bottom_frame.grid(column= 0, row= 2, sticky = (N, W, E, S))
bottom_frame.grid_propagate(False)
bottom_frame.columnconfigure(0, weight = 1)
bottom_frame.columnconfigure(1, weight = 1)
bottom_frame.columnconfigure(2, weight = 1)
bottom_frame.columnconfigure(3, weight = 1)
bottom_frame.rowconfigure(0, weight= 1)

# set up the buttons:
for burger in burger_list:
    burger.create_button(burger_list.index(burger))

# Display the first burger of the program
# First 5 second countdown is initiated inside cycle_burgers() 
cycle_burgers()
root.mainloop()
