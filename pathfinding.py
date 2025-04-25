from collections import deque  # Importa deque, uma estrutura de fila eficiente
from functools import lru_cache  # Importa decorador para cache de resultados de função


class PathFinding:
    def __init__(self, game):
        self.game = game  # Referência para o objeto principal do jogo
        self.map = game.map.mini_map  # Mini mapa (matriz de células representando o mundo)
        
        # Vizinhanças possíveis: cima, baixo, esquerda, direita, e diagonais
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        
        self.graph = {}  # Dicionário que vai armazenar o grafo dos caminhos válidos
        self.get_graph()  # Inicializa o grafo com os caminhos possíveis no mapa

    @lru_cache  # Usa cache para evitar cálculos repetidos em chamadas iguais
    def get_path(self, start, goal):
        # Executa BFS (busca em largura) para encontrar caminho mais curto
        self.visited = self.bfs(start, goal, self.graph)
        
        path = [goal]  # Começa a reconstrução do caminho a partir do destino
        step = self.visited.get(goal, start)  # Obtém de onde veio o destino

        # Reconstrói o caminho de trás pra frente, até chegar no início
        while step and step != start:
            path.append(step)
            step = self.visited[step]
        
        return path[-1]  # Retorna o próximo passo mais próximo do início

    def bfs(self, start, goal, graph):
        queue = deque([start])  # Inicializa fila com o ponto de partida
        visited = {start: None}  # Marca como visitado e armazena o caminho percorrido

        while queue:
            cur_node = queue.popleft()  # Remove o próximo nó a visitar
            if cur_node == goal:
                break  # Encerra se chegou ao destino
            
            next_nodes = graph[cur_node]  # Pega os vizinhos acessíveis

            for next_node in next_nodes:
                # Só visita nós ainda não visitados e que não estão ocupados por NPCs
                if next_node not in visited and next_node not in self.game.object_handler.npc_positions:
                    queue.append(next_node)
                    visited[next_node] = cur_node  # Marca de onde veio
        return visited  # Retorna todos os caminhos possíveis a partir do início

    def get_next_nodes(self, x, y):
        # Retorna vizinhos válidos (sem colisão com paredes no world_map)
        return [
            (x + dx, y + dy)
            for dx, dy in self.ways
            if (x + dx, y + dy) not in self.game.map.world_map
        ]

    def get_graph(self):
        # Percorre o mini mapa e monta o grafo de caminhos acessíveis
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:  # Se não for parede
                    # Adiciona o nó (x, y) com seus vizinhos válidos
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)
