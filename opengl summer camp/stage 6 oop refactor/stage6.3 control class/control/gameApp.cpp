#include "gameApp.h"

GameApp::GameApp(GameAppCreateInfo* createInfo) {
	this->window = createInfo->window;
	this->shader = createInfo->shaders[0];
	glfwGetWindowSize(window, &width, &height);
	createMaterials();
	createModels();
	createObjects();
}

returnCode GameApp::mainLoop() {
	//events
	returnCode nextAction = processInput();
	glfwPollEvents();

	//update
	cube->update();
	player->update(shader);

	//draw
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	cube->draw(shader);

	glfwSwapBuffers(window);
	return nextAction;
}

GameApp::~GameApp() {
	delete cube;
	delete woodTexture;
	delete player;
	delete rectModel;
}

void GameApp::createMaterials() {
	MaterialCreateInfo materialInfo{};
	materialInfo.filename = "textures/wood.jpeg";
	woodTexture = new Material(&materialInfo);
}

void GameApp::createModels() {
	RectangleModelCreateInfo rectInfo{};
	rectInfo.shader = shader;
	rectInfo.size = { 1.0f, 2.0f, 1.0f };
	rectModel = new RectangleModel(&rectInfo);
}

void GameApp::createObjects() {
	CubeCreateInfo cubeInfo{};
	cubeInfo.position = { 1.0f, -3.0f, 0.5f };
	cubeInfo.eulers = { 0.0f, 0.0f, 0.0f };
	cubeInfo.model = rectModel;
	cubeInfo.material = woodTexture;
	cube = new WoodenCube(&cubeInfo);

	PlayerCreateInfo playerInfo{};
	playerInfo.eulers = { 0.0f, 0.0f, 0.0f };
	playerInfo.position = { 0.0f, 0.0f, 1.0f };
	player = new Player(&playerInfo);
}

returnCode GameApp::processInput() {
	returnCode nextAction = returnCode::CONTINUE;
	int wasdState{ 0 };
	float walk_direction{ player->eulers.z };
	bool walking{ false };

	if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS) {
		wasdState += 1;
	}

	if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS) {
		wasdState += 2;
	}

	if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS) {
		wasdState += 4;
	}

	if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS) {
		wasdState += 8;
	}

	switch (wasdState) {
	case 1:
	case 11:
		//forwards
		walking = true;
		break;
	case 3:
		//left-forwards
		walking = true;
		walk_direction += 45;
		break;
	case 2:
	case 7:
		//left
		walking = true;
		walk_direction += 90;
		break;
	case 6:
		//left-backwards
		walking = true;
		walk_direction += 135;
		break;
	case 4:
	case 14:
		//backwards
		walking = true;
		walk_direction += 180;
		break;
	case 12:
		//right-backwards
		walking = true;
		walk_direction += 225;
		break;
	case 8:
	case 13:
		//right
		walking = true;
		walk_direction += 270;
		break;
	case 9:
		//right-forwards
		walking = true;
		walk_direction += 315;
	}

	if (walking) {
		player->position += 0.1f * glm::vec3{
			glm::cos(glm::radians(walk_direction)),
			glm::sin(glm::radians(walk_direction)),
			0.0f
		};
	}

	double mouse_x, mouse_y;
	glfwGetCursorPos(window, &mouse_x, &mouse_y);
	glfwSetCursorPos(window, static_cast<double>(width / 2), static_cast<double>(height / 2));

	float delta_x{ static_cast<float>(mouse_x - static_cast<double>(width / 2)) };
	player->eulers.z -= delta_x;

	float delta_y{ static_cast<float>(mouse_y - static_cast<double>(height / 2)) };
	player->eulers.y = std::max(std::min(player->eulers.y + delta_y, 180.0f), 0.0f);

	if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS) {
		nextAction = returnCode::QUIT;
	}

	return nextAction;
}