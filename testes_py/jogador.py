import os
path_project = os.path.abspath('..')
import sys
sys.path.append(path_project)

import pandas as pd
from cafu.queries import AtuacoesJogador, Bio
from cafu.metadata import path
path_save = path('dir_results')

def f():
    help_ = (
             f"""
             Args:
                id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/_/id/<id_jogador>. 
                jogo: (int) jogo (1-último, 2-penultimo, ...)
             Ex: 252107/vinicius-junior 1
             Resultados salvos em: {path_save}/atuacoes_jogador.csv, {path_save}/bio_jogador.csv
             """
            )
    
    args = sys.argv[1:]
    if len(args) == 0:
        print(help_)
    else:
        id_jogador = args[0]
        jogo = args[1]
        
        query = AtuacoesJogador(id_jogador)

        data = [
                query.campeonato(),
                query.date(jogo),
                query.casa_fora(jogo),
                query.adversario(jogo),
                query.resultado(jogo),
                query.gols(jogo),
                query.assistencias(jogo),
                query.finalizacoes(jogo),
                query.finalizacoes_no_gol(jogo),
                query.faltas_cometidas(jogo),
                query.faltas_sofridas(jogo),
                query.impedimentos(jogo),
                query.cartoes_amarelos(jogo),
                query.cartoes_vermelhos(jogo)
               ]

        query.web.close()

        index = [
                 'campeonato',
                 'date',
                 'casa_fora',
                 'adversario',
                 'resultado',
                 'gols',
                 'assistencias',
                 'finalizacoes',
                 'finalizacoes_no_gol',
                 'faltas_cometidas',
                 'faltas_sofridas',
                 'impedimentos',
                 'cartoes_amarelos',
                 'cartoes_vermelhos'
                ]

        df = pd.DataFrame(data=data, index=index)
        try:
            id_jogador1 = id_jogador.replace('/','')
            df.to_csv(path_save+f'/atuacoes_jogador/id_jogador={id_jogador1}_jogo={jogo}.csv')
        except:
            os.mkdir(path_save+'/atuacoes_jogador')
            df.to_csv(path_save+f'/atuacoes_jogador/id_jogador={id_jogador1}_jogo={jogo}.csv')

        query = Bio(id_jogador)

        data = [
                query.time(1)[0],
                query.time(1)[1],
                query.posicao(),
                query.altura(),
                query.massa(),
                query.data_nascimento(),
                query.nacionalidade()
               ]

        query.web.close()

        index = [
                 'time',
                 'qt_temporadas',
                 'posicao',
                 'altura',
                 'massa',
                 'data_nascimento',
                 'nacionalidade'
                 ]

        df = pd.DataFrame(data=data, index=index)
        try:
            id_jogador1 = id_jogador.replace('/','')
            df.to_csv(path_save+f'/bio_jogador/id_jogador={id_jogador1}_jogo={jogo}.csv')
        except:
            os.mkdir(path_save+'/bio_jogador')
            df.to_csv(path_save+f'/bio_jogador/id_jogador={id_jogador1}_jogo={jogo}.csv')
    
if __name__=='__main__':
    f()