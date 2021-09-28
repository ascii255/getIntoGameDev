#include "shaders.h"

unsigned int util::load_shader(const char* vertexFilepath, const char* fragmentFilePath) {
	//read the contents of the files, dump to strings
	std::ifstream fileReader;
	std::stringstream bufferedLines;
	std::string line;

	fileReader.open(vertexFilepath);
	//getline returns 0 on eof
	while (std::getline(fileReader, line)) {
		bufferedLines << line << '\n';
		//std::cout << line << '\n';
	}
	// str() : returns the contents of the stringstream as an std::string
	// the string must be copied to another variable because it isn't a 
	// persistent object within the stringstream.
	// c_str() : converts a c++-style std string to a c-style string, ie a char*
	std::string vertexShaderSource = bufferedLines.str();
	const char* vertexSrc = vertexShaderSource.c_str();
	//std::cout << vertexShaderSource << '\n';

	//calling str("newstring") resets the stringstream
	//this is not necessary, these objects are scoped to the function
	//and will be cleaned when the function ends.
	//it's mostly just to show how to do this sort of thing in a larger program.
	bufferedLines.str("");
	fileReader.close();

	fileReader.open(fragmentFilePath);
	while (std::getline(fileReader, line)) {
		bufferedLines << line << '\n';
	}
	std::string fragmentShaderSource = bufferedLines.str();
	const char* fragmentSrc = fragmentShaderSource.c_str();

	unsigned int vertexShader = glCreateShader(GL_VERTEX_SHADER);
	glShaderSource(vertexShader, 1, &vertexSrc, NULL);
	glCompileShader(vertexShader);

	int success;
	char errorLog[1024];
	glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
	if (!success) {
		glGetShaderInfoLog(vertexShader, 1024, NULL, errorLog);
		std::cout << "Vertex Shader compilation error:\n" << errorLog << '\n';
	}

	unsigned int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
	glShaderSource(fragmentShader, 1, &fragmentSrc, NULL);
	glCompileShader(fragmentShader);

	glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &success);
	if (!success) {
		glGetShaderInfoLog(fragmentShader, 1024, NULL, errorLog);
		std::cout << "fragment Shader compilation error:\n" << errorLog << '\n';
	}

	unsigned int shader = glCreateProgram();
	glAttachShader(shader, vertexShader);
	glAttachShader(shader, fragmentShader);
	glLinkProgram(shader);

	glGetProgramiv(shader, GL_LINK_STATUS, &success);
	if (!success) {
		glGetProgramInfoLog(shader, 1024, NULL, errorLog);
		std::cout << "Shader linking error:\n" << errorLog << '\n';
	}

	glDeleteShader(vertexShader);
	glDeleteShader(fragmentShader);

	return shader;
}