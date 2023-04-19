import tkinter as tk
from tkinter import filedialog
import networkx as nx
import matplotlib.pyplot as plt

class Grafo:

    def __init__(self, numeroVertices):
        self.numeroVertices = numeroVertices  
        self.arestas = []    

    def adicionarAresta(self, vertice_1, vertice_2, peso):
        self.arestas.append([vertice_1, vertice_2, peso])

    def encontrarPai(self, pais, vertice):
        if pais[vertice] == vertice:
            return vertice
        return self.encontrarPai(pais, pais[vertice])

    def unir(self, pais, altura, vertice_1, vertice_2):
        
        # une dois conjuntos em um único conjunto
        pai_1 = self.encontrarPai(pais, vertice_1)
        pai_2 = self.encontrarPai(pais, vertice_2)

        if altura[pai_1] < altura[pai_2]:
            pais[pai_1] = pai_2
        elif altura[pai_1] > altura[pai_2]:
            pais[pai_2] = pai_1
        else:
            pais[pai_2] = pai_1
            altura[pai_1] += 1

            
    def kruskal(self):
      arestasArvoreGeradoraMinima = []             

      indiceArestaMenorPeso = 0        
      indiceArestaAdicionadaNaArvore = 0       

      if not self.arestas:
          print("Não há arestas para construir a árvore geradora mínima.")
          return

      self.arestas = sorted(self.arestas, key=lambda item: item[2])  

      pais = []
      altura = []

      for vertice in range(self.numeroVertices):
          pais.append(vertice)
          altura.append(0)

      while indiceArestaAdicionadaNaArvore < self.numeroVertices - 1 and indiceArestaMenorPeso < len(self.arestas):
          
          # pega a aresta de menor peso
          vertice_1, vertice_2, peso = self.arestas[indiceArestaMenorPeso]   
          indiceArestaMenorPeso += 1

          pai_1 = self.encontrarPai(pais, vertice_1)
          pai_2 = self.encontrarPai(pais, vertice_2)

          # se a aresta não forma um ciclo, adiciona-a ao resultado
          if pai_1 != pai_2:
              indiceArestaAdicionadaNaArvore += 1
              arestasArvoreGeradoraMinima.append([vertice_1, vertice_2, peso])
              self.unir(pais, altura, pai_1, pai_2)

      # imprime a árvore geradora mínima
      print("Arestas da árvore geradora mínima:")
      for vertice_1, vertice_2, peso in arestasArvoreGeradoraMinima:
          print(f"{vertice_1} - {vertice_2}: {peso}")

      # cria o grafo com as arestas da árvore geradora mínima
      G = nx.Graph()
      for vertice_1, vertice_2, peso in arestasArvoreGeradoraMinima:
          G.add_edge(vertice_1, vertice_2, weight=peso)

      pos = nx.spring_layout(G)
      edge_labels = nx.get_edge_attributes(G, 'weight')
      
      plt.figure(figsize=(40, 77))

      nx.draw_networkx_nodes(G, pos, node_color='w')
      nx.draw_networkx_edges(G, pos)
      nx.draw_networkx_labels(G, pos)
      nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

      plt.show()
       

# Interface do Usuário
class Aplicacao(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Algoritmo de Kruskal")
        self.master.geometry("500x300")
        self.pack()
        self.criarWidgets()

    def criarWidgets(self):
        self.titulo = tk.Label(self, text="Implementação do Algoritmo de Kruskal", font="bold")
        self.titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.botaoSelecionarArquivo = tk.Button(self, text="Selecionar um Arquivo", command=self.selecionarArquivo)
        self.botaoSelecionarArquivo.grid(row=1, column=0,  columnspan=2, padx=10, pady=5)

        self.rotuloCaminhoArquivo = tk.Label(self, text="Nenhum arquivo selecionado.")
        self.rotuloCaminhoArquivo.grid(row=2, columnspan=2, column=0, padx=10, pady=5)

        self.rotuloConteudoArquivo = tk.Label(self, text="")

        self.botaoExecutarAcao = tk.Button(self, text="Executar Ação", state="disabled", command=self.executarAcao)
        self.botaoExecutarAcao.grid(row=5, column=0,  columnspan=2, padx=10, pady=10)

        self.botaoSair = tk.Button(self, text="Sair", command=self.master.quit)
        self.botaoSair.grid(row=6, column=0,  columnspan=2, padx=10, pady=10)

    def selecionarArquivo(self):
        caminhoArquivo = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])
        self.rotuloCaminhoArquivo.config(text=caminhoArquivo)

        with open(caminhoArquivo, "r") as arquivo:
            conteudoArquivo = arquivo.read()
            self.rotuloConteudoArquivo.config(text=conteudoArquivo)

            self.listaConteudoArquivo = conteudoArquivo.splitlines()

        self.botaoExecutarAcao.config(state="normal")

    def executarAcao(self):
        grafo = Grafo(1005)

        tuplas = []
        for linha in self.listaConteudoArquivo:
            valores = linha.strip().split()
            tupla = (int(valores[0]), int(valores[1]))
            tuplas.append(tupla)

        quantTuplas = len(tuplas)

        for tupla in tuplas:
            grafo.adicionarAresta(tupla[0], tupla[1], quantTuplas)
            quantTuplas -= 1

        
        grafo.kruskal()
        


root = tk.Tk()
app = Aplicacao(master=root)
app.mainloop()
