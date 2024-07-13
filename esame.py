class ExamException(Exception):
    pass

class CSVTimeSeriesFile():
    def __init__(self, name):
        
        self.name = name
        
    def get_data(self):
        
        self.can_read = True
        try:
            my_file = open(self.name, 'r')
            my_file.readline()  #gestire questa parte - così viene saltata la prima linea, in caso occuparsi dell'intestazione?
        except Exception:
            self.can_read = False
        
        if not self.can_read:
            my_file.close()
            raise ExamException ('Errore nell\'apertura o nella lettura del file')
        
        else:
            #creo una lista vuota che conterrà poi la lista di liste 
            data = []
            for line in my_file:
                columns = line.strip().split(',')
                try: 
                   epoch = int(columns[0])
                   temperature = float(columns[1]) #si ferma a due elementi!!!!
                   data.append([epoch,temperature])
                except Exception:
                    pass   
            #controllo che non ci sia un timestamp fuori ordine o duplicato in caso alzo un'eccezione
            for i in range(len(data)-1):
                   if data[i][0] >= data[i+1][0]:
                       raise ExamException('Timestamp fuori ordine o duplicato: {} dopo {}'.format(data[i+1][0],data[i][0]))
            return data

def compute_daily_max_difference(time_series):
    daily_max_difference_list = [] #creo la lista che conterrà le massime differenze di temperatura giornaliere
    i = 0
    while i < len(time_series):
        epoch = time_series[i][0]
        day_start_epoch = epoch - (epoch % 86400)
        day_end_epoch = day_start_epoch + 86400

        min_temperature = time_series[i][1]
        max_temperature = time_series[i][1]
        count_temperatures = 0

        # Iterate to find all temperatures within the same day
        while i < len(time_series) and time_series[i][0] < day_end_epoch:
            temperature = time_series[i][1]
            if temperature < min_temperature:
                min_temperature = temperature
            if temperature > max_temperature:
                max_temperature = temperature
            i += 1
            count_temperatures +=1

        if count_temperatures == 1:
            daily_max_difference_list.append(None)
        else:
            daily_max_difference_list.append(max_temperature - min_temperature)

    return daily_max_difference_list
    
    

    
                    
time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
lista_differenze = compute_daily_max_difference(time_series)
print(lista_differenze)
