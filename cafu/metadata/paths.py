import os
from datetime import date

paths = {
         'initial_path': '/Users/luanhenriquecosta/futebol/Futebol',
         'logs_cafu': os.getenv('path_logs_cafu'),
         'dir_results': os.getenv('path_dir_results')
        }

"""
description_paths

- initial_path: caminho local para o projeto

- logs_cafu: caminho local para o diretório onde o arquivo 'logs.txt' será criado, os logs gerados pela execução das funções irão para este arquivo

- dir_results: caminho local para o diretório de teste, onde resultados dos testes automatizados (testes_py) serão salvos
"""

def path(key):
    """
    Args:
        key: (str) chave do dicionário paths
    Returns:
        str: caminho 
    """
    
    response = paths[key]
    
    if key=='logs_cafu':
        today = date.today()
        response = response+f'/{str(today)}'
        try:
            os.mkdir(response)
        except:
            pass
    
    return response