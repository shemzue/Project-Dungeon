#ifndef MENU_H
#define MENU_H

#include "imgui/imgui.h"
#include <string>

class Menu {
public:
    static bool showMenu;
    static std::string playerName;
    static int playerClass;  // 0: Guerreiro, 1: Mago, 2: Arqueiro
    static int gender;        // 0: Masculino, 1: Feminino
    static float skinTone;    // Personalização da pele

    static void Render();  // Método para desenhar o menu
};

#endif
