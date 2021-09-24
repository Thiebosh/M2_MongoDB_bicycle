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

            # menu_box = Box(app, align="top", layout="grid", border=True)

            # frames = []
            # for i in range(5):
            #     name = f"step{i+1}"

            #     frames.append(Box(app, width=app.width, height="fill"))
            #     frames[-1].hide()

            #     PushButton(menu_box, width="18", grid=[i,0], text=name, command=showFrame, args=(frames, i))

            #     globals()[name](collection_live, collection_history, frames[-1])

            app.display()
        except Exception as e:
            print(e)


    def createLeftScreen(self, container):
        resultBox = Box(container, height="fill", width=int(container.width/3), align="left")

        resultTitle = Box(resultBox, width="fill")
        Text(resultTitle, text="Résultats de recherche")

        self.resultContainer = ListBox(resultBox, height="fill", width=resultBox.width, scrollbar=True)

        # boutons du bas
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
        searchBox = Box(container, width="fill", align="top")

        self.upperRight_form(searchBox)


    def upperRight_form(self, container):
        Text(container, text="Recherche de station")

        Box(container, height="40")  # margin

        inputs = Box(container, layout="grid")
        Text(inputs, grid=[0,0], text="Ville cible")
        Text(inputs, grid=[1,0])  # margin
        town = TextBox(inputs, grid=[2,0], width="25")
        Text(inputs, grid=[0,1], text="Nom de station")
        Text(inputs, grid=[1,1])  # margin
        station = TextBox(inputs, grid=[2,1], width="25")

        Box(container, height="40")  # margin

        PushButton(container, text="submit", command=self.updateResult_form, args=(town, station))


    def updateResult_form(self, town, station):
        self.updatePanel.hide()
        self.resultContainer.clear()

        self.resultList = searchByTownAndStation(self.collection_live, town.value, station.value)

        for item in self.resultList:
            self.resultContainer.append(f"{item['ville']} ; {item['nom']}")


    def createLowerRightScreen(self, container):
        updateBox = Box(container, width="fill", align="bottom")
        Text(updateBox, text="Modif de station")

        # add forms

        # call exo4_2 function

        self.updatePanel = updateBox
        self.updatePanel.hide()
