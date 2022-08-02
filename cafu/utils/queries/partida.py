import requests as r
from html2json import collect
import json
from bs4 import BeautifulSoup

def sem_espaco(string):
    s=[]
    i=0
    j=0
    stop =False
    while not stop:
        
        while string[i] == ' ' and not stop:
            if i < len(string)-1:
                i += 1
            if i == len(string)-1:
                stop=True
        
        s.append('')
        
        while string[i] != ' ' and not stop:
            s[j] = s[j]+string[i]
            if i < len(string)-1:
                i += 1
            if i==len(string)-1:
                if string[i] != ' ':
                    s[j] = s[j]+string[i]
                stop=True
        j +=1
    return s

def padrao(p,string):
    
    ind = []
    i=0
    while i+len(p) <= len(string): 
        if string[i:i+len(p)] == p:
            ind.append([i,i+len(p)])
        i += 1
    return ind

def padrao_inicio_fim(inicio,fim,string):
    padrao1 = padrao(inicio,string)
    padrao2 = padrao(fim,string)
    
    padraoif = []
    
    padrao1.append([len(string),len(string)])
    for p2 in padrao2:
        for i in range(len(padrao1)-1):
            if p2[0]>=padrao1[i][0] and p2[1]<=padrao1[i+1][0] :
                if (len(padraoif)>0 and padrao1[i][0]>padraoif[len(padraoif)-1][0]) or len(padraoif)==0:
                    padraoif.append([padrao1[i][0],p2[1]])
    return padraoif

def mes(x): 
    
    dict_mes = {'Janeiro': 1,
                'Fevereiro': 2,
                'Março': 3,
                'Abril': 4, 
                'Maio': 5,
                'Junho': 6,
                'Julho': 7,
                'Agosto': 8,
                'Setembro': 9,
                'Outubro': 10,
                'Novembro': 11,
                'Dezembro': 12
               }
    
    return dict_mes[x]

####################################

def jogadores_inscritos(jogo_id): 
    """
    Retorna todos os jogadores inscritos para a partida.
    """
    
    req = r.get("https://www.espn.com.br/futebol/escalacoes?jogoId="+jogo_id)
    soup=BeautifulSoup(req.content, 'html.parser')
    st=soup.prettify()
    abt=sem_espaco(st)
    
    s=padrao_inicio_fim(['<span','class="name">\n','<a'],['</a>\n'],abt)
    
    # Buscar em qual índice ocorre a mudança, dos jogadores do time da casa, para os jogadores do time visitante.
    abt0=abt[s[0][0]:s[len(s)-1][1]] 
    ind_change=padrao(['class="name">\n\t\t\t\n\t\t\t<span'],abt0)[0][0]+s[0][0]
    
    player=[]
    for q in range(len(s)):
        abt1=abt[s[q][0]+5:s[q][1]-1]
        abt1
        jogador = ''
        for x in abt1:
            jogador = jogador + ' ' + x
    
        jogador=jogador[1:-1]

        i=0
        stop=False
        while not stop:
            try:
                camisa=int(abt[s[q][0]-i][:-1])
            except:
                camisa=None
            if i==8 or camisa != None:
                stop = True
            i+=1
    
        abt1=abt[s[q][0]-8:s[q][0]]
        v=padrao_inicio_fim(['class="detail">\n'],['</span>\n'],abt1)
        try:
            tempo_substituicao=int(abt1[v[0][0]+1][:-2])
        except:
            try:
                tempo_substituicao=int(abt1[v[0][0]+1][:-5])
            except:
                tempo_substituicao=0
        
        if s[q][0] < ind_change:
            time = 'casa'
        else:
            time = 'visitante'
        
        player.append([jogador, camisa, tempo_substituicao, time])
    
    jogadores_casa_0=[x[:-1] for x in player if x[-1] == 'casa']
    jogadores_visitante_0=[x[:-1] for x in player if x[-1] == 'visitante']
    
    return jogadores_casa_0, jogadores_visitante_0

# Funções auxiliares da função: requisicao_gols

def teste_gols(jogo_id): 
    """
    Retorna se o time da casa e o time visitante, marcaram gols.
    """
    
    req = r.get("https://www.espn.com.br/futebol/escalacoes?jogoId="+jogo_id)
    soup=BeautifulSoup(req.content, 'html.parser')
    st=soup.prettify()
    abt=sem_espaco(st)
    
    te=padrao_inicio_fim(['<ul',
    'class="goal',
    'icon-font-before',
    'icon-soccer-ball-before',
    'icon-soccerball"',
    'data-event-type="goal">\n',
    '<li>\n'],['</ul>\n'],abt)
    
    teste_casa=False
    teste_visitante=False
    if len(te)==2:
        teste_casa=True
        teste_visitante=True
    elif len(te)==1:
        if abt[te[0][0]-2][:]=='data-home-away="home"':
            teste_casa=True
        else:
            teste_visitante=True
            
    return teste_casa, teste_visitante


def gols_casa_visitante(q, jogo_id): 
    """
    Retorna os dados da função requisição_gols, para q={0, 1}. 
    Se ambos os times marcaram: q=0 representa time da casa, q=1 representa time visitante. 
    Se apenas um time marcou, q=0 represente este time, q=1 gera erro. Se nenhum time marcou, q=0 e q=1 geram erro.
    """
    
    req = r.get("https://www.espn.com.br/futebol/escalacoes?jogoId="+jogo_id)
    soup=BeautifulSoup(req.content, 'html.parser')
    st=soup.prettify()
    abt=sem_espaco(st)

    te=padrao_inicio_fim(['<ul',
    'class="goal',
    'icon-font-before',
    'icon-soccer-ball-before',
    'icon-soccerball"',
    'data-event-type="goal">\n',
    '<li>\n'],['</ul>\n'],abt)
        
    abt_q_1=abt[te[q][0]:te[q][1]]
    te_q=padrao_inicio_fim(['<span>\n'],['</span>\n'],abt_q_1)
    te1=padrao_inicio_fim(['<li>\n'],['<span>\n'],abt_q_1)
        
    gols_q = []
    for q in range(len(te1)):
        jogador_gol=''
        for x in abt_q_1[te1[q][0]:te1[q][1]][1:-1]:
            jogador_gol = jogador_gol + ' ' + x

        jogador_gol = jogador_gol[1:-1]
        gols_q.append({'jogador': jogador_gol, 'minutos_gols':[]})
        
    
    numeros=('0','1','2','3','4','5','6','7','8','9','10')
    minuto_q=[]
    for i in range(len(te_q)):
        for j in range(len(abt_q_1[te_q[i][0]+1:te_q[i][1]-1])):
            
            min_valido = False
            
            if j>0:
                minuto_q_0 = '('+abt_q_1[te_q[i][0]+1:te_q[i][1]-1][j]
            else:
                minuto_q_0 = abt_q_1[te_q[i][0]+1:te_q[i][1]-1][j]
                
            if minuto_q_0[1:3][1] == "'":
                minuto = minuto_q_0[1:3][0]
                if minuto in numeros:
                    min_valido = True
            else: 
                minuto = minuto_q_0[1:3]
                if minuto[0] in numeros and minuto[1] in numeros:
                    min_valido = True
                    
            if min_valido:
                gols_q[i]['minutos_gols'].append(int(minuto))                
                
    return gols_q