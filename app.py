# import main Flask class and request object
from flask import Flask, request
from cafu.queries import Partida, AtuacoesJogador, Bio, GetOdds

# create the Flask app
app = Flask(__name__)

@app.route('/partida')
def partida():
    """
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
    """    
    
    jogo_id = request.args.get('jogo_id')
    req = Partida(jogo_id)
        
    try:
        minuto = req.minuto
    except:
        minuto = 90
    
    data = {
            'status': req.status,
            'minuto': minuto,
            'campeonato': req.campeonato(),
            'data': req.date,
            'nomes_times': req.nomes_times(),
            'formacao': req.formacao(),
            'jogadores': req.jogadores(),
            'gols': req.gols(),
            'placar': req.placar(),
            'posse': req.posse(),
            'chutes_fora_nogol': req.chutes_fora_nogol(),
            'faltas': req.faltas(),
            'cartoes_amarelos': req.cartoes_amarelos(),
            'cartoes_vermelhos': req.cartoes_vermelhos(),
            'impedimentos': req.impedimentos(),
            'escanteios': req.escanteios(),
            'defesas': req.defesas()
           }

    return data

@app.route('/partida/minuto_a_minuto')
def partida_minuto_a_minuto():
    """
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
    """    
    
    jogo_id = request.args.get('jogo_id')
    req = Partida(jogo_id)
    data = req.minuto_a_minuto()
    
    return data

@app.route('/jogador/partida')
def jogador_partida():
    """
    Args:
       id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/_/id/<id_jogador>. 
       jogo: (int) jogo (1-último, 2-penultimo, ...)
    Ex: 252107/vinicius-junior 1
    """
        
    id_jogador = request.args.get('id_jogador')
    jogo = request.args.get('jogo')    
    query = AtuacoesJogador(id_jogador)
    
    data = {
            'campeonato': query.campeonato(),
            'date': query.date(jogo),
            'casa_fora': query.casa_fora(jogo),
            'adversario': query.adversario(jogo),
            'resultado': query.resultado(jogo),
            'gols': query.gols(jogo),
            'assistencias': query.assistencias(jogo),
            'finalizacoes': query.finalizacoes(jogo),
            'finalizacoes_no_gol': query.finalizacoes_no_gol(jogo),
            'faltas_cometidas': query.faltas_cometidas(jogo),
            'faltas_sofridas': query.faltas_sofridas(jogo),
            'impedimentos': query.impedimentos(jogo),
            'cartoes_amarelos': query.cartoes_amarelos(jogo),
            'cartoes_vermelhos': query.cartoes_vermelhos(jogo)
           }

    query.web.close()

    return data

@app.route('/jogador/bio')
def jogador_bio():
    """
    Args:
       id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/_/id/<id_jogador>. 
    Ex: 252107/vinicius-junior
    """
        
    id_jogador = request.args.get('id_jogador')
    query = Bio(id_jogador)
    
    data = {
            'time': query.time(1)[0],
            'qt_temporadas': query.time(1)[1],
            'posicao': query.posicao(),
            'altura': query.altura(),
            'massa': query.massa(),
            'data_nascimento': query.data_nascimento(),
            'nacionalidade': query.nacionalidade()
           }

    query.web.close()

    return data

@app.route('/odds')
def odds():
    """
    Args:
        campeonato: (str) chave do dicionário dict_id_campeonato, caminho metadata/campeonatos_dafabet
        index: (int) Posição que o jogo aparece no site Dafabet
    Ex: franca 0
    """
    
    campeonato = request.args.get('campeonato')
    index = request.args.get('index')
    index = int(index)

    query = GetOdds()
    query.get_campeonato_dafabet(campeonato)
    query.join_link_odds_partida(index)
    query.open_odds()
    data = query.get_odds()
    
    return data
            
if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=3000)