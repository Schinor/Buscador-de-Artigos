import os
from dotenv import load_dotenv

# Carrega variáveis assim que o módulo é importado
load_dotenv()

class Settings:
    API_KEY = os.getenv("CHAVE_API")
    DEFAULT_MODEL = "gemini-2.5-flash"
    ARXIV_MAX_RESULTS = 5
    
    # Validação simples
    @staticmethod
    def validate():
        if not Settings.API_KEY:
            raise ValueError("A variável CHAVE_API não foi encontrada no .env")

# Instância para uso rápido
settings = Settings()