# -*- coding: utf-8 -*-

import os.path
import time as tm
import pandas as pd
from datetime import date
from datetime import datetime, timedelta, time
import csv
from pathlib import Path


"""
Arquivo: teste3.py
arquivo para testar a função que faz o calculo da data limit inicial a partir de um arquivo Dataframe

"""


## header=True com cabeçalho
def ler_csv(data, header):
    file = open(data, "r", encoding='UTF8')
    if header:
        reader = csv.reader(file, delimiter=",")
        # Skip the first line (header row)
        next(reader, None)  
        data = list(reader)
    else:
        data = list(csv.reader(file, delimiter=","))
    file.close()
    return data

def adicionar_horas_uteis(data_inicial, horas_uteis):
    horas_uteis = int(horas_uteis)
    # Horários de trabalho
    inicio_manha = time(8, 0)
    fim_manha = time(12, 0)
    inicio_tarde = time(14, 0)
    fim_tarde = time(18, 0)

    # Converter data_inicial para datetime se necessário
    if isinstance(data_inicial, str):
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d %H:%M:%S')

    # Adicionar horas úteis
    while horas_uteis > 0:
        # Verificar se é fim de semana
        if data_inicial.weekday() >= 5:  # Sábado e Domingo
            # Ir para a próxima segunda-feira
            data_inicial += timedelta(days=(7 - data_inicial.weekday()))
            data_inicial = data_inicial.replace(hour=inicio_manha.hour, minute=inicio_manha.minute)
            continue

        # Verificar o horário atual e ajustar se necessário
        if data_inicial.time() < inicio_manha:
            data_inicial = data_inicial.replace(hour=inicio_manha.hour, minute=inicio_manha.minute, second=0, microsecond=0)
        elif inicio_manha <= data_inicial.time() < fim_manha:
            pass
        elif fim_manha <= data_inicial.time() < inicio_tarde:
            data_inicial = data_inicial.replace(hour=inicio_tarde.hour, minute=inicio_tarde.minute, second=0, microsecond=0)
        elif inicio_tarde <= data_inicial.time() < fim_tarde:
            pass
        else:
            # Ir para o próximo dia útil às 08:00
            data_inicial += timedelta(days=1)
            data_inicial = data_inicial.replace(hour=inicio_manha.hour, minute=inicio_manha.minute, second=0, microsecond=0)
            continue

        # Calcular o tempo restante no dia útil atual
        if inicio_manha <= data_inicial.time() < fim_manha:
            fim_turno = fim_manha
        else:
            fim_turno = fim_tarde
        tempo_restante_turno = datetime.combine(data_inicial.date(), fim_turno) - data_inicial

        if tempo_restante_turno.total_seconds() / 3600 > horas_uteis:
            data_inicial += timedelta(hours=horas_uteis)
            horas_uteis = 0
        else:
            horas_uteis -= tempo_restante_turno.total_seconds() / 3600
            data_inicial += tempo_restante_turno

    return data_inicial

def datalimit_inicial2(nome_exe5):
    # pegar a datahlimie e o sla e somar
    # para achar a datalimit_inicial

    print(f"função datalimit_inicial de {nome_exe5}")
    df = pd.read_csv("temporario.csv")
    # remover as linhas com chamados suspensos e em andamento
    # df = df[df['situacao'] != 'Suspensa']
    # df = df[df['situacao'] != 'EmAndamento']

    # df.to_csv("teste1.csv", header=False, index=False)
    # df = ler_csv("teste1.csv", False)
    
    df2 = []
    tt2 = []
    # for tt in df:
    for index, row in df.iterrows():    
            data_ini = row[4]
            sla_int = row[19]
            # criar campo data limite2 com a data inicial + sla em dias e horas uteis
            data_ini = data_ini[0:19]
            data_fim = row[20]
            data_fim = data_fim[0:19]
            
            data_limt2 = adicionar_horas_uteis(data_ini, sla_int)
            data_limt2 = data_limt2.strftime("%Y-%m-%d %H:%M:%S")

            # criar novo campo dentro_real com (S,N)
            # comparar a nova data_limite2 e a data_final se a data_final for maior que a data_limite2
            # dentro_real = N
            dentro_real = ""
            if type(data_limt2) == str and data_limt2 != "":
                dt_obj1 = datetime.strptime(data_limt2, "%Y-%m-%d %H:%M:%S")
            else:
                dt_obj1 = data_limt2

            if type(data_fim) == str and data_fim != "":
                dt_obj2 = datetime.strptime(data_fim, "%Y-%m-%d %H:%M:%S")
            else:
                dt_obj2 = data_fim

            if dt_obj2 != "":
                if dt_obj2>dt_obj1:
                    #data_final é maior que a data_limite2
                    dentro_real="N"
                else:
                    #datafinal é menor que a data limite2 esta dentro do prazo
                    dentro_real="S"
            else:
                dentro_real="S"

            tt2.append(row+[data_limt2]+[dentro_real])
            df2.append(tt2[0])
            tt2 = []

    # Salvar o DataFrame atualizado em um novo arquivo CSV
    #df = pd.DataFrame(df2)
    #df.to_csv('teste2.csv', index=False, sep=',', encoding='utf-8')
    data = df2
    return


def tarefa(unidades):
    header = False
    data = ler_csv("temp1.csv", False) # LER o CSV e transformar em LIST

    data2 = datalimit_inicial2(data)



    print(f"Exportação com sucesso - teste1 ")
    tm.sleep(3)
   



unidades = [34]
tarefa(unidades)




