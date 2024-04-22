from fila import FilaPedidos
from estoque import Estoque

class PilhaVendas:
    def __init__(self, fila_pedidos, estoque):
        self.vendas = {}
        self.fila = fila_pedidos
        self.estoque = estoque

    def processar_venda(self):
        if self.fila.pedidos_processados:
            chave = list(self.fila.pedidos_processados.keys())[0]
            valor = list(self.fila.pedidos_processados.values())[0]

            self.vendas.update({chave: valor})
            self.remover_primeiro_item_dicionario()
        else:
            print('Nao há pedidos para serem vendidos')

    def remover_primeiro_item_dicionario(self):
        chave = next(iter(self.fila.pedidos_processados))
        valor = self.fila.pedidos_processados.pop(chave)
        return chave, valor

    def desfazer_venda(self):
        if self.vendas:
            venda = next(iter(self.vendas))
            produtos_vendidos = self.vendas[venda]
            for produto in produtos_vendidos:
                self.estoque.produtos.append(produto)
            
            del self.vendas[venda]
            



