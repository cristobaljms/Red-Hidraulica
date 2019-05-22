def seleccion(FO, Nc, B):

    Pmax = B/Nc
    Pmin = (2-B)/Nc

    arrProbabilidad = []

    for i in range(1, Nc+1):
        Pi = Pmin + ( Pmax - Pmin ) * ((Nc - i)/(Nc - 1))
        PiN = Pi * Nc
        if PiN >= 1.5:
            arrProbabilidad.append(FO[i])
            arrProbabilidad.append(FO[i])
        elif PiN >= 0.5:
            arrProbabilidad.append(FO[i])

    arrPadresCruzamiento = []

    for i in arrProbabilidad:
        arrPadresCruzamiento.append(i['binarios'])

    arrIndividuos=[i+1 for i in range(Nc)]

    flagA = True
    while(flagA):
        auxArr = copy.deepcopy(arrIndividuos)
        arrIndexPadres = []
        while(len(auxArr) > 1):
            a = random.choice(auxArr)
            b = random.choice(auxArr)
            if (a != b and (a + 1) != b and (a-1) != b):
                auxArr.remove(a)
                auxArr.remove(b)
                arrIndexPadres.append({'a':a, 'b':b})    
            if(len(auxArr) == 2 and ((auxArr[0] + 1) == auxArr[1] or (auxArr[1] + 1) == auxArr[0])):
                break
            elif( len(auxArr) == 1 ):
                flagA = False
                arrIndexPadres.append({'a':auxArr[0], 'b':-1})
            elif(len(auxArr) == 0):
                flagA = False
              
    return [arrIndexPadres, arrProbabilidad]