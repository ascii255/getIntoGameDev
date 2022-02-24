cmake_minimum_required(VERSION 3.19)

project(19-textures
    VERSION 1.0.0
    DESCRIPTION "get into game dev - 19 - textures"
    HOMEPAGE_URL not_available_yet
    LANGUAGES CXX
)

add_executable(main)

set_target_properties(main PROPERTIES
    CXX_STANDARD_REQUIRED YES
    LINKER_LANGUAGE CXX
    MACOSX_BUNDLE TRUE
)

target_compile_features(main PRIVATE cxx_std_20)

file(GLOB_RECURSE SHADERS ${PROJECT_SOURCE_DIR}/shaders/*.spv)
source_group(TREE ${PROJECT_SOURCE_DIR} PREFIX Resources FILES ${SHADERS})

file(GLOB_RECURSE TEXTURES ${PROJECT_SOURCE_DIR}/../resources/tex/*.jpg)
source_group(Resources/tex FILES ${TEXTURES})

target_sources(main PRIVATE
    ${PROJECT_SOURCE_DIR}/stb_image.cpp
    ${PROJECT_SOURCE_DIR}/textures.cpp
    ${PROJECT_SOURCE_DIR}/../resources/stb_image.h
    ${SHADERS}
    ${TEXTURES}
)

target_include_directories(main PRIVATE ${PROJECT_SOURCE_DIR}/../resources)

set_source_files_properties(${SHADERS} PROPERTIES
    MACOSX_PACKAGE_LOCATION Resources/shaders
)

set_source_files_properties(${TEXTURES} PROPERTIES
    MACOSX_PACKAGE_LOCATION Resources/tex
)

if(NOT APPLE)
    add_custom_command(TARGET main PRE_BUILD
        COMMAND ${CMAKE_COMMAND} -E make_directory
            ${CMAKE_CURRENT_BINARY_DIR}/$<CONFIG>/shaders
        COMMAND ${CMAKE_COMMAND} -E copy
            ${PROJECT_SOURCE_DIR}/shaders/*.spv
            ${CMAKE_CURRENT_BINARY_DIR}/$<CONFIG>/shaders
    )
    add_custom_command(TARGET main PRE_BUILD
        COMMAND ${CMAKE_COMMAND} -E make_directory
            ${CMAKE_CURRENT_BINARY_DIR}/$<CONFIG>/tex
        COMMAND ${CMAKE_COMMAND} -E copy
            ${PROJECT_SOURCE_DIR}/../resources/tex/*.jpg
            ${CMAKE_CURRENT_BINARY_DIR}/$<CONFIG>/tex
    )
endif()

include(FindVulkan)

find_package(glfw3 3.3 REQUIRED)

target_link_libraries(main PRIVATE glfw Vulkan::Vulkan)
