from guizero import App, Box, PushButton
# from bson.objectid import ObjectId

from exo4.exo4_1.exo import step1
from exo4.exo4_2.exo import step2
from exo4.exo4_3.exo import step3
from exo4.exo4_4.exo import step4
from exo4.exo4_5.exo import step5


def showFrame(frames, index):
    for frame in frames:
        frame.hide()
    frames[index].show()


def exo4(collection_live, collection_history, *_):
    try:
        app = App(title="Business program", height="600", width="800")
        app.tk.resizable(False, False)  # everything will be absolute

        menu_box = Box(app, align="top", layout="grid", border=True)

        frames = []
        for i in range(5):
            name = f"step{i+1}"

            frames.append(Box(app, width=app.width, height="fill", border=True))
            frames[-1].hide()

            PushButton(menu_box, grid=[i,0], text=name, command=showFrame, args=(frames, i))

            globals()[name](collection_live, collection_history, frames[-1])

        app.display()
    except Exception as e:
        print(e)
