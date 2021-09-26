from guizero import App, Box, TextBox, ListBox, Text, PushButton, Picture, Combo
from tkinter import Scrollbar, Spinbox, DoubleVar
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.colors import ListedColormap
import json
import os

from utils.utils import listFiles, readJson, formGenerator, dumpGraph
from exo4.exo4_1.exo import searchByTownAndStation
from exo4.exo4_2.exo import updateStation
from exo4.exo4_3.exo import deleteStation
from exo4.exo4_4.exo import flipStations, getCoordsByTown, searchByPolygon
from exo4.exo4_5.exo import searchByStats


class exo4:
    def __init__(self, collection_live, collection_history, *_):
        plt.switch_backend('agg') # able to end prgm when close windows

        self.collection_live = collection_live
        self.collection_history = collection_history
        self.resultList = []
        self.resultContainer = None
        self.resultButtons = []
        self.updatePanel = None
        self.updateInputs = None
        self.updateButton = None
        self.currentFrame = None
        self.tmpDir = "tmp"
        self.baseGraphs = []
        self.graphs = []
        self.pictures = []
        self.boundingBoxes = []
        self.polygon = None

        if not os.path.exists(self.tmpDir):
            os.mkdir(self.tmpDir)

        try:
            app = App(title="Business program", height="600", width="800")
            app.tk.resizable(False, False)  # everything will be absolutely relative

            self.createLeftScreen(app)
            Box(app, height="fill", align="left", border=True)
            self.createRightScreen(app)

            app.display()
        except Exception as e:
            print(e)


    def __del__(self):
        for file in listFiles(self.tmpDir):
            os.remove(file)
        os.removedirs(self.tmpDir)


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

        self.resultContainer = ListBox(resultBox, height="fill", width=resultBox.width, multiselect=True, scrollbar=True,
                                        command=self.resultContainerSelection)

        menu_box = Box(resultBox, align="bottom", layout="grid")

        scrollbar = Scrollbar(resultBox.tk, orient="horizontal")
        scrollbar.pack(side="bottom", fill="both")
        self.resultContainer.children[0].tk.configure(xscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.resultContainer.children[0].tk.xview)

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
            if key in ["_id", "geometry", "actif"]:
                continue

            Text(self.updateInputs, grid=[0,i], text=key.title())
            Text(self.updateInputs, grid=[1,i])  # margin
            inputs[key] = TextBox(self.updateInputs, grid=[2,i], width="25", text=value)

        for i, value in enumerate(entity["geometry"]["coordinates"]):
            key = ["latitude", "longitude"][i]
            j = i + len(inputs) + 1
            Text(self.updateInputs, grid=[0,j], text=key.title())
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
            to_remove.append(self.resultList[index]["_id"])
            del self.resultList[index]

        self.resultContainer.clear()
        for item in self.resultList:
            self.resultContainer.append(f"{item['ville']} ; {item['nom']}")

        deleteStation(self.collection_live, self.collection_history, to_remove)
        self.updateMaps()


    def leftScreen_flip(self, state):
        self.updatePanel.hide()

        indexes = [i for i, entity in enumerate(self.resultList)
                    if f"{entity['ville']} ; {entity['nom']}" in self.resultContainer.value]
        dbIndexes = [self.resultList[index]["_id"] for index in indexes]

        flipStations(self.collection_live, dbIndexes, state)
        self.updateMaps()
        for index in indexes:
            self.flipDisplayState(index, state)


    def createRightScreen(self, container):
        mainSection = Box(container, height="fill", width=int(container.width*2/3))

        self.createUpperRightScreen(mainSection)

        self.createLowerRightScreen(mainSection)


    def createUpperRightScreen(self, container):
        menu_box = Box(container, align="top", layout="grid")

        frames = []
        frames.append(Box(container, width="fill", align="top"))
        self.upperRight_form(frames[-1])

        frames.append(Box(container, width="fill", height="fill", align="top"))
        self.upperRight_map(frames[-1])

        frames.append(Box(container, width="fill", height="fill", align="top"))
        self.upperRight_stats(frames[-1])

        for i, name in enumerate(["Formulaire", "Map", "Statistiques"]):
            PushButton(menu_box, width="22", grid=[i,0], text=name, command=self.showFrame, args=(frames, i))
            frames[i].hide()


    def showFrame(self, frames, index):
        self.polygon = None

        for frame in frames:
            frame.hide()
        frames[index].show()

        self.currentFrame = index


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
        formGenerator(container, inputs)

        Box(container, height="40")  # margin

        args = (inputs["town"]["ptr"], inputs["station"]["ptr"])
        PushButton(container, text="Rechercher", width="16",
                    command=self.updateResult_form, args=args)


    def upperRight_map(self, container):
        Box(container, height="10")  # margin
        Text(container, align="top", text="Sélection polygonale")
        Box(container, height="10")  # margin
        menu_box = Box(container, align="top", layout="grid")

        footer = Box(container, align="bottom")
        Box(footer, height="10")  # margin
        inputs = Box(footer, layout="grid")
        Text(inputs, grid=[0,0,1,2], text="Polygone : ")
        polyField = TextBox(inputs, grid=[1,0,1,2], width=25)
        Text(inputs, grid=[2,0])
        PushButton(inputs, grid=[3,0], width=7, text="Appliquer", command=self.draw_polygon, args=(polyField,))
        PushButton(inputs, grid=[3,1], width=7, text="Retirer", command=self.clear_polygon)
        Box(footer, height="10")  # margin
        PushButton(footer, text="Sélectionner", command=self.updateResult_polygon)
        Box(footer, height="10")  # margin

        towns = []
        for i, file in enumerate(listFiles("apis/imgs")):
            name = file[10:-4]
            towns.append(PushButton(menu_box, width="10", grid=[i,0], text=name, command=self.showMap, args=(i, polyField, towns)))

            mapBox = readJson(f"apis/{name.lower()}.json")["visual"]["boundingBox"]

            fig = plt.figure()
            ax = fig.gca()
            ax.grid(True)
            ax.imshow(plt.imread(file), extent=mapBox, zorder=0, aspect='equal')
            ax.set_xlim(mapBox[0], mapBox[1])
            ax.set_ylim(mapBox[2], mapBox[3])

            fig.savefig(f"{self.tmpDir}/{i}.png")
            self.baseGraphs.append(fig)
            self.graphs.append(fig)
            self.boundingBoxes.append([])

            self.pictures.append(Picture(container, image=f"{self.tmpDir}/{i}.png", height=350, align="top"))
            self.pictures[-1].hide()

        self.updateMaps()


    def showMap(self, i, textField, buttons):
        buttons[self.currentFrame].text = buttons[self.currentFrame].text.title()

        self.clear_polygon()
        self.showFrame(self.pictures, i)
        textField.clear()
        box = self.boundingBoxes[i]
        textField.append([[box[0], box[2]], [box[0], box[3]], [box[1], box[3]], [box[1], box[2]]]) # whole box

        buttons[i].text = buttons[i].text.upper()


    def updateMaps(self):
        for i, line in enumerate(getCoordsByTown(self.collection_live)):
            df = pd.DataFrame([line for line in line["coords"]], columns=["lat", "lon", "actif"])

            padding = 0.001 # overflow approx
            self.boundingBoxes[i] = (round(df.lon.min()-padding, 4),
                                    round(df.lon.max()+padding, 4),
                                    round(df.lat.min()-padding, 4),
                                    round(df.lat.max()+padding, 4))

            newfig = dumpGraph(self.baseGraphs[i])
            newfig.gca().scatter(df.lon, df.lat, zorder=3, s=10, c=df.actif,
                                cmap=ListedColormap(["darkolivegreen"] if len(df.actif.unique()) == 1 else ["r", "darkolivegreen"]))
            newfig.savefig(f"{self.tmpDir}/{i}.png")

            self.graphs[i]= newfig
            self.pictures[i].value = f"{self.tmpDir}/{i}.png"


    def draw_polygon(self, field):
        if not field.value:
            return

        self.polygon = json.loads(field.value)

        index = self.currentFrame
        newfig = dumpGraph(self.graphs[index])
        ax = newfig.gca()
        ax.add_patch(Polygon(self.polygon, zorder=1, alpha=0.2, color="cornflowerblue"))
        ax.add_patch(Polygon(self.polygon, zorder=2, linestyle='solid', fill=False, color="blue"))
        ax.scatter([x for x, _ in self.polygon], [y for _, y in self.polygon], c="blue", marker="x")
        newfig.savefig(f"{self.tmpDir}/{index}.png")

        self.pictures[index].value = f"{self.tmpDir}/{index}.png"


    def clear_polygon(self):
        self.polygon = None

        index = self.currentFrame
        fig = self.graphs[index]
        fig.savefig(f"{self.tmpDir}/{index}.png")

        self.pictures[index].value = f"{self.tmpDir}/{index}.png"


    def upperRight_stats(self, container):
        Box(container, height="10")  # margin
        Text(container, text="Recherche statistique")
        Box(container, height="25")  # margin

        Box(container, height="10")  # margin
        
        inputsContainer = Box(container, layout="grid")
        Text(inputsContainer, grid=[1,0], text="Ratio vélo / total ")
        comparison = [">", ">=", "==", "<=", "<"]
        compare = Combo(inputsContainer, grid=[2,0], width=2, options=comparison, selected="<")
        Text(inputsContainer, grid=[3,0])
        box = Box(inputsContainer, grid=[4,0])

        #Create an instance of Tkinter frame or window
        #Set the default value for SpinBox
        ratio = DoubleVar(box.tk, value=20.0)
        box.add_tk_widget(Spinbox(box.tk, from_=0, to=100, width=5, textvariable=ratio))
        # ratio = TextBox(inputsContainer, grid=[4,0], width=5, text="20")
        Text(inputsContainer, grid=[5,0], text=" %")

        Box(container, height="15")  # margin

        inputsContainer = Box(container, layout="grid")
        hours = list(range(24))
        minuts = list(range(0, 60, 5))
        Text(inputsContainer, grid=[1,0], text="De ")
        begin_hour = Combo(inputsContainer, grid=[2,0], width=1, options=hours, selected="18")
        Text(inputsContainer, grid=[3,0], text=":")
        begin_minuts = Combo(inputsContainer, grid=[4,0], width=1, options=minuts)
        Text(inputsContainer, grid=[5,0], text=" à ")
        end_hour = Combo(inputsContainer, grid=[6,0], width=1, options=hours, selected="19")
        Text(inputsContainer, grid=[7,0], text=":")
        end_minuts = Combo(inputsContainer, grid=[8,0], width=1, options=minuts)

        Box(container, height="15")  # margin

        inputsContainer = Box(container, layout="grid")
        days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        Text(inputsContainer, grid=[1,0], text="Du ")
        begin_week = Combo(inputsContainer, grid=[2,0], width=12, options=days, selected="Lundi")
        Text(inputsContainer, grid=[3,0], text=" au ")
        end_week = Combo(inputsContainer, grid=[4,0], width=12, options=days, selected="Vendredi")

        Box(container, height="25")  # margin

        args = (compare, ratio, begin_hour, begin_minuts, end_hour, end_minuts, days, begin_week, end_week)
        PushButton(container, width="10", text="Rechercher", command=self.updateResult_stats, args=args)


    def updateResult_form(self, town, station):
        self.insertResult(searchByTownAndStation(self.collection_live, town.value, station.value))


    def updateResult_polygon(self):
        self.insertResult(searchByPolygon(self.collection_live, self.polygon))


    def updateResult_stats(self, compare, ratio, begin_hour, begin_minuts, end_hour, end_minuts, week, begin_week, end_week):
        compare_map = {
            ">": "$gt",
            ">=": "$gte",
            "==": "$eq",
            "<=": "$lte",
            "<": "$lt"
        }
        try:
            args = (compare_map[compare.value], ratio.get(),
                    begin_hour.value, begin_minuts.value,
                    end_hour.value, end_minuts.value,
                    week.index(begin_week.value), week.index(end_week.value))
            self.insertResult(searchByStats(self.collection_live, self.collection_history, *args))
        except:
            pass # possible ratio non float value


    def insertResult(self, list):
        self.updatePanel.hide()
        self.resultContainer.clear()
        self.resultList = []

        for i, item in enumerate(list):
            self.resultContainer.append(f"{item['ville']} ; {item['nom']}")
            self.resultList.append(item)
            self.flipDisplayState(i, item["actif"])


    def flipDisplayState(self, index, state):
        self.resultContainer.children[0].tk.itemconfig(index, { "bg":("white" if state else "lightgrey") })


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
        self.updateMaps()

        self.updatePanel.hide()
