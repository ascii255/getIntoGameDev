#include "cube.h"
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

WoodenCube::WoodenCube(CubeCreateInfo* createInfo) {
	this->position = createInfo->position;
	this->eulers = createInfo->eulers;
	this->model = createInfo->model;
	this->material = createInfo->material;
}

void WoodenCube::update() {
	float angle = glm::radians(static_cast<float>(10 * glfwGetTime()));
	eulers = { angle, 2 * angle, 0.0f };
}

void WoodenCube::draw(unsigned int shader) {
	material->use(shader);
	model->draw(shader, position, eulers);
}
