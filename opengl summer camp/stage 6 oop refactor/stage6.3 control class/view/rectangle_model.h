#pragma once

#include "../config.h"

struct RectangleModelCreateInfo {
	glm::vec3 size;
	unsigned int shader;
};

class RectangleModel {
public:
	unsigned int VBO, VAO, vertexCount;
	std::vector<float> vertices;
	RectangleModel(RectangleModelCreateInfo* createInfo);
	void draw(unsigned int shader, glm::vec3 position, glm::vec3 eulers);
	~RectangleModel();
};