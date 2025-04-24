import pygame
import sys

pygame.init()

# Tela
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu do Jogo")

# Fontes
FONT = pygame.font.SysFont("Arial", 28)
BIG_FONT = pygame.font.SysFont("Arial", 38, bold=True)

# Cores
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
LIGHT_BLUE = (173, 216, 230)

# Dados
CLASSES = ["Mago", "Guerreiro", "Atirador"]
player_name = ""
selected_class = 0
dropdown_open = False

# Estados
input_rect = pygame.Rect(80, 80, 250, 40)
class_button = pygame.Rect(80, 150, 250, 40)
dropdown_rects = [pygame.Rect(80, 200 + i * 40, 250, 40) for i in range(len(CLASSES))]
active_input = False

clock = pygame.time.Clock()

def draw_text(text, font, color, surface, x, y):
    txt = font.render(text, True, color)
    surface.blit(txt, (x, y))

def draw_menu():
    SCREEN.fill(BLACK)

    # Título
    draw_text("Criação de Personagem", BIG_FONT, WHITE, SCREEN, 80, 10)

    # Nome
    draw_text("Nome:", FONT, WHITE, SCREEN, 80, 50)
    pygame.draw.rect(SCREEN, LIGHT_BLUE if active_input else WHITE, input_rect, 2)

    # Garantir texto visível na caixa
    displayed_name = player_name
    while FONT.size(displayed_name)[0] > input_rect.width - 10:
        displayed_name = displayed_name[1:]

    draw_text(displayed_name or "Digite seu nome...", FONT, GRAY if not player_name else WHITE, SCREEN, input_rect.x + 5, input_rect.y + 5)

    # Classe com botão dropdown
    draw_text("Classe:", FONT, WHITE, SCREEN, 80, 120)
    pygame.draw.rect(SCREEN, WHITE, class_button, 2)
    draw_text(CLASSES[selected_class], FONT, WHITE, SCREEN, class_button.x + 5, class_button.y + 5)

    # Dropdown aberto
    if dropdown_open:
        for i, rect in enumerate(dropdown_rects):
            pygame.draw.rect(SCREEN, LIGHT_BLUE if i == selected_class else WHITE, rect, 0)
            draw_text(CLASSES[i], FONT, BLACK, SCREEN, rect.x + 5, rect.y + 5)

    # Imagem da classe
    try:
        image_path = f"resources/sprites/menu/{CLASSES[selected_class].lower()}.png"
        class_img = pygame.image.load(image_path).convert_alpha()
        class_img = pygame.transform.scale(class_img, (180, 220))
        SCREEN.blit(class_img, (WIDTH - 260, 100))
    except:
        pygame.draw.rect(SCREEN, GRAY, (WIDTH - 260, 100, 180, 220))
        draw_text("Sem imagem", FONT, BLACK, SCREEN, WIDTH - 250, 200)

    # Instruções
    draw_text("Pressione ENTER para iniciar", FONT, LIGHT_BLUE, SCREEN, 80, 550)

    pygame.display.flip()

def menu_loop():
    global player_name, selected_class, active_input, dropdown_open

    running = True
    while running:
        draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active_input = True
                    dropdown_open = False
                else:
                    active_input = False

                if class_button.collidepoint(event.pos):
                    dropdown_open = not dropdown_open
                elif dropdown_open:
                    for i, rect in enumerate(dropdown_rects):
                        if rect.collidepoint(event.pos):
                            selected_class = i
                            dropdown_open = False
                            break
                    else:
                        dropdown_open = False

            if event.type == pygame.KEYDOWN:
                if active_input:
                    if event.key == pygame.K_RETURN:
                        active_input = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.unicode.isprintable():
                        test_name = player_name + event.unicode
                        if FONT.size(test_name)[0] < input_rect.width - 10:
                            player_name = test_name
                else:
                    if event.key == pygame.K_RETURN and player_name:
                        return {
                            "name": player_name,
                            "class": CLASSES[selected_class]
                        }

        clock.tick(60)
