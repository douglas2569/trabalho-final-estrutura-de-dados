from datetime import datetime
from abc import ABC, abstractmethod
import os 

class Registros():    

    def __init__(self):
        self.__produtos = []
        self.__vendas = []
   
    def get_produtos(self):
        return self.__produtos 

    
    def get_vendas(self):
        return self.__vendas 


class Estoque(): #usar pilha para da CTRL + Z ou  Y em excluir e atualizar produtos
    def __init__(self, database):        
        self.__produtos = database.get_produtos()   
    
    def adicionar_produto(self, produto):        
       self.__produtos.append(produto)
          
    
    def atualizar_estoque(self, codigo, quantidade): # usar o mecanismo de pesquisa binaria, recursao
        for produto in self.__produtos:
            if produto.codigo == codigo:
                produto.quantidade += quantidade
                return True
        return False
    
    def estoque(self):
        return self.__produtos
    
    def produto_por_id(self, produto_id): # fazer pesquisa binaria
       for produto in self.__produtos:
            if produto.produto_id == produto_id:            
                return produto
        
       return -1 


class Produto(id):
    def __init__(self, nome, preco, quantidade, perecivel=False, data_validade=None):
        self.produto_id += id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.perecivel = perecivel
        self.data_validade = data_validade

    def __str__(self):
        return f"{self.nome} (Código: {self.codigo}) - R$ {self.preco:.2f}"
    
    def set_produto_id(self, produto_id):
        self.produto_id = produto_id

    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome

    def set_preco(self, preco):
        self.preco = preco

    def get_quantidade(self):
        return self.quantidade

    def set_quantidade(self, quantidade):
        self.quantidade = quantidade

    def set_perecivel(self, perecivel):
        self.perecivel = perecivel

    def set_data_validade(self, data_validade):
        self.data_validade = data_validade

class Venda:    
    def __init__(self, venda_id, descricao='', itens=[]):
        self.__venda_id = venda_id
        self.__descricao = descricao
        self.__itens = itens

    def get_venda_id(self):
        return self.__venda_id
        
    def get_descricao(self):
        return self.__descricao

    def get_produtos_venda(self):
        return self.__itens
    
class Controle_Venda:
    def __init__(self, database):        
        self.__estoque = Estoque(database)
        self.__vendas = database.get_vendas() 
    
    def realizar_venda(self, venda): 
        for produto in venda.get_produtos_venda():
            produto_bd = self.__estoque.produto_por_id(produto['produto_id'])
            if produto_bd.get_quantidade() < produto['quantidade']:
                venda.get_produtos_venda().remove(produto)
                print('O produto ',produto_bd.get_nome(), ' foi removido da venda por nao possui quantidade suficiente em estoque')
            else:
                produto_bd.set_quantidade( produto_bd.get_quantidade() -  produto['quantidade'])

        self.__vendas.append(venda)  
        print('venda realizada com sucesso')
        
    def relatorio_vendas(self):
        for venda in self.__vendas:
            for produto in venda.get_produtos_venda():
                produto_bd = self.__estoque.produto_por_id(produto['produto_id'])
                print(f"Código: {produto['produto_id']} | Nome: {produto_bd.get_nome()} | {produto['quantidade']} vendido(s)")
    


if __name__ == "__main__":        
    database = Registros()
    produto_id = 0
    venda_id = 0

    ''' produto1 = Produto(1, "Camiseta", 29.99, 100)
        produto2 = Produto(2, "Bermuda", 39.99, 50, True, datetime(2023, 12, 31))
        
        Estoque(database).adicionar_produto(produto1)
        Estoque(database).adicionar_produto(produto2)

        venda = Venda(1,'venda de natal', [{'produto_id':1, 'quantidade':101}, {'produto_id':2, 'quantidade':1}])   

        Controle_Venda(database).realizar_venda(venda)
        Controle_Venda(database).relatorio_vendas()    
    '''

    while True:
        print(f" --------- Inicio --------- ")
        print(f"0 - Sair")
        print(f"1 - Estoque")
        print(f"2 - Comprar")
        opcao = int(input("Escolha uma opção: "))

        match opcao:
            case 0:                
                break
            case 1:
                while True:
                    os.system('cls')
                    print(f" --------- Estoque --------- ")
                    print(f"0 - Sair")
                    print(f"1 - Adicionar produto")                
                    opcao = int(input("Escolha uma opção: "))
                    match opcao:
                        case 0:
                            break     
                        case 1:
                            print(f" --------- Cadastrar Produto --------- ")
                            print(f"0 - Sair")
                            print(f"1 - Adicionar produto")  
                            produto2 = Produto(2, "Bermuda", 39.99, 50, True, datetime(2023, 12, 31))
                            opcao = int(input("Escolha uma opção: "))   
            case 2:
                ...           
            case _:
                print("Falha no engano")

        os.system('cls')

        
    
