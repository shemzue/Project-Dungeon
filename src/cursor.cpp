#include "cursor.h"

bool cursorEnabled = true;

void toggleCursor(GLFWwindow* window) {
    cursorEnabled = !cursorEnabled;
    glfwSetInputMode(window, GLFW_CURSOR, cursorEnabled ? GLFW_CURSOR_NORMAL : GLFW_CURSOR_DISABLED);
}
