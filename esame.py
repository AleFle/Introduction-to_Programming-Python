class ExamException(Exception):
    pass

class CSVTimeSeriesFile():
    def __init__(self, name):
        self.name = name 
        
    def get_data(self):
        #controllo che il nome del file sia istanza di string (o di una sua sottoclasse)
        if not isinstance(self.name,str):
            raise ExamException ('Il nome del file deve essere una stringa.')
        
        #provo ad aprire il file e leggere la prima riga e se riesce chiudo il file di test, altrimenti sollevo un'eccezione.
        try:
            test_file = open(self.name, 'r')
            test_file.readline()
            test_file.close()
        except Exception as e:
           raise ExamException ('Errore in apertura o lettura del file: {}'.format(e))
        
        file = open(self.name, 'r') #ora posso sicuramente aprire il file
        data = [] # preparo la lista che conterrà le liste [epoch, temperature], con epoch e temperature valori numerici
        
        for line in file:
            fields = [field.strip() for field in line.split(',')]#ciascuna lista fields (per ogni riga) sarà ['field_1', 'field_2', ..., 'field_n'] se ci sono "n" campi
            #tentativo di cast per i primi due elementi della lista fields - epoch, temperature
            try: 
                epoch = int(float(fields[0])) #cast del primo elemento (epoch) prima a float (perché potrebbe esserlo) poi, se riuscito, a int
                temperature = float(fields[1]) #cast del secondo elemento (temperature) a float
                data.append([epoch,temperature]) #se i cast sono avvenuti con successo, aggiungo alla lista "data" la lista [epoch, temperature]
            except Exception:
                pass   #qualsiasi eccezione (e.g. len(fields) < 2, cast non riusciti, etc.) viene gestita ignorando la riga
        file.close() #ora posso chiudere il file
        #controllo che non ci siano timestamp fuori ordine o duplicati
        for i in range(len(data)-1): #ciclo sulle liste confrontando sempre il primo elemento (i.e. epoch) di una lista con quello della successiva
                if data[i][0] >= data[i+1][0]:
                    raise ExamException("Timestamp fuori ordine o duplicato: {} all'indice {}, dopo {} all'indice {}".format(data[i+1][0],i+1,data[i][0],i))
        return data

def compute_daily_max_difference(time_series):
    daily_max_difference_list = [] #preparo una lista che conterrà le escursioni termiche (massima diff. di temperatura nella giornata)
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
            daily_max_difference_list.append(round(max_temperature - min_temperature,3)) # round to avoid

    return daily_max_difference_list


    

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
print(compute_daily_max_difference(time_series))

