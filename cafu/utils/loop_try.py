from time import sleep
from tqdm import tqdm
from cafu.metadata.paths import path

import logging
filename = path('logs_cafu')+'/logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

def loop_try(f, max_iterate, time_sleep=0, bool_progress=False):
    """
    loop de tentativas de executar a função <f>
    
    Args:
        f: (function) Args - None. Returns - tuple (x1, x2) x1 bool, se a função foi bem executada ou não
        max_iterate: número máximo de tentativas
        time_sleep: (float) tempo de espera para a próxima tentativa, em segundos
        bool_progress: (bool) se o método tqdm será utilizado
    Returns:
        tuple: (x1, x2) x1 bool, se o método foi bem sucedido
    """
    
    i = 1
    success = False 
    if bool_progress:
        with tqdm(total=max_iterate) as barra_progresso:
            while (i<=max_iterate) and not success:
                if i>1:
                    sleep(time_sleep)
                success, response = f()
                i+=1
                barra_progresso.update(1)
    else:
        while (i<=max_iterate) and not success:
            if i>1:
                sleep(time_sleep)
            success, response = f()
            i+=1
            
    if success:
        logging.info(f"SUCCESS utils.loop_try.loop_try: Function executed successfully. <f>={f}, "
                     f"<max_iterate>={max_iterate}, <time_sleep>={time_sleep}, <barra_progresso>={bool_progress}")
    else:
        logging.error(f"ERROR utils.loop_try.loop_try: Unexpected error: Could not execute function "
                      f"with default max_iterate. <f>={f},<max_iterate>={max_iterate}, <time_sleep>={time_sleep}, "
                      f"<barra_progresso>={bool_progress}")
        
    return success, response