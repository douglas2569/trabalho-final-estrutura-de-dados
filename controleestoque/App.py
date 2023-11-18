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


class Produto:    
    def __init__(self, ultimo_id, nome, preco, quantidade, perecivel=False, data_validade=None):
        self.produto_id = ultimo_id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.perecivel = perecivel
        self.data_validade = data_validade

    def __str__(self):
        return f"{self.nome} (Código: {self.codigo}) - R$ {self.preco:.2f}"
    
    def get_produto_id(self):
        return self.produto_id
    
    def set_produto_id(self, ultimo_id):
        self.produto_id += ultimo_id


    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome


    def get_preco(self):
        return self.preco
        
    def set_preco(self, preco):
        self.preco = preco


    def get_quantidade(self):
        return self.quantidade

    def set_quantidade(self, quantidade):
        self.quantidade = quantidade


    def get_perecivel(self):
        return self.perecivel

    def set_perecivel(self, perecivel):
        self.perecivel = perecivel


    def get_data_validade(self):
        return self.data_validade

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
    ultimo_produto_id = 0
    ultimo_venda_id = 0

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
                    print(f"0 - Voltar")
                    print(f"1 - Adicionar produto")                
                    opcao = int(input("Escolha uma opção: "))
                    match opcao:
                        case 0:
                            break     
                        case 1:
                            # Produto(ultimo_produto_id, "Bermuda", 39.99, 50, True, datetime(2023, 12, 31))
                            print(f" --------- Cadastrar Produto --------- ")  
                            produto = []    
                            produto.append(ultimo_produto_id + 1)

                            nome = input("Nome: ")  
                            produto.append(nome)   
                            preco = float(input("Preço: "))  
                            produto.append(preco)   
                            quantidade = int(input("Quantidade: "))  
                            produto.append(quantidade)   
                            perecivel = input("É perecivel?(s/n) : ") 
                            if perecivel == 's':
                                produto.append(True)   
                                data = input("informe a data (00/00/0000) : ") 
                                data = data.split('/')                                
                                produto.append(datetime(int(data[2]), int(data[1]), int(data[0])))  
                            else:
                                produto.append(False)  
                                produto.append(None) 
                            print(produto)
                            Estoque(database).adicionar_produto(produto)
                            ultimo_produto_id += 1
                            produto = Produto(produto[0], produto[1], produto[2], produto[3], produto[4], produto[5])
                            input("Produto cadastrado com sucesso.") 

            case 2:
                ...           
            case _:
                print("Falha no engano")

        os.system('cls')

        
    
