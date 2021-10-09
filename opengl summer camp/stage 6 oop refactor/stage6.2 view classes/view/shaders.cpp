#include <fstream>
#include <sstream>
#include <string>
#include <glad/glad.h>
#include <iostream>
#include "shaders.h"

unsigned int util::load_shader(const char* vertexFilepath, const char* fragmentFilepath) {

	std::ifstream fileReader;
	std::stringstream bufferedLines;
	std::string line;

	fileReader.open(vertexFilepath);
	while (std::getline(fileReader, line)) {
		bufferedLines << line << '\n';
	}

	std::string vertexSrc = bufferedLines.str();
	const char* vertexShaderSource = vertexSrc.c_str();

	bufferedLines.str("");
	fileReader.close();

	fileReader.open(fragmentFilepath);
	while (std::getline(fileReader, line)) {
		bufferedLines << line << '\n';
	}

	std::string fragmentSrc = bufferedLines.str();
	const char* fragmentShaderSource = fragmentSrc.c_str();

	bufferedLines.str("");
	fileReader.close();

	unsigned int vertexShader = glCreateShader(GL_VERTEX_SHADER);
	//&: addressof operator
	glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
	glCompileShader(vertexShader);
	int success;
	char errorLog[1024];
	glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
	if (!success) {
		glGetShaderInfoLog(vertexShader, 1024, NULL, errorLog);
		std::cout << "Vertex shader compilation error:\n" << errorLog << '\n';
	}

	unsigned int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
	glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
	glCompileShader(fragmentShader);
	glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &success);
	if (!success) {
		glGetShaderInfoLog(fragmentShader, 1024, NULL, errorLog);
		std::cout << "Fragment shader compilation error:\n" << errorLog << '\n';
	}

	unsigned int shader = glCreateProgram();
	glAttachShader(shader, vertexShader);
	glAttachShader(shader, fragmentShader);
	glLinkProgram(shader);
	glGetProgramiv(shader, GL_LINK_STATUS, &success);
	if (!success) {
		glGetProgramInfoLog(fragmentShader, 1024, NULL, errorLog);
		std::cout << "Shader linking error:\n" << errorLog << '\n';
	}

	glDeleteShader(vertexShader);
	glDeleteShader(fragmentShader);

	return shader;
}