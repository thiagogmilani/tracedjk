##!/usr/bin/python 3.5  
## coding: utf-8 
## Developed and implemented by Thiago Milani

# COMANDO TRACEROUTE

# -n = EXIBE APENAS O ENDEREÇO IP E O TEMPO.
# -q 3 = LIMITA APENAS 3 TESTES POR ROTEADOR.
# -w 5 = AUMENTA O TEMPO DE RESPOSTA DE CARA ROTEADOR PARA 5 SEGUNDOS.
# -m 99 = LIMITA O NUMERO MAXINO DE ROTEADORES DE BUSCA

##### IMPORTA AS BIBLIOTECAS NECESSÁRIAS #####

import os
import sys
import socket
from pprint import pprint
from collections import defaultdict


##############################################################################################

class Graph:
  def __init__(self):
    self.nodes = set()
    self.edges = defaultdict(list)
    self.distances = {}

  def add_node(self, value):
    self.nodes.add(value)

  def add_edge(self, from_node, to_node, distance):
    self.edges[from_node].append(to_node)
    self.edges[to_node].append(from_node)
    self.distances[(from_node, to_node)] = distance
    self.distances[(to_node, from_node)] = distance

def dijsktra(graph, initial):
  visited = {initial: 0}
  path = {}

  nodes = set(graph.nodes)

  while nodes: 
    min_node = None

    for node in nodes:

      if node in visited:
        if min_node is None:
          min_node = node
        elif visited[node] < visited[min_node]:
          min_node = node

    if min_node is None:
      break

    nodes.remove(min_node)
    current_weight = visited[min_node]

    for edge in graph.edges[min_node]:
      weight = current_weight + graph.distances[(min_node, edge)]
      if edge not in visited or weight < visited[edge]:
        visited[edge] = weight
        path[edge] = min_node

  return visited, path

##############################################################################################

def traceroute():
	##### EXECUTA O COMANDO TRACEROUTE N VEZES E ARMAZENA O RESULTADO EM ARQUIVO #####
	for i in range (int(N)):

		os.system('traceroute -n -q 1 -w 5 -m 99 '+str(site)+' > traceroute'+str(i+1)+'.txt')

def iporigem():
	##### IDENTIFICA O IP DE ORIGEM #####
	router = open('ips.txt','r')
	ori = router.readline()[:-1]
	router.close()
	return (ori)

def ipdestino(dominio):
	##### IDENTIFICA O IP DE DESTINO #####
	out, addresses = [], socket.getaddrinfo(str(dominio), 80)
	for address in addresses:

	    if address[-1][0] not in out:
	        out.append(address[-1][0])

	des = out[0]
	return (des)

def criaarq():
	##### CRIA OS ARQUIVOS .TXT PARA ARMAZENAR OS IPS E OS TEMPOS CORRESPONDENTES #####
	os.system('touch ips.txt')
	os.system('touch times.txt')

def definegrafo(N):
	##### A CADA ITERAÇÃO VERIFICA UM DOS ARQUIVOS CRIADO #####
	for i in range(int(N)):

		router = open('traceroute'+str(i+1)+'.txt','r')	
		##### ITERAÇÃO QUE VERIFICA CADA LINHA DO ARQUIVO E CAPTURA APENAS A COLUNA DOS IPS #####
		for line in router:

			cpl = (line.split(' '))
			if cpl[0]== '':

				if cpl[3][0]!='*':
					w_ips = open('ips.txt','a')
					w_time = open('times.txt','a')
					w_ips.write (cpl[3])
					w_ips.write ('\n')
					w_time.write (cpl[5])
					w_time.write ('\n')
					w_ips.close()
					w_time.close()
					destino = cpl[3]

			else:

				if cpl[2][0]!='*':
					w_ips = open('ips.txt','a')
					w_time = open('times.txt','a')
					w_ips.write (cpl[2])
					w_ips.write ('\n')
					w_time.write (cpl[4])
					w_time.write ('\n')
					w_ips.close()
					w_time.close()
					destino = cpl[2]

		w_ips = open('ips.txt','a')
		w_time = open('times.txt','a')
		w_ips.close()
		w_time.close()
		router.close()

##### GERA O GRAFO PARA IMPRESSÃO #####
def geragrafo():
	##### CRIAO O GRAFO E INICIA ELE TODO ZERADO#####
	route = open('ips.txt','r')
	g = {}
	for x in route:	
		g[x] = []
	route.close()
	
	##### ATRIBUE NAS VARIÁVEIS O CONTEÚDO DOS ARQUIVOS DE ROTA, TEMPO E O NÚMERO DE LINHAS DO ARQUIVO #####
	num_lines = sum(1 for line in open ('ips.txt'))
	time = open('times.txt','r')
	route = open('ips.txt','r')
	
	##### PREENCHE O GRAFO COM O OS IPS NOS VERTICES E O TEMPO NAS ARESTAS #####
	for x in  range (0, num_lines-1):
		
		sourse_ip = route.readline()
		pos = route.tell()
		dst_ip = route.readline()
		route.seek(pos)
		t = time.readline()
		
		##### VERIFICA SE O IP DE ORIGEM DA ITERAÇÃO É IGUAL O IP DE DESTINO FINAL #####
		if sourse_ip[:-1] != destino:
			g[sourse_ip].append((dst_ip[:-1],t[:-1]))		
	route.close()
	time.close()
	return (g)




##### MAIN #####
##### CAPTURA O DOMÍNIO QUE SERÁ RASTREADO #####
## Developed and implemented by Thiago Milani

os.system('clear')
site = input('DIGITE O DOMÍNIO A SER RASTREADO: ')
print ('\n')

N = input('DIGITE O NÚMERO DE VERIFICAÇÕES A SER REALIZADA: ')
print ('\n')

##### CHAMADA DAS FUNÇÕES PRINTIPAIS #####
traceroute()
criaarq()
definegrafo(N)
origem = iporigem()
destino = ipdestino(site)

##### DETERMINA O NÍMERO DE LINHAS A PERCORRER E INICIA OS ARQUIVOS #####
num_lines = sum(1 for line in open ('ips.txt'))
times = open('times.txt','r')
route = open('ips.txt','r')

##### PREENCHE O GRAFO COM O OS IPS NOS VERTICES (NODE) E O TEMPO NAS ARESTAS (EDGE) #####

# INICIA O OBJETO G EM GRAPH
g = Graph()

# REPETIÇÃO PARA PERCORRER TODAS AS LINHAS DOS ARQUIVOS
for x in  range (0, num_lines-1):

	ip = route.readline()
	# ADD NOVO NODE AO OBJETO G (GRAPH)
	g.add_node(ip[:-1])
	pos = route.tell()
	dst_ip = route.readline()
	route.seek(pos)
	t = times.readline()
	# ADD NOVO EDGE AO OBJETO G (GRAPH)
	g.add_edge(ip[:-1],dst_ip[:-1],float(t[:-1]))

route.close()
times.close()

# PRINT DO GRAFO E DIJKSTRA
print ('CAMINHOS POSSÍVEIS ATÉ O DOMÍNIO '+str(site)+'('+str(destino)+') :\n')
pprint (geragrafo())
print ('\n\n\n')
print ('MENORES CAMINHOS COM DIJKSTRA :\n')
djk = (dijsktra(g, origem))
pprint (djk)

# ARMAZENA RESULTADO DO DIJKSTRA EM ARQUIVO
resultado = open('resultado.txt','a')
resultado.write('\nMENORES CAMINHOS COM DJIKSTRA: \n\n')
resultado.write (str(djk))
resultado.write('\n')
resultado.close()

## Developed and implemented by Thiago Milani