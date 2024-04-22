from estoque import Estoque


class FilaPedidos:
    def __init__(self):
        self.pedidos_registrados = {}
        self.pedidos_processados = {}
        self.numero_pedido = 1    
        self.estoque = Estoque()
      
    def registrar_pedido(self, pedido: list = []):
        self.pedidos_registrados.update({f'Pedido#{self.numero_pedido}': pedido})
        print(f'pedido: {pedido}')
        print(f'{self.pedidos_registrados}  REGISTRADO!')
       
        self.numero_pedido += 1

    def processar_pedido(self):
        chave = list(self.pedidos_registrados.keys())[0]
        valor = list(self.pedidos_registrados.values())[0]

        self.pedidos_processados.update({chave: valor})
        self.remover_primeiro_item_dicionario()
        print("Pedidos registrados:", self.pedidos_registrados)
        print("Pedidos processados:", self.pedidos_processados)
    
    def remover_primeiro_item_dicionario(self):
        chave = next(iter(self.pedidos_registrados))
        valor = self.pedidos_registrados.pop(chave)
        return chave, valor

    def retornar_itens_pelo_valor(self, pedido):
        return [item for item in self.pedidos_registrados[pedido]]
     