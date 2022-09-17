import random
import time

# Tamanho total do tabuleiro
MAX_SIZE = 10
# Define indicador de peça Preta
BLACK_PIECE = 'p'
# Define indicador de peça Dama Preta
BLACK_PIECE_CHECK = 'P'
# Define indicador de peça Branca
WHITE_PIECE = 'b'
# Define indicador de peça Dama Branca
WHITE_PIECE_CHECK = 'B'
# Define indicador de casa sem peça
BLANK = '-'

class Tabuleiro:

    def __init__(self,n):
        self.casas=[]
        self.pretas=0
        self.brancas=0
        self.lado=n
    
    def imprima(self):
        # Inicializa o cabeçalho do tabuleiro
        board_header = "  | "
        # Appenda a quantidade de colunas para o cabeçalho
        for i in range(MAX_SIZE):
            board_header += "{0} ".format(i)
        board_header += "\n--+----------------"
        # Imprime o cabeçalho
        print(board_header)
        # Mostra as linhas do tabuleiro
        for i in range(self.lado):
            # Imprime o identificador da liha
            print(i,'|',end=' ')
            # Percorre as colunas
            for j in range(self.lado):
                # Verifica se é espaço para inserir as peças
                if (j+i)%2==0:
                    print('-',end=' ')
                else:
                    print(self.casas[i][j].cont,end=' ')
            print()
    
    #Gira o tabuleiro, o que é útil ao trocar a vez (a direita da branca vira a esquerda da preta)
    def inverta(self):
        for i in range(self.lado):
            for j in range(self.lado):
                vtemp=self.casas[i][j].vesq
                atemp=self.casas[i][j].aesq
                self.casas[i][j].vesq=self.casas[i][j].adir
                self.casas[i][j].aesq=self.casas[i][j].vdir
                self.casas[i][j].vdir=atemp
                self.casas[i][j].adir=vtemp
                
    #Apenas para conferir se cada casa relevante para o jogo tem os vizinhos correctos
    def conferência(self):
        for i in range(self.lado):
            for j in range(self.lado):
                if (i+j)%2==1: 
                    casebre=self.casas[i][j]
                    print(i,j,casebre.aesq,casebre.adir,casebre.vesq,casebre.vdir)
                
    #Invocada apenas uma vez para determinar as adjacências de cada casa
    def gere_casas(self):
        for i in range(self.lado):
            self.casas.append([])
            for j in range(self.lado):
                self.casas[i].append(Casa(i,j))
            
        for i in range(self.lado):
           for j in range(self.lado):
               if (i+j)%2==1:
                   self.casas[i][j].gere_adj_desta(i,j)
         
        #Preenche o tabuleiro vazio com a configuração inicial do jogo
        for i in range(self.lado):
            for j in range(self.lado):
                if (i+j)%2==1:
                    if i<=3:
                        self.casas[i][j].cont = BLACK_PIECE
                        self.pretas+=1
                    elif i>=6:
                        self.casas[i][j].cont = WHITE_PIECE
                        self.brancas+=1

    #Verifique se uma dama foi formada na rodada
    def verifique_dama(self,vez):
        for i in range(self.lado):
            for j in range(self.lado):
                casa=self.casas[i][j]
                if casa.cont==vez[0]:
                    if casa.adir==None and casa.aesq==None:
                        casa.cont=vez[1]
    
    #Há apenas damas no tabuleiro?
    def qso_damas(self):
        for i in range(self.lado):
            for j in range(self.lado):
                casa=self.casas[i][j]
                # Verifica se a casa contém uma peça preta ou branca
                if casa.cont == BLACK_PIECE or casa.cont == WHITE_PIECE:
                    return(0)
        return(1)
                    
class Casa:   
    def __init__(self,i,j):
        #####################################################
        # Árvore de vizinhança: cada casa tem quatro vizinhas
        self.vesq=None #Casa vizinha de trás e esquerda
        self.vdir=None #Casa vizinha de trás e direita
        self.adir=None #Casa vizinha da frente e direita
        self.aesq=None #Casa vizinha da frente e esquerda
        #####################################################
        #'+' livre, 'b' branca, 'B' dama branca, 'p' preta, 'P' dama preta
        self.cont = BLANK
        self.posi = i
        self.posj = j
    
    #Gera as vizinhas da casa. Note que as casas na borda do tabuleiro não têm vizinhas.
    def gere_adj_desta(self,i,j):
        if j!=0 and i!=0: self.aesq=tabuleiro.casas[i-1][j-1]
        if j!=(MAX_SIZE - 1) and i!=0: self.adir=tabuleiro.casas[i-1][j+1]
        if j!=0 and i!=(MAX_SIZE - 1): self.vesq=tabuleiro.casas[i+1][j-1]
        if j!=(MAX_SIZE - 1) and i!=(MAX_SIZE - 1): self.vdir=tabuleiro.casas[i+1][j+1]

#Se sem captura disponível, encontra o caminho que uma dama pode fazer em sua 1a jogada.
#Se com captura disponível, retorna a lista de capturas possíveis. Cada elemento de tal
#lista é uma outra lista dada por [casa da peça a ser comida, casa posterior à peça a ser comida].
#Neste último caso, como a dama pode se mover para qualquer casa livre após a peça comida (se outra
#captura não estiver disponível, é claro), a lista de captura retornada deve ser tratada para
#incluir todas as casas possíveis de parada após a peça comida.
def diagonal_livre(av,avseguinte,vezseguinte):
    if av!=None: av_oc=av.cont
    else:
        av_oc='fora'
        return(2,None)
        
    if av_oc == BLANK: #Espaço à direita livre
        return(0,av)
    elif av_oc in vezseguinte:
        if avseguinte!=None:
            # Verifica se 
            if avseguinte.cont == BLANK:
                return(1,[av,avseguinte])
        return(2,None)
    else: #Peça amiga
        return(2,None)

#Lista todas as casas livres a partir de p1 (incluso) na direcção p0:p1 (p0 e p1 são casas)
def diagonal_direccional(p0,p1,forçar_p1=0):
    diagonal=[]
    while p1!=None:
        #Passar o arg forçar_p1=1 força a entrada de p1 na diagonal, mesmo se não estiver livre
        if p1.cont != BLANK and forçar_p1==0:
            return(diagonal)
        else:
            forçar_p1=0
            diagonal.append(p1)
            
            #Determina a direcção p0:p1 para adicionar a casa seguinte
            if p1==p0.adir:
                p0=p1
                p1=p1.adir
            elif p1==p0.vdir:
                p0=p1
                p1=p1.vdir
            elif p1==p0.aesq:
                p0=p1
                p1=p1.aesq
            elif p1==p0.vesq:
                p0=p1
                p1=p1.vesq
    return(diagonal)

#Função que rege a dama sem que ela tenha feito captura alguma até o momento.
#lcaptura: Lista de capturas possíveis, se houver.
#llivre: Lista de movimentos possíveis se não houver captura disponível.
#lrcaptura: Lista de capturas possíveis, se houver, com *todas* as casas de parada possíveis.
def move_dama(tabuleiro,peça,vezseguinte):
    lcaptura=[];llivre=[];fim=[0,0,0,0];ret=[None,None,None,None]
    ad=peça.adir;ae=peça.aesq;vd=peça.vdir;ve=peça.vesq
    if ad!=None: viz0=[ad,ad.adir]
    else:        viz0=[None,None]
    if ae!=None: viz1=[ae,ae.aesq]
    else:        viz1=[None,None]
    if vd!=None: viz2=[vd,vd.vdir]
    else:        viz2=[None,None]
    if ve!=None: viz3=[ve,ve.vesq]
    else:        viz3=[None,None]
    viz=[viz0,viz1,viz2,viz3]
    
    #Varre as quatro diagonais emanando da dama. Para quando obstruída por uma peça ou pela borda
    #do tabuleiro.
    for z in range(4):
        fim[z],ret[z]=diagonal_livre(viz[z][0],viz[z][1],vezseguinte)
        
        if fim[z]==1: lcaptura.append(ret[z])
            
        while (fim[z]==0): #Enquanto não encontrar obstrução, continue varrendo.
            fim[z],ret[z]=diagonal_livre(viz[z][0],viz[z][1],vezseguinte)
            if viz[z][1]==None and fim[z]==0: #Obstrução: Fim do tabuleiro
                llivre.append(ret[z])
                break
            elif fim[z]==0: #Sem obstrução. Determina a direcção viz[z][0]:viz[z][1]
                if viz[z][1]==viz[z][0].adir:
                    viz[z][0]=viz[z][1]
                    viz[z][1]=viz[z][1].adir
                elif viz[z][1]==viz[z][0].vdir:
                    viz[z][0]=viz[z][1]
                    viz[z][1]=viz[z][1].vdir
                elif viz[z][1]==viz[z][0].aesq:
                    viz[z][0]=viz[z][1]
                    viz[z][1]=viz[z][1].aesq
                elif viz[z][1]==viz[z][0].vesq:
                    viz[z][0]=viz[z][1]
                    viz[z][1]=viz[z][1].vesq
            
                llivre.append(ret[z])
            
            elif fim[z]==1: #Obstrução: Peça inimiga capturável
                lcaptura.append(ret[z])
 
    if 1 in fim: #Há ao menos uma captura disponível
        lrcaptura=[]
        maiscaptura=0 #0 se não há captura dupla, 1 cc.
        for dupla in lcaptura:
            p0=dupla[0];p1=dupla[1] #p0 é a peça a ser capturada
            dd=diagonal_direccional(p0,p1,1) #Determine as casas livres após a captura
            #Para cada casa livre após a captura, averigue se adjacente a ela há alguma peça
            #inimiga capturável. Se sim, haverá captura dupla.
            for y in range(len(dd)):
                if detectar_inimigo(tabuleiro,dd[y],p0,vezseguinte)!=[]:
                    maiscaptura=1 #Bandeira de captura dupla activada
                    lrcaptura.append([p0,dd[y]])
        if maiscaptura: #Haverá captura dupla após esta captura
            return(lrcaptura,1)
        else: #Não havendo captura dupla, a dama pode parar em qualquer casa após a captura.
            for dupla in lcaptura:
                p0=dupla[0];p1=dupla[1]
                dd=diagonal_direccional(p0,p1,1)
                for y in range(len(dd)):
                    lrcaptura.append([p0,dd[y]])
            return(lrcaptura,1)

    else:
        return(llivre,2) #Não há captura disponível

#Acha as possibilidades de movimento de uma peça ordinária
def move_ordinaria(tabuleiro,peça,vezseguinte):
    lcaptura=detectar_inimigo(tabuleiro,peça,0,vezseguinte)
    if lcaptura!=[]: return(lcaptura,1) #Peça tem pelo menos uma captura
    
    d=peça.adir
    e=peça.aesq
    
    #Teste se a peça está na periferia do tabuleiro
    if d!=None:
        d_oc = d.cont
    else:
        d_oc = 'fora'
    if e!=None:
        e_oc = e.cont
    else:
        e_oc = 'fora'
    
    llivre=[]
    # Verifica se existe espaço livre
    if d_oc == BLANK: #Espaço à direita livre
        llivre.append(d)
    if e_oc == BLANK: #Espaço à esquerda livre
        llivre.append(e)
    
    if llivre!=[]: return(llivre,2) #Peça pode andar, mas sem captura
    
    return([],0) #Peça imobilizada

def dobradinha(tabuleiro,peça,vezseguinte):
    #Se tiver chegado à última fileira, transforme a peça em dama
    if peça.aesq==None and peça.adir==None:
        # Verifica se a peça que chegou na última fileira é branca
        if peça.cont == WHITE_PIECE:
            peça.cont = WHITE_PIECE_CHECK
        # Verifica se a peça que chegou na última fileira é preta
        if peça.cont == BLACK_PIECE:
            peça.cont = BLACK_PIECE_CHECK
        
    return(detectar_inimigo(tabuleiro,peça,0,vezseguinte))

#Detecta se peça inimiga nas adjacências imediatas pode ser capturada.
#O argumento bloqueada é passado em caso de uma dama estar calculando captura dupla. Tal argumento
#representa a peça que será eliminada na primeira captura, bloqueando-a e assim evitando que a
#função considere o movimento de volta como uma possível captura dupla.
def detectar_inimigo(tabuleiro,peça,bloqueada,vezseguinte):
    ad=peça.adir
    ae=peça.aesq
    ve=peça.vesq
    vd=peça.vdir
    
    foul=vezseguinte[0] #Ordinária oponente
    FOUL=vezseguinte[1] #Dama oponente
    #Teste se a peça está na periferia do tabuleiro ou se está bloqueada
    if ad!=None and ad!=bloqueada: ad_oc=ad.cont
    else: ad_oc='fora'
    if ae!=None and ae!=bloqueada: ae_oc=ae.cont
    else: ae_oc='fora'
    if vd!=None and vd!=bloqueada: vd_oc=vd.cont
    else: vd_oc='fora'
    if ve!=None and ve!=bloqueada: ve_oc=ve.cont
    else: ve_oc='fora'
    
    lcaptura=[]
    #Há peça inimiga adjacente? Pode ser capturada?
    if ad_oc==foul or ad_oc==FOUL:
        if ad.adir!=None:
            if ad.adir.cont == BLANK: #Captura disponível à direita
                lcaptura.append([ad,ad.adir])
    if ae_oc==foul or ae_oc==FOUL:
        if ae.aesq!=None:
            if ae.aesq.cont == BLANK: #Caputra disponível à esquerda
                lcaptura.append([ae,ae.aesq])
    if vd_oc==foul or vd_oc==FOUL:
        if vd.vdir!=None:
            if vd.vdir.cont == BLANK: #Captura disponível à direita
                lcaptura.append([vd,vd.vdir])
    if ve_oc==foul or ve_oc==FOUL:
        if ve.vesq!=None:
            if ve.vesq.cont == BLANK: #Caputra disponível à esquerda
                lcaptura.append([ve,ve.vesq])
    return(lcaptura)

#Cria a lista de jogadas possíveis para o jogador com a vez
def calcule_jogadas(tabuleiro,vez,vezseguinte,apenas_calcule1):
    jogadasord=[];jogadascapt=[]
    bandeiramor=0 #Indica se há captura disponível para a cor da vez

    if apenas_calcule1: #Caso em que há dobradinha: Apenas a peça que comeu deve se mover de novo.
        peça=apenas_calcule1
        if peça.cont==vez[0]: lista,bandeira=move_ordinaria(tabuleiro,peça,vezseguinte)
        elif peça.cont==vez[1]: lista,bandeira=move_dama(tabuleiro,peça,vezseguinte)
        for n in range(len(lista)):
            jogadascapt.append([peça,lista[n]])
        return(jogadascapt,1)
    
    #Varre o tabuleiro inteiro a procura de peças da cor da vez
    for i in range(tabuleiro.lado):
        for j in range(tabuleiro.lado):
            if (i+j)%2!=0:
                casa=tabuleiro.casas[i][j]
                if casa.cont==vez[0] or casa.cont==vez[1]:
                    peça=casa #Esta casa contém uma peça da cor da vez
                    if casa.cont==vez[0]: lista,bandeira=move_ordinaria(tabuleiro,peça,vezseguinte)
                    if casa.cont==vez[1]: lista,bandeira=move_dama(tabuleiro,peça,vezseguinte)
                
                    #Há captura disponível
                    if bandeira==1:
                        bandeiramor=1
                        for n in range(len(lista)):
                            jogadascapt.append([peça,lista[n]])
                    
                    #Há movimento disponível
                    elif bandeira==2:
                        for n in range(len(lista)):
                            jogadasord.append([peça,lista[n]])
                            
    if bandeiramor: return(jogadascapt,bandeiramor) #Alguma peça da vez pode capturar
    else: return(jogadasord,bandeiramor)

#Imprime as jogadas possíveis na saída padrão
def imprima_jogadas(lista,bandeiramor):
    print("\n    Origem | Destino")
    print("ID :  i j  |   i j")
    if bandeiramor:
        for i in range(len(lista)):
            print(format(i,'02'),':',lista[i][0].posi,lista[i][0].posj,'  |  ',
            lista[i][1][1].posi,lista[i][1][1].posj)
    else:
        for i in range(len(lista)):
            print(format(i,'02'),':',lista[i][0].posi,lista[i][0].posj,'  |  ',
            lista[i][1].posi,lista[i][1].posj)
    print()

#Trata a entrada do usuário para que seleccione uma jogada válida ou abandone o jogo
def escolha_jogada(número_de_jogadas):
    while 1:
        try:
            x=int(input("Digite o ID da jogada que quer fazer ou -1 para sair: "))
        except:
            print("Você deve digitar um inteiro!")
            continue
        if x<número_de_jogadas and x>=0:
            return(x)
        elif x==-1:
            print("Saída forçada")
            exit()
        else:
            print("Movimentação não existe. Tente novamente.")
            
def jogada_aleatoria(número_de_jogadas):
    return(random.randint(0,número_de_jogadas-1))
    
##############################################################################################
#Função cerne. O cont_empate é iniciado se só houver damas no tabuleiro e aí é incrementado a
#cada jogada sem captura. Se chegar a 20, é declarado empate.
def jogue(tabuleiro,vez,cont_empate=0,apenas_calcule1=0):
    
    invert=True
    print("Placar (brancas x pretas): ",tabuleiro.brancas," x ",tabuleiro.pretas)
    if (vez=='bB'):
        print(" >| Vez das brancas   |")
        vezseguinte='pP'
    else:
        print(" >| Vez das pretas    |")
        vezseguinte='bB'
    tabuleiro.imprima()
    
    #Calcula possíveis jogadas e determina se o jogo findou
    if tabuleiro.brancas==0 or tabuleiro.pretas==0:
        print("#############\n#Fim de jogo#\n#############")
        return
    jogadas,bandeira=calcule_jogadas(tabuleiro,vez,vezseguinte,apenas_calcule1)
    apenas_calcule1=0
    if jogadas==[] or cont_empate==20:
        print("########\n#Empate#\n########")
        return

    print("\nJogadas disponíveis:")
    imprima_jogadas(jogadas,bandeira)
    
    if vez == 'bB':
        x=escolha_jogada(len(jogadas)) #Jogador, escolha uma jogada
    else:
        x=jogada_aleatoria(len(jogadas)) #Computador, jogue aleatòriamente
        time.sleep(1.5) #Apenas finge que o computador está pensando
        
    if bandeira: #Captura
        cont_empate=0
        jogada=jogadas[x]
        casaant=jogada[0]
        retirar=jogada[1][0]
        casadep=jogada[1][1]
        
        casadep.cont=jogada[0].cont
        casaant.cont = BLANK
        retirar.cont = BLANK
        
        if vez=='bB': tabuleiro.pretas-=1
        else: tabuleiro.brancas-=1
        
        if dobradinha(tabuleiro,casadep,vezseguinte)!=[]:
            # Indica que o tabuleiro não deve ser invertido
            invert=False
            # Necessário porque a vez continua a mesma na próxima rodada
            vezseguinte=vez 
            #Na próxima vez, apenas considera esta peça porque é dobradinha
            apenas_calcule1=casadep
            print("###########################")
            print("#Outra captura disponível!#")
            print("###########################")
        
    else: #Sem captura
        jogada=jogadas[x]
        casaant=jogada[0]
        casadep=jogada[1]
        casadep.cont=jogada[0].cont
        casaant.cont = BLANK
        if tabuleiro.qso_damas(): cont_empate+=1

    tabuleiro.verifique_dama(vez)
    if invert:
        tabuleiro.inverta()
    jogue(tabuleiro,vezseguinte,cont_empate,apenas_calcule1)

tabuleiro=Tabuleiro(MAX_SIZE)
tabuleiro.gere_casas()
jogue(tabuleiro,'bB')