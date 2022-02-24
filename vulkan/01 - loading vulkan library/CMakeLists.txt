cmake_minimum_required(VERSION 3.19)

project(01-loading_vulkan_library
    VERSION 1.0.0
    DESCRIPTION "get into game dev - 01 - loading vulkan library"
    HOMEPAGE_URL https://youtu.be/c8WwICaKx3k
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
    ${PROJECT_SOURCE_DIR}/Finished/engine.cpp
    ${PROJECT_SOURCE_DIR}/Finished/engine.h
    ${PROJECT_SOURCE_DIR}/Finished/main.cpp
)

target_include_directories(main PRIVATE ${PROJECT_SOURCE_DIR}/Finished)

include(FindVulkan)

find_package(glfw3 3.3 REQUIRED)

target_link_libraries(main PRIVATE glfw Vulkan::Vulkan)
