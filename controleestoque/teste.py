class Registros(): 
  
    def __init__(self):
        self.__produtos = []
        self.__vendas = []
   
    def get_produtos(self):
        return self.__produtos 

    
    def get_vendas(self):
        return self.__vendas 
    @staticmethod
    def limpar_tela():
        if platform.system() == 'Windows' or platform.system() == 'windows':
            os.system('cls') 
        else:
            os.system('clear') 

    @staticmethod
    def converter_data(data):
        data = str(data) 
        data = data.split('-')                                
        data = f"{data[2]}/{data[1]}/{data[0]}"
        return data
    
    @staticmethod
    def inverter_data(data):
        data = str(data) 
        data = data.split('/')

        return date(int(data[2]), int(data[1]), int(data[0]))

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
            return f"ID: {self.produto_id} | {self.nome} | R$ {self.preco} | {self.quantidade} | {Helpers.converter_data(self.data_validade)}"
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

class Estoque(): 
    def __init__(self, database):        
        self.__produtos = database.get_produtos()  

    def cadastrar_produto(self, produto):        
       self.__produtos.append(produto)
    
    @staticmethod
    def produto_por_id_binaria(produto_id, produtos, db_produtos): # pesquisa binaria ainda não concluida
        if len(produtos) <= 0:
            return []  

        if len(produtos) == 1:    
            return [ db_produtos.index(produtos[0]), produtos[0] ]  

        tamanho = len(produtos) 
        meio = tamanho // 2    
                      
        if produtos[meio].get_produto_id() < produto_id:
            return Estoque.produto_por_id_binaria(produto_id, produtos[meio:], db_produtos)            
        elif  produtos[meio].get_produto_id() > produto_id:  
            return Estoque.produto_por_id_binaria(produto_id, produtos[:meio], db_produtos)            
        else:            
            return [ db_produtos.index(produtos[meio]), produtos[meio], db_produtos ]
  
if __name__ == "__main__": 
    database = Registros() 
   
    result = Estoque.produto_por_id_binaria(2, database.get_produtos(), list(database.get_produtos())) 
    print(f"Indice {result[0]} - Valor {result[1]} ")