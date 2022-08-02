import os
path_project = os.path.abspath('..')
import sys
sys.path.append(path_project)

import pandas as pd
#from cafu.utils import find_jogo_id
from cafu.queries import Partida
from cafu.metadata import path
path_save = path('dir_results')

def f():
    help_ = (
             f"""
             There are two possibilities for args:
             Args1:
                time_casa0: (str) time da casa
                time_visitante0: (str) time visitante
                campeonato: (str) chave primária do dicionário campeonatos, caminho metadata/campeonatos_espn
                temporada: (str) chave secundária do dicionário campeonatos, caminho metadata/campeonatos_espn 
             Ex: palmeiras fluminense brasil 2021-2021
             Args2:
                jogo_id: (int or str) completa o link https://www.espn.com.br/futebol/escalacoes?jogoId=<jogo_id>
             Ex: 614698
             Resultados salvos em: {path_save}/partida.csv, {path_save}/descricao_partida.csv
             """
            )
    
    args = sys.argv[1:]
    if len(args) == 0:
        print(help_)
    else:
        if len(args) == 1:
            jogo_id = args[0]
        else:
            jogo_id = find_jogo_id(*args)
        req = Partida(jogo_id)
        
        try:
            minuto = req.minuto
        except:
            minuto = 90
    
        data = [
                req.status,
                minuto,
                req.campeonato(),
                req.date,
                req.nomes_times(),
                req.formacao(),
                req.jogadores(),
                req.gols(),
                req.placar(),
                req.posse(),
                req.chutes_fora_nogol(),
                req.faltas(),
                req.cartoes_amarelos(),
                req.cartoes_vermelhos(),
                req.impedimentos(),
                req.escanteios(),
                req.defesas()
               ]
        index = [
                 'status',
                 'minuto',
                 'campeonato',
                 'data',
                 'nomes_times',
                 'formacao',
                 'jogadores',
                 'gols',
                 'placar',
                 'posse',
                 'chutes_fora_nogol',
                 'faltas',
                 'cartoes_amarelos',
                 'cartoes_vermelhos',
                 'impedimentos',
                 'escanteios',
                 'defesas'
                ]
        df = pd.DataFrame(data=data, index=index)
        try:
            df.to_csv(path_save+f'/partida/jogo_id={jogo_id}.csv')
        except:
            os.mkdir(path_save+'/partida')
            df.to_csv(path_save+f'/partida/jogo_id={jogo_id}.csv')

        minuto_a_minuto = req.minuto_a_minuto()
        df = pd.DataFrame(minuto_a_minuto)
        try:
            df.to_csv(path_save+f'/descricao_partida/jogo_id={jogo_id}.csv', index=False)
        except:
            os.mkdir(path_save+'/descricao_partida')
            df.to_csv(path_save+f'/descricao_partida/jogo_id={jogo_id}.csv', index=False)
    
if __name__=='__main__':
    f()