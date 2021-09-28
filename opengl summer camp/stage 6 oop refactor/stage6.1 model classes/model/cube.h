#pragma once
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <vector>

struct CubeCreateInfo {
	glm::vec3 position, eulers;
	unsigned int shader;
};

class WoodenCube {
public:
	glm::vec3 position, eulers;
	unsigned int VBO, VAO, vertexCount;
	std::vector<float> vertices;
	WoodenCube(CubeCreateInfo* createInfo);
	void update();
	void draw(unsigned int shader);
	~WoodenCube();
};