#include <glad/glad.h>
#include "material.h"
#define STB_IMAGE_IMPLEMENTATION
#include "../stb_image.h"

Material::Material(MaterialCreateInfo* createInfo) {
	int texWidth, texHeight, nrChannels;
	unsigned char* data = stbi_load(createInfo->filename, &texWidth, &texHeight, &nrChannels, STBI_rgb_alpha);
	glCreateTextures(GL_TEXTURE_2D, 1, &texture);
	glTextureStorage2D(texture, 1, GL_RGBA8, texWidth, texHeight);
	glTextureSubImage2D(texture, 0, 0, 0, texWidth, texHeight, GL_RGBA, GL_UNSIGNED_BYTE, data);
	glTextureParameteri(texture, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTextureParameteri(texture, GL_TEXTURE_WRAP_T, GL_REPEAT);
	glTextureParameteri(texture, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
	glTextureParameteri(texture, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	stbi_image_free(data);
}

void Material::use(unsigned int shader) {
	glUseProgram(shader);
	glBindTextureUnit(0, texture);
}

Material::~Material() {
	glDeleteTextures(1, &texture);
}