from cafu.utils.queries.webdriver_chrome import WebdriverChrome
from cafu.metadata.paths import path

class OpenDoc(WebdriverChrome):
    """
    Args:
        subpackage: (str) complemento do caminho para um subpackage específico

    Abre a documentação da biblioteca cafu
    """
    
    def __init__(self, subpackage=''):
        super().__init__(headless=False)
        
        path_doc = (
                    'file:///' +
                    path('initial_path') +
                    f'/docs/build/html/module/cafu{subpackage}.html'
                   )

        self.web.get(path_doc)