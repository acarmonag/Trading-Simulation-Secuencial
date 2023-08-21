import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc
import time
import random
from datetime import timedelta
import numpy as np

class Chart:

    def __init__(self):
        self.data = []

    def graficar_velas_chinas(self):
        plt.ion()
        fig, ax = plt.subplots()
        index = 0  # Índice para rastrear la posición actual en los datos
        
        while index < len(self.data):  # Condición de salida cuando no hay más datos
            # Tomar un segmento de datos hasta el índice actual
            segmento_data = self.data[:index+1]
            
            if len(self.data) >= 20:  # Si hay 20 datos
                del self.data[0] 
                
            ax.clear()
            
            fechas_num = [mdates.date2num(item['Fecha']) for item in segmento_data]
            quotes = [(fechas_num[i], float(item['Apertura']), float(item['Alto']), float(item['Bajo']), float(item['Cierre'])) for i, item in enumerate(segmento_data)]
            
            # Calcular los SMA de 5 y 13 períodos
            cierres = [float(item['Cierre']) for item in segmento_data]
            sma5 = np.convolve(cierres, np.ones(5)/5, mode='valid')
            sma13 = np.convolve(cierres, np.ones(13)/13, mode='valid')
            
            ax.xaxis_date()
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            plt.xticks(rotation=45)
            
            candlestick_ohlc(ax, quotes, width=0.02, colorup='g', colordown='r')
            
            # Graficar los SMA
            if index >= 4:  # Solo graficar el SMA de 5 períodos si hay al menos 5 datos
                ax.plot(fechas_num[4:index+1], sma5, label='SMA 5', color='blue')
            if index >= 12:  # Solo graficar el SMA de 13 períodos si hay al menos 13 datos
                ax.plot(fechas_num[12:index+1], sma13, label='SMA 13', color='orange')
            
            ax.legend()  # Mostrar la leyenda
            
            try:
                plt.pause(1)  # Pausa para una actualización
            except KeyboardInterrupt:
                plt.close(fig)
                break  # Pausa para una actualización más lenta (puedes ajustar este valor)
            
            index += 1
