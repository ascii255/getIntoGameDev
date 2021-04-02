"""
    PyVulkan Tutorial
    - Stage two, creating vulkan instance -
    requirements: glfw, vulkan (pip install)
"""
################################# imports #####################################
from vulkan import *
import glfw
import glfw.GLFW as constants

class App:

    def __init__(self):
        self.initWindow()
        self.initVulkan()
        self.mainLoop()
    
    def initWindow(self):
        glfw.init()

        glfw.window_hint(constants.GLFW_CLIENT_API, constants.GLFW_NO_API)
        glfw.window_hint(constants.GLFW_RESIZABLE, constants.GLFW_FALSE)
        self.width = 640
        self.height = 480

        self.window = glfw.create_window(self.width, self.height, "Vulkan Window", None, None)
    
    def initVulkan(self):
        self.createInstance()
    
    def createInstance(self):
        appInfo = VkApplicationInfo(
            sType = VK_STRUCTURE_TYPE_APPLICATION_INFO, 
            pApplicationName = "Hello Vulkan!",
            applicationVersion = VK_MAKE_VERSION(1, 0, 0),
            pEngineName = "No Engine",
            engineVersion = VK_MAKE_VERSION(1, 0, 0),
            apiVersion = VK_API_VERSION_1_0)
        
        glfwExtensions = glfw.get_required_instance_extensions()
        #print(glfwExtensions)

        createInfo = VkInstanceCreateInfo(
            sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,
            pApplicationInfo = appInfo,
            enabledExtensionCount = len(glfwExtensions),
            ppEnabledExtensionNames = glfwExtensions,
            enabledLayerCount = 0)

        try:
            self.instance = vkCreateInstance(createInfo, None)
        except:
            print("Failed to create instance!")
    
    def mainLoop(self):
        while (not glfw.window_should_close(self.window)):
            glfw.poll_events()
        self.exit()
    
    def exit(self):
        vkDestroyInstance(self.instance, None)
        glfw.destroy_window(self.window)
        glfw.terminate()

myApp = App()