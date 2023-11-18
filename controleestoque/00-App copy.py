from datetime import datetime
from abc import ABC, abstractmethod

class Registros(ABC):
    produtos = []
    vendas = []

    def __init__(self):
        self.__produtos = []
        self.__vendas = []

    @abstractmethod
    def get_produtos(self):
        return self.produtos 

    
    def get_vendas(self):
        return self.__vendas 


class Estoque(): #usar pilha para da CTRL + Z ou  Y em excluir e atualizar produtos
    def __init__(self):        
        ...    
    
    def adicionar_produto(self, produto):        
        Registros.get_produtos().append(produto)        
    
    def atualizar_estoque(self, codigo, quantidade): # usar o mecanismo de pesquisa binaria, recursao
        for produto in self.__produtos:
            if produto.codigo == codigo:
                produto.quantidade += quantidade
                return True
        return False
    
    def estoque(self):
        return self.__produtos


class Produto:
    def __init__(self, codigo, nome, preco, quantidade, perecivel=False, data_validade=None):
        self.codigo = codigo
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.perecivel = perecivel
        self.data_validade = data_validade

    def __str__(self):
        return f"{self.nome} (Código: {self.codigo}) - R$ {self.preco:.2f}"
    
    def set_codigo(self, codigo):
        self.codigo = codigo

    def set_nome(self, nome):
        self.nome = nome

    def set_preco(self, preco):
        self.preco = preco

    def set_quantidade(self, quantidade):
        self.quantidade = quantidade

    def set_perecivel(self, perecivel):
        self.perecivel = perecivel

    def set_data_validade(self, data_validade):
        self.data_validade = data_validade

class Venda(ABC):
    def __init__(self, vendas):
        self.vendas = Registros.get_vendas()

    @abstractmethod
    def vender_produto(self, codigo, quantidade):
        for produto in self.produtos:
            if produto.codigo == codigo and produto.quantidade >= quantidade:
                produto.quantidade -= quantidade
                return True
        return False

    @abstractmethod
    def relatorio_vendas(self):
        for produto in self.produtos:
            print(f"{produto.nome}: {produto.quantidade} vendido(s)")


if __name__ == "__main__":        

    # produto1 = Produto(1, "Camiseta", 29.99, 100)
    produto = Produto(1, "Bermuda", 39.99, 50, True, datetime(2023, 12, 31))
    # print(produto)
    Estoque().adicionar_produto(produto)
    Estoque().adicionar_produto(produto)
    print(Registros.produtos)
    
    #Estoque.Estoque.adicionar_produto(produto2)

    #Venda.realizar_venda(codigo=1, quantidade=10)
    #Venda.realizar_venda(codigo=2, quantidade=20)

    #Estoque.estoque.relatorio_vendas()