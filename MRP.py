import PySimpleGUI as sg

class Product:
    products = []

    def __init__(self, name, craft_time, starting_volume = 0, ingredients = None):
        self.name = name
        self.craft_time = int(craft_time)
        self.volume = int(starting_volume)
        self.ingredients = ingredients

        Product.products.append(self)
    
    def __str__(self):
        return f"{self.name}, in storage {self.volume}, Ingredients:{self.ingredients}"

    def Craft(self, requested_volume, ready_on):
        start_crafting = ready_on - self.craft_time

        if self.ingredients:
            #iterate over all ingredients specified when definid this product
            for ingredient_dict in self.ingredients:
                #get ingredient name and volume from ingredient dictionary ie. {"name" : volume}
                ingredient_name = list(ingredient_dict.keys())[0]
                ingredient_volume = list(ingredient_dict.values())[0]

                #get the ingredient of the given name
                ingredient = list(filter(lambda x: x.name == ingredient_name, Product.products))[0]

                #check if ingredient is in product list and is an instance of class Product
                if ingredient in Product.products and isinstance(ingredient, Product):
                    #caluclate the volume to craft and update storage ammount of ingredient
                    if ingredient.volume > ingredient_volume * requested_volume:
                        volume_to_craft = 0
                        ingredient.volume -= ingredient_volume * requested_volume
                    else:
                        volume_to_craft = ingredient_volume * requested_volume - ingredient.volume
                        ingredient_volume = 0

                    #start crafting of the ingredient, start_crafting is when current product needs to start crafting ie. on when the ingredient needs to be ready
                    if volume_to_craft > 0:
                        ingredient.Craft(volume_to_craft, start_crafting)
        print(f"{requested_volume} {self} started crafting on {start_crafting} week")

class Table:
    td = []
    Ingredients = []
    Ingredients_Table = []     
def setup():

    layout = [[sg.Text("Input you product information")],
            [sg.Text("Name", size=(15,1)), sg.InputText(key="Name")],
            [sg.Text("Time to produce", size=(15,1)), sg.InputText(key="craft_time")],
            [sg.Text("Ammount in storage", size=(15,1)), sg.InputText(key="starting_volume")],
            [sg.Text("Ingredients", size=(15,1)), sg.InputText(key="ingredient_Name"),
                                                  sg.Spin([i for i in range(0, 99)], initial_value=1, key="ingredient_volume"),
                                                  sg.Button("Add ingredient")],
            [sg.Table(Table.Ingredients_Table, ["Name", "Ammount"], key = "ingredients_table", row_height=20, num_rows=2)],
            [sg.Button("Submit"), sg.Button("Clear Input"), sg.Button("Clear Table"), sg.Button("Cancel")],
            [sg.Table(Table.td, ["Name", "Time to produce", "Ammount in storage", "Ingredients"], key = "my_table")]]

    # Create the Window
    window = sg.Window('Hello Example', layout)

    def Clear_input():
        window["Name"]("")
        window["craft_time"]("")
        window["starting_volume"]("")
        window["ingredient_Name"]("")
        window["ingredient_volume"](1)
        Table.Ingredients = []
        Table.Ingredients_Table = []

        values["ingredient_Name"] = []
        values["ingredient_volume"] = []
        window["ingredients_table"].update(values = Table.Ingredients_Table)

    def Clear_table():
        Table.td = []
        window["my_table"].update(values = Table.td)
        Table.Ingredients = []

    def Add_ingredient():
        Table.Ingredients_Table.append([values["ingredient_Name"], values["ingredient_volume"]])
        Table.Ingredients.append({values["ingredient_Name"]: values["ingredient_volume"]})
        window["ingredients_table"].update(values = Table.Ingredients_Table)

        window["ingredient_Name"]("")
        window["ingredient_volume"](1)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        
        # if user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        if event == "Clear Input":
            Clear_input()

        if event == "Clear Table":
            Clear_table()

        if event == "Add ingredient":
            Add_ingredient()

        if event == "Submit":
            Table.td.append([values["Name"], values["craft_time"], values["starting_volume"], Table.Ingredients])
            window["my_table"].update(values = Table.td)
            Clear_input()



    window.close()

def main():
    setup()
    
    '''
    leg = Product("leg", 1, 2)
    desk = Product("desk", 2, 1)
    chair = Product("Chair", 3, 0, [{'leg': 4}, {'desk': 1}])
    chair.Craft(4, 8)
    '''
    
    products = []
    #start wtih last product
    td = Table.td[::-1]
    for product in td:
        products.append(Product(product[0], product[1], product[2], product[3]))
    for product in Product.products:
        print(product)
        

    products[-1].Craft(4, 8)
    


main()