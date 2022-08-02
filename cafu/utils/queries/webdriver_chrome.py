from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from cafu.utils.string import convert_str_var_time
from cafu.metadata.campeonatos_dafabet import campeonato_dafabet
from cafu.metadata.paths import path
path_driver = path('initial_path')+'/chromedriver'

import logging
filename = path('logs_cafu')+'/logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

class WebdriverChrome():
    """
    Inicializa a sessão do chromedriver e entra em alguns links úteis. 
    Método self.web.close() fecha a sessão do Chrome driver
    
    Args:
        start_webdriver: (bool) se o Chrome driver deve ser iniciado
        headless: (bool) se o navegador será mostrado ou não
    """
    
    def __init__(self, start_webdriver=True, headless=True):
        
        init = time.time()
        
        try:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument("--headless")
            if start_webdriver:
                self.web = webdriver.Chrome(path_driver, options=chrome_options)
                
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS utils.queries.webdriver_chrome.WebdriverChrome: "
                         f"Chromedriver started successfully. <start_webdriver>={start_webdriver}, "
                         f"<headless>={headless}. runtime = {runtime_str}")
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error("ERROR utils.queries.webdriver_chrome.WebdriverChrome: Unexpected error: "
                          f"Could started Chromedriver. <start_webdriver>={start_webdriver}, "
                          f"<headless>={headless}. runtime = {runtime_str}")
            logging.error(err)
        
    def get_atuacoes_jogador(self, id_jogador):
        """
        Entra no link para a busca das informações das atuações do jogador, buscando todo o histórico

        Args:
            id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/jogos/_/id/<id_jogador>. 
                              Ex <id_jogador>='199017/everton-ribeiro'
        """
        
        init = time.time()
        
        try:
            self.web.get(f'https://www.espn.com.br/futebol/jogador/jogos/_/id/{id_jogador}')
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS utils.queries.webdriver_chrome.WebdriverChrome.get_atuacoes_jogador: "
                         f"Function executed successfully. <id_jogador>={id_jogador}. runtime = {runtime_str}")
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR utils.queries.webdriver_chrome.WebdriverChrome.get_atuacoes_jogador: "
                          f"Unexpected error: Could not execute function. <id_jogador>={id_jogador}. runtime = {runtime_str}")
            logging.error(err)
        
    def get_bio_jogador(self, id_jogador):
        """
        Entra no link para a busca da biografia do jogador

        Args:
            id_jogador: (str) completa o link https://www.espn.com.br/futebol/jogador/bio/_/id/<id_jogador>. 
                              Ex <id_jogador>='199017/everton-ribeiro'
        """
        
        init = time.time()
        
        try:
            self.web.get(f'https://www.espn.com.br/futebol/jogador/bio/_/id/{id_jogador}')
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS utils.queries.webdriver_chrome.WebdriverChrome.get_bio_jogador: "
                         f"Function executed successfully. <id_jogador>={id_jogador}. runtime = {runtime_str}")
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR utils.queries.webdriver_chrome.WebdriverChrome.get_bio_jogador: "
                          f"Unexpected error: Could not execute function. <id_jogador>={id_jogador}. "
                          f"runtime = {runtime_str}")
            logging.error(err)
        
    def get_campeonato_dafabet(self, chave_campeonato):
        """
        Entra no link para a busca das odds no site Dafabet

        Args:
            chave_campeonato: (str) chave do dicionário dict_id_campeonato, caminho metadata/campeonatos_dafabet
        """
        
        init = time.time()
        
        try:
            id_campeonato = campeonato_dafabet(chave_campeonato)
            self.web.get(f'https://www.dafabet.com/pt/dfgoal/sports/240-football/{id_campeonato}')
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS utils.queries.webdriver_chrome.WebdriverChrome.get_campeonato_dafabet: "
                         f"Function executed successfully. <chave_campeonato>={chave_campeonato}. "
                         f"runtime = {runtime_str}")
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR utils.queries.webdriver_chrome.WebdriverChrome.get_campeonato_dafabet: "
                          f"Unexpected error: Could not execute function. <chave_campeonato>={chave_campeonato}. "
                          f"runtime = {runtime_str}")
            logging.error(err)
    
    def get_partida_espn(self, jogo_id):
        """
        Entra no link para o resumo da partida no site ESPN

        Args:
            jogo_id: (int or str) completa o link https://www.espn.com.br/futebol/escalacoes?jogoId=<jogo_id>. 
        """
        
        init = time.time()
        
        try:
            self.web.get(f'https://www.espn.com.br/futebol/partida/_/jogoId/{str(jogo_id)}')
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS utils.queries.webdriver_chrome.WebdriverChrome.get_partida_espn: "
                         f"Function executed successfully. <jogo_id>={jogo_id}. "
                         f"runtime = {runtime_str}")
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR utils.queries.webdriver_chrome.WebdriverChrome.get_partida_espn: "
                          f"Unexpected error: Could not execute function. <jogo_id>={jogo_id}. "
                          f"runtime = {runtime_str}")
            logging.error(err)