# Funcion que realiza todas las operaciones necesarias en la proposicion

from switchcase import switch


def classifier(divided_proposition, primitive_table):
    # Manejo de errores

    if type(divided_proposition) == str:
        return divided_proposition

    operators = ['~', '∧', '∨', '→', '⟷']
    truth_table = primitive_table

    if 't' in divided_proposition:
        truth_table['t'] = tautology(truth_table)
    if 'c' in divided_proposition:
        truth_table['c'] = contradiction(truth_table)

    # Evaluar cada parte de la proposicion
    for proposition in divided_proposition:

        propositionKeys = list(truth_table.keys())
        operator = ''
        p = ''
        q = ''
        tempEnd = 0
        if len(proposition) != 1:
            pastPropositionIndex = len(propositionKeys) - 1

            # Buscar si alguna de las proposiciones creadas existe en la proposicino que se evalua
            # Buscando primero en las proposiciones mas complejas

            while pastPropositionIndex >= 0:
                if propositionKeys[pastPropositionIndex] in proposition:

                    # start, end: puntos de referencia de incio y final de la proposicion encontrada
                    # dentro de la proposicion que se evalua

                    start = proposition.find(propositionKeys[pastPropositionIndex])
                    end = proposition[::-1].find(propositionKeys[pastPropositionIndex][::-1]) * (-1) - 1

                    negationFlag = False

                    if end < -2:
                        if not p:
                            p = propositionKeys[pastPropositionIndex]
                            p = truth_table[p]
                            k = end
                            while k < len(proposition):
                                if proposition[k] in operators:
                                    operator = proposition[k]
                                    break
                                k += 1
                            tempEnd = end
                    if -start <= -1:
                        if not q:
                            if tempEnd != end:
                                q = propositionKeys[pastPropositionIndex]
                                if len(q) == len(proposition) - 1:
                                    negationFlag = True
                                q = truth_table[q]
                                k = start
                                while k >= 0:
                                    if proposition[k] in operators:
                                        operator = proposition[k]
                                        break
                                    k -= 1

                    if negationFlag:
                        break
                    if p and q:
                        break
                pastPropositionIndex -= 1

            for case in switch(operator):
                if case('∧'):
                    truth_table[proposition] = and_function(p, q)
                if case('∨'):
                    truth_table[proposition] = or_function(p, q)
                if case('→'):
                    truth_table[proposition] = if_function(p, q)
                if case('⟷'):
                    truth_table[proposition] = bi_function(p, q)
                if case('~'):
                    truth_table[proposition] = not_function(q)

    return truth_table


def and_function(a, b):
    truth_table_and = []
    for index in range(len(a)):
        if a[index] == 'V' and b[index] == 'V':
            truth_table_and.append('V')
        else:
            truth_table_and.append('F')
    return truth_table_and


def or_function(a, b):
    truth_table_or = []
    for index in range(len(a)):
        if a[index] == 'F' and b[index] == 'F':
            truth_table_or.append('F')
        else:
            truth_table_or.append('V')
    return truth_table_or


def not_function(a):
    truth_table_not = []
    for value in a:
        if value == 'V':
            truth_table_not.append('F')
        else:
            truth_table_not.append('V')
    return truth_table_not


def if_function(a, b):
    truth_table_if = []
    for index in range(len(a)):
        if a[index] == 'V' and b[index] == 'F':
            truth_table_if.append('F')
        else:
            truth_table_if.append('V')
    return truth_table_if


def bi_function(a, b):
    p = if_function(a, b)
    q = if_function(b, a)
    truth_table_bi = and_function(p, q)
    return truth_table_bi


def tautology(truth_table):
    truth_table_tautology = []
    for i in range(len(truth_table[list(truth_table.keys())[0]])):
        truth_table_tautology.append('V')
    return truth_table_tautology


def contradiction(truth_table):
    truth_table_contradiction = []
    for i in range(len(truth_table[list(truth_table.keys())[0]])):
        truth_table_contradiction.append('F')
    return truth_table_contradiction
