
class Estoque:
    def __init__(self):
        self.produtos = ['Cama', 'Monitor', 'Teclado', 'Televisão']
  
    def adicionar_produto(self, produto):
        self.produtos.append(produto)
        print(f'Produtos Estoque: {self.produtos}')

    def remover_produto(self, produto):
        produtos_lower = [p.lower() for p in self.produtos]

        produto_lower = produto.lower()

        if produto_lower in produtos_lower:
            self.produtos.remove(produto)
            print(f'Produto: {produto} Removido.')
        else:
            print("Produto não encontrado no estoque.")
