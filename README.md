# Dungeon game baseado em DOOM clone style 3d (raycasting) in Python

Control: 'WASD' + mouse


![Imagem do jogo](ft.png)


# Project Dungeon

Um jogo estilo Doom retrô em Python, com raycasting, NPCs com inteligência artificial, sistema de armas por classe (mago, guerreiro, atirador), sons personalizados e menu interativo. Desenvolvido com Pygame.

---

## Como Executar

### 1. Execução recomendada: `setup.py`

O script `setup.py` realiza automaticamente os seguintes passos:

- Cria o ambiente virtual `.venv`
- Instala as dependências do projeto
- Executa o jogo uma única vez

Para executar:

```bash
python setup.py
```

Após essa primeira execução, use um dos métodos abaixo para rodar o jogo novamente.

---

### 2. Execução manual (caso o ambiente virtual já esteja criado)

Ative o ambiente virtual e execute o jogo:

**No PowerShell (Windows):**

```powershell
.venv\Scripts\Activate.ps1
python main.py
```

**Ou diretamente com o Python do ambiente:**

```powershell
.venv\Scripts\python.exe main.py
```

---

## Jogabilidade

Ao iniciar o jogo, o menu permite inserir o nome do jogador e escolher uma das classes disponíveis. Cada classe possui uma arma e sons próprios.

### Classes disponíveis:

- Mago: Bola de fogo (fireball)
- Guerreiro: Espada (slash)
- Atirador: Espingarda (shotgun)

### Controles

| Tecla             | Função            |
|-------------------|-------------------|
| W A S D           | Movimentação      |
| Mouse             | Direção/Mira      |
| Clique esquerdo   | Ataque            |
| ESC               | Pausar/Menu       |

---

## Estrutura do Projeto

```
Project-Dungeon/
├── main.py               # Inicia o jogo
├── map.py                # Lógica do mapa e minimapa
├── player.py             # Jogador e movimentação
├── weapon.py             # Armas e efeitos visuais
├── sound.py              # Sons e música de fundo
├── object_handler.py     # NPCs e objetos interativos
├── menu.py               # Menu principal
├── setup.py              # Setup automático (env + execução)
├── requirements.txt      # Dependências do projeto
├── resources/            # Imagens, sons e sprites
└── .venv/                # Ambiente virtual (não versionado)
```

---

## Requisitos

- Python 3.10 ou superior
- Pygame

Para instalar manualmente as dependências:

```bash
pip install -r requirements.txt
```

---

## Dicas e Problemas Comuns

- Se o PowerShell bloquear o script de ativação, execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

- Se o jogo não abrir novamente após rodar o `setup.py`, execute diretamente com:

```powershell
.venv\Scripts\python.exe main.py
```

---

## Melhorias Futuras (Backlog de Features)

Essas são sugestões de implementação para evolução do jogo:

- **Algoritmo de geração procedural de mapas**  
  Usar algoritmos como *Perlin Noise* ou *cellular automata* para criar mapas diferentes a cada partida, com paredes e obstáculos responsivos ao tamanho da janela.

- **Sistema de objetivos e troca de fases**  
  Criar um "goal" no mapa (por exemplo, uma saída ou item especial). Ao alcançá-lo, carregar um novo mapa ou reiniciar com mais dificuldade.

- **Melhorar menu e configurações**  
  Incluir opções de volume, resolução, modo tela cheia e navegação por teclado/mouse.

- **Textura do chão com iluminação realista**  
  Aplicar interpolação de luz com base na distância da fonte, adaptando o sombreamento no `raycasting` para o piso.

- **Portas, janelas e espelhos**  
  Estender o algoritmo de raycasting para reconhecer superfícies refletoras e interativas com raio ajustável por tipo de material.

- **Combate e projéteis visuais aprimorados**  
  Incluir sprites animados de projéteis, colisões visuais e feedback de dano nos inimigos.

- **Sistema de drop e evolução de armas**  
  Implementar drops aleatórios e upgrades com base na performance do jogador ou fases avançadas.

- **Delay personalizável em ataques**  
  Controlar o tempo de espera entre ataques por tipo de arma/classe, em vez de depender apenas de evento único por clique.

- **Munição, mana e vigor**  
  Limitar ataques com recursos que se esgotam e recarregam, como munição para armas ou barra de mana para magias.

- **Novos tipos de inimigos e classes de jogador**  
  Introduzir variedade de comportamentos e habilidades, com inimigos de longo alcance, tanques, evasivos, etc.

- **Armadilhas e debuffs**  
  Criar áreas que causam lentidão, dano ao longo do tempo, ou que afetam temporariamente o jogador.

- **Sons detalhados para cada interação**  
  Diferenciar sons de ataque, dano, movimentação, coleta e interface para maior imersão.

- **Melhoria no design e movimentação de objetos**  
  Trabalhar melhor nas sprites, física de objetos e fluidez nas animações de movimentação.

- **Storyboards e cutscenes**  
  Adicionar cenas introdutórias com base na escolha de personagem usando `pygame.Surface` e transições suaves.

- **Tela inicial (Start Game)**  
  Exibir uma capa ou título antes de entrar diretamente no menu principal, com opção de "Iniciar Jogo".

---

## Créditos e Inspiração

Este projeto foi inspirado nos tutoriais e ideias apresentadas no canal **Coder Space**, que serviram como base para a estrutura de raycasting e organização do jogo.

Todos os **designs e artes em pixel** foram criados com o auxílio do **ChatGPT como ferramenta criativa**, desde a concepção visual dos personagens até a composição dos elementos gráficos do cenário.
