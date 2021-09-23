from guizero import Box, TextBox, ListBox, Text, PushButton


def searchByTownAndStation(collection, town, station, displayBox):
    displayBox.clear()

    print(town.value)
    print(station.value)
    filter = {
        
    }

    for item in collection.find(filter).limit(2):
        displayBox.append(item)


def step1(collection, _, frame):
    # left screen part
    resultBox = Box(frame, height="fill", width=int(frame.width/3), align="left", border=True)
    
    resultTitle = Box(resultBox, width="fill", border=True)
    Text(resultTitle, text="Résultats de recherche")

    resultList = ListBox(resultBox, height="fill", width=resultBox.width, scrollbar=True)


    # right screen part
    mainSection = Box(frame, height="fill", width=int(frame.width*2/3), border=True)
    Text(mainSection, text="Recherche de station")

    Box(mainSection, height="40")  # margin

    inputs = Box(mainSection, layout="grid")
    Text(inputs, grid=[0,0], text="Ville cible")
    Text(inputs, grid=[1,0])  # margin
    townName = TextBox(inputs, grid=[2,0], width="25")
    Text(inputs, grid=[0,1], text="Nom de station")
    Text(inputs, grid=[1,1])  # margin
    stationName = TextBox(inputs, grid=[2,1], width="25")

    Box(mainSection, height="40")  # margin

    PushButton(mainSection, text="submit",
                command=searchByTownAndStation,
                args=(collection, townName, stationName, resultList))
