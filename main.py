from estoque import Estoque
from fila import FilaPedidos
from venda import PilhaVendas
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox


# Criação da classe principal da loja

class AppLoja(Estoque, FilaPedidos, PilhaVendas):
    def __init__(self):
        super().__init__()

        # Instância dos objetos Estoque, FilaPedidos e PilhaVendas
        self.estoque = Estoque()
        self.fila_pedidos = FilaPedidos()
        self.pilha_vendas = PilhaVendas(self.fila_pedidos, self.estoque)

        # Criação da janela principal
        self.root = tk.Tk()
        self.root.title('VitaNova')
        self.root.resizable(False, False)
        
        # Configuração da posição e do tomanho da janela principal
        largura_janela = 840
        altura_janela = 520
        self.centralizarJanela(self.root, largura_janela, altura_janela)

        # Estruturas da Janela Principal
    
        self.label_titulo = tk.Label(self.root, text='Loja VitaNova', font='Arial 26 bold')
        self.label_titulo.place(x=300, y=10)

        self.botao1 = ctk.CTkButton(self.root, text='Add. Produto', corner_radius=8, width=107, height=25, font=('System', 14), command=self.janela_addproduto)
        self.botao1.place(x=93, y=415)

        self.botao7 = ctk.CTkButton(self.root, text='Rem. Produto', corner_radius=8, width=107, height=25, font=('System', 14), command=self.removerProduto)
        self.botao7.place(x=93, y=440)

        self.botao2 = ctk.CTkButton(self.root, text='Reg. Pedido', corner_radius=8, width=107, height=25, font=('System', 14), command=self.janela_registrar_pedido)
        self.botao2.place(x=363, y=415)

        self.botao3 = ctk.CTkButton(self.root, text='Pro. Pedido', corner_radius=8, width=107, height=25, font=('System', 14), command=self.processarPedido)
        self.botao3.place(x=363, y=440)

        self.botao4 = ctk.CTkButton(self.root, text='Pro. Venda', corner_radius=8, width=107, height=25, font=('System', 14), command=self.processarVenda)
        self.botao4.place(x=643, y=415)

        self.botao5 = ctk.CTkButton(self.root, text='Desf. Venda', corner_radius=8, width=107, height=25, font=('System', 14), command=self.desfazerVenda)
        self.botao5.place(x=643, y=440)

        self.botao6 = ctk.CTkButton(self.root, text='Sair', corner_radius=12, width=80, height=35, font=('System', 14), command=lambda: self.root.destroy())
        self.botao6.place(x=750, y=480)

        self.label_estoque = tk.Label(self.root, text='Estoque', font='Arial 16 bold')
        self.label_estoque.place(x=100, y=80)

        self.estoque_listbox = tk.Listbox(self.root, width=28, height=18, relief='solid')
        self.estoque_listbox.place(x=60, y=120)

        self.label_filapedidos = tk.Label(self.root, text='Fila de Pedidos', font='Arial 16 bold')
        self.label_filapedidos.place(x=335, y=80)
        
        self.filapedidos_listbox = tk.Listbox(self.root, width=28, height=8, relief='solid')
        self.filapedidos_listbox.place(x=330, y=120)
        self.filapedidos_listbox.bind('<Double-Button-1>', self.ver_pedidos_registrados)

        self.label_pedidos_processados = tk.Label(self.root, text='Pedidos Processados', font='Arial 15 bold')
        self.label_pedidos_processados.place(x=310, y=255)

        self.filapedidos_processados_listbox = tk.Listbox(self.root, width=28, height=7, relief='solid')
        self.filapedidos_processados_listbox.place(x=330, y=295)

        self.label_vendas = tk.Label(self.root, text='Vendas', font='Arial 16 bold')
        self.label_vendas.place(x=650, y= 80)

        self.vendas_listbox = tk.Listbox(self.root, width=28, height=18, relief='solid')
        self.vendas_listbox.place(x=610, y=120)
        self.atualizarListbox()
        
    # Função criada para remover um produto adicionado a loja. Ele remove o produto selecionado na listbox ao apertar o botao Remover produto (Rem. Produto)

    def removerProduto(self):
        indices_selecionados = self.estoque_listbox.curselection()

        if indices_selecionados:
            indice_selecionado = indices_selecionados[0]
            produto_selecionado = self.estoque_listbox.get(indice_selecionado)
            condicao_remover = messagebox.askyesno('Remover', f'Tem certeza que deseja remover o item: {produto_selecionado}')

            if condicao_remover:
                self.estoque.remover_produto(produto_selecionado)
                self.atualizarListbox()
            else:
                pass
        else:
            messagebox.showwarning('Erro', 'Nenhum item selecionado.')

    # Função criada para sempre centralizar a janela aberta de acordo com a resolução do monitor

    def centralizarJanela(self, root, largura_janela, altura_janela):
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()

        x = (largura_tela - largura_janela) // 2
        y = (altura_tela -altura_janela) // 2

        root.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')
    
    # Função criada para atualizar os itens nas listbox em tempo real

    def atualizarListbox(self):
        self.estoque_listbox.delete(0, tk.END)
        self.filapedidos_listbox.delete(0, tk.END)
        self.filapedidos_processados_listbox.delete(0, tk.END)
        self.vendas_listbox.delete(0, tk.END)

        for item in self.estoque.produtos:
            self.estoque_listbox.insert(tk.END, item)
        
        for item in self.fila_pedidos.pedidos_registrados:
            self.filapedidos_listbox.insert(tk.END, item)

        for item in self.fila_pedidos.pedidos_processados:
            self.filapedidos_processados_listbox.insert(tk.END, item)

        for item in self.pilha_vendas.vendas:
            self.vendas_listbox.insert(tk.END, item)

    # Função que cria janela para adicionar novos produtos a loja, aberta ao apertar o botao Adicionar Produto (Add. Produto)

    def janela_addproduto(self):
        self.root2 = tk.Toplevel()
        largura_janela = 320
        altura_janela = 200

        self.root2.title('Produto')
        self.root2.resizable(False, False)
        self.centralizarJanela(self.root2, largura_janela, altura_janela)

        pedido_label = tk.Label(self.root2, text='Adicionar Produto:', font='Arial 16 bold')
        pedido_label.grid(column=0, row=0, padx=60, pady=20)

        entrada_produto = tk.Entry(self.root2, width=20, font='Arial 14')
        entrada_produto.grid(column=0, row=1)

        botao_adicionar = ctk.CTkButton(self.root2, text='Adicionar', font=('System', 14), corner_radius=16, width=10, command=lambda: self.adicionarProduto(entrada_produto, self.estoque, self.root2))
        botao_adicionar.grid(pady=30)
        
    def adicionarProduto(self, entrada_produto, estoque, root2):
        produto = entrada_produto.get()
        produtos_lower = [p.lower() for p in estoque.produtos]

        if produto.lower():
            if produto.lower() in produtos_lower:
                messagebox.showinfo('Erro', 'Produto já existente.')
            else:
                estoque.adicionar_produto(produto)
                self.atualizarListbox()
                root2.destroy()
        
    # Função que cria janela para fazer o registro de pedidos, aberta ao apertar o botao de Registrar pedido (Reg. Pedido)

    def janela_registrar_pedido(self):
        self.root3 = tk.Toplevel()
        self.root3.resizable(False, False)
        self.root3.title('Registrar Pedido')

        largura_janela = 480
        altura_janela = 360
        self.centralizarJanela(self.root3, largura_janela, altura_janela)

        seta_direita = tk.Label(self.root3, text='-------------->', font='Arial 12 bold')
        seta_direita.place(x=210, y=58)

        seta_esquerda = tk.Label(self.root3, text='<--------------', font='Arial 12 bold')
        seta_esquerda.place(x=185, y=248)

        produtos_disponiveis_label = tk.Label(self.root3, text='Produtos Disp.', font='Arial 12 bold')
        produtos_disponiveis_label.place(x=37, y=25)

        self.produtos_disponiveis_listbox = tk.Listbox(self.root3, width=20, height=14, relief='solid')
        self.produtos_disponiveis_listbox.place(x=35, y=50)

        for item in self.estoque.produtos:
            self.produtos_disponiveis_listbox.insert(tk.END, item)

        adicionar_produto_botao = ctk.CTkButton(self.root3, text='Add', font=('System', 14), width=45, height=25, corner_radius=8, command=self.adicionar_produto_pedidos)
        adicionar_produto_botao.place(x=160, y=60)

        remover_produto_botao = ctk.CTkButton(self.root3, text='Rem', font=('System', 14), width=40, height=25, corner_radius=8, command=self.remover_produto_pedidos)
        remover_produto_botao.place(x=275, y=250)

        seu_pedido_label = tk.Label(self.root3, text='Seu Pedido', font='Arial 12 bold')
        seu_pedido_label.place(x=338, y=25)
        
        self.seu_pedido_listbox = tk.Listbox(self.root3, width=20, height=14, relief='solid')
        self.seu_pedido_listbox.place(x=325, y=50)

        finalizar_pedido = ctk.CTkButton(self.root3, text='Finalizar Pedido', font=('System', 16), width=45, height=30, corner_radius=8, command=self.finalizar_pedido)
        finalizar_pedido.place(x=180, y=310)

    # Função usada para adicionar um produto na listbox de Seus pedidos, dentro da tela de registrar pedido

    def adicionar_produto_pedidos(self):
        indice_selecionado = self.produtos_disponiveis_listbox.curselection()

        if indice_selecionado:  
            indice = indice_selecionado[0]
            produto_selecionado = self.produtos_disponiveis_listbox.get(indice)  

            self.seu_pedido_listbox.insert(tk.END, produto_selecionado)

            self.produtos_disponiveis_listbox.delete(indice)
        else:
            pass   

    # Função usada para remover um produto na listbox de Seus pedidos, dentro da tela de registrar pedido

    def remover_produto_pedidos(self):
        indice_selecionado = self.seu_pedido_listbox.curselection()

        if indice_selecionado:
            indice = indice_selecionado[0]
            produto_selecionado = self.seu_pedido_listbox.get(indice)

            self.produtos_disponiveis_listbox.insert(tk.END, produto_selecionado)
            self.seu_pedido_listbox.delete(indice)
        else:
            pass
    
    # Função criada para salvar pedido e adicionar na fila

    def ver_pedidos_registrados(self, event):
        index = self.filapedidos_listbox.curselection()[0]
        valor = self.filapedidos_listbox.get(index) 
        root = tk.Toplevel()
        root.title(valor)
        largura_janela = 300
        altura_janela = 140
        itens = self.fila_pedidos.retornar_itens_pelo_valor(valor)
        itens_formatados = ''
        c = 0

        for item in itens:
            if c == 4 or c == 8:
                itens_formatados += '\n'
            itens_formatados += str(item) + ', '
            c += 1

        self.centralizarJanela(root, largura_janela, altura_janela)
        
        pedido_label = tk.Label(root, text='Itens do Pedido:', font='Arial 14 bold')
        pedido_label.place(x=75, y=5)

        pedidos_label = tk.Label(root, text=f'{itens_formatados}', font='Arial 10')
        pedidos_label.place(x=10, y=40)

    def processarPedido(self):
        if self.filapedidos_listbox.size() == 0:
            messagebox.showinfo('Erro', 'Nao há pedidos para Processar')
        else:
            self.fila_pedidos.processar_pedido()
            self.atualizarListbox()

    def processarVenda(self):
        if self.filapedidos_processados_listbox.size() == 0:
            messagebox.showinfo('Erro', 'Nao há pedidos para Vender')
        else:
            self.pilha_vendas.processar_venda()
            self.atualizarListbox()

    def desfazerVenda(self):
        if self.vendas_listbox.size() == 0:
            messagebox.showinfo('Erro', 'Nao há Vendas feitas para desfazer')
        else:
            self.pilha_vendas.desfazer_venda()
            self.atualizarListbox()

    def finalizar_pedido(self):
        if self.seu_pedido_listbox.size() > 0:
            condicao_finalizar = messagebox.askyesno('Finalizar Pedido', 'Deseja finalizar seu pedido? Ele será adicionado a fila.')
            if condicao_finalizar:
                items = []
                for i in range(self.seu_pedido_listbox.size()):
                    item = self.seu_pedido_listbox.get(i)
                    items.append(item)

                self.fila_pedidos.registrar_pedido(items)    
                for item in items:
                    self.estoque.produtos.remove(item)
                    print(f'Item Removido: {item}')
                self.atualizarListbox()       
                self.root3.destroy() 
        else:
            self.root3.destroy()
            messagebox.showwarning('Erro', 'Adicione algo antes de fechar um pedido.')


if __name__ == '__main__':
    app = AppLoja()
    app.root.mainloop()
