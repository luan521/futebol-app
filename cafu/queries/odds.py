import time
from time import sleep
from tqdm import tqdm
from cafu.utils.queries.dafabet import TrafficOddsPartida
from cafu.utils.loop_try import loop_try
from cafu.utils.string import convert_str_var_time
from cafu.metadata.paths import path

import logging
filename = path('logs_cafu')+'/logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

class GetOdds(TrafficOddsPartida):
    """
    Busca as odds da partida
    
    Args:
        start_webdriver: (bool) se o Chrome driver deve ser iniciado
        headless: (bool) se o navegador será mostrado ou não
    """
    
    def __init__(self, start_webdriver=True, headless=True):
        super().__init__(start_webdriver, headless)
        
        self.qt_mercados = None
        
    def open_odds(self, max_iterate=30):
        """
        Entra no link "Todos os mercados" e abre todas as odds
        
        Args:
            max_iterate: número máximo de tentativas
        Returns:
            int: quantidade de mercados na partida
        """
        
        try:
            market_group_all_selector = self.web.find_element_by_xpath('//*[@id="market_group_all"]')
            qt_mercados = market_group_all_selector.text.split('(')[1][:-1]
            market_group_all_selector.click()
            
            logging.info("P-1 SUCCESS queries.odds.GetOdds.open_odds: Open link Todos os mercados")
        except Exception as err:
            logging.error("ERROR queries.odds.GetOdds.open_odds: Unexpected error: Could not open link Todos os mercados")
            logging.error(err)
            
            return
        
        def _try_open_odds():
            try:
                eventos = self.web.find_elements_by_class_name('event_path-title.ellipsis.rollup-title.x.collapsed')
                for e in tqdm(eventos):
                    try:
                        e.click()
                    except:
                        pass
                if len(eventos) == 0:
                    return True, None
                else:
                    return False, None
            except:
                return False, None
        success = loop_try(_try_open_odds, max_iterate)[0]
        
        if success:
            logging.info("SUCCESS queries.odds.GetOdds.open_odds: Function executed successfully")
            
            return qt_mercados
        else:
            logging.error(f"ERROR queries.odds.GetOdds.open_odds: Unexpected error: Could not "
                          f"execute function with default max_iterate. <max_iterate>={max_iterate}")
            
            return
    
    def _close_open_bets(self):
        """
        Método interno da classe.
        Fecha as apostas abertas, para prosseguir com a coleta das odds
        """
        
        stop = False
        while not stop:
            try:
                class_button_exit = 'remove.icon-remove.icons-remove'
                button_exit = self.web.find_elements_by_class_name(class_button_exit)[0]
                button_exit.click()
            except:
                stop = True
        
    def get_odds(self, qt_desconsiderar=0):
        """
        Busca todas as odds da partida
        
        Args:
            qt_desconsiderar: (int) quantidade de links iniciais que serão desconsiderados, default=0
        Returns:
            dict or tuple: método bem sucedido -> return dict, odds da partida. método não bem sucedido -> 
        return tuple, (odds adquiridas com sucesso, quantidade de links bem sucedidos)
        """
        
        init = time.time()
        
        class_name_all_odds = 'formatted_price.price'
        elements_all_odds = self.web.find_elements_by_class_name(class_name_all_odds)
        if qt_desconsiderar>0:
            elements_all_odds = elements_all_odds[qt_desconsiderar:]
        
        response = {}
        count = 0
        for e in tqdm(elements_all_odds):
            odds = e.text
            if odds != '':
                e.click()
                class_evento = 'market-description.bg-info.text-md.text-light.p5.m0.pl10'
                class_tipo_aposta = 'selection-market-period-description'
                
                def _find_evento():
                    try:
                        evento = self.web.find_elements_by_class_name(class_evento)[0].text
                        return True, evento
                    except:
                        try:
                            xpath = '//*[@id="centre"]/div[7]/div[1]/span[2]'
                            self.web.find_element_by_xpath(xpath).click()
                        except:
                            logging.warning("WARNING queries.odds.GetOdds.get_odds: "
                                            "Could not fix method to find <evento>, part-1")
                            return False, None
                        try:
                            sleep(1)
                            e.click()
                        except:
                            logging.warning("WARNING queries.odds.GetOdds.get_odds: "
                                            "Could not fix method to find <evento>, part-2")
                        return False, None
                def _find_tipo_aposta():
                    try:
                        tipo_aposta = self.web.find_elements_by_class_name(class_tipo_aposta)[0].text
                        # Garantindo que o método não retorne tipo_aposta=','
                        if tipo_aposta == ',': 
                            return False, None
                        else:
                            return True, tipo_aposta
                    except:
                        try:
                            xpath = '//*[@id="centre"]/div[7]/div[1]/span[2]'
                            self.web.find_element_by_xpath(xpath).click()
                        except:
                            logging.warning("WARNING queries.odds.GetOdds.get_odds: "
                                            "Could not fix method to find <tipo_aposta>, part-1")
                            return False, None
                        try:
                            sleep(1)
                            e.click()
                        except:
                            logging.warning("WARNING queries.odds.GetOdds.get_odds: "
                                            "Could not fix method to find <tipo_aposta>, part-2")
                        return False, None
                max_iterate, time_sleep = 10, 2
                success, evento = loop_try(_find_evento, max_iterate, time_sleep)
                if not success:
                    end = time.time()
                    runtime_str = convert_str_var_time(init, end)
                    logging.error(f"ERROR queries.odds.GetOdds.get_odds: "
                                  "Could not find <evento> by method find_elements_by_class_name. "
                                  f"<qt_desconsiderar>={qt_desconsiderar}. runtime = {runtime_str}")
                    return response, count
                success, tipo_aposta = loop_try(_find_tipo_aposta, max_iterate, time_sleep)
                if not success:
                    end = time.time()
                    runtime_str = convert_str_var_time(init, end)
                    logging.error("ERROR queries.odds.GetOdds.get_odds: "
                                  "Could not find <tipo_aposta> by method find_elements_by_class_name. "
                                  f"<qt_desconsiderar>={qt_desconsiderar}. runtime = {runtime_str}")
                    return response, count
                logging.info(f"INFO queries.odds.GetOdds.get_odds: Complete {tipo_aposta} | {evento} | {odds}")
                
                try:
                    response[tipo_aposta][evento] = odds
                except:
                    try:
                        response[tipo_aposta] = {evento: odds} 
                    except Exception as err:
                        end = time.time()
                        runtime_str = convert_str_var_time(init, end)
                        logging.error(f"ERROR queries.odds.GetOdds.get_odds: Could not add odds to dict. "
                                      f"<qt_desconsiderar>={qt_desconsiderar}. runtime = {runtime_str}")
                        logging.error(err)

                        return response, count
            self._close_open_bets()
            count+=1
        
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.info(f"SUCCESS queries.odds.GetOdds.get_odds: Function executed successfully. "
                     f"<qt_desconsiderar>={qt_desconsiderar}. runtime = {runtime_str}")

        return response