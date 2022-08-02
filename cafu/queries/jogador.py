import time
from cafu.utils.string import convert_str_var_time
from cafu.utils.queries.webdriver_chrome import WebdriverChrome
from cafu.metadata.paths import path

import logging
filename = path('logs_cafu')+'/logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

class AtuacoesJogador(WebdriverChrome):
    """
    Extrai informações do desempenho do jogador no atual campeonato disputado
    
    Args:
        id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/_/id/<id_jogador>. 
                          Ex <id_jogador>='199017/everton-ribeiro'
        headless: (bool) se o navegador será mostrado ou não
    """
    
    def __init__(self, id_jogador, headless=True):
        super().__init__(headless=headless)
        self.get_atuacoes_jogador(id_jogador)
        self.id_jogador = id_jogador

    def _x_path(self, pos_v, pos_h, section=2):
        """
        Método interno da classe.
        Define o xpath do método find_element_by_xpath da biblioteca selenium, para a busca de uma informação em um jogo
        
        .. figure:: ../../../imagens_doc/atuacoes_jogador.png
        
        Args:
            pos_v: (int) posição horizontal da informação na tabela, referente a coluna 
            pos_h: (int) posição vertical da informação na tabela, referente ao jogo (1-último, 2-penultimo, ...)
        Returns:
            str: xpath 
        """
        
        response = (f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/div[1]/div/div[2]/'
                    f'div[2]/div/div/div/div/div[2]/table/tbody/tr[{pos_h}]/td[{pos_v}]')
        return response 
    
    def campeonato(self):
        """
        Returns:
            str: campeonato em que o jogador atua
        """
        
        init = time.time()
        
        xpath = '//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/div[1]/div/div[2]/div[1]'
        try:
            response = self.web.find_element_by_xpath(xpath).text
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.AtuacoesJogador.campeonato: Unexpected error: "
                          f"Could not execute function. <id_jogador>={self.id_jogador}. runtime = {runtime_str}")
            logging.error(err)

            return
        
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.info(f"SUCCESS queries.jogador.AtuacoesJogador.campeonato: Function executed successfully. "
                     f"<id_jogador>={self.id_jogador}. runtime = {runtime_str}")
        
        return response
    
    def date(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            str: data da partida 
        """
        
        init = time.time()
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(1,jogo)).text
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.AtuacoesJogador.date: Unexpected error: "
                          f"Could not execute function. <id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
            logging.error(err)

            return
        
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.info(f"SUCCESS queries.jogador.AtuacoesJogador.date: Function executed successfully. "
                     f"<id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
        
        return response
    
    def casa_fora(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            str: se o jogo foi em casa ou fora
        """
        
        init = time.time()
        
        try:
            identificador = self.web.find_element_by_xpath(self._x_path(2,jogo)).text.split('\n')[0]
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.AtuacoesJogador.casa_fora: Unexpected error: "
                          f"Could not execute function. <id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
            logging.error(err)    
            return
        
        if identificador == 'x':
            response = 'casa'
        elif identificador == 'em':
            response = 'fora'
        else:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.AtuacoesJogador.casa_fora: Unexpected error: "
                          f"identificador not in (x, em). <id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")  
            return
        
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.info(f"SUCCESS queries.jogador.AtuacoesJogador.casa_fora: Function executed successfully. "
                     f"<id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
        
        return response
    
    def adversario(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            str: time adversário
        """
        
        init = time.time()
        
        try:
            response = self.web.find_element_by_xpath(self._x_path(2,jogo)).text.split('\n')[1]
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.AtuacoesJogador.adversario: Unexpected error: "
                          f"Could not execute function. <id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
            logging.error(err)

            return
        
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.info(f"SUCCESS queries.jogador.AtuacoesJogador.adversario: Function executed successfully. "
                     f"<id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
        
        return response
    
    def resultado(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            dict: resultado (V, E, D), placar
        """
        
        init = time.time()
        
        try:
            info = self.web.find_element_by_xpath(self._x_path(3,jogo)).text.split('\n')
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.AtuacoesJogador.resultado: Unexpected error: "
                          f"Could not execute function. <id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
            logging.error(err)

            return
        
        try:
            response = {'resultado': info[0], 'placar':info[1]}
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS queries.jogador.AtuacoesJogador.resultado: Function executed successfully. "
                         f"<id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
            
            return response
        except:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.AtuacoesJogador.resultado: Unexpected error: split method. "
                          f"<id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
            
            return
    
    def gols(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de gols marcados pelo jogador
        """
        
        init = time.time()
        
        try:
            response = int(self.web.find_element_by_xpath(self._x_path(4,jogo)).text)
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.AtuacoesJogador.gols: Unexpected error: "
                          f"Could not execute function. <id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
            logging.error(err)

            return
        
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.info(f"SUCCESS queries.jogador.AtuacoesJogador.gols: Function executed successfully. "
                     f"<id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
        
        return response
    
    def assistencias(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de assistências feitas pelo jogador
        """
        
        init = time.time()
        
        try:
            response = int(self.web.find_element_by_xpath(self._x_path(5,jogo)).text)
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.AtuacoesJogador.assistencias: Unexpected error: "
                          f"Could not execute function. <id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
            logging.error(err)

            return
        
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.info(f"SUCCESS queries.jogador.AtuacoesJogador.assistencias: Function executed successfully. "
                     f"<id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
        
        return response
    
    def finalizacoes(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de finalizações feitas pelo jogador
        """
        
        init = time.time()
        
        try:
            response = int(self.web.find_element_by_xpath(self._x_path(6,jogo)).text)
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.AtuacoesJogador.finalizacoes: Unexpected error: "
                          f"Could not execute function. <id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
            logging.error(err)

            return
            
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.info(f"SUCCESS queries.jogador.AtuacoesJogador.finalizacoes: Function executed successfully. "
                     f"<id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
        
        return response
        
    def finalizacoes_no_gol(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de finalizações no gol, feitas pelo jogador
        """
        
        init = time.time()
        
        try:
            response = int(self.web.find_element_by_xpath(self._x_path(7,jogo)).text)
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.AtuacoesJogador.finalizacoes_no_gol: "
                          f"Unexpected error: Could not execute function. <id_jogador>={self.id_jogador}, "
                          f"<jogo>={jogo}. runtime = {runtime_str}")
            logging.error(err)

            return
        
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.info(f"SUCCESS queries.jogador.AtuacoesJogador.finalizacoes_no_gol: Function executed successfully. "
                     f"<id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
        
        return response
    
    def faltas_cometidas(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de faltas cometidas pelo jogador
        """
        
        init = time.time()
        
        try:
            response = int(self.web.find_element_by_xpath(self._x_path(8,jogo)).text)
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.AtuacoesJogador.faltas_cometidas: "
                          f"Unexpected error: Could not execute function. <id_jogador>={self.id_jogador}, "
                          f"<jogo>={jogo}. runtime = {runtime_str}")
            logging.error(err)

            return
            
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.info(f"SUCCESS queries.jogador.AtuacoesJogador.faltas_cometidas: Function executed successfully. "
                     f"<id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
        
        return response
    
    def faltas_sofridas(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de faltas sofridas pelo jogador
        """
        
        init = time.time()
        
        try:
            response = int(self.web.find_element_by_xpath(self._x_path(9,jogo)).text)
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.AtuacoesJogador.faltas_sofridas: "
                          f"Unexpected error: Could not execute function. <id_jogador>={self.id_jogador}, "
                          f"<jogo>={jogo}. runtime = {runtime_str}")
            logging.error(err)

            return
            
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.info(f"SUCCESS queries.jogador.AtuacoesJogador.faltas_sofridas: Function executed successfully. "
                     f"<id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
        
        return response
    
    def impedimentos(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de impedimentos do jogador
        """
        
        init = time.time()
        
        try:
            response = int(self.web.find_element_by_xpath(self._x_path(10,jogo)).text)
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.AtuacoesJogador.impedimentos: "
                          f"Unexpected error: Could not execute function. <id_jogador>={self.id_jogador}, "
                          f"<jogo>={jogo}. runtime = {runtime_str}")
            logging.error(err)

            return
            
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.info(f"SUCCESS queries.jogador.AtuacoesJogador.impedimentos: "
                     f"Function executed successfully. <id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
        
        return response
    
    def cartoes_amarelos(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de cartões amarelos levados pelo jogador
        """
        
        init = time.time()
        
        try:
            response = int(self.web.find_element_by_xpath(self._x_path(11,jogo)).text)
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.AtuacoesJogador.cartoes_amarelos: "
                          f"Unexpected error: Could not execute function. <id_jogador>={self.id_jogador}, "
                          f"<jogo>={jogo}. runtime = {runtime_str}")
            logging.error(err)

            return
            
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.info(f"SUCCESS queries.jogador.AtuacoesJogador.cartoes_amarelos: "
                     f"Function executed successfully. <id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
        
        return response
    
    def cartoes_vermelhos(self, jogo):
        """
        Args:
            jogo: (int) jogo (1-último, 2-penultimo, ...)
        Returns:
            int: quantidade de cartões vermelhos levados pelo jogador
        """
        
        init = time.time()
        
        try:
            response = int(self.web.find_element_by_xpath(self._x_path(12,jogo)).text)
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.AtuacoesJogador.cartoes_vermelhos: "
                          f"Unexpected error: Could not execute function. <id_jogador>={self.id_jogador}, "
                          f"<jogo>={jogo}. runtime = {runtime_str}")
            logging.error(err)

            return
            
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.info(f"SUCCESS queries.jogador.AtuacoesJogador.cartoes_vermelhos: "
                     f"Function executed successfully. <id_jogador>={self.id_jogador}, <jogo>={jogo}. runtime = {runtime_str}")
        
        return response
    
class Bio(WebdriverChrome):
    """
    Extrai informações da biografia do jogador
    
    Args:
        id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/bio/_/id/<id_jogador>.
                          Ex <id_jogador>='199017/everton-ribeiro'
        headless: (bool) se o navegador será mostrado ou não
    """
    
    def __init__(self, id_jogador, headless=True):
        super().__init__(headless=headless)
        self.get_bio_jogador(id_jogador)
        self.id_jogador = id_jogador

    def _x_path(self, pos):
        """
        Método interno da classe.
        Define o xpath do método find_element_by_xpath da biblioteca selenium, para a busca de uma informação de biografia
        
        .. figure:: ../../../imagens_doc/biografia.png
        
        Args:
            pos: (int) posição na tabela biografia (2-posicao, 3-altura;massa, ...)
        Returns:
            str: xpath 
        """
        
        return f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section[1]/div/div[{pos}]/div/span[2]'
    
    def time(self, pos):
        """
        Todos os times do histórico de carreira do jogador
        Args:
            pos: (int) posição na tabela "Histórico da Carreira"
        Returns:
            tuple: time do jogador, quantidade de temporadas
        """
        
        init = time.time()
        
        x_path_time = f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section[2]/div/a[{pos}]/div/span[1]'
        x_path_temps = f'//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section[2]/div/a[{pos}]/div/span[2]'
        try:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            response = self.web.find_element_by_xpath(x_path_time).text, self.web.find_element_by_xpath(x_path_temps).text
            logging.info(f"SUCCESS queries.jogador.Bio.time: Function executed successfully. "
                         f"<id_jogador>={self.id_jogador}, <pos>={pos}. runtime = {runtime_str}")
            
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.Bio.time: Unexpected error: Could not execute function. "
                          f"<id_jogador>={self.id_jogador}, <pos>={pos}. runtime = {runtime_str}")
            logging.error(err)
            
            return 
    
    def posicao(self):
        """
        Returns:
            str: posição do jogador
        """
        
        init = time.time()
        
        try:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            response = self.web.find_element_by_xpath(self._x_path(2)).text
            logging.info(f"SUCCESS queries.jogador.Bio.posicao: Function executed successfully. "
                         f"<id_jogador>={self.id_jogador}. runtime = {runtime_str}")
            
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.Bio.posicao: Unexpected error: Could not execute function. "
                          f"<id_jogador>={self.id_jogador}. runtime = {runtime_str}")
            logging.error(err)
            
            return 
    
    def altura(self):
        """
        Returns:
            str: altura do jogador
        """
        
        init = time.time()
        
        try:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            response = self.web.find_element_by_xpath(self._x_path(3)).text.split(', ')[0]
            logging.info(f"SUCCESS queries.jogador.Bio.altura: Function executed successfully. "
                         f"<id_jogador>={self.id_jogador}. runtime = {runtime_str}")
            
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.Bio.altura: Unexpected error: Could not execute function. "
                          f"<id_jogador>={self.id_jogador}. runtime = {runtime_str}")
            logging.error(err)
            
            return 
    
    def massa(self):
        """
        Returns:
            str: massa do jogador
        """
        
        init = time.time()
        
        try:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            response = self.web.find_element_by_xpath(self._x_path(3)).text.split(', ')[1]
            logging.info(f"SUCCESS queries.jogador.Bio.massa: Function executed successfully. "
                         f"<id_jogador>={self.id_jogador}. runtime = {runtime_str}")
            
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.Bio.massa: Unexpected error: Could not execute function "
                          f"<id_jogador>={self.id_jogador}. runtime = {runtime_str}")
            logging.error(err)
            
            return 
    
    def data_nascimento(self):
        """
        Returns:
            str: data de nascimento do jogador
        """
        
        init = time.time()
        
        try:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            response = self.web.find_element_by_xpath(self._x_path(4)).text.split(' (')[0]
            logging.info(f"SUCCESS queries.jogador.Bio.data_nascimento: Function executed successfully "
                         f"<id_jogador>={self.id_jogador}. runtime = {runtime_str}")
            
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.Bio.data_nascimento: Unexpected error: Could not execute function "
                          f"<id_jogador>={self.id_jogador}. runtime = {runtime_str}")
            logging.error(err)
            
            return
    
    def nacionalidade(self):
        """
        Returns:
            str: nacionalidade do jogador
        """
        
        init = time.time()
        
        try:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            response = self.web.find_element_by_xpath(self._x_path(5)).text.split(' (')[0]
            logging.info(f"SUCCESS queries.jogador.Bio.nacionalidade: Function executed successfully "
                         f"<id_jogador>={self.id_jogador}. runtime = {runtime_str}")
            
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.jogador.Bio.nacionalidade: Unexpected error: Could not execute function "
                          f"<id_jogador>={self.id_jogador}. runtime = {runtime_str}")
            logging.error(err)
            
            return