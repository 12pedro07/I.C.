import matplotlib.pyplot as plt
import plotly.plotly as py
import csv
from collections import OrderedDict
from tqdm import tqdm

##############################################
###                                        ###
###   EXEMPLO DE CLASSE EM "data_storage": ###
###                                        ###
###       - ssd__                          ###
###       - SIFT_10_25pct                  ###
###       - RootSIFT_50_5pct               ###
###                                        ###
##############################################

class data_storage():
    def __init__ (self, method, param='', pct=''):
        self.method = method
        self.param = param
        self.pct = pct
        self.objects = OrderedDict()
        self.objects ['medicine']       = 0
        self.objects ['chocolate_milk'] = 0
        self.objects ['heineken']       = 0
        self.objects ['yellow_juice']   = 0
        self.objects ['red_juice']      = 0
        self.objects ['purple_juice']   = 0
        self.objects ['milk_bottle']    = 0
        self.objects ['milk_box']       = 0
        self.objects ['cereal']         = 0
        self.objects ['iron_man']       = 0
        self.objects ['shampoo']        = 0
        self.objects ['monster']        = 0
        self.objects ['tea_box']        = 0
    def add_detection(self,obj_name):
        if obj_name in self.objects : self.objects[obj_name] += 1

ans_dict = {} # { 'nome_da_imagem' : [lista_das_respostas_corretas] }
class_dict = {} # { 'nome_da_clase' : classe }

obj_namelist = list(data_storage('').objects) # lista com o nome dos objetos na mesma ordem do csv

def plot():
    multiple_bars = plt.figure()

    x = obj_namelist

    bar0 = gabarito.objects.values()
    bar1 = class_dict['SIFT_10_5pct'].objects.values()
    bar2 = class_dict['SIFT_10_10pct'].objects.values()
    bar3 = class_dict['SIFT_10_25pct'].objects.values()
    bar4 = class_dict['SIFT_10_50pct'].objects.values()
    bar5 = class_dict['SIFT_10_75pct'].objects.values()
    bar6 = class_dict['SIFT_10_100pct'].objects.values()

    ax = plt.subplot(1,1,1)
    ax.bar(x,   bar0,      width=0.8,  color='gray',   align='center', label="GABARITO")
    ax.bar(x,   bar1,      width=0.6,  color='r',      align='center', label="SIFT_10_5pct")
    ax.bar(x,   bar2,      width=0.5,  color='g',      align='center', label="SIFT_10_10pct")
    ax.bar(x,   bar3,      width=0.4,  color='b',      align='center', label="SIFT_10_25pct")
    ax.bar(x,   bar4,      width=0.3,  color='y',      align='center', label="SIFT_10_50pct")
    ax.bar(x,   bar5,      width=0.2,  color='black',  align='center', label="SIFT_10_75pct")
    ax.bar(x,   bar6,      width=0.1,  color='brown',  align='center', label="SIFT_10_100pct")

    plt.grid(True, axis='y')
    plt.ylabel('Detecções corretas')
    plt.legend()
    plt.show()

    plot_url = py.plot_mpl(multiple_bars, filename='detected_itens')

def atualize():
    if name in ans_dict: # como a geracao do csv nao foi perfeita, nem todas as possibilidades sao analizadas, por isso existe este check
        [v_name_c.add_detection(obj_namelist[i]) for i in range(len(ans_dict[name])) if (ans_dict[name][i] == guess[i]) and (ans_dict[name][i]=='1')]

with open('gabarito_objetos.csv') as csvfile: # gerar um dicionario com as respostas corretas para comparacao
    gabarito_CSV = csv.reader(csvfile, delimiter=',')
    gabarito = data_storage('GABARITO')
    for row in gabarito_CSV:
        if row[0] != 'imagem':
            name = row[0].replace("+AF8-","_").lower()
            answers = [row[x+1] for x in range(len(row)-1)]
            ans_dict[name] = answers # dicionario com os nomes dos objetos e uma lista com as respostas corretas (fora de ordem mas gerado corretamente)
            aux = 0
            for element in row[1:(len(row))]:
                if element == '1' : gabarito.add_detection(obj_namelist[aux])
                aux = aux+1

[print(x, ans_dict[x]) for x in ans_dict]

with open('logfile.csv') as csvfile: # analizando os metodos
    logfile_CSV = csv.reader(csvfile, delimiter=',')
    before = []
    atual = []
    for row in tqdm(logfile_CSV):
        if row[0] != 'detector':
            atual = []
            method = row[0]
            param = row[1]
            tmp = row[2].split('/')
            pct = tmp[2] if (len(tmp) > 1) else row[2]
            name = row[4][12:17].replace(".","") # nome da imagem analizada
            guess = [row[x] for x in range(5,18)] # lista com as respostas que o algoritmo deu
            ###### criando um dicionario com as classes referentes a cada pasta, metodo e algoritmo ######
            atual.append(method)
            atual.append(param)
            atual.append(pct)
            if atual != before:
                ###### Criando as classes ######
                v_name_s = method+'_'+param+'_'+pct # nome da classe em string
                exec("%s = %d" % (v_name_s,0))
                v_name_c = v_name_s # classe de fato
                v_name_c = data_storage(method,param=param,pct=pct)
                class_dict[v_name_s] = v_name_c

            atualize()

            before = atual.copy()
            #############

[print(class_dict[x].objects.values, x) for x in class_dict]
# print(class_dict['SIFT_10_50pct'].objects)


plot()
