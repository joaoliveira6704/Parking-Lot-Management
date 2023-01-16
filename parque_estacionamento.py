# Este programa faz a gestão de um parque de estacionamento. Tem 4 opções principais, Adicionar Carro, Remover Carro, Mostrar Carros, Editar Carro, e uma opção para sair.

# Trabalho realizado por:
#João Oliveira - A043242
#Gonçalo Condesso - A043413

import msvcrt
import csv
import random
import re
import datetime
import threading
from datetime import time
from os import system, name
from time import sleep

def clear():
    # Apagar elementos da consola
    # Para Windows
    if name == 'nt':
        _ = system('cls')
 
    # Para MacOS e Linux
    else:
        _ = system('clear')

class Carro:
    def __init__(self, marca, matricula, numero_ticket, data_entrada):
        self.marca = marca
        self.matricula = matricula
        self.numero_ticket = numero_ticket
        self.data_entrada = data_entrada

n_lugares = 5
numeros_ticket = set()
matriculas_usadas = set()
carros = []
data_minima = datetime.datetime.strptime("03/01/2020 00:00:01", "%d/%m/%Y %H:%M:%S")
data_atual = datetime.datetime.now()
parar_thread = threading.Event()

# Atualiza a data em tempo real, ao milésimo de segundo, em background
def atualizar_data():
    global data_atual

    loop = True

    while loop:
        data_atual = datetime.datetime.now()

        if parar_thread.is_set():
            break


def criar_ticket():
    # Gerar um número de ticket único entre 100000 e 999999
    numero_ticket = random.randint(100000, 999999)
    while numero_ticket in numeros_ticket:
        numero_ticket = random.randint(100000, 999999)
    numeros_ticket.add(numero_ticket)
    return numero_ticket

def calcular_custo(data_entrada, data_saida):
    data_entrada = datetime.datetime.strptime(data_entrada, "%d/%m/%Y %H:%M:%S")
    data_saida = datetime.datetime.strptime(data_saida, "%d/%m/%Y %H:%M:%S")
    duracao = (data_saida - data_entrada).total_seconds() / 60 
    custo = 0
    data_entrada = data_entrada.time()
    if time(8,0) <= data_entrada < time(20,0):
        if duracao < 15:
            custo = 0.35
        elif duracao < 30:
            custo = 0.50
        elif duracao < 45:
            custo = 1.15
        elif duracao < 60:
            custo = 1.40
        elif duracao < 75:
            custo = 1.70
        else:
            custo = 1.40 + 0.30 *((duracao // 15) - 4)
    else:
        if duracao < 15:
            custo = 0.30
        else:
            custo = 0.30 * (duracao // 15)
    return custo

def adicionar_carro():
    if len(carros) >= n_lugares:
        clear()
        print("Desculpe, o estacionamento está cheio.")
        sleep(2)
        menu()
    else:
        # Adicionar um carro ao estacionamento
        marca = input("Insira a marca do carro: ")
        clear()
        while (not marca.isalpha()) or len(marca) == 0:
            clear()
            marca = input("A marca só pode conter letras. Insira a marca do carro novamente: ")
            clear()
        print("Marca do carro: " + marca)
        matricula = input("Insira a matricula do carro (no formato AABB00): ")
        # Verifica se a matricula corresponde a um dos seguintes formatos (AA00AA, 00AAAA, AAAA00, 00AA00, AA0000, 0000AA)
        while matricula.upper() in matriculas_usadas or not re.match(r'^(?:(?P<part1>[A-Za-z]{2})(?P<part2>[0-9]{2})(?P<part3>[A-Za-z]{2})|(?P<part4>[0-9]{2})(?P<part5>[A-Za-z]{4})|(?P<part6>[A-Za-z]{4})(?P<part7>[0-9]{2})|(?P<part8>[0-9]{2})(?P<part9>[A-Za-z]{2})(?P<part10>[0-9]{2})|(?P<part11>[A-Za-z]{2})(?P<part12>[0-9]{4})|(?P<part13>[0-9]{4})(?P<part14>[A-Za-z]{2}))$', matricula):
            clear()
            print("Marca do carro: " + marca)
            matricula = input("Formato inválido ou matricula já existente! Por favor insira novamente a matrícula do carro (no formato AABB00): ")
        matricula = matricula.upper()
        matriculas_usadas.add(matricula.upper())
        clear()
        print("Marca do carro: " + marca)
        print("Matricula do carro: " + matricula)
        #Verifica se a data introduzida corresponde ao formato pedido
        data_entrada = input("Insira a data de entrada (no formato DD/MM/AAAA HH:MM:SS): ")
        while True:
            try:
                datetime.datetime.strptime(data_entrada, "%d/%m/%Y %H:%M:%S")
                break
            except ValueError:
                clear()
                print("Marca do carro: " + marca)
                print("Matricula do carro: " + matricula)
                data_entrada = input("Formato de data inválido, insira novamente (no formato DD/MM/AAAA HH:MM:SS): ")
        # Verifica se a data introduzida é igual ou superior à data de abertura do parque e inferior à data atual
        while (datetime.datetime.strptime(data_entrada, "%d/%m/%Y %H:%M:%S") < data_minima) or (datetime.datetime.strptime(data_entrada, "%d/%m/%Y %H:%M:%S") > data_atual):
            clear()
            print("Marca do carro: " + marca)
            print("Matricula do carro: " + matricula)
            data_entrada = input("A data introduzida deve ser igual ou superior a 3 de Janeiro de 2000 e inferior à data atual (no formato DD/MM/AAAA HH:MM:SS): ")
            while True:
                try:
                    datetime.datetime.strptime(data_entrada, "%d/%m/%Y %H:%M:%S")
                    break
                except ValueError:
                    clear()
                    print("Marca do carro: " + marca)
                    print("Matricula do carro: " + matricula)
                    data_entrada = input("Formato de data inválido, insira novamente (no formato DD/MM/AAAA HH:MM:SS): ")
        numero_ticket = criar_ticket()
        carro = Carro(marca, matricula.upper(), numero_ticket, data_entrada)
        carros.append(carro)
        clear()
        print("Carro adicionado com sucesso com o número de ticket {}.".format(numero_ticket))
        print()
        sleep(1)
        menu()

def remover_carro():
    # Remover um carro do estacionamento
    if len(carros) > 0:
        print("Carros no parque de estacionamento:\n")
        for carro in carros:
            print("- Número de ticket: {}".format(carro.numero_ticket) + " | " + "Marca: {}".format(carro.marca + " | " + "Matricula: {}".format(carro.matricula) + " | " + "Data de entrada: {}".format(carro.data_entrada)))
        numero_ticket = input("\nInsira o número de ticket do carro: ")
        while (not numero_ticket.isnumeric()) or (int(numero_ticket) not in numeros_ticket):
            clear()
            print("Número inválido ou inexistente! Tente novamente!\n")
            remover_carro()
        numero_ticket = int(numero_ticket)
        clear()
        for i, carro in enumerate(carros):
            if carro.numero_ticket == numero_ticket:
                print("- Número de ticket: {}".format(carro.numero_ticket) + " | " + "Marca: {}".format(carro.marca + " | " + "Matricula: {}".format(carro.matricula) + " | " + "Data de entrada: {}".format(carro.data_entrada)))
        data_saida = input("\nInsira a data de saída (no formato YYYY-MM-DD HH:MM:SS): ")
        while True:
            try:
                datetime.datetime.strptime(data_saida, "%d/%m/%Y %H:%M:%S")
                break
            except ValueError:
                clear()
                for i, carro in enumerate(carros):
                    if carro.numero_ticket == numero_ticket:
                        print("- Número de ticket: {}".format(carro.numero_ticket) + " | " + "Marca: {}".format(carro.marca + " | " + "Matricula: {}".format(carro.matricula) + " | " + "Data de entrada: {}".format(carro.data_entrada)))
                data_saida = input("\nFormato de data inválido, insira novamente (no formato DD/MM/AAAA HH:MM:SS): ")
        while data_saida <= carro.data_entrada or (datetime.datetime.strptime(data_saida, "%d/%m/%Y %H:%M:%S") > data_atual):
            clear()
            for i, carro in enumerate(carros):
                if carro.numero_ticket == numero_ticket:
                    print("- Número de ticket: {}".format(carro.numero_ticket) + " | " + "Marca: {}".format(carro.marca + " | " + "Matricula: {}".format(carro.matricula) + " | " + "Data de entrada: {}".format(carro.data_entrada)))
            data_saida = input("\nA data de saída deve ser maior que a data de entrada e menor que a data atual, insira novamente (no formato DD/MM/AAAA HH:MM:SS): ")
            while True:
                try:
                    datetime.datetime.strptime(data_saida, "%d/%m/%Y %H:%M:%S")
                    break
                except ValueError:
                    clear()
                    for i, carro in enumerate(carros):
                        if carro.numero_ticket == numero_ticket:
                            print("- Número de ticket: {}".format(carro.numero_ticket) + " | " + "Marca: {}".format(carro.marca + " | " + "Matricula: {}".format(carro.matricula) + " | " + "Data de entrada: {}".format(carro.data_entrada)))
                    data_saida = input("\nFormato de data inválido, insira novamente (no formato DD/MM/AAAA HH:MM:SS): ")
        for i, carro in enumerate(carros):
            if carro.numero_ticket == numero_ticket:
                custo = calcular_custo(carro.data_entrada, data_saida)
                del carros[i]
                numeros_ticket.remove(numero_ticket)
                matriculas_usadas.remove(carro.matricula)
                clear()
                print("Carro Removido: \n")
                print("Número de ticket: {}".format(numero_ticket))
                print("Marca: {}".format(carro.marca))
                print("matricula: {}".format(carro.matricula))
                print("Data de entrada: {}".format(carro.data_entrada))
                print("Data de saída: {}".format(data_saida))
                print("Custo: {:.2f} euros".format(custo))
                print("\nClique em qualquer tecla para voltar ao menu")
                msvcrt.getch()
                clear()
                menu()
    else:
        print("Não existem carros no parque de estacionamento! \n\nAdicione um carro e tente novamente!")
        sleep(2)
        menu()

def mostrar_carros():
    # Mostrar todos os carros no estacionamento
    if len(carros) <= 0:
        print("Não existem carros no parque de estacionamento! \n\nAdicione um carro e tente novamente!")
        sleep(2)
        menu()
    else:
        print("Quantidade de lugares disponiveis: " + str(n_lugares - len(carros)))
        print("\nCarros no parque de estacionamento:")
        for carro in carros:
            print("- Número de ticket: {}".format(carro.numero_ticket) + " | " + "Marca: {}".format(carro.marca + " | " + "Matricula: {}".format(carro.matricula) + " | " + "Data de entrada: {}".format(carro.data_entrada)))
        print()
        print("Clique em qualquer tecla para voltar ao menu", end="")
        msvcrt.getch()
        menu()

def editar_carro():
    if len(carros) <= 0:
        print("Não existem carros no parque de estacionamento! \n\nAdicione um carro e tente novamente!")
        sleep(2)
        menu()
    else:
        # Editar as informações de um carro
        print("Carros no parque de estacionamento:\n")
        for carro in carros:
            print("- Número de ticket: {}".format(carro.numero_ticket) + " | " + "Marca: {}".format(carro.marca + " | " + "Matricula: {}".format(carro.matricula) + " | " + "data de entrada: {}".format(carro.data_entrada)))
        numero_ticket = input("\nInsira o número de ticket do carro: ")
        while (not numero_ticket.isnumeric()) or (int(numero_ticket) not in numeros_ticket):
            clear()
            print("Número inválido ou inexistente! Tente novamente!\n")
            editar_carro()
        numero_ticket = int(numero_ticket)
        clear()
        for i, carro in enumerate(carros):
            if carro.numero_ticket == numero_ticket:
                matriculas_usadas.remove(carro.matricula)
                marca = input("Insira a nova marca do carro: ")
                clear()
                while (not marca.isalpha()) or len(marca) == 0:
                    clear()
                    marca = input("A marca só pode conter letras. Insira a marca do carro novamente: ")
                    clear()
                print("Nova marca do carro: " + marca)
                matricula = input("Insira a nova matricula do carro (no formato AABB00): ")
                matricula = matricula.upper()
                clear()
                # Verifica se a matricula corresponde a um dos seguintes formatos (AA00AA, 00AAAA, AAAA00, 00AA00, AA0000, 0000AA)
                while matricula.upper() in matriculas_usadas or not re.match(r'^(?:(?P<part1>[A-Za-z]{2})(?P<part2>[0-9]{2})(?P<part3>[A-Za-z]{2})|(?P<part4>[0-9]{2})(?P<part5>[A-Za-z]{4})|(?P<part6>[A-Za-z]{4})(?P<part7>[0-9]{2})|(?P<part8>[0-9]{2})(?P<part9>[A-Za-z]{2})(?P<part10>[0-9]{2})|(?P<part11>[A-Za-z]{2})(?P<part12>[0-9]{4})|(?P<part13>[0-9]{4})(?P<part14>[A-Za-z]{2}))$', matricula):
                    clear()
                    print("Nova marca do carro: " + marca)
                    matricula = input("Formato inválido ou matricula já existente! Por favor insira novamente a matrícula do carro (no formato AABB00): ")
                    matricula = matricula.upper()
                    clear()
                print("Nova marca do carro: " + marca)
                print("Nova matricula do carro(no formato AABB00): " + matricula)
                data_entrada = input("Insira a data de entrada (no formato DD/MM/AAAA HH:MM:SS): ")
                while True:
                    try:
                        datetime.datetime.strptime(data_entrada, "%d/%m/%Y %H:%M:%S")
                        break
                    except ValueError:
                        clear()
                        print("Nova marca do carro: " + marca)
                        print("Nova matricula do carro(no formato AABB00): " + matricula)
                        data_entrada = input("Formato de data inválido, insira novamente (no formato DD/MM/AAAA HH:MM:SS): ")
                # Verifica se a data introduzida é igual ou superior à data de abertura do parque e inferior à data atual
                while (datetime.datetime.strptime(data_entrada, "%d/%m/%Y %H:%M:%S") < data_minima) or (datetime.datetime.strptime(data_entrada, "%d/%m/%Y %H:%M:%S") > data_atual):
                    clear()
                    print("Nova marca do carro: " + marca)
                    print("Nova matricula do carro: " + matricula)
                    data_entrada = input("A data introduzida deve ser igual ou superior a 3 de Janeiro de 2000 e inferior à data atual (no formato DD/MM/AAAA HH:MM:SS): ")
                    while True:
                        try:
                            datetime.datetime.strptime(data_entrada, "%d/%m/%Y %H:%M:%S")
                            break
                        except ValueError:
                            clear()
                            print("Nova marca do carro: " + marca)
                            print("Nova matricula do carro: " + matricula)
                            data_entrada = input("Formato de data inválido, insira novamente (no formato DD/MM/AAAA HH:MM:SS): ")
                carro.marca = marca
                carro.matricula = matricula
                matriculas_usadas.add(matricula.upper())
                carro.data_entrada = data_entrada
                clear()
                print("Informações do carro editadas com sucesso.")
                sleep(2)
                menu()

def sair():
    # Guardar os carros no estacionamento num ficheiro CSV
    guardar = input("Deseja guardar as alterações? (S/N) ")
    if guardar.upper() == "S":
        salvar_carros()
        salvar_matriculas()
        clear()
        print("Informações dos carros guardadas com sucesso!")
        sleep(2)
        clear()
    parar_thread.set()
    exit()

def salvar_carros():
    with open('carros.csv', 'w', newline='') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        for carro in carros:
            escritor.writerow([carro.marca, carro.matricula, carro.numero_ticket, carro.data_entrada])
        clear()
        print("A salvar informações", end="")
        sleep(1)
        print(".", end="")
        sleep(1)
        print(".", end="")
        sleep(1)
        print(".", end="")
        sleep(1)
        clear()

def ler_ficheiro_csv():
    clear()
    global carros
    global numeros_ticket
    try:
        with open('carros.csv', 'r') as arquivo_csv:
            leitor = csv.reader(arquivo_csv)
            for linha in leitor:
                if len(linha) != 4:
                    continue
                marca, matricula, numero_ticket, data_entrada = linha
                carro = Carro(marca, matricula, int(numero_ticket), data_entrada)
                carros.append(carro)
                numeros_ticket.add(carro.numero_ticket)
            print("A ler e carregar informações", end="")
            sleep(1)
            print(".", end="")
            sleep(1)
            print(".", end="")
            sleep(1)
            print(".", end="")
            sleep(1)
            clear()
            print("Informações dos carros lidas com sucesso!")
            sleep(3)
            clear()
    except FileNotFoundError:
        open('carros.csv', 'a').close()
        open('matriculas.csv', 'a').close()

def salvar_matriculas():
    # Salvar matriculas usadas
    with open('matriculas.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for matricula in matriculas_usadas:
            writer.writerow([matricula])

def carregar_matriculas():
    # Carregar matriculas usadas
    with open('matriculas.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            matriculas_usadas.add(row[0])

# Mostrar o menu
def menu():
    clear()
    print("Menu:")
    print("\n1. Adicionar carro")
    print("2. Remover carro")
    print("3. Mostrar carros")
    print("4. Editar carro")
    print("\n5. Sair")
    opcao = input("\nInsira a opção desejada: ")
    if opcao == "1":
        clear()
        adicionar_carro()
    elif opcao == "2":
        clear()
        remover_carro()
    elif opcao == "3":
        clear()
        mostrar_carros()
    elif opcao == "4":
        clear()
        editar_carro()
    elif opcao == "5":
        clear()
        sair()
    else:
        clear()
        print("Opção inválida!")
        sleep(1)
        menu()

ler_ficheiro_csv()
carregar_matriculas()
atualizar_thread = threading.Thread(target=atualizar_data)
atualizar_thread.start()
menu()
atualizar_thread.join()