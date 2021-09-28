#pragma once
#include "../view/rectangle_model.h"
#include "../view/material.h"

struct CubeCreateInfo {
	glm::vec3 position, eulers;
	RectangleModel* model;
	Material* material;
};

class WoodenCube {
public:
	glm::vec3 position, eulers;
	RectangleModel* model;
	Material* material;
	WoodenCube(CubeCreateInfo* createInfo);
	void update();
	void draw(unsigned int shader);
};