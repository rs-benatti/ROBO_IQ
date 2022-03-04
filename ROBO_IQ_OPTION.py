import pyautogui as gui
import time, pyperclip, datetime, re, schedule, telepot

time.sleep(5)
gui.PAUSE = 0.5
gui.FAILSAFE = True
#Colocar estatísticas
#Colocar precisão de segundos
#Colocar alerta que algo vai acontecer
#Checar se dá pra rodar em outra área de trabalho
#Operar com duas ao mesmo tempo
#presetar iqOption #fechar abas laterais, colocar em 30 min
#Garantir contra mercado fechado. O robô não compra mais nenhum se tentar em um mercado fechado

#Primeira moeda do roll é na posiçção Point(x=780, y=157)
#última moeda do roll é nMundo Milionario
# a posiçção Point(x=821, y=645)
bot = telepot.Bot("1266652607:AAFgCAKtYZAHuR29LcmD1aYKpIPDnB8npBc")#Iniciando um objeto com o ID do meu bot do telegram

def enviaMsg(msg):# Serve pra o bot enviar mensagem para mim
    bot.sendMessage(1173601583, msg) #O primeiro parâmetro é um ID do telegram

def alerta():#Mexe o mouse em forma de quadrado como forma de alerta que algo vai acontecer. Apear da função existir, não tá sendo empregada
    a = 0
    while a < 2:
        gui.moveRel(0, 100, duration = 0.10)
        gui.moveRel(100, 0, duration = 0.10)
        gui.moveRel(0, -100, duration = 0.10)
        gui.moveRel(-100, 0, duration = 0.10)
        a += 1

def setValue(value):#Coloca o valor a ser usado na entrada
    gui.moveTo(1305, 212)#Local onde se digita o valor
    gui.click()
    gui.typewrite(['right', 'right', 'right', 'right', 'right', 'right'])#Vai pra ponta direita do número, para apaga-lo por inteiro
    gui.typewrite(['backspace', 'backspace', 'backspace', 'backspace', 'backspace', 'backspace', 'backspace', 'backspace', 'backspace'])#apaga o número
    gui.typewrite(str(value))#digita o valor enviado como parâmetro

def iqInicializar():#Faz login no iqOption, supondo que já esteja aberto
    gui.moveTo(602, 464)#Move o mouse para o botão de entrar
    time.sleep(1)
    im = gui.screenshot()
    if im.getpixel((602, 464)) == (187, 92, 12):#Checa se o botão de entrar está na cor esperada
        gui.moveTo(665, 368)#Clica no local de digitar a senha
        gui.click()
        gui.sleep(0.5)
        gui.typewrite(['right', 'right', 'right', 'right', 'right', 'right'])#Vai pra ponta direita da senha, para apaga-lo por inteiro
        gui.typewrite(['backspace', 'backspace', 'backspace', 'backspace', 'backspace', 'backspace', 'backspace', 'backspace', 'backspace'])#apaga a senha
        gui.typewrite('*******')#Digita minha senha
        gui.moveTo(680, 459)#Clica no botão de entrar
        gui.click()
        gui.sleep(7)#Espera carregar

def iqOptionAbrir():#Abre o iqOption se ele já não estiver aberto
    im = gui.screenshot()
    if im.getpixel((498, 733)) == (6, 23, 27) or im.getpixel((34, 72)) != (255, 119, 0):#Checa se o pixel do ícone do iqOption não está acinzentado
        gui.moveTo(515, 747)#Clica no ícone
        gui.click()
        gui.sleep(1)
    i = 0
    while i < 100:#Serve para colocar o gráfico no seu último tempo, para evitar erros na busca pela placa de lucro/prejuízo
        i += 1
        gui.hotkey('alt', 'left')#alt + left é um atalho do iq para se localizar no gráfico

def telegramAbrir():#Abre ou minimiza o telegram, independente de sua situação atual
    gui.moveTo(464, 748)#ícone do telegram na barra de tarefas
    gui.click()
    time.sleep(1)

def telegramSearch(string):#Procura por alguma conversa no telegram
    gui.moveTo(475, 113)#Clica na caixa de texto
    gui.click()
    gui.typewrite(string)#Digita o nome da conversa
    gui.typewrite(['enter'])#Aperta enter, entrando na primeira conversa que aparecer (a mais compatível com o pesquisado)

def telegramCopy():#Seleciona mensagens recentes nem alguma conversa#Checar se tá copiando mesmo #buscar pixel meio azulado
    gui.moveTo(850, 500)#Bota o mouse na parte inferior da conversa, no centro
    gui.mouseDown()#Aperta o botão p baixo, segurando-o
    gui.moveTo(629, 76)#Move o mouse pra cima, induzindo a conversa a subir
    gui.sleep(3)#A conversa sobe por 3 segundos
    gui.mouseUp()#O botao do mouse é solto
    gui.hotkey('ctrl', 'c')#Copia as mensagens
    time.sleep(1)#pausa para estabilizar
    gui.typewrite(['esc'])#'esc' para sair da seleção de mensagens
    try:
        gui.click(gui.center(gui.locateOnScreen('seta do telegram.png')))
    except:
        gui.moveTo(1045, 580)#Clica em um botão no canto inferior direito da conversa para voltar para a última mensagem enviada na conversa
    #deixando a conversa preparada para receber mais uma pesquisa
    gui.click()

def buscaPrev(texto):#busca por padrões de mensagens que indiquem previsões de sinais do grupo 'Mundo Milionário'#retorna 0 se ainda não tem previsão #enviar pyperclip.paste()
    hoje = datetime.datetime.now()
    buscaHorario = re.compile(r'''
        ((\d\d #Procura pela data
        , #Virgula
        \d\d #horas
        : #dois pontos
        \d\d #minutos
        , #virhula
        \w\w\w\w\w\w #nome da opção
        , #virgula
        (PUT|CALL)) #put ou call
        \s*) #um espaço, ou mais
    ''', re.VERBOSE)
    prevsDeHoje = []
    try: #método try except pq se não encontrar nada que se encaixe no padrão, daria erro
        for test in buscaHorario.findall(texto): #busca tudo que se encaixa no padrão (para cada coisa que se encaixa no padrão)
            #o número que representa o dia é seguido de uma vírgula e o horário, sendo o único número que se encaixa nesse padrão
            if ((str(hoje.day) + ',0') in test[0]) or((str(hoje.day) + ',1') in test[0]) or((str(hoje.day) + ',2') in test[0]):#assim, é checado se tem algum número que se encaixe com o dia de hoje e seja seguido por uma virgula + um número que represente um horário
                prevsDeHoje.append(test[0])#se encontrou, adiciona ao array prevsDeHoje
        if len(prevsDeHoje) >= 5: #ao fim do loop for, se prevsDeHoje tiver um tamanho razoável, prevsDeHoje é retornad pela função
            return prevsDeHoje  #Isso é feito com o intuito de evitar possíveis erros
        else: #caso contrário, retorna 0, indicando que as exigências para os padrões não foram atendidas
            return 0
    except:
        return 0

def buscaHora(texto): 
    buscaHoraDaCompra = re.compile(r'''(#padrão para o horário da compra
        (\d\d)#horas
        :
        (\d\d)#minutos
    )''', re.VERBOSE)
    horas = []
    for group in buscaHoraDaCompra.findall(texto):
        horas.append(int(group[1]))
        horas.append(int(group[2]))
    return horas #horas[0] é as horas, horas [1] são os minutos

def buscaCompra(texto):#busca pelo tipo de compra, se é call ou put
    buscaCall = re.compile(r'(CALL)')#procura por call
    buscaPut = re.compile(r'(PUT)')#procura por put
    #retorna a string encontrada
    if buscaCall.search(texto) != None:
        return 'CALL'
    if buscaPut.search(texto) != None:
        return 'PUT'

def buscaNome(texto):#busca pelo nome da opção
    buscaNomeDaCompra = re.compile(r'''(
        [a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z]#seis letras seguidas
    )''', re.VERBOSE)
    return buscaNomeDaCompra.search(texto).group()#retorna o nome da opção
#ao passo que buscaPrev busca todas as previsões, buscaHora, buscaNome e buscaCompra devem ser aplicados para uma linha de previsão só

def lucroOuPreju():#busca por um tom esverdeado ou avermelhado ao fim de uma operação
    i = 0
    while i < 100:
        i += 1
        gui.hotkey('alt', 'left') #vai para o fina do gráfico, para que a plaquinha de lucro ou prejuízo fique numa posição previsivel
    gui.moveTo(920, 165)#move para o ponto de patida da busca pela placa
    a = 0
    tempoAnt = datetime.datetime.now()
    print('Buscand resultado')
    while datetime.datetime.now().minute - tempoAnt.minute < 2:# durante dois minutos procura verticalmente na posição x=165 pela placa
        im = gui.screenshot()
        a += 3#procura de 3 em 3 pixels pra ir rapidinho
        if a > 456:#se a descer muito, zera a, reposicionando a busca pra um '0 de máquina'
            a = 0 #zera 'a'
        if im.getpixel((910, 165 + a))[1] > 120 and im.getpixel((910, 165 + a))[0] < 120 and im.getpixel((910, 165 + a))[2] < 120:# procura por um tom esverdeado
            print('LUCRO')
            return 'LUCRO'
        if im.getpixel((910, 165 + a))[0] > 120 and im.getpixel((910, 165 + a))[1] < 120 and im.getpixel((910, 165 + a))[2] < 120:#procura por um tom avermelhado
            print('PREJU')
            return 'PREJU'
    #se não encontrar, retorna abstenção #util para detecçção de erros
    return 'ABSTENÇÃO'

def martingale():#Faz a multiplicação do valor de entrada, mas não realiza compras
    gui.moveTo(1304, 194)#clica no lugar de botar o número
    gui.click()
    gui.sleep(0.3)#estabiliza
    gui.moveTo(1173, 491)#clica na calculadora
    gui.click()
    gui.sleep(0.3)#estabiliza
    gui.moveTo(1056, 237)#clica no asterisco
    gui.click()
    gui.sleep(0.3)#estabiliza
    gui.moveTo(1173, 491)#clica na calculadora
    gui.click()
    gui.typewrite(['esc'])#sai da mudança de valor
    '''
    gui.moveTo(1302, 431)
    gui.click()
    '''

class moeda: #classe com algumas funções inerentes a abrir as moedas
    def __init__(self, posx, posy, nome): 
        self.posx = posx
        self.posy = posy
        self.nome = str(nome)
    def novo(self):#clica no mais para adcionar botões
        gui.moveTo(420, 63)
        gui.click()
    def create(self):#digita o nome da opção e seleciona
        self.novo()#Clica para adicionar nova moeda
        time.sleep(0.5)
        gui.typewrite(self.nome)#digita o nome daopção
        gui.moveTo(580, 100)#clica nas opções binárias
        gui.click()
        gui.moveTo(1003, 155) #move o mouse pra cima da opção, para ver se ela existe
        im = gui.screenshot()
        if im.getpixel((822, 162)) != (28, 32, 48): #(28, 32, 48) é a cor de fundo, assim, quando o mouse foi p cima da opção, se ela existir, seria uma cor diferente
            pixelX = 966
            foundGreen = 0
            while pixelX < 1074:#busca horizontalmente por um pixel verde, para saber se a opção está fechada, ou aberta, estando fechando, as porcentagens do rendimento não aparecem
                if im.getpixel((pixelX, 148))[0] < 100 and im.getpixel((pixelX, 148))[1] > 180 and im.getpixel((pixelX, 148))[2] < 100:# == (51, 204, 89): busca por um pixel com uma tonalidade forte
                    foundGreen = 1
                pixelX += 1
            if foundGreen == 1:# se encontrou o pixel verde, seleciona a opção binária
                gui.moveTo(780, 157)
                gui.click()
            else:#senão, clica em digital
                gui.moveTo(580, 160)#seleciona as opções digitais
                gui.click()
                time.sleep(0.5)
                gui.moveTo(780, 157)#clica na primeira opção
                gui.click()
        else:# senão, seleciona uma digital
            gui.moveTo(580, 160)#sleciona as opções digitais
            gui.click()
            time.sleep(0.5)
            gui.moveTo(780, 157)#escolhe a primeira
            gui.click()
        #seleciona o tempo das barras
        time.sleep(3)
        gui.moveTo(94, 576)#clica na blinha de mudar o tempo
        gui.click()
        time.sleep(0.5)
        gui.moveTo(328, 414)#seleciona 5 min
        gui.click()

def novo():#a mesma função, só que fora da classe #?????
    gui.moveTo(420, 63)
    gui.click()

def fechar():#função para fechar as opções que estão abertas
    gui.moveTo(384, 40)
    gui.click()

def call(exp, buyTime, buySecond):#exp deve ser 1, 2, 3, 4 ou 5 #O default é 5
    iqOptionAbrir()
    gui.moveTo(1281, 125)#clica no botão de escolher o tempo
    gui.click()
    time.sleep(1)
    try:#poderia ser usado exp apenas igual a 5, ao inés de ser recebido como parâmetro, uma vez que o programa está voltado para opções M5
        if int(exp) < 1 or int(exp) > 5:
            exp = 5
        incrementox = (int(exp) - 1) * 30
    except:
        print("O parâmetro enviado a 'call' não é valido")
        incrementox = 120#padrão para exp = 5
    iqOptionAbrir()
    im = gui.screenshot()
    if im.getpixel((983, 225 + incrementox)) == (28, 32, 48):#checa se o tempo a ser selecionado existe na posição para os tempos de opções binárias
        gui.moveTo(983, 225 + incrementox)#clica no tempo
        gui.click()
    else:#caso contrário, clica no digital de 5 min
        gui.moveTo(1198, 227)
        gui.click()
    time.sleep(3)# estabiliza
    seconds = buySecond - buyTime.second #faz as contas para ajusar o tempo para que a compra seja feita nos segundos especificados no último parâmetro
    clickTime = buyTime + datetime.timedelta(seconds= seconds)
    abreTime = clickTime - datetime.timedelta(seconds=5)#tempo para abrir o iqOption antes de comprar
    while datetime.datetime.now() < abreTime:
        time.sleep(0.5)
    iqOptionAbrir()
    while datetime.datetime.now() < clickTime:#espera pelo tempo de clicar em 'call'
        time.sleep(0.5)
    gui.moveTo(1302, 431)#clica em call
    time.sleep(0.5)
    gui.click()
    time.sleep(0.5)
def put(exp, buyTime, buySecond):
    iqOptionAbrir()
    gui.moveTo(1281, 125)#clica no botão de escolher o tempo
    gui.click()
    time.sleep(1)
    try:#poderia ser usado exp apenas igual a 5, ao inés de ser recebido como parâmetro, uma vez que o programa está voltado para opções M5
        if int(exp) < 1 or int(exp) > 5:
            exp = 5
        incrementox = (int(exp) - 1) * 30
    except:
        print("O parâmetro enviado a 'put' não é valido")
        incrementox = 120#padrão para exp = 5
    im = gui.screenshot()
    if im.getpixel((983, 225 + incrementox)) == (28, 32, 48):#checa se o tempo a ser selecionado existe na posição para os tempos de opções binárias
        gui.moveTo(983, 225 + incrementox)#clica no tempo
        gui.click()
    else:#caso contrário, clica no digital de 5 min
        gui.moveTo(1198, 227)
        gui.click()
    time.sleep(3)
    seconds = buySecond - buyTime.second #faz as contas para ajusar o tempo para que a compra seja feita nos segundos especificados no último parâmetro
    clickTime = buyTime + datetime.timedelta(seconds= seconds)
    abreTime = clickTime - datetime.timedelta(seconds=5)#tempo para abrir o iqOption antes de comprar
    while datetime.datetime.now() < abreTime:
        time.sleep(0.5)
    iqOptionAbrir()
    while datetime.datetime.now() < clickTime:#espera pelo tempo de clicar em 'call'
        time.sleep(0.5)
    gui.moveTo(1302, 546)#clia em 'put'
    time.sleep(0.5)
    gui.click()
    time.sleep(0.5)

def stopGain(numOp, martingales):#seá necessário contabilizar o número de operações(incllusive martingale) e um vetor que armazene 1 nas operações que foram martingales
    #exemplo: na primeira aposta vc apostou, perdeu e fez um matingale, então o primeiro elemento do vetor é 0(martingale[0] = 0) e o segundo, é um (martingale[1] = 1)
    #falta fazer rolar a parada e abrir e fechar o histórico
    gui.moveTo(42, 203)
    gui.click()
    gui.sleep(0.5)
    gui.moveTo(329, 154)
    gui.click()
    gui.sleep(0.5)
    pos = 0
    vermelhoAnt = 0
    saldo = 0.0
    moved = 0
    #inicial y = 218 x = 270 e final x = 319
    #58 pixels entre um e outro
    while (pos < numOp):
        posy = 218 + (pos * 58)
        im = gui.screenshot()
        verde = 0 
        vermelho = 0
        if pos >= 9:
            if moved == 0:
                gui.moveTo(332, 192)
                gui.mouseDown()
                gui.moveTo(332, 278)
                gui.mouseUp()
                gui.sleep(1)
                moved = 1
            posy = 218 + ((pos - 9) * 58)
        for x in range(270, 319):
            cor = im.getpixel((x, posy))
            if cor[0] < 100 and cor[1] > 180 and cor[2] < 100:
                verde = 1
            if cor[0] > 180 and cor[1] < 100 and cor[2] < 100:
                vermelho = 1  
        if verde == 1:
            print(f'{pos + 1}° é verde')
            saldo = saldo + 0.8
            if martingales[(numOp) - pos - 1] == 1:
                print('martingale bem executado')
                saldo = saldo + 1.0
        elif vermelho == 1:
            print(f'{pos + 1}° é vermelho')
            saldo = saldo - 1.0
            if vermelhoAnt == vermelho and martingales[(numOp) - pos - 1] == 1:
                print('Dois vermelhos seguidos')
                saldo = saldo -1.15
        else:
            print('inconclusivo')
        vermelhoAnt = vermelho
        gui.moveTo(270, posy)
        gui.sleep(1)
        pos += 1
    gui.moveTo(306, 127)
    gui.click()
    gui.sleep(0.5)
    if saldo >= 1.6:
        print('stopGain')
    else: 
        print('bad')
    print(saldo)
    return saldo

def butPut():#só um click no botão do put
    gui.moveTo(1302, 546)
    gui.click()

def butCall():#só um click no 'call'
    gui.moveTo(1302, 431)
    gui.click()

def setTempo():#coloca o tempo de expiração em 5 min, avaliando se é binária ou digital
    gui.moveTo(1281, 125)#clica no botão de mudar o tempo
    gui.click()
    time.sleep(1)
    im = gui.screenshot()
    if im.getpixel((983, 345)) == (28, 32, 48):#checa se o botão de 5 min exxite na opção binária
        gui.moveTo(983, 345)#clica
        gui.click()
    else:#senão, escolhe os 5 min digitais
        gui.moveTo(1198, 227)
        gui.click()
    time.sleep(3)

def main():
    '''
    telegramAbrir()
    telegramSearch('Mundo Milionario')
    telegramCopy()
    time.sleep(0.5)
    telegramAbrir()
    '''
    pyperclip.copy(r'''
    26,17:35,USDJPY,CALL
    26,17:37,USDJPY,CALL
    26,17:39,EURGBP,CALL
    26,17:41,EURJPY,CALL
    26,17:43,AUDJPY,CALL
    26,17:45,AUDJPY,CALL
    26,17:47,USDJPY,CALL
    26,17:49,EURJPY,CALL
    26,17:51,EURJPY,CALL
    26,17:53,EURJPY,CALL''')
    numOp = 0
    martins = []
    prevs = buscaPrev(pyperclip.paste())
    while prevs == 0:
        print("Erro")
        time.sleep(120)
        telegramAbrir()
        time.sleep(0.5)
        telegramSearch('Mundo Milionario')
        time.sleep(0.5)
        telegramCopy()
        telegramAbrir()
        prevs = buscaPrev(pyperclip.paste())
    hoje = datetime.datetime.now()
    iqOptionAbrir()
    for prev in prevs:
        time.sleep(1)
        iqOptionAbrir()
        iqOptionAbrir()
        time.sleep(4)
        iqInicializar()
        iqOptionAbrir()
        time.sleep(0.5)    
        fechar()
        hora = buscaHora(prev)
        nome = buscaNome(prev)
        compra = buscaCompra(prev)
        buyMinute = hora[1]
        buyHour = hora[0]
        buyTimeAnt = datetime.datetime(hoje.year, hoje.month, hoje.day, buyHour, buyMinute, 00)
        buyTime = buyTimeAnt - datetime.timedelta(seconds=28)
        print(buyTime)
        print(nome)
        print(compra)
        value = 10
        msg = f'Próxima operação:\n\n{nome.upper()}\nHorário da compra: {buyTimeAnt.hour}:{buyTimeAnt.minute}.{buyTimeAnt.second}\nOperação: {compra}\nValor de entrada: R${float(value)}'
        if buyTime > datetime.datetime.now():
            enviaMsg(msg)
        while datetime.datetime.now() < buyTime:
            time.sleep(0.5)
        gui.typewrite(['esc'])
        if datetime.datetime.now().minute == buyTime.minute and datetime.datetime.now().hour == buyTime.hour and datetime.datetime.now().second < buyTime.second + 3:
            print(prev)
            print(buyTime)
            print(nome)
            print(compra)
            iqOptionAbrir()
            obj = moeda(780, 157, nome)
            obj.create()
            setValue(value)
            time.sleep(2)
            if compra == 'CALL':
                call(5, buyTime, 57)
            if compra == 'PUT':
                put(5, buyTime, 57)
            enviaMsg(f'Operação realizada: ✅\n\n{nome.upper()}\nHorário da compra: {buyTimeAnt.hour}:{buyTimeAnt.minute}.{buyTimeAnt.second}\nOperação: {compra}\nValor de entrada: R${float(value)}')
            numOp += 1
            endTime = buyTime + datetime.timedelta(seconds = 325)
            setTempoTime = endTime - datetime.timedelta(seconds=25)
            print(setTempoTime)
            print(endTime)
            while datetime.datetime.now() < setTempoTime:
                time.sleep(0.5)
            gui.typewrite(['esc'])
            iqOptionAbrir()
            time.sleep(1)
            butCall()
            setValue(value * 1.3)
            #martingale()
            setTempo()
            novo()
            while datetime.datetime.now() < endTime:
                time.sleep(0.5)
            gui.typewrite(['esc'])
            iqOptionAbrir()
            resultado = lucroOuPreju()
            fechar()
            novo()
            martins.append(0)
            martingaleFlag = 0
            if resultado == 'LUCRO':
                fechar()
                msg = f'Operação finalizada\n\n{nome.upper()}\nHorário da compra: {buyTimeAnt.hour}:{buyTimeAnt.minute}.{buyTimeAnt.second}\nOperação: {compra}\nValor de entrada: R${float(value)}\n\nResultado: Lucro✅✅'
            if resultado == 'ABSTENÇÃO':
                fechar()
                msg = f'Operação finalizada\n\n{nome.upper()}\nHorário da compra: {buyTimeAnt.hour}:{buyTimeAnt.minute}.{buyTimeAnt.second}\nOperação: {compra}\nValor de entrada: R${float(value)}\n\nResultado: ABSTENÇÃO❗️❗️'
            if resultado == 'PREJU':
                time.sleep(1)
                martingaleFlag = 1
                msg = f'Operação finalizada\n\n{nome.upper()}\nHorário da compra: {buyTimeAnt.hour}:{buyTimeAnt.minute}.{buyTimeAnt.second}\nOperação: {compra}\nValor de entrada: R${float(value)}\n\nResultado: Execução de um martingale❌❌'
                if compra == 'CALL':
                    butCall()
                if compra == 'PUT':
                    butPut()
            enviaMsg(msg)
            if stopGain(numOp, martins) >= 2.4:
                break
            if martingaleFlag == 1:
                numOp += 1
                martins.append(1)
        fechar()
        fechar()
main()
