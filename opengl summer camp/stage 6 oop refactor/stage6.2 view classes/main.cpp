#include "config.h"
#include "model/cube.h"
#include "model/player.h"
#include "view/shaders.h"
#include "view/rectangle_model.h"
#include "view/material.h"

GLFWwindow* initialize(int width, int height) {
	glfwInit();

	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 5);
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

	GLFWwindow* window = glfwCreateWindow(640, 480, "This is working I hope", NULL, NULL);
	if (!window) {
		std::cout << "Window creation failed\n";
		return NULL;
	}
	glfwMakeContextCurrent(window);

	if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
		std::cout << "GLAD initialization failed\n";
		return NULL;
	}

	glViewport(0, 0, 640, 480);

	return window;
}

void processInput(GLFWwindow* window, Player* player) {

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
	glfwSetCursorPos(window, static_cast<double>(640 / 2), static_cast<double>(480 / 2));

	float delta_x{ static_cast<float>(mouse_x - static_cast<double>(640 / 2)) };
	player->eulers.z -= delta_x;

	float delta_y{ static_cast<float>(mouse_y - static_cast<double>(480 / 2)) };
	player->eulers.y = std::max(std::min(player->eulers.y + delta_y, 180.0f), 0.0f);

	if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS) {
		glfwSetWindowShouldClose(window, true);
	}
}

int main() {

	int width = 640;
	int height = 480;
	float aspectRatio = (float)width / float(height);
	GLFWwindow* window = initialize(width, height);
	if (!window) {
		glfwTerminate();
		return -1;
	}
	glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_HIDDEN);

	unsigned int shader = util::load_shader("shaders/textured3Dvertex.txt", "shaders/textured3Dfragment.txt");
	glUseProgram(shader);
	glUniform1i(glGetUniformLocation(shader, "basicTexture"), 0);

	//create objects
	MaterialCreateInfo materialInfo{};
	materialInfo.filename = "textures/wood.jpeg";
	Material* woodTexture = new Material(&materialInfo);

	RectangleModelCreateInfo rectInfo{};
	rectInfo.shader = shader;
	rectInfo.size = { 1.0f, 2.0f, 1.0f };
	RectangleModel* rectModel = new RectangleModel(&rectInfo);

	CubeCreateInfo cubeInfo{};
	cubeInfo.position = { 1.0f, -3.0f, 0.5f };
	cubeInfo.eulers = { 0.0f, 0.0f, 0.0f };
	cubeInfo.model = rectModel;
	cubeInfo.material = woodTexture;
	WoodenCube* cube = new WoodenCube(&cubeInfo);

	PlayerCreateInfo playerInfo{};
	playerInfo.eulers = { 0.0f, 0.0f, 0.0f };
	playerInfo.position = { 0.0f, 0.0f, 1.0f };
	Player* player = new Player(&playerInfo);

	//set up framebuffer
	glClearColor(0.5f, 0.1f, 0.3f, 1.0f);
	glEnable(GL_DEPTH_TEST);
	glm::mat4 projection_transform = glm::perspective(45.0f, aspectRatio, 0.1f, 10.0f);
	glUniformMatrix4fv(glGetUniformLocation(shader, "projection"), 1, GL_FALSE, glm::value_ptr(projection_transform));

	while (!glfwWindowShouldClose(window)) {

		//events
		processInput(window, player);
		glfwPollEvents();

		//update
		cube->update();
		player->update(shader);
		
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		cube->draw(shader);

		glfwSwapBuffers(window);
		
	}

	//free memory
	delete cube;
	delete woodTexture;
	delete player;
	delete rectModel;
	glDeleteProgram(shader);
	glfwTerminate();

	return 0;
}