#include "rectangle_model.h"
#include <glad/glad.h>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <glm/gtx/euler_angles.hpp>

RectangleModel::RectangleModel(RectangleModelCreateInfo* createInfo) {
	glUseProgram(createInfo->shader);
	float l = createInfo->size.x;
	float w = createInfo->size.y;
	float h = createInfo->size.z;
	vertices = { {
			-l / 2.0f, -w / 2.0f, -h / 2.0f, 0.0f, 0.0f, // bottom
			 l / 2.0f, -w / 2.0f, -h / 2.0f, 1.0f, 0.0f,
			 l / 2.0f,  w / 2.0f, -h / 2.0f, 1.0f, 1.0f,

			 l / 2.0f,  w / 2.0f, -h / 2.0f, 1.0f, 1.0f,
			-l / 2.0f,  w / 2.0f, -h / 2.0f, 0.0f, 1.0f,
			-l / 2.0f, -w / 2.0f, -h / 2.0f, 0.0f, 0.0f,

			-l / 2.0f, -w / 2.0f,  h / 2.0f, 0.0f, 0.0f, //top
			 l / 2.0f, -w / 2.0f,  h / 2.0f, 1.0f, 0.0f,
			 l / 2.0f,  w / 2.0f,  h / 2.0f, 1.0f, 1.0f,

			 l / 2.0f,  w / 2.0f,  h / 2.0f, 1.0f, 1.0f,
			-l / 2.0f,  w / 2.0f,  h / 2.0f, 0.0f, 1.0f,
			-l / 2.0f, -w / 2.0f,  h / 2.0f, 0.0f, 0.0f,

			-l / 2.0f,  w / 2.0f,  h / 2.0f, 1.0f, 0.0f, //left
			-l / 2.0f,  w / 2.0f, -h / 2.0f, 1.0f, 1.0f,
			-l / 2.0f, -w / 2.0f, -h / 2.0f, 0.0f, 1.0f,

			-l / 2.0f, -w / 2.0f, -h / 2.0f, 0.0f, 1.0f,
			-l / 2.0f, -w / 2.0f,  h / 2.0f, 0.0f, 0.0f,
			-l / 2.0f,  w / 2.0f,  h / 2.0f, 1.0f, 0.0f,

			 l / 2.0f,  w / 2.0f,  h / 2.0f, 1.0f, 0.0f, //right
			 l / 2.0f,  w / 2.0f, -h / 2.0f, 1.0f, 1.0f,
			 l / 2.0f, -w / 2.0f, -h / 2.0f, 0.0f, 1.0f,

			 l / 2.0f, -w / 2.0f, -h / 2.0f, 0.0f, 1.0f,
			 l / 2.0f, -w / 2.0f,  h / 2.0f, 0.0f, 0.0f,
			 l / 2.0f,  w / 2.0f,  h / 2.0f, 1.0f, 0.0f,

			-l / 2.0f, -w / 2.0f, -h / 2.0f, 0.0f, 1.0f, //back
			 l / 2.0f, -w / 2.0f, -h / 2.0f, 1.0f, 1.0f,
			 l / 2.0f, -w / 2.0f,  h / 2.0f, 1.0f, 0.0f,

			 l / 2.0f, -w / 2.0f,  h / 2.0f, 1.0f, 0.0f,
			-l / 2.0f, -w / 2.0f,  h / 2.0f, 0.0f, 0.0f,
			-l / 2.0f, -w / 2.0f, -h / 2.0f, 0.0f, 1.0f,

			-l / 2.0f,  w / 2.0f, -h / 2.0f, 0.0f, 1.0f, //front
			 l / 2.0f,  w / 2.0f, -h / 2.0f, 1.0f, 1.0f,
			 l / 2.0f,  w / 2.0f,  h / 2.0f, 1.0f, 0.0f,

			 l / 2.0f,  w / 2.0f,  h / 2.0f, 1.0f, 0.0f,
			-l / 2.0f,  w / 2.0f,  h / 2.0f, 0.0f, 0.0f,
			-l / 2.0f,  w / 2.0f, -h / 2.0f, 0.0f, 1.0f
	} };
	vertexCount = vertices.size() / 5;

	glCreateBuffers(1, &VBO);
	glCreateVertexArrays(1, &VAO);
	glVertexArrayVertexBuffer(VAO, 0, VBO, 0, 5 * sizeof(float));
	glNamedBufferStorage(VBO, vertices.size() * sizeof(float), vertices.data(), GL_DYNAMIC_STORAGE_BIT);
	glEnableVertexArrayAttrib(VAO, 0);
	glEnableVertexArrayAttrib(VAO, 1);
	glVertexArrayAttribFormat(VAO, 0, 3, GL_FLOAT, GL_FALSE, 0);
	glVertexArrayAttribFormat(VAO, 1, 2, GL_FLOAT, GL_FALSE, 3 * sizeof(float));
	glVertexArrayAttribBinding(VAO, 0, 0);
	glVertexArrayAttribBinding(VAO, 1, 0);
}

void RectangleModel::draw(unsigned int shader, glm::vec3 position, glm::vec3 eulers) {
	glUseProgram(shader);
	glm::mat4 model_transform{ glm::mat4(1.0f) };
	model_transform = glm::translate(model_transform, position);
	model_transform = model_transform * glm::eulerAngleXYZ(eulers.x, eulers.y, eulers.z);
	glUniformMatrix4fv(glGetUniformLocation(shader, "model"), 1, GL_FALSE, glm::value_ptr(model_transform));
	glBindVertexArray(VAO);
	glDrawArrays(GL_TRIANGLES, 0, vertexCount);
}

RectangleModel::~RectangleModel() {
	glDeleteBuffers(1, &VBO);
	glDeleteVertexArrays(1, &VAO);
}