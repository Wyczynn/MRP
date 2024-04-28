import PySimpleGUI as sg
import pandas as pd

class Product:
    products = []

    def __init__(self, name, craft_time, starting_volume = 0, ingredients = None):
        self.name = name
        self.craft_time = int(craft_time)
        self.volume = int(starting_volume)
        self.ingredients = ingredients

        Product.products.append(self)
    
    def Craft(self, requested_volume, ready_on):
        #update storage ammount of ingredient
        craft_volume = requested_volume - self.volume
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
                    #caluclate the volume to craft
                    volume_to_craft = ingredient_volume * craft_volume

                    #start crafting of the ingredient, start_crafting is when current product needs to start crafting ie. on when the ingredient needs to be ready
                    if volume_to_craft > 0:
                        ingredient.Craft(volume_to_craft, start_crafting)

        Table.time.append([self.name, requested_volume, ready_on, craft_volume, start_crafting])

class Table:
    td = []
    Ingredients = []
    Ingredients_Table = []
    time = []
def setup():

    layout = [[sg.Text("Input you product information")],
            [sg.Text("Name", size=(20,1)), sg.InputText(key="Name")],
            [sg.Text("Time to produce(days)", size=(20,1)), sg.InputText(key="craft_time")],
            [sg.Text("Ammount in storage", size=(20,1)), sg.InputText(key="starting_volume")],
            [sg.Text("Ingredients", size=(20,1)), sg.InputText(key="ingredient_Name"),
                                                  sg.Spin([i for i in range(0, 99)], initial_value=1, key="ingredient_volume"),
                                                  sg.Button("Add ingredient")],
            [sg.Table(Table.Ingredients_Table, ["Name", "Ammount"], key = "ingredients_table", row_height=20, num_rows=2)],
            [sg.Button("Add Product"), sg.Button("Clear Input"), sg.Button("Clear Table"), sg.Button("Cancel"), sg.Button("Submit")],
            [sg.Table(Table.td, ["Name", "Time to produce", "Ammount in storage", "Ingredients"], key = "my_table")]]

    layout2 = [[sg.Table(Table.td, ["Name", "Time to produce", "Ammount in storage", "Ingredients"], key = "my_table")],
               [sg.Text("Name of the main item"), sg.InputText(key="name")],
               [sg.Text("Requested ammount"), sg.InputText(key="volume")],
               [sg.Text("Delivery date"), sg.InputText(key="delivery")],
               [sg.Button("Cancel"), sg.Button("Craft")]]
    # Create the Window
    window = sg.Window('MRP2000', layout)

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
        if event == sg.WIN_CLOSED or event == "Cancel" or event == "Submit":
            break
        if event == "Clear Input":
            Clear_input()

        if event == "Clear Table":
            Clear_table()

        if event == "Add ingredient":
            Add_ingredient()

        if event == "Add Product":
            Table.td.append([values["Name"], values["craft_time"], values["starting_volume"], Table.Ingredients])
            window["my_table"].update(values = Table.td)
            Clear_input()
    window.close()

    #create window to specify what to craft
    window = sg.Window('MRP2000', layout2)
    for product in Table.td:
        Product(product[0], product[1], product[2], product[3])

    while True:
        event, values = window.read()

        if event == "Craft":

            item_to_craft = list(filter(lambda x: x.name == values["name"], Product.products))[0]
            if isinstance(item_to_craft, Product):
                item_to_craft.Craft(int(values["volume"]), int(values["delivery"]))
            else:
                print("hello")
            break

        if event == sg.WIN_CLOSED or event == "Cancel" or event == "Submit":
            break


def main():
    setup()

    time_df = pd.DataFrame(Table.time, columns=["Product", "Requested volume", "Ready on", "Volume to craft", "Start crafting"])
    df = pd.DataFrame(Table.td, columns=["Product", "Crafting Time", "In storage", "Ingredients"])

    with pd.ExcelWriter('Product.xlsx') as writer:
        df.to_excel(writer, sheet_name='Production', startrow=1, startcol=0)
        time_df.to_excel(writer, sheet_name='Production', startrow=1+len(df)+3, startcol=0)
    
main()