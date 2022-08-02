import json
from time import sleep
from cafu.utils.loop_try import loop_try
from cafu.utils.queries.webdriver_chrome import WebdriverChrome

from cafu.metadata.paths import path
import os
user, password = os.getenv('dafabet_user'), os.getenv('dafabet_password')

import logging
filename = path('logs_cafu')+'\\logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

class Login(WebdriverChrome):
    """
    Faz o login no site Dafabet
    
    Args:
        start_webdriver: (bool) se o Chrome driver deve ser iniciado
        headless: (bool) se o navegador será mostrado ou não
    """
    
    def __init__(self, start_webdriver=True, headless=True):
        super().__init__(start_webdriver, headless)
        
    def login(self):
        """
        Faz o login no site Dafabet
        """
        
        # css selector
        user_path = '#LoginForm_username'
        password_path = '#LoginForm_password'
        enter_button_path = '#LoginForm_submit'

        try:
            # get elements
            user_element = self.web.find_element_by_css_selector(user_path)
            password_element = self.web.find_element_by_css_selector(password_path)
            enter_button_element = self.web.find_element_by_css_selector(enter_button_path)

            # send values
            user_element.send_keys(user)
            password_element.send_keys(password)
            enter_button_element.click()
            
            logging.info("SUCCESS utils.queries.dafabet.Login.login: "
                         "Function executed successfully")
        except Exception as err:
            logging.error("ERROR utils.queries.dafabet.Login.login: Unexpected error: "
                          "Could not execute function")
            logging.error(err)
        
class TrafficOddsPartida(Login):
    """
    Tráfego entre as partidas de um campeonato
    
    Args:
        start_webdriver: (bool) se o Chrome driver deve ser iniciado
        headless: (bool) se o navegador será mostrado ou não
    """
    
    def __init__(self, start_webdriver=True, headless=True):
        super().__init__(start_webdriver, headless)
        
    def get_quantidade_partidas(self):
        """
        Returns:
            int: Quantidade de partidas no campeonato
        """
        
        try:
            partidas = self.web.find_elements_by_class_name('more_markets')
            response = len(partidas)
            
            if response > 0:
                logging.info("SUCCESS utils.queries.dafabet.TrafficOddsPartida.get_quantidade_partidas: "
                             "Function executed successfully")
            else:
                logging.warning("WARNING utils.queries.dafabet.TrafficOddsPartida.get_quantidade_partidas: "
                                "No matches found")
            
            return response
        except Exception as err:
            logging.error("ERROR utils.queries.dafabet.TrafficOddsPartida.get_quantidade_partidas: "
                          "Unexpected error: Could not execute function")
            logging.error(err)
            
            return     
        
    def join_link_odds_partida(self, index, max_iterate=10):
        """
        Entra dentro do link de uma partida, no campeonato. 
        Barra de progresso para a quantidade de tentativas, em relação à quantidade máxima <max_iterate>

        Args:
            index: (int) índice da partida do campeonato
            max_iterate: número máximo de tentativas
        Returns:
            str: descrição da partida, quando o método é bem sucedido
        """
        
        def _try_join_link_odds_partida():
            try:
                partidas = self.web.find_elements_by_class_name('more_markets')
                qt_odds = partidas[index].text
                if qt_odds == '0':
                    logging.warning("WARNING utils.queries.dafabet.TrafficOddsPartida.join_link_odds_partida: "
                                    "Did not enter in link because quantity of odds equal zero")
                    return True, None
                partidas[index].click()
                descricao_partida = {}
                sleep(2)
                try:
                    descricao_partida_texto = self.web.find_elements_by_class_name('event-header-description')[0].text
                    descricao_partida['horario'] = descricao_partida_texto.split('\n')[1][9:]
                    descricao_partida['time_casa'] = descricao_partida_texto.split('\n')[0].split(' vs ')[0]
                    descricao_partida['time_visitante'] = descricao_partida_texto.split('\n')[0].split(' vs ')[1]
                except: # Evento ao-vivo
                    descricao_partida_texto = self.web.find_elements_by_class_name('live-event')[0].text
                    descricao_partida['horario'] = 'ao vivo'
                    descricao_partida['time_casa'] = descricao_partida_texto.split(' vs ')[0]
                    descricao_partida['time_visitante'] = descricao_partida_texto.split(' vs ')[1]
                return True, descricao_partida
            except:
                return False, None
        success, descricao_partida = loop_try(_try_join_link_odds_partida, max_iterate, 
                                              time_sleep=2, bool_progress=True)

        if success and (descricao_partida is not None):
            logging.info(f"SUCCESS utils.queries.dafabet.TrafficOddsPartida.join_link_odds_partida: "
                         f"Function executed successfully. <index>={index}, <max_iterate>={max_iterate}. "
                         f"{descricao_partida}")
        elif (descricao_partida is not None):
            logging.error(f"ERROR utils.queries.dafabet.TrafficOddsPartida.join_link_odds_partida: "
                          f"Unexpected error: Could not execute function with default max_iterate. "
                          f"<index>={index}, <max_iterate>={max_iterate}")
        return descricao_partida