"""
    PyVulkan Tutorial
    - Stage four, setting up a hardware and logical device -
"""
################################# imports #####################################
from vulkan import *
import glfw
import glfw.GLFW as constants
import cffi

"""
    Declare whether to run in debug mode,
    and specify the validation layers which will run.
"""
debug_mode = True
validationLayers = ["VK_LAYER_KHRONOS_validation",]

"""
    Helper functions to create and destroy deguggers.
"""
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

#stores the indices of different queue families within vulkan
class queueFamilyIndices:
    def __init__(self):
        self.graphicsFamily = None
    
    def complete(self):
        return (self.graphicsFamily is not None)

class App:

    def __init__(self):
        self.window = None
        self.instance = None
        self.debugMessenger = None
        self.physicalDevice = VK_NULL_HANDLE
        self.device = None
        self.graphicsQueue = None

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
        except:
            return False
        
        for testLayer in validationLayers:
            layerFound = False
            for layerProperties in availableLayers:
                if (testLayer == layerProperties.__getattr__("layerName")):
                    layerFound = True
                    break
            
            if not layerFound:
                return False
        return True
    
    def getRequiredExtensions(self):
        """
            Return the set of extensions which glfw will need to
            run the app.
        """
        glfwExtensions = glfw.get_required_instance_extensions()
        if (debug_mode):
            glfwExtensions.append(VK_EXT_DEBUG_UTILS_EXTENSION_NAME)
        return glfwExtensions

    def debugCallback(self, *args):
        print(f"validation layer: {ffi.string(args[2].pMessage)}\n")
        return VK_FALSE

    def initVulkan(self):
        self.createInstance()
        self.setupDebugMessenger()
        self.pickPhysicalDevice()
        self.createLogicalDevice()

    def createInstance(self):
        if (debug_mode and not self.validationLayersSupported()):
            raise RuntimeError("validation layer/s not supported.\n")
            return

        appInfo = VkApplicationInfo(
            sType = VK_STRUCTURE_TYPE_APPLICATION_INFO, 
            pApplicationName = "Hello Vulkan!",
            applicationVersion = VK_MAKE_VERSION(1, 0, 0),
            pEngineName = "No Engine",
            engineVersion = VK_MAKE_VERSION(1, 0, 0),
            apiVersion = VK_API_VERSION_1_0)

        extensions = self.getRequiredExtensions()
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
            raise RuntimeError("Failed to create instance!")
    
    def setupDebugMessenger(self):
        if (not debug_mode):
            return
        
        createInfo = VkDebugUtilsMessengerCreateInfoEXT(
            sType = VK_STRUCTURE_TYPE_DEBUG_UTILS_MESSENGER_CREATE_INFO_EXT,
            messageSeverity = VK_DEBUG_UTILS_MESSAGE_SEVERITY_WARNING_BIT_EXT +\
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
            raise RuntimeError("couldn't create debugger")

    def pickPhysicalDevice(self):
        devices = vkEnumeratePhysicalDevices(self.instance)
        #print(devices)
        for device in devices:
            #print(device)
            if self.deviceSuitable(device):
                self.physicalDevice = device
                break
        
        if (self.physicalDevice is None):
            raise RuntimeError("Failed to find a suitable GPU!")

    def deviceSuitable(self, device):
        indices = self.findQueueFamilyIndices(device)
        return indices.complete()
    
    def findQueueFamilyIndices(self, device):
        """ Find the first index of a queue which supports graphics """
        indices = queueFamilyIndices()

        queueFamilies = vkGetPhysicalDeviceQueueFamilyProperties(device)
        #print(queueFamilies)
        i = 0
        for queueFamily in queueFamilies:
            #print(queueFamily)
            #print(queueFamily.queueFlags)
            if (queueFamily.queueFlags & VK_QUEUE_GRAPHICS_BIT):
                indices.graphicsFamily = i
                #print("has graphics")
            i += 1
        return indices

    def createLogicalDevice(self):
        indices = self.findQueueFamilyIndices(self.physicalDevice)

        queueCreateInfo = VkDeviceQueueCreateInfo(
            sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO,
            queueFamilyIndex = indices.graphicsFamily,
            queueCount = 1,
            pQueuePriorities = [1,]
        )

        if (debug_mode):
            layerCount = len(validationLayers)
            enabledLayerNames = validationLayers
        else:
            layerCount = 0
            enabledLayerNames = None
        
        deviceFeatures = VkPhysicalDeviceFeatures()

        deviceCreateInfo = VkDeviceCreateInfo(
            sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO,
            flags = 0,
            pQueueCreateInfos = queueCreateInfo,
            queueCreateInfoCount = 1,
            pEnabledFeatures = deviceFeatures,
            enabledExtensionCount = 0,
            enabledLayerCount = layerCount,
            ppEnabledLayerNames = enabledLayerNames
        )
        try:
            self.device = vkCreateDevice(self.physicalDevice, deviceCreateInfo, None)
        except Exception as e:
            print(e)
        self.graphicsQueue = vkGetDeviceQueue(self.device, indices.graphicsFamily, 0)

    def mainLoop(self):
        while (not glfw.window_should_close(self.window)):
            glfw.poll_events()
        self.exit()
    
    def exit(self):
        vkDestroyDevice(self.device, None)
        if (debug_mode):
            destroyDebugUtilsMessengerEXT(self.instance, self.debugMessenger, None)
        vkDestroyInstance(self.instance, None)
        glfw.destroy_window(self.window)
        glfw.terminate()

myApp = App()