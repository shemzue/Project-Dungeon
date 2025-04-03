#include <GLFW/glfw3.h>
#include <iostream>
#include "menu.h"
#include "Game.h"
#include "Dungeon.h"
#include "initGL.h" 
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"

extern void initOpenGL();
extern void processInput(GLFWwindow* window);
extern void toggleCursor(GLFWwindow* window);
extern bool cursorEnabled;

int main() {
    initOpenGL();

    while (!glfwWindowShouldClose(window)) {
        processInput(window);
    
        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplGlfw_NewFrame();
        ImGui::NewFrame();
    
        if (inDungeon) {
            Dungeon::Render();  // Agora renderiza um mundo 3D, sem ImGui

        } else {
            Menu::Render();  // Menu inicial
        }
    
        ImGui::Render();
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
    
        glfwSwapBuffers(window);
        glfwPollEvents();
    }
    

    // Finaliza o ImGui corretamente
    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    ImGui::DestroyContext();   

    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}
