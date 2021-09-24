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
        self.updatePanel = None

        try:
            app = App(title="Business program", height="600", width="800")
            app.tk.resizable(False, False)  # everything will be absolutely relative

            self.createLeftScreen(app)
            Box(app, height="fill", align="left", border=True)
            self.createRightScreen(app)

            app.display()
        except Exception as e:
            print(e)


    def createLeftScreen(self, container):
        resultBox = Box(container, height="fill", width=int(container.width/3), align="left")

        resultTitle = Box(resultBox, width="fill")
        Text(resultTitle, text="Résultats de recherche")

        self.resultContainer = ListBox(resultBox, height="fill", width=resultBox.width, scrollbar=True)

        menu_box = Box(resultBox, align="bottom", layout="grid")
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
            PushButton(menu_box, width="15", grid=button["grid"], text=button["name"],
                        command=button["command"], args=button["args"])


    def leftScreen_update(self):
        self.updatePanel.hide()
        print("update index ...")
        # search index in resultContainer

        self.updatePanel.show()


    def leftScreen_delete(self):
        self.updatePanel.hide()
        print("delete indexes ...")
        # search indexes in resultContainer

        for index in []:
            # remove index in resultContainer
            deleteStation(self.collection_live, self.collection_history, self.resultList[0]) # index
            # remove index in resultList


    def leftScreen_flip(self, state):
        self.updatePanel.hide()
        print(f"flip {state} indexes ...")
        # search indexes in resultContainer

        flipStations(self.collection_live, [], state)


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

        self.resultList = searchByTownAndStation(self.collection_live, town.value, station.value)

        for item in self.resultList:
            self.resultContainer.append(f"{item['ville']} ; {item['nom']}")


    def createLowerRightScreen(self, container):
        updateBox = Box(container, width="fill", align="bottom")
        Box(updateBox, width="fill", align="top", border=True)

        Box(updateBox, height="10")  # margin

        Text(updateBox, text="Modification des données d'une station")

        Box(updateBox, height="25")  # margin

        inputs = {
            "town": {
                "text": "Champ",
                "placeholder": "Donnée"
            }
        }
        inputsContainer = Box(updateBox, layout="grid")
        for i, (key, data) in enumerate(inputs.items()):
            Text(inputsContainer, grid=[0,i], text=data["text"])
            Text(inputsContainer, grid=[1,i])  # margin
            inputs[key]["ptr"] = TextBox(inputsContainer, grid=[2,i], width="25", text=data["placeholder"])

        Box(updateBox, height="40")  # margin

        PushButton(updateBox, text="Modifier", width="16",
                    command=self.updateFields, args=())

        Box(updateBox, height="10")  # margin

        self.updatePanel = updateBox
        self.updatePanel.hide()

    
    def updateFields(self):
        newObject = self.resultList[0] # index

        # update newObject with fields

        updateStation(self.collection_live, newObject)

        # update self.resultContainer if displayed data changed

        self.updatePanel.hide()
