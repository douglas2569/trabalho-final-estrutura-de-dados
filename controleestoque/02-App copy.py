from datetime import date, timedelta
from abc import ABC, abstractmethod
import os 

def converter_data(data):
    data = str(data) 
    data = data.split('-')                                
    data = f"{data[2]}/{data[1]}/{data[0]}"

    return data

def inverter_data(data):
    data = str(data) 
    data = data.split('/')

    return date(int(data[2]), int(data[1]), int(data[0]))

class Registros():    

    def __init__(self):
        self.__produtos = []
        self.__vendas = []
   
    def get_produtos(self):
        return self.__produtos 

    
    def get_vendas(self):
        return self.__vendas 

class Estoque(): 
    def __init__(self, database):        
        self.__produtos = database.get_produtos()  

    def mostrar_produtos(self):                
        for produto in self.__produtos:
            print(produto) 
    
    def mostrar_produtos_vencidos(self):
        for produto in self.__produtos:
            if produto.get_perecivel() and produto.get_data_validade() < date.today():
                print(produto)

    def mostrar_produtos_vencimento(self, dia):
        for produto in self.__produtos:
            if produto.get_perecivel() and produto.get_data_validade() >= date.today() and produto.get_data_validade() <= date.today() + timedelta(dia):
                print(produto)
    
    def cadastrar_produto(self, produto):        
       self.__produtos.append(produto)
     
    def repor_produto(self, produto_id, quantidade): 
        produto_bd = self.produto_por_id(produto_id)        
        if len(produto_bd) < 2:
           raise ValueError('ID invalido')
                   
        if  quantidade < 0:                
            print('Não é permitido valores negativos para quantidade')
        else:                
            produto_bd[1].set_quantidade( produto_bd[1].get_quantidade() +  quantidade) 
            self.__produtos[produto_bd[0]] = produto_bd[1]
    
    def remover_produto(self, produto_id, quantidade): 
        produto_bd = self.produto_por_id(produto_id)
        if len(produto_bd) < 2:
            return
        if  quantidade <= 0:                
            print('Não é permitido valores negativos para quantidade')
        elif produto_bd[1].get_quantidade() < quantidade:
            print('Não há quantidade de produtos suficiente')
        else:                
            produto_bd[1].set_quantidade( produto_bd[1].get_quantidade() -  quantidade) 
            self.__produtos[produto_bd[0]] = produto_bd[1] 
            print('Produto removido com sucesso')  

    def excluir_produto(self, produto_id):
        produto_bd = self.produto_por_id(produto_id)        
        if len(produto_bd) < 2:
            return
                         
        self.__produtos.remove(produto_bd[1])               

    def estoque(self):
        return self.__produtos
    
    def produto_por_id(self, produto_id): # fazer pesquisa binaria
       
       for produto in self.__produtos:      
            if produto.get_produto_id() == produto_id:            
                return [self.__produtos.index(produto), produto]
        
       return [] 
    
    def produto_vencido(self, produto_id): 
       produto_bd = self.produto_por_id(produto_id)
       if len(produto_bd) < 2:
            return
       
       if produto_bd[1].get_perecivel() and produto_bd[1].get_data_validade() < date.today():   
            return True
       return False 

class Produto:    
    def __init__(self, ultimo_id, nome, preco, quantidade, perecivel=False, data_validade=None):
        self.produto_id = ultimo_id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.perecivel = perecivel
        self.data_validade = data_validade

    def __str__(self):
        if self.perecivel:            
            return f"ID: {self.produto_id} | {self.nome} | R$ {self.preco} | {self.quantidade} | {converter_data(self.data_validade)}"
        else:
            return f"ID: {self.produto_id} | {self.nome} | R$ {self.preco} | {self.quantidade}"

    
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
    def __init__(self, database, venda_id, descricao='', itens=[]):
        self.__venda_id = venda_id
        self.__descricao = descricao
        self.__itens = itens
        self.__estoque = Estoque(database)

    def __str__(self):   
       str = f"\n{self.__descricao}\n"
       for item in self.__itens:
            produto = self.__estoque.produto_por_id(item['produto_id'])
            str += f"\t{item['produto_id']} | {produto[1].get_nome()} |{item['quantidade']}\n"
            
       return str
    
    def get_venda_id(self):
        return self.__venda_id
        
    def get_descricao(self):
        return self.__descricao

    def get_produtos_venda(self):
        return self.__itens
    
    def set_produtos_venda(self, itens):
        self.__itens = itens
    
class Controle_Venda:
    def __init__(self, database):        
        self.__estoque = Estoque(database)
        self.__vendas = database.get_vendas() 
    
    def realizar_venda(self, venda):
        produtos_venda = list(venda.get_produtos_venda())        
        for produto in produtos_venda:
            produto_bd = self.__estoque.produto_por_id(produto['produto_id'])

            if len(produto_bd) < 2:
                continue
            
            if Estoque(database).produto_vencido(produto['produto_id']):
                venda.get_produtos_venda().remove(produto)                
                input(f"O produto {produto_bd[1].get_nome()} foi removido da venda porque está vencido")

            elif produto_bd[1].get_quantidade() < produto['quantidade']:
                venda.get_produtos_venda().remove(produto)
                input(f"O produto {produto_bd[1].get_nome()} foi removido da venda por nao possui quantidade suficiente em estoque")

            else:
                produto_bd[1].set_quantidade( produto_bd[1].get_quantidade() -  produto['quantidade'] ) 
                self.__estoque.estoque()[produto_bd[0]] = produto_bd[1]
              


        if len(venda.get_produtos_venda()) > 0:
            self.__vendas.append(venda)
            print(venda)
            input("Compra efetuada com sucesso.") 
        
    def relatorio_vendas(self):
        for venda in self.__vendas:
            for produto in venda.get_produtos_venda():
                produto_bd = self.__estoque.produto_por_id(produto['produto_id'])                
                print(f"ID: {produto['produto_id']} | Nome: {produto_bd[1].get_nome()} | {produto['quantidade']} vendido(s)")

    def vendas(self):
        return self.__vendas 
    
if __name__ == "__main__":        
    database = Registros()
    ultimo_produto_id = 0
    ultimo_venda_id = 0  

    while True:
        print(f" --------- Inicio --------- ")
        print(f"0 - Sair")
        print(f"1 - Estoque")
        print(f"2 - Comprar")
        print(f"3 - Relatório de Vendas")
        
        try:
            opcao = int(input("Escolha uma opção*: "))
        except:
            input("Informe uma opção valida")
            os.system('cls')
            continue

        match opcao:
            case 0:                
                break
            
            case 1:
                while True:
                    os.system('cls')
                    print(f" --------- Estoque --------- ")
                    print(f"0 - Voltar")
                    print(f"1 - Adicionar um novo produto")                
                    print(f"2 - Mostrar produtos")                
                    print(f"3 - Mostrar produtos proximo ao vencimento ( 30 dias )")                
                    print(f"4 - Mostrar produtos vencidos")                
                    print(f"5 - Repor produto")   
                    print(f"6 - Excluir produto")   

                    try:
                        opcao = int(input("Escolha uma opção*: "))
                    except:
                         input("Informe uma opção valida")
                         os.system('cls')
                         continue
                    
                    match opcao:
                        case 0:
                            break     
                        
                        case 1:
                            os.system('cls')
                            print(f" --------- Cadastrar Produto --------- ")  
                            produto = []    
                            produto.append(ultimo_produto_id + 1)

                            nome = input("Nome*: ")  
                            produto.append(nome)   
                            preco = float(input("Preço*: "))  
                            produto.append(preco)   
                            quantidade = int(input("Quantidade*: "))  
                            produto.append(quantidade)   
                            perecivel = input("É perecivel?(s/n)*: ") 
                            if perecivel == 's':
                                produto.append(True)   
                                data = input("Data de vencimento (00/00/0000)*: ")     
                                produto.append(inverter_data(data))  
                            else:
                                produto.append(False)  
                                produto.append(None)
                            
                            produto = Produto(produto[0], produto[1], produto[2], produto[3], produto[4], produto[5])
                            Estoque(database).cadastrar_produto(produto)
                            ultimo_produto_id += 1
                            input("Produto cadastrado com sucesso.") 

                        case 2:
                            os.system('cls')
                            print(f" --------- Todos Produtos --------- ")  
                            Estoque(database).mostrar_produtos()
                            input("Entender para continuar.")  
                        
                        case 3:
                            os.system('cls')
                            print(f" --------- Produtos proximo ao vencimento ( 30 dias ) --------- ")  
                            Estoque(database).mostrar_produtos_vencimento(30)
                            input("Entender para continuar.")
                        
                        case 4:
                            os.system('cls')
                            print(f" --------- Produtos Vencidos --------- ")  
                            Estoque(database).mostrar_produtos_vencidos()
                            input("Entender para continuar.")

                        case 5:
                            os.system('cls')
                            print(f" --------- Repor Produto --------- ")  
                            produto_id = int(input("Informe o ID do produto que deseja repor*: ")) 
                            quantidade = int(input("Informe a quantidade*: ")) 
                            try:
                                Estoque(database).repor_produto(produto_id, quantidade)
                                input("Produto reposto com sucesso.") 
                            except ValueError:
                                input("Informe um ID valido")
                                continue

                        case 6:
                            os.system('cls')
                            print(f" --------- Excluir Produto --------- ")  
                            produto_id = int(input("Informe o ID do produto que deseja excluir*: ")) 
                            #try:
                            Estoque(database).excluir_produto(produto_id)
                            input("Produto excluido com sucesso.") 
                            #except ValueError:
                                #input("Informe um ID valido")
                                #continue

            case 2:
                while True:
                    os.system('cls')
                    if len(Estoque(database).estoque()) <= 0:
                        input("Não é possivel efetuar compras, pois não a produtos cadastrados")  
                        break
                                
                    print(f" --------- Comprar --------- ")
                    print(f"0 - Voltar")
                    print(f"1 - Mostrar produtos")                
                    print(f"2 - Efetuar compra") 

                    try:
                        opcao = int(input("Escolha uma opção*: "))
                    except:
                         input("Informe uma opção valida")
                         os.system('cls')
                         continue
                    
                    match opcao:
                        case 0:
                            break 

                        case 1:
                            os.system('cls')
                            print(f" --------- Produtos --------- ")  
                            Estoque(database).mostrar_produtos()  
                            input("Pressione Enter para continuar.") 

                        case 2:
                            os.system('cls')                            
                            print(f" --------- Efetuar Compra --------- ")
                            venda = []    
                            venda.append(ultimo_venda_id + 1)

                            descricao = input("Descrição: ")  
                            venda.append(descricao) 
                            produtos = []  
                            while True:
                                produto_id = int(input("Informe o ID do produto que deseja comprar*: ")) 
                                quantidade = int(input("Informe a quantidade*: ")) 
                                produtos.append({"produto_id":produto_id, "quantidade":quantidade})

                                respota = input("Deseja adicionar mais um produto a compra (s/n)? ")
                                if respota != 's':
                                    break

                            venda.append(produtos)     
                            venda = Venda(database, venda[0],venda[1], venda[2]) 
                            os.system('cls')
                            print(f" --------- Detalhes da compra --------- ")
                            Controle_Venda(database).realizar_venda(venda)
                            ultimo_venda_id += 1 
                            
            case 3:                
                os.system('cls')
                if len(Controle_Venda(database).vendas()) <= 0:
                    input("Nenhuma venda foi realizada")  
                else:                
                    print(f" --------- Relatorio de Vendas --------- ")                                      
                    Controle_Venda(database).relatorio_vendas()
                    input("Pressione enter para continuar.")                                      

            case _:
                print("Falha no engano")

        os.system('cls')

        
    
