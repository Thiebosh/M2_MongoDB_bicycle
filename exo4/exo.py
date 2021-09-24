from ast import Str
from tkinter.constants import BOTH
from guizero import App, Box, TextBox, ListBox, Text, PushButton

from exo4.exo4_1.exo import searchByTownAndStation
from exo4.exo4_2.exo import updateStation
from exo4.exo4_3.exo import deleteStation
from exo4.exo4_4.exo import flipStations
from exo4.exo4_5.exo import step5


class exo4:
    def __init__(self, collection_live, collection_history, *_):
        self.collection_live = collection_live
        self.collection_history = collection_history
        self.resultList = []
        self.resultContainer = None
        self.resultButtons = []
        self.updatePanel = None
        self.updateInputs = None
        self.updateButton = None

        try:
            app = App(title="Business program", height="600", width="800")
            app.tk.resizable(False, False)  # everything will be absolutely relative

            self.createLeftScreen(app)
            Box(app, height="fill", align="left", border=True)
            self.createRightScreen(app)

            app.display()
        except Exception as e:
            print(e)


    def resultContainerSelection(self):
        self.updatePanel.hide()

        if not self.resultContainer.value:
            for btn in self.resultButtons:
                btn.disable()
            return

        for btn in self.resultButtons:
            btn.enable()

        if len(self.resultContainer.value) > 1:
            self.resultButtons[0].disable()


    def createLeftScreen(self, container):
        resultBox = Box(container, height="fill", width=int(container.width/3), align="left")

        resultTitle = Box(resultBox, width="fill")
        Text(resultTitle, text="Résultats de recherche")

        self.resultContainer = ListBox(resultBox, height="fill", width=resultBox.width, multiselect=True, #scrollbar=True,
                                        command=self.resultContainerSelection)

        menu_box = Box(resultBox, align="bottom", layout="grid")

        # # sadly not working... peut être en l'englobant dans une frame tkinter
        # from tkinter import Listbox as tkListbox, Scrollbar
        # scrollbar = Scrollbar(resultBox.tk, orient="horizontal")
        # scrollbar.pack(side="bottom", fill="both")
        # tkListbox(self.resultContainer.tk).configure(xscrollcommand=scrollbar.set)
        # scrollbar.configure(command=tkListbox(self.resultContainer.tk).xview)

        buttons = [
            {
                "name": "Modifier infos",
                "command": self.leftScreen_update,
                "args": (),
                "grid": [0,0]
            },
            {
                "name": "Supprimer sélection",
                "command": self.leftScreen_delete,
                "args": (),
                "grid": [1,0]
            },
            {
                "name": "Activer sélection",
                "command": self.leftScreen_flip,
                "args": (True,),
                "grid": [0,1]
            },
            {
                "name": "Désactiver sélection",
                "command": self.leftScreen_flip,
                "args": (False,),
                "grid": [1,1]
            }
        ]
        for button in buttons:
            btn = PushButton(menu_box, width="15", grid=button["grid"], text=button["name"],
                                command=button["command"], args=button["args"], enabled=False)
            self.resultButtons.append(btn)


    def leftScreen_update(self):
        index = [i for i, entity in enumerate(self.resultList)
                if self.resultContainer.value[0] == f"{entity['ville']} ; {entity['nom']}"][0]

        entity = self.resultList[index]

        inputs = {}
        for i, (key, value) in enumerate(entity.items()):
            if key in ["_id", "geometry"]:
                continue

            Text(self.updateInputs, grid=[0,i], text=key)
            Text(self.updateInputs, grid=[1,i])  # margin
            inputs[key] = TextBox(self.updateInputs, grid=[2,i], width="25", text=value)

        for i, value in enumerate(entity["geometry"]["coordinates"]):
            key = ["latitude", "longitude"][i]
            j = i + len(inputs) + 1
            Text(self.updateInputs, grid=[0,j], text=key)
            Text(self.updateInputs, grid=[1,j])  # margin
            inputs[key] = TextBox(self.updateInputs, grid=[2,j], width="25", text=value)

        self.updateButton.update_command(command=self.updateFields, args=(index, entity, inputs))
        
        self.updatePanel.show()


    def leftScreen_delete(self):
        self.updatePanel.hide()

        indexes = [i for i, entity in enumerate(self.resultList)
                    if f"{entity['ville']} ; {entity['nom']}" in self.resultContainer.value]

        to_remove = []
        for index in indexes[::-1]: # reverse
            to_remove.append(self.resultList[index])
            del self.resultList[index]

        self.resultContainer.clear()
        for item in self.resultList:
            self.resultContainer.append(f"{item['ville']} ; {item['nom']}")

        for index in indexes:
            deleteStation(self.collection_live, self.collection_history, to_remove)


    def leftScreen_flip(self, state):
        self.updatePanel.hide()
        print(f"flip {state} indexes ...")

        indexes = [i for i, entity in enumerate(self.resultList)
                    if f"{entity['ville']} ; {entity['nom']}" in self.resultContainer.value]

        flipStations(self.collection_live, indexes, state)


    def createRightScreen(self, container):
        mainSection = Box(container, height="fill", width=int(container.width*2/3))

        self.createUpperRightScreen(mainSection)

        self.createLowerRightScreen(mainSection)


    def createUpperRightScreen(self, container):
        menu_box = Box(container, align="top", layout="grid")

        frames = []
        frames.append(Box(container, width="fill", align="top"))
        self.upperRight_form(frames[-1])
        
        frames.append(Box(container, width="fill", align="top"))
        self.upperRight_map(frames[-1])
        
        frames.append(Box(container, width="fill", align="top"))
        self.upperRight_stats(frames[-1])

        for i, name in enumerate(["Formulaire", "Map", "Statistiques"]):
            PushButton(menu_box, width="22", grid=[i,0], text=name, command=self.showFrame, args=(frames, i))
            frames[i].hide()


    def showFrame(self, frames, index):
        for frame in frames:
            frame.hide()
        frames[index].show()


    def upperRight_form(self, container):
        Box(container, height="10")  # margin

        Text(container, text="Recherche de station")

        Box(container, height="25")  # margin

        inputs = {
            "town": {
                "text": "Ville cible"
            },
            "station": {
                "text": "Nom de station"
            }
        }
        inputsContainer = Box(container, layout="grid")
        for i, (key, data) in enumerate(inputs.items()):
            Text(inputsContainer, grid=[0,i], text=data["text"])
            Text(inputsContainer, grid=[1,i])  # margin
            inputs[key]["ptr"] = TextBox(inputsContainer, grid=[2,i], width="25")

        Box(container, height="40")  # margin

        args = (inputs["town"]["ptr"], inputs["station"]["ptr"])
        PushButton(container, text="Rechercher", width="16",
                    command=self.updateResult_form, args=args)


    def upperRight_map(self, container):
        Box(container, height="10")  # margin

        Text(container, text="Polygonalisation")


    def upperRight_stats(self, container):
        Box(container, height="10")  # margin

        Text(container, text="Recherche statistique")


    def updateResult_form(self, town, station):
        self.updatePanel.hide()
        self.resultContainer.clear()

        for item in searchByTownAndStation(self.collection_live, town.value, station.value):
            self.resultContainer.append(f"{item['ville']} ; {item['nom']}")
            self.resultList.append(item)


    def createLowerRightScreen(self, container):
        updateBox = Box(container, width="fill", align="bottom")
        Box(updateBox, width="fill", align="top", border=True)

        Box(updateBox, height="10")  # margin

        Text(updateBox, text="Modification des données d'une station")

        Box(updateBox, height="25")  # margin

        self.updateInputs = Box(updateBox, layout="grid")

        Box(updateBox, height="40")  # margin

        self.updateButton = PushButton(updateBox, text="Modifier", width="16")

        Box(updateBox, height="10")  # margin

        self.updatePanel = updateBox
        self.updatePanel.hide()

    
    def updateFields(self, index, entity, inputs):
        intFields = ["nbvelosdispo", "nbplacesdispo", "nbplacestotal"]
        for key, value in inputs.items():            
            if key in ["longitude", "latitude"]:
                continue

            try:
                entity[key] = int(value.value) if key in intFields else value.value
            except:
                pass # no modif

        try:
            entity["geometry"]["coordinates"] = [int(inputs["latitude"].value), int(inputs["longitude"].value)]
        except:
            pass # no modif

        self.resultList[index] = entity

        self.resultContainer.clear()
        for item in self.resultList:
            self.resultContainer.append(f"{item['ville']} ; {item['nom']}")

        updateStation(self.collection_live, entity)

        self.updatePanel.hide()
