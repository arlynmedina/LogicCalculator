# Función que regresa un diccionario con los valores de verdad de las primitivas

def valoresPrimitivos(proposition):

    #  Si existe un error, se recibe una string, en caso contrario, se recibe una lista que puede ser evaluada

    if type(proposition) != str:

        # Contar el numero de proposiciones primitivas

        primitives = ['p', 'q', 'r']
        nOfPrimitives = 0

        for primitive in primitives:
            if primitive in proposition:
                nOfPrimitives += 1

        # Asignar los valores de verdad de acuerdo a la cantidad de primitivas

        if nOfPrimitives == 0:
            o0 = {}
            for char in proposition:
                if char in ['t', 'c']:
                    o0[char] = ['']
            return o0

        elif nOfPrimitives == 1:
            o1 = {
                proposition[0]: ['V', 'F']
            }
            return o1

        elif nOfPrimitives == 2:
            o2 = {
                proposition[0]: ['V', 'V', 'F', 'F'],
                proposition[1]: ['V', 'F', 'V', 'F']
            }
            return o2

        else:
            o3 = {
                proposition[0]: ['V', 'V', 'V', 'V', 'F', 'F', 'F', 'F'],
                proposition[1]: ['V', 'V', 'F', 'F', 'V', 'V', 'F', 'F'],
                proposition[2]: ['V', 'F', 'V', 'F', 'V', 'F', 'V', 'F']
            }
            return o3

    else:
        return proposition
