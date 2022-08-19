# Calculadora de tablas de verdad
# Creado por: Luis, Arlyn, Caro

import tkinter as tk
from tkinter import ttk
from PrimitiveValues import valoresPrimitivos
from DivideProposition import divideProposition
from Operators import classifier


# Diseño de GUI

# Ventana de Error

def popError(parentwindow, text):
    errorWindow = tk.Toplevel(parentwindow)
    errorWindow.focus()
    errorWindow.grab_set()
    errorWindow.title('Error')
    errorWindow.geometry('240x125')

    errorText = tk.Label(errorWindow, text=text, font='Helvetica 10', justify=tk.CENTER)
    accept = tk.Button(errorWindow, text='Aceptar', width=10, height=1, command=lambda: errorWindow.destroy())
    errorText.place(x=20, y=20)
    accept.place(x=90, y=75)


# Ventanas de Resultados:

# - Tablas de verdad

def tableResult(parentwindow, proposition):
    if proposition:
        truthTable = classifier(divideProposition(proposition), valoresPrimitivos(divideProposition(proposition)))
        if type(truthTable) == str:
            popError(parentwindow, truthTable)
        else:
            resultsWindow = tk.Toplevel(parentwindow)
            resultsWindow.focus()
            resultsWindow.grab_set()
            resultsWindow.title('Resultado')
            resultsWindow.geometry('900x300')
            parentwindow.withdraw()

            textDisplay = tk.StringVar()
            textDisplay.set(proposition)

            columns = tuple(truthTable.keys())
            table = ttk.Treeview(resultsWindow, columns=columns)
            table.heading('#0', text='')
            table.column('#0', width=0, stretch=tk.NO)
            for i in range(len(columns)):
                table.heading(columns[i], text=columns[i])
                table.column(columns[i], width=880 // len(truthTable), stretch=tk.NO, anchor=tk.CENTER)

            for i in range(len(truthTable[columns[0]])):
                values = []
                for key in list(truthTable.keys()):
                    values.append(truthTable[key][i])
                table.insert(parent='', index=i, value=values)

            propositionDisplay = tk.Entry(resultsWindow, textvariable=textDisplay, state=tk.DISABLED,
                                          disabledbackground='white', font='Helvetica 15', justify=tk.CENTER)
            propositionDisplay.place(x=10, y=10)
            table.place(x=10, y=60)

            lastProposition = truthTable[list(truthTable.keys())[-1]]
            valuesAreEqual = True

            for i in range(len(lastProposition)):
                if i < len(lastProposition) - 1:
                    if lastProposition[i] != lastProposition[i + 1]:
                        valuesAreEqual = False

            if valuesAreEqual:
                text = tk.StringVar()
                if lastProposition[0] == 'V':
                    text.set('Tautología')
                else:
                    text.set('Contradicción')
                tcDisplay = tk.Entry(resultsWindow, textvariable=text, state='readonly', readonlybackground='#4D5AF7',
                                     width=30, justify=tk.CENTER, font='Helvetica 12')
                tcDisplay.place(x=500, y=10, height=30)

            resultsWindow.wait_window()
            parentwindow.deiconify()


# - Equivalencias Logicas

def equivalenceResult(parentwindow, proposition1, proposition2):
    truthTable1 = classifier(divideProposition(proposition1), valoresPrimitivos(divideProposition(proposition1)))
    truthTable2 = classifier(divideProposition(proposition2), valoresPrimitivos(divideProposition(proposition2)))

    if type(truthTable1) == str or type(truthTable2) == str:
        if type(truthTable1) == str:
            popError(parentwindow, f'Proposición 1: {truthTable1}')
        else:
            popError(parentwindow, f'Proposición 2: {truthTable2}')
    else:
        resultsWindow = tk.Toplevel(parentwindow)
        resultsWindow.focus()
        resultsWindow.grab_set()
        resultsWindow.title('Resultado')
        resultsWindow.geometry('900x300')
        parentwindow.withdraw()

        textDisplay1 = tk.StringVar()
        textDisplay1.set(proposition1)
        textDisplay2 = tk.StringVar()
        textDisplay2.set(proposition2)
        textEquivalence = tk.StringVar()
        textResult = tk.StringVar()

        dividedProposition1 = divideProposition(proposition1)
        dividedProposition2 = divideProposition(proposition2)
        completeProposition = dividedProposition1
        for proposition in dividedProposition2:
            if proposition not in completeProposition:
                completeProposition.append(proposition)
        completeProposition = sorted(completeProposition, key=len)

        truthTable = classifier(completeProposition, valoresPrimitivos(completeProposition))

        columns = tuple(truthTable.keys())
        table = ttk.Treeview(resultsWindow, columns=columns)
        table.heading('#0', text='')
        table.column('#0', width=0, stretch=tk.NO)
        for i in range(len(columns)):
            table.heading(columns[i], text=columns[i])
            table.column(columns[i], width=880 // len(truthTable), stretch=tk.NO, anchor=tk.CENTER)

        if truthTable[proposition1] == truthTable[proposition2]:
            textEquivalence.set('≡')
            textResult.set('Son lógicamente equivalentes')
        else:
            textEquivalence.set('≢')
            textResult.set('No son lógicamente equivalentes')

        for i in range(len(truthTable[columns[0]])):
            values = []
            for key in list(truthTable.keys()):
                values.append(truthTable[key][i])
            table.insert(parent='', index=i, value=values)

        propositionDisplay1 = tk.Entry(resultsWindow, textvariable=textDisplay1, state=tk.DISABLED,
                                       disabledbackground='white', font='Helvetica 15', justify=tk.CENTER)
        propositionDisplay2 = tk.Entry(resultsWindow, textvariable=textDisplay2, state=tk.DISABLED,
                                       disabledbackground='white', font='Helvetica 15', justify=tk.CENTER)
        equivalenceSign = tk.Label(resultsWindow, textvariable=textEquivalence, font='Helvetica 20',
                                   justify=tk.CENTER)
        textResultLabel = tk.Label(resultsWindow, textvariable=textResult, font='Helvetica 12')

        propositionDisplay1.place(x=10, y=10)
        propositionDisplay2.place(x=300, y=10)
        equivalenceSign.place(x=257, y=3)
        textResultLabel.place(x=550, y=10)
        table.place(x=10, y=60)

        resultsWindow.wait_window()
        parentwindow.deiconify()


# Ventana de la calculadora
#   mode:
#       0: Tablas de verdad
#       1: Equivalencias logicas

focusedDisplay = ''  # Ugh, variable global (indica el display seleccionado)


def calcWindow(parentwindow, mode):
    global focusedDisplay
    mainWindow = tk.Toplevel(parentwindow)
    mainWindow.focus()
    mainWindow.grab_set()
    mainWindow.geometry('500x250')
    parentwindow.withdraw()

    if mode == 0:

        # Modo tablas de verdad

        mainWindow.title('Crear Tablas de Verdad')

        text = tk.StringVar()
        focusedDisplay = text
        display = tk.Entry(mainWindow, state='readonly', readonlybackground='white', font='Helvetica 18',
                           textvariable=text)
        calculate = tk.Button(mainWindow, text='=', width=10, height=2,
                              command=lambda: tableResult(mainWindow, text.get()))
        display.place(x=10, y=10, width=475, height=60)
    else:

        # Modo equivalencias logicas

        mainWindow.title('Calcular equivalencias')

        text1 = tk.StringVar()
        text2 = tk.StringVar()
        focusedDisplay = text1  # Display seleccionado por default es el 1

        display1 = tk.Entry(mainWindow, state='readonly', readonlybackground='white', font='Helvetica 18',
                            textvariable=text1)
        display1.configure(readonlybackground='#83F684')
        display2 = tk.Entry(mainWindow, state='readonly', readonlybackground='white', font='Helvetica 18',
                            textvariable=text2)

        def switchDisplay():  # Cambiar el display seleccionado
            global focusedDisplay
            if focusedDisplay == text1:
                focusedDisplay = text2
                display2.configure(readonlybackground='#83F684')  # Color del display seleccionado
                display1.configure(readonlybackground='white')  # Color del display no seleccionado
            else:
                focusedDisplay = text1
                display1.configure(readonlybackground='#83F684')
                display2.configure(readonlybackground='white')

        switch = tk.Button(mainWindow, text='⮀', width=2, height=1, command=lambda: switchDisplay())
        identical = tk.Label(mainWindow, font='Helvetica 18', text='≡')
        calculate = tk.Button(mainWindow, text='=', width=10, height=2,
                              command=lambda: equivalenceResult(mainWindow, text1.get(), text2.get()))

        display1.place(x=10, y=15, width=200, height=60)
        display2.place(x=270, y=15, width=200, height=60)
        identical.place(x=230, y=35)
        switch.place(x=230, y=5)

    p = tk.Button(mainWindow, text='p', width=10, height=2, command=lambda: showInDisplay('p', focusedDisplay))
    q = tk.Button(mainWindow, text='q', width=10, height=2, command=lambda: showInDisplay('q', focusedDisplay))
    r = tk.Button(mainWindow, text='r', width=10, height=2, command=lambda: showInDisplay('r', focusedDisplay))
    t = tk.Button(mainWindow, text='t', width=10, height=2, command=lambda: showInDisplay('t', focusedDisplay))
    c = tk.Button(mainWindow, text='c', width=10, height=2, command=lambda: showInDisplay('c', focusedDisplay))
    negation = tk.Button(mainWindow, text='~', width=10, height=2, command=lambda: showInDisplay('~', focusedDisplay))
    conjunction = tk.Button(mainWindow, text='∧', width=10, height=2,
                            command=lambda: showInDisplay('∧', focusedDisplay))
    disjunction = tk.Button(mainWindow, text='∨', width=10, height=2,
                            command=lambda: showInDisplay('∨', focusedDisplay))
    implication = tk.Button(mainWindow, text='→', width=10, height=2,
                            command=lambda: showInDisplay('→', focusedDisplay))
    bi = tk.Button(mainWindow, text='⟷', width=10, height=2, command=lambda: showInDisplay('⟷', focusedDisplay))
    openP = tk.Button(mainWindow, text='(', width=10, height=2, command=lambda: showInDisplay('(', focusedDisplay))
    closeP = tk.Button(mainWindow, text=')', width=10, height=2, command=lambda: showInDisplay(')', focusedDisplay))

    delete = tk.Button(mainWindow, text='Delete', width=10, height=2, command=lambda: showInDisplay(0, focusedDisplay))
    clear = tk.Button(mainWindow, text='Clear', width=10, height=2, command=lambda: showInDisplay(1, focusedDisplay))

    p.place(x=10, y=90)
    q.place(x=105, y=90)
    r.place(x=200, y=90)
    t.place(x=295, y=90)
    c.place(x=390, y=90)
    negation.place(x=10, y=140)
    conjunction.place(x=105, y=140)
    disjunction.place(x=200, y=140)
    implication.place(x=295, y=140)
    bi.place(x=390, y=140)
    openP.place(x=10, y=190)
    closeP.place(x=105, y=190)
    delete.place(x=200, y=190)
    clear.place(x=295, y=190)
    calculate.place(x=390, y=190)

    mainWindow.wait_window()
    parentwindow.deiconify()


# Modificar la proposicion en display

def showInDisplay(char, text):
    if char == 0:  # Borrar el ultimo caracter
        text.set(text.get()[0:-1])
    elif char == 1:  # Limpiar el display
        text.set('')
    else:
        text.set(f'{text.get()}{char}')


# Ventana Acerca de

def aboutWindow(parentwindow):
    mainWindow = tk.Toplevel(parentwindow)
    mainWindow.focus()
    mainWindow.grab_set()
    mainWindow.geometry('500x250')
    parentwindow.withdraw()
    mainWindow.title('Información del programa')

    label1 = tk.Label(mainWindow, text="Creadores del programa: ", font='Helvetica 18')
    label1.place(x=0, y=0)
    label2 = tk.Label(mainWindow, text="1. Luis Raúl Acosta Mendoza")
    label2.place(x=0, y=30)
    label3 = tk.Label(mainWindow, text="2. Ana Carolina Arellano Valdez")
    label3.place(x=0, y=55)
    label4 = tk.Label(mainWindow, text="3. Arlyn Linette Medina García")
    label4.place(x=0, y=80)
    label5 = tk.Label(mainWindow, text="Link de GitHub", font='Helvetica 18')
    label5.place(x=0, y=110)

    mainWindow.wait_window()
    parentwindow.deiconify()


# Ventana principal

root = tk.Tk()
root.title('Logic Calculator')
root.geometry('335x325')
title = tk.Label(root, text='Calculadora Lógica', width=30, height=3)
truthTableButton = tk.Button(root, text='Crear tablas de verdad', width=30, height=3,
                             command=lambda: calcWindow(root, 0))
equivalence = tk.Button(root, text='Calcular equivalencias lógicas', width=30, height=3,
                        command=lambda: calcWindow(root, 1))
about = tk.Button(root, text='Acerca de', width=30, height=2, command=lambda: aboutWindow(root))

title.place(x=55, y=30)
truthTableButton.place(x=55, y=100)
equivalence.place(x=55, y=170)
about.place(x=55, y=240)
root.mainloop()
