"""
    PyVulkan Tutorial
    - Stage three, setting up validation layers -
"""
################################# imports #####################################
from vulkan import *
import glfw
import glfw.GLFW as constants
import cffi

debug_mode = True

validationLayers = ["VK_LAYER_KHRONOS_validation",]

def createDebugUtilsMessengerEXT(instance, pCreateInfo, pAllocator):
    try:
        func = vkGetInstanceProcAddr(instance, "vkCreateDebugUtilsMessengerEXT")
        return func(instance, pCreateInfo, pAllocator)
    except:
        print("Couldn't find debug initialiser.")

def destroyDebugUtilsMessengerEXT(instance, debugMessenger, pAllocator):
    try:
        func = vkGetInstanceProcAddr(instance, "vkDestroyDebugUtilsMessengerEXT")
        func(instance, debugMessenger, pAllocator)
    except:
        print("Couldn't destroy debug messenger.")

class App:

    def __init__(self):
        self.instance = None
        self.debugMessenger = None

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
    
    def validationLayersSupported(self):
        """
            Check whether the requested validation layer/s are
            present in Vulkan's set of supported layers
        """

        try:
            availableLayers = vkEnumerateInstanceLayerProperties()
            #print(availableLayers)
        except:
            return False
        
        for testLayer in validationLayers:
            layerFound = False
            for layerProperties in availableLayers:
                #print(layerProperties)
                #print(layerProperties.__getattr__("layerName"))
                if (testLayer == layerProperties.__getattr__("layerName")):
                    layerFound = True
                    break
            
            if not layerFound:
                return False
        return True
    
    def getRequiredExtensions(self):
        glfwExtensions = glfw.get_required_instance_extensions()
        if (debug_mode):
            glfwExtensions.append(VK_EXT_DEBUG_UTILS_EXTENSION_NAME)
        return glfwExtensions

    def debugCallback(self, *args):
        #print(args)
        #print(f"validation layer: {args[2].pMessage}\n")
        print(f"validation layer: {ffi.string(args[2].pMessage)}\n")
        return VK_FALSE

    def initVulkan(self):
        self.createInstance()
        self.setupDebugMessenger()

    def createInstance(self):
        if (debug_mode and not self.validationLayersSupported()):
            print("validation layer/s not supported.\n")
            return

        appInfo = VkApplicationInfo(
            sType = VK_STRUCTURE_TYPE_APPLICATION_INFO, 
            pApplicationName = "Hello Vulkan!",
            applicationVersion = VK_MAKE_VERSION(1, 0, 0),
            pEngineName = "No Engine",
            engineVersion = VK_MAKE_VERSION(1, 0, 0),
            apiVersion = VK_API_VERSION_1_0)

        extensions = self.getRequiredExtensions()
        print(extensions)
        if (debug_mode):
            layerCount = len(validationLayers)
            layerNames = validationLayers
        else:
            layerCount = 0
            layerNames = None
        
        createInfo = VkInstanceCreateInfo(
            sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,
            pApplicationInfo = appInfo,
            enabledExtensionCount = len(extensions),
            ppEnabledExtensionNames = extensions,
            enabledLayerCount = layerCount,
            ppEnabledLayerNames = layerNames)

        try:
            self.instance = vkCreateInstance(createInfo, None)
        except:
            print("Failed to create instance!")
    
    def setupDebugMessenger(self):
        if (not debug_mode):
            return
        
        createInfo = VkDebugUtilsMessengerCreateInfoEXT(
            sType = VK_STRUCTURE_TYPE_DEBUG_UTILS_MESSENGER_CREATE_INFO_EXT,
            messageSeverity = VK_DEBUG_UTILS_MESSAGE_SEVERITY_VERBOSE_BIT_EXT +\
                                VK_DEBUG_UTILS_MESSAGE_SEVERITY_WARNING_BIT_EXT +\
                                VK_DEBUG_UTILS_MESSAGE_SEVERITY_ERROR_BIT_EXT,
            messageType = VK_DEBUG_UTILS_MESSAGE_TYPE_GENERAL_BIT_EXT +\
                            VK_DEBUG_UTILS_MESSAGE_TYPE_VALIDATION_BIT_EXT +\
                            VK_DEBUG_UTILS_MESSAGE_TYPE_PERFORMANCE_BIT_EXT,
            pfnUserCallback = self.debugCallback
        )

        #load creation function
        try:
            self.debugMessenger = createDebugUtilsMessengerEXT(self.instance, createInfo, None)
        except:
            print("couldn't create debugger")

    def mainLoop(self):
        while (not glfw.window_should_close(self.window)):
            glfw.poll_events()
        self.exit()
    
    def exit(self):
        if (debug_mode):
            #destroyDebugUtilsMessengerEXT(self.instance, self.debugMessenger, None)
            pass
        vkDestroyInstance(self.instance, None)
        glfw.destroy_window(self.window)
        glfw.terminate()

myApp = App()