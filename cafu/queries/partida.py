import requests as r
from html2json import collect
import json
from bs4 import BeautifulSoup
import datetime
import time
from cafu.utils.string import convert_str_var_time
from cafu.utils.queries.webdriver_chrome import WebdriverChrome
from cafu.utils.queries.partida import (sem_espaco, padrao, padrao_inicio_fim, mes,
                                        jogadores_inscritos, teste_gols, gols_casa_visitante)

from cafu.metadata.paths import path

import logging
filename = path('logs_cafu')+'/logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

class Partida(WebdriverChrome):
    """
    Retorna informações sobre uma partida de futebol, buscando no site da ESPN
    
    Args:
        jogo_id: (int or str) completa o link https://www.espn.com.br/futebol/escalacoes?jogoId=<jogo_id>. 
        check_status: (bool) se o status da partida será buscado ou não, ao iniciar a classe
    """

    def __init__(self, jogo_id, check_status=True):
        
        init = time.time()
        
        self.jogo_id = str(jogo_id)
        
        if check_status:
            super().__init__()
            self.get_partida_espn(self.jogo_id)
            # buscando a data da partida
            try:
                xpath = '//*[@id="gamepackage-game-information"]/article/div/ul[2]/li/div/span/span[2]'
                text = self.web.find_element_by_xpath(xpath).text
                year = int(text.split(', ')[1])
                day_month = text.split(', ')[0]
                day = int(day_month.split(' de ')[0])
                month = mes(day_month.split(' de ')[1])
                xpath = '//*[@id="gamepackage-game-information"]/article/div/ul[2]/li/div/span/span[1]'
                hour_minute = self.web.find_element_by_xpath(xpath).text
                hour = int(hour_minute.split(':')[0])
                minute = int(hour_minute.split(':')[1])
                self.date = datetime.datetime(year, month, day, hour, minute)
            except Exception as err:
                self.date = None
                end = time.time()
                runtime_str = convert_str_var_time(init, end)
                logging.error("ERROR queries.Partida.__init__: Unexpected error: "
                              f"Could not find date by method find_element_by_xpath of selenium. "
                              f"<jogo_id>={self.jogo_id}. runtime = {runtime_str}")
                logging.error(err)
            # buscando status da partida
            try:
                xpath = '//*[@id="gamepackage-matchup-wrap--soccer"]/div[2]/div[2]/span[1]'
                status = self.web.find_element_by_xpath(xpath).text
                # case: jogo em andamento
                if status == '':
                    xpath = '//*[@id="gamepackage-matchup-wrap--soccer"]/div[2]/div[2]/span[2]'
                    status = self.web.find_element_by_xpath(xpath).text
                self.web.close()
            except Exception as err:
                self.web.close()
                end = time.time()
                runtime_str = convert_str_var_time(init, end)
                logging.error("ERROR queries.Partida.__init__: Unexpected error: "
                              f"Could not find status by method find_element_by_xpath of selenium. "
                              f"<jogo_id>={self.jogo_id}. runtime = {runtime_str}")
                logging.error(err)
                return
            if status == 'Finalizado':
                self.status = status
                end = time.time()
                runtime_str = convert_str_var_time(init, end)
                logging.info(f"SUCCESS queries.Partida.__init__: "
                             f"status da partida: {status}. <jogo_id>={self.jogo_id}. "
                             f"runtime = {runtime_str}")
            elif status == 'Cancelado':
                self.status = status
                end = time.time()
                runtime_str = convert_str_var_time(init, end)
                logging.info(f"WARNING queries.Partida.__init__: "
                             f"status da partida: {status}. <jogo_id>={self.jogo_id}. "
                             f"runtime = {runtime_str}")
            # case: jogo em andamento
            elif ('\'' in status) or (status == 'INT'):
                self.status = 'Em_andamento'
                self.minuto = status
                end = time.time()
                runtime_str = convert_str_var_time(init, end)
                logging.info(f"INFO queries.Partida.__init__: "
                             f"status da partida: {self.status}, minuto: {status}. <jogo_id>={self.jogo_id}. "
                             f"runtime = {runtime_str}")
            else:
                try:
                    test_format_status = status.split('\n')[1]
                    self.status = 'Nao_Finalizado'
                    end = time.time()
                    runtime_str = convert_str_var_time(init, end)
                    logging.info(f"INFO queries.Partida.__init__: "
                                 f"partida ocorrerá na data: {self.date}. <jogo_id>={self.jogo_id}. "
                                 f"runtime = {runtime_str}")
                except Exception as err:
                    self.status = None
                    end = time.time()
                    runtime_str = convert_str_var_time(init, end)
                    logging.error(f"ERROR queries.Partida.__init__: Unexpected error: "
                                  f"status in unexpected format, return status={status}. "
                                  f"<jogo_id>={self.jogo_id}. runtime = {runtime_str}")
                    logging.error(err)
            
    def campeonato(self):
        """
        Returns:
            str: campeonato disputado
        """
        
        init = time.time()
    
        try:
            req = r.get("https://www.espn.com.br/futebol/escalacoes?jogoId="+self.jogo_id)
            soup = BeautifulSoup(req.content, 'html.parser')
            st = soup.prettify()
            abt = sem_espaco(st)

            ind = padrao_inicio_fim(['class="game-details','header">\n'],['</div>\n'],abt)
            abt1 = abt[ind[0][0]:ind[0][1]][2:-1]

            response = ''
            for x in abt1:
                response = response + ' ' + x
            response = response[1:-1]
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS queries.Partida.campeonato: "
                         f"Function executed successfully. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.Partida.campeonato: "
                          f"Unexpected error: Could not execute function. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            logging.error(err)
            
    def day(self):
        """
        Returns:
            datetime: data da partida
        """
        
        init = time.time()
        
        try:
            req = r.get("https://www.espn.com.br/futebol/escalacoes?jogoId="+self.jogo_id)
            soup = BeautifulSoup(req.content, 'html.parser')
            st = soup.prettify()
            abt = sem_espaco(st)

            ind = padrao_inicio_fim(['<title>\n'],['</title>\n'],abt)

            abt1 = abt[ind[0][0]:ind[0][1]]
            ind_date = padrao_inicio_fim(['partida'],['ESPN\n'],abt1)[0][0]+2

            date = abt1[ind_date:ind_date+3]
            month = date[1][:-1]

            day = int(date[0])
            month = mes(month)
            year = int(date[2])

            response = datetime.datetime(year, month, day)
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS queries.Partida.day: "
                         f"Function executed successfully. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.Partida.day: "
                          f"Unexpected error: Could not execute function. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            logging.error(err)
            
    def nomes_times(self):
        """
        Returns:
            tuple: (time da casa, time visitante)
        """
        
        init = time.time()
        
        try:
            req = r.get("https://www.espn.com.br/futebol/escalacoes?jogoId="+self.jogo_id)
            soup = BeautifulSoup(req.content, 'html.parser')
            st = soup.prettify()
            abt = sem_espaco(st)

            ind = padrao_inicio_fim(['<title>\n'],['</title>\n'],abt)
            abt1 = abt[ind[0][0]:ind[0][1]]
            ind_time_casa = padrao_inicio_fim(['<title>\n'],['X'],abt1)
            ind_time_visitante = padrao_inicio_fim(['X'],['-'],abt1)

            time_0 = abt1[ind_time_casa[0][0]+1:ind_time_casa[0][1]-1]
            time_casa = ''
            for x in time_0:
                time_casa = time_casa + ' ' + x
            time_casa = time_casa[1:]

            time_0 = abt1[ind_time_visitante[0][0]+1:ind_time_visitante[0][1]-1]
            time_visitante = ''
            for x in time_0:
                time_visitante = time_visitante + ' ' + x
            time_visitante = time_visitante[1:]

            response = time_casa, time_visitante
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS queries.Partida.nomes_times: "
                         f"Function executed successfully. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.Partida.nomes_times: "
                          f"Unexpected error: Could not execute function. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            logging.error(err)
            return None, None
            
    def formacao(self):
        """
        Returns:
            tuple: (formação do time da casa, formação do time visitante)
        """
        
        init = time.time()
    
        try:
            req = r.get("https://www.espn.com.br/futebol/escalacoes?jogoId="+self.jogo_id)
            soup = BeautifulSoup(req.content, 'html.parser')
            st = soup.prettify()
            abt = sem_espaco(st)
            
            ind_formacao_casa = padrao_inicio_fim(['class="formations__text">\n'],['</div>\n'],abt)[0][0]+1
            ind_formacao_visitante = padrao_inicio_fim(['class="formations__text">\n'],['</div>\n'],abt)[1][0]+1
            formacao_casa = abt[ind_formacao_casa][:-1] 
            formacao_visitante = abt[ind_formacao_visitante][:-1]
            
            response = formacao_casa, formacao_visitante
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS queries.Partida.formacao: "
                         f"Function executed successfully. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.Partida.formacao: "
                          f"Unexpected error: Could not execute function. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            logging.error(err)
            return None, None
            
    def jogadores(self):
        """
        Returns:
            tuple: (jogadores do time da casa, jogadores do time visitante) apenas jogadores que atuaram na partida.
            nome, camisa, minuto que entrou, minuto que saiu.
        """
        
        init = time.time()
    
        try:
            jogadores_casa_0, jogadores_visitante_0 = jogadores_inscritos(self.jogo_id)

            jogadores_casa_1 = []
            jogadores_visitante_1 = []
            s = 1
            i = 0
            while s<=12:
                if s<12 or jogadores_casa_0[i][2]!=0:
                    jogadores_casa_1.append(jogadores_casa_0[i])
                i+=1
                if jogadores_casa_0[i][2]==0:
                    s+=1

            s=1
            i=0
            while s<=12:
                if s<12 or jogadores_visitante_0[i][2]!=0:
                    jogadores_visitante_1.append(jogadores_visitante_0[i])
                i+=1
                if jogadores_visitante_0[i][2]==0:
                    s+=1

            jogadores_casa=[]
            jogadores_visitante=[]
            for i in range(len(jogadores_casa_1)):
                jogadores_casa.append({'nome': jogadores_casa_1[i][0], 
                                       'camisa': jogadores_casa_1[i][1], 
                                       'inicio_jogando': jogadores_casa_1[i][2], 
                                       'final_jogando': 90})
                if i<len(jogadores_casa_1)-1 and jogadores_casa_1[i+1][2]!=0:
                    jogadores_casa[i]['final_jogando']=jogadores_casa_1[i+1][2]

            for i in range(len(jogadores_visitante_1)):
                jogadores_visitante.append({'nome': jogadores_visitante_1[i][0], 
                                            'camisa': jogadores_visitante_1[i][1], 
                                            'inicio_jogando': jogadores_visitante_1[i][2], 
                                            'final_jogando': 90})
                if i<len(jogadores_visitante_1)-1 and jogadores_visitante_1[i+1][2]!=0:
                    jogadores_visitante[i]['final_jogando']=jogadores_visitante_1[i+1][2]

            response = jogadores_casa, jogadores_visitante
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS queries.Partida.jogadores: "
                         f"Function executed successfully. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.Partida.jogadores: "
                          f"Unexpected error: Could not execute function. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            logging.error(err)
            return None, None
            
    def gols(self):
        """
        Returns:
            tuple: (gols marcados pelo time da casa, gols marcados pelo time visitante). 
            nome do jogador, minuto
        """
        
        init = time.time()

        try:
            teste_casa, teste_visitante = teste_gols(self.jogo_id)

            gols_casa = None
            if teste_casa:
                gols_casa = gols_casa_visitante(0,self.jogo_id)

            gols_visitante = None
            if teste_visitante:
                if teste_casa:
                    gols_visitante = gols_casa_visitante(1,self.jogo_id)
                else:
                    gols_visitante = gols_casa_visitante(0,self.jogo_id)

            response = gols_casa, gols_visitante
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS queries.Partida.gols: "
                         f"Function executed successfully. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.Partida.gols: "
                          f"Unexpected error: Could not execute function. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            logging.error(err)
            return None, None
            
            
    def placar(self):
        """
        Returns:
            tuple: placar da partida
        """
        
        init = time.time()
        
        try:
            req = r.get("https://www.espn.com.br/futebol/escalacoes?jogoId="+self.jogo_id)
            soup = BeautifulSoup(req.content, 'html.parser')
            st = soup.prettify()
            abt = sem_espaco(st)

            ind_casa = padrao_inicio_fim(['<span', 'class="score', 'icon-font-after"', 
                                        'data-home-away="home"', 'data-stat="score">\n'],['</span>\n'],abt)
            gols_casa = abt[ind_casa[0][0]:ind_casa[0][1]][5][:-1]
            gols_casa = int(gols_casa)

            ind_visitante = padrao_inicio_fim(['<span', 'class="score', 'icon-font-before"', 
                                             'data-home-away="away"', 'data-stat="score">\n'],['</span>\n'],abt)
            gols_visitante = abt[ind_visitante[0][0]:ind_visitante[0][1]][5][:-1]
            gols_visitante = int(gols_visitante)

            response = gols_casa, gols_visitante
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS queries.Partida.placar: "
                         f"Function executed successfully. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.Partida.placar: "
                          f"Unexpected error: Could not execute function. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            logging.error(err)
            return None, None
            
    def posse(self):
        """
        Returns:
            tuple: posse de bola
        """
        
        init = time.time()
        
        try:
            req = r.get("https://www.espn.com.br/futebol/partida-estatisticas?jogoId="+self.jogo_id)
            soup = BeautifulSoup(req.content, 'html.parser')
            st = soup.prettify()
            abt = sem_espaco(st)

            ind = padrao_inicio_fim(['Posse\n'],['</div>\n'],abt)
            abt1 = abt[ind[0][0]:ind[0][1]]
            ind = padrao(['data-stat="possessionPct">\n'],abt1)

            resultado_casa = float(abt1[ind[0][1]][:-2])/100
            resultado_visitante = float(abt1[ind[1][1]][:-2])/100

            response = resultado_casa, resultado_visitante
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS queries.Partida.posse: "
                         f"Function executed successfully. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.Partida.posse: "
                          f"Unexpected error: Could not execute function. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            logging.error(err)
            return None, None
            
    def chutes_fora_nogol(self):
        """
        Returns:
            tuple: (time da casa [x1, x2], time visitante [x3, x4]) chutes para fora, chutes no gol
        """
        
        init = time.time()
        
        try:
            req = r.get("https://www.espn.com.br/futebol/partida-estatisticas?jogoId="+self.jogo_id)
            soup = BeautifulSoup(req.content, 'html.parser')
            st = soup.prettify()
            abt = sem_espaco(st)

            ind = padrao_inicio_fim(['chutes', '(no', 'gol)\n'],['data-home-away="away"'],abt)
            abt1 = abt[ind[0][0]:ind[0][1]+10]

            ind = padrao(['data-stat="shotsSummary">\n'],abt1)
            resultado_casa = abt1[ind[0][1]:ind[0][1]+2]
            resultado_visitante =abt1[ind[1][1]:ind[1][1]+2]

            resultado_casa[1] = int(resultado_casa[1][1:-2])
            resultado_visitante[1] = int(resultado_visitante[1][1:-2])
            resultado_casa[0] = int(resultado_casa[0]) - resultado_casa[1]
            resultado_visitante[0] = int(resultado_visitante[0]) - resultado_visitante[1]

            response = resultado_casa, resultado_visitante
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS queries.Partida.chutes_fora_nogol: "
                         f"Function executed successfully. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.Partida.chutes_fora_nogol: "
                          f"Unexpected error: Could not execute function. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            logging.error(err)
            return None, None

    def faltas(self):
        """
        Returns:
            tuple: (quantidade de faltas cometidas pelo time da casa, 
            quantidade de faltas cometidas pelo time visitante)
        """
        
        init = time.time()
        
        try:
            req = r.get("https://www.espn.com.br/futebol/partida-estatisticas?jogoId="+self.jogo_id)
            soup = BeautifulSoup(req.content, 'html.parser')
            st = soup.prettify()
            abt = sem_espaco(st)

            imp = padrao(['faltas\n'],abt)

            resultado_casa = int(abt[imp[0][0]-3][:-1])
            resultado_visitante = int(abt[imp[0][0]+5][:-1])

            response = resultado_casa, resultado_visitante
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS queries.Partida.faltas: "
                         f"Function executed successfully. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.Partida.faltas: "
                          f"Unexpected error: Could not execute function. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            logging.error(err)
            return None, None
            
    def cartoes_amarelos(self):
        """
        Returns:
            tuple: (quantidade de cartões amarelos levados pelo time da casa, 
            quantidade de cartões amarelos levados pelo time visitante)
        """
        
        init = time.time()
        
        try:
            req = r.get("https://www.espn.com.br/futebol/partida-estatisticas?jogoId="+self.jogo_id)
            soup = BeautifulSoup(req.content, 'html.parser')
            st = soup.prettify()
            abt = sem_espaco(st)

            imp = padrao(['Cartões','amarelos\n'],abt)

            resultado_casa = int(abt[imp[0][0]-3][:-1])
            resultado_visitante = int(abt[imp[0][0]+6][:-1])

            response = resultado_casa, resultado_visitante
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS queries.Partida.cartoes_amarelos: "
                         f"Function executed successfully. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.Partida.cartoes_amarelos: "
                          f"Unexpected error: Could not execute function. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            logging.error(err)
            return None, None

    def cartoes_vermelhos(self):
        """
        Returns:
            tuple: (quantidade de cartões vermelhos levados pelo time da casa, 
            quantidade de cartões vermelhos levados pelo time visitante)
        """
        
        init = time.time()
        
        try:
            req = r.get("https://www.espn.com.br/futebol/partida-estatisticas?jogoId="+self.jogo_id)
            soup = BeautifulSoup(req.content, 'html.parser')
            st = soup.prettify()
            abt = sem_espaco(st)

            imp = padrao(['Cartões','Vermelhos\n'],abt)

            resultado_casa = int(abt[imp[0][0]-3][:-1])
            resultado_visitante = int(abt[imp[0][0]+6][:-1])

            response = resultado_casa, resultado_visitante
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS queries.Partida.cartoes_vermelhos: "
                         f"Function executed successfully. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.Partida.cartoes_vermelhos: "
                          f"Unexpected error: Could not execute function. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            logging.error(err)
            return None, None
            
    def impedimentos(self):
        """
        Returns:
            tuple: (quantidade de impedimentos marcados para o time da casa, 
            quantidade de impedimentos marcados para o time visitante)
        """
        
        init = time.time()
        
        try:
            req = r.get("https://www.espn.com.br/futebol/partida-estatisticas?jogoId="+self.jogo_id)
            soup = BeautifulSoup(req.content, 'html.parser')
            st = soup.prettify()
            abt = sem_espaco(st)

            imp = padrao(['Impedimentos\n'],abt)

            resultado_casa = int(abt[imp[0][0]-3][:-1])
            resultado_visitante = int(abt[imp[0][0]+5][:-1])

            response = resultado_casa, resultado_visitante
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS queries.Partida.impedimentos: "
                         f"Function executed successfully. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.Partida.impedimentos: "
                          f"Unexpected error: Could not execute function. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            logging.error(err)
            return None, None

    def escanteios(self):
        """
        Returns:
            tuple: (quantidade de escanteios para o time da casa, 
            quantidade de escanteios para o time visitante)
        """
        
        init = time.time()
        
        try:
            req = r.get("https://www.espn.com.br/futebol/partida-estatisticas?jogoId="+self.jogo_id)
            soup = BeautifulSoup(req.content, 'html.parser')
            st = soup.prettify()
            abt = sem_espaco(st)

            imp = padrao(['Escanteios\n'],abt)

            resultado_casa = int(abt[imp[0][0]-3][:-1])
            resultado_visitante = int(abt[imp[0][0]+5][:-1])

            response = resultado_casa, resultado_visitante
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS queries.Partida.escanteios: "
                         f"Function executed successfully. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.Partida.escanteios: "
                          f"Unexpected error: Could not execute function. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            logging.error(err)
            return None, None

    def defesas(self):
        
        init = time.time()
        
        try:
            req = r.get("https://www.espn.com.br/futebol/partida-estatisticas?jogoId="+self.jogo_id)
            soup =  BeautifulSoup(req.content, 'html.parser')
            st = soup.prettify()
            abt = sem_espaco(st)

            imp = padrao(['defesas\n'],abt)

            resultado_casa = int(abt[imp[0][0]-3][:-1])
            resultado_visitante = int(abt[imp[0][0]+5][:-1])

            response = resultado_casa, resultado_visitante
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS queries.Partida.defesas: "
                         f"Function executed successfully. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.Partida.defesas: "
                          f"Unexpected error: Could not execute function. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            logging.error(err)
            return None, None
            
    def minuto_a_minuto(self):
        """
        Returns:
            list: descrições dos momentos da partida. tempo, descrição
        """
        
        init = time.time()
        
        try:
            req = r.get("https://www.espn.com.br/futebol/comentario?jogoId="+self.jogo_id)
            soup = BeautifulSoup(req.content, 'html.parser')
            st = soup.prettify()
            abt = sem_espaco(st)

            ind = padrao_inicio_fim(['Principais\n'],['data-behavior="soccer_commentary_key_events"'],abt)
            abt1 = abt[ind[0][0]:ind[0][1]]

            ind = padrao_inicio_fim(['class="time-stamp">\n'],['</tr>\n'],abt1)

            response = []
            for x in ind:
                acontecimento = abt1[x[0]:x[1]]

                ind1 = padrao(['class="time-stamp">\n'],acontecimento)
                try:
                    tempo = int(acontecimento[ind1[0][1]][:-2])
                except:
                    final_do_jogo = True
                    for x in response:
                        if x['tempo'] < 90:
                            final_do_jogo = False
                    if final_do_jogo:
                        tempo = 90
                    else:
                        tempo = 0

                ind2 = padrao_inicio_fim(['class="game-details">\n'],['</td>\n'],acontecimento)
                descricao = ''
                for palavra in acontecimento[ind2[0][0]+1:ind2[0][1]-1]:
                    descricao = descricao + ' ' + palavra
                descricao = descricao[1:-1]

                response.append({'tempo': tempo, 'descrição' : descricao})
            
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.info(f"SUCCESS queries.Partida.minuto_a_minuto: "
                         f"Function executed successfully. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            return response
        except Exception as err:
            end = time.time()
            runtime_str = convert_str_var_time(init, end)
            logging.error(f"ERROR queries.Partida.minuto_a_minuto: "
                          f"Unexpected error: Could not execute function. <jogo_id>={self.jogo_id}. runtime = {runtime_str}")
            logging.error(err)
