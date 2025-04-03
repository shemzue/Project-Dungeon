#include <GLFW/glfw3.h>
#include <iostream>
#include "initGL.h"
#include "imgui.h"
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"

// Variável global para armazenar a janela
GLFWwindow* window = nullptr; // Define a variável apenas aqui

void initOpenGL() {
    std::cout << "Inicializando OpenGL..." << std::endl;

    if (!glfwInit()) {
        std::cerr << "Erro ao inicializar GLFW!" << std::endl;
        exit(EXIT_FAILURE);
    }

    window = glfwCreateWindow(800, 600, "Jogo", NULL, NULL);
    if (!window) {
        std::cerr << "Erro ao criar a janela GLFW!" << std::endl;
        glfwTerminate();
        exit(EXIT_FAILURE);
    }

    std::cout << "Janela criada com sucesso: " << window << std::endl;
    glfwMakeContextCurrent(window);

    // Inicializa o ImGui
    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGuiIO& io = ImGui::GetIO();
    (void)io;
    ImGui_ImplGlfw_InitForOpenGL(window, true);
    ImGui_ImplOpenGL3_Init("#version 330");

    std::cout << "ImGui inicializado com sucesso!" << std::endl;
}


void processInput(GLFWwindow* window) {
    if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);
}
