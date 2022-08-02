import os
path_project = os.path.abspath('..')
import sys
sys.path.append(path_project)

import json
from cafu.queries import GetOdds
from cafu.metadata import path
path_save = path('dir_results')

def f():
    help_ = (
             f"""
             Args:
                 campeonato: (str) chave do dicionário dict_id_campeonato, caminho metadata/campeonatos_dafabet
                 index: (int) Posição que o jogo aparece no site Dafabet
             Ex: franca 0
             Resultado salvo em: {path_save}/odds.json
             """
            )
    
    args = sys.argv[1:]
    if len(args) == 0:
        print(help_)
    else:
        campeonato = args[0]
        index = int(args[1])
        
        query = GetOdds()
        query.get_campeonato_dafabet(campeonato)
        query.join_link_odds_partida(index)
        query.open_odds()
        odds = query.get_odds()

        query.web.close() # encerra a sessão
        
        try:
            with open(path_save+f'/odds/campeonato={campeonato}_index={index}.json', 'w') as fp:
                json.dump(odds, fp)
        except:
            os.mkdir(path_save+'/odds')
            with open(path_save+f'/odds/campeonato={campeonato}_index={index}.json', 'w') as fp:
                json.dump(odds, fp)
        
if __name__=='__main__':
    f()