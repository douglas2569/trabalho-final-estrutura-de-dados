from datetime import datetime
from abc import ABC, abstractmethod

class Registros(ABC):
    def __init__(self):
        self.produtos = []
        self.vendas = []

    @abstractmethod
    def get_produtos(self):
        return self.produtos 

    @abstractmethod
    def get_vendas(self):
        return self.vendas 


class Estoque(ABC):
    def __init__(self, produtos):        
        self.produtos = Registros.get_produtos()

    @abstractmethod
    def adicionar_produto(self, produto):
        self.produtos.append(produto)

    @abstractmethod
    def atualizar_estoque(self, codigo, quantidade): # usar o mecanismo de pesquisa binaria, recursao
        for produto in self.produtos:
            if produto.codigo == codigo:
                produto.quantidade += quantidade
                return True
        return False

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

    produto1 = Produto(codigo=1, nome="Camiseta", preco=29.99, quantidade=100)
    produto2 = Produto(codigo=2, nome="Bermuda", preco=39.99, quantidade=50, perecivel=True, data_validade=datetime(2023, 12, 31))
    
    Estoque.adicionar_produto('', produto1)
    #Estoque.Estoque.adicionar_produto(produto2)

    #Venda.realizar_venda(codigo=1, quantidade=10)
    #Venda.realizar_venda(codigo=2, quantidade=20)

    #Estoque.estoque.relatorio_vendas()