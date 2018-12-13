import math
import numpy as np
from numpy import inf

def concatArr(arr):
    cad = ""
    for i in arr:
        cad += i
    return cad


def bubbleSort(arr, key):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j][key] > arr[j+1][key] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def getK(Cc):
    if Cc > 10:
        result = 10
        while Cc > 10:
            Cc /= 10
            result *= 10
        return result/10
    else:
        return 1


def infToZeros(arreglo):
    dimension = arreglo.shape
    for i in range(0, dimension[0]):
        for j in range(0, dimension[1]):
            if(arreglo[i,j] == inf):
                arreglo[i,j] = 0
    return arreglo


def f_calculo(Re, rf_D, fhijo=0.001, error=0.001):
    ban = False
    if(Re<=2200):
        f = 64/Re
    else:
        Xi = 1/math.sqrt(fhijo)
        ban = True
        while(ban):
            fx = -2*np.log10((rf_D/3.7)+((2.51*Xi)/Re))
            dividendo = 2.51/Re
            divisor = ((rf_D/3.7)) + (( 2.51*Xi ) / Re )
            Fx = ( -2/np.log(10) ) * (dividendo/divisor)
            Xi_1 = Xi - (fx-Xi)/(Fx-1)
            compare = abs(Xi_1-Xi)
            if(compare<=error):
                f = 1/pow(Xi,2)
                ban = False
            else:
                Xi = Xi_1
    return f


def validateError(Error):
    flag = False
    dimension = Error.shape
    for i in range(0, dimension[0]):
        for j in range(0, dimension[1]):
            if(Error[i,j] > 0.001):
                flag = True
    return flag


def TableFormatter(ntuberias,tuberias, Qx, Lx, Dx, A,V,Re, f,hf,Km,hm,hfhm,a, af):
        V = np.round(V, 4)
        A = np.round(A, 4)
        Qx = np.round(Qx, 4)
        hf = np.round(hf, 4)
        Km = np.round(Km, 4)
        hm = np.round(hm, 4)
        hfhm = np.round(hfhm, 4)
        a = np.round(a, 4)
        af = np.round(af, 4)
        f = np.round(f,4)
        tabla = []
        for i in range(0,ntuberias):
            tabla.append({
                'tuberia': "{}-{}".format(tuberias[i]['start'],tuberias[i]['end']),
                'Qx':Qx[i], 
                'Lx': Lx[i], 
                'Dx': Dx[i],
                'A': A[i], 
                'V': V[i],
                'Re': Re[i],  
                'f': f[i], 
                'hf': hf[i], 
                'Km': Km[i], 
                'hm': hm[i], 
                'hfhm': hfhm[i], 
                'a': a[i],   
                'af': af[i]
            })
        return tabla

def handleArrMutacionToMatrizBinarios(arr, ndiametros):
    matriz = []

    if ndiametros == 4:
        const = 2
    else:
        const = 3  

    for a in arr:
        c = ""
        row = []
        for i in range(len(a)):
            c += a[i] 
            if len(c) == const:
                row.append(c)
                c = ""
        matriz.append(row)

    return np.matrix(matriz)    