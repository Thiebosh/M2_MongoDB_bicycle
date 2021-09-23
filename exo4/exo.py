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


def exo4(*_):
    app = App(title="Business program")

    menu_box = Box(app, align="top", border=True)

    menu_btn = []
    frames = []

    for i in range(5):
        name = f"Step{i+1}"

        frames.append(Box(app, width="fill", height="fill", border=True))
        frames[-1].hide()

        menu_btn.append(PushButton(menu_box, command=showFrame, args=(frames, i), text=name, align="left"))

        globals()[f"step{i+1}"](frames[-1])

    app.display()
