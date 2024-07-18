class ExamException(Exception):
    pass

class CSVTimeSeriesFile():
    def __init__(self, name):
        self.name = name 
        
    def get_data(self):
        #controllo che il nome del file sia una stringa
        if not isinstance(self.name, str):
            raise ExamException ('Il nome del file deve essere una stringa.')
        
        #provo ad aprire il file e leggere la prima riga
        try:
            test_file = open(self.name, 'r')
            test_file.readline()
            test_file.close()
        except Exception as e:
           raise ExamException ('Errore in apertura o lettura del file: {}'.format(e))
        
        file = open(self.name, 'r')
        data = [] # preparo la lista che conterrà le liste [epoch, temperature], con epoch e temperature valori numerici
        
        for line in file:
            fields = [field.strip() for field in line.split(',')]
            #tentativo di cast per i primi due elementi (epoch, temperature) della lista fields
            try: 
                epoch = int(float(fields[0])) #cast del primo elemento (epoch) prima a float (perché potrebbe esserlo) poi, se riuscito, a int
                temperature = float(fields[1]) #cast del secondo elemento (temperature) a float
                data.append([epoch,temperature]) #se i cast sono avvenuti con successo, aggiungo alla lista "data" la lista [epoch, temperature]
            except Exception:
                pass   #qualsiasi eccezione viene gestita ignorando la riga
        
        file.close() #ora posso chiudere il file
        
        #controllo che non ci siano timestamp fuori ordine o duplicati
        for i in range(len(data)-1): #ciclo sulle liste confrontando sempre il primo elemento (i.e. epoch) di una lista con quello della successiva
                if data[i][0] >= data[i+1][0]:
                    raise ExamException("Timestamp fuori ordine o duplicato: {} all'indice {}, dopo {} all'indice {}".format(data[i+1][0],i+1,data[i][0],i))
        
        return data


def group_temperatures_by_day(time_series):
    #preparo un dizionario che avrà come chiavi gli epoch che segnano l'inizio della giornata e come valori le liste di temperature giornaliere
    daily_temperatures_dict = {} 
    for lista in time_series: #(time_series è una lista di liste)
        epoch = lista[0]
        temperature = lista[1]
        day_start_epoch = epoch - (epoch % 86400) # a partire da un epoch trovo l'inizio di quella giornata 
        if day_start_epoch not in daily_temperatures_dict: #se non è già presente come chiave del mio dizionario 
            daily_temperature_list = [] #preparo un lista vuota che avrà le temperature di quella giornata
            daily_temperatures_dict[day_start_epoch] = daily_temperature_list #aggiungo la chiave al mio dizionario e ci associo la lista
        
        daily_temperature_list.append(temperature) #aggiungo le temperature alla lista
        #quando ci sarà un nuovo day_start_epoch (calcolato da epoch preso dalle liste nell'iterazione)-> nuova chiave, nuova lista, aggiungo elementi
        #così per tutta l'iterazione
    
    return daily_temperatures_dict


def compute_daily_max_difference(time_series):
    daily_max_difference = [] #preparo una lista che conterrà le escursioni termiche
    daily_temperatures_dict = group_temperatures_by_day(time_series) #creazione del dizionario
    list_days_start_epoch = list(daily_temperatures_dict) #la funzione list() sul dizionario mi crea una lista contenente le chiavi del dizionario
    for key in list_days_start_epoch:
        list_of_temperatures_per_day = daily_temperatures_dict[key] #salvo la lista per quella giornata
        
        #se la lista ha più di 1 elemento allora la differenza è definita
        if len(list_of_temperatures_per_day) > 1:
            min_temperature = min(list_of_temperatures_per_day) #min() restituisce il minimo della lista
            max_temperature = max(list_of_temperatures_per_day) #max() restituisce il massimo della lista
            daily_max_difference.append(round(max_temperature - min_temperature,3)) #faccio max - min, arrotondo alla terza cifra decimale e aggiungo alla lista
        else:
            #se la lista non ha almeno 2 elementi allora la differenza non è definita
            daily_max_difference.append(None) #aggiungo None alla lista
    
    return daily_max_difference