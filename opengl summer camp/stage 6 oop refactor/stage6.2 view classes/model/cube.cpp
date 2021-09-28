#include "cube.h"

WoodenCube::WoodenCube(CubeCreateInfo* createInfo) {
	this->model = createInfo->model;
	this->material = createInfo->material;
	this->position = createInfo->position;
	this->eulers = createInfo->eulers;
}

void WoodenCube::update() {
	float angle{ glm::radians(static_cast<float>(10 * glfwGetTime())) };
	eulers = { angle, 2 * angle, 0.0f };
}

void WoodenCube::draw(unsigned int shader) {
	material->use(shader);
	model->draw(shader, position, eulers);
}