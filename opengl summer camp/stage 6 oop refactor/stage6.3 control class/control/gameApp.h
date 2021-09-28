#pragma once
#include "../config.h"
#include "../model/cube.h"
#include "../model/player.h"
#include "../view/shaders.h"
#include "../view/rectangle_model.h"
#include "../view/material.h"

struct GameAppCreateInfo {
	GLFWwindow* window;
	std::vector<unsigned int> shaders;
};

enum class returnCode {
	CONTINUE, QUIT
};

class GameApp {
public:
	GameApp(GameAppCreateInfo* createInfo);
	returnCode mainLoop();
	~GameApp();
private:
	void createMaterials();
	void createModels();
	void createObjects();
	returnCode processInput();
	GLFWwindow* window;
	unsigned int shader;
	WoodenCube* cube;
	Material* woodTexture;
	Player* player;
	RectangleModel* rectModel;
	int width, height;
};