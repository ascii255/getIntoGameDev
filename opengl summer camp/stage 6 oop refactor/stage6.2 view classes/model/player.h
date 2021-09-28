#pragma once
#include "../config.h"

struct PlayerCreateInfo {
	glm::vec3 position, eulers;
};

class Player {
public:
	glm::vec3 position, eulers;
	Player(PlayerCreateInfo* createInfo);
	void update(unsigned int shader);
};