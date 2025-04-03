#ifndef INIT_GL_H
#define INIT_GL_H

#include <GLFW/glfw3.h>

extern GLFWwindow* window;

void initOpenGL();
void processInput(GLFWwindow* window);
void toggleCursor(GLFWwindow* window);

#endif
