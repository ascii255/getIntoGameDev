"""
    PyVulkan Tutorial
    - Stage one, basic setup -
    requirements: glfw (pip install)
"""
################################# imports #####################################
#from vulkan import *
import glfw
import glfw.GLFW as constants

class App:

    #start a new app
    def __init__(self):
        #initialise glfw
        glfw.init()

        #tell glfw not to create an opengl context
        glfw.window_hint(constants.GLFW_CLIENT_API, constants.GLFW_NO_API)
        glfw.window_hint(constants.GLFW_RESIZABLE, constants.GLFW_FALSE)
        self.width = 640
        self.height = 480

        # (width, height, title, monitor, share)
        self.window = glfw.create_window(self.width, self.height, "Vulkan Window", None, None)
        self.testVulkan()
        self.mainLoop()

    def testVulkan(self):
        if (glfw.vulkan_supported()):
            print("Vulkan is supported.")
        else:
            print("Vulkan is not supported.")

    def mainLoop(self):
        while (not glfw.window_should_close(self.window)):
            #clear the event queue for the next frame
            glfw.poll_events()
        self.exit()

    def exit(self):
        #free any memory
        glfw.destroy_window(self.window)
        glfw.terminate()


myApp = App()