#include "Dungeon.h"
#include <iostream>
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"
#include <GL/gl.h>
#include <GLFW/glfw3.h>

extern GLFWwindow* window;  // Referência à janela principal

void Dungeon::Render() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);  // Limpa a tela

    // Configura a câmera (provisória, precisa de uma classe de câmera)
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    // Renderiza um "chão" de paralelepípedos simples
    glColor3f(0.5f, 0.5f, 0.5f);  // Cinza
    glBegin(GL_QUADS);
        glVertex3f(-5.0f, 0.0f, -5.0f);
        glVertex3f( 5.0f, 0.0f, -5.0f);
        glVertex3f( 5.0f, 0.0f,  5.0f);
        glVertex3f(-5.0f, 0.0f,  5.0f);
    glEnd();

    glfwSwapBuffers(window);  // Atualiza a tela
}
