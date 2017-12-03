import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sp

from ztrans import *
#from scipy.io.wavfile import read # libreria para lectura de archivos de audio

# Diseño de filtro FIR
def diseño_filtro(bt,f1,f2,ganancia,fs,tipo_filtro,ventana):
    print('BT: '+str(bt)+' f1: '+str(f1)+' f2: '+str(f2))
    print('Ganancia: '+str(ganancia)+' fs: '+str(fs))
    print('Filtro: '+str(tipo_filtro)+' Ventana: '+str(ventana))
    fs = float(fs)
    bt = float(bt)
    wc1 = 2*np.pi*float(f1)/fs # frecuencia de corte 1 normalizada en radianes
    wc2 = 2*np.pi*float(f2)/fs
    bwn=2*np.pi*bt/fs # ancho de banda  normalizado en radianes
    M=int(4/bwn) # orden estimado del filtro
    N = 512 #Orden estimado del filtro
    n = np.arange(-M,M)
    
    if tipo_filtro == 'PB':
        h1 = +wc1/np.pi * np.sinc(wc1*(n)/np.pi)
    elif tipo_filtro == 'PBN':
        h1=(wc2/np.pi)*np.sinc((wc2*n)/np.pi)-(wc1/np.pi)*np.sinc(wc1*n/np.pi)
        h1[n==0]=2*(wc2-wc1)/np.pi # cuando es pasabanda
    elif tipo_filtro == 'PA':
        h1 = -wc1/np.pi * np.sinc(wc1*(n)/np.pi)
        h1[n==0]=1-(wc1)/np.pi
    
    #Respuesta en frecuencia del filtro.
    w1,Hh1 = signal.freqz(h1,1,whole=True, worN=N)
    #Ventana
    if ventana == 'REC':
        win = signal.boxcar(len(n))
    elif ventana == 'BLK':
        win = signal.blackman(len(n))
    elif ventana == 'HAM':
        win= signal.hamming(len(n))
    elif ventana == 'HAN':
        win = signal.hann(len(n))
        
    h2=h1*win # Multiplico la respuesta ideal por la ventana
    A=np.sqrt(10**(0.1*float(ganancia)))
    h2=h2*A # Ganancia del filtro
    
    w2,Hh2 = signal.freqz(h2,1,whole=True, worN=N) # Respuesta en frecuencia del filtro enventanado
    #(w2-np.pi)*fs/(2*np.pi),np.abs(np.fft.fftshift(Hh2)) Vectores a retornar para graficar
    
    
    return (w2-np.pi)*fs/(2*np.pi),np.abs(np.fft.fftshift(Hh2)),np.angle(np.fft.fftshift(Hh2)),h2


#Diseño de filtro IIR
def diseño_filtro_iir(f1,f2,fs,tf,rs):
    f1 = float(f1)
    f2 = float(f2)
    fs = float(fs)
    rs = float(rs)
    wc1=f1/(fs/2.0)
    wc2=f2/(fs/2.0)
    #print(wc2)
    if tf == 'PBN':
        N,D=sp.cheby2(12,rs,[wc1,wc2],'bandpass')       
        w2,Hh2=sp.freqz(N,D,whole='true',worN=1024)
        
    else:
        if tf == 'PB':
            N,D=sp.cheby2(12,rs,wc1,'lowpass')       
            w2,Hh2=sp.freqz(N,D,whole='true',worN=1024)
            
        else:
            N,D=sp.cheby2(12,rs,wc1,'highpass')       
            w2,Hh2=sp.freqz(N,D,whole='true',worN=1024)
    #print(type(N))
    #print(type(D))
    return (w2-np.pi)*fs/(2*np.pi),np.abs(np.fft.fftshift(Hh2)),np.angle(np.fft.fftshift(Hh2)),N,D
            
            
            

    
    

x = diseño_filtro_iir(400,600,1300,'PA',10)