#include "menu.h"
#include "Game.h"
#include "imgui.h"
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"
#include <GLFW/glfw3.h>
#include "initGL.h"

extern GLFWwindow* window;

bool Menu::showMenu = true;
std::string Menu::playerName = "Sialo";
int Menu::playerClass = 0;
int Menu::gender = 0;
float Menu::skinTone = 0.5f;

void Menu::Render() {
    if (!showMenu) return;

    ImGui::Begin("Seleção de Personagem");

    // Campo de texto para nome
    char buffer[32];
    strncpy(buffer, playerName.c_str(), sizeof(buffer));
    buffer[sizeof(buffer) - 1] = '\0';
    ImGui::InputText("Nome", buffer, sizeof(buffer));
    playerName = std::string(buffer);

    // Seletor de classe
    const char* classes[] = { "Guerreiro", "Mago", "Arqueiro" };
    ImGui::Combo("Classe", &playerClass, classes, IM_ARRAYSIZE(classes));

    // Seletor de gênero
    const char* genders[] = { "Masculino", "Feminino" };
    ImGui::Combo("Gênero", &gender, genders, IM_ARRAYSIZE(genders));

    // Slider para personalização da pele
    ImGui::SliderFloat("Tom de Pele", &skinTone, 0.0f, 1.0f);

    // Botão para começar o jogo
    if (ImGui::Button("Iniciar Jogo")) {
        showMenu = false;  // Fecha o menu
        Game::StartGame();  // Inicia o jogo e coloca o player na dungeon
    }

    ImGui::End();
}
