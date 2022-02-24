cmake_minimum_required(VERSION 3.19)

project(18-uniform_buffer_objects
    VERSION 1.0.0
    DESCRIPTION "get into game dev - 18 - uniform buffer objects"
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

target_sources(main PRIVATE
    ${PROJECT_SOURCE_DIR}/uniformBufferObjects.cpp
    ${SHADERS}
)

set_source_files_properties(${SHADERS} PROPERTIES
    MACOSX_PACKAGE_LOCATION Resources/shaders
)

if(NOT APPLE)
    add_custom_command(TARGET main PRE_BUILD
        COMMAND ${CMAKE_COMMAND} -E make_directory
            ${CMAKE_CURRENT_BINARY_DIR}/$<CONFIG>/shaders
        COMMAND ${CMAKE_COMMAND} -E copy
            ${PROJECT_SOURCE_DIR}/shaders/*.spv
            ${CMAKE_CURRENT_BINARY_DIR}/$<CONFIG>/shaders
    )
endif()

include(FindVulkan)

find_package(glfw3 3.3 REQUIRED)

target_link_libraries(main PRIVATE glfw Vulkan::Vulkan)
