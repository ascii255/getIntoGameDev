cmake_minimum_required(VERSION 3.19)

project(05-logical_device_creation
    VERSION 1.0.0
    DESCRIPTION "get into game dev - 05 - logical device creation"
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

target_sources(main PRIVATE
    ${PROJECT_SOURCE_DIR}/logicalDevices.cpp
)

include(FindVulkan)

find_package(glfw3 3.3 REQUIRED)

target_link_libraries(main PRIVATE glfw Vulkan::Vulkan)
