"""
    Level Editor Program - By Blindspot Software 2021
"""
import tkinter as tk
import math
from tkinter import filedialog
from PIL import Image, ImageTk

"""
    ToDo:
        create room class                                   - done
        create room editor (textures and ambient level)     - done
        create light editor tab with room checking          - done
        create monster placement tab.
"""

TYPES = ["Rooms","Sectors","Lights","Player"]
GRID_SIZES = [8, 16, 32]
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 610
GROUND_COLOUR = "green"
WALL_COLOUR = "red"
DOOR_COLOUR = "yellow"
FILENAMES = [
    "tex/ceiling1.png",
    "tex/ceiling2.png",
    "tex/floor1.png",
    "tex/floor2.png",
    "tex/wall1.png",
    "tex/wall2.png"
]

class Editor:
    """
        Controls the Gui and level data, runs the show.
    """
    def __init__(self):
        """
            Create and start the program.
        """
        self.program = tk.Tk()
        self.program.title("Map Maker")
        self.camera_pos = [0,0]
        self.populateFunction = [
            self.populateRoomProperties,
            self.populateSectorProperties,
            self.populateLightProperties,
            self.populatePlayerProperties
            ]
        self.newMap()
        self.makeMenu()
        self.makeLayout()
        self.program.mainloop()

################################## File stuff #################################

    def makeMenu(self):
        """
            Create the File Menu bar
        """
        self.menu = tk.Menu(self.program)
        self.filemenu = tk.Menu(self.menu,tearoff=0)
        self.filemenu.add_command(label="New", command=self.newMap)
        self.filemenu.add_command(label="Save", command=self.saveMap)
        self.filemenu.add_command(label="Load", command=self.loadMap)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.program.config(menu=self.menu)

    def makeLayout(self):
        """
            Construct the components of the gui.
        """
        #make elements
        self.left_frame = tk.Frame(self.program)
        self.right_frame = tk.Frame(self.program)

        self.type_selector = Selector(self.right_frame,width=200,height=50,bg="gray")
        self.type_selector.bind("<Button-1>",self.typeSelectorClick)
        self.type_selector.draw(TYPES[self.current_type])

        self.element_selector = Selector(self.right_frame,width=200,height=50,bg="gray")
        self.element_selector.bind("<Button-1>",self.elementSelectorClick)
        self.element_selector.draw()

        self.search_frame = tk.Frame(self.right_frame)
        self.search_tag = tk.StringVar(self.program)
        self.search_entry = tk.Entry(self.search_frame,textvariable=self.search_tag)
        self.search_button = tk.Button(self.search_frame,command=self.selectElement,text="Search by tag")

        self.camera_frame = tk.Frame(self.right_frame)
        labels = ["Camera x: ","Camera y: "]
        data = self.camera_pos
        self.camera_parameters = ParameterFrame(self.camera_frame,labels,data)
        self.camera_button = tk.Button(self.camera_frame,text="snap camera",command=self.updateCamera)

        self.property_editor_frame = tk.Frame(self.right_frame)
        self.populateRoomProperties()

        self.view_controller = ViewController(self.right_frame,width=150,height=150,bg="gray")
        self.view_controller.bind("<Button-1>",self.viewControllerClick)
        self.view_controller.draw()
        self.map_view = MapView(self.left_frame,width=CANVAS_WIDTH,height=CANVAS_HEIGHT,bg="black")
        self.map_view.draw(self)

        #pack elements
        self.map_view.pack()
        self.type_selector.pack(side=tk.TOP)
        self.element_selector.pack(side=tk.TOP)
        self.search_entry.pack(side=tk.LEFT)
        self.search_button.pack(side=tk.LEFT)
        self.search_frame.pack()
        self.camera_parameters.pack(side=tk.LEFT)
        self.camera_button.pack(side=tk.LEFT)
        self.camera_frame.pack()
        self.property_editor_frame.pack(side=tk.TOP)
        self.view_controller.pack(side=tk.BOTTOM)
        self.left_frame.pack(side=tk.LEFT)
        self.right_frame.pack(side=tk.LEFT,expand=tk.TRUE,fill=tk.BOTH)

    def newMap(self):
        """
            Reset level data for a new map.
        """
        self.rooms = []
        self.selected_room = 0

        self.sectors = []
        self.selected_sector = 0

        self.lights = []
        self.selected_light = 0

        self.player = None

        self.current_type = 0

    def saveMap(self):
        """
            Save the current level data to a text file.
        """
        #get filepath to save to
        filepath = filedialog.asksaveasfilename(initialdir = ".")
        with open(filepath,mode="w") as f:
            #save rooms
            r = 0
            while r < self.room_count:
                if r < len(self.rooms):
                    floor = self.rooms[r].getFloorTexture()
                    wall = self.rooms[r].getWallTexture()
                    ceiling = self.rooms[r].getCeilingTexture()
                    ambient = self.rooms[r].getAmbient()
                    f.write(f"r{r}({floor}, {wall}, {ceiling}, {ambient[0]}, {ambient[1]}, {ambient[2]})\n")
                else:
                    f.write(f"r{r}(0, 0, 0, 1, 1, 1)\n")
                r += 1
            #save sectors
            for s in self.sectors:
                tag = s.getTag()
                (x,y) = s.getPosition()
                (w,h) = s.getSize()
                (wall_N,wall_E,wall_S,wall_W) = s.getSides()
                (door_N,door_E,door_S,door_W) = s.getDoors()
                room = s.getRoom()
                f.write(f"{tag}({x},{y},{w},{h},{int(wall_N)},{int(wall_E)},{int(wall_S)},{int(wall_W)},{int(door_N)},{int(door_E)},{int(door_S)},{int(door_W)},{room})\n")
            #save lights
            for l in self.lights:
                tag = l.getTag()
                (x,y,z) = l.getPosition()
                (r,g,b) = l.getColor()
                strength = l.getStrength()
                room = "r0"
                #find the sector which contains the light
                for s in self.sectors:
                    if s.inside((x,y)):
                        room = s.getRoom()
                        break
                f.write(f"{tag}({x},{y},{z},{r},{g},{b},{strength},{room})\n")
            #save player
            if self.player is not None:
                tag = "p"
                (x,y) = self.player.getPosition()
                d = self.player.getDirection()
                room = "r0"
                #find the sector which contains the player
                for s in self.sectors:
                    if s.inside((x,y)):
                        room = s.getRoom()
                        break
                f.write(f"{tag}({x},{y},{d},{room})\n")

    def loadMap(self):
        """
            Reset program's level data then read new level data from a text file.
        """
        filepath = filedialog.askopenfilename(initialdir = ".")
        with open(filepath,mode="r") as f:
            self.newMap()
            line = f.readline()
            while line:
                start = line.find('(')+1
                end = line.find(')')
                tag = line[0:start-1]
                if line[0]=='r':
                    l = line[start:end].replace('\n','').split(',')
                    if len(l) == 1:
                        r = Room(tag)
                    else:
                        # s(floor, wall, ceiling, r, g, b)
                        r = Room(tag)
                        r.setFloorTexture(int(l[0]))
                        r.setWallTexture(int(l[1]))
                        r.setCeilingTexture(int(l[2]))
                        r.setAmbient([float(l[3]), float(l[4]), float(l[5])])
                    self.rooms.append(r)
                if line[0]=='s':
                    #sector
                    # s(x,y,width,height,w_n,w_e,w_s,w_w,d_n,d_e,d_s,d_w,r)
                    l = line[start:end].replace('\n','').split(',')
                    pos = (float(l[0]),float(l[1]))
                    size = (float(l[2]),float(l[3]))
                    sides = [int(l[4]),int(l[5]),int(l[6]),int(l[7])]
                    doors = [int(l[8]),int(l[9]),int(l[10]),int(l[11])]
                    s = Sector(pos,size,sides,doors,tag)
                    if len(l) == 13:
                        s.setRoom(int(l[12].replace("r","")))
                    self.sectors.append(s)
                if line[0]=='l':
                    #light
                    # l(x,y,z,r,g,b,strength)
                    l = line[start:end].replace('\n','').split(',')
                    pos = (float(l[0]),float(l[1]),float(l[2]))
                    color = (float(l[3]),float(l[4]),float(l[5]))
                    strength = float(l[6])
                    l = Light(pos,color,strength,tag)
                    self.lights.append(l)
                elif line[0]=='p':
                    #player
                    # p(x,y,direction,room)
                    l = line[start:end].replace('\n','').split(',')
                    self.player = Player(float(l[0]),float(l[1]),float(l[2]),"p")
                line = f.readline()
            self.recalculateRooms()
            self.map_view.draw(self)
            self.populateSectorProperties()

################################## Rooms ######################################

    def populateRoomProperties(self):
        """
            Construct and pack widgets to the property_editor_frame for sector
            creation/editing.
        """
        #clear the frame
        for widget in self.property_editor_frame.winfo_children():
            widget.destroy()
        if self.selected_room==len(self.rooms):
            #no rooms, or the user is poised to make a new one
            self.property_label = tk.Label(self.property_editor_frame,text="No Room currently selected.")
            self.new_button = tk.Button(self.property_editor_frame,text="New Room",command=self.addRoom)
            #pack
            self.property_label.pack()
            self.new_button.pack()
        else:
            room = self.rooms[self.selected_room]
            self.property_label = tk.Label(self.property_editor_frame,text=f"Room: {room.getTag()}")
            self.frame_a = tk.Frame(self.property_editor_frame)
            #floor texture
            label = "Floor Texture:"
            data = room.getFloorTexture()
            self.floorTex_image = ImageFrame(self.frame_a,label,data)
            #wall texture
            label = "Wall Texture:"
            data = room.getWallTexture()
            self.wallTex_image = ImageFrame(self.frame_a,label,data)
            #ceiling texture
            label = "Ceiling Texture:"
            data = room.getCeilingTexture()
            self.ceilingTex_image = ImageFrame(self.property_editor_frame,label,data)
            #ambient level
            labels = ["Ambient r: ","g: ", "b: "]
            data = room.getAmbient()
            self.ambient_parameters = ParameterFrame(self.property_editor_frame,labels,data)
            #action frame
            labels = ["Update Room","New Room","Delete Room"]
            commands = [self.updateRoom,self.addRoom,self.deleteRoom]
            self.action_frame = ButtonPanel(self.property_editor_frame,labels,commands)
            #pack
            self.property_label.pack()
            self.floorTex_image.pack(side=tk.LEFT)
            self.wallTex_image.pack(side=tk.LEFT)
            self.frame_a.pack()
            self.ceilingTex_image.pack()
            self.ambient_parameters.pack()
            self.action_frame.pack()

    def updateRoom(self):
        """
            Update the currently selected sector with data from the gui.
        """
        room = self.rooms[self.selected_room]
        newTex = self.floorTex_image.getParameters()
        room.setFloorTexture(newTex)
        newTex = self.wallTex_image.getParameters()
        room.setWallTexture(newTex)
        newTex = self.ceilingTex_image.getParameters()
        room.setCeilingTexture(newTex)
        newAmbient = [float(parameter) for parameter in self.ambient_parameters.getParameters()]
        room.setAmbient(newAmbient)
        self.populateRoomProperties()

    def addRoom(self):
        """
            Create a new sector with some default parameters,
            then refresh the gui.
        """
        #look for gaps
        target = 0
        expected = 0
        for r in self.rooms:
            index = int(r.tag[1:])
            if index != expected:
                break
            else:
                target += 1
                expected += 1
        room = Room(f"r{target}")
        self.rooms.insert(target,room)
        self.selected_room = target
        self.populateRoomProperties()

    def deleteRoom(self):
        """
            Delete the currently selected sector then refresh the gui.
        """
        room = self.rooms[self.selected_room]
        self.rooms.pop(self.rooms.index(room))
        self.populateRoomProperties()

################################## Sectors ####################################

    def populateSectorProperties(self):
        """
            Construct and pack widgets to the property_editor_frame for sector
            creation/editing.
        """
        #clear the frame
        for widget in self.property_editor_frame.winfo_children():
            widget.destroy()
        if self.selected_sector==len(self.sectors):
            #no sectors, or the user is poised to make a new one
            self.property_label = tk.Label(self.property_editor_frame,text="No sector currently selected.")
            self.new_button = tk.Button(self.property_editor_frame,text="New Sector",command=self.addSector)
            #pack
            self.property_label.pack()
            self.new_button.pack()
        else:
            sector = self.sectors[self.selected_sector]
            self.property_label = tk.Label(self.property_editor_frame,text=f"Sector: {sector.getTag()}, Room: {sector.getRoom()}")
            #position
            labels = ["x: ","y: "]
            data = sector.getPosition()
            self.position_parameters = ParameterFrame(self.property_editor_frame,labels,data)
            #size
            labels = ["w: ","h: "]
            data = sector.getSize()
            self.size_parameters = ParameterFrame(self.property_editor_frame,labels,data)
            #sides
            self.tick_frame = tk.Frame(self.property_editor_frame)
            labels = ["N Wall","E Wall","S Wall","W Wall"]
            data = sector.getSides()
            self.wall_parameters = ParameterGrid(self.tick_frame,labels,data)
            #doors
            labels = ["N Door","E Door","S Door","W Door"]
            data = sector.getDoors()
            self.door_parameters = ParameterGrid(self.tick_frame,labels,data)
            #room
            self.room_button = tk.Button(self.property_editor_frame,text="Recalculate Rooms",command=self.recalculateRooms)
            #action buttons
            labels = ["Update Sector","New Sector","Delete Sector"]
            commands = [self.updateSector,self.addSector,self.deleteSector]
            self.action_frame = ButtonPanel(self.property_editor_frame,labels,commands)
            #pack
            self.property_label.pack()
            self.position_parameters.pack()
            self.size_parameters.pack()
            self.wall_parameters.pack(side=tk.LEFT)
            self.door_parameters.pack(side=tk.LEFT)
            self.tick_frame.pack()
            self.room_button.pack()
            self.action_frame.pack()

    def updateSector(self):
        """
            Update the currently selected sector with data from the gui.
        """
        sector = self.sectors[self.selected_sector]
        newPos = [float(parameter) for parameter in self.position_parameters.getParameters()]
        sector.setPosition(newPos)
        newSize = [float(parameter) for parameter in self.size_parameters.getParameters()]
        sector.setSize(newSize)
        newSides = list(self.wall_parameters.getParameters())
        sector.setSides(newSides)
        newDoors = list(self.door_parameters.getParameters())
        sector.setDoors(newDoors)
        self.recalculateRooms()
        sector.updateNeighbourWalls()
        sector.updateNeighbourDoors()
        self.populateSectorProperties()
        self.map_view.draw(self)

    def addSector(self):
        """
            Create a new sector with some default parameters,
            then refresh the gui.
        """
        startPos = (0,0)
        startSize = (1,1)
        startSides = [0,0,0,0]
        startDoors = [0,0,0,0]
        #look for gaps
        target = 0
        expected = 0
        for s in self.sectors:
            index = int(s.tag[1:])
            if index != expected:
                break
            else:
                target += 1
                expected += 1
        sector = Sector(startPos,startSize,startSides,startDoors,f"s{target}")
        self.sectors.insert(target,sector)
        self.selected_sector = target
        self.recalculateRooms()
        self.populateSectorProperties()
        self.map_view.draw(self)

    def deleteSector(self):
        """
            Delete the currently selected sector then refresh the gui.
        """
        sector = self.sectors[self.selected_sector]
        self.sectors.pop(self.sectors.index(sector))
        self.populateSectorProperties()
        self.map_view.draw(self)

################################## Lights #####################################

    def populateLightProperties(self):
        """
            Construct and pack widgets to the property_editor_frame for sector
            creation/editing.
        """
        #clear the frame
        for widget in self.property_editor_frame.winfo_children():
            widget.destroy()
        if self.selected_light==len(self.lights):
            #no lights, or the user is poised to make a new one
            self.property_label = tk.Label(self.property_editor_frame,text="No light currently selected.")
            self.new_button = tk.Button(self.property_editor_frame,text="New Light",command=self.addLight)
            #pack
            self.property_label.pack()
            self.new_button.pack()
        else:
            light = self.lights[self.selected_light]
            self.property_label = tk.Label(self.property_editor_frame,text=f"Light: {light.getTag()}")
            #position
            labels = ["x: ", "y: ", "z: "]
            data = light.getPosition()
            self.position_parameters = ParameterFrame(self.property_editor_frame,labels,data)
            #color
            labels = ["r: ", "g: ", "b: "]
            data = light.getColor()
            self.color_parameters = ParameterFrame(self.property_editor_frame,labels,data)
            #strength
            labels = ["strength: ",]
            data = [light.getStrength(),]
            self.strength_parameter = ParameterFrame(self.property_editor_frame,labels,data)
            #room
            self.room_button = tk.Button(self.property_editor_frame,text="Recalculate Rooms",command=self.recalculateRooms)
            #action buttons
            labels = ["Update Light","New Light","Delete Light"]
            commands = [self.updateLight,self.addLight,self.deleteLight]
            self.action_frame = ButtonPanel(self.property_editor_frame,labels,commands)
            #pack
            self.property_label.pack()
            self.position_parameters.pack()
            self.color_parameters.pack()
            self.strength_parameter.pack()
            self.room_button.pack()
            self.action_frame.pack()

    def updateLight(self):
        """
            Update the currently selected light with data from the gui.
        """
        light = self.lights[self.selected_light]
        newPos = [float(parameter) for parameter in self.position_parameters.getParameters()]
        light.setPosition(newPos)
        newColor = [float(parameter) for parameter in self.color_parameters.getParameters()]
        light.setColor(newColor)
        newStrength = float(self.strength_parameter.getParameters()[0])
        light.setStrength(newStrength)
        self.populateLightProperties()

    def addLight(self):
        """
            Create a new light with some default parameters,
            then refresh the gui.
        """
        startPos = (0, 0, 0)
        startColor = (1,1,1)
        startStrength = 1
        #look for gaps
        target = 0
        expected = 0
        for l in self.lights:
            index = int(l.tag[1:])
            if index != expected:
                break
            else:
                target += 1
                expected += 1
        light = Light(startPos,startColor,startStrength,f"l{target}")
        self.lights.insert(target,light)
        self.selected_light = target
        self.populateLightProperties()

    def deleteLight(self):
        """
            Delete the currently selected light then refresh the gui.
        """
        light = self.lights[self.selected_light]
        self.lights.pop(self.lights.index(light))
        self.populateLightProperties()

################################## Players ####################################

    def populatePlayerProperties(self):
        """
            Construct and pack widgets to the property_editor_frame for player
            creation/editing.
        """
        #clear the frame
        for widget in self.property_editor_frame.winfo_children():
            widget.destroy()
        if self.player is None:
            #no player
            self.property_label = tk.Label(self.property_editor_frame,
                                            text="There is no player.")
            self.new_button = tk.Button(self.property_editor_frame,
                                        text="Make Player",
                                        command=self.addPlayer)
            #pack
            self.property_label.pack()
            self.new_button.pack()
        else:
            self.property_label = tk.Label(self.property_editor_frame,text="Player")
            #position
            self.pos_frame = tk.Frame(self.property_editor_frame)
            self.x_label = tk.Label(self.pos_frame,text="x: ")
            self.newX = tk.StringVar(self.program,value=str(self.player.pos[0]))
            self.x_entry = tk.Entry(self.pos_frame,textvariable=self.newX)
            self.y_label = tk.Label(self.pos_frame,text="y: ")
            self.newY = tk.StringVar(self.program,value=str(self.player.pos[1]))
            self.y_entry = tk.Entry(self.pos_frame,textvariable=self.newY)
            #direction
            self.direction_frame = tk.Frame(self.property_editor_frame)
            self.direction_label = tk.Label(self.direction_frame,text="Direction: ")
            self.new_direction = tk.StringVar(self.program,value=str(self.player.direction))
            self.direction_entry = tk.Entry(self.direction_frame,textvariable=self.new_direction)
            #action buttons
            self.action_frame = tk.Frame(self.property_editor_frame)
            self.update_button = tk.Button(self.action_frame,
                                        text="Update Player",
                                        command=self.updatePlayer)
            self.delete_button = tk.Button(self.action_frame,
                                        text="Delete Player",
                                        command=self.deletePlayer)
            #pack
            self.property_label.pack()

            self.x_label.pack(side=tk.LEFT)
            self.x_entry.pack(side=tk.LEFT)
            self.y_label.pack(side=tk.LEFT)
            self.y_entry.pack(side=tk.LEFT)
            self.pos_frame.pack()

            self.direction_label.pack(side=tk.LEFT)
            self.direction_entry.pack(side=tk.LEFT)
            self.direction_frame.pack()

            self.update_button.pack(side=tk.LEFT)
            self.delete_button.pack(side=tk.LEFT)
            self.action_frame.pack()

    def updatePlayer(self):
        """
            Update the player object with data from the gui.
        """
        newPos = (float(self.newX.get()),float(self.newY.get()))
        self.player.setPosition(newPos)
        self.player.setDirection(float(self.new_direction.get()))
        self.map_view.draw(self)
        self.populatePlayerProperties()

    def addPlayer(self):
        """
            Create a new player object with some default parameters,
            then refresh the gui.
        """
        startX = 0
        startY = 0
        startDirection = 0
        self.player = Player(startX,startY,startDirection,"p")
        self.map_view.draw(self)
        self.populatePlayerProperties()

    def deletePlayer(self):
        """
            Delete the player object then refresh the gui.
        """
        self.player = None
        self.map_view.draw(self)
        self.populatePlayerProperties()

################################## Gui Buttons ################################

    def typeSelectorClick(self,event):
        """
            Handle a click on the type selector (data types include Sectors, Objects etc)
        """
        x = event.x
        y = event.y
        if (x>10 and x<40 and y>10 and y<40):
            #left arrow
            self.current_type = (self.current_type - 1)%len(TYPES)

        elif (x>160 and x<190 and y>10 and y<40):
            #right arrow
            self.current_type = (self.current_type + 1)%len(TYPES)
        
        self.type_selector.draw(TYPES[self.current_type])
        self.populateFunction[self.current_type]()
        self.map_view.draw(self)

    def elementSelectorClick(self,event):
        """
            Handle a click on the element selector (elements are specific instances, eg. s1,s2,...)
        """
        x = event.x
        y = event.y
        if (self.current_type == 3): #player
            return
        if (x>10 and x<40 and y>10 and y<40):
            #left arrow
            self.incrementElement(-1)
        elif (x>160 and x<190 and y>10 and y<40):
            #right arrow
            self.incrementElement(1)
        self.populateFunction[self.current_type]()
        self.map_view.draw(self)

    def incrementElement(self, increment):
        if (self.current_type == 0):
            self.selected_room = (self.selected_room + increment)%len(self.rooms)
        elif (self.current_type == 1):
            self.selected_sector = (self.selected_sector + increment)%len(self.sectors)
        elif (self.current_type == 2):
            self.selected_light = (self.selected_light + increment)%len(self.lights)
        else:
            return

    def viewControllerClick(self,event):
        """
            Handle a click on the view controller. The view controller lets the user scroll or zoom.
        """
        x = event.x
        y = event.y
        if(x>10 and x<40 and y>55 and y<95):
            self.camera_pos = (self.camera_pos[0] - 1, self.camera_pos[1])
        elif(x>55 and x<95 and y>10 and y<40):
            self.camera_pos = (self.camera_pos[0], self.camera_pos[1] + 1)
        elif(x>110 and x<140 and y>55 and y<95):
            self.camera_pos = (self.camera_pos[0] + 1, self.camera_pos[1])
        elif(x>55 and x<95 and y>110 and y<140):
            self.camera_pos = (self.camera_pos[0], self.camera_pos[1] - 1)
        elif(x>50 and x<100 and y>50 and y<70):
            size_index = self.map_view.size_index
            if size_index<2:
                size_index += 1
                self.map_view.setSize(size_index)
        elif(x>50 and x<100 and y>80 and y<100):
            size_index = self.map_view.size_index
            if size_index>0:
                size_index -= 1
                self.map_view.setSize(size_index)
        self.map_view.draw(self)

    def updateCamera(self):
        self.camera_pos = [int(parameter) for parameter in self.camera_parameters.getParameters()]
        self.map_view.draw(self)

    def selectElement(self):
        """
            General lookup method. Query element by tag.
        """
        tag = self.search_tag.get()
        if tag[0]=="s":
            #sector
            found_element = False
            element = 0
            for s in self.sectors:
                if s.tag==tag:
                    found_element = True
                    break
                element += 1
            if found_element:
                self.current_type = 0
                self.selected_sector = element
                self.populateSectorProperties()
                self.type_selector.draw(TYPES[self.current_type])
        elif tag[0]=="p":
            if self.player is not None:
                self.current_type = 1
                self.populatePlayerProperties()
                self.type_selector.draw(TYPES[self.current_type])

################################## Geometry Checks ############################

    def recalculateRooms(self):
        """
            Reset all room data, then calculate which room each sector should belong to.
        """
        if len(self.sectors)==0:
            return
        self.resetRooms()
        self.recalculateSectorConnections()
        while not self.roomCalculationIsDone():
            sector_to_expand = self.findSectorWithoutRoom()
            self.expandSector(sector_to_expand)
        self.populateSectorProperties()

    def roomCalculationIsDone(self):
        """
            Returns True if all sectors have been assigned to a room
        """
        done = True
        for sector in self.sectors:
            if sector.getRoom() == "":
                done = False
                break
        return done

    def findSectorWithoutRoom(self):
        """
            Returns a reference to the first sector without a room.
        """
        sector_found = None
        for sector in self.sectors:
            if sector.getRoom() == "":
                sector_found = sector
                break
        return sector_found

    def expandSector(self,sector):
        """
            Start with a given sector, make a new room for it,
            then search its neighbours and add them to the room.
            Continue until all connecting sectors are in the room.
            This works a bit like flood fill.
        """
        #make a new room
        room_tag = f"r{self.room_count}"
        self.room_count += 1
        sectors_to_expand = [sector]
        expanded_sectors = []
        while len(sectors_to_expand)!=0:
            sector = sectors_to_expand.pop()
            expanded_sectors.append(sector)
            sector.setRoom(room_tag)
            for new_sector in sector.getConnectedSectorsWithBlocks():
                if (new_sector not in sectors_to_expand) and (new_sector not in expanded_sectors):
                    sectors_to_expand.append(new_sector)

    def resetRooms(self):
        """
            Remove all room data.
        """
        self.room_count = 0
        for sector in self.sectors:
            sector.setRoom("")
            sector.overwriteDoors()

    def resetSectorConnections(self):
        """
            Reset all sector connections.
        """
        for sector in self.sectors:
            sector.connects_N = None
            sector.connects_E = None
            sector.connects_S = None
            sector.connects_W = None

    def recalculateSectorConnections(self):
        """
            Reset all connection data, then recalculate which sectors
            are connected to each other.
        """
        self.resetSectorConnections()
        #find how sectors connect
        for sector in self.sectors:
            A = sector.pos_a
            B = sector.pos_b
            C = sector.pos_c
            D = sector.pos_d
            for sector2 in self.sectors:
                hasA = False
                hasB = False
                hasC = False
                hasD = False
                if sector==sector2:
                    continue
                corners = sector2.getCorners()
                #do any corners match?
                for corner in corners:
                    if A[0] == corner[0] and A[1] == corner[1]:
                        hasA = True
                    elif B[0] == corner[0] and B[1] == corner[1]:
                        hasB = True
                    elif C[0] == corner[0] and C[1] == corner[1]:
                        hasC = True
                    elif D[0] == corner[0] and D[1] == corner[1]:
                        hasD = True
                if hasA and hasB:
                    sector.connects_W = sector2
                    continue
                elif hasB and hasC:
                    sector.connects_S = sector2
                    continue
                elif hasC and hasD:
                    sector.connects_E = sector2
                    continue
                elif hasD and hasA:
                    sector.connects_N = sector2
                    continue

################################## Other Gui widgets ##########################

class MapView(tk.Canvas):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        self.size_index = 2
        self.size = GRID_SIZES[self.size_index]

    def setSize(self,newIndex):
        self.size_index = newIndex
        self.size = GRID_SIZES[self.size_index]

    def draw(self,program):
        camera_pos = program.camera_pos
        self.delete("all")
        #gridlines
        columns = CANVAS_WIDTH//self.size
        rows = CANVAS_HEIGHT//self.size
        for x in range(columns):
            self.create_line(self.size*x,0,self.size*x,CANVAS_HEIGHT,fill="gray")
            self.create_text(self.size*x + 5,CANVAS_HEIGHT-10,text=str(x+camera_pos[0]),fill="white")
        for y in range(rows):
            self.create_line(0,self.size*y,CANVAS_WIDTH,self.size*y,fill="gray")
            self.create_text(10,self.size*y+5,text=str(rows-y+camera_pos[1]),fill="white")
        #sectors
        for s in program.sectors:
            #get sector data
            pos = s.getPosition()
            size = s.getSize()
            sides = s.getSides()
            doors = s.getDoors()

            x = self.size*(pos[0]-camera_pos[0])
            y = self.size*(rows - pos[1] + camera_pos[1])
            w = size[0]*self.size
            h = size[1]*self.size
            mid_x = x + w/2
            mid_y = y + h/2
            current_colour = ""

            if sides[0]:
                current_colour = WALL_COLOUR
            elif doors[0]:
                current_colour = DOOR_COLOUR
            else:
                current_colour = GROUND_COLOUR
            self.create_line(x,y,x+w,y,fill=current_colour)

            if sides[2]:
                current_colour = WALL_COLOUR
            elif doors[2]:
                current_colour = DOOR_COLOUR
            else:
                current_colour = GROUND_COLOUR
            self.create_line(x,y+h,x+w,y+h,fill=current_colour)

            if sides[1]:
                current_colour = WALL_COLOUR
            elif doors[1]:
                current_colour = DOOR_COLOUR
            else:
                current_colour = GROUND_COLOUR
            self.create_line(x+w,y,x+w,y+h,fill=current_colour)

            if sides[3]:
                current_colour = WALL_COLOUR
            elif doors[3]:
                current_colour = DOOR_COLOUR
            else:
                current_colour = GROUND_COLOUR
            self.create_line(x,y,x,y+h,fill=current_colour)

            self.create_text(mid_x,mid_y,text=s.tag,fill="white")
        #player
        if program.player is not None:
            pos = program.player.pos

            x = self.size*(pos[0]-camera_pos[0])
            y = self.size*(rows - pos[1] + camera_pos[1])
            r = program.player.radius*self.size/32
            x2 = x + r*math.cos(math.radians(program.player.direction))
            y2 = y - r*math.sin(math.radians(program.player.direction))
            self.create_oval(x-r, y-r, x+r, y+r, fill="red", outline="black")
            self.create_line(x, y, x2, y2, fill="black")
            self.create_text(x,y,text=program.player.tag,fill="black")
        #lights
        for l in program.lights:
            pos = l.getPosition()

            x = self.size*(pos[0]-camera_pos[0])
            y = self.size*(rows - pos[1] + camera_pos[1])
            r = 12*self.size/32
            self.create_oval(x-r, y-r, x+r, y+r, fill="white", outline="black")
            self.create_text(x,y,text=l.getTag(),fill="black")

    def pack(self,**kwargs):
        super().pack(**kwargs)

class Selector(tk.Canvas):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)

    def draw(self,content=""):
        self.delete("all")
        self.create_polygon((10,25,40,10,40,40),outline="black",fill="white")
        self.create_polygon((60,10,140,10,140,40,60,40),outline="black",fill="white")
        self.create_text(90,25,text=content,fill="black")
        self.create_polygon((160,10,190,25,160,40),outline="black",fill="white")

    def pack(self,**kwargs):
        super().pack(**kwargs)

class ViewController(tk.Canvas):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)

    def draw(self):
        self.delete("all")
        #left arrow
        self.create_polygon((10,75,40,55,40,95),outline="black",fill="white")
        #up arrow
        self.create_polygon((55,40,75,10,95,40),outline="black",fill="white")
        #right arrow
        self.create_polygon((140,75,110,55,110,95),outline="black",fill="white")
        #down arrow
        self.create_polygon((55,110,75,140,95,110),outline="black",fill="white")
        #zoom in
        self.create_polygon((50,50,100,50,100,70,50,70),outline="black",fill="white")
        self.create_line((75,55,75,65),fill="black")
        self.create_line((70,60,80,60),fill="black")
        #zoom out
        self.create_polygon((50,100,100,100,100,80,50,80),outline="black",fill="white")
        self.create_line((70,90,80,90),fill="black")

    def pack(self,**kwargs):
        super().pack(**kwargs)

class ParameterFrame(tk.Frame):
    def __init__(self,master,labels,data,**kwargs):
        super().__init__(master,**kwargs)
        self.widgets = []
        self.parameters = []
        for i in range(len(labels)):
            new_label = tk.Label(self,text=labels[i])
            self.widgets.append(new_label)
            new_parameter = tk.StringVar(self,value=str(data[i]))
            self.parameters.append(new_parameter)
            new_entry_field = tk.Entry(self,textvariable=self.parameters[i])
            self.widgets.append(new_entry_field)

    def getParameters(self):
        result = []
        for parameter in self.parameters:
            result.append(parameter.get())
        return result

    def pack(self,**kwargs):
        for widget in self.widgets:
            widget.pack(side=tk.LEFT)
        super().pack(**kwargs)

class ParameterGrid(tk.Frame):
    def __init__(self,master,labels,data,**kwargs):
        super().__init__(master,**kwargs)
        self.widgets = []
        self.parameters = []
        self.top_row = tk.Frame(self)
        self.mid_row = tk.Frame(self)
        self.bottom_row = tk.Frame(self)
        for i in range(len(labels)):
            if i==0:
                widget_master = self.top_row
            elif i==2:
                widget_master = self.bottom_row
            else:
                widget_master = self.mid_row

            new_label = tk.Label(widget_master,text=labels[i])
            self.widgets.append(new_label)
            new_parameter = tk.IntVar(self,value=int(data[i]))
            self.parameters.append(new_parameter)
            new_check_button = tk.Checkbutton(widget_master,variable=new_parameter,onvalue=1,offvalue=0)
            self.widgets.append(new_check_button)

    def getParameters(self):
        result = []
        for parameter in self.parameters:
            result.append(parameter.get())
        return result

    def pack(self,**kwargs):
        for widget in self.widgets:
            widget.pack(side=tk.RIGHT)
        self.top_row.pack()
        self.mid_row.pack()
        self.bottom_row.pack()
        super().pack(**kwargs)

class ButtonPanel(tk.Frame):
    def __init__(self,master,labels,commands,**kwargs):
        super().__init__(master,**kwargs)
        self.widgets = []
        for i in range(len(labels)):
            new_button = tk.Button(self,text=labels[i],command=commands[i])
            self.widgets.append(new_button)

    def pack(self,**kwargs):
        for widget in self.widgets:
            widget.pack(side=tk.LEFT,**kwargs)
        super().pack(**kwargs)

class ImageFrame(tk.Frame):
    def __init__(self,master,label,image,**kwargs):
        super().__init__(master,**kwargs)
        self.label = tk.Label(self,text=label)
        self.image_index = image
        self.canvas = tk.Canvas(self,width=128,height=128)
        self.canvas.bind("<Button-1>",self.imageClick)
        self.reDraw()

    def imageClick(self,event):
        if (event.x > 64):
            increment = 1
        else:
            increment = -1
        
        self.image_index = (self.image_index + increment)%len(FILENAMES)
        self.reDraw()

    def reDraw(self):
        self.canvas.delete("all")
        self.image = ImageTk.PhotoImage(Image.open(FILENAMES[self.image_index]).resize((256,256)))
        self.canvas.create_image(0, 0, image=self.image)

    def getParameters(self):
        return self.image_index

    def pack(self,**kwargs):
        self.label.pack()
        self.canvas.pack()
        super().pack(**kwargs)

############################ Data Classes #####################################

class Room:
    def __init__(self, tag):
        self.ambient = [0.2,0.2,0.2]
        self.ceilingTexture = 0
        self.wallTexture = 0
        self.floorTexture = 0
        self.tag = tag
    
    def getTag(self):
        return self.tag

    def getFloorTexture(self):
        return self.floorTexture
    
    def getWallTexture(self):
        return self.wallTexture
    
    def getCeilingTexture(self):
        return self.ceilingTexture
    
    def setFloorTexture(self, newTexture):
        self.floorTexture = newTexture
    
    def setWallTexture(self, newTexture):
        self.wallTexture = newTexture
    
    def setCeilingTexture(self, newTexture):
        self.ceilingTexture = newTexture

    def getAmbient(self):
        return self.ambient

    def setAmbient(self, newAmbient):
        self.ambient = newAmbient

class Sector:
    def __init__(self,pos,size,sides,doors,tag):
        self.pos = pos
        self.size = size
        #North, East, South, West
        self.sides = list(sides)
        self.room = ""
        #North, East, South, West
        self.doors = list(doors)
        self.tag = tag
        self.calculateCorners()
        self.connects_N = None
        self.connects_E = None
        self.connects_S = None
        self.connects_W = None

    def getTag(self):
        return self.tag

    def calculateCorners(self):
        self.pos_a = self.pos
        self.pos_b = (self.pos[0],self.pos[1]-self.size[1])
        self.pos_c = (self.pos[0]+self.size[0],self.pos[1]-self.size[1])
        self.pos_d = (self.pos[0]+self.size[0],self.pos[1])

    def getCorners(self):
        return [
                    self.pos_a,
                    self.pos_b,
                    self.pos_c,
                    self.pos_d
        ]

    def setPosition(self,newPos):
        self.pos = newPos
        self.calculateCorners()

    def getPosition(self):
        return self.pos

    def setSize(self,newSize):
        self.size = newSize
        self.calculateCorners()

    def getSize(self):
        return self.size

    def setSides(self,newSides):
        self.sides = list(newSides)
        self.overwriteDoors()

    def getSides(self):
        return self.sides

    def setDoors(self,newDoors):
        self.doors = list(newDoors)
        self.overwriteDoors()

    def getDoors(self):
        return self.doors

    def overwriteDoors(self):
        #walls beat doors
        for i in range(len(self.doors)):
            if self.sides[i]:
                self.doors[i] = 0
                self.sides[i] = 1

    def setRoom(self,newRoom):
        self.room = newRoom

    def getRoom(self):
        return self.room

    def getConnectedSectors(self):
        connected_sectors = []
        if self.connects_N is not None:
            connected_sectors.append(self.connects_N)
        if self.connects_E is not None:
            connected_sectors.append(self.connects_E)
        if self.connects_S is not None:
            connected_sectors.append(self.connects_S)
        if self.connects_W is not None:
            connected_sectors.append(self.connects_W)
        return connected_sectors

    def getConnectedSectorsWithBlocks(self):
        """
            Get a list of the sectors which connect to this sector,
            factoring in walls and doors which may block line of sight
        """
        connected_sectors = []
        if (self.connects_N is not None) and (self.sides[0]==0) and (self.doors[0]==0):
            connected_sectors.append(self.connects_N)

        if (self.connects_E is not None) and (self.sides[1]==0) and (self.doors[1]==0):
            connected_sectors.append(self.connects_E)

        if (self.connects_S is not None) and (self.sides[2]==0) and (self.doors[2]==0):
            connected_sectors.append(self.connects_S)

        if (self.connects_W is not None) and (self.sides[3]==0) and (self.doors[3]==0):
            connected_sectors.append(self.connects_W)

        return connected_sectors

    def updateNeighbourWalls(self):
        if self.sides[0] and self.connects_N is not None:
            self.connects_N.sides[2] = 1
            self.connects_N.doors[2] = 0
        if self.sides[1] and self.connects_E is not None:
            self.connects_E.sides[3] = 1
            self.connects_E.doors[3] = 0
        if self.sides[2] and self.connects_S is not None:
            self.connects_S.sides[0] = 1
            self.connects_S.doors[0] = 0
        if self.sides[3] and self.connects_W is not None:
            self.connects_W.sides[1] = 1
            self.connects_W.doors[1] = 0

    def updateNeighbourDoors(self):
        if self.doors[0] and self.connects_N is not None:
            self.connects_N.sides[2] = 0
            self.connects_N.doors[2] = 1
        if self.doors[1] and self.connects_E is not None:
            self.connects_E.sides[3] = 0
            self.connects_E.doors[3] = 1
        if self.doors[2] and self.connects_S is not None:
            self.connects_S.sides[0] = 0
            self.connects_S.doors[0] = 1
        if self.doors[3] and self.connects_W is not None:
            self.connects_W.sides[1] = 0
            self.connects_W.doors[1] = 1

    def inside(self, point):
        return point[0] > self.pos[0] \
            and point[0] < (self.pos[0] + self.size[0]) \
            and point[1] < self.pos[1] \
            and point[1] > (self.pos[1] - self.size[1])

    def __str__(self):
        return self.tag

    def __repr__(self):
        return self.tag

class Player:
    def __init__(self,x,y,direction,tag):
        self.radius = 12
        self.pos = (x,y)
        self.direction = direction
        self.tag = tag

    def setPosition(self,newPos):
        self.pos = newPos

    def getPosition(self):
        return self.pos

    def setDirection(self,newDirection):
        self.direction = newDirection

    def getDirection(self):
        return self.direction

class Light:
    def __init__(self, pos, color, strength, tag):
        self.tag = tag
        self.pos = pos
        self.color = color
        self.strength = strength

    def getTag(self):
        return self.tag

    def setPosition(self, newPos):
        self.pos = newPos

    def getPosition(self):
        return self.pos

    def setColor(self, newColor):
        self.color = newColor

    def getColor(self):
        return self.color

    def setStrength(self, newStrength):
        self.strength = newStrength

    def getStrength(self):
        return self.strength

program = Editor()
