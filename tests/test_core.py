import unittest
from unittest.mock import patch, MagicMock
from core.parser import parsear_resposta_ia
from core.search import buscar_artigos_arxiv

class TestCoreFunctions(unittest.TestCase):

    # TESTE 1: Testa se o parser converte texto em dicionário corretamente
    def test_parser_texto_valido(self):
        texto_fake_ia = """
        Titulo: Teste de IA
        Ano: 2024
        Link: http://teste.com
        Resumo: Um resumo teste.
        Utilidade: Muito util.
        Relevancia: 9
        ---
        """
        resultado = parsear_resposta_ia(texto_fake_ia)
        
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]['titulo'], "Teste de IA")
        self.assertEqual(resultado[0]['nota'], 9)

    # TESTE 2: Testa se o parser ignora lixo
    def test_parser_texto_invalido(self):
        texto_lixo = "Desculpe, não encontrei nada."
        resultado = parsear_resposta_ia(texto_lixo)
        self.assertEqual(resultado, [])

    # TESTE 3: Testa a busca do ArXiv MOCKADA (Sem internet)
    @patch('core.search.arxiv.Client') # Substitui o arxiv.Client real por um falso
    def test_busca_arxiv_mock(self, MockClient):
        # Configura o comportamento do Mock
        mock_instance = MockClient.return_value
        
        # Simula um resultado do ArXiv
        mock_result = MagicMock()
        mock_result.title = "Paper Falso"
        mock_result.summary = "Resumo Falso"
        mock_result.pdf_url = "http://fake.pdf"
        mock_result.published.strftime.return_value = "2023-01-01"
        
        # Diz que client.results retorna uma lista com esse resultado
        mock_instance.results.return_value = [mock_result]
        
        # Executa a função
        dados = buscar_artigos_arxiv("tema teste")
        
        # Verifica se funcionou
        self.assertEqual(len(dados), 1)
        self.assertEqual(dados[0]['titulo'], "Paper Falso")

if __name__ == '__main__':
    unittest.main()