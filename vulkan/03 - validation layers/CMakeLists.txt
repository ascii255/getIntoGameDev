cmake_minimum_required(VERSION 3.19)

project(03-validation_layers
    VERSION 1.0.0
    DESCRIPTION "get into game dev - 03 - validation layers"
    HOMEPAGE_URL https://youtu.be/Bsd9BtOoiNw
    LANGUAGES CXX
)

add_executable(main)

set_target_properties(main PROPERTIES
    CXX_STANDARD_REQUIRED YES
    LINKER_LANGUAGE CXX
    MACOSX_BUNDLE TRUE
)

target_compile_features(main PRIVATE cxx_std_20)

target_sources(main PRIVATE
    ${PROJECT_SOURCE_DIR}/Finished/config.h
    ${PROJECT_SOURCE_DIR}/Finished/engine.cpp
    ${PROJECT_SOURCE_DIR}/Finished/engine.h
    ${PROJECT_SOURCE_DIR}/Finished/instance.h
    ${PROJECT_SOURCE_DIR}/Finished/logging.h
    ${PROJECT_SOURCE_DIR}/Finished/main.cpp
)

target_include_directories(main PRIVATE ${PROJECT_SOURCE_DIR}/Finished)

include(FindVulkan)

find_package(glfw3 3.3 REQUIRED)

target_link_libraries(main PRIVATE glfw Vulkan::Vulkan)
