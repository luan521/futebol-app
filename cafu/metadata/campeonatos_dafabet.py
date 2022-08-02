dict_id_campeonato = {
                      'alemanha': '23404-germany/23405-bundesliga',
                      'brasil': '22977-brazil/22980-brasileiro-serie-a',
                      'espanha': '22925-spain/23034-laliga',
                      'franca': '23168-france/23169-ligue-1',
                      'inglaterra': '23025-england/23132-premier-league',
                      'italia': '23375-italy/23454-serie-a',
                     }

def campeonato_dafabet(campeonato=None):
    """
    Args:
        campeonato: (str) chave do dicionário dict_id_campeonato
    Returns:
        str or dict: completa o link https://www.dafabet.com/pt/dfgoal/sports/240-football/<id_campeonato>. 
        Ex <campeontato>='brasil-a -> '<id_campeonato>=''22977-brazil/22980-brasileiro-serie-a''.
        Se <campeonato>=None, retorna <dict_id_campeonato>
    """
    
    if campeonato is None:
        return dict_id_campeonato
    else:
        return dict_id_campeonato[campeonato]