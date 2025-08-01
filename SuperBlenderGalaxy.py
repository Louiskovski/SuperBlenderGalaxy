bl_info = {
    "name": "Mario Galaxy Map Editor / Converter",
    "author": "Louis Miles",
    "version": (0, 6, 0),
    "blender": (4, 4, 0),
    "location": "In 3D Viewport right under 'Mario Galaxy'",
    "description": "Transforms Blender into a Mario Galaxy Level Editor",
    "warning": "Work in Progress!! Make Backups!, No rendering of original Assets, only your assets from your Blend files",
    "doc_url": "",
}


import bpy
import math
import os
import shutil
import subprocess
C = bpy.context
import struct
import csv
import sys
import requests
import os.path

# Database:
import xml.etree.ElementTree as ET
from bpy.props import StringProperty, EnumProperty, CollectionProperty


###DEF OPERATORS -----------------------------------------------------

def ArcPack(GalaxyMapName, WiiExplorerPathFolder, GalaxyFilesystem):

    import os

    # rarcpackPath="C:/SuperMarioGravity/Tools/Archive/Rarc Tools/rarcpack-casesensitive.exe"
    # rarcdumpPath="C:/SuperMarioGravity/Tools/Archive/Rarc Tools/rarcdump.exe"
    # yaz0encPath="C:/SuperMarioGravity/Tools/Archive/Rarc Tools/yaz0enc.exe" # komprimieren
    # yaz0decPath="C:/SuperMarioGravity/Tools/Archive/Rarc Tools/yaz0dec.exe" # entschluesseln
    #WiiExplorerPathFolder="C:/SuperMarioGravity/Tools/Archive/WiiExplorer.V1.5.0.5/"
    WiiExplorerPath=WiiExplorerPathFolder + "WiiExplorer.exe"
    # ArcToolPath="C:/SuperMarioGravity/Tools/Archive/Rarc Tools/ARCTool_ver0.1.5.0.exe" #Es muss ver0.1.5.0 sein, sonst fragt er dauernd, obs komprimiert werden soll




    ### GalaxyMap oeffnen und core infos sammeln

    #GalaxyMapName = "TestomatMap" #TEST
    #GalaxyMapName = bpy.context.scene.name
    GalaxyMapNameWithExt = GalaxyMapName + ".arc"
    GalaxyMapNameEcn = GalaxyMapNameWithExt + " 0.rarc"

    MapName = GalaxyMapName + "Map"


    #GalaxyFilesystem = "C:/SuperMarioGravity/FILESYSTEM/FILESYSTEM/StageData/"
    #GalaxyFilesystem = "C:\\TESTi\\StageData\\" #test


    # #Mit Wiiexplorer stagemap zu arc packen und komprimieren
    # subprocess.run([str(WiiExplorerPath), str("-p"), str("-yz"), str(bpy.path.abspath("//05_MapExport\\" + MapName + "\\stage"))])

    
    GalaxyFilesystem2 = GalaxyFilesystem.replace("/", "\\") #Geht sonst nicht, was weiss ich
    
    #Ordnerstruktur im Filesystem erstellen, falls es noch nicht existiert
    os.popen(("mkdir ") + (GalaxyFilesystem2 + GalaxyMapName + "\\")).read()
    
    # Dummy ARC mit richtigem Root Namen ins Filesystem stecken
    
    #ARCtemplate_bytes = b'\x59\x61\x7A\x30\x00\x00\x00\xC0\x00\x00\x00\x00\x00\x00\x00\x00\xFF\x52\x41\x52\x43\x00\x00\x00\xC0\x5A\x10\x03\x20\x10\x07\xA0\x00\x00\x00\x00\x01\x50\x1B\xAE\x02\x10\x27\x40\x50\x27\x80\x00\x02\x20\x16\xFD\x00\x00\x52\x4F\x4F\x54\x20\x33\x35\x9E\xA2\x30\x1F\xF0\x3E\xFF\xFF\x00\x2E\x10\x38\xAB\x06\x50\x57\x10\x50\x13\xB8\x10\x4C\x08\xFF\x1F\x10\x00\x60\x13\x00\x03\x06\x73\x74\x61\x67\x65\xF8\x00\x2E\x00\x2E\x2E\x00\x25\x04'
     
    # Mit ExportInfo.txt Debug Text, zum Checken der Version und so 
    ARCtemplate_bytes = b'\x59\x61\x7A\x30\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\x52\x41\x52\x43\x00\x00\x01\x00\x54\x10\x00\x20\x10\x04\xA0\x10\x08\x40\x50\x03\x60\x02\xA7\x01\x50\x1B\x03\x50\x1B\x20\x27\x80\x00\x03\x7D\x30\x33\x00\x52\x4F\x4F\x54\x20\x3C\x35\x9F\xA2\x30\x1F\x00\x02\x01\x83\x94\x11\x00\x00\xAF\x0B\x50\x4F\x26\x20\x68\xFF\xFF\x00\x2E\xF5\x02\x00\x00\x06\x50\x63\x10\x50\x13\xB8\x63\x10\x13\x08\xFF\x10\x00\x60\x13\x20\x94\x73\x74\xFF\x61\x67\x65\x00\x2E\x00\x2E\x2E\xFF\x00\x45\x78\x70\x6F\x72\x74\x49\xFE\x6E\x66\x6F\x2E\x74\x78\x74\x50\xA0\x7F\x40\x14\x65\x64\x20\x77\x69\x74\x68\xFF\x20\x53\x75\x70\x65\x72\x42\x6C\xFF\x65\x6E\x64\x65\x72\x47\x61\x6C\xFF\x61\x78\x79\x20\x76\x2E\x30\x2E\xC0\x36\x00\x00\x00\x07'
     
     
    with open(GalaxyFilesystem + GalaxyMapName + "\\" +  MapName + ".arc", "wb") as binary_file:
        # Write bytes to file
        binary_file.write(ARCtemplate_bytes)
    

    ##Mit WiiExplorer zur Arc verschicken
    #Achtung: WiiExplorer's Rootname ist immer Root und nicht Stage, scheint dem Spiel aber wurscht zu sein EDIT: Aber nicht Whitehole! shit EDIT:Fixed
    subprocess.run([str(WiiExplorerPath), str("--script"), str(WiiExplorerPathFolder+"BlenderMapScript_Pack.txt"), str(MapName), str(bpy.path.abspath("//05_MapExport\\" + MapName + "\\stage\\jmp")), str(bpy.path.abspath("//05_MapExport\\" + MapName + "\\stage\\camera")), str(GalaxyFilesystem + GalaxyMapName + str("\\") +  MapName + ".arc"), str("jmp"), str("camera")])
    # 0 = Mapname, 1 = Pfad zur jmp, 2 = Pfad zur camera, 3 = Arc Export Pfad, 4 = 'jmp', 5 = 'camera'



    #Arc zum Filesystem verschieben und richtigen Namen geben
    #shutil.move((bpy.path.abspath("//05_MapExport\\" + MapName + ".arc")), (GalaxyFilesystem + GalaxyMapName + str("\\") +  MapName + ".arc"))
	
    
def ScenarioArcPack(GalaxyMapName, WiiExplorerPathFolder, GalaxyFilesystem):



    #WiiExplorerPathFolder="C:/SuperMarioGravity/Tools/Archive/WiiExplorer.V1.5.0.5/"
    WiiExplorerPath=WiiExplorerPathFolder + "WiiExplorer.exe"
    MapScenarioName = GalaxyMapName + "Scenario"


    #GalaxyFilesystem = "C:/SuperMarioGravity/FILESYSTEM/FILESYSTEM/StageData/"
    #GalaxyFilesystem = "C:\\TESTi\\StageData\\" #test
    
    GalaxyFilesystem2 = GalaxyFilesystem.replace("/", "\\") #Geht sonst nicht, was weiss ich
    
    #Ordnerstruktur im Filesystem erstellen, falls es noch nicht existiert
    os.popen(("mkdir ") + (GalaxyFilesystem2 + GalaxyMapName + str("\\"))).read()
    

    ##Mit WiiExplorer in Arc packen und zum Filesystem verschicken
    ##Root Name ist vollkommen wurscht!
    subprocess.run([str(WiiExplorerPath), str("--script"), str(WiiExplorerPathFolder+"BlenderMapScript_PackScenario.txt"), str(MapScenarioName), str(bpy.path.abspath("//05_MapExport\\" + MapScenarioName + "\\GalaxyInfo.bcsv")), str(bpy.path.abspath("//05_MapExport\\" + MapScenarioName + "\\ScenarioData.bcsv")), str(bpy.path.abspath("//05_MapExport\\" + MapScenarioName + "\\ZoneList.bcsv")), str(GalaxyFilesystem + GalaxyMapName + str("\\") +  MapScenarioName + ".arc"), str("GalaxyInfo.bcsv"), str("ScenarioData.bcsv"), str("ZoneList.bcsv")])
    # 0 = Arcname, 1 = Pfad zur galaxyinfo, 2 = Pfad zur scenario, 3 = pfad zur zonenliste, 4 = Arc Export Pfad, 5 = 'GalaxyInfo', 6 = 'ScenarioData', 7 = Zonelist

    
def CameraEdit(GalaxyMapName, WiiExplorerPathFolder, CameraEditorPathFolder):

    import bpy
    import math
    import os
    import shutil
    import subprocess
    C = bpy.context
    import struct
    import os.path

    #GalaxyMapName = bpy.context.scene.name
    MapName = GalaxyMapName + "Map"
    WiiExplorerPath = WiiExplorerPathFolder + "WiiExplorer.exe"
    CameraEditorPath = CameraEditorPathFolder + "LaunchCamPlus.exe"
    CSVheadings = "version:Int:0,id:String:0,camtype:String:0,string:String:0,angleB:Float:0.0,angleA:Float:0.0,roll:Float:0.0,dist:Float:0.0,fovy:Float:0.0,camint:Int:0,camendint:Int:0,gndint:Int:0,num1:Int:0,num2:Int:0,uplay:Float:0.0,lplay:Float:0.0,pushdelay:Int:0,pushdelaylow:Int:0,udown:Int:0,loffset:Float:0.0,loffsetv:Float:0.0,upper:Float:0.0,lower:Float:0.0,evfrm:Int:0,evpriority:Int:0,woffset.X:Float:0.0,woffset.Y:Float:0.0,woffset.Z:Float:0.0,wpoint.X:Float:0.0,wpoint.Y:Float:0.0,wpoint.Z:Float:0.0,axis.X:Float:0.0,axis.Y:Float:0.0,axis.Z:Float:0.0,vpanaxis.X:Float:0.0,vpanaxis.Y:Float:0.0,vpanaxis.Z:Float:0.0,up.X:Float:0.0,up.Y:Float:0.0,up.Z:Float:0.0,flag.noreset:Int:0,flag.nofovy:Int:0,flag.lofserpoff:Int:0,flag.antibluroff:Int:0,flag.collisionoff:Int:0,flag.subjectiveoff:Int:0,gflag.enableEndErpFrame:Int:0,gflag.thru:Int:0,gflag.camendint:Int:0,vpanuse:Int:0,eflag.enableEndErpFrame:Int:0,eflag.enableErpFrame:Int:0"


    #Camera Ordner erstellen falls es noch nicht existiert
    os.popen(("mkdir ") + (bpy.path.abspath("//05_MapExport\\" + MapName + "\\stage\\camera\\"))).read()


    #Erstelle leere BCAM Datei wenn sie noch nicht existiert 
    path = bpy.path.abspath("//05_MapExport\\" + MapName + "\\stage\\camera\\CameraParam.bcam")
    check_file = os.path.isfile(path)

    if check_file == False: 
        blenderCipher=open(path, 'w') # Text Datei erstellen und oeffnen
        blenderCipher.write(CSVheadings) #Die Headings hinzufuegen
        blenderCipher.close() #CSV Datei schliessen
        #Wandle CSV zu BCSV
        import subprocess
        os.popen(("pyjmap tojmap smg ") + path + (" ") + path)


    #CAMERA EDITOR STARTEN
    subprocess.Popen([str(CameraEditorPath), str(bpy.path.abspath("//05_MapExport\\" + MapName + "\\stage\\camera\\CameraParam.bcam"))])



def LayerDisplay(val):
    import bpy
    import math
    import csv
    import sys
    import os
    import shutil
    import subprocess
    C = bpy.context
    import struct
    import requests
    import bpy
    import math
    import csv
    import sys
    import os
    import shutil
    import subprocess
    C = bpy.context
    import struct
    import requests

    #LayerMask = bpy.context.scene[val]
    LayerMask = bpy.context.view_layer[val]
    LayerMask = int(LayerMask)
    print(LayerMask)

    #LayerMask = 49479

    print()
    print()
    print("===========")
    print()
    print()

    if LayerMask >= 32768:
        LayerP = True
        LayerMask = LayerMask - 32768
    else:
        LayerP = False


    if LayerMask >= 16384:
        LayerO = True
        LayerMask = LayerMask - 16384
    else:
        LayerO = False


    if LayerMask >= 8192:
        LayerN = True
        LayerMask = LayerMask - 8192
    else:
        LayerN = False


    if LayerMask >= 4096:
        LayerM = True
        LayerMask = LayerMask - 4096
    else:
        LayerM = False


    if LayerMask >= 2048:
        LayerL = True
        LayerMask = LayerMask - 2048
    else:
        LayerL = False


    if LayerMask >= 1024:
        LayerK = True
        LayerMask = LayerMask - 1024
    else:
        LayerK = False


    if LayerMask >= 512:
        LayerJ = True
        LayerMask = LayerMask - 512
    else:
        LayerJ = False


    if LayerMask >= 256:
        LayerI = True
        LayerMask = LayerMask - 256
    else:
        LayerI = False


    if LayerMask >= 128:
        LayerH = True
        LayerMask = LayerMask - 128
    else:
        LayerH = False


    if LayerMask >= 64:
        LayerG = True
        LayerMask = LayerMask - 64
    else:
        LayerG = False


    if LayerMask >= 32:
        LayerF = True
        LayerMask = LayerMask - 32
    else:
        LayerF = False


    if LayerMask >= 16:
        LayerE = True
        LayerMask = LayerMask - 16
    else:
        LayerE = False


    if LayerMask >= 8:
        LayerD = True
        LayerMask = LayerMask - 8
    else:
        LayerD = False


    if LayerMask >= 4:
        LayerC = True
        LayerMask = LayerMask - 4
    else:
        LayerC = False


    if LayerMask >= 2:
        LayerB = True
        LayerMask = LayerMask - 2
    else:
        LayerB = False


    if LayerMask >= 1:
        LayerA = True
        LayerMask = LayerMask - 1
    else:
        LayerA = False

    active = bpy.context.view_layer.objects.active
    for obj in bpy.data.collections[val].all_objects:
        if (obj["Layer"]) == "LayerA":
            if LayerA == True:
                obj.hide_set(False)

            else:
                obj.hide_set(True)
                
        if (obj["Layer"]) == "LayerB":
            if LayerB == True:
                obj.hide_set(False)
            else:
                obj.hide_set(True)
                
        if (obj["Layer"]) == "LayerC":
            if LayerC == True:
                obj.hide_set(False)
            else:
                obj.hide_set(True)
                
        if (obj["Layer"]) == "LayerD":
            if LayerD == True:
                obj.hide_set(False)
            else:
                obj.hide_set(True)
                
        if (obj["Layer"]) == "LayerE":
            if LayerE == True:
                obj.hide_set(False)
            else:
                obj.hide_set(True)
                
        if (obj["Layer"]) == "LayerF":
            if LayerF == True:
                obj.hide_set(False)
            else:
                obj.hide_set(True)
                
        if (obj["Layer"]) == "LayerG":
            if LayerG == True:
                obj.hide_set(False)
            else:
                obj.hide_set(True)
                
        if (obj["Layer"]) == "LayerH":
            if LayerH == True:
                obj.hide_set(False)
            else:
                obj.hide_set(True)
                
        if (obj["Layer"]) == "LayerI":
            if LayerI == True:
                obj.hide_set(False)
            else:
                obj.hide_set(True)
                
        if (obj["Layer"]) == "LayerJ":
            if LayerJ == True:
                obj.hide_set(False)
            else:
                obj.hide_set(True)
                
        if (obj["Layer"]) == "LayerK":
            if LayerK == True:
                obj.hide_set(False)
            else:
                obj.hide_set(True)
                
        if (obj["Layer"]) == "LayerL":
            if LayerL == True:
                obj.hide_set(False)
            else:
                obj.hide_set(True)
                
        if (obj["Layer"]) == "LayerM":
            if LayerM == True:
                obj.hide_set(False)
            else:
                obj.hide_set(True)
                
        if (obj["Layer"]) == "LayerN":
            if LayerN == True:
                obj.hide_set(False)
            else:
                obj.hide_set(True)
                
        if (obj["Layer"]) == "LayerO":
            if LayerO == True:
                obj.hide_set(False)
            else:
                obj.hide_set(True)
                
        if (obj["Layer"]) == "LayerP":
            if LayerP == True:
                obj.hide_set(False)
            else:
                obj.hide_set(True)
        
        
        
        

	
def CSVtoBlender(self, GalaxyMapName, ZoneID, AssetSearch, MapAssetBlendFile, BlendFilesFolder):
    import bpy
    import math
    import csv
    import sys
    import os
    import shutil
    import subprocess
    C = bpy.context
    import struct
    import requests
    import os.path


    #GalaxyMapName = bpy.context.scene.name #WIRD NUN IN EINEM ANDEREM SCRIPT DEFINIERT



    ## Zonenprefix:
    
    ZonePrefix = "  (Z" + str(ZoneID) + ")"
    if ZoneID == 0:
        ZonePrefix = ""
    
    
    
    #### Checken welche Layers die Map enthaelt #####

    if os.path.isdir(bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName)) + "Map" + ("//stage//jmp//Placement//LayerA")):
        LayerA = True
    else:
        LayerA = False

    if os.path.isdir(bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName)) + "Map" + ("//stage//jmp//Placement//LayerB")):
        LayerB = True
    else:
        LayerB = False
        
    if os.path.isdir(bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName)) + "Map" + ("//stage//jmp//Placement//LayerC")):
        LayerC = True
    else:
        LayerC = False
        
    if os.path.isdir(bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName)) + "Map" + ("//stage//jmp//Placement//LayerD")):
        LayerD = True
    else:
        LayerD = False
        
    if os.path.isdir(bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName)) + "Map" + ("//stage//jmp//Placement//LayerE")):
        LayerE = True
    else:
        LayerE = False
        
    if os.path.isdir(bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName)) + "Map" + ("//stage//jmp//Placement//LayerF")):
        LayerF = True
    else:
        LayerF = False
        
    if os.path.isdir(bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName)) + "Map" + ("//stage//jmp//Placement//LayerG")):
        LayerG = True
    else:
        LayerG = False
        
    if os.path.isdir(bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName)) + "Map" + ("//stage//jmp//Placement//LayerH")):
        LayerH = True
    else:
        LayerH = False
        
    if os.path.isdir(bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName)) + "Map" + ("//stage//jmp//Placement//LayerI")):
        LayerI = True
    else:
        LayerI = False
        
    if os.path.isdir(bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName)) + "Map" + ("//stage//jmp//Placement//LayerJ")):
        LayerJ = True
    else:
        LayerJ = False
        
    if os.path.isdir(bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName)) + "Map" + ("//stage//jmp//Placement//LayerK")):
        LayerK = True
    else:
        LayerK = False
        
    if os.path.isdir(bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName)) + "Map" + ("//stage//jmp//Placement//LayerL")):
        LayerL = True
    else:
        LayerL = False
        
    if os.path.isdir(bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName)) + "Map" + ("//stage//jmp//Placement//LayerM")):
        LayerM = True
    else:
        LayerM = False
        
    if os.path.isdir(bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName)) + "Map" + ("//stage//jmp//Placement//LayerN")):
        LayerN = True
    else:
        LayerN = False
        
    if os.path.isdir(bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName)) + "Map" + ("//stage//jmp//Placement//LayerO")):
        LayerO = True
    else:
        LayerO = False
        
    if os.path.isdir(bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName)) + "Map" + ("//stage//jmp//Placement//LayerP")):
        LayerP = True
    else:
        LayerP = False



    # GalaxyMapNameWithExt = GalaxyMapName + ".arc"
    # GalaxyMapNameEcn = GalaxyMapNameWithExt + " 0.rarc"

    # GalaxyFilesystem = "C:/SuperMarioGravity/FILESYSTEM/FILESYSTEM/StageData/"



    dirname = bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName)) + "Map" + ("//")


    ####CSV zu Blender Operationen########################

    def CSVimport_DebugMoveInfo():
        CSVname = (dirname) + ("stage/jmp/Debug/") + (LAYERname) + ("/DebugMoveInfo")
        
        ##Zaehlen, wie viele rows es gibt
        file = open(CSVname)
        row_count = len(file.readlines())
        print(row_count)

        with open (CSVname) as f:
            #reader = csv.reader(f)
            reader = csv.DictReader(f) #So liest er anhand column namen row['bla'] und nicht row[3]
            #row = next(reader) #gehe zur naechsten Row #Wegen das in der letzten Zeile unnoetig
            
            for i in range(row_count): #row_count ist wie oft er das hier wiederholen soll
                for row in reader:
                    
                    name = row['name:String:0']
                    I_id = int(row['l_id:Int:0'])
                    pos_x = float(row['pos_x:Float:0.0'])
                    pos_y = float(row['pos_z:Float:0.0']) *-1
                    pos_z = float(row['pos_y:Float:0.0'])       # Yoben ist in Blender Zoben
                    dir_x = float(row['dir_x:Float:0.0'])
                    dir_y = float(row['dir_z:Float:0.0']) *-1
                    dir_z = float(row['dir_y:Float:0.0'])
                    scale_x = float(row['scale_x:Float:0.0'])
                    scale_y = float(row['scale_z:Float:0.0'])# *-1
                    scale_z = float(row['scale_y:Float:0.0'])   
            
                    dir_x = dir_x * math.pi/180  #grad zu radians, fuer Blender
                    dir_y = dir_y * math.pi/180
                    dir_z = dir_z * math.pi/180

                    print("Debug Objekt kommt -----------------------------------")
                    print(name)
                    print()
                    bpy.ops.object.empty_add(type='ARROWS', radius=50, align='WORLD', location=(pos_x, pos_y, pos_z), scale=(scale_x, scale_y, scale_z), rotation=(dir_x, dir_y, dir_z))
                    #Scaling beim vorherigen Befehl wird ignoriert, lol. Also:
                    bpy.context.object.scale[0] = scale_x
                    bpy.context.object.scale[1] = scale_y
                    bpy.context.object.scale[2] = scale_z
                    
                    bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
                    
                    bpy.context.view_layer.objects.active.name = name
                    bpy.context.object["Object Name"] = name
                    bpy.context.object["Link ID"] = I_id
                    
                    bpy.context.object["Layer"] = LAYERname
                    
                    obj = bpy.context.active_object # our created cube is the active one
                    bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
                    bpy.data.collections['Debug' + ZonePrefix].objects.link(obj)# add it to our specific collection
                    #bpy.data.collections[LAYERname].objects.link(obj)# Extra Link wegen Layers 
                    #bpy.ops.object.collection_link(collection='Debug')

                    
                    break


    def CSVimport_MiscLists(): #GLE
        
        ## Erstmal checken, ob es GLE relevante DAteien hat: 
        
        GLEcheck = 0
        
        Pfad = (dirname) + ("stage/jmp/List/ScenarioSettings")
        check_file = os.path.isfile(Pfad)
        if check_file == True:
            ScenarioSettingsExist = True
            GLEcheck = GLEcheck + 1
        else:
            ScenarioSettingsExist = False
            
            
        
            
        CSVname = (dirname) + ("stage/jmp/List/ChangeSceneListInfo")
        check_file = os.path.isfile(CSVname)
        print("check_file")
        print(check_file)
        if check_file == True:
            ##Zaehlen, wie viele Columns es gibt
            with open (CSVname) as f:
                data = list(csv.reader(f))
                #RowNumber = ("rows:", len(data))
                ColumnNumber = len(data[0])
            print("ColumnNumber:")
            print(ColumnNumber)
            if ColumnNumber >= 7:
                ChangeSceneList = True
                GLEcheck = GLEcheck + 1
            else:
                ChangeSceneList = False
                    
            
                
        CSVname = (dirname) + ("stage/jmp/List/StageInfo")
        check_file = os.path.isfile(CSVname)
        if check_file == True:
            ##Zaehlen, wie viele Columns es gibt
            with open (CSVname) as f:
                data = list(csv.reader(f))
                #RowNumber = ("rows:", len(data))
                ColumnNumber = len(data[0])
                if ColumnNumber >= 3:
                    StageInfoExist = True
                    GLEcheck = GLEcheck + 1
                else:
                    StageInfoExist = False
        
        
        if GLEcheck > 0:
            GLEMap = True
        else:
            GLEMap = False
      
        print("Is Map a GLE Map:")
        print(GLEcheck)
        
        if GLEMap == True:
            ####GLE Collection erstellen
            shared_assets_collection_name = GalaxyMapName
            cname = "GLE" + ZonePrefix
            context = bpy.context
            name = cname
            scene = context.scene
            coll = bpy.data.collections.get(name)
            # if it doesn't exist create it
            if coll is None:
                print("Existiert noch nicht")
            else:
                col = bpy.data.collections.get(name)
                if col:
                    col.name = name + "_OLD"
				
            c = bpy.data.collections.new(cname)
            bpy.data.collections.get(shared_assets_collection_name).children.link(c)
        
            #Erst ScenarioSettings importieren
            if ScenarioSettingsExist == True:
            
                CSVname = (dirname) + ("stage/jmp/List/ScenarioSettings")
                
                ##Zaehlen, wie viele rows es gibt
                file = open(CSVname)
                row_count = len(file.readlines())
                print(row_count)

                with open (CSVname) as f:
                    #reader = csv.reader(f)
                    reader = csv.DictReader(f) #So liest er anhand column namen row['bla'] und nicht row[3]
                    #row = next(reader) #gehe zur naechsten Row #Wegen das in der letzten Zeile unnoetig
                    
                    for i in range(row_count): #row_count ist wie oft er das hier wiederholen soll
                        for row in reader:
                            
                            ScenarioNo = row['ScenarioNo:Int:0']
                            NoStarChance = row['[AD3040E7]:Char:0']
                            PlayAttackMan = row['[042858FE]:Char:0']  ##  ##
                            ScoreAttack = row['[9ED80B5A]:Char:0']
                            RaceId = row['[9172CFEC]:Char:0']
                            RaceTutorial = row['[E854CD6F]:Char:0']
                            ManualPurpleCoin = row['[EE3174F3]:Char:0']
                            NoStopClock = row['[2094384B]:Char:0']
                            NoPause = row['[E0253095]:Char:0']
                            NoPauseReturn = row['[F734D625]:Char:0']
                            NoPauseExit = row['[F2620B53]:Char:0']  
                            StoryLayout = row['[0B713C5F]:Char:0']
                            PeachStarGet = row['[31A66813]:Char:0']
                            PauseVol = row['[4FC5431D]:Float:0.0']
                            NoWelcome = row['[E4347A41]:Char:0']
                            NoScenarioTitle = row['[38D97447]:Char:0']
                            NoBootOut = row['[9E939DDB]:Char:0']
                            try:
                                PauseStarSource = row["[C0241383]:String:0"] # ??
                            except:
                                PauseStarSource = str("")

                            print("GLE - Scenario Settings kommt -----------------------------------")
                            print()
                            
                            bpy.ops.object.empty_add(type='ARROWS', radius=50, align='WORLD', location=(0.0, 0.0, 0.0), scale=(1, 1, 1))
                            
                            bpy.context.view_layer.objects.active.name = "GLE-MapSettings__Scenario" + ScenarioNo
                            bpy.context.object["ScenarioNo"] = ScenarioNo
                            bpy.context.object["NoStarChance"] = NoStarChance
                            bpy.context.object["PlayAttackMan"] = PlayAttackMan
                            bpy.context.object["ScoreAttack"] = ScoreAttack
                            bpy.context.object["RaceId"] = RaceId
                            bpy.context.object["RaceTutorial"] = RaceTutorial
                            bpy.context.object["ManualPurpleCoin"] = ManualPurpleCoin
                            bpy.context.object["NoStopClock"] = NoStopClock
                            bpy.context.object["NoPause"] = NoPause
                            bpy.context.object["NoPauseReturn"] = NoPauseReturn
                            bpy.context.object["NoPauseExit"] = NoPauseExit
                            bpy.context.object["StoryLayout"] = StoryLayout
                            bpy.context.object["PeachStarGet"] = PeachStarGet
                            bpy.context.object["PauseVol"] = PauseVol
                            bpy.context.object["PauseStarSource"] = PauseStarSource
                                
                            bpy.context.object["NoWelcome"] = NoWelcome
                            bpy.context.object["NoScenarioTitle"] = NoScenarioTitle
                            bpy.context.object["NoBootOut"] = NoBootOut
                            
                            obj = bpy.context.active_object # our created cube is the active one
                            bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
                            bpy.data.collections["GLE" + ZonePrefix].objects.link(obj)# add it to our specific collection
                            #bpy.data.collections[LAYERname].objects.link(obj)# Extra Link wegen Layers 
                            #bpy.ops.object.collection_link(collection='Debug')

                            
                            break

            ##Jetzt ChangeSceneList
            if ChangeSceneList == True:
            
                CSVname = (dirname) + ("stage/jmp/List/ChangeSceneListInfo")
                
                #Zaehlen, wie viele rows es gibt
                file = open(CSVname)
                row_count = len(file.readlines())
                print(row_count)

                with open (CSVname) as f:
                    reader = csv.reader(f)
                    row = next(reader) #gehe zur naechsten Row
                    
                    for i in range(row_count): #row_count ist wie oft er das hier wiederholen soll
                        for row in reader:
                            
                            GalaxyName = row[0]
                            ScenarioNo = row[1]
                            ZoneName = row[2]
                            MarioNo = row[3]
                            Player = row[4]
                            ResultPathId = row[5]
                            EntryPathId = row[6]

                            print("GLE - ChangeSceneList kommt -----------------------------------")
                            print()
                            
                            bpy.ops.object.empty_add(type='ARROWS', radius=50, align='WORLD', location=(0.0, 0.0, 0.0), scale=(1, 1, 1))
                            
                            bpy.context.view_layer.objects.active.name = "GLE-ChangeSceneList__Scenario" + ScenarioNo
                            bpy.context.object["GalaxyName"] = GalaxyName
                            bpy.context.object["ScenarioNo"] = ScenarioNo
                            bpy.context.object["ZoneName"] = ZoneName
                            bpy.context.object["MarioNo"] = MarioNo
                            bpy.context.object["Player"] = Player
                            bpy.context.object["ResultPathId"] = ResultPathId
                            bpy.context.object["EntryPathId"] = EntryPathId  ##  ##
                            
                            obj = bpy.context.active_object # our created cube is the active one
                            bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
                            bpy.data.collections["GLE" + ZonePrefix].objects.link(obj)# add it to our specific collection
                            #bpy.data.collections[LAYERname].objects.link(obj)# Extra Link wegen Layers 
                            #bpy.ops.object.collection_link(collection='Debug')

                            
                            break

            ##Und jetzt StageInfo:
            if StageInfoExist == True:
                
                CSVname = (dirname) + ("stage/jmp/List/StageInfo")
                
                #Zaehlen, wie viele rows es gibt
                file = open(CSVname)
                row_count = len(file.readlines())
                print(row_count)

                with open (CSVname) as f:
                    reader = csv.reader(f)
                    row = next(reader) #gehe zur naechsten Row
                    
                    for i in range(row_count): #row_count ist wie oft er das hier wiederholen soll
                        for row in reader:
                            
                            Type = row[0]
                            ScenarioNo = row[1]
                            Param00Int = row[2]

                            print("GLE - StageInfo kommt -----------------------------------")
                            print()
                            
                            bpy.ops.object.empty_add(type='ARROWS', radius=50, align='WORLD', location=(0.0, 0.0, 0.0), scale=(1, 1, 1))
                            
                            bpy.context.view_layer.objects.active.name = "GLE-StageInfo__Scenario" + ScenarioNo
                            bpy.context.object["Type"] = Type
                            bpy.context.object["Scenario No"] = ScenarioNo
                            bpy.context.object["Index into the ChangeSceneListInfo file"] = Param00Int ## ##
                            
                            obj = bpy.context.active_object # our created cube is the active one
                            bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
                            bpy.data.collections["GLE" + ZonePrefix].objects.link(obj)# add it to our specific collection
                            #bpy.data.collections[LAYERname].objects.link(obj)# Extra Link wegen Layers 
                            #bpy.ops.object.collection_link(collection='Debug')

                            
                            break
                        
    def CSVimport_GeneralPosInfo():
        CSVname = (dirname) + ("stage/jmp/GeneralPos/") + (LAYERname) + ("/GeneralPosInfo")
        
        ##Zaehlen, wie viele rows es gibt
        file = open(CSVname)
        row_count = len(file.readlines())
        print(row_count)

        with open (CSVname) as f:
            #reader = csv.reader(f)
            reader = csv.DictReader(f) #So liest er anhand column namen row['bla'] und nicht row[3]
            #row = next(reader) #gehe zur naechsten Row #Wegen das in der letzten Zeile unnoetig
            
            for i in range(row_count):
                for row in reader:
                    
                    name = row['name:String:0']
                    PosName = row['PosName:String:0']
                    pos_x = float(row['pos_x:Float:0.0'])
                    pos_y = float(row['pos_z:Float:0.0']) *-1
                    pos_z = float(row['pos_y:Float:0.0'])       # Yoben ist in Blender Zoben
                    dir_x = float(row['dir_x:Float:0.0'])
                    dir_y = float(row['dir_z:Float:0.0']) *-1
                    dir_z = float(row['dir_y:Float:0.0'])
                    #scale_x = float(row[8])
                    #scale_y = float(row[10]) #*-1
                    #scale_z = float(row[9])
                    Obj_ID = int(row['Obj_ID:Short:0'])  
            
                    dir_x = dir_x * math.pi/180  #grad zu radians, fuer Blender
                    dir_y = dir_y * math.pi/180
                    dir_z = dir_z * math.pi/180

                    print("GeneralPos Objekt kommt -----------------------------------")
                    print(name)
                    print()
                    bpy.ops.object.empty_add(type='SINGLE_ARROW', radius=50, align='WORLD', location=(pos_x, pos_y, pos_z), scale=(1, 1, 1), rotation=(dir_x, dir_y, dir_z))
                    bpy.context.view_layer.objects.active.name = name
                    bpy.context.object["Object Name"] = name
                    bpy.context.object["Linked Object ID"] = Obj_ID
                    bpy.context.object["Position Name"] = PosName
                    
                    bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
                    
                    bpy.context.object["Layer"] = LAYERname
                    
                    obj = bpy.context.active_object # our created cube is the active one
                    bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
                    bpy.data.collections['Positions' + ZonePrefix].objects.link(obj)# add it to our specific collection
                    #bpy.data.collections[LAYERname].objects.link(obj)# Extra Link wegen Layers 
                    #bpy.ops.object.collection_link(collection='Positions')

                    
                    break




    def CSVimport_MapPartsInfo():
        CSVname = (dirname) + ("stage/jmp/MapParts/") + (LAYERname) + ("/MapPartsInfo")
        
        ##Zaehlen, wie viele rows es gibt
        file = open(CSVname)
        row_count = len(file.readlines())
        print(row_count)

        with open (CSVname) as f:
            #reader = csv.reader(f)
            reader = csv.DictReader(f) #So liest er anhand column namen row['bla'] und nicht row[3]
            #row = next(reader) #gehe zur naechsten Row #Wegen das in der letzten Zeile unnoetig
            
            for i in range(row_count):
                for row in reader:
                    
                    name = row['name:String:0']
                    I_id = int(row['l_id:Int:0'])
                    MoveConditionType = int(row['MoveConditionType:Int:0'])
                    RotateSpeed = int(row['RotateSpeed:Int:0'])
                    RotateAngle = int(row['RotateAngle:Int:0'])
                    RotateAxis = int(row['RotateAxis:Int:0'])                
                    RotateAccelType = int(row['RotateAccelType:Int:0'])                
                    RotateStopTime = int(row['RotateStopTime:Int:0'])                
                    RotateType = int(row['RotateType:Int:0'])  
                    ShadowType = int(row['ShadowType:Int:0'])  
                    SignMotionType = int(row['SignMotionType:Int:0'])  
                    PressType = int(row['PressType:Int:0'])  
                    ParamScale = float(row['ParamScale:Float:0.0']) 
                    CameraSetId = int(row['CameraSetId:Int:0'])
                    FarClip = int(row['FarClip:Int:0']    )        
                    Obj_arg0 = int(row['Obj_arg0:Int:0'])
                    Obj_arg1 = int(row['Obj_arg1:Int:0'])
                    Obj_arg2 = int(row['Obj_arg2:Int:0'])
                    Obj_arg3 = int(row['Obj_arg3:Int:0'])

                    SW_APPEAR = int(row['SW_APPEAR:Int:0'])
                    SW_DEAD = int(row['SW_DEAD:Int:0'])
                    SW_A = int(row['SW_A:Int:0'])
                    SW_B = int(row['SW_B:Int:0'])
                    SW_AWAKE = int(row['SW_AWAKE:Int:0'])
                    SW_PARAM = int(row['SW_PARAM:Int:0'])

                    pos_x = float(row['pos_x:Float:0.0'])
                    pos_y = float(row['pos_z:Float:0.0']) *-1
                    pos_z = float(row['pos_y:Float:0.0'])       # Yoben ist in Blender Zoben
                    dir_x = float(row['dir_x:Float:0.0'])
                    dir_y = float(row['dir_z:Float:0.0']) *-1
                    dir_z = float(row['dir_y:Float:0.0'])
                    scale_x = float(row['scale_x:Float:0.0'])
                    scale_y = float(row['scale_z:Float:0.0'])# *-1
                    scale_z = float(row['scale_y:Float:0.0'])
                    
                    CastId = int(row['CastId:Int:0'])
                    ViewGroupId = int(row['ViewGroupId:Int:0'])
                    ShapeModelNo = int(row['ShapeModelNo:Short:0'])
                    CommonPath_ID = int(row['CommonPath_ID:Short:0'])
                    ClippingGroupId = int(row['ClippingGroupId:Short:0'])
                    GroupId = int(row['GroupId:Short:0'])
                    DemoGroupId = int(row['DemoGroupId:Short:0'])
                    MapParts_ID = int(row['MapParts_ID:Short:0'])
                    Obj_ID = int(row['Obj_ID:Short:0'])
                    ParentId = int(row['ParentId:Short:0'])    
            
                    dir_x = dir_x * math.pi/180  #grad zu radians, fuer Blender
                    dir_y = dir_y * math.pi/180
                    dir_z = dir_z * math.pi/180

                    print("MapPart Objekt kommt -----------------------------------")
                    print(name)
                    print()
                    bpy.ops.object.empty_add(type='PLAIN_AXES', radius=50, align='WORLD', location=(pos_x, pos_y, pos_z), scale=(scale_x, scale_y, scale_z), rotation=(dir_x, dir_y, dir_z))
                    #Scaling beim vorherigen Befehl wird ignoriert, lol. Also:
                    bpy.context.object.scale[0] = scale_x
                    bpy.context.object.scale[1] = scale_y
                    bpy.context.object.scale[2] = scale_z
                    
                    bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
                    
                    bpy.context.view_layer.objects.active.name = name
                    bpy.context.object["Object Name"] = name
                    bpy.context.object["Link ID"] = I_id
                    bpy.context.object["MoveConditionType"] = MoveConditionType
                    bpy.context.object["RotateSpeed"] = RotateSpeed
                    bpy.context.object["RotateAngle"] = RotateAngle
                    bpy.context.object["RotateAxis"] = RotateAxis
                    bpy.context.object["RotateAccelType"] = RotateAccelType
                    bpy.context.object["RotateStopTime"] = RotateStopTime
                    bpy.context.object["RotateType"] = RotateType
                    bpy.context.object["ShadowType"] = ShadowType
                    bpy.context.object["SignMotionType"] = SignMotionType
                    bpy.context.object["PressType"] = PressType
                    bpy.context.object["Speed Scale"] = ParamScale
                    bpy.context.object["Camera Set ID"] = CameraSetId
                    bpy.context.object["Far Clip"] = FarClip
                    
                    bpy.context.object["Obj_Arg0"] = Obj_arg0
                    bpy.context.object["Obj_Arg1"] = Obj_arg1
                    bpy.context.object["Obj_Arg2"] = Obj_arg2
                    bpy.context.object["Obj_Arg3"] = Obj_arg3
                    
                    bpy.context.object["SW_APPEAR"] = SW_APPEAR
                    bpy.context.object["SW_DEAD"] = SW_DEAD
                    bpy.context.object["SW_A"] = SW_A
                    bpy.context.object["SW_B"] = SW_B
                    bpy.context.object["SW_AWAKE"] = SW_AWAKE
                    bpy.context.object["SW_PARAM"] = SW_PARAM
                    
                    bpy.context.object["Cast Group ID"] = CastId
                    bpy.context.object["View Group ID"] = ViewGroupId
                    bpy.context.object["Model ID"] = ShapeModelNo
                    bpy.context.object["Path ID"] = CommonPath_ID
                    bpy.context.object["Clipping Group ID"] = ClippingGroupId
                    bpy.context.object["Group ID"] = GroupId
                    bpy.context.object["Cutscene Group ID"] = DemoGroupId
                    bpy.context.object["Linked MapParts ID"] = MapParts_ID
                    bpy.context.object["Linked Object ID"] = Obj_ID
                    bpy.context.object["Parent Object ID"] = ParentId

                    bpy.context.object["Layer"] = LAYERname
                    
                    if AssetSearch == True:
                    
                        try:
                            bpy.context.object.instance_type = 'COLLECTION'
                            bpy.context.object.instance_collection = bpy.data.collections[ObjektName]
                        except:
                            print("Asset nicht in aktiver Blenderdatei")
                    
                    
                            ### WIP - Linke Assets von anderen Blender Dateien ###    
                            ##Idee: Das weglassen, und stattdessen als separaten Button einbauen, um Objekten ohne Assets es dann hinzubla       
                            
                            from bpy.props import StringProperty, BoolProperty
                            from pathlib import Path

                            def get_glob_files(folder, suffix, recursive=True):
                                s = f'**/*{suffix}'  if recursive else f'*{suffix}'
                                return [str(fp) for fp in Path(folder).glob(s) if fp.is_file()]

                            # test
                            #folder_path = "C:\\SuperMarioGravity\\WORKSPACE\\01_Galaxien"
                            folder_path = BlendFilesFolder
                            print(get_glob_files(folder_path, '.blend'))
                            #directory = folder_path
                            for blend in get_glob_files(folder_path, '.blend'):
                                try:

                                    # path to the blend
                                    #filepath = (self.directory, '.blend') #Kann man auch Library statt Blend Datei durchsuchen?
                                    filepath = blend
                                    print("Lese von dieser Blend Datei:")
                                    print(blend)
                                    
                                    if filepath == bpy.data.filepath:
                                        print("Not allow load library from current file")
                                        # Don't append current file, It will crash blender even the code inside the try:
                                        #return
                                    else:
                                    
                                        # name of collection(s) to append or link
                                        coll_name = name
                                        # append, set to true to keep the link to the original file
                                        link = True
                                        # link all collections starting with 'objekttest'
                                        with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                                            data_to.collections = [c for c in data_from.collections if c.startswith(coll_name)]
                                        # link collection to selected Empty
                                        bpy.context.object.instance_type = 'COLLECTION'
                                        bpy.context.object.instance_collection = bpy.data.collections[name]
                                except:
                                    print("Dieses Asset wurde in der Library nicht gefunden:")
                                    print(name)
                                    pass
                            ### WIP - Linke Assets von anderen Blender Dateien ### ENDE


                    obj = bpy.context.active_object # our created cube is the active one
                    bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
                    bpy.data.collections['MapParts' + ZonePrefix].objects.link(obj)# add it to our specific collection
                    #bpy.data.collections[LAYERname].objects.link(obj)# Extra Link wegen Layers 
                    


                    
                    break





    def CSVimport_Placement_AreaObjInfo():
        CSVname = (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ("/AreaObjInfo")
        
        ##Zaehlen, wie viele rows es gibt
        file = open(CSVname)
        row_count = len(file.readlines())
        print(row_count)

        with open (CSVname) as f:
            #reader = csv.reader(f)
            reader = csv.DictReader(f) #So liest er anhand column namen row['bla'] und nicht row[3]
            #row = next(reader) #gehe zur naechsten Row #Wegen das in der letzten Zeile unnoetig
            
            for i in range(row_count):
                for row in reader:
                    
                    name = row['name:String:0']
                    I_id = int(row['l_id:Int:0'])
                    Obj_arg0 = int(row['Obj_arg0:Int:0'])
                    Obj_arg1 = int(row['Obj_arg1:Int:0'])
                    Obj_arg2 = int(row['Obj_arg2:Int:0'])
                    Obj_arg3 = int(row['Obj_arg3:Int:0'])
                    Obj_arg4 = int(row['Obj_arg4:Int:0'])
                    Obj_arg5 = int(row['Obj_arg5:Int:0'])
                    Obj_arg6 = int(row['Obj_arg6:Int:0'])
                    Obj_arg7 = int(row['Obj_arg7:Int:0'])
                    Priority = int(row['Priority:Int:0'])
                    SW_APPEAR = int(row['SW_APPEAR:Int:0'])
                    SW_A = int(row['SW_A:Int:0'])
                    SW_B = int(row['SW_B:Int:0'])
                    SW_AWAKE = int(row['SW_AWAKE:Int:0'])
                    
                    pos_x = float(row['pos_x:Float:0.0'])
                    pos_y = float(row['pos_z:Float:0.0']) *-1
                    pos_z = float(row['pos_y:Float:0.0'])       # Yoben ist in Blender Zoben
                    dir_x = float(row['dir_x:Float:0.0'])
                    dir_y = float(row['dir_z:Float:0.0']) *-1
                    dir_z = float(row['dir_y:Float:0.0'])
                    scale_x = float(row['scale_x:Float:0.0'])
                    scale_y = float(row['scale_z:Float:0.0']) #*-1
                    scale_z = float(row['scale_y:Float:0.0'])
                    
                    FollowId = int(row['FollowId:Int:0'])
                    AreaShapeNo = str(row['AreaShapeNo:Short:0'])
                    CommonPath_ID = int(row['CommonPath_ID:Short:0'])
                    ClippingGroupId = int(row['ClippingGroupId:Short:0'])
                    GroupId = int(row['GroupId:Short:0'])
                    DemoGroupId = int(row['DemoGroupId:Short:0'])
                    MapParts_ID = int(row['MapParts_ID:Short:0'])
                    Obj_ID = int(row['Obj_ID:Short:0'])
            
                    dir_x = dir_x * math.pi/180  #grad zu radians, fuer Blender
                    dir_y = dir_y * math.pi/180
                    dir_z = dir_z * math.pi/180

                    print("Areal kommt -----------------------------------")
                    print(name)
                    print()
                    bpy.ops.object.empty_add(type='PLAIN_AXES', radius=20, align='WORLD', location=(pos_x, pos_y, pos_z), scale=(scale_x, scale_y, scale_z), rotation=(dir_x, dir_y, dir_z))
                    #Scaling beim vorherigen Befehl wird ignoriert, lol. Also:
                    bpy.context.object.scale[0] = scale_x
                    bpy.context.object.scale[1] = scale_y
                    bpy.context.object.scale[2] = scale_z
                    #bpy.context.object.instance_type = 'COLLECTION'
                    
                    bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
                    
                    bpy.context.view_layer.objects.active.name = name
                    bpy.context.object["Object Name"] = name
                    bpy.context.object["Link ID"] = I_id
                    bpy.context.object["Obj_Arg0"] = Obj_arg0
                    bpy.context.object["Obj_Arg1"] = Obj_arg1
                    bpy.context.object["Obj_Arg2"] = Obj_arg2
                    bpy.context.object["Obj_Arg3"] = Obj_arg3
                    bpy.context.object["Obj_Arg4"] = Obj_arg4
                    bpy.context.object["Obj_Arg5"] = Obj_arg5
                    bpy.context.object["Obj_Arg6"] = Obj_arg6
                    bpy.context.object["Obj_Arg7"] = Obj_arg7
                    bpy.context.object["Priority"] = Priority
                    bpy.context.object["SW_APPEAR"] = SW_APPEAR
                    bpy.context.object["SW_A"] = SW_A
                    bpy.context.object["SW_B"] = SW_B
                    bpy.context.object["SW_AWAKE"] = SW_AWAKE
                    
                    bpy.context.object["Linked Area ID"] = FollowId
                    #bpy.context.object["Shape ID"] = AreaShapeNo
                    bpy.context.object["Path ID"] = CommonPath_ID
                    bpy.context.object["Clipping Group ID"] = ClippingGroupId
                    bpy.context.object["Group ID"] = GroupId
                    bpy.context.object["Cutscene Group ID"] = DemoGroupId
                    bpy.context.object["Linked MapParts ID"] = MapParts_ID
                    bpy.context.object["Linked Object ID"] = Obj_ID
                    
                    bpy.context.object["Layer"] = LAYERname
                    
                    ########################################### COLLECTION LINK
                    
                    try:

                        if AreaShapeNo == '0':
                            AreaShapeCOL = "AreaShape 0  Cube" #Dem Emtpy eine Collection Instanz zuweisen
                        if AreaShapeNo == '1':
                            AreaShapeCOL = "AreaShape 1  Cube Middle" #Dem Emtpy eine Collection Instanz zuweisen    
                        if AreaShapeNo == '2':
                            AreaShapeCOL = "AreaShape 2  Sphere" #Dem Emtpy eine Collection Instanz zuweisen
                        if AreaShapeNo == '3':
                            AreaShapeCOL = "AreaShape 3  Cylinder" #Dem Emtpy eine Collection Instanz zuweisen
                        if AreaShapeNo == '4':
                            AreaShapeCOL = "AreaShape 4  Half Sphere" #Dem Emtpy eine Collection Instanz zuweisen

                        #folder = bpy.path.abspath("//")

                        # get all blend files in the folder
                        #blends = [f for f in os.listdir(folder) if f.endswith(".blend")]

                        #for blend in blends:

                        # path to the blend
                        filepath = MapAssetBlendFile
                        # name of collection(s) to append or link
                        coll_name = AreaShapeCOL #FIX oder
                        # append, set to true to keep the link to the original file
                        link = True
                        # link all collections lose an die Blenderdatei
                        with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                            data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 0  Cube")]
                        
                        with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                            data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 1  Cube Middle")]
                        
                        with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                            data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 2  Sphere")]
                            
                        with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                            data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 3  Cylinder")]
                            
                        with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                            data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 4  Half Sphere")]
                            
                        # link collection to selected Empty
                        bpy.context.object.instance_type = 'COLLECTION'
                        bpy.context.object.instance_collection = bpy.data.collections[AreaShapeCOL]
                        

                        
                    except:
                        print("KEIN ZUGRIFF AUF DIE BLEND DATEI")
                        print(name)
                        pass
                    
                    #################################  COLLECTION LINK END
                    
                    
                    
                    
                    obj = bpy.context.active_object # our created cube is the active one
                    bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
                    bpy.data.collections['Areas' + ZonePrefix].objects.link(obj)# add it to our specific collection
                    #bpy.data.collections[LAYERname].objects.link(obj)# Extra Link wegen Layers 
                    #bpy.ops.object.collection_link(collection='Areas')

                    
                    break






    def CSVimport_Placement_CameraCubeInfo():
        CSVname = (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ("/CameraCubeInfo")
        
        ##Zaehlen, wie viele rows es gibt
        file = open(CSVname)
        row_count = len(file.readlines())
        print(row_count)

        with open (CSVname) as f:
            #reader = csv.reader(f)
            reader = csv.DictReader(f) #So liest er anhand column namen row['bla'] und nicht row[3]
            #row = next(reader) #gehe zur naechsten Row #Wegen das in der letzten Zeile unnoetig
            
            for i in range(row_count):
                for row in reader:
                    
                    name = row['name:String:0']
                    I_id = int(row['l_id:Int:0'])
                    Obj_arg0 = int(row['Obj_arg0:Int:0'])
                    Obj_arg1 = int(row['Obj_arg1:Int:0'])
                    Obj_arg2 = int(row['Obj_arg2:Int:0'])
                    Obj_arg3 = int(row['Obj_arg3:Int:0'])
                    InterpolateIn = int(row['InterpolateIn:Int:0']) #eh unused
                    InterpolateOut = int(row['InterpolateOut:Int:0']) #
                    SW_APPEAR = int(row['SW_APPEAR:Int:0'])
                    SW_A = int(row['SW_A:Int:0'])
                    SW_B = int(row['SW_B:Int:0'])
                    SW_AWAKE = int(row['SW_AWAKE:Int:0'])
                    Validity = row['Validity:String:0'] #was ist das
                    
                    pos_x = float(row['pos_x:Float:0.0'])
                    pos_y = float(row['pos_z:Float:0.0']) *-1
                    pos_z = float(row['pos_y:Float:0.0'])       # Yoben ist in Blender Zoben
                    dir_x = float(row['dir_x:Float:0.0'])
                    dir_y = float(row['dir_z:Float:0.0']) *-1
                    dir_z = float(row['dir_y:Float:0.0'])
                    scale_x = float(row['scale_x:Float:0.0'])
                    scale_y = float(row['scale_z:Float:0.0']) #*-1
                    scale_z = float(row['scale_y:Float:0.0'])
                    
                    FollowId = int(row['FollowId:Int:0'])
                    AreaShapeNo = str(row['AreaShapeNo:Short:0'])
                    MapParts_ID = int(row['MapParts_ID:Short:0'])
                    Obj_ID = int(row['Obj_ID:Short:0']) 
            
                    dir_x = dir_x * math.pi/180  #grad zu radians, fuer Blender
                    dir_y = dir_y * math.pi/180
                    dir_z = dir_z * math.pi/180

                    print("Kamera Areal kommt -----------------------------------")
                    print(name)
                    print()
                    bpy.ops.object.empty_add(type='SPHERE', radius=20, align='WORLD', location=(pos_x, pos_y, pos_z), scale=(scale_x, scale_y, scale_z), rotation=(dir_x, dir_y, dir_z))
                    #Scaling beim vorherigen Befehl wird ignoriert, lol. Also:
                    bpy.context.object.scale[0] = scale_x
                    bpy.context.object.scale[1] = scale_y
                    bpy.context.object.scale[2] = scale_z
                    bpy.context.object.instance_type = 'COLLECTION'

                    bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus

                    bpy.context.view_layer.objects.active.name = name
                    bpy.context.object["Object Name"] = name
                    bpy.context.object["Link ID"] = I_id
                    bpy.context.object["Camera ID"] = Obj_arg0
                    bpy.context.object["Obj_Arg1"] = Obj_arg1
                    bpy.context.object["Priority"] = Obj_arg2
                    bpy.context.object["Affected Contexts"] = Obj_arg3
                    bpy.context.object["Interpolate In (Unused)"] = InterpolateIn
                    bpy.context.object["Interpolate Out (Unused)"] = InterpolateOut
                    bpy.context.object["SW_APPEAR"] = SW_APPEAR
                    bpy.context.object["SW_A"] = SW_A
                    bpy.context.object["SW_B"] = SW_B
                    bpy.context.object["SW_AWAKE"] = SW_AWAKE
                    bpy.context.object["Validity"] = Validity
                    bpy.context.object["Linked Area ID"] = FollowId
                    #bpy.context.object["Shape ID"] = AreaShapeNo
                    bpy.context.object["Linked MapParts ID"] = MapParts_ID
                    bpy.context.object["Linked Object ID"] = Obj_ID
                    
                    bpy.context.object["Layer"] = LAYERname
                    
                    ########################################### COLLECTION LINK
                    
                    try:

                        if AreaShapeNo == '0':
                            AreaShapeCOL = "AreaShape 0  Cube" #Dem Emtpy eine Collection Instanz zuweisen
                        if AreaShapeNo == '1':
                            AreaShapeCOL = "AreaShape 1  Cube Middle" #Dem Emtpy eine Collection Instanz zuweisen    
                        if AreaShapeNo == '2':
                            AreaShapeCOL = "AreaShape 2  Sphere" #Dem Emtpy eine Collection Instanz zuweisen
                        if AreaShapeNo == '3':
                            AreaShapeCOL = "AreaShape 3  Cylinder" #Dem Emtpy eine Collection Instanz zuweisen
                        if AreaShapeNo == '4':
                            AreaShapeCOL = "AreaShape 4  Half Sphere" #Dem Emtpy eine Collection Instanz zuweisen



                        # path to the blend
                        filepath = MapAssetBlendFile
                        # name of collection(s) to append or link
                        coll_name = AreaShapeCOL #FIX oder
                        # append, set to true to keep the link to the original file
                        link = True
                        # link all collections starting with 'objekttest'
                        with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                            data_to.collections = [c for c in data_from.collections if c.startswith(coll_name)]
                        # link collection to selected Empty
                        bpy.context.object.instance_type = 'COLLECTION'
                        bpy.context.object.instance_collection = bpy.data.collections[AreaShapeCOL]
                        

                        
                    except:
                        print("KEIN ZUGRIFF AUF DIE BLEND DATEI")
                        print(name)
                        pass
                    
                    ################################# COLLECTION LINK END
                    
                    obj = bpy.context.active_object # our created cube is the active one
                    bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
                    bpy.data.collections['Cameras' + ZonePrefix].objects.link(obj)# add it to our specific collection
                    #bpy.data.collections[LAYERname].objects.link(obj)# Extra Link wegen Layers 
                    #bpy.ops.object.collection_link(collection='Cameras')

                    
                    break





    def CSVimport_Placement_DemoObjInfo():
        CSVname = (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ("/DemoObjInfo")
        
        ##Zaehlen, wie viele rows es gibt
        file = open(CSVname)
        row_count = len(file.readlines())
        print(row_count)

        with open (CSVname) as f:
            #reader = csv.reader(f)
            reader = csv.DictReader(f) #So liest er anhand column namen row['bla'] und nicht row[3]
            #row = next(reader) #gehe zur naechsten Row #Wegen das in der letzten Zeile unnoetig
            
            for i in range(row_count):
                for row in reader:
                    
                    name = row['name:String:0']
                    DemoName = row['DemoName:String:0']
                    TimeSheetName = row['TimeSheetName:String:0']
                    I_id = int(row['l_id:Int:0'])
                    SW_APPEAR = int(row['SW_APPEAR:Int:0'])
                    SW_DEAD = int(row['SW_DEAD:Int:0'])
                    SW_A = int(row['SW_A:Int:0'])
                    SW_B = int(row['SW_B:Int:0'])
                    DemoSkip = int(row['DemoSkip:Int:0'])
                    
                    pos_x = float(row['pos_x:Float:0.0'])
                    pos_y = float(row['pos_z:Float:0.0']) *-1
                    pos_z = float(row['pos_y:Float:0.0'])       # Yoben ist in Blender Zoben
                    dir_x = float(row['dir_x:Float:0.0'])
                    dir_y = float(row['dir_z:Float:0.0']) *-1
                    dir_z = float(row['dir_y:Float:0.0'])
                    scale_x = float(row['scale_x:Float:0.0'])
                    scale_y = float(row['scale_z:Float:0.0'])# *-1
                    scale_z = float(row['scale_y:Float:0.0'])      
            
                    dir_x = dir_x * math.pi/180  #grad zu radians, fuer Blender
                    dir_y = dir_y * math.pi/180
                    dir_z = dir_z * math.pi/180

                    print("Cutscenen Objekt kommt -----------------------------------")
                    print(name)
                    print()
                    bpy.ops.object.empty_add(type='CUBE', radius=50, align='WORLD', location=(pos_x, pos_y, pos_z), scale=(scale_x, scale_y, scale_z), rotation=(dir_x, dir_y, dir_z))
                    #Scaling beim vorherigen Befehl wird ignoriert, lol. Also:
                    bpy.context.object.scale[0] = scale_x
                    bpy.context.object.scale[1] = scale_y
                    bpy.context.object.scale[2] = scale_z
                    
                    bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
                    
                    bpy.context.view_layer.objects.active.name = name
                    bpy.context.object["Object Name"] = name
                    
                    bpy.context.object["Cutscene Name"] = DemoName
                    bpy.context.object["Sheet Name"] = TimeSheetName
                    bpy.context.object["Link ID"] = I_id
                    bpy.context.object["SW_APPEAR"] = SW_APPEAR
                    bpy.context.object["SW_DEAD"] = SW_DEAD
                    bpy.context.object["SW_A"] = SW_A
                    bpy.context.object["SW_B"] = SW_B
                    bpy.context.object["Skippable"] = DemoSkip
                    
                    bpy.context.object["Layer"] = LAYERname
                    
                    obj = bpy.context.active_object # our created cube is the active one
                    bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
                    bpy.data.collections['Cutscenes' + ZonePrefix].objects.link(obj)# add it to our specific collection
                    #bpy.data.collections[LAYERname].objects.link(obj)# Extra Link wegen Layers 
                    #bpy.ops.object.collection_link(collection='Cutscenes')

                    
                    break







    def CSVimport_Placement_ObjInfo():
        CSVname = (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ("/ObjInfo")
        
        ##Zaehlen, wie viele rows es gibt
        file = open(CSVname)
        row_count = len(file.readlines())
        print(row_count)

        with open (CSVname) as f:
            #reader = csv.reader(f)
            reader = csv.DictReader(f) #So liest er anhand column namen row['bla'] und nicht row[3]
            #row = next(reader) #gehe zur naechsten Row #Wegen das in der letzten Zeile unnoetig
            
            for i in range(row_count):
                for row in reader:
                    
                    name = row['name:String:0']
                    I_id = int(row['l_id:Int:0'])
                    obj_arg0 = int(row['Obj_arg0:Int:0'])
                    obj_arg1 = int(row['Obj_arg1:Int:0'])
                    obj_arg2 = int(row['Obj_arg2:Int:0'])
                    obj_arg3 = int(row['Obj_arg3:Int:0'])
                    obj_arg4 = int(row['Obj_arg4:Int:0'])
                    obj_arg5 = int(row['Obj_arg5:Int:0'])
                    obj_arg6 = int(row['Obj_arg6:Int:0'])
                    obj_arg7 = int(row['Obj_arg7:Int:0'])
                    CameraSetId = int(row['CameraSetId:Int:0'])
                    SW_APPEAR = int(row['SW_APPEAR:Int:0'])
                    SW_DEAD = int(row['SW_DEAD:Int:0'])
                    SW_A = int(row['SW_A:Int:0'])
                    SW_B = int(row['SW_B:Int:0'])
                    SW_AWAKE = int(row['SW_AWAKE:Int:0'])
                    SW_PARAM = int(row['SW_PARAM:Int:0'])
                    MessageId = int(row['MessageId:Int:0'])
                    ParamScale = float(row['ParamScale:Float:0.0'])
                    
                    pos_x = float(row['pos_x:Float:0.0'])
                    pos_y = float(row['pos_z:Float:0.0']) *-1
                    pos_z = float(row['pos_y:Float:0.0'])       # Yoben ist in Blender Zoben
                    dir_x = float(row['dir_x:Float:0.0'])
                    dir_y = float(row['dir_z:Float:0.0']) *-1
                    dir_z = float(row['dir_y:Float:0.0'])
                    scale_x = float(row['scale_x:Float:0.0'])
                    scale_y = float(row['scale_z:Float:0.0']) #*-1
                    scale_z = float(row['scale_y:Float:0.0'])
                    
                    CastId = int(row['CastId:Int:0'])
                    ViewGroupId = int(row['ViewGroupId:Int:0'])
                    ShapeModelNo = int(row['ShapeModelNo:Short:0'])
                    CommonPath_ID = int(row['CommonPath_ID:Short:0'])
                    ClippingGroupId = int(row['ClippingGroupId:Short:0'])
                    GroupId = int(row['GroupId:Short:0'])
                    DemoGroupId = int(row['DemoGroupId:Short:0'])
                    MapParts_ID = int(row['MapParts_ID:Short:0'])
                    Obj_ID = int(row['Obj_ID:Short:0'])
                    GeneratorID = int(row['GeneratorID:Short:0'])
            
                    dir_x = dir_x * math.pi/180  #grad zu radians, fuer Blender
                    dir_y = dir_y * math.pi/180
                    dir_z = dir_z * math.pi/180

                    print("Objekt kommt -----------------------------------")
                    print(name)
                    print()
                    bpy.ops.object.empty_add(type='CUBE', radius=50, align='WORLD', location=(pos_x, pos_y, pos_z), scale=(scale_x, scale_y, scale_z), rotation=(dir_x, dir_y, dir_z))
                    #Scaling beim vorherigen Befehl wird ignoriert, lol. Also:
                    bpy.context.object.scale[0] = scale_x
                    bpy.context.object.scale[1] = scale_y
                    bpy.context.object.scale[2] = scale_z
                    
                    bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
                    
                    bpy.context.view_layer.objects.active.name = name
                    bpy.context.object["Object Name"] = name
                    bpy.context.object["Link ID"] = I_id
                    bpy.context.object["Obj_Arg0"] = obj_arg0
                    bpy.context.object["Obj_Arg1"] = obj_arg1
                    bpy.context.object["Obj_Arg2"] = obj_arg2
                    bpy.context.object["Obj_Arg3"] = obj_arg3
                    bpy.context.object["Obj_Arg4"] = obj_arg4
                    bpy.context.object["Obj_Arg5"] = obj_arg5
                    bpy.context.object["Obj_Arg6"] = obj_arg6
                    bpy.context.object["Obj_Arg7"] = obj_arg7
                    bpy.context.object["Camera Set ID"] = CameraSetId
                    bpy.context.object["SW_APPEAR"] = SW_APPEAR
                    bpy.context.object["SW_DEAD"] = SW_DEAD
                    bpy.context.object["SW_A"] = SW_A
                    bpy.context.object["SW_B"] = SW_B
                    bpy.context.object["SW_AWAKE"] = SW_AWAKE
                    bpy.context.object["SW_PARAM"] = SW_PARAM
                    bpy.context.object["Message ID"] = MessageId
                    bpy.context.object["Speed Scale"] = ParamScale
                    bpy.context.object["Cast Group ID"] = CastId
                    bpy.context.object["View Group ID"] = ViewGroupId
                    bpy.context.object["Model ID"] = ShapeModelNo
                    bpy.context.object["Path ID"] = CommonPath_ID
                    bpy.context.object["Clipping Group ID"] = ClippingGroupId
                    bpy.context.object["Group ID"] = GroupId
                    bpy.context.object["Cutscene Group ID"] = DemoGroupId
                    bpy.context.object["Linked MapParts ID"] = MapParts_ID
                    bpy.context.object["Linked Object ID"] = Obj_ID
                    bpy.context.object["Generator Object ID"] = GeneratorID
                    
                    bpy.context.object["Layer"] = LAYERname
                    
                    if AssetSearch == True:
                    
                        try:
                            bpy.context.object.instance_type = 'COLLECTION'
                            bpy.context.object.instance_collection = bpy.data.collections[ObjektName]
                        except:
                            print("Asset nicht in aktiver Blenderdatei")
                    
                    
                            ### WIP - Linke Assets von anderen Blender Dateien ###    
                            ##Idee: Das weglassen, und stattdessen als separaten Button einbauen, um Objekten ohne Assets es dann hinzubla       
                            
                            from bpy.props import StringProperty, BoolProperty
                            from pathlib import Path

                            def get_glob_files(folder, suffix, recursive=True):
                                s = f'**/*{suffix}'  if recursive else f'*{suffix}'
                                return [str(fp) for fp in Path(folder).glob(s) if fp.is_file()]

                            # test
                            #folder_path = "C:\\SuperMarioGravity\\WORKSPACE\\01_Galaxien"
                            folder_path = BlendFilesFolder
                            print(get_glob_files(folder_path, '.blend'))
                            #directory = folder_path
                            for blend in get_glob_files(folder_path, '.blend'):
                                try:

                                    # path to the blend
                                    #filepath = (self.directory, '.blend') #Kann man auch Library statt Blend Datei durchsuchen?
                                    filepath = blend
                                    print("Lese von dieser Blend Datei:")
                                    print(blend)
                                    if filepath == bpy.data.filepath:
                                        print("Not allow load library from current file")
                                        # Don't append current file, It will crash blender even the code inside the try:
                                        #return
                                    else:
                                    
                                        # name of collection(s) to append or link
                                        coll_name = name
                                        # append, set to true to keep the link to the original file
                                        link = True
                                        # link all collections starting with 'objekttest'
                                        with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                                            data_to.collections = [c for c in data_from.collections if c.startswith(coll_name)]
                                        # link collection to selected Empty
                                        bpy.context.object.instance_type = 'COLLECTION'
                                        bpy.context.object.instance_collection = bpy.data.collections[name]
                                except:
                                    print("Dieses Asset wurde in der Library nicht gefunden:")
                                    print(name)
                                    pass
                        ### WIP - Linke Assets von anderen Blender Dateien ### ENDE
                    
                    
                    #bpy.context.object["LAYER"] = LAYERname
                    #bpy.ops.object.move_to_collection(collection='Objects')
                    #bpy.ops.object.collection_link(collection=LAYERname)
                    
                    obj = bpy.context.active_object # Erstellte Obj is the active one
                    bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
                    bpy.data.collections['Objects' + ZonePrefix].objects.link(obj)# add it to our specific collection
                    #bpy.data.collections[LAYERname].objects.link(obj)# Extra Link wegen Layers
                    #bpy.context.object["Layer"] = LAYERname
                    #bpy.ops.object.collection_link(collection=LAYERname)#Extra Link wegen Layers

                    
                    break
            






    def CSVimport_Placement_PlanetObjInfo(): #Gravity
        CSVname = (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ("/PlanetObjInfo")
        
        ##Zaehlen, wie viele rows es gibt
        file = open(CSVname)
        row_count = len(file.readlines())
        print(row_count)

        with open (CSVname) as f:
            #reader = csv.reader(f)
            reader = csv.DictReader(f) #So liest er anhand column namen row['bla'] und nicht row[3]
            #row = next(reader) #gehe zur naechsten Row #Wegen das in der letzten Zeile unnoetig
            
            for i in range(row_count):
                for row in reader:
                    
                    name = row['name:String:0']
                    I_id = int(row['l_id:Int:0'])
                    Obj_arg0 = int(row['Obj_arg0:Int:0'])
                    Obj_arg1 = int(row['Obj_arg1:Int:0'])
                    Obj_arg2 = int(row['Obj_arg2:Int:0'])
                    Obj_arg3 = int(row['Obj_arg3:Int:0'])
                    Range = float(row['Range:Float:0.0'])
                    Distant = float(row['Distant:Float:0.0'])
                    Priority = int(row['Priority:Int:0'])
                    Inverse = int(row['Inverse:Int:0'])
                    Power = row['Power:String:0']
                    Gravity_type = row['Gravity_type:String:0'] #ACHTUNG, das ist nur dieses Heavy dings. Objektname definiert den Typ
                    SW_APPEAR = int(row['SW_APPEAR:Int:0'])
                    SW_DEAD = int(row['SW_DEAD:Int:0'])
                    SW_A = int(row['SW_A:Int:0'])
                    SW_B = int(row['SW_B:Int:0'])
                    SW_AWAKE = int(row['SW_AWAKE:Int:0'])
                    
                    pos_x = float(row['pos_x:Float:0.0'])
                    pos_y = float(row['pos_z:Float:0.0']) *-1
                    pos_z = float(row['pos_y:Float:0.0'])       # Yoben ist in Blender Zoben
                    dir_x = float(row['dir_x:Float:0.0'])
                    dir_y = float(row['dir_z:Float:0.0']) *-1
                    dir_z = float(row['dir_y:Float:0.0'])
                    scale_x = float(row['scale_x:Float:0.0'])
                    scale_y = float(row['scale_z:Float:0.0'])# *-1
                    scale_z = float(row['scale_y:Float:0.0'])
                    
                    FollowId = int(row['FollowId:Int:0'])
                    CommonPath_ID = int(row['CommonPath_ID:Short:0'])
                    ClippingGroupId = int(row['ClippingGroupId:Short:0'])
                    GroupId = int(row['GroupId:Short:0'])
                    DemoGroupId = int(row['DemoGroupId:Short:0'])
                    MapParts_ID = int(row['MapParts_ID:Short:0'])
                    Obj_ID = int(row['Obj_ID:Short:0'])
            
                    dir_x = dir_x * math.pi/180  #grad zu radians, fuer Blender
                    dir_y = dir_y * math.pi/180
                    dir_z = dir_z * math.pi/180

                    print("Gravity Objekt kommt -----------------------------------")
                    print(name)
                    print()
                    bpy.ops.object.volume_add(align='WORLD', location=(pos_x, pos_y, pos_z), scale=(1, 1, 1), rotation=(dir_x, dir_y, dir_z))
                    #Scaling beim vorherigen Befehl wird ignoriert, lol. Also:
                    #bpy.context.object.scale[0] = scale_x
                    #bpy.context.object.scale[1] = scale_y
                    #bpy.context.object.scale[2] = scale_z
                    
                    bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
                    
                    bpy.context.view_layer.objects.active.name = name
                    
                    bpy.context.object["Object Name"] = name
                    bpy.context.object["Link ID"] = I_id
                    bpy.context.object["Obj_Arg0"] = Obj_arg0
                    bpy.context.object["Obj_Arg1"] = Obj_arg1
                    bpy.context.object["Obj_Arg2"] = Obj_arg2
                    bpy.context.object["Obj_Arg3"] = Obj_arg3
                    
                    bpy.context.object["Range"] = Range
                    bpy.context.object["Distance"] = Distant
                    bpy.context.object["Priority"] = Priority
                    bpy.context.object["Inverse"] = Inverse
                    bpy.context.object["Power"] = Power
                    bpy.context.object["Gravity_type"] = Gravity_type
                    bpy.context.object["SW_APPEAR"] = SW_APPEAR
                    bpy.context.object["SW_DEAD"] = SW_DEAD
                    bpy.context.object["SW_A"] = SW_A
                    bpy.context.object["SW_B"] = SW_B
                    bpy.context.object["SW_AWAKE"] = SW_AWAKE
                    
                    bpy.context.object["Linked Area ID"] = FollowId
                    bpy.context.object["Path ID"] = CommonPath_ID
                    bpy.context.object["Clipping Group ID"] = ClippingGroupId
                    bpy.context.object["Group ID"] = GroupId
                    bpy.context.object["Cutscene Group ID"] = DemoGroupId
                    bpy.context.object["Linked MapParts ID"] = MapParts_ID
                    bpy.context.object["Linked Object ID"] = Obj_ID
                    
                    bpy.context.object["Layer"] = LAYERname
                    
                    bpy.context.object.lock_scale[0] = True ### Scale wird nur in der Geometry Node festgelegt
                    bpy.context.object.lock_scale[1] = True
                    bpy.context.object.lock_scale[2] = True
                    
                    #############################################
                    #Geometry Node linken. Komplizierter Dreck
                    
                    obj = bpy.context.object #geht das so
                    #file_path = "C:\\SuperMarioGravity\\WORKSPACE\\04_Library\\GravityTypes.blend"
                    file_path = MapAssetBlendFile
                    
                    Gravity_type = name
                    
                    node_name = Gravity_type #"GlobalCubeGravity" #test
                    
                    
                    if Gravity_type == "GlobalPlaneGravityInBox":
                        node_name = "GlobalPlaneGravity"
                        
                    if Gravity_type == "GlobalPlaneGravityInCylinder":
                        node_name = "GlobalPlaneGravity"
                    
                    if Gravity_type == "ZeroGravityBox":
                        node_name = "GlobalPlaneGravity"
                        
                    if Gravity_type == "ZeroGravityCylinder":
                        node_name = "GlobalPlaneGravity"
                        
                    if Gravity_type == "ZeroGravitySphere":
                        node_name = "GlobalPlaneGravity"
                        
                    
                    link = True
                    
                    from os.path import join as os_path_join

                    inner_path = "NodeTree"
                    node_groups = bpy.data.node_groups


                    bpy.ops.wm.append(
                        filepath=os_path_join(file_path, inner_path, node_name),
                        directory=os_path_join(file_path, inner_path),
                        filename=node_name,
                        link=link)


                    #modifier=bpy.context.object.modifiers.new("GRAVITY", "NODES")
                    #modifier=bpy.context.view_layer.objects.active.modifiers.new(type='NODES')
                    
                    #bpy.context.object.modifiers.new(type='NODES')
                    #bpy.context.object.modifiers["GeometryNodes"].name = "GRAVITY"
                    #bpy.context.object.modifiers["GRAVITY"].node_group = Gravity_type
                    
                    modifier=bpy.context.object.modifiers.new("GRAVITY", "NODES")
                    
                    try:
                        modifier.node_group = bpy.data.node_groups[node_name]
                    except:
                        modifier.node_group = bpy.data.node_groups["GlobalPlaneGravity"] #Falls es nen ungueltigen Objektnamen nutzt
                    
                    #Gravity Parameter applien:
                    bpy.context.object.modifiers["GRAVITY"]["Input_2"] = float(Range)
                    bpy.context.object.modifiers["GRAVITY"]["Input_3"] = float(Distant)
                    bpy.context.object.modifiers["GRAVITY"]["Input_4"] = int(Obj_arg0)
                    bpy.context.object.modifiers["GRAVITY"]["Input_5"] = int(Obj_arg1)
                    bpy.context.object.modifiers["GRAVITY"]["Input_6"] = int(Obj_arg2)
                    bpy.context.object.modifiers["GRAVITY"]["Input_7"] = int(Obj_arg3)
                    bpy.context.object.modifiers["GRAVITY"]["Input_8"][0] = scale_x
                    bpy.context.object.modifiers["GRAVITY"]["Input_8"][2] = scale_z
                    bpy.context.object.modifiers["GRAVITY"]["Input_8"][1] = scale_y
                    
                    # #Path Zeug:
                    # if not CommonPath_ID == "-1":
                        # target_curve_name = str(CommonPath_ID) + str(ZonePrefix)

                        # for obj in bpy.data.objects:
                            # if obj.type == 'CURVE':
                                # if obj.data.name == target_curve_name:
                                    # ObjectPathObjName = obj
                                    # break
                        
                            # ObjectPathObjName = ObjectPathObjName.name
                        
                            # bpy.context.object.modifiers["GRAVITY"]["Input_9"] = bpy.data.objects[ObjectPathObjName]
                        
                    #nur wenn planar:
                    if Gravity_type == "GlobalPlaneGravity":
                        bpy.context.object.modifiers["GRAVITY"]["Input_10"] = 0 #Sphere
                        bpy.context.object.modifiers["GRAVITY"]["Input_11"] = False #0
                        
                    if Gravity_type == "GlobalPlaneGravityInBox":
                        bpy.context.object.modifiers["GRAVITY"]["Input_10"] = 1 #Cube
                        bpy.context.object.modifiers["GRAVITY"]["Input_11"] = False #0
                        
                    if Gravity_type == "GlobalPlaneGravityInCylinder":
                        bpy.context.object.modifiers["GRAVITY"]["Input_10"] = 2 #Cylinder
                        bpy.context.object.modifiers["GRAVITY"]["Input_11"] = False #0
                        
                    if Gravity_type == "ZeroGravitySphere":
                        bpy.context.object.modifiers["GRAVITY"]["Input_10"] = 0 #Sphere
                        bpy.context.object.modifiers["GRAVITY"]["Input_11"] = True #1
                        
                    if Gravity_type == "ZeroGravityBox":
                        bpy.context.object.modifiers["GRAVITY"]["Input_10"] = 1 #Cube
                        bpy.context.object.modifiers["GRAVITY"]["Input_11"] = True #1
                        
                    if Gravity_type == "ZeroGravityCylinder":
                        bpy.context.object.modifiers["GRAVITY"]["Input_10"] = 2 #Cylinder
                        bpy.context.object.modifiers["GRAVITY"]["Input_11"] = True #1
                    
                    #########################################################
                    
                    #obj = bpy.context.active_object # our created cube is the active one
                    #sack = (bpy.context.collection.name)
                    #bpy.ops.collection.objects_remove_active(collection=sack) #Remove active object from current collection
                    #bpy.data.collections['Gravities' + ZonePrefix].objects.link(obj)# add it to our specific collection
                    
                    
                    # #Der Collection kram muss hier anders sein, weil, was weiss ich leck mich
                    # obj = bpy.context.view_layer.objects.active # Erstellte Obj is the active one
                    # bpy.data.collections['Gravities' + ZonePrefix].objects.link(obj)# add it to our specific collection
                    
                    # new_obj = bpy.context.active_object  # Get a handle on new object
                    # new_obj.users_collection[0].objects.unlink(new_obj)
                    
                    #NEEE GEHT AUCH NET IMMER DIESER DRECK.
                    
                    
                    
                    ##FIX. DER GEHT. YEEEEEEEES
                    col = bpy.data.collections['Gravities' + ZonePrefix]
                    obj = bpy.context.object
                    #bpy.context.scene.collection.children.link(col)
                    for other_col in obj.users_collection:
                        other_col.objects.unlink(obj)
                    if obj.name not in col.objects:
                        col.objects.link(obj)

                    
                    
                    
                    
                    break






    def CSVimport_Placement_StageObjInfo():
        CSVname = (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ("/StageObjInfo")
        
        ##Zaehlen, wie viele rows es gibt
        file = open(CSVname)
        row_count = len(file.readlines())
        print(row_count)

        with open (CSVname) as f:
            #reader = csv.reader(f)
            reader = csv.DictReader(f) #So liest er anhand column namen row['bla'] und nicht row[3]
            #row = next(reader) #gehe zur naechsten Row #Wegen das in der letzten Zeile unnoetig
            
            for i in range(row_count):
                for row in reader:
                    
                    name = row['name:String:0']
                    I_id = int(row['l_id:Int:0'])
                    
                    pos_x = float(row['pos_x:Float:0.0'])
                    pos_y = float(row['pos_z:Float:0.0']) *-1
                    pos_z = float(row['pos_y:Float:0.0'])       # Yoben ist in Blender Zoben
                    dir_x = float(row['dir_x:Float:0.0'])
                    dir_y = float(row['dir_z:Float:0.0']) *-1
                    dir_z = float(row['dir_y:Float:0.0'])  
            
                    dir_x = dir_x * math.pi/180  #grad zu radians, fuer Blender
                    dir_y = dir_y * math.pi/180
                    dir_z = dir_z * math.pi/180

                    print("Zone kommt -----------------------------------")
                    print(name)
                    print()
                    bpy.ops.object.empty_add(type='PLAIN_AXES', radius=100, align='WORLD', location=(pos_x, pos_y, pos_z), scale=(1, 1, 1), rotation=(dir_x, dir_y, dir_z))
                    
                    bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
                    
                    bpy.context.view_layer.objects.active.name = name
                    bpy.context.object["Object Name"] = name
                    bpy.context.object["Link ID"] = I_id
                    
                    bpy.context.object["Layer"] = LAYERname
                    
                    bpy.context.object.instance_type = 'COLLECTION'
                    try:
                        bpy.context.object.instance_collection = bpy.data.collections[name]
                    except:
                        print("This zone was not found:")
                        print(name)
                    
                    obj = bpy.context.active_object # our created cube is the active one
                    bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
                    bpy.data.collections['ZonePositions' + ZonePrefix].objects.link(obj)# add it to our specific collection
                    #bpy.data.collections[LAYERname].objects.link(obj)# Extra Link wegen Layers 
                    #bpy.ops.object.collection_link(collection='ZonePositions')

                    
                    break





    def CSVimport_StartInfo():
        CSVname = (dirname) + ("stage/jmp/Start/") + (LAYERname) + ("/StartInfo")
        
        ##Zaehlen, wie viele rows es gibt
        file = open(CSVname)
        row_count = len(file.readlines())
        print(row_count)

        with open (CSVname) as f:
            #reader = csv.reader(f)
            reader = csv.DictReader(f) #So liest er anhand column namen row['bla'] und nicht row[3]
            #row = next(reader) #gehe zur naechsten Row #Wegen das in der letzten Zeile unnoetig
            
            for i in range(row_count):
                for row in reader:
                    
                    name = row['name:String:0']
                    MarioNo = int(row['MarioNo:Int:0'])
                    obj_arg0 = int(row['Obj_arg0:Int:0'])
                    Camera_id = int(row['Camera_id:Int:0'])
                    
                    pos_x = float(row['pos_x:Float:0.0'])
                    pos_y = float(row['pos_z:Float:0.0']) *-1
                    pos_z = float(row['pos_y:Float:0.0'])       # Yoben ist in Blender Zoben
                    dir_x = float(row['dir_x:Float:0.0'])
                    dir_y = float(row['dir_z:Float:0.0']) *-1
                    dir_z = float(row['dir_y:Float:0.0'])
                    scale_x = float(row['scale_x:Float:0.0'])
                    scale_y = float(row['scale_z:Float:0.0']) #*-1
                    scale_z = float(row['scale_y:Float:0.0'])
                          
            
                    dir_x = dir_x * math.pi/180  #grad zu radians, fuer Blender
                    dir_y = dir_y * math.pi/180
                    dir_z = dir_z * math.pi/180

                    print("Startpunkt kommt -----------------------------------")
                    print(name)
                    print()
                    bpy.ops.object.empty_add(type='PLAIN_AXES', radius=100, align='WORLD', location=(pos_x, pos_y, pos_z), scale=(scale_x, scale_y, scale_z), rotation=(dir_x, dir_y, dir_z))
                    bpy.context.view_layer.objects.active.name = name
                    #bpy.context.object["Object Name"] = name  #Nee, soll eh immer "Mario" sein
                    
                    bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
                    
                    bpy.context.object["Spawn ID"] = MarioNo
                    bpy.context.object["Entrance Type"] = obj_arg0
                    bpy.context.object["Camera ID"] = Camera_id
                    
                    bpy.context.object["Layer"] = LAYERname
                    #bpy.ops.object.move_to_collection(collection='Spawns')
                    
                    obj = bpy.context.active_object # our created cube is the active one
                    bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
                    bpy.data.collections['Spawns' + ZonePrefix].objects.link(obj)# add it to our specific collection
                    #bpy.data.collections[LAYERname].objects.link(obj)# Extra Link wegen Layers             
                    #bpy.ops.object.collection_link(collection=LAYERname)


                    
                    break



    #Paths erstmal importieren
        
    ########################### PATH IMPORT ###########################


    #(dirname) + ("stage/jmp/Path/CommonPathInfo")
    CSVname = (dirname) + ("stage/jmp/Path/CommonPathInfo")
    PathCSVname = (dirname) + ("stage/jmp/Path/CommonPathPointInfo.")

    ##Zaehlen, wie viele rows es gibt
    file = open(CSVname)
    row_count = len(file.readlines())
    print("Anzahl der Paths:")
    print(row_count)

    with open (CSVname) as f:
        reader = csv.reader(f)
        row = next(reader) #gehe zur naechsten Row (ignoriere Header)
        
        for i in range(row_count):
            for row in reader:
                
                name = row[0]
                type = row[1]
                closed = row[2]
                #num_pnt = row[3] #brauchts nicht. Les es vom Path selbst
                l_id = row[4] #WICHTIG. Das ist die ID. Start ist immer 0. 'no' muss auch identisch sein
                path_arg0 = int(row[5])
                path_arg1 = int(row[6])
                path_arg2 = int(row[7])
                path_arg3 = int(row[8])
                path_arg4 = int(row[9])
                path_arg5 = int(row[10])
                path_arg6 = int(row[11])
                path_arg7 = int(row[12])
                usage = row[13]
                no = row[14]  #WICHTIG. Das ist die ID. Start ist immer 0
                #Path_ID = row[15] #Ist immer -1. pfeif drauf
                
                
                #AB HIER LOOP fuer POINTS ###########################
                csv_filepath= PathCSVname + no #+ (".csv")

                # read all control points from csv file
                with open(csv_filepath) as csv_file: # work with the opened file
                    
                    # first read the complete file (we need to know the amount of points)
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    

                    #curve_data = { "control_points": [], "handle_left": [], "handle_right": [] }
                    curve_data = { "control_points": [], "handle_left": [], "handle_right": [] , "point_argument0": [] , "point_argument1": [] , "point_argument2": [] , "point_argument3": [] , "point_argument4": [] , "point_argument5": [] , "point_argument6": [] , "point_argument7": [] }

                    for idx, row in enumerate(csv_reader):
                        if idx != 0: # ignore csv header
                            
                            point_arg0 = int(row[0]) #Speed
                            point_arg1 = int(row[1])    #Acceleraion bla
                            point_arg2 = int(row[2]) #Rotation Speed + Welche Richtung
                            point_arg3 = int(row[3]) #Grad, ob - oder + regelt arg 2
                            point_arg4 = int(row[4]) #Axe
                            point_arg5 = int(row[5]) #Wartezeit
                            point_arg6 = int(row[6]) #Rotation Typ: 1 = Drehe und Bewege, -1 = Stoppe bei jedem Punkt zum Drehen
                            point_arg7 = int(row[7]) #Iwas anderes
                            
                            PointX = float(row[8])
                            PointY = float(row[10]) *-1
                            PointZ = float(row[9])
                            PointC1_X = float(row[11]) #Handle Left
                            PointC1_Y = float(row[13]) *-1
                            PointC1_Z = float(row[12])
                            PointC2_X = float(row[14]) #Handle Right
                            PointC2_Y = float(row[16]) *-1
                            PointC2_Z = float(row[15])
                            
                            # save the curve data (control points and the handles)
                            curve_data["control_points"].append((PointX, PointY, PointZ))
                            curve_data["handle_left"].append((PointC1_X, PointC1_Y, PointC1_Z))
                            curve_data["handle_right"].append((PointC2_X, PointC2_Y, PointC2_Z))
                            
                            #TEST: save args
                            curve_data["point_argument0"].append(point_arg0)
                            curve_data["point_argument1"].append(point_arg1)
                            curve_data["point_argument2"].append(point_arg2)
                            curve_data["point_argument3"].append(point_arg3)
                            curve_data["point_argument4"].append(point_arg4)
                            curve_data["point_argument5"].append(point_arg5)
                            curve_data["point_argument6"].append(point_arg6)
                            curve_data["point_argument7"].append(point_arg7)

                    # create bezier curve and add enough control points to it
                    bpy.ops.curve.primitive_bezier_curve_add(location=(0,0,0))
                    bpy.context.object.name = name
                    bpy.context.object.data.name = no + ZonePrefix
                    if closed == "CLOSE":
                        bpy.context.object.data.splines[0].use_cyclic_u = True
                    
                    curve = bpy.context.active_object
                    bez_points = curve.data.splines[0].bezier_points

                    num_control_points = len(curve_data["control_points"])

                    # note: a created bezier curve has already 2 control points
                    bez_points.add(num_control_points - 2)

                    # now copy the csv data
                    for i in range(num_control_points):      

                        bez_points[i].co = curve_data["control_points"][i]
                        bez_points[i].handle_left_type  = 'FREE'
                        bez_points[i].handle_right_type = 'FREE'
                        
                        # set the handle coordinates
                        bez_points[i].handle_left  = curve_data["handle_left"][i]
                        bez_points[i].handle_right = curve_data["handle_right"][i]
                        
                        
                        ########### Point Args auf Punkte anwenden ################################
                        
                        ## 000 Werte:
                        if curve_data["point_argument0"][i] > -1:
                            PointArg0 = True
                        else:
                            PointArg0 = False
                            
                        if curve_data["point_argument5"][i] > -1:
                            PointArg5 = True
                        else:
                            PointArg5 = False     


                        
                        if curve_data["point_argument1"][i] > -1:
                            PathPointSetup = True
                        else:
                            if curve_data["point_argument2"][i] > -1:
                                PathPointSetup = True
                            else:
                                if curve_data["point_argument3"][i] > -1:
                                    PathPointSetup = True
                                else:
                                    if curve_data["point_argument4"][i] > -1:
                                        PathPointSetup = True
                                    else:
                                        if curve_data["point_argument6"][i] > -1:
                                            PathPointSetup = True
                                        else:
                                            if curve_data["point_argument7"][i] > -1:
                                                PathPointSetup = True
                                            else:
                                                PathPointSetup = False
                            
                            
                        if PathPointSetup == True:
                            Point_ID = str(i)
                            print(("Path Point SETUP for Point ID: ") + (Point_ID))
                            
                            #############################################
                            #Geometry Node linken. Komplizierter Dreck
                            
                            obj = curve
                            file_path = MapAssetBlendFile
                            node_name = "PointArgs1"
                            link = True
                            
                            from os.path import join as os_path_join

                            inner_path = "NodeTree"
                            node_groups = bpy.data.node_groups


                            bpy.ops.wm.append(
                                filepath=os_path_join(file_path, inner_path, node_name),
                                directory=os_path_join(file_path, inner_path),
                                filename=node_name,
                                link=link)


                            modifier=bpy.context.object.modifiers.new(Point_ID, "NODES")
                            
                            modifier.node_group = bpy.data.node_groups['PointArgs1']
                            
                            #########################################################
                            
                            
                            
                            
                            print(int(point_arg1))
                            bpy.context.object.modifiers[str(Point_ID)]["Input_4"] = curve_data["point_argument1"][i]
                            print(int(point_arg2))
                            bpy.context.object.modifiers[str(Point_ID)]["Input_5"] = curve_data["point_argument2"][i]
                            print(int(point_arg3))
                            bpy.context.object.modifiers[str(Point_ID)]["Input_6"] = curve_data["point_argument3"][i]
                            print(int(point_arg4))
                            bpy.context.object.modifiers[str(Point_ID)]["Input_7"] = curve_data["point_argument4"][i]
                            print(int(point_arg6))
                            bpy.context.object.modifiers[str(Point_ID)]["Input_9"] = curve_data["point_argument6"][i]
                            print(int(point_arg7))
                            bpy.context.object.modifiers[str(Point_ID)]["Input_1"] = curve_data["point_argument7"][i]
                            #print(int(point_arg7))
                            bpy.context.object.modifiers[str(Point_ID)]["Input_16"] = int(Point_ID)

                        
                        
                        
                        if PointArg5 == True:
                            bez_points[i].radius = curve_data["point_argument5"][i] * 0.001
                        else:
                            bez_points[i].radius = 1
                            
                        if PointArg0 == True:
                            point_arg0 = curve_data["point_argument0"][i] * math.pi/180  #grad zu radians, fuer Blender
                            bez_points[i].tilt = point_arg0
                        else:
                            
                            bez_points[i].tilt = -1 * math.pi/180
                        

                    #Pivot Point zum ersten Punkt schicken:
                    bpy.context.scene.tool_settings.use_transform_data_origin = True
                    #bpy.ops.transform.translate(value=(PointX, PointY, PointZ), orient_axis_ortho='X', orient_type='GLOBAL') #Geht in 4.3.2 nicht mehr
                    bpy.ops.transform.translate(value=(PointX, PointY, PointZ), orient_type='GLOBAL')
                    bpy.context.scene.tool_settings.use_transform_data_origin = False
                #ENDE DES POINT LOOPS ##############################
                #Settings
                bpy.context.object["Name Alternative"] = name
                bpy.context.object["PathArg0 (Posture Type)"] = path_arg0
                bpy.context.object["PathArg1 (Stop Motion Type)"] = path_arg1
                bpy.context.object["PathArg2 (Guide Type)"] = path_arg2
                bpy.context.object["PathArg3"] = path_arg3
                bpy.context.object["PathArg4 (Initial Position Type)"] = path_arg4
                bpy.context.object["PathArg5"] = path_arg5
                bpy.context.object["PathArg6"] = path_arg6
                bpy.context.object["PathArg7"] = path_arg7
                bpy.context.object["Usage"] = usage

                #obj = bpy.context.active_object # our created cube is the active one
                #bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene #GEHT HIER NICHT. WARUM AUCH IMMER
                # #FIX:
                # for col in bpy.data.collections:
                    # if bpy.context.object in col.objects[:]:
                        # col.objects.unlink(obj)
                # bpy.data.collections['Paths' + ZonePrefix].objects.link(obj)# add it to our specific collection
                    
                # obj = bpy.context.active_object # our created cube is the active one
                # bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
                # bpy.data.collections['Paths' + ZonePrefix].objects.link(obj)# add it to our specific collection
                
                # #Der Collection kram muss hier anders sein, weil, was weiss ich leck mich
                # obj = bpy.context.view_layer.objects.active # Erstellte Obj is the active one
                # bpy.data.collections['Paths' + ZonePrefix].objects.link(obj)# add it to our specific collection
                    
                # new_obj = bpy.context.active_object  # Get a handle on new object
                # new_obj.users_collection[0].objects.unlink(new_obj)
                
                #NEEE GEHT AUCH NET DIESER DRECK.
                    
                    
                    
                ##FIX. DES GEHT. YEEEEEEEES
                col = bpy.data.collections['Paths' + ZonePrefix]
                obj = bpy.context.object
                #bpy.context.scene.collection.children.link(col)
                for other_col in obj.users_collection:
                    other_col.objects.unlink(obj)
                if obj.name not in col.objects:
                    col.objects.link(obj)
                
                break

        
        
    #Jetzt alles andere importieren:

    CSVimport_MiscLists() #GLE Listen
    
    #Common Layer
    LAYERname = "Common"
    CSVimport_DebugMoveInfo()#
    CSVimport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
    #CSVimport_List() #unused infos, pfeif drauf
    CSVimport_MapPartsInfo()#
    CSVimport_Placement_AreaObjInfo()#
    CSVimport_Placement_CameraCubeInfo()#
    #CSVimport_Placement_ChangeObjInfo() #unused
    CSVimport_Placement_DemoObjInfo()# #Cutscenen
    CSVimport_Placement_ObjInfo()# #Eigentliche Objekte
    CSVimport_Placement_PlanetObjInfo()# #Gravity
    CSVimport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
    CSVimport_StartInfo()#


    #Andere Zusatz Layers:
    if LayerA == True:
        LAYERname = "LayerA"
        CSVimport_DebugMoveInfo()#
        CSVimport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVimport_List() #unused infos, pfeif drauf
        CSVimport_MapPartsInfo()#
        CSVimport_Placement_AreaObjInfo()#
        CSVimport_Placement_CameraCubeInfo()#
        #CSVimport_Placement_ChangeObjInfo() #unused
        CSVimport_Placement_DemoObjInfo()# #Cutscenen
        CSVimport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVimport_Placement_PlanetObjInfo()# #Gravity
        CSVimport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVimport_StartInfo()#

        
    if LayerB == True:
        LAYERname = "LayerB"
        CSVimport_DebugMoveInfo()#
        CSVimport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVimport_List() #unused infos, pfeif drauf
        CSVimport_MapPartsInfo()#
        CSVimport_Placement_AreaObjInfo()#
        CSVimport_Placement_CameraCubeInfo()#
        #CSVimport_Placement_ChangeObjInfo() #unused
        CSVimport_Placement_DemoObjInfo()# #Cutscenen
        CSVimport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVimport_Placement_PlanetObjInfo()# #Gravity
        CSVimport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVimport_StartInfo()#
        
    if LayerC == True:
        LAYERname = "LayerC"
        CSVimport_DebugMoveInfo()#
        CSVimport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVimport_List() #unused infos, pfeif drauf
        CSVimport_MapPartsInfo()#
        CSVimport_Placement_AreaObjInfo()#
        CSVimport_Placement_CameraCubeInfo()#
        #CSVimport_Placement_ChangeObjInfo() #unused
        CSVimport_Placement_DemoObjInfo()# #Cutscenen
        CSVimport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVimport_Placement_PlanetObjInfo()# #Gravity
        CSVimport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVimport_StartInfo()#
            
    if LayerD == True:
        LAYERname = "LayerD"
        CSVimport_DebugMoveInfo()#
        CSVimport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVimport_List() #unused infos, pfeif drauf
        CSVimport_MapPartsInfo()#
        CSVimport_Placement_AreaObjInfo()#
        CSVimport_Placement_CameraCubeInfo()#
        #CSVimport_Placement_ChangeObjInfo() #unused
        CSVimport_Placement_DemoObjInfo()# #Cutscenen
        CSVimport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVimport_Placement_PlanetObjInfo()# #Gravity
        CSVimport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVimport_StartInfo()#
            
    if LayerE == True:
        LAYERname = "LayerE"
        CSVimport_DebugMoveInfo()#
        CSVimport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVimport_List() #unused infos, pfeif drauf
        CSVimport_MapPartsInfo()#
        CSVimport_Placement_AreaObjInfo()#
        CSVimport_Placement_CameraCubeInfo()#
        #CSVimport_Placement_ChangeObjInfo() #unused
        CSVimport_Placement_DemoObjInfo()# #Cutscenen
        CSVimport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVimport_Placement_PlanetObjInfo()# #Gravity
        CSVimport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVimport_StartInfo()#
            
    if LayerF == True:
        LAYERname = "LayerF"
        CSVimport_DebugMoveInfo()#
        CSVimport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVimport_List() #unused infos, pfeif drauf
        CSVimport_MapPartsInfo()#
        CSVimport_Placement_AreaObjInfo()#
        CSVimport_Placement_CameraCubeInfo()#
        #CSVimport_Placement_ChangeObjInfo() #unused
        CSVimport_Placement_DemoObjInfo()# #Cutscenen
        CSVimport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVimport_Placement_PlanetObjInfo()# #Gravity
        CSVimport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVimport_StartInfo()#
            
    if LayerG == True:
        LAYERname = "LayerG"
        CSVimport_DebugMoveInfo()#
        CSVimport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVimport_List() #unused infos, pfeif drauf
        CSVimport_MapPartsInfo()#
        CSVimport_Placement_AreaObjInfo()#
        CSVimport_Placement_CameraCubeInfo()#
        #CSVimport_Placement_ChangeObjInfo() #unused
        CSVimport_Placement_DemoObjInfo()# #Cutscenen
        CSVimport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVimport_Placement_PlanetObjInfo()# #Gravity
        CSVimport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVimport_StartInfo()#
            
    if LayerH == True:
        LAYERname = "LayerH"
        CSVimport_DebugMoveInfo()#
        CSVimport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVimport_List() #unused infos, pfeif drauf
        CSVimport_MapPartsInfo()#
        CSVimport_Placement_AreaObjInfo()#
        CSVimport_Placement_CameraCubeInfo()#
        #CSVimport_Placement_ChangeObjInfo() #unused
        CSVimport_Placement_DemoObjInfo()# #Cutscenen
        CSVimport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVimport_Placement_PlanetObjInfo()# #Gravity
        CSVimport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVimport_StartInfo()#
            
    if LayerI == True:
        LAYERname = "LayerI"
        CSVimport_DebugMoveInfo()#
        CSVimport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVimport_List() #unused infos, pfeif drauf
        CSVimport_MapPartsInfo()#
        CSVimport_Placement_AreaObjInfo()#
        CSVimport_Placement_CameraCubeInfo()#
        #CSVimport_Placement_ChangeObjInfo() #unused
        CSVimport_Placement_DemoObjInfo()# #Cutscenen
        CSVimport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVimport_Placement_PlanetObjInfo()# #Gravity
        CSVimport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVimport_StartInfo()#
            
    if LayerJ == True:
        LAYERname = "LayerJ"
        CSVimport_DebugMoveInfo()#
        CSVimport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVimport_List() #unused infos, pfeif drauf
        CSVimport_MapPartsInfo()#
        CSVimport_Placement_AreaObjInfo()#
        CSVimport_Placement_CameraCubeInfo()#
        #CSVimport_Placement_ChangeObjInfo() #unused
        CSVimport_Placement_DemoObjInfo()# #Cutscenen
        CSVimport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVimport_Placement_PlanetObjInfo()# #Gravity
        CSVimport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVimport_StartInfo()#
        
    if LayerK == True:
        LAYERname = "LayerK"
        CSVimport_DebugMoveInfo()#
        CSVimport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVimport_List() #unused infos, pfeif drauf
        CSVimport_MapPartsInfo()#
        CSVimport_Placement_AreaObjInfo()#
        CSVimport_Placement_CameraCubeInfo()#
        #CSVimport_Placement_ChangeObjInfo() #unused
        CSVimport_Placement_DemoObjInfo()# #Cutscenen
        CSVimport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVimport_Placement_PlanetObjInfo()# #Gravity
        CSVimport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVimport_StartInfo()#
            
    if LayerL == True:
        LAYERname = "LayerL"
        CSVimport_DebugMoveInfo()#
        CSVimport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVimport_List() #unused infos, pfeif drauf
        CSVimport_MapPartsInfo()#
        CSVimport_Placement_AreaObjInfo()#
        CSVimport_Placement_CameraCubeInfo()#
        #CSVimport_Placement_ChangeObjInfo() #unused
        CSVimport_Placement_DemoObjInfo()# #Cutscenen
        CSVimport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVimport_Placement_PlanetObjInfo()# #Gravity
        CSVimport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVimport_StartInfo()#
            
    if LayerM == True:
        LAYERname = "LayerM"
        CSVimport_DebugMoveInfo()#
        CSVimport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVimport_List() #unused infos, pfeif drauf
        CSVimport_MapPartsInfo()#
        CSVimport_Placement_AreaObjInfo()#
        CSVimport_Placement_CameraCubeInfo()#
        #CSVimport_Placement_ChangeObjInfo() #unused
        CSVimport_Placement_DemoObjInfo()# #Cutscenen
        CSVimport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVimport_Placement_PlanetObjInfo()# #Gravity
        CSVimport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVimport_StartInfo()#
            
    if LayerN == True:
        LAYERname = "LayerN"
        CSVimport_DebugMoveInfo()#
        CSVimport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVimport_List() #unused infos, pfeif drauf
        CSVimport_MapPartsInfo()#
        CSVimport_Placement_AreaObjInfo()#
        CSVimport_Placement_CameraCubeInfo()#
        #CSVimport_Placement_ChangeObjInfo() #unused
        CSVimport_Placement_DemoObjInfo()# #Cutscenen
        CSVimport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVimport_Placement_PlanetObjInfo()# #Gravity
        CSVimport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVimport_StartInfo()#
            
    if LayerO == True:
        LAYERname = "LayerO"
        CSVimport_DebugMoveInfo()#
        CSVimport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVimport_List() #unused infos, pfeif drauf
        CSVimport_MapPartsInfo()#
        CSVimport_Placement_AreaObjInfo()#
        CSVimport_Placement_CameraCubeInfo()#
        #CSVimport_Placement_ChangeObjInfo() #unused
        CSVimport_Placement_DemoObjInfo()# #Cutscenen
        CSVimport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVimport_Placement_PlanetObjInfo()# #Gravity
        CSVimport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVimport_StartInfo()#
            
    if LayerP == True:
        LAYERname = "LayerP"
        CSVimport_DebugMoveInfo()#
        CSVimport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVimport_List() #unused infos, pfeif drauf
        CSVimport_MapPartsInfo()#
        CSVimport_Placement_AreaObjInfo()#
        CSVimport_Placement_CameraCubeInfo()#
        #CSVimport_Placement_ChangeObjInfo() #unused
        CSVimport_Placement_DemoObjInfo()# #Cutscenen
        CSVimport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVimport_Placement_PlanetObjInfo()# #Gravity
        CSVimport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVimport_StartInfo()#
	
def Export(GalaxyMapName, ZoneID):

    import bpy
    import math
    import csv
    import sys
    import os
    import shutil
    import subprocess
    C = bpy.context
    import struct
    import requests



    # rarcpackPath="C:/SuperMarioGravity/Tools/Archive/Rarc Tools/rarcpack-casesensitive.exe"
    # yaz0encPath="C:/SuperMarioGravity/Tools/Archive/Rarc Tools/yaz0enc.exe"


    #os.popen(yaz0encPath + MapName + (".arc")

    ## Zonenprefix:
    
    
    ZonePrefix = "  (Z" + str(ZoneID) + ")"
    if ZoneID == 0:
        ZonePrefix = ""


    ###CSV OPERATIONEN

    ##CSV Headings:

    #GalaxyMapName = bpy.context.scene.name
    #MapName = "TestomatMap"
    MapName = GalaxyMapName + "Map"
    #LayerName = "Common"




    ### Alte Map Dateien loeschen, außer Kamerazeug ###
    try:
        shutil.rmtree(bpy.path.abspath('//05_MapExport/')+MapName+"/stage/jmp")
    except:
        print("Export Ordner existierte nicht. Also muss die Zone brandneu sein")




    ##################Check welche Layer die Map hat in Blender###########




    #Check LayerA
    LayerName = "LayerA"
    ObjectCounter = 0
    for obj in bpy.data.collections[GalaxyMapName].all_objects:
        try:
            if (obj["Layer"]) == LayerName:
                ObjectCounter = ObjectCounter + 1
        except:
            print("No")
    if ObjectCounter == 0:
        print(LayerName+" ist nicht da")
        LayerA = False
    else:
        print(LayerName+" ist da")
        LayerA = True



    #Check LayerB
    LayerName = "LayerB"
    ObjectCounter = 0
    for obj in bpy.data.collections[GalaxyMapName].all_objects:
        try:
            if (obj["Layer"]) == LayerName:
                ObjectCounter = ObjectCounter + 1
        except:
            print("No")
    if ObjectCounter == 0:
        print(LayerName+" ist nicht da")
        LayerB = False
    else:
        print(LayerName+" ist da")
        LayerB = True

    #Check LayerC
    LayerName = "LayerC"
    ObjectCounter = 0
    for obj in bpy.data.collections[GalaxyMapName].all_objects:
        try:
            if (obj["Layer"]) == LayerName:
                ObjectCounter = ObjectCounter + 1
        except:
            print("No")
    if ObjectCounter == 0:
        print(LayerName+" ist nicht da")
        LayerC = False
    else:
        print(LayerName+" ist da")
        LayerC = True

    #Check LayerD
    LayerName = "LayerD"
    ObjectCounter = 0
    for obj in bpy.data.collections[GalaxyMapName].all_objects:
        try:
            if (obj["Layer"]) == LayerName:
                ObjectCounter = ObjectCounter + 1
        except:
            print("No")
    if ObjectCounter == 0:
        print(LayerName+" ist nicht da")
        LayerD = False
    else:
        print(LayerName+" ist da")
        LayerD = True

    #Check LayerE
    LayerName = "LayerE"
    ObjectCounter = 0
    for obj in bpy.data.collections[GalaxyMapName].all_objects:
        try:
            if (obj["Layer"]) == LayerName:
                ObjectCounter = ObjectCounter + 1
        except:
            print("No")
    if ObjectCounter == 0:
        print(LayerName+" ist nicht da")
        LayerE = False
    else:
        print(LayerName+" ist da")
        LayerE = True

    #Check LayerF
    LayerName = "LayerF"
    ObjectCounter = 0
    for obj in bpy.data.collections[GalaxyMapName].all_objects:
        try:
            if (obj["Layer"]) == LayerName:
                ObjectCounter = ObjectCounter + 1
        except:
            print("No")
    if ObjectCounter == 0:
        print(LayerName+" ist nicht da")
        LayerF = False
    else:
        print(LayerName+" ist da")
        LayerF = True

    #Check LayerG
    LayerName = "LayerG"
    ObjectCounter = 0
    for obj in bpy.data.collections[GalaxyMapName].all_objects:
        try:
            if (obj["Layer"]) == LayerName:
                ObjectCounter = ObjectCounter + 1
        except:
            print("No")
    if ObjectCounter == 0:
        print(LayerName+" ist nicht da")
        LayerG = False
    else:
        print(LayerName+" ist da")
        LayerG = True

    #Check LayerH
    LayerName = "LayerH"
    ObjectCounter = 0
    for obj in bpy.data.collections[GalaxyMapName].all_objects:
        try:
            if (obj["Layer"]) == LayerName:
                ObjectCounter = ObjectCounter + 1
        except:
            print("No")
    if ObjectCounter == 0:
        print(LayerName+" ist nicht da")
        LayerH = False
    else:
        print(LayerName+" ist da")
        LayerH = True

    #Check LayerI
    LayerName = "LayerI"
    ObjectCounter = 0
    for obj in bpy.data.collections[GalaxyMapName].all_objects:
        try:
            if (obj["Layer"]) == LayerName:
                ObjectCounter = ObjectCounter + 1
        except:
            print("No")
    if ObjectCounter == 0:
        print(LayerName+" ist nicht da")
        LayerI = False
    else:
        print(LayerName+" ist da")
        LayerI = True

    #Check LayerJ
    LayerName = "LayerJ"
    ObjectCounter = 0
    for obj in bpy.data.collections[GalaxyMapName].all_objects:
        try:
            if (obj["Layer"]) == LayerName:
                ObjectCounter = ObjectCounter + 1
        except:
            print("No")
    if ObjectCounter == 0:
        print(LayerName+" ist nicht da")
        LayerJ = False
    else:
        print(LayerName+" ist da")
        LayerJ = True

    #Check LayerK
    LayerName = "LayerK"
    ObjectCounter = 0
    for obj in bpy.data.collections[GalaxyMapName].all_objects:
        try:
            if (obj["Layer"]) == LayerName:
                ObjectCounter = ObjectCounter + 1
        except:
            print("No")
    if ObjectCounter == 0:
        print(LayerName+" ist nicht da")
        LayerK = False
    else:
        print(LayerName+" ist da")
        LayerK = True

    #Check LayerL
    LayerName = "LayerL"
    ObjectCounter = 0
    for obj in bpy.data.collections[GalaxyMapName].all_objects:
        try:
            if (obj["Layer"]) == LayerName:
                ObjectCounter = ObjectCounter + 1
        except:
            print("No")
    if ObjectCounter == 0:
        print(LayerName+" ist nicht da")
        LayerL = False
    else:
        print(LayerName+" ist da")
        LayerL = True

    #Check LayerM
    LayerName = "LayerM"
    ObjectCounter = 0
    for obj in bpy.data.collections[GalaxyMapName].all_objects:
        try:
            if (obj["Layer"]) == LayerName:
                ObjectCounter = ObjectCounter + 1
        except:
            print("No")
    if ObjectCounter == 0:
        print(LayerName+" ist nicht da")
        LayerM = False
    else:
        print(LayerName+" ist da")
        LayerM = True

    #Check LayerN
    LayerName = "LayerN"
    ObjectCounter = 0
    for obj in bpy.data.collections[GalaxyMapName].all_objects:
        try:
            if (obj["Layer"]) == LayerName:
                ObjectCounter = ObjectCounter + 1
        except:
            print("No")
    if ObjectCounter == 0:
        print(LayerName+" ist nicht da")
        LayerN = False
    else:
        print(LayerName+" ist da")
        LayerN = True

    #Check LayerO
    LayerName = "LayerO"
    ObjectCounter = 0
    for obj in bpy.data.collections[GalaxyMapName].all_objects:
        try:
            if (obj["Layer"]) == LayerName:
                ObjectCounter = ObjectCounter + 1
        except:
            print("No")
    if ObjectCounter == 0:
        print(LayerName+" ist nicht da")
        LayerO = False
    else:
        print(LayerName+" ist da")
        LayerO = True

    #Check LayerP
    LayerName = "LayerP"
    ObjectCounter = 0
    for obj in bpy.data.collections[GalaxyMapName].all_objects:
        try:
            if (obj["Layer"]) == LayerName:
                ObjectCounter = ObjectCounter + 1
        except:
            print("No")
    #    finally:
    #        ""
    if ObjectCounter == 0:
        print(LayerName+" ist nicht da")
        LayerP = False
    else:
        print(LayerName+" ist da")
        LayerP = True




    ####################################  OBJEKTE EXPORTIEREN  ##########################################





    ############### DebugMoveInfo ##################

    def CSVexport_DebugMoveInfo():

        CSVheadings = "name:String:0,l_id:Int:0,pos_x:Float:0.0,pos_y:Float:0.0,pos_z:Float:0.0,dir_x:Float:0.0,dir_y:Float:0.0,dir_z:Float:0.0,scale_x:Float:0.0,scale_y:Float:0.0,scale_z:Float:0.0"



        os.popen(("mkdir ") + (bpy.path.abspath('//05_MapExport\\'))+MapName+str('\\stage\\jmp\\Debug\\')+LayerName+str('\\')).read() # Map Ordnerstruktur erstellen
        blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Debug\\'+LayerName+'\\DebugMoveInfo','w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)
        blenderCipher.write(CSVheadings) #Die Headings hinzufuegen



        active = bpy.context.view_layer.objects.active

        for obj in bpy.data.collections["Debug" + ZonePrefix].all_objects: #Jedes Objekt in csv umwandeln
            if (obj["Layer"]) == LayerName:

                name = get_base_object_name(obj.name)
                I_id = (obj["Link ID"])
                pos_x = (obj.location[0])
                pos_y = (obj.location[2])
                pos_z = (obj.location[1]) * -1
                dir_x = (obj.rotation_euler[0])
                dir_y = (obj.rotation_euler[2])
                dir_z = (obj.rotation_euler[1]) * -1
                scale_x = (obj.scale[0])
                scale_y = (obj.scale[2])
                scale_z = (obj.scale[1])
                
                dir_x = (math.degrees(dir_x)) #radians zu Grad (degree)
                dir_y = (math.degrees(dir_y))
                dir_z = (math.degrees(dir_z))
                
                #Baue CSV Code zusammen:
                OBJEKTCODE = str(name) + "," + str(I_id) + "," + str(pos_x) + "," + str(pos_y) + "," + str(pos_z) + "," + str(dir_x) + "," + str(dir_y) + "," + str(dir_z) + "," + str(scale_x) + "," + str(scale_y) + "," + str(scale_z)
                
                blenderCipher.write('\n'+OBJEKTCODE) #Schreibe Code in die CSV
                
                print(name) #Debug
                print(OBJEKTCODE) #Debug
            
        blenderCipher.close() #CSV Datei schliessen

        #Wandle CSV zu BCSV
        import subprocess
        os.popen(("pyjmap tojmap smg ") + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Debug\\'+LayerName+'\\DebugMoveInfo ') + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Debug\\'+LayerName+'\\DebugMoveInfo'))






    ############### GeneralPosInfo ##################

    def CSVexport_GeneralPosInfo():

        CSVheadings = "name:String:0,PosName:String:0,pos_x:Float:0.0,pos_y:Float:0.0,pos_z:Float:0.0,dir_x:Float:0.0,dir_y:Float:0.0,dir_z:Float:0.0,Obj_ID:Short:0"



        os.popen(("mkdir ") + (bpy.path.abspath('//05_MapExport\\'))+MapName+str('\\stage\\jmp\\GeneralPos\\')+LayerName+str('\\')).read() # Map Ordnerstruktur erstellen
        blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\GeneralPos\\'+LayerName+'\\GeneralPosInfo','w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)
        blenderCipher.write(CSVheadings) #Die Headings hinzufuegen



        active = bpy.context.view_layer.objects.active

        for obj in bpy.data.collections["Positions" + ZonePrefix].all_objects: #Jedes Objekt in csv umwandeln
            if (obj["Layer"]) == LayerName:

                name = get_base_object_name(obj.name)
                PosName = (obj["Position Name"])
                pos_x = (obj.location[0])
                pos_y = (obj.location[2])
                pos_z = (obj.location[1]) * -1
                dir_x = (obj.rotation_euler[0])
                dir_y = (obj.rotation_euler[2])
                dir_z = (obj.rotation_euler[1]) * -1
                #scale_x = (obj.scale[0])
                #scale_y = (obj.scale[2])
                #scale_z = (obj.scale[1])
                Obj_ID = (obj["Linked Object ID"])
                
                dir_x = (math.degrees(dir_x)) #radians zu Grad (degree)
                dir_y = (math.degrees(dir_y))
                dir_z = (math.degrees(dir_z))
                
                #Baue CSV Code zusammen:
                OBJEKTCODE = str(name) + "," + str(PosName) + "," + str(pos_x) + "," + str(pos_y) + "," + str(pos_z) + "," + str(dir_x) + "," + str(dir_y) + "," + str(dir_z) + "," + str(Obj_ID)
                
                blenderCipher.write('\n'+OBJEKTCODE) #Schreibe Code in die CSV
                
                print(name) #Debug
                print(OBJEKTCODE) #Debug
            
        blenderCipher.close() #CSV Datei schliessen

        #Wandle CSV zu BCSV
        import subprocess
        os.popen(("pyjmap tojmap smg ") + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\GeneralPos\\'+LayerName+'\\GeneralPosInfo ') + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\GeneralPos\\'+LayerName+'\\GeneralPosInfo'))








    ############### MapPartsInfo ##################

    def CSVexport_MapPartsInfo():

        CSVheadings = "name:String:0,l_id:Int:0,MoveConditionType:Int:0,RotateSpeed:Int:0,RotateAngle:Int:0,RotateAxis:Int:0,RotateAccelType:Int:0,RotateStopTime:Int:0,RotateType:Int:0,ShadowType:Int:0,SignMotionType:Int:0,PressType:Int:0,ParamScale:Float:0.0,CameraSetId:Int:0,FarClip:Int:0,Obj_arg0:Int:0,Obj_arg1:Int:0,Obj_arg2:Int:0,Obj_arg3:Int:0,SW_APPEAR:Int:0,SW_DEAD:Int:0,SW_A:Int:0,SW_B:Int:0,SW_AWAKE:Int:0,SW_PARAM:Int:0,pos_x:Float:0.0,pos_y:Float:0.0,pos_z:Float:0.0,dir_x:Float:0.0,dir_y:Float:0.0,dir_z:Float:0.0,scale_x:Float:0.0,scale_y:Float:0.0,scale_z:Float:0.0,CastId:Int:0,ViewGroupId:Int:0,ShapeModelNo:Short:0,CommonPath_ID:Short:0,ClippingGroupId:Short:0,GroupId:Short:0,DemoGroupId:Short:0,MapParts_ID:Short:0,Obj_ID:Short:0,ParentId:Short:0"



        os.popen(("mkdir ") + (bpy.path.abspath('//05_MapExport\\'))+MapName+str('\\stage\\jmp\\MapParts\\')+LayerName+str('\\')).read() # Map Ordnerstruktur erstellen
        blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\MapParts\\'+LayerName+'\\MapPartsInfo','w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)
        blenderCipher.write(CSVheadings) #Die Headings hinzufuegen



        active = bpy.context.view_layer.objects.active

        for obj in bpy.data.collections["MapParts" + ZonePrefix].all_objects: #Jedes Objekt in csv umwandeln
            if (obj["Layer"]) == LayerName:


                
                    #Checken, ob es Collection Instanz nutzt
                if obj.instance_collection == None:
                    print("Nutzt keine Collection Instanz")
                    name = get_base_object_name(obj.name) #Nehme also Namen des Objekts     
                else:
                    print("Nutzt Collection Instanz")
                    name = (obj.instance_collection.name) #Nehme Namen der Collection als Objektnamen
                
                I_id = (obj["Link ID"])
                MoveConditionType = (obj["MoveConditionType"])
                RotateSpeed = (obj["RotateSpeed"])
                RotateAngle = (obj["RotateAngle"])
                RotateAxis = (obj["RotateAxis"])               
                RotateAccelType = (obj["RotateAccelType"])               
                RotateStopTime = (obj["RotateStopTime"])                
                RotateType = (obj["RotateType"])  
                ShadowType = (obj["ShadowType"])  
                SignMotionType = (obj["SignMotionType"])  
                PressType = (obj["PressType"])  
                ParamScale = (obj["Speed Scale"]) 
                CameraSetId = (obj["Camera Set ID"])
                FarClip = (obj["Far Clip"])            
                Obj_arg0 = (obj["Obj_Arg0"])
                Obj_arg1 = (obj["Obj_Arg1"])
                Obj_arg2 = (obj["Obj_Arg2"])
                Obj_arg3 = (obj["Obj_Arg3"])

                SW_APPEAR = (obj["SW_APPEAR"])
                SW_DEAD = (obj["SW_DEAD"])
                SW_A = (obj["SW_A"])
                SW_B = (obj["SW_B"])
                SW_AWAKE = (obj["SW_AWAKE"])
                SW_PARAM = (obj["SW_PARAM"])

                pos_x = (obj.location[0])
                pos_y = (obj.location[2])
                pos_z = (obj.location[1]) * -1
                dir_x = (obj.rotation_euler[0])
                dir_y = (obj.rotation_euler[2])
                dir_z = (obj.rotation_euler[1]) * -1
                scale_x = (obj.scale[0])
                scale_y = (obj.scale[2])
                scale_z = (obj.scale[1])
                
                CastId = (obj["Cast Group ID"])
                ViewGroupId = (obj["View Group ID"])
                ShapeModelNo = (obj["Model ID"])
                CommonPath_ID = (obj["Path ID"])
                ClippingGroupId = (obj["Clipping Group ID"])
                GroupId = (obj["Group ID"])
                DemoGroupId = (obj["Cutscene Group ID"])
                MapParts_ID = (obj["Linked MapParts ID"])
                Obj_ID = (obj["Linked Object ID"])
                ParentId = (obj["Parent Object ID"])    

                
                dir_x = (math.degrees(dir_x)) #radians zu Grad (degree)
                dir_y = (math.degrees(dir_y))
                dir_z = (math.degrees(dir_z))
                
                
                #Baue CSV Code zusammen:
                OBJEKTCODE = str(name) + "," + str(I_id) + "," + str(MoveConditionType) + "," + str(RotateSpeed) + "," + str(RotateAngle) + "," + str(RotateAxis) + "," + str(RotateAccelType) + "," + str(RotateStopTime) + "," + str(RotateType) + "," + str(ShadowType) + "," + str(SignMotionType) + "," + str(PressType) + "," + str(ParamScale) + "," + str(CameraSetId) + "," + str(FarClip) + "," + str(Obj_arg0) + "," + str(Obj_arg1) + "," + str(Obj_arg2) + "," + str(Obj_arg3) + "," + str(SW_APPEAR) + "," + str(SW_DEAD) + "," + str(SW_A) + "," + str(SW_B) + "," + str(SW_AWAKE) + "," + str(SW_PARAM) + "," + str(pos_x) + "," + str(pos_y) + "," + str(pos_z) + "," + str(dir_x) + "," + str(dir_y) + "," + str(dir_z) + "," + str(scale_x) + "," + str(scale_y) + "," + str(scale_z) + "," + str(CastId) + "," + str(ViewGroupId) + "," + str(ShapeModelNo) + "," + str(CommonPath_ID) + "," + str(ClippingGroupId) + "," + str(GroupId) + "," + str(DemoGroupId) + "," + str(MapParts_ID) + "," + str(Obj_ID) + "," + str(ParentId)
                
                blenderCipher.write('\n'+OBJEKTCODE) #Schreibe Code in die CSV
                
                print(name) #Debug
                print(OBJEKTCODE) #Debug
            
        blenderCipher.close() #CSV Datei schliessen

        #Wandle CSV zu BCSV
        import subprocess
        os.popen(("pyjmap tojmap smg ") + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\MapParts\\'+LayerName+'\\MapPartsInfo ') + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\MapParts\\'+LayerName+'\\MapPartsInfo'))






    ############### AreaObjInfo ##################

    def CSVexport_Placement_AreaObjInfo():

        CSVheadings = "name:String:0,l_id:Int:0,Obj_arg0:Int:0,Obj_arg1:Int:0,Obj_arg2:Int:0,Obj_arg3:Int:0,Obj_arg4:Int:0,Obj_arg5:Int:0,Obj_arg6:Int:0,Obj_arg7:Int:0,Priority:Int:0,SW_APPEAR:Int:0,SW_A:Int:0,SW_B:Int:0,SW_AWAKE:Int:0,pos_x:Float:0.0,pos_y:Float:0.0,pos_z:Float:0.0,dir_x:Float:0.0,dir_y:Float:0.0,dir_z:Float:0.0,scale_x:Float:0.0,scale_y:Float:0.0,scale_z:Float:0.0,FollowId:Int:0,AreaShapeNo:Short:0,CommonPath_ID:Short:0,ClippingGroupId:Short:0,GroupId:Short:0,DemoGroupId:Short:0,MapParts_ID:Short:0,Obj_ID:Short:0"



        os.popen(("mkdir ") + (bpy.path.abspath('//05_MapExport\\'))+MapName+str('\\stage\\jmp\\Placement\\')+LayerName+str('\\')).read() # Map Ordnerstruktur erstellen
        blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Placement\\'+LayerName+'\\AreaObjInfo','w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)
        blenderCipher.write(CSVheadings) #Die Headings hinzufuegen



        active = bpy.context.view_layer.objects.active

        for obj in bpy.data.collections["Areas" + ZonePrefix].all_objects: #Jedes Objekt in csv umwandeln
            if (obj["Layer"]) == LayerName:

                name = get_base_object_name(obj.name)
                I_id = (obj["Link ID"])
                Obj_arg0 = (obj["Obj_Arg0"])
                Obj_arg1 = (obj["Obj_Arg1"])
                Obj_arg2 = (obj["Obj_Arg2"])
                Obj_arg3 = (obj["Obj_Arg3"])
                Obj_arg4 = (obj["Obj_Arg4"])
                Obj_arg5 = (obj["Obj_Arg5"])
                Obj_arg6 = (obj["Obj_Arg6"])
                Obj_arg7 = (obj["Obj_Arg7"])
                Priority = (obj["Priority"])
                SW_APPEAR = (obj["SW_APPEAR"])
                SW_A = (obj["SW_A"])
                SW_B = (obj["SW_B"])
                SW_AWAKE = (obj["SW_AWAKE"])
                
                pos_x = (obj.location[0])
                pos_y = (obj.location[2])
                pos_z = (obj.location[1]) * -1
                dir_x = (obj.rotation_euler[0])
                dir_y = (obj.rotation_euler[2])
                dir_z = (obj.rotation_euler[1]) * -1
                scale_x = (obj.scale[0])
                scale_y = (obj.scale[2])
                scale_z = (obj.scale[1])
                
                dir_x = (math.degrees(dir_x)) #radians zu Grad (degree)
                dir_y = (math.degrees(dir_y))
                dir_z = (math.degrees(dir_z))
                
                FollowId = (obj["Linked Area ID"])
                

                try:
                    if obj.instance_collection.name == "AreaShape 0  Cube":
                        AreaShapeNo = "0"
                        
                    if obj.instance_collection.name == "AreaShape 1  Cube Middle":
                        AreaShapeNo = "1"
                        
                    if obj.instance_collection.name == "AreaShape 2  Sphere":
                        AreaShapeNo = "2"
                        
                    if obj.instance_collection.name == "AreaShape 3  Cylinder":
                        AreaShapeNo = "3"
                        
                    if obj.instance_collection.name == "AreaShape 4  Half Sphere":
                        AreaShapeNo = "4"
                        
                except: 
                    
                    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                    print("fehlerhaftes Areal")
                    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

                    AreaShapeNo = "0"
                
                    
                
                CommonPath_ID = (obj["Path ID"])
                ClippingGroupId = (obj["Clipping Group ID"])
                GroupId = (obj["Group ID"])
                DemoGroupId = (obj["Cutscene Group ID"])
                MapParts_ID = (obj["Linked MapParts ID"])
                Obj_ID = (obj["Linked Object ID"])  
                
                #Baue CSV Code zusammen:
                OBJEKTCODE = str(name) + "," + str(I_id) + "," + str(Obj_arg0) + "," + str(Obj_arg1) + "," + str(Obj_arg2) + "," + str(Obj_arg3) + "," + str(Obj_arg4) + "," + str(Obj_arg5) + "," + str(Obj_arg6) + "," + str(Obj_arg7) + "," + str(Priority) + "," + str(SW_APPEAR) + "," + str(SW_A) + "," + str(SW_B) + "," + str(SW_AWAKE) + "," + str(pos_x) + "," + str(pos_y) + "," + str(pos_z) + "," + str(dir_x) + "," + str(dir_y) + "," + str(dir_z) + "," + str(scale_x) + "," + str(scale_y) + "," + str(scale_z) + "," + str(FollowId) + "," + str(AreaShapeNo) + "," + str(CommonPath_ID) + "," + str(ClippingGroupId) + "," + str(GroupId) + "," + str(DemoGroupId) + "," + str(MapParts_ID) + "," + str(Obj_ID)
                
                blenderCipher.write('\n'+OBJEKTCODE) #Schreibe Code in die CSV
                
                print(name) #Debug
                print(OBJEKTCODE) #Debug
            
        blenderCipher.close() #CSV Datei schliessen

        #Wandle CSV zu BCSV
        import subprocess
        os.popen(("pyjmap tojmap smg ") + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Placement\\'+LayerName+'\\AreaObjInfo ') + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Placement\\'+LayerName+'\\AreaObjInfo'))









    ############### CameraObjInfo ##################

    def CSVexport_Placement_CameraCubeInfo():

        CSVheadings = "name:String:0,l_id:Int:0,Obj_arg0:Int:0,Obj_arg1:Int:0,Obj_arg2:Int:0,Obj_arg3:Int:0,InterpolateIn:Int:0,InterpolateOut:Int:0,SW_APPEAR:Int:0,SW_A:Int:0,SW_B:Int:0,SW_AWAKE:Int:0,Validity:String:0,pos_x:Float:0.0,pos_y:Float:0.0,pos_z:Float:0.0,dir_x:Float:0.0,dir_y:Float:0.0,dir_z:Float:0.0,scale_x:Float:0.0,scale_y:Float:0.0,scale_z:Float:0.0,FollowId:Int:0,AreaShapeNo:Short:0,MapParts_ID:Short:0,Obj_ID:Short:0"



        os.popen(("mkdir ") + (bpy.path.abspath('//05_MapExport\\'))+MapName+str('\\stage\\jmp\\Placement\\')+LayerName+str('\\')).read() # Map Ordnerstruktur erstellen
        blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Placement\\'+LayerName+'\\CameraCubeInfo','w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)
        blenderCipher.write(CSVheadings) #Die Headings hinzufuegen



        active = bpy.context.view_layer.objects.active

        for obj in bpy.data.collections["Cameras" + ZonePrefix].all_objects: #Jedes Objekt in csv umwandeln
            if (obj["Layer"]) == LayerName:

                name = "CameraArea"
                I_id = (obj["Link ID"])
                Obj_arg0 = (obj["Camera ID"])
                Obj_arg1 = (obj["Obj_Arg1"])
                Obj_arg2 = (obj["Priority"])
                Obj_arg3 = (obj["Affected Contexts"])
                InterpolateIn = (obj["Interpolate In (Unused)"])
                InterpolateOut = (obj["Interpolate Out (Unused)"])
                SW_APPEAR = (obj["SW_APPEAR"])
                SW_A = (obj["SW_A"])
                SW_B = (obj["SW_B"])
                SW_AWAKE = (obj["SW_AWAKE"])
                Validity = (obj["Validity"])

                pos_x = (obj.location[0])
                pos_y = (obj.location[2])
                pos_z = (obj.location[1]) * -1
                dir_x = (obj.rotation_euler[0])
                dir_y = (obj.rotation_euler[2])
                dir_z = (obj.rotation_euler[1]) * -1
                scale_x = (obj.scale[0])
                scale_y = (obj.scale[2])
                scale_z = (obj.scale[1])
                
                dir_x = (math.degrees(dir_x)) #radians zu Grad (degree)
                dir_y = (math.degrees(dir_y))
                dir_z = (math.degrees(dir_z))
                
                FollowId = (obj["Linked Area ID"])
                
                try:
                    if obj.instance_collection.name == "AreaShape 0  Cube":
                        AreaShapeNo = "0"
                        
                    if obj.instance_collection.name == "AreaShape 1  Cube Middle":
                        AreaShapeNo = "1"
                        
                    if obj.instance_collection.name == "AreaShape 2  Sphere":
                        AreaShapeNo = "2"
                        
                    if obj.instance_collection.name == "AreaShape 3  Cylinder":
                        AreaShapeNo = "3"
                        
                    if obj.instance_collection.name == "AreaShape 4  Half Sphere":
                        AreaShapeNo = "4"
                        
                except: 
                    
                    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                    print("fehlerhaftes Areal")
                    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

                    AreaShapeNo = "0"
                    
                    
                MapParts_ID = (obj["Linked MapParts ID"])
                Obj_ID = (obj["Linked Object ID"])  
                
                #Baue CSV Code zusammen:
                OBJEKTCODE = str(name) + "," + str(I_id) + "," + str(Obj_arg0) + "," + str(Obj_arg1) + "," + str(Obj_arg2) + "," + str(Obj_arg3) + "," + str(InterpolateIn) + "," + str(InterpolateOut) + "," + str(SW_APPEAR) + "," + str(SW_A) + "," + str(SW_B) + "," + str(SW_AWAKE) + "," + str(Validity) + "," + str(pos_x) + "," + str(pos_y) + "," + str(pos_z) + "," + str(dir_x) + "," + str(dir_y) + "," + str(dir_z) + "," + str(scale_x) + "," + str(scale_y) + "," + str(scale_z) + "," + str(FollowId) + "," + str(AreaShapeNo) + "," + str(MapParts_ID) + "," + str(Obj_ID)
                
                blenderCipher.write('\n'+OBJEKTCODE) #Schreibe Code in die CSV
                
                print(name) #Debug
                print(OBJEKTCODE) #Debug
            
        blenderCipher.close() #CSV Datei schliessen

        #Wandle CSV zu BCSV
        import subprocess
        os.popen(("pyjmap tojmap smg ") + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Placement\\'+LayerName+'\\CameraCubeInfo ') + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Placement\\'+LayerName+'\\CameraCubeInfo'))






    ############### DemoObjInfo ##################

    def CSVexport_Placement_DemoObjInfo():

        CSVheadings = "name:String:0,DemoName:String:0,TimeSheetName:String:0,l_id:Int:0,SW_APPEAR:Int:0,SW_DEAD:Int:0,SW_A:Int:0,SW_B:Int:0,DemoSkip:Int:0,pos_x:Float:0.0,pos_y:Float:0.0,pos_z:Float:0.0,dir_x:Float:0.0,dir_y:Float:0.0,dir_z:Float:0.0,scale_x:Float:0.0,scale_y:Float:0.0,scale_z:Float:0.0"



        os.popen(("mkdir ") + (bpy.path.abspath('//05_MapExport\\'))+MapName+str('\\stage\\jmp\\Placement\\')+LayerName+str('\\')).read() # Map Ordnerstruktur erstellen
        blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Placement\\'+LayerName+'\\DemoObjInfo','w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)
        blenderCipher.write(CSVheadings) #Die Headings hinzufuegen



        active = bpy.context.view_layer.objects.active

        for obj in bpy.data.collections["Cutscenes" + ZonePrefix].all_objects: #Jedes Objekt in csv umwandeln
            if (obj["Layer"]) == LayerName:

                name = get_base_object_name(obj.name)
                DemoName = (obj["Cutscene Name"])
                TimeSheetName = (obj["Sheet Name"])
                I_id = (obj["Link ID"])
                SW_APPEAR = (obj["SW_APPEAR"])
                SW_DEAD = (obj["SW_DEAD"])
                SW_A = (obj["SW_A"])
                SW_B = (obj["SW_B"])
                DemoSkip = (obj["Skippable"])
                
                pos_x = (obj.location[0])
                pos_y = (obj.location[2])
                pos_z = (obj.location[1]) * -1
                dir_x = (obj.rotation_euler[0])
                dir_y = (obj.rotation_euler[2])
                dir_z = (obj.rotation_euler[1]) * -1
                scale_x = (obj.scale[0])
                scale_y = (obj.scale[2])
                scale_z = (obj.scale[1])
                
                dir_x = (math.degrees(dir_x)) #radians zu Grad (degree)
                dir_y = (math.degrees(dir_y))
                dir_z = (math.degrees(dir_z))
                
                
                #Baue CSV Code zusammen:
                OBJEKTCODE = str(name) + "," + str(DemoName) + "," + str(TimeSheetName) + "," + str(I_id) + "," + str(SW_APPEAR) + "," + str(SW_DEAD) + "," + str(SW_A) + "," + str(SW_B) + "," + str(DemoSkip) + "," + str(pos_x) + "," + str(pos_y) + "," + str(pos_z) + "," + str(dir_x) + "," + str(dir_y) + "," + str(dir_z) + "," + str(scale_x) + "," + str(scale_y) + "," + str(scale_z)
                
                blenderCipher.write('\n'+OBJEKTCODE) #Schreibe Code in die CSV
                
                print(name) #Debug
                print(OBJEKTCODE) #Debug
            
        blenderCipher.close() #CSV Datei schliessen

        #Wandle CSV zu BCSV
        import subprocess
        os.popen(("pyjmap tojmap smg ") + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Placement\\'+LayerName+'\\DemoObjInfo ') + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Placement\\'+LayerName+'\\DemoObjInfo'))













    ############### OBJINFO ##################

    def CSVexport_Placement_ObjInfo():

        CSVheadings = "name:String:0,l_id:Int:0,Obj_arg0:Int:0,Obj_arg1:Int:0,Obj_arg2:Int:0,Obj_arg3:Int:0,Obj_arg4:Int:0,Obj_arg5:Int:0,Obj_arg6:Int:0,Obj_arg7:Int:0,CameraSetId:Int:0,SW_APPEAR:Int:0,SW_DEAD:Int:0,SW_A:Int:0,SW_B:Int:0,SW_AWAKE:Int:0,SW_PARAM:Int:0,MessageId:Int:0,ParamScale:Float:0.0,pos_x:Float:0.0,pos_y:Float:0.0,pos_z:Float:0.0,dir_x:Float:0.0,dir_y:Float:0.0,dir_z:Float:0.0,scale_x:Float:0.0,scale_y:Float:0.0,scale_z:Float:0.0,CastId:Int:0,ViewGroupId:Int:0,ShapeModelNo:Short:0,CommonPath_ID:Short:0,ClippingGroupId:Short:0,GroupId:Short:0,DemoGroupId:Short:0,MapParts_ID:Short:0,Obj_ID:Short:0,GeneratorID:Short:0"


        os.popen(("mkdir ") + (bpy.path.abspath('//05_MapExport\\'))+MapName+str('\\stage\\jmp\\Placement\\')+LayerName+str('\\')).read() # Map Ordnerstruktur erstellen
        blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Placement\\'+LayerName+'\\ObjInfo','w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)
        blenderCipher.write(CSVheadings) #Die Headings hinzufuegen



        active = bpy.context.view_layer.objects.active

        for obj in bpy.data.collections["Objects" + ZonePrefix].all_objects: #Jedes Objekt in csv umwandeln
            if "Layer" in obj:
                if (obj["Layer"]) == LayerName:
                        
                    #Checken, ob es Collection Instanz nutzt
                    if obj.instance_collection == None:
                        print("Nutzt keine Collection Instanz")
                        name = get_base_object_name(obj.name)     
                    else:
                        print("Nutzt Collection Instanz")
                        name = (obj.instance_collection.name) #Nehme Namen der Collection als Objektnamen

                    
                    
                    
                    
                    I_id = (obj["Link ID"])
                    obj_arg0 = (obj["Obj_Arg0"])
                    obj_arg1 = (obj["Obj_Arg1"])
                    obj_arg2 = (obj["Obj_Arg2"])
                    obj_arg3 = (obj["Obj_Arg3"])
                    obj_arg4 = (obj["Obj_Arg4"])
                    obj_arg5 = (obj["Obj_Arg5"])
                    obj_arg6 = (obj["Obj_Arg6"])
                    obj_arg7 = (obj["Obj_Arg7"])
                    CameraSetId = (obj["Camera Set ID"])
                    SW_APPEAR = (obj["SW_APPEAR"])
                    SW_DEAD = (obj["SW_DEAD"])
                    SW_A = (obj["SW_A"])
                    SW_B = (obj["SW_B"])
                    SW_AWAKE = (obj["SW_AWAKE"])
                    SW_PARAM = (obj["SW_PARAM"])
                    MessageId = (obj["Message ID"])
                    ParamScale = (obj["Speed Scale"])
                    
                    pos_x = (obj.location[0])
                    pos_y = (obj.location[2])
                    pos_z = (obj.location[1]) * -1
                    dir_x = (obj.rotation_euler[0])
                    dir_y = (obj.rotation_euler[2])
                    dir_z = (obj.rotation_euler[1]) * -1
                    scale_x = (obj.scale[0])
                    scale_y = (obj.scale[2])
                    scale_z = (obj.scale[1])
                    
                    dir_x = (math.degrees(dir_x)) #radians zu Grad (degree)
                    dir_y = (math.degrees(dir_y))
                    dir_z = (math.degrees(dir_z))
                    
                    CastId = (obj["Cast Group ID"])
                    ViewGroupId = (obj["View Group ID"])
                    ShapeModelNo = (obj["Model ID"])
                    CommonPath_ID = (obj["Path ID"])
                    ClippingGroupId = (obj["Clipping Group ID"])
                    GroupId = (obj["Group ID"])
                    DemoGroupId = (obj["Cutscene Group ID"])
                    MapParts_ID = (obj["Linked MapParts ID"])
                    Obj_ID = (obj["Linked Object ID"])
                    GeneratorID = (obj["Generator Object ID"])
                    
                    
                    
                    #Baue CSV Code zusammen:
                    OBJEKTCODE = str(name) + "," + str(I_id) + "," + str(obj_arg0) + "," + str(obj_arg1) + "," + str(obj_arg2) + "," + str(obj_arg3) + "," + str(obj_arg4) + "," + str(obj_arg5) + "," + str(obj_arg6) + "," + str(obj_arg7) + "," + str(CameraSetId) + "," + str(SW_APPEAR) + "," + str(SW_DEAD) + "," + str(SW_A) + "," + str(SW_B) + "," + str(SW_AWAKE) + "," + str(SW_PARAM) + "," + str(MessageId) + "," + str(ParamScale) + "," + str(pos_x) + "," + str(pos_y) + "," + str(pos_z) + "," + str(dir_x) + "," + str(dir_y) + "," + str(dir_z) + "," + str(scale_x) + "," + str(scale_y) + "," + str(scale_z) + "," + str(CastId) + "," + str(ViewGroupId) + "," + str(ShapeModelNo) + "," + str(CommonPath_ID) + "," + str(ClippingGroupId) + "," + str(GroupId) + "," + str(DemoGroupId) + "," + str(MapParts_ID) + "," + str(Obj_ID) + "," + str(GeneratorID)
                    
                    blenderCipher.write('\n'+OBJEKTCODE) #Schreibe Code in die CSV
                    
                    print(name) #Debug
                    print(OBJEKTCODE) #Debug
                
            
            
            
        blenderCipher.close() #CSV Datei schliessen

        #Wandle CSV zu BCSV
        import subprocess
        os.popen(("pyjmap tojmap smg ") + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Placement\\'+LayerName+'\\ObjInfo ') + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Placement\\'+LayerName+'\\ObjInfo'))







    ############### Gravity ##################

    def CSVexport_Placement_PlanetObjInfo():

        CSVheadings = "name:String:0,l_id:Int:0,Obj_arg0:Int:0,Obj_arg1:Int:0,Obj_arg2:Int:0,Obj_arg3:Int:0,Range:Float:0.0,Distant:Float:0.0,Priority:Int:0,Inverse:Int:0,Power:String:0,Gravity_type:String:0,SW_APPEAR:Int:0,SW_DEAD:Int:0,SW_A:Int:0,SW_B:Int:0,SW_AWAKE:Int:0,pos_x:Float:0.0,pos_y:Float:0.0,pos_z:Float:0.0,dir_x:Float:0.0,dir_y:Float:0.0,dir_z:Float:0.0,scale_x:Float:0.0,scale_y:Float:0.0,scale_z:Float:0.0,FollowId:Int:0,CommonPath_ID:Short:0,ClippingGroupId:Short:0,GroupId:Short:0,DemoGroupId:Short:0,MapParts_ID:Short:0,Obj_ID:Short:0"



        os.popen(("mkdir ") + (bpy.path.abspath('//05_MapExport\\'))+MapName+str('\\stage\\jmp\\Placement\\')+LayerName+str('\\')).read() # Map Ordnerstruktur erstellen
        blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Placement\\'+LayerName+'\\PlanetObjInfo','w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)
        blenderCipher.write(CSVheadings) #Die Headings hinzufuegen



        active = bpy.context.view_layer.objects.active

        for obj in bpy.data.collections["Gravities" + ZonePrefix].all_objects: #Jedes Objekt in csv umwandeln
            if (obj["Layer"]) == LayerName:

                name = obj.modifiers["GRAVITY"].node_group.name
                if obj.modifiers["GRAVITY"].node_group.name == "GlobalPlaneGravity":
                    
                    #Sphere
                    if obj.modifiers["GRAVITY"]["Input_10"] == 0:
                        if obj.modifiers["GRAVITY"]["Input_11"] == 0:
                            name = "GlobalPlaneGravity"
                        else:
                            name = "ZeroGravitySphere"
                    #Cube
                    if obj.modifiers["GRAVITY"]["Input_10"] == 1:
                        if obj.modifiers["GRAVITY"]["Input_11"] == 0:
                            name = "GlobalPlaneGravityInBox"
                        else:
                            name = "ZeroGravityBox"
                    #Cylinder
                    if obj.modifiers["GRAVITY"]["Input_10"] == 2:
                        if obj.modifiers["GRAVITY"]["Input_11"] == 0:
                            name = "GlobalPlaneGravityInCylinder"
                        else:
                            name = "ZeroGravityCylinder"
                
                
                
                
                I_id = (obj["Link ID"])
                Obj_arg0 = obj.modifiers["GRAVITY"]["Input_4"]
                Obj_arg1 = obj.modifiers["GRAVITY"]["Input_5"]
                Obj_arg2 = obj.modifiers["GRAVITY"]["Input_6"]
                Obj_arg3 = obj.modifiers["GRAVITY"]["Input_7"]
                Range = obj.modifiers["GRAVITY"]["Input_2"]
                Distant = obj.modifiers["GRAVITY"]["Input_3"]
                Priority = (obj["Priority"])
                Inverse = (obj["Inverse"])
                Power = (obj["Power"])
                Gravity_type = (obj["Gravity_type"])
                SW_APPEAR = (obj["SW_APPEAR"])
                SW_DEAD = (obj["SW_DEAD"])
                SW_A = (obj["SW_A"])
                SW_B = (obj["SW_B"])
                SW_AWAKE = (obj["SW_AWAKE"])
                
                pos_x = (obj.location[0])
                pos_y = (obj.location[2])
                pos_z = (obj.location[1]) * -1
                dir_x = (obj.rotation_euler[0])
                dir_y = (obj.rotation_euler[2])
                dir_z = (obj.rotation_euler[1]) * -1
                scale_x = obj.modifiers["GRAVITY"]["Input_8"][0]
                scale_y = obj.modifiers["GRAVITY"]["Input_8"][2]
                scale_z = obj.modifiers["GRAVITY"]["Input_8"][1]
                
                FollowId = (obj["Linked Area ID"])
                
                ### PATH:
                #CommonPath_ID = (obj["Path ID"])
                try:
                    GNodePathObjName = str(obj.modifiers["GRAVITY"]["Input_9"].name) #Den Objektnamen im GeometryNode rauskriegen
                    CommonPath_ID = bpy.data.objects[GNodePathObjName].data.name #Kriege Curve Data Namen (nicht objektnamen)
                    CommonPath_ID = CommonPath_ID.replace(ZonePrefix, '') #Prefix entfernen
                except:
                    CommonPath_ID = int(-1) #Falls es leer ist oder die Curvedatanamen keine Zahl ist, nehme einfach -1
                ######
                
                ClippingGroupId = (obj["Clipping Group ID"])
                GroupId = (obj["Group ID"])
                DemoGroupId = (obj["Cutscene Group ID"])
                MapParts_ID = (obj["Linked MapParts ID"])
                Obj_ID = (obj["Linked Object ID"])   
                
                
                dir_x = (math.degrees(dir_x)) #radians zu Grad (degree)
                dir_y = (math.degrees(dir_y))
                dir_z = (math.degrees(dir_z))
                
                
                #Baue CSV Code zusammen:
                OBJEKTCODE = str(name) + "," + str(I_id) + "," + str(Obj_arg0) + "," + str(Obj_arg1) + "," + str(Obj_arg2) + "," + str(Obj_arg3) + "," + str(Range) + "," + str(Distant) + "," + str(Priority) + "," + str(Inverse) + "," + str(Power) + "," + str(Gravity_type) + "," + str(SW_APPEAR) + "," + str(SW_DEAD) + "," + str(SW_A) + "," + str(SW_B) + "," + str(SW_AWAKE) + "," + str(pos_x) + "," + str(pos_y) + "," + str(pos_z) + "," + str(dir_x) + "," + str(dir_y) + "," + str(dir_z) + "," + str(scale_x) + "," + str(scale_y) + "," + str(scale_z) + "," + str(FollowId) + "," + str(CommonPath_ID) + "," + str(ClippingGroupId) + "," + str(GroupId) + "," + str(DemoGroupId) + "," + str(MapParts_ID) + "," + str(Obj_ID)
                
                blenderCipher.write('\n'+OBJEKTCODE) #Schreibe Code in die CSV
                
                print(name) #Debug
                print(OBJEKTCODE) #Debug
            
        blenderCipher.close() #CSV Datei schliessen

        #Wandle CSV zu BCSV
        import subprocess
        os.popen(("pyjmap tojmap smg ") + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Placement\\'+LayerName+'\\PlanetObjInfo ') + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Placement\\'+LayerName+'\\PlanetObjInfo'))





    ############### Zonen Positionen ##################

    def CSVexport_Placement_StageObjInfo():

        CSVheadings = "name:String:0,l_id:Int:0,pos_x:Float:0.0,pos_y:Float:0.0,pos_z:Float:0.0,dir_x:Float:0.0,dir_y:Float:0.0,dir_z:Float:0.0"



        os.popen(("mkdir ") + (bpy.path.abspath('//05_MapExport\\'))+MapName+str('\\stage\\jmp\\Placement\\')+LayerName+str('\\')).read() # Map Ordnerstruktur erstellen
        blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Placement\\'+LayerName+'\\StageObjInfo','w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)
        blenderCipher.write(CSVheadings) #Die Headings hinzufuegen



        active = bpy.context.view_layer.objects.active

        for obj in bpy.data.collections["ZonePositions" + ZonePrefix].all_objects: #Jedes Objekt in csv umwandeln
            if (obj["Layer"]) == LayerName:


                if obj.instance_type == 'COLLECTION':#Checken, ob das Objekt ne Collection Instanz nutzt
                    print("Nutzt Collection Instanz")
                    try:
                        name = (obj.instance_collection.name) #Nehme Namen der Collection als Objektnamen
                    except:
                        name = (obj.name)
                else:
                    print("Nutzt KEINE Collection Instanz")
                    name = (obj.name)
                I_id = (obj["Link ID"])
                
                pos_x = (obj.location[0])
                pos_y = (obj.location[2])
                pos_z = (obj.location[1]) * -1
                dir_x = (obj.rotation_euler[0])
                dir_y = (obj.rotation_euler[2])
                dir_z = (obj.rotation_euler[1]) * -1
                #scale_x = (obj.scale[0])
                #scale_y = (obj.scale[2])
                #scale_z = (obj.scale[1])
                
                dir_x = (math.degrees(dir_x)) #radians zu Grad (degree)
                dir_y = (math.degrees(dir_y))
                dir_z = (math.degrees(dir_z))
                
                #Baue CSV Code zusammen:
                OBJEKTCODE = str(name) + "," + str(I_id) + "," + str(pos_x) + "," + str(pos_y) + "," + str(pos_z) + "," + str(dir_x) + "," + str(dir_y) + "," + str(dir_z)
                
                blenderCipher.write('\n'+OBJEKTCODE) #Schreibe Code in die CSV
                
                print(name) #Debug
                print(OBJEKTCODE) #Debug
            
        blenderCipher.close() #CSV Datei schliessen

        #Wandle CSV zu BCSV
        import subprocess
        os.popen(("pyjmap tojmap smg ") + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Placement\\'+LayerName+'\\StageObjInfo ') + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Placement\\'+LayerName+'\\StageObjInfo'))




    ############### Start Positionen ##################

    def CSVexport_StartInfo():

        CSVheadings = "name:String:0,MarioNo:Int:0,Obj_arg0:Int:0,Camera_id:Int:0,pos_x:Float:0.0,pos_y:Float:0.0,pos_z:Float:0.0,dir_x:Float:0.0,dir_y:Float:0.0,dir_z:Float:0.0,scale_x:Float:0.0,scale_y:Float:0.0,scale_z:Float:0.0"



        os.popen(("mkdir ") + (bpy.path.abspath('//05_MapExport\\'))+MapName+str('\\stage\\jmp\\Start\\')+LayerName+str('\\')).read() # Map Ordnerstruktur erstellen
        blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Start\\'+LayerName+'\\StartInfo','w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)
        blenderCipher.write(CSVheadings) #Die Headings hinzufuegen



        active = bpy.context.view_layer.objects.active

        for obj in bpy.data.collections["Spawns" + ZonePrefix].all_objects: #Jedes Objekt in csv umwandeln
            if (obj["Layer"]) == LayerName:

                name = "Mario"
                MarioNo = (obj["Spawn ID"])
                obj_arg0 = (obj["Entrance Type"])
                Camera_id = (obj["Camera ID"])
                
                pos_x = (obj.location[0])
                pos_y = (obj.location[2])
                pos_z = (obj.location[1]) * -1
                dir_x = (obj.rotation_euler[0])
                dir_y = (obj.rotation_euler[2])
                dir_z = (obj.rotation_euler[1]) * -1
                scale_x = (obj.scale[0]) #Wofur...
                scale_y = (obj.scale[2])
                scale_z = (obj.scale[1])
                
                dir_x = (math.degrees(dir_x)) #radians zu Grad (degree)
                dir_y = (math.degrees(dir_y))
                dir_z = (math.degrees(dir_z))
                
                #Baue CSV Code zusammen:
                OBJEKTCODE = str(name) + "," + str(MarioNo) + "," + str(obj_arg0) + "," + str(Camera_id) + "," + str(pos_x) + "," + str(pos_y) + "," + str(pos_z) + "," + str(dir_x) + "," + str(dir_y) + "," + str(dir_z) + "," + str(scale_x) + "," + str(scale_y) + "," + str(scale_z)
                
                blenderCipher.write('\n'+OBJEKTCODE) #Schreibe Code in die CSV
                
                print(name) #Debug
                print(OBJEKTCODE) #Debug
            
        blenderCipher.close() #CSV Datei schliessen

        #Wandle CSV zu BCSV
        import subprocess
        os.popen(("pyjmap tojmap smg ") + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Start\\'+LayerName+'\\StartInfo ') + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Start\\'+LayerName+'\\StartInfo'))










    #Common Layer
    LayerName = "Common"
    CSVexport_DebugMoveInfo()# Why
    CSVexport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
    #CSVexport_List() #unused infos, pfeif drauf
    CSVexport_MapPartsInfo()#
    CSVexport_Placement_AreaObjInfo()#
    CSVexport_Placement_CameraCubeInfo()#
    #CSVexport_Placement_ChangeObjInfo() #unused
    CSVexport_Placement_DemoObjInfo()# #Cutscenen
    CSVexport_Placement_ObjInfo()# #Eigentliche Objekte
    CSVexport_Placement_PlanetObjInfo()# #Gravity
    CSVexport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
    CSVexport_StartInfo()#


    #Andere Zusatz Layers:

    if LayerA == True:
        LayerName = "LayerA"
        CSVexport_DebugMoveInfo()#
        CSVexport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVexport_List() #unused infos, pfeif drauf
        CSVexport_MapPartsInfo()#
        CSVexport_Placement_AreaObjInfo()#
        CSVexport_Placement_CameraCubeInfo()#
        #CSVexport_Placement_ChangeObjInfo() #unused
        CSVexport_Placement_DemoObjInfo()# #Cutscenen
        CSVexport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVexport_Placement_PlanetObjInfo()# #Gravity
        CSVexport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVexport_StartInfo()#


    if LayerB == True:
        LayerName = "LayerB"
        CSVexport_DebugMoveInfo()#
        CSVexport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVexport_List() #unused infos, pfeif drauf
        CSVexport_MapPartsInfo()#
        CSVexport_Placement_AreaObjInfo()#
        CSVexport_Placement_CameraCubeInfo()#
        #CSVexport_Placement_ChangeObjInfo() #unused
        CSVexport_Placement_DemoObjInfo()# #Cutscenen
        CSVexport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVexport_Placement_PlanetObjInfo()# #Gravity
        CSVexport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVexport_StartInfo()#


    if LayerC == True:
        LayerName = "LayerC"
        CSVexport_DebugMoveInfo()#
        CSVexport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVexport_List() #unused infos, pfeif drauf
        CSVexport_MapPartsInfo()#
        CSVexport_Placement_AreaObjInfo()#
        CSVexport_Placement_CameraCubeInfo()#
        #CSVexport_Placement_ChangeObjInfo() #unused
        CSVexport_Placement_DemoObjInfo()# #Cutscenen
        CSVexport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVexport_Placement_PlanetObjInfo()# #Gravity
        CSVexport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVexport_StartInfo()#


    if LayerD == True:
        LayerName = "LayerD"
        CSVexport_DebugMoveInfo()#
        CSVexport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVexport_List() #unused infos, pfeif drauf
        CSVexport_MapPartsInfo()#
        CSVexport_Placement_AreaObjInfo()#
        CSVexport_Placement_CameraCubeInfo()#
        #CSVexport_Placement_ChangeObjInfo() #unused
        CSVexport_Placement_DemoObjInfo()# #Cutscenen
        CSVexport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVexport_Placement_PlanetObjInfo()# #Gravity
        CSVexport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVexport_StartInfo()#


    if LayerE == True:
        LayerName = "LayerE"
        CSVexport_DebugMoveInfo()#
        CSVexport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVexport_List() #unused infos, pfeif drauf
        CSVexport_MapPartsInfo()#
        CSVexport_Placement_AreaObjInfo()#
        CSVexport_Placement_CameraCubeInfo()#
        #CSVexport_Placement_ChangeObjInfo() #unused
        CSVexport_Placement_DemoObjInfo()# #Cutscenen
        CSVexport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVexport_Placement_PlanetObjInfo()# #Gravity
        CSVexport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVexport_StartInfo()#


    if LayerF == True:
        LayerName = "LayerF"
        CSVexport_DebugMoveInfo()#
        CSVexport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVexport_List() #unused infos, pfeif drauf
        CSVexport_MapPartsInfo()#
        CSVexport_Placement_AreaObjInfo()#
        CSVexport_Placement_CameraCubeInfo()#
        #CSVexport_Placement_ChangeObjInfo() #unused
        CSVexport_Placement_DemoObjInfo()# #Cutscenen
        CSVexport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVexport_Placement_PlanetObjInfo()# #Gravity
        CSVexport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVexport_StartInfo()#


    if LayerG == True:
        LayerName = "LayerG"
        CSVexport_DebugMoveInfo()#
        CSVexport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVexport_List() #unused infos, pfeif drauf
        CSVexport_MapPartsInfo()#
        CSVexport_Placement_AreaObjInfo()#
        CSVexport_Placement_CameraCubeInfo()#
        #CSVexport_Placement_ChangeObjInfo() #unused
        CSVexport_Placement_DemoObjInfo()# #Cutscenen
        CSVexport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVexport_Placement_PlanetObjInfo()# #Gravity
        CSVexport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVexport_StartInfo()#


    if LayerH == True:
        LayerName = "LayerH"
        CSVexport_DebugMoveInfo()#
        CSVexport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVexport_List() #unused infos, pfeif drauf
        CSVexport_MapPartsInfo()#
        CSVexport_Placement_AreaObjInfo()#
        CSVexport_Placement_CameraCubeInfo()#
        #CSVexport_Placement_ChangeObjInfo() #unused
        CSVexport_Placement_DemoObjInfo()# #Cutscenen
        CSVexport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVexport_Placement_PlanetObjInfo()# #Gravity
        CSVexport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVexport_StartInfo()#


    if LayerI == True:
        LayerName = "LayerI"
        CSVexport_DebugMoveInfo()#
        CSVexport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVexport_List() #unused infos, pfeif drauf
        CSVexport_MapPartsInfo()#
        CSVexport_Placement_AreaObjInfo()#
        CSVexport_Placement_CameraCubeInfo()#
        #CSVexport_Placement_ChangeObjInfo() #unused
        CSVexport_Placement_DemoObjInfo()# #Cutscenen
        CSVexport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVexport_Placement_PlanetObjInfo()# #Gravity
        CSVexport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVexport_StartInfo()#


    if LayerJ == True:
        LayerName = "LayerJ"
        CSVexport_DebugMoveInfo()#
        CSVexport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVexport_List() #unused infos, pfeif drauf
        CSVexport_MapPartsInfo()#
        CSVexport_Placement_AreaObjInfo()#
        CSVexport_Placement_CameraCubeInfo()#
        #CSVexport_Placement_ChangeObjInfo() #unused
        CSVexport_Placement_DemoObjInfo()# #Cutscenen
        CSVexport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVexport_Placement_PlanetObjInfo()# #Gravity
        CSVexport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVexport_StartInfo()#


    if LayerK == True:
        LayerName = "LayerK"
        CSVexport_DebugMoveInfo()#
        CSVexport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVexport_List() #unused infos, pfeif drauf
        CSVexport_MapPartsInfo()#
        CSVexport_Placement_AreaObjInfo()#
        CSVexport_Placement_CameraCubeInfo()#
        #CSVexport_Placement_ChangeObjInfo() #unused
        CSVexport_Placement_DemoObjInfo()# #Cutscenen
        CSVexport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVexport_Placement_PlanetObjInfo()# #Gravity
        CSVexport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVexport_StartInfo()#


    if LayerL == True:
        LayerName = "LayerL"
        CSVexport_DebugMoveInfo()#
        CSVexport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVexport_List() #unused infos, pfeif drauf
        CSVexport_MapPartsInfo()#
        CSVexport_Placement_AreaObjInfo()#
        CSVexport_Placement_CameraCubeInfo()#
        #CSVexport_Placement_ChangeObjInfo() #unused
        CSVexport_Placement_DemoObjInfo()# #Cutscenen
        CSVexport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVexport_Placement_PlanetObjInfo()# #Gravity
        CSVexport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVexport_StartInfo()#


    if LayerM == True:
        LayerName = "LayerM"
        CSVexport_DebugMoveInfo()#
        CSVexport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVexport_List() #unused infos, pfeif drauf
        CSVexport_MapPartsInfo()#
        CSVexport_Placement_AreaObjInfo()#
        CSVexport_Placement_CameraCubeInfo()#
        #CSVexport_Placement_ChangeObjInfo() #unused
        CSVexport_Placement_DemoObjInfo()# #Cutscenen
        CSVexport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVexport_Placement_PlanetObjInfo()# #Gravity
        CSVexport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVexport_StartInfo()#


    if LayerN == True:
        LayerName = "LayerN"
        CSVexport_DebugMoveInfo()#
        CSVexport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVexport_List() #unused infos, pfeif drauf
        CSVexport_MapPartsInfo()#
        CSVexport_Placement_AreaObjInfo()#
        CSVexport_Placement_CameraCubeInfo()#
        #CSVexport_Placement_ChangeObjInfo() #unused
        CSVexport_Placement_DemoObjInfo()# #Cutscenen
        CSVexport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVexport_Placement_PlanetObjInfo()# #Gravity
        CSVexport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVexport_StartInfo()#


    if LayerO == True:
        LayerName = "LayerO"
        CSVexport_DebugMoveInfo()#
        CSVexport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVexport_List() #unused infos, pfeif drauf
        CSVexport_MapPartsInfo()#
        CSVexport_Placement_AreaObjInfo()#
        CSVexport_Placement_CameraCubeInfo()#
        #CSVexport_Placement_ChangeObjInfo() #unused
        CSVexport_Placement_DemoObjInfo()# #Cutscenen
        CSVexport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVexport_Placement_PlanetObjInfo()# #Gravity
        CSVexport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVexport_StartInfo()#


    if LayerP == True:
        LayerName = "LayerP"
        CSVexport_DebugMoveInfo()#
        CSVexport_GeneralPosInfo()# #Positionen fuer Cutscenes und mehr
        #CSVexport_List() #unused infos, pfeif drauf
        CSVexport_MapPartsInfo()#
        CSVexport_Placement_AreaObjInfo()#
        CSVexport_Placement_CameraCubeInfo()#
        #CSVexport_Placement_ChangeObjInfo() #unused
        CSVexport_Placement_DemoObjInfo()# #Cutscenen
        CSVexport_Placement_ObjInfo()# #Eigentliche Objekte
        CSVexport_Placement_PlanetObjInfo()# #Gravity
        CSVexport_Placement_StageObjInfo()# #Zonen Position   Nur bei Main Galaxy
        CSVexport_StartInfo()#
        
        
        
    #################################### PATH EXPORT ##########################################




    C = bpy.context



    # rarcpackPath="C:/SuperMarioGravity/Tools/Archive/Rarc Tools/rarcpack-casesensitive.exe"
    # yaz0encPath="C:/SuperMarioGravity/Tools/Archive/Rarc Tools/yaz0enc.exe"



    ############### PATHS ##################


    ######### PATH OBJECTS ########

    CSVheadingsPath = "name:String:0,type:String:0,closed:String:0,num_pnt:Int:0,l_id:Int:0,path_arg0:Int:0,path_arg1:Int:0,path_arg2:Int:0,path_arg3:Int:0,path_arg4:Int:0,path_arg5:Int:0,path_arg6:Int:0,path_arg7:Int:0,usage:String:0,no:Short:0,Path_ID:Short:0"


    os.popen(("mkdir ") + (bpy.path.abspath('//05_MapExport\\'))+MapName+str('\\stage\\jmp\\Path\\')).read() # Map Ordnerstruktur erstellen
    blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Path\\CommonPathInfo','w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)
    blenderCipher.write(CSVheadingsPath) #Die Headings hinzufuegen



    active = bpy.context.view_layer.objects.active

    for obj in bpy.data.collections["Paths" + ZonePrefix].all_objects: #Jedes Objekt in csv umwandeln
        
        #Zaehle Points:
        #TheCurve = bpy.context.active_object
        #TheBez_points = TheCurve.data.splines[0].bezier_points
        TheBez_points = obj.data.splines[0].bezier_points
        
        
        

        if (obj["Name Alternative"]) == "":
            name = obj.name #Nehme Objektnamen als name
        else:
            name = (obj["Name Alternative"]) #Nehme Text aus der 'Name Alternative' property
        type = "Bezier" #Sind andere Typen uberhaupt moglich?
        
        if obj.data.splines[0].use_cyclic_u == False:
            closed = "OPEN"
        else:
            closed = "CLOSE"
            
        num_pnt = len(TheBez_points[:])
        l_id = obj.data.name
        l_id = l_id.replace(ZonePrefix, '')  #Zonen Prefix entfernen
        path_arg0 = (obj["PathArg0 (Posture Type)"])
        path_arg1 = (obj["PathArg1 (Stop Motion Type)"])
        path_arg2 = (obj["PathArg2 (Guide Type)"])
        path_arg3 = (obj["PathArg3"])
        path_arg4 = (obj["PathArg4 (Initial Position Type)"])
        path_arg5 = (obj["PathArg5"])
        path_arg6 = (obj["PathArg6"])
        path_arg7 = (obj["PathArg7"])
        usage = (obj["Usage"])
        no = l_id
        Path_ID = "-1" #Ist immer -1
        
        
        #Baue CSV Code zusammen:
        OBJEKTCODE = str(name) + "," + str(type) + "," + str(closed) + "," + str(num_pnt) + "," + str(l_id) + "," + str(path_arg0) + "," + str(path_arg1) + "," + str(path_arg2) + "," + str(path_arg3) + "," + str(path_arg4) + "," + str(path_arg5) + "," + str(path_arg6) + "," + str(path_arg7) + "," + str(usage) + "," + str(no) + "," + str(Path_ID)
        
        blenderCipher.write('\n'+OBJEKTCODE) #Schreibe Code in die CSV
        
        print(name) #Debug
        print(OBJEKTCODE) #Debug
        
    blenderCipher.close() #CSV Datei schliessen
    
    ### Path Liste anhand der IDs sortieren, damit die Reihenfolge stimmt
    file_name = bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Path\\CommonPathInfo'
    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)
        data = list(reader)

    # Sortieren nach der 5. Spalte (Path Id)
    data.sort(key=lambda row: int(row[4]))

    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)



    ######### PATH POINTS ########


    CSVheadingsPoints = "point_arg0:Int:0,point_arg1:Int:0,point_arg2:Int:0,point_arg3:Int:0,point_arg4:Int:0,point_arg5:Int:0,point_arg6:Int:0,point_arg7:Int:0,pnt0_x:Float:0.0,pnt0_y:Float:0.0,pnt0_z:Float:0.0,pnt1_x:Float:0.0,pnt1_y:Float:0.0,pnt1_z:Float:0.0,pnt2_x:Float:0.0,pnt2_y:Float:0.0,pnt2_z:Float:0.0,id:Short:0"


    active = bpy.context.view_layer.objects.active

    for obj in bpy.data.collections["Paths" + ZonePrefix].all_objects: #Jedes Objekt in csv umwandeln
        
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        #os.popen(("mkdir ") + (bpy.path.abspath('//04_MapExport\\'))+MapName+str('\\stage\\jmp\\Path\\')).read() # Map Ordnerstruktur erstellen
        import sys, getopt
        import os
        import bpy
        import bpy
        import math
        import mathutils
        import os
        import math
        import subprocess

        #MapName = "TestomatPATHSMap"


        os.popen(("mkdir ") + (bpy.path.abspath('//05_MapExport\\'))+MapName+str('\\stage\\jmp\\Path\\')).read() # Map Ordnerstruktur erstellen


        #obj = bpy.context.active_object
        objType = obj.type
        l_id = obj.data.name
        l_id = l_id.replace(ZonePrefix, '')  #Zonen Prefix entfernen
        Path_ID = l_id


        beziers = []

        for subcurve in obj.data.splines:
            if subcurve.type == 'BEZIER':
                beziers.append(subcurve)
                            

        for subcurve in obj.data.splines:
            
            count = 0 #Point IDs zum Zaehlen
            
            
            blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Path\\CommonPathPointInfo.'+Path_ID,'w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)

            blenderCipher.write("point_arg0:Int:0,point_arg1:Int:0,point_arg2:Int:0,point_arg3:Int:0,point_arg4:Int:0,point_arg5:Int:0,point_arg6:Int:0,point_arg7:Int:0,pnt0_x:Float:0.0,pnt0_y:Float:0.0,pnt0_z:Float:0.0,pnt1_x:Float:0.0,pnt1_y:Float:0.0,pnt1_z:Float:0.0,pnt2_x:Float:0.0,pnt2_y:Float:0.0,pnt2_z:Float:0.0,id:Short:0");
            #str = '%d,%f,%f,%f,%f,%f,%f,%f,%f,%f\n'

            for bezier in beziers:
                for point in bezier.bezier_points:
                    
                    point_arg0 = math.degrees(point.tilt) #radians zu Grad (degree)
                    point_arg0 = round(point_arg0)
                    
                    if point.radius > 1 or point.radius == 1:
                        point_arg5 = -1
                    else:
                        point_arg5 = float(point.radius) * 10000
                        point_arg5 = round(point_arg5)
                    
                    try:
                        PointiID = str(count)
                        point_arg1 = obj.modifiers[PointiID]["Input_4"]
                        point_arg2 = obj.modifiers[PointiID]["Input_5"]
                        point_arg3 = obj.modifiers[PointiID]["Input_6"]
                        point_arg4 = obj.modifiers[PointiID]["Input_7"]
                        
                        point_arg6 = obj.modifiers[PointiID]["Input_9"]
                        point_arg7 = obj.modifiers[PointiID]["Input_10"]
                    except:
                        point_arg1 = "-1"
                        point_arg2 = "-1"
                        point_arg3 = "-1"
                        point_arg4 = "-1"
                        
                        point_arg6 = "-1"
                        point_arg7 = "-1"
                    
                    

                    #### Lokale Pos zu Globale verwandeln:
                    
                    SMGPointXYZ = obj.matrix_world @ point.co
                    SMGPointLEFT_XYZ = obj.matrix_world @ point.handle_left
                    SMGPointRIGHT_XYZ = obj.matrix_world @ point.handle_right
                    
                    SMGPointX = SMGPointXYZ[0]
                    SMGPointY = SMGPointXYZ[2]
                    SMGPointZ = -SMGPointXYZ[1]
                    
                    SMGPointLeftX = SMGPointLEFT_XYZ[0]
                    SMGPointLeftY = SMGPointLEFT_XYZ[2]
                    SMGPointLeftZ = -SMGPointLEFT_XYZ[1]
                    
                    SMGPointRightX = SMGPointRIGHT_XYZ[0]
                    SMGPointRightY = SMGPointRIGHT_XYZ[2]
                    SMGPointRightZ = -SMGPointRIGHT_XYZ[1]
                    
                    
                    
                    
                    blenderCipher.write(('\n') + str(point_arg0) + "," + str(point_arg1) + "," + str(point_arg2) + "," + str(point_arg3) + "," + str(point_arg4) + "," + str(point_arg5) + "," + str(point_arg6) + "," + str(point_arg7) + "," + str(SMGPointX) + "," +  str(SMGPointY) + "," +  str(SMGPointZ) + "," +  str(SMGPointLeftX) + "," +  str(SMGPointLeftY) + "," +  str(SMGPointLeftZ) + "," +  str(SMGPointRightX) + "," +  str(SMGPointRightY) + "," +  str(SMGPointRightZ) + "," +  str(count))
                    count = count + 1

            blenderCipher.close()
        import subprocess
        os.popen(("pyjmap tojmap smg ") + (bpy.path.abspath('//05_MapExport\\'))+MapName+('\\stage\\jmp\\Path\\CommonPathPointInfo.')+Path_ID + (" ") + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Path\\CommonPathPointInfo.')+Path_ID)

        
        
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    blenderCipher.close() #CSV Datei schliessen

    #Wandle CSV zu BCSV
    import subprocess
    os.popen(("pyjmap tojmap smg ") + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Path\\CommonPathInfo ') + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\Path\\CommonPathInfo'))




    ############### (GLE) ##################
    
    ## Checken ob es existiert
    context = bpy.context

    # name of collection
    name = ("GLE" + ZonePrefix)

    scene = context.scene

    coll = bpy.data.collections.get(name)
    if coll is None:
        GLExist = False
    else:
        GLExist = True
    
    
    ## Los gehts 
    if GLExist == True:
        ### Change Scene List ################
        CSVheadings = "GalaxyName:String:0,ScenarioNo:Int:0,ZoneName:String:0,MarioNo:Int:0,[8EA38701]:Int:0,[0EC8B6BD]:Short:0,[195DF712]:Short:0"



        os.popen(("mkdir ") + (bpy.path.abspath('//05_MapExport\\'))+MapName+str('\\stage\\jmp\\List\\')).read() # Map Ordnerstruktur erstellen
        blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\List\\ChangeSceneListInfo','w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)
        blenderCipher.write(CSVheadings) #Die Headings hinzufuegen



        active = bpy.context.view_layer.objects.active

        for obj in bpy.data.collections["GLE" + ZonePrefix].all_objects: #Jedes Objekt in csv umwandeln
            if "EntryPathId" in obj:

                GalaxyName = (obj["GalaxyName"])
                ScenarioNo = (obj["ScenarioNo"])
                ZoneName = (obj["ZoneName"])
                MarioNo = (obj["MarioNo"])
                Player = (obj["Player"])
                ResultPathId = (obj["ResultPathId"])
                EntryPathId = (obj["EntryPathId"])
                
                #Baue CSV Code zusammen:
                OBJEKTCODE = str(GalaxyName) + "," + str(ScenarioNo) + "," + str(ZoneName) + "," + str(MarioNo) + "," + str(Player) + "," + str(ResultPathId) + "," + str(EntryPathId)
                
                blenderCipher.write('\n'+OBJEKTCODE) #Schreibe Code in die CSV
                
                print(name) #Debug
                print(OBJEKTCODE) #Debug
            
        blenderCipher.close() #CSV Datei schliessen

        #Wandle CSV zu BCSV
        import subprocess
        os.popen(("pyjmap tojmap smg ") + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\List\\ChangeSceneListInfo ') + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\List\\ChangeSceneListInfo'))



        ### Stage Info ################
        CSVheadings = "Type:String:0,ScenarioNo:Int:0,Param00Int:Int:0"



        os.popen(("mkdir ") + (bpy.path.abspath('//05_MapExport\\'))+MapName+str('\\stage\\jmp\\List\\')).read() # Map Ordnerstruktur erstellen
        blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\List\\StageInfo','w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)
        blenderCipher.write(CSVheadings) #Die Headings hinzufuegen



        active = bpy.context.view_layer.objects.active

        for obj in bpy.data.collections["GLE" + ZonePrefix].all_objects: #Jedes Objekt in csv umwandeln
            if "Index into the ChangeSceneListInfo file" in obj:

                Type = (obj["Type"])
                ScenarioNo = (obj["Scenario No"])
                Param00Int = (obj["Index into the ChangeSceneListInfo file"])
                
                #Baue CSV Code zusammen:
                OBJEKTCODE = str(Type) + "," + str(ScenarioNo) + "," + str(Param00Int)
                
                blenderCipher.write('\n'+OBJEKTCODE) #Schreibe Code in die CSV
                
                print(name) #Debug
                print(OBJEKTCODE) #Debug
            
        blenderCipher.close() #CSV Datei schliessen

        #Wandle CSV zu BCSV
        import subprocess
        os.popen(("pyjmap tojmap smg ") + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\List\\StageInfo ') + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\List\\StageInfo'))


        ### Scenario Info ################
        CSVheadings = "ScenarioNo:Int:0,[AD3040E7]:Char:0,[042858FE]:Char:0,[9ED80B5A]:Char:0,[9172CFEC]:Char:0,[E854CD6F]:Char:0,[EE3174F3]:Char:0,[2094384B]:Char:0,[0B713C5F]:Char:0,[E0253095]:Char:0,[F734D625]:Char:0,[F2620B53]:Char:0,[9E939DDB]:Char:0,[31A66813]:Char:0,[E4347A41]:Char:0,[38D97447]:Char:0,[4FC5431D]:Float:0.0,[C0241383]:String:0"



        os.popen(("mkdir ") + (bpy.path.abspath('//05_MapExport\\'))+MapName+str('\\stage\\jmp\\List\\')).read() # Map Ordnerstruktur erstellen
        blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\List\\ScenarioSettings','w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)
        blenderCipher.write(CSVheadings) #Die Headings hinzufuegen



        active = bpy.context.view_layer.objects.active

        for obj in bpy.data.collections["GLE" + ZonePrefix].all_objects: #Jedes Objekt in csv umwandeln
            if "PlayAttackMan" in obj:

                ScenarioNo = (obj["Scenario No"])
                NoStarChance = (obj["NoStarChance"])
                PlayAttackMan = (obj["PlayAttackMan"])
                ScoreAttack = (obj["ScoreAttack"])
                RaceId = (obj["RaceId"])
                RaceTutorial = (obj["RaceTutorial"])
                ManualPurpleCoin = (obj["ManualPurpleCoin"])
                NoStopClock = (obj["NoStopClock"])
                NoPause = (obj["NoPause"])
                NoPauseReturn = (obj["NoPauseReturn"])
                NoPauseExit = (obj["NoPauseExit"])
                StoryLayout = (obj["StoryLayout"])
                PeachStarGet = (obj["PeachStarGet"])
                PauseVol = (obj["PauseVol"])
                PauseStarSource = (obj["PauseStarSource"]) ###
                NoWelcome = (obj["NoWelcome"])
                NoScenarioTitle = (obj["NoScenarioTitle"])
                NoBootOut = (obj["NoBootOut"])
                
                #Baue CSV Code zusammen:
                OBJEKTCODE = str(ScenarioNo) + "," + str(NoStarChance) + "," + str(PlayAttackMan) + "," + str(ScoreAttack) + "," + str(RaceId) + "," + str(RaceTutorial) + "," + str(ManualPurpleCoin) + "," + str(NoStopClock) + "," + str(StoryLayout) + "," + str(NoPause) + "," + str(NoPauseReturn) + "," + str(NoPauseExit) + "," + str(NoBootOut) + "," + str(PeachStarGet) + "," + str(NoWelcome) + "," + str(NoScenarioTitle) + "," + str(PauseVol) + "," + str(PauseStarSource)
                
                blenderCipher.write('\n'+OBJEKTCODE) #Schreibe Code in die CSV
                
                print(name) #Debug
                print(OBJEKTCODE) #Debug
            
        blenderCipher.close() #CSV Datei schliessen

        #Wandle CSV zu BCSV
        import subprocess
        os.popen(("pyjmap tojmap smg ") + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\List\\ScenarioSettings ') + (bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\jmp\\List\\ScenarioSettings'))


    # ### DEBUG INFO ###
    # # falls was kaputt geht
    # DebugText= "Exported with SuperBlenderGalaxy v.0.6"
    # blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+MapName+'\\stage\\ExportInfo.txt','w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)
    # blenderCipher.write(DebugText) #Die Headings hinzufuegen
    # blenderCipher.close() #Text Datei schliessen
	
def MapARCEntpacken(GalaxyMapName, WiiExplorerPathFolder, GalaxyFilesystem):



    # rarcpackPath="C:/SuperMarioGravity/Tools/Archive/Rarc Tools/rarcpack-casesensitive.exe"
    # rarcdumpPath="C:/SuperMarioGravity/Tools/Archive/Rarc Tools/rarcdump.exe"
    # yaz0encPath="C:/SuperMarioGravity/Tools/Archive/Rarc Tools/yaz0enc.exe" # komprimieren
    # yaz0decPath="C:/SuperMarioGravity/Tools/Archive/Rarc Tools/yaz0dec.exe" # entschluesseln
    #WiiExplorerPathFolder="C:/SuperMarioGravity/Tools/Archive/WiiExplorer.V1.5.0.5/"
    WiiExplorerPath=WiiExplorerPathFolder + "WiiExplorer.exe"
    #WiiExplorerPath = WiiExplorerPath.replace("/", "//") #why
    #GalaxyFilesystem = GalaxyFilesystem.replace("/", "\\")


    ### GalaxyMap oeffnen und core infos sammeln

    #GalaxyMapName = "TestomatMap" #TEST
    #GalaxyMapName = bpy.context.scene.name
    #LayerName = "Common" #TEST #brauchst eh nicht
    GalaxyMapNameWithExt = GalaxyMapName + ".arc"
    GalaxyMapNameEcn = GalaxyMapNameWithExt + " 0.rarc"
    MapName = GalaxyMapName + "Map"
    
    ## fur testen:
    #GalaxyFilesystem = "C:/SuperMarioGravity/FILESYSTEM/FILESYSTEM/StageData/"

    
    ### Wichtige DEV Ordner erstellen

    nested_directory = bpy.path.abspath("//04_MapImport//{}//".format(GalaxyMapName+"Map"))
    try:
        os.makedirs(nested_directory)
        print(f"Nested directories '{nested_directory}' created successfully.")
    except FileExistsError:
        print(f"One or more directories in '{nested_directory}' already exist.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{nested_directory}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    nested_directory = bpy.path.abspath("//05_MapExport//{}//".format(GalaxyMapName+"Map"))
    try:
        os.makedirs(nested_directory)
        print(f"Nested directories '{nested_directory}' created successfully.")
    except FileExistsError:
        print(f"One or more directories in '{nested_directory}' already exist.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{nested_directory}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    
    # ### GalaxyMap zur Blenderdatei kopieren
    # shutil.copy(GalaxyFilesystem+GalaxyMapName+"/"+GalaxyMapName+"Map.arc", bpy.path.abspath("//{}".format(GalaxyMapNameWithExt)))


    # #Arc datei lesen, ob am Anfang Yaz0 ist, um zu wissen dass es komprimiert ist, und dann entpacken
    # with open(bpy.path.abspath('//'+GalaxyMapNameWithExt), "rb+") as fo:
       # #data = f.read()
       # fo.seek(0, 0)
       # data = fo.read(4)
       # #print(data)
       
       # #Das = (b'Yaz0')
       # #x = struct.unpack('f', data)[0]
        
       # # Print the float value
       # #print(x)
        
        
        # #Checke, ob Yaz0 vorhanden ist
       # if data == (b'Yaz0'):
            # print("Yaz0 komprimiert")
            # subprocess.run([str(yaz0decPath), str(bpy.path.abspath("//{}".format(GalaxyMapNameWithExt)))]) #entschluesseln
            # subprocess.run([str(rarcdumpPath), str(bpy.path.abspath("//{}".format(GalaxyMapNameEcn)))]) #entpacken
            # GalaxyMapNameFOLDERname = GalaxyMapNameEcn + "_dir"
            
       # else:
            # print("Nicht komrimiert")
            # subprocess.run([str(rarcdumpPath), str(bpy.path.abspath("//{}".format(GalaxyMapName)))]) #entpacken
            # GalaxyMapNameFOLDERname = GalaxyMapNameWithExt + "_dir"


    #os.rename((bpy.path.abspath("//{}".format(GalaxyMapNameFOLDERname))), (bpy.path.abspath("//{}".format(GalaxyMapName+"Map")))) #Ordnernamen einfachen Map Namen ohne ext oder so geben




    #os.rename((bpy.path.abspath("//{}".format(GalaxyMapNameFOLDERname))), (bpy.path.abspath("//{}".format(GalaxyMapName+"Map")))) #Ordnernamen einfachen Map Namen ohne ext oder so geben

    dir = bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName+"Map")) #Den Map Ordner aus dem Import Ordner loeschen, falls er schon existiert
    if os.path.exists(dir):
        shutil.rmtree(dir)

    # Falls der Ordner "Camera" und nicht "camera" lautet. Sonst exportet Wiiexplorer es net
    subprocess.run([str(WiiExplorerPath), str("--script"), str(WiiExplorerPathFolder+"BlenderMapScript_Rename.txt"), str(GalaxyFilesystem + GalaxyMapName + str("\\") +  MapName + ".arc"), str("camera"), str("Camera")])
    # 0 = Arc Pfad, 1 = 'camera', 2 = 'Camera'

    subprocess.run([str(WiiExplorerPath), str("--script"), str(WiiExplorerPathFolder+"BlenderMapScript_Extract.txt"), str(MapName), str(bpy.path.abspath("//04_MapImport\\" + MapName + "\\stage\\jmp")), str(bpy.path.abspath("//04_MapImport\\" + MapName + "\\stage\\camera")), str(GalaxyFilesystem + GalaxyMapName + str("\\") +  MapName + ".arc"), str("jmp"), str("camera"), str("Camera")])
    # 0 = Mapname, 1 = Pfad zur jmp, 2 = Pfad zur camera, 3 = Pfad zur ARC, 4 = 'jmp', 5 = 'camera', 6 = 'Camera'
    

    
    
    # shutil.move((bpy.path.abspath("//{}".format(GalaxyMapName+"Map"))), (bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName+"Map"))),'w') #Den Ordner zum 04_Import Ordner verschieben



    #KameraDateien zum 05_MapExport Ordner kopieren

    directory_name = bpy.path.abspath("//05_MapExport//{}//stage//".format(GalaxyMapName+"Map"))

    # Create the directory
    try:
        os.mkdir(directory_name)
        print("Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print("Directory '{directory_name}' already exists.")



    shutil.copytree((bpy.path.abspath("//04_MapImport//{}//stage//camera/".format(GalaxyMapName+"Map"))), (bpy.path.abspath("//05_MapExport//{}//stage//camera/".format(GalaxyMapName+"Map"))), dirs_exist_ok=True)






	
def MapBCSVZuCSV(GalaxyMapName, GalaxyFilesystem):


    #GalaxyMapName = "TESTSpinCity" #TEST
    #LayerName = "Common" #TEST
    #GalaxyMapNameWithExt = GalaxyMapName + ".arc"
    #GalaxyMapNameEcn = GalaxyMapNameWithExt + " 0.rarc"

    #GalaxyMapNameFOLDERname = "TESTSpinCity.arc 0.rarc_dir"


    #GalaxyMapName = "TestomatMap" #TEST
    #GalaxyMapName = bpy.context.scene.name ##############
    #LayerName = "Common" #TEST #brauchst eh nicht
    GalaxyMapNameWithExt = GalaxyMapName + ".arc"
    GalaxyMapNameEcn = GalaxyMapNameWithExt + " 0.rarc"

    #GalaxyFilesystem = "C:/SuperMarioGravity/FILESYSTEM/FILESYSTEM/StageData/"







    #dirname = bpy.path.abspath("//{}".format(GalaxyMapName)) + ("//")
    dirname = bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName)) + "Map" + ("//")
        # = C:\SuperMarioGravity\Scripts\SuperBlenderGalaxy\tests\TestomatMap//

    print(dirname)


    #Checken welche Layer in der Map sind:

    if os.path.isdir(dirname + "stage/jmp/Placement/LayerA"):
        print("LayerA ist da")
        LayerA = True
    else:
        print("LayerA ist nicht da")
        LayerA = False
        
    if os.path.isdir(dirname + "stage/jmp/Placement/LayerB"):
        print("LayerB ist da")
        LayerB = True
    else:
        print("LayerB ist nicht da")
        LayerB = False
        
    if os.path.isdir(dirname + "stage/jmp/Placement/LayerC"):
        print("LayerC ist da")
        LayerC = True
    else:
        print("LayerC ist nicht da")
        LayerC = False
        
    if os.path.isdir(dirname + "stage/jmp/Placement/LayerD"):
        print("LayerD ist da")
        LayerD = True
    else:
        print("LayerD ist nicht da")
        LayerD = False
        
    if os.path.isdir(dirname + "stage/jmp/Placement/LayerE"):
        print("LayerE ist da")
        LayerE = True
    else:
        print("LayerE ist nicht da")
        LayerE = False
        
    if os.path.isdir(dirname + "stage/jmp/Placement/LayerF"):
        print("LayerF ist da")
        LayerF = True
    else:
        print("LayerF ist nicht da")
        LayerF = False
        
    if os.path.isdir(dirname + "stage/jmp/Placement/LayerG"):
        print("LayerG ist da")
        LayerG = True
    else:
        print("LayerG ist nicht da")
        LayerG = False
        
    if os.path.isdir(dirname + "stage/jmp/Placement/LayerH"):
        print("LayerH ist da")
        LayerH = True
    else:
        print("LayerH ist nicht da")
        LayerH = False
        
    if os.path.isdir(dirname + "stage/jmp/Placement/LayerI"):
        print("LayerI ist da")
        LayerI = True
    else:
        print("LayerI ist nicht da")
        LayerI = False
        
    if os.path.isdir(dirname + "stage/jmp/Placement/LayerJ"):
        print("LayerJ ist da")
        LayerJ = True
    else:
        print("LayerJ ist nicht da")
        LayerJ = False
        
    if os.path.isdir(dirname + "stage/jmp/Placement/LayerK"):
        print("LayerK ist da")
        LayerK = True
    else:
        print("LayerK ist nicht da")
        LayerK = False
        
    if os.path.isdir(dirname + "stage/jmp/Placement/LayerL"):
        print("LayerL ist da")
        LayerL = True
    else:
        print("LayerL ist nicht da")
        LayerL = False
        
    if os.path.isdir(dirname + "stage/jmp/Placement/LayerM"):
        print("LayerM ist da")
        LayerM = True
    else:
        print("LayerM ist nicht da")
        LayerM = False
        
    if os.path.isdir(dirname + "stage/jmp/Placement/LayerN"):
        print("LayerN ist da")
        LayerN = True
    else:
        print("LayerN ist nicht da")
        LayerN = False
        
    if os.path.isdir(dirname + "stage/jmp/Placement/LayerO"):
        print("LayerO ist da")
        LayerO = True
    else:
        print("LayerO ist nicht da")
        LayerO = False
        
    if os.path.isdir(dirname + "stage/jmp/Placement/LayerP"):
        print("LayerP ist da")
        LayerP = True
    else:
        print("LayerP ist nicht da")
        LayerP = False
        
        




    #### ZU CSV

    subprocess.call(("pyjmap tocsv smg ") + (dirname) + ("stage/jmp/List/ChangeSceneListInfo ") + (dirname) + ("stage/jmp/List/ChangeSceneListInfo"))
    subprocess.call(("pyjmap tocsv smg ") + (dirname) + ("stage/jmp/List/StageInfo ") + (dirname) + ("stage/jmp/List/StageInfo"))
    
    #Falls GLE Zone
    Pfad = (dirname) + ("stage/jmp/List/ScenarioSettings")
    check_file = os.path.isfile(Pfad)
    if check_file == True:
        subprocess.call(("pyjmap tocsv smg ") + (dirname) + ("stage/jmp/List/ScenarioSettings ") + (dirname) + ("stage/jmp/List/ScenarioSettings"))
        

    ## PATHS:

    #Zaehle Anzahl der Paths:
    lst = os.listdir((dirname) + ("stage/jmp/Path/"))
    NumberPathFiles = len(lst)
    
    UnusedPath = dirname + "stage/jmp/Path/CommonPathPointInfo"
    check_file = os.path.isfile(UnusedPath)
    if check_file == False: 
        NumberPathFiles = NumberPathFiles + 1
    
    
    PathID = NumberPathFiles - 3 # 3 statt 2, weil erster Path 0 sein kann
    PathAnzahl = NumberPathFiles - 2 # Zum Loopen, also wie oft wiederholen bla
    
    print("Anzahl der Paths:")
    print(PathAnzahl)
    print("Start ID vom Path:")
    print(PathID)


    subprocess.call(("pyjmap tocsv smg ") + ('"') + (dirname) + ('stage/jmp/Path/CommonPathInfo" ') + ('"') + (dirname) + ("stage/jmp/Path/CommonPathInfo") + ('"'))

    for i in range(PathAnzahl):
        print("Loopi")
        print(PathID)
        subprocess.call(("pyjmap tocsv smg ") + ('"') + (dirname) + ("stage/jmp/Path/CommonPathPointInfo.") + str(PathID) + ('" ') + ('"') + (dirname) + ("stage/jmp/Path/CommonPathPointInfo.") + str(PathID) + ('"'))
        PathID = PathID - 1


    #Wiederholendes Bla    
    def ToCSVlayerConvert():
        #print("Convert BCSV to CSV from ") + (LAYERname) #geht nicht, lol
        subprocess.call(("pyjmap tocsv smg ") + ('"') + (dirname) + ("stage/jmp/GeneralPos/") + (LAYERname) + ('/GeneralPosInfo" ') + ('"') + (dirname) + ("stage/jmp/GeneralPos/") + (LAYERname) + ("/GeneralPosInfo") + ('"') )
        subprocess.call(("pyjmap tocsv smg ") + ('"') + (dirname) + ("stage/jmp/MapParts/") + (LAYERname) + ('/MapPartsInfo" ') + ('"') + (dirname) + ("stage/jmp/MapParts/") + (LAYERname) + ("/MapPartsInfo") + ('"') )
        subprocess.call(("pyjmap tocsv smg ") + ('"') + (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ('/AreaObjInfo" ') + ('"') + (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ("/AreaObjInfo") + ('"') )
        subprocess.call(("pyjmap tocsv smg ") + ('"') + (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ('/CameraCubeInfo" ') + ('"') + (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ("/CameraCubeInfo") + ('"') )
        subprocess.call(("pyjmap tocsv smg ") + ('"') + (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ('/ChangeObjInfo" ') + ('"') + (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ("/ChangeObjInfo") + ('"') )
        subprocess.call(("pyjmap tocsv smg ") + ('"') + (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ('/DemoObjInfo" ') + ('"') + (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ("/DemoObjInfo") + ('"') )
        subprocess.call(("pyjmap tocsv smg ") + ('"') + (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ('/PlanetObjInfo" ') + ('"') + (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ("/PlanetObjInfo") + ('"') )
        subprocess.call(("pyjmap tocsv smg ") + ('"') + (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ('/StageObjInfo" ') + ('"') + (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ("/StageObjInfo") + ('"') )
        subprocess.call(("pyjmap tocsv smg ") + ('"') + (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ('/ObjInfo" ') + ('"') + (dirname) + ("stage/jmp/Placement/") + (LAYERname) + ("/ObjInfo") + ('"') )
        subprocess.call(("pyjmap tocsv smg ") + ('"') + (dirname) + ("stage/jmp/Start/") + (LAYERname) + ('/StartInfo" ') + ('"') + (dirname) + ("stage/jmp/Start/") + (LAYERname) + ("/StartInfo") + ('"') )
        subprocess.call(("pyjmap tocsv smg ") + ('"') + (dirname) + ("stage/jmp/Debug/") + (LAYERname) + ('/DebugMoveInfo" ') + ('"') + (dirname) + ("stage/jmp/Debug/") + (LAYERname) + ("/DebugMoveInfo") + ('"') )
        #PATHS:
        #os.popen(("pyjmap tocsv smg ") + (dirname) + ("stage/jmp/List/LayerA/StageInfo ") + (dirname) + ("stage/jmp/List/LayerA/StageInfo.csv"))
        #os.popen(("pyjmap tocsv smg ") + (dirname) + ("stage/jmp/List/LayerA/StageInfo ") + (dirname) + ("stage/jmp/List/LayerA/StageInfo.csv"))
        #os.popen(("pyjmap tocsv smg ") + (dirname) + ("stage/jmp/List/LayerA/StageInfo ") + (dirname) + ("stage/jmp/List/LayerA/StageInfo.csv"))
        #os.popen(("pyjmap tocsv smg ") + (dirname) + ("stage/jmp/List/LayerA/StageInfo ") + (dirname) + ("stage/jmp/List/LayerA/StageInfo.csv"))



    #Common Layer
    LAYERname = "Common"
    ToCSVlayerConvert()

    #Andere Zusatz Layers:
    if LayerA == True:
        LAYERname = "LayerA"
        ToCSVlayerConvert()
        
    if LayerB == True:
        LAYERname = "LayerB"
        ToCSVlayerConvert()
        
    if LayerC == True:
        LAYERname = "LayerC"
        ToCSVlayerConvert()
            
    if LayerD == True:
        LAYERname = "LayerD"
        ToCSVlayerConvert()
            
    if LayerE == True:
        LAYERname = "LayerE"
        ToCSVlayerConvert()
            
    if LayerF == True:
        LAYERname = "LayerF"
        ToCSVlayerConvert()
            
    if LayerG == True:
        LAYERname = "LayerG"
        ToCSVlayerConvert()
            
    if LayerH == True:
        LAYERname = "LayerH"
        ToCSVlayerConvert()
            
    if LayerI == True:
        LAYERname = "LayerI"
        ToCSVlayerConvert()
            
    if LayerJ == True:
        LAYERname = "LayerJ"
        ToCSVlayerConvert()    
        
    if LayerK == True:
        LAYERname = "LayerK"
        ToCSVlayerConvert()
            
    if LayerL == True:
        LAYERname = "LayerL"
        ToCSVlayerConvert()
            
    if LayerM == True:
        LAYERname = "LayerM"
        ToCSVlayerConvert()
            
    if LayerN == True:
        LAYERname = "LayerN"
        ToCSVlayerConvert()
            
    if LayerO == True:
        LAYERname = "LayerO"
        ToCSVlayerConvert()
            
    if LayerP == True:
        LAYERname = "LayerP"
        ToCSVlayerConvert()
        
        

	
def ScenarioBCSVZuCSV(context, GalaxyMapName):



    #GalaxyMapName = bpy.context.scene.name


    dirname = bpy.path.abspath("//04_MapImport//{}Scenario//".format(GalaxyMapName)) #+ GalaxyMapName + "Scenario/"

    print(dirname)



    #BCSV zu CSV umwandeln
    subprocess.call(("pyjmap tocsv smg ") + ('"') + (dirname) + ('GalaxyInfo.bcsv" ') + ('"') + (dirname) + ('GalaxyInfo.bcsv"'))
    subprocess.call(("pyjmap tocsv smg ") + ('"') + (dirname) + ('ScenarioData.bcsv" ') + ('"') + (dirname) + ('ScenarioData.bcsv"'))
    subprocess.call(("pyjmap tocsv smg ") + ('"') + (dirname) + ('ZoneList.bcsv" ') + ('"') + (dirname) + ('ZoneList.bcsv"'))
	
def ZonenCreate(ZonenName, ZoneID):



    
    #ZonenName = "Test2Zone"
    #ZoneID = 2
    ZonePrefix = "  (Z" + str(ZoneID) + ")"

    if ZoneID == 0:
        ZonePrefix = ""





    ##DEF Check ob Collection schon existiert:
    def CheckIfAlreadyExist():
        context = bpy.context

        # name of collection
        name = cname

        scene = context.scene

        coll = bpy.data.collections.get(name)
        # if it doesn't exist create it
        if coll is None:
            print("Existiert noch nicht. Gut")
            
        else:
            col = bpy.data.collections.get(name)
            if col:
                col.name = name + "_OLD"
                ZoneID = bpy.data.collections[name + "_OLD"]["Zone ID"] #Alte ID aufgreifen und fur neue Zone nehmen
                ZonePrefix = "  (Z" + str(ZoneID) + ")"
                bpy.data.collections[name + "_OLD"]["Zone ID"] = "NONE"
                
                
                
    ##Haupt Collection Erstellen
    cname = ZonenName
    CheckIfAlreadyExist()

    collection = bpy.data.collections.new(ZonenName)
    bpy.context.scene.collection.children.link(collection)

    bpy.data.collections[ZonenName]["Zone ID"] = ZoneID
    
    ##Unterkategorien Collections Erstellen
    shared_assets_collection_name = ZonenName

    cname = "Objects" + ZonePrefix
    CheckIfAlreadyExist()
    c = bpy.data.collections.new(cname)
    bpy.data.collections.get(shared_assets_collection_name).children.link(c)

    cname = "MapParts" + ZonePrefix
    CheckIfAlreadyExist()
    c = bpy.data.collections.new(cname)
    bpy.data.collections.get(shared_assets_collection_name).children.link(c)

    cname = "Spawns" + ZonePrefix
    CheckIfAlreadyExist()
    c = bpy.data.collections.new(cname)
    bpy.data.collections.get(shared_assets_collection_name).children.link(c)

    cname = "Positions" + ZonePrefix
    CheckIfAlreadyExist()
    c = bpy.data.collections.new(cname)
    bpy.data.collections.get(shared_assets_collection_name).children.link(c)

    cname = "Cameras" + ZonePrefix
    CheckIfAlreadyExist()
    c = bpy.data.collections.new(cname)
    bpy.data.collections.get(shared_assets_collection_name).children.link(c)

    cname = "Areas" + ZonePrefix
    CheckIfAlreadyExist()
    c = bpy.data.collections.new(cname)
    bpy.data.collections.get(shared_assets_collection_name).children.link(c)

    cname = "Gravities" + ZonePrefix
    CheckIfAlreadyExist()
    c = bpy.data.collections.new(cname)
    bpy.data.collections.get(shared_assets_collection_name).children.link(c)

    cname = "Cutscenes" + ZonePrefix
    CheckIfAlreadyExist()
    c = bpy.data.collections.new(cname)
    bpy.data.collections.get(shared_assets_collection_name).children.link(c)

    cname = "Debug" + ZonePrefix
    CheckIfAlreadyExist()
    c = bpy.data.collections.new(cname)
    bpy.data.collections.get(shared_assets_collection_name).children.link(c)

    cname = "ZonePositions" + ZonePrefix
    CheckIfAlreadyExist()
    c = bpy.data.collections.new(cname)
    bpy.data.collections.get(shared_assets_collection_name).children.link(c)

    cname = "Paths" + ZonePrefix
    CheckIfAlreadyExist()
    c = bpy.data.collections.new(cname)
    bpy.data.collections.get(shared_assets_collection_name).children.link(c)
    
    # cname = "MiscSettings" + ZonePrefix
    # CheckIfAlreadyExist()
    # c = bpy.data.collections.new(cname)
    # bpy.data.collections.get(shared_assets_collection_name).children.link(c)
	
class AddZoneToScenario(bpy.types.Operator):
    """Add zone to scenario"""
    bl_idname = "scenario55.addzone" 
    bl_label = "Add Zone to scenario"
    def execute(self, context):
        ZoneName = bpy.context.collection.name
        scene = bpy.context.scene
        if "Zone ID" in bpy.context.collection:
            for view_layer in scene.view_layers:
                if "ScenarioName" in view_layer:
                    bpy.context.view_layer[ZoneName] = "0"
        return {'FINISHED'}

def ScenarioARCEntpacken(GalaxyMapName, WiiExplorerPathFolder, GalaxyFilesystem):



    # rarcpackPath="C:/SuperMarioGravity/Tools/Archive/Rarc Tools/rarcpack-casesensitive.exe"
    # rarcdumpPath="C:/SuperMarioGravity/Tools/Archive/Rarc Tools/rarcdump.exe"
    # yaz0encPath="C:/SuperMarioGravity/Tools/Archive/Rarc Tools/yaz0enc.exe" # komprimieren
    # yaz0decPath="C:/SuperMarioGravity/Tools/Archive/Rarc Tools/yaz0dec.exe" # entschluesseln
    #WiiExplorerPathFolder="C:/SuperMarioGravity/Tools/Archive/WiiExplorer.V1.5.0.5/"
    WiiExplorerPath=WiiExplorerPathFolder + "WiiExplorer.exe"




    #GalaxyMapName = bpy.context.scene.name
    GalaxyMapNameWithExt = GalaxyMapName + ".arc"
    GalaxyMapNameEcn = GalaxyMapNameWithExt + " 0.rarc"

    #GalaxyFilesystem = "C:/SuperMarioGravity/FILESYSTEM/FILESYSTEM/StageData/"
    
    ScenarioName = GalaxyMapName + "Scenario"

    # ### GalaxyScenario zur Blenderdatei kopieren
    # shutil.copy(GalaxyFilesystem+GalaxyMapName+"/"+GalaxyMapName+"Scenario.arc", bpy.path.abspath("//{}".format(GalaxyMapNameWithExt)))




    # #Arc datei lesen, ob am Anfang Yaz0 ist, um zu wissen dass es komprimiert ist, und dann entpacken
    # with open(bpy.path.abspath('//'+GalaxyMapNameWithExt), "rb+") as fo:
       # #data = f.read()
       # fo.seek(0, 0)
       # data = fo.read(4)
       # #print(data)
       
       # #Das = (b'Yaz0')
       # #x = struct.unpack('f', data)[0]
        
       # # Print the float value
       # #print(x)
        
        
        # #Checke, ob Yaz0 vorhanden ist
       # if data == (b'Yaz0'):
            # print("Yaz0 komprimiert")
            # subprocess.run([str(yaz0decPath), str(bpy.path.abspath("//{}".format(GalaxyMapNameWithExt)))]) #entschluesseln
            # subprocess.run([str(rarcdumpPath), str(bpy.path.abspath("//{}".format(GalaxyMapNameEcn)))]) #entpacken
            # GalaxyMapNameFOLDERname = GalaxyMapNameEcn + "_dir"
            
       # else:
            # print("Nicht komrimiert")
            # subprocess.run([str(rarcdumpPath), str(bpy.path.abspath("//{}".format(GalaxyMapName)))]) #entpacken
            # GalaxyMapNameFOLDERname = GalaxyMapNameWithExt + "_dir"


    #os.rename((bpy.path.abspath("//{}".format(GalaxyMapNameFOLDERname))), (bpy.path.abspath("//{}".format(GalaxyMapName+"Map")))) #Ordnernamen einfachen Map Namen ohne ext oder so geben

    #os.rename((bpy.path.abspath("//{}".format(GalaxyMapNameFOLDERname))), (bpy.path.abspath("//{}".format(GalaxyMapName+"Scenario")))) #Ordnernamen einfachen Map Namen ohne ext oder so geben

    
    

    dir = bpy.path.abspath("//04_MapImport//{}".format(ScenarioName)) #Den Scenario Ordner aus dem Import Ordner loeschen, falls er schon existiert
    if os.path.exists(dir):
        shutil.rmtree(dir)

    os.popen(("mkdir ") + (bpy.path.abspath('//04_MapImport\\'))+ScenarioName+str('\\')).read()
    #shutil.move((bpy.path.abspath("//{}".format(GalaxyMapName+"Scenario"))), (bpy.path.abspath("//04_MapImport//{}".format(GalaxyMapName+"Scenario"))),'w') #Den Ordner zum 04_Import Ordner verschieben

    subprocess.run([str(WiiExplorerPath), str("--script"), str(WiiExplorerPathFolder+"BlenderMapScript_Scenario.txt"), str(GalaxyFilesystem + GalaxyMapName + str("\\") +  ScenarioName + ".arc"), str(bpy.path.abspath("//04_MapImport\\" + ScenarioName + "\\GalaxyInfo.bcsv")), str(bpy.path.abspath("//04_MapImport\\" + ScenarioName + "\\ScenarioData.bcsv")), str(bpy.path.abspath("//04_MapImport\\" + ScenarioName + "\\ZoneList.bcsv")), str("GalaxyInfo.bcsv"), str("ScenarioData.bcsv"), str("ZoneList.bcsv")])
    # 0 = arc, 1 = Exportpfad GalaxyInfo.bcsv, 2 = Exportpfad ScenarioData.bcsv, 3 = exportpfad ZoneList.bcsv, 4 = 'GalaxyInfo.bcsv', 5 = 'ScenarioData.bcsv', 6 = 'ZoneList.bcsv'


def HashCalculate(valHash):
    import sys
    name = valHash
    h = 0
    for c in name:
        h = (h*31 + ord(c)) & 0xFFFFFFFF
    valHash = hex(h).lstrip("0x").rstrip("L").zfill(8).upper()
    
    print("Hash is:")
    print(valHash)
	
	
def GiveFreeSwitchID(Switch, FullGalaxy):

    def GetFreeSwitchID(collections, properties, min_value=0, max_value=127):
        used_values = set()

        # Alle Objekte in den angegebenen Collections durchgehen
        for collection in collections:
            for obj in collection.objects:
                for prop in properties:
                    if prop in obj:  # Prüfen, ob die Property existiert
                        used_values.add(obj[prop])

        # Die kleinste nicht verwendete Zahl im Bereich finden
        for new_value in range(min_value, max_value + 1):
            if new_value not in used_values:
                return new_value

        return None  # Falls keine Zahl im Bereich verfügbar ist
        
        
        
    ## ZONE ID Vom aktiven Objekt bekommen ##
    
    ## WHY GEHT DIESE  SCHEISSE NICHT ?????!??
    
    # obj = bpy.context.object  # Das aktuell ausgewählte Objekt

    # if obj:
        # collections = obj.users_collection  # Alle Collections des Objekts
        
        # for col in collections:
            # if "Zone ID" in col:  # Prüfen, ob die Collection das Custom Property hat
                # ZoneID = col["Zone ID"]  # Den Wert abrufen
                # print(f"Zone ID-Wert: {ZoneID}")
                # print("-------------------------------------")
                # break  # Falls nur die erste passende Collection ausgegeben werden soll
        # else:
            # print("Keine Collection mit 'Zone ID' gefunden. -------------------------------------")
    # else:
        # print("Kein Objekt ausgewählt.-------------------------------------")
    
    # Hier ich geb auf, du arsch:
    GalaxyMapName = bpy.context.collection.name
    ZoneID = bpy.data.collections[GalaxyMapName]["Zone ID"]
    
    ZonePrefix = "  (Z" + str(ZoneID) + ")"
    if ZoneID == 0:
        ZonePrefix = ""


    # Namen der Collections, die geprüft werden sollen
    collection_names = ["Objects" + ZonePrefix, "MapParts" + ZonePrefix, "Spawns" + ZonePrefix, "Cameras" + ZonePrefix, "Areas" + ZonePrefix, "Gravities" + ZonePrefix]

    # Liste der Collections abrufen
    
    if FullGalaxy == False:
        collections = [bpy.data.collections.get(name) for name in collection_names if bpy.data.collections.get(name)]
    else:
        collections = bpy.data.collections  # Alle Collections verwenden


    # Properties, die gecheckt werden sollen
    properties_to_check = {"SW_A", "SW_APPEAR", "SW_B", "SW_AWAKE", "SW_PARAM", "SW_DEAD"}

    if collections:
        if FullGalaxy == False:
            unused_value = GetFreeSwitchID(collections, properties_to_check, 0, 127)  #Per Zone 0-127, global alles: 1000-1127
            
            if unused_value is not None:
                print(f"Die nächste freie Zahl im Bereich 0-127 ist: {unused_value}")
                
                
                #bpy.context.object["SW_A"] = unused_value
                bpy.context.object[Switch] = unused_value
            else:
                print("Es gibt keine freien Zahlen mehr im Bereich 0-127!")
                self.report({'INFO'}, "NO SWITCH AVAILABLE! 0-127 are used!")
                
        else:
            unused_value = GetFreeSwitchID(collections, properties_to_check, 1000, 1127)
            
            if unused_value is not None:
                print(f"Die nächste freie Zahl im Bereich 1000-1127 ist: {unused_value}")
                
                #bpy.context.object["SW_A"] = unused_value
                bpy.context.object[Switch] = unused_value
            else:
                print("Es gibt keine freien Zahlen mehr im Bereich 1000-1127!")
                self.report({'INFO'}, "NO SWITCH AVAILABLE! 1000-1127 are used!")
    else:
        print("Keine der angegebenen Collections wurde gefunden!")
        self.report({'INFO'}, "Collections don't exist")

    
    
import bpy
import xml.etree.ElementTree as ET
import os

# Globaler Cache für XML-Daten (kein lag)
xml_cache = {}

def load_labels_from_xml(obj_name, NumberOfArgs, IsGravityObject):
    global xml_cache

    # XML-Pfad abrufen
    xml_path = bpy.context.workspace.get("Object Database", "")
    
    # Prüfen, ob Datei existiert
    if not os.path.exists(xml_path):
        return "Unknown", [f"Obj_Arg{i}" for i in range(NumberOfArgs)]

    # Prüfen, ob XML bereits geladen wurde
    if xml_path not in xml_cache:
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            xml_cache[xml_path] = {obj.get("id"): obj for obj in root.findall("object")}
        except Exception as e:
            print(f"Fehler beim Laden der XML: {e}")
            return "Unknown", [f"Obj_Arg{i}" for i in range(NumberOfArgs)]

    # Objekt suchen
    obj_data = xml_cache[xml_path].get(obj_name)
    if obj_data:
        display_name = obj_data.find("name").text if obj_data.find("name") is not None else "Unknown"
        labels = [field.get("name", f"Obj_Arg{i}") for i, field in enumerate(obj_data.findall("field"))]
        # Standard-Notes aus XML
        notes = obj_data.find("notes").text if obj_data.find("notes") is not None else ""

        # Field-Infos an Notes anhängen
        notes = notes + "\n-- PARAMETERS --"
        for field in obj_data.findall("field"):
            field_id = field.get("id", "?")
            name = field.get("name", "Unknown")
            field_notes = field.get("notes", "").replace("&quot;", "\"")
            values = field.get("values", "None").replace("&quot;", "\"")

            # Formatierung der Field-Informationen
            field_text = f"\n~ {name} (arg{field_id}) ~\n{field_notes}\n{values}\n|\n"

            # Falls values leer ist, nicht anzeigen
            if values == "None":
                field_text = f"Arg {field_id}: {name}. {field_notes}."

            # Notes erweitern
            notes += f"\n\n{field_text}" if notes else field_text

        return display_name, labels, notes

    return "Unknown", [f"Obj_Arg{i}" for i in range(NumberOfArgs)], "Undocumented"  # Fallback

    
    

###CLASSES -----------------------------------------------------

class GalaxyMapOperator1(bpy.types.Operator):
    """Import Whole Galaxy Stage with sub zones"""
    bl_idname = "object.galaxymap_operator1" 
    bl_label = "Import Full Galaxy:"
    def execute(self, context):
        GalaxyMapName = bpy.context.workspace["Galaxy Name"]
        WiiExplorerPathFolder = bpy.context.workspace["WiiExplorer Folder Path"]
        AssetSearch = bpy.context.workspace["Asset Searching Enabled"]
        GalaxyFilesystem = bpy.context.workspace["StageData Folder Path"]
        MapAssetBlendFile = bpy.context.workspace["Map Assets Blend file"]
        BlendFilesFolder = bpy.context.workspace["Workspace (for searching in Blend files)"]
        
        
        if bpy.context.workspace["Asset Searching Enabled"] == False:
            AssetSearch = False
        else:
            AssetSearch = True
        
        GalaxyMapNameBackup = GalaxyMapName
        ScenarioARCEntpacken(GalaxyMapName, WiiExplorerPathFolder, GalaxyFilesystem)
        ScenarioBCSVZuCSV(context, GalaxyMapName)
        
        
        dirname = bpy.path.abspath("//04_MapImport//{}Scenario//".format(GalaxyMapName)) #+ GalaxyMapName + "Scenario//"
        CSVname = (dirname) + ("ZoneList.bcsv")
        ##Zaehlen, wie viele rows es gibt
        file = open(CSVname)
        row_count = len(file.readlines())
        print("Anzahl der Zonen:")
        print(row_count)
        
        ZonesList = [] #Brauchen wir dann, wenn wir Scenarioinfos importieren
        
        with open (CSVname) as f:
            reader = csv.reader(f)
            row = next(reader) #gehe zur naechsten Row
            
            #Erstmal nur die Collections erstellen
            bpy.ops.scene.new(type='NEW') # Neue Scene erstellen
            bpy.context.scene.name = "LEVEL EDITING"
            ZoneID = 0
            for i in range(row_count): #row_count ist wie oft er das hier wiederholen soll
                for row in reader:
                    ZonenName = row[0]
                    ZonenCreate(ZonenName, ZoneID)
                    
                    #ZonenInfos sammeln wegen Scenario:
                    ZonesList.append(ZonenName)
                    
                    #LoopBla
                    ZoneID = ZoneID + 1
                    print("test " + ZonenName)
                    

                    
            f.seek(1) # Gehe zur 1en Linie in der CSV
            row = next(reader) #gehe zur naechsten Row
            #Jetzt die Zonen extrahieren und importieren
            ZoneID = 0
            for i in range(row_count): #row_count ist wie oft er das hier wiederholen soll
                for row in reader:
                    GalaxyMapName = row[0]
                    MapARCEntpacken(GalaxyMapName, WiiExplorerPathFolder, GalaxyFilesystem)
                    MapBCSVZuCSV(GalaxyMapName, GalaxyFilesystem)
                    CSVtoBlender(self, GalaxyMapName, ZoneID, AssetSearch, MapAssetBlendFile, BlendFilesFolder)
                    ZoneID = ZoneID + 1
        
        GalaxyMapName = GalaxyMapNameBackup
        ##ScenarioKram
        dirname = bpy.path.abspath("//04_MapImport//{}Scenario//".format(GalaxyMapName)) #+ GalaxyMapName + "Scenario//"
        CSVname = (dirname) + ("ScenarioData.bcsv")
        ##Zaehlen, wie viele rows es gibt
        file = open(CSVname)
        row_count = len(file.readlines())
        print("Anzahl der Scenarios:")
        print(row_count)
        with open (CSVname) as f:
            print("Hallo")
            reader = csv.DictReader(f, delimiter=',') #So liest er anhand column namen row['bla'] und nicht row[3]
            #row = next(reader) #gehe zur naechsten Row #Wegen das in der letzten Zeile unnoetig
            ScenarioLoopID = 0
            for i in range(row_count): #row_count ist wie oft er das hier wiederholen soll
                for row in reader:
                    ScenarioID = row['ScenarioNo:Int:0']
                    ScenarioName = row['ScenarioName:String:0']
                    StarMask = row['PowerStarId:Int:0']
                    PowerStarType = row['PowerStarType:String:0']
                    AppearPowerStarObj = row['AppearPowerStarObj:String:0']
                    Comet = row['Comet:String:0']
                    CometLimitTimer = row['CometLimitTimer:Int:0']
                    LuigiModeTimer = row['LuigiModeTimer:Int:0']
                    
                    try:
                        PowerStarColor = row['PowerStarColor:Int:0']
                        GLE_PowserStarColor = True
                    except:
                        try:
                            PowerStarColor = row['[108314CC]:Int:0']
                            GLE_PowserStarColor = True
                        except:
                            GLE_PowserStarColor = False
                    
                    
                    
                    # VIEW LAYER per Scenario erstellen:
                    
                    NewLayerName = "[" + str(ScenarioID) + "] " + str(ScenarioName)
                    
                    if ScenarioID == 1:
                        bpy.context.scene.view_layers["ViewLayer"].name = NewLayerName
                    else:
                        # Überprüfen, ob der Name bereits existiert
                        if NewLayerName not in bpy.context.scene.view_layers:
                            TheNewLayer = bpy.context.scene.view_layers.new(name=NewLayerName)
                            print(f"Neuer View Layer '{NewLayerName}' wurde erstellt.")
                        else:
                            print(f"View Layer '{NewLayerName}' existiert bereits.")
                        
                        bpy.context.window.view_layer = bpy.context.scene.view_layers[NewLayerName] #neuen Layer als den aktiven machen



                    # bpy.context.scene.name = "[" + str(ScenarioID) + "] " + str(ScenarioName) #nur name
                    
                    # bpy.context.scene["StarMask"] = int(StarMask)
                    # bpy.context.scene["ScenarioNo"] = int(ScenarioID)
                    # bpy.context.scene["ScenarioName"] = ScenarioName
                    # bpy.context.scene["Scenario Type"] = PowerStarType #Scenario typ, also ob grun oder hidden
                    # bpy.context.scene["Power Star Trigger"] = AppearPowerStarObj
                    # bpy.context.scene["Comet"] = Comet
                    # bpy.context.scene["Comet Time Limit"] = CometLimitTimer #In Sekunden
                    # bpy.context.scene["LuigiModeTimer (unused)"] = LuigiModeTimer
                    
                    ## 
                    

                    
                    bpy.context.scene.view_layers[NewLayerName]["StarMask"] = int(StarMask)
                    bpy.context.scene.view_layers[NewLayerName]["ScenarioNo"] = int(ScenarioID)
                    bpy.context.scene.view_layers[NewLayerName]["ScenarioName"] = ScenarioName
                    bpy.context.scene.view_layers[NewLayerName]["Scenario Type"] = PowerStarType #Scenario typ, also ob grun oder hidden
                    bpy.context.scene.view_layers[NewLayerName]["Power Star Trigger"] = AppearPowerStarObj
                    bpy.context.scene.view_layers[NewLayerName]["Comet"] = Comet
                    bpy.context.scene.view_layers[NewLayerName]["Comet Time Limit"] = CometLimitTimer #In Sekunden
                    bpy.context.scene.view_layers[NewLayerName]["LuigiModeTimer (unused)"] = LuigiModeTimer
                    
                    # GLE
                    if GLE_PowserStarColor == True:
                        bpy.context.scene.view_layers[NewLayerName]["Power Star Color"] = PowerStarColor
                        
                    

                    for val in ZonesList:
                        print(val)
                        try:
                            LayerMask = row[val + ":Int:0"] #val ist der ZonenName. Nehme Info von der ZonenNamen Colunm
                            bpy.context.scene.view_layers[NewLayerName][val] = LayerMask #Property fuer Scene mit Zonennamen und dessen Layer Mask
                        except: #Falls es als Hashish und nicht normalen Namen gespeichert ist und so
                            valHash = val
                            #HashCalculate(valHash) #Er uebernimmt den neuen string net...
                            import sys
                            name = valHash
                            h = 0
                            for c in name:
                                h = (h*31 + ord(c)) & 0xFFFFFFFF
                            valHash = hex(h).lstrip("0x").rstrip("L").zfill(8).upper()
                            print("Hash is:")
                            print(valHash)
                            
                            LayerMask = row["["+valHash+"]" + ":Int:0"] #val ist der ZonenName. Nehme Info von der ZonenNamen Colunm
                            bpy.context.scene.view_layers[NewLayerName][val] = LayerMask #Property fuer Scene mit Zonennamen und dessen Layer Mask
                        try:
                            LayerDisplay(val)
                        except:
                            print("LayerDisplay hat net geklappt!")
                    
                    ScenarioLoopID = ScenarioLoopID + 1
            
        
        ## GalaxyInfo
        #Hat nur Welt ID, ausser GLE wird genutzt
        
        dirname = bpy.path.abspath("//04_MapImport//{}Scenario//".format(GalaxyMapName)) #+ GalaxyMapName + "Scenario//"
        CSVname = (dirname) + ("GalaxyInfo.bcsv")
        ##Zaehlen, wie viele rows es gibt
        file = open(CSVname)
        row_count = len(file.readlines())
        
        with open (CSVname) as f:
            reader = csv.DictReader(f, delimiter=',')
            
            for i in range(row_count): #row_count ist wie oft er das hier wiederholen soll
                for row in reader:
                    
                    try:
                        WorldNo = row["WorldNo:Int:0"]
                        GLEscenario = False
                    # except:
                        # GLEscenario = True
                        # Type = row["Type:String:0"
                        # Param00Int = row["Param00Int:Int:0"]
                        # Param00Str = row["Param00Str:String:0"]
                        
                        # try:
                            # PowerStarNum = row["PowerStarNum:Int:0"]
                        # try:
                         # = row["[1D2DCADA]:String:0"] #FlagName1
                        # try:
                         # = row["[859CBC11]:String:0"]
                        # try:
                         # = row["[859CBC12]:String:0"]
                        # try:
                         # = row["[859CBC13]:String:0"]
                        # try:
                         # = row["[859CBC14]:String:0"]
                        # try:
                         # = row["[8F1FE1E1]:Int:0"] # Param01Int (Optional)
                        # try:
                         # = row["[09E9B634]:Int:0"] # TicoCoinNum
                        
                        # ## Da sind so viele moglichkeiten, dass ich mir was anderes ausdenken muss. Lass mas erstmal
                        
                        
                        for col in bpy.data.collections:
                            if "Zone ID" in col:
                                if col["Zone ID"] == 0:
                                    col["World Number"] = int(WorldNo)
        
                    except:
                        print("bla")
        self.report({'INFO'}, "GALAXY IMPORTED!")
        return {'FINISHED'}
    

class GalaxyMapOperator2(bpy.types.Operator):
    """Import single Zone"""
    bl_idname = "objecti.galaxymap_operator2" 
    bl_label = "Import Single Zone" 
    def execute(self, context):
        #GalaxyMapName = bpy.context.scene.name #nehme den Scenenamen als GalaxyMap Namen zb BigGalaxy
        GalaxyMapName = bpy.context.workspace["Zone Name"]
        WiiExplorerPathFolder = bpy.context.workspace["WiiExplorer Folder Path"]
        AssetSearch = bpy.context.workspace["Asset Searching Enabled"]
        BlendFilesFolder = bpy.context.workspace["Workspace (for searching in Blend files)"]
        MapAssetBlendFile = bpy.context.workspace["Map Assets Blend file"]
        GalaxyFilesystem = bpy.context.workspace["StageData Folder Path"]
        
        
        
        if bpy.context.workspace["Asset Searching Enabled"] == 0:
            AssetSearch = False
        else:
            AssetSearch = True
            
        ZonenName = GalaxyMapName
        
        ZoneCount = 0
        for col in bpy.data.collections:
            if "Zone ID" in col:
                ZoneCount = ZoneCount + 1
        ZoneID = ZoneCount #Get a free Zone ID for new zone

        scene = bpy.context.scene
        for view_layer in scene.view_layers:
            if "ScenarioNo" in view_layer:
                #print(scene["Test"])
                bpy.context.view_layer[GalaxyMapName] = 0 #Star Mask add
        
        ZonenCreate(ZonenName, ZoneID)
        MapARCEntpacken(GalaxyMapName, WiiExplorerPathFolder, GalaxyFilesystem)
        MapBCSVZuCSV(GalaxyMapName, GalaxyFilesystem)
        CSVtoBlender(self, GalaxyMapName, ZoneID, AssetSearch, MapAssetBlendFile, BlendFilesFolder)
        #ArcPack(context) #
        self.report({'INFO'}, "ZONE IMPORTED!")
        return {'FINISHED'}
    
class GalaxyMapOperator3(bpy.types.Operator):
    """Export Whole Galaxy Stage with sub zones"""
    bl_idname = "objecto.galaxymap_operator3" 
    bl_label = "Export Full Galaxy" 
    def execute(self, context):
        
        GalaxyFilesystem = bpy.context.workspace["StageData Folder Path"]
        WiiExplorerPathFolder = bpy.context.workspace["WiiExplorer Folder Path"]
        
        for col in bpy.data.collections:
                if "Zone ID" in col:
                    print("==========================================")
                    print("Export this zone:")
                    print(col.name)
                    print("Zone ID:")
                    print(col["Zone ID"])
                    
                    GalaxyMapName = (col.name)
                    ZoneID = bpy.data.collections[GalaxyMapName]["Zone ID"]
                    Export(GalaxyMapName, ZoneID)
                    ArcPack(GalaxyMapName, WiiExplorerPathFolder, GalaxyFilesystem)
                    
                    print("Zone Export Finished")
                    print("==========================================")
                    
        
                

        self.report({'INFO'}, "GALAXY EXPORTED!")
        return {'FINISHED'}
    
class GalaxyMapOperator4(bpy.types.Operator):
    """Export single Zone"""
    bl_idname = "objectu.galaxymap_operator4" 
    bl_label = "Export Single Zone" 
    def execute(self, context):
        if not "Zone ID" in bpy.context.collection:
            self.report({'WARNING'}, 'No valid Zone selected!')
            return {'FINISHED'}
        GalaxyMapName = bpy.context.collection.name
        ZoneID = bpy.data.collections[GalaxyMapName]["Zone ID"]
        WiiExplorerPathFolder = bpy.context.workspace["WiiExplorer Folder Path"]
        GalaxyFilesystem = bpy.context.workspace["StageData Folder Path"]
        
        Export(GalaxyMapName, ZoneID)
        ArcPack(GalaxyMapName, WiiExplorerPathFolder, GalaxyFilesystem)
        
        self.report({'INFO'}, '"'+GalaxyMapName + '" successfully exported!')
        return {'FINISHED'}
 
 
 
 
class GalaxyMapOperator5(bpy.types.Operator):
    """Create Collection Assets for a new Zone"""
    bl_idname = "objecta.galaxymap_operator5" 
    bl_label = "Create new Zone" 
    def execute(self, context):
        #GalaxyMapName = "NewZone"
        GalaxyMapName = bpy.context.workspace["Zone Name"]
        ZonenName = GalaxyMapName
        
        
        
        
        ZoneCount = 0
        for col in bpy.data.collections:
            if "Zone ID" in col:
                ZoneCount = ZoneCount + 1
        ZoneID = ZoneCount #Get a free Zone ID for new zone

        scene = bpy.context.scene
        for view_layer in scene.view_layers:
            if "ScenarioNo" in view_layer:
                #print(scene["Test"])
                view_layer[GalaxyMapName] = "0" #Star Mask add
        
        ZonenCreate(ZonenName, ZoneID)
        bpy.data.collections[ZonenName]["Zone ID"] = ZoneID
        self.report({'INFO'}, "Zone "+ZonenName+" created!")
        return {'FINISHED'}
    
class GalaxyMapOperator6(bpy.types.Operator):
   """Edit selected zone with LaunchCamPlus"""
   bl_idname = "objecty.galaxymap_operator6" 
   bl_label = "Start Camera Editor" 
   def execute(self, context):
       GalaxyMapName = bpy.context.collection.name
       WiiExplorerPathFolder = bpy.context.workspace["WiiExplorer Folder Path"]
       CameraEditorPathFolder = bpy.context.workspace["LaunchCamPlus Folder Path"]
       
       CameraEdit(GalaxyMapName, WiiExplorerPathFolder, CameraEditorPathFolder)
       self.report({'INFO'}, "Launch Cam Plus will be started")
       return {'FINISHED'}
   
   
class GalaxyMapOperator7(bpy.types.Operator):
    """Update Layer Info of current Scenario"""
    bl_idname = "objecte.galaxymap_operator7" 
    bl_label = "Update Layer Info" 
    def execute(self, context):
        for scene in bpy.data.scenes:
            if "StarMask" in scene:
                for Zone in bpy.data.collections:
                    if "Zone ID" in Zone:
                        print(Zone.name)
                        val = Zone.name
                        #bpy.context.window.scene = bpy.data.scenes[scene.name]
                        try:
                            LayerDisplay(val)
                        except:
                            print("bla")
        return {'FINISHED'}

class GalaxyMapOperator8(bpy.types.Operator):
   """Export mission settings and zone list information"""
   bl_idname = "objecthihi.galaxymap_operator8" 
   bl_label = "Export Scenario Info" 
   def execute(self, context):
        WiiExplorerPathFolder = bpy.context.workspace["WiiExplorer Folder Path"]
        GalaxyFilesystem = bpy.context.workspace["StageData Folder Path"]
        
        
        
        ## GalaxyInfo
        for col in bpy.data.collections:
            if "Zone ID" in col:
                if col["Zone ID"] == 0:
                    GalaxyMapName = col.name
                    if col["World Number"] == 0:
                        print("GLE Map. Nichts machen!")
                        GLEGalaxyInfo = True
                    else:
                        WorldNo = col["World Number"]
                        GLEGalaxyInfo = False
        
        if GLEGalaxyInfo == False:
            CSVheadings = "WorldNo:Int:0"
            os.popen(("mkdir ") + (bpy.path.abspath('//05_MapExport\\'))+GalaxyMapName+str('Scenario\\')).read() # Ordnerstruktur erstellen
            blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+GalaxyMapName+'Scenario\\GalaxyInfo.bcsv','w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)
            blenderCipher.write(CSVheadings) #Die Headings hinzufuegen
            
            blenderCipher.write('\n'+str(WorldNo)) #Schreibe Code in die CSV
            blenderCipher.close() #CSV Datei schliessen

            #Wandle CSV zu BCSV
            import subprocess
            os.popen(("pyjmap tojmap smg ") + (bpy.path.abspath('//05_MapExport\\')+GalaxyMapName+'Scenario\\GalaxyInfo.bcsv ') + (bpy.path.abspath('//05_MapExport\\')+GalaxyMapName+'Scenario\\GalaxyInfo.bcsv'))
        
        # if GLEGalaxyInfo == False:
        
        
        ##### Zone List ########
        
        CSVheadings = "ZoneName:String:0"
        os.popen(("mkdir ") + (bpy.path.abspath('//05_MapExport\\'))+GalaxyMapName+str('Scenario\\')).read() # Ordnerstruktur erstellen
        blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+GalaxyMapName+'Scenario\\ZoneList.bcsv','w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)
        blenderCipher.write(CSVheadings) #Die Headings hinzufuegen
        
        ##Zonen in richtiger Reihenfolge ( anhand Zone ID) in die Liste stopfen
        ZoneList = []
        ZoneCounter = 0
        for col in bpy.data.collections:
            if "Zone ID" in col:
                ZoneCounter = ZoneCounter + 1
        ZoneCounter2 = 0
        for x in range(ZoneCounter):
            for col in bpy.data.collections:
                if "Zone ID" in col:
                    if col["Zone ID"] == ZoneCounter2:
                        ZoneCounter2 = ZoneCounter2 + 1
                        ZoneList.append(col.name)
        
        for ZoneListName in ZoneList:

            #Baue CSV Code zusammen:
            OBJEKTCODE = str(ZoneListName)
            blenderCipher.write('\n'+OBJEKTCODE) #Schreibe Code in die CSV
        
        blenderCipher.close() #CSV Datei schliessen
        
        #Wandle CSV zu BCSV
        import subprocess
        os.popen(("pyjmap tojmap smg ") + (bpy.path.abspath('//05_MapExport\\')+GalaxyMapName+'Scenario\\ZoneList.bcsv ') + (bpy.path.abspath('//05_MapExport\\')+GalaxyMapName+'Scenario\\ZoneList.bcsv'))
        
        
        #### ScenarioData.bcsv ##############
        
        ScenarioList = []
        ScenarioCounter = 0
        # for scene in bpy.data.scenes:
            # #print(scene.name)
            # if "ScenarioNo" in scene:
                # #print(scene["Test"])
                # ScenarioCounter = ScenarioCounter + 1
        scene = bpy.context.scene
        for view_layer in scene.view_layers:
            print(f"View Layer: {view_layer.name}")
            if "ScenarioNo" in view_layer:
                print(f"  ScenarioNo: {view_layer['ScenarioNo']}")
                ScenarioCounter = ScenarioCounter + 1


        ## Headings, mit Zonennamen hinzufugen
        os.popen(("mkdir ") + (bpy.path.abspath('//05_MapExport\\'))+GalaxyMapName+str('Scenario\\')).read() # Ordnerstruktur erstellen
        blenderCipher=open(bpy.path.abspath('//05_MapExport\\')+GalaxyMapName+'Scenario\\ScenarioData.bcsv','w') # Text Datei erstellen und oeffnen (ueberschreibt es auch)
        
        CSVheadings = "ScenarioNo:Int:0,ScenarioName:String:0,PowerStarId:Int:0,AppearPowerStarObj:String:0,PowerStarType:String:0,Comet:String:0,CometLimitTimer:Int:0,LuigiModeTimer:Int:0"
        blenderCipher.write(CSVheadings) #Die Headings hinzufuegen
        
        for ZoneListName in ZoneList:
            blenderCipher.write(','+ZoneListName+":Int:0") #Schreibe Code in die CSV
            

        ScenarioCounter2 = 1
        GLE_PowerStarColorCheck = 0
        
        scene = bpy.context.scene
        for x in range(ScenarioCounter):
            for view_layer in scene.view_layers:
                if "ScenarioNo" in view_layer:
                    if view_layer["ScenarioNo"] == ScenarioCounter2:
                        ScenarioID = view_layer["ScenarioNo"]
                        ScenarioName = view_layer["ScenarioName"]
                        PowerStarType = view_layer["Scenario Type"]
                        StarMask = view_layer["StarMask"]
                        ####Todo kein starmask sondern auswahl, bwz boolean array
                        AppearPowerStarObj = view_layer["Power Star Trigger"]
                        Comet = view_layer["Comet"]
                        CometLimitTimer = view_layer["Comet Time Limit"]
                        LuigiModeTimer = view_layer["LuigiModeTimer (unused)"]
                        try: #GLE
                            PowerStarColor = view_layer["Power Star Color"]
                            PowerStarColor = "," + str(PowerStarColor)
                            if not GLE_PowerStarColorCheck == 0:
                                blenderCipher.write(',PowerStarColor:Int:0')
                                GLE_PowerStarColorCheck = GLE_PowerStarColorCheck + 1
                        except:
                            PowerStarColor = ""
                        
                        ### Temporare PyMap Bug Loesung. Einziges Problem: Stern nicht normal im Scenario Select da. Geht trotzdem mit Level-Select Patch
                        if Comet == "":
                            Comet = " "
                        if AppearPowerStarObj == "":
                            AppearPowerStarObj = " "
                        
                        
                        
                        
                        blenderCipher.write('\n'+str(ScenarioID) + "," + str(ScenarioName) + "," + str(StarMask) + "," + str(AppearPowerStarObj) + "," + str(PowerStarType) + "," + str(Comet) + "," + str(CometLimitTimer) + "," + str(LuigiModeTimer))

                        for ZoneListName in ZoneList:
                            blenderCipher.write(','+view_layer[ZoneListName])
                        
                        ScenarioCounter2 = ScenarioCounter2 + 1

        blenderCipher.close() #CSV Datei schliessen

        #Wandle CSV zu BCSV
        import subprocess
        os.popen(("pyjmap tojmap smg ") + (bpy.path.abspath('//05_MapExport\\')+GalaxyMapName+'Scenario\\ScenarioData.bcsv ') + (bpy.path.abspath('//05_MapExport\\')+GalaxyMapName+'Scenario\\ScenarioData.bcsv'))
        
        
        
        ScenarioArcPack(GalaxyMapName, WiiExplorerPathFolder, GalaxyFilesystem)
        
        
        #ArcPack(context) #
        self.report({'INFO'}, "Scenario exported!")
        return {'FINISHED'}
   
class GalaxyMapOperator9(bpy.types.Operator):
   """Create brandnew galaxy. Only use this if nothing is present in your Blender file"""
   bl_idname = "objectbla.galaxymap_operator9" 
   bl_label = "Create brandnew galaxy" 
   def execute(self, context):
        GalaxyMapName = "NewGalaxy"
        ZonenName = GalaxyMapName
        
        #bpy.ops.scene.new(type='LINK_COPY')
        
        bpy.ops.scene.new(type='NEW')
        scene = bpy.context.scene
        
        #bpy.context.scene.name = "[1] New Scenario" #nur name
        
        NewLayerName = "NewScenario"
        
        #bpy.context.window.view_layer = bpy.context.scene.view_layers[NewLayerName]
        
        
        ScenarioID = 1
        ZoneID = 0
        ZonenName = bpy.context.workspace["Galaxy Name"]
        ZonenCreate(ZonenName, ZoneID)
        
        #NewLayerName = "[" + str(ScenarioID) + "] " + str(ScenarioName)
        
        bpy.context.scene.view_layers["ViewLayer"].name = NewLayerName

        
        bpy.context.scene.view_layers[NewLayerName]["StarMask"] = 0
        bpy.context.scene.view_layers[NewLayerName]["ScenarioNo"] = 1
        bpy.context.scene.view_layers[NewLayerName]["ScenarioName"] = "New Scenario"
        bpy.context.scene.view_layers[NewLayerName]["Scenario Type"] = "Normal" #Scenario typ, also ob grun oder hidden
        bpy.context.scene.view_layers[NewLayerName]["Power Star Trigger"] = ""
        bpy.context.scene.view_layers[NewLayerName]["Comet"] = ""
        bpy.context.scene.view_layers[NewLayerName]["Comet Time Limit"] = 0 #In Sekunden
        bpy.context.scene.view_layers[NewLayerName]["LuigiModeTimer (unused)"] = 0
        
        #bpy.context.scene.view_layers[NewLayerName][val] = LayerMask
        

        bpy.data.collections[ZonenName]["Zone ID"] = 0
        bpy.data.collections[ZonenName]["World Number"] = 1
        
        self.report({'INFO'}, "Galaxy "+GalaxyMapName+" created!")
        return {'FINISHED'}
    
    
    
class GalaxyMapOperator10(bpy.types.Operator):
   """Create new scenario/mission"""
   bl_idname = "objectbob.galaxymap_operator10" 
   bl_label = "Create new scenario" 
   def execute(self, context):        

        ScenarioCount = 1
        
        scene = bpy.context.scene
        for view_layer in scene.view_layers:
            if "ScenarioNo" in view_layer:
                ScenarioCount = ScenarioCount + 1
                #scene[GalaxyMapName] = 0 #Star Mask add
        
        #bpy.ops.scene.new(type='LINK_COPY')
        #bpy.context.scene.name = "[1] New Scenario" #nur name
        NewLayerName = "[" + str(ScenarioCount) + "] New Scenario"
        if NewLayerName not in bpy.context.scene.view_layers:
            TheNewLayer = bpy.context.scene.view_layers.new(name=NewLayerName)
            print(f"Neuer View Layer '{NewLayerName}' wurde erstellt.")
        else:
            print(f"View Layer '{NewLayerName}' existiert bereits.")
        
        bpy.context.window.view_layer = bpy.context.scene.view_layers[NewLayerName] #neuen Layer als den aktiven machen
        
        bpy.context.scene.view_layers[NewLayerName]["StarMask"] = 0
        bpy.context.scene.view_layers[NewLayerName]["ScenarioNo"] = ScenarioCount
        bpy.context.scene.view_layers[NewLayerName]["ScenarioName"] = "New Scenario"
        bpy.context.scene.view_layers[NewLayerName]["Scenario Type"] = "Normal" #Scenario typ, also ob grun oder hidden
        bpy.context.scene.view_layers[NewLayerName]["Power Star Trigger"] = ""
        bpy.context.scene.view_layers[NewLayerName]["Comet"] = ""
        bpy.context.scene.view_layers[NewLayerName]["Comet Time Limit"] = 0 #In Sekunden
        bpy.context.scene.view_layers[NewLayerName]["LuigiModeTimer (unused)"] = 0
        
        for Zone in bpy.data.collections:
            if "Zone ID" in Zone:
                bpy.context.scene.view_layers[NewLayerName][Zone.name] = "0"
        
        #bpy.data.collections[ZonenName]["Zone ID"] = 0
        #bpy.data.collections[ZonenName]["World Number"] = 1
        
        self.report({'INFO'}, 'Mission "'+NewLayerName+'" created!')
        return {'FINISHED'}


### ADDING OBJECTS

class GalaxyMapOperator11(bpy.types.Operator): #Normal Object info apply
   """Add required properties for general object"""
   bl_idname = "objecthuhuh.galaxymap_operator11" 
   bl_label = "Normal Object" 
   def execute(self, context):
        #bpy.context.object["Object Name"] = ""
        bpy.context.object["Link ID"] = 0
        bpy.context.object["Obj_Arg0"] = -1
        bpy.context.object["Obj_Arg1"] = -1
        bpy.context.object["Obj_Arg2"] = -1
        bpy.context.object["Obj_Arg3"] = -1
        bpy.context.object["Obj_Arg4"] = -1
        bpy.context.object["Obj_Arg5"] = -1
        bpy.context.object["Obj_Arg6"] = -1
        bpy.context.object["Obj_Arg7"] = -1
        bpy.context.object["Camera Set ID"] = -1
        bpy.context.object["SW_APPEAR"] = -1
        bpy.context.object["SW_DEAD"] = -1
        bpy.context.object["SW_A"] = -1
        bpy.context.object["SW_B"] = -1
        bpy.context.object["SW_AWAKE"] = -1
        bpy.context.object["SW_PARAM"] = -1
        bpy.context.object["Message ID"] = -2
        bpy.context.object["Speed Scale"] = 1
        bpy.context.object["Cast Group ID"] = -1
        bpy.context.object["View Group ID"] = -1
        bpy.context.object["Model ID"] = -1
        bpy.context.object["Path ID"] = -1
        bpy.context.object["Clipping Group ID"] = -1
        bpy.context.object["Group ID"] = -1
        bpy.context.object["Cutscene Group ID"] = -1
        bpy.context.object["Linked MapParts ID"] = -1
        bpy.context.object["Linked Object ID"] = -1
        bpy.context.object["Generator Object ID"] = -1
        bpy.context.object["Layer"] = "Common"
        
        bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
        
        return {'FINISHED'}
    

class GalaxyMapOperator12(bpy.types.Operator): #MapPart Object info apply
   """Add required properties for MapPart"""
   bl_idname = "objectheyheyhey.galaxymap_operator12" 
   bl_label = "MapPart Object" 
   def execute(self, context):
        #bpy.context.object["Object Name"] = ""
        bpy.context.object["Link ID"] = -1
        bpy.context.object["MoveConditionType"] = 0
        bpy.context.object["RotateSpeed"] = 0
        bpy.context.object["RotateAngle"] = 0
        bpy.context.object["RotateAxis"] = 0
        bpy.context.object["RotateAccelType"] = 0
        bpy.context.object["RotateStopTime"] = 0
        bpy.context.object["RotateType"] = 0
        bpy.context.object["ShadowType"] = 0
        bpy.context.object["SignMotionType"] = 0
        bpy.context.object["PressType"] = 0
        bpy.context.object["Speed Scale"] = 1
        bpy.context.object["Camera Set ID"] = -1
        bpy.context.object["Far Clip"] = -1
        
        bpy.context.object["Obj_Arg0"] = -1
        bpy.context.object["Obj_Arg1"] = -1
        bpy.context.object["Obj_Arg2"] = -1
        bpy.context.object["Obj_Arg3"] = -1
        
        bpy.context.object["SW_APPEAR"] = -1
        bpy.context.object["SW_DEAD"] = -1
        bpy.context.object["SW_A"] = -1
        bpy.context.object["SW_B"] = -1
        bpy.context.object["SW_AWAKE"] = -1
        bpy.context.object["SW_PARAM"] = -1
        
        bpy.context.object["Cast Group ID"] = -1
        bpy.context.object["View Group ID"] = -1
        bpy.context.object["Model ID"] = -1
        bpy.context.object["Path ID"] = -1
        bpy.context.object["Clipping Group ID"] = -1
        bpy.context.object["Group ID"] = -1
        bpy.context.object["Cutscene Group ID"] = -1
        bpy.context.object["Linked MapParts ID"] = -1
        bpy.context.object["Linked Object ID"] = -1
        bpy.context.object["Parent Object ID"] = -1

        bpy.context.object["Layer"] = "Common"
        
        bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
        return {'FINISHED'}



class WM_OT_myOp(bpy.types.Operator): #ADD Object?
   """Add required properties for MapPart"""
   bl_idname = "wm.myop" 
   bl_label = "Add Object" 
   
   def execute(self, context):
        text = bpy.props.StringProperty(name= "Enter Name", default= "")
        t = self.text
        #s = self.scale
        print(t)
        return {'FINISHED'}



class GalaxyMapAddObject(bpy.types.Operator): #ADD Object
    """Add Object to scene"""
    bl_idname = "galaxymap1.galaxyaddobj" 
    bl_label = "General" 



    def execute(self, context):
        
        
        AssetSearch = bpy.context.workspace["Asset Searching Enabled"]
        BlendFilesFolder = bpy.context.workspace["Workspace (for searching in Blend files)"]
        MapAssetBlendFile = bpy.context.workspace["Map Assets Blend file"]
        
        if bpy.context.workspace["Asset Searching Enabled"] == 0:
            AssetSearch = False
        else:
            AssetSearch = True
        #bpy.ops.wm.console_toggle() #Zum CMD Fenster springen. Geht manchmal eh net....
        #ObjektName = input("Enter Object Name: ")
        ObjektName = bpy.context.workspace["Add this object"]
        print(ObjektName)
        
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD')
        
        bpy.context.view_layer.objects.active.name = ObjektName
        #bpy.context.object["Object Name"] = ObjektName
        bpy.context.object["Link ID"] = 0
        bpy.context.object["Obj_Arg0"] = -1
        bpy.context.object["Obj_Arg1"] = -1
        bpy.context.object["Obj_Arg2"] = -1
        bpy.context.object["Obj_Arg3"] = -1
        bpy.context.object["Obj_Arg4"] = -1
        bpy.context.object["Obj_Arg5"] = -1
        bpy.context.object["Obj_Arg6"] = -1
        bpy.context.object["Obj_Arg7"] = -1
        bpy.context.object["Camera Set ID"] = -1
        bpy.context.object["SW_APPEAR"] = -1
        bpy.context.object["SW_DEAD"] = -1
        bpy.context.object["SW_A"] = -1
        bpy.context.object["SW_B"] = -1
        bpy.context.object["SW_AWAKE"] = -1
        bpy.context.object["SW_PARAM"] = -1
        bpy.context.object["Message ID"] = -2
        bpy.context.object["Speed Scale"] = 1
        bpy.context.object["Cast Group ID"] = -1
        bpy.context.object["View Group ID"] = -1
        bpy.context.object["Model ID"] = -1
        bpy.context.object["Path ID"] = -1
        bpy.context.object["Clipping Group ID"] = -1
        bpy.context.object["Group ID"] = -1
        bpy.context.object["Cutscene Group ID"] = -1
        bpy.context.object["Linked MapParts ID"] = -1
        bpy.context.object["Linked Object ID"] = -1
        bpy.context.object["Generator Object ID"] = -1
        bpy.context.object["Layer"] = "Common"
        
        bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
        
        if AssetSearch == True:
        
            try:
                bpy.context.object.instance_type = 'COLLECTION'
                bpy.context.object.instance_collection = bpy.data.collections[ObjektName]
            except:
                print("Asset nicht in aktiver Blenderdatei")
        
                ### WIP - Linke Assets von anderen Blender Dateien ###    
                ##Idee: Das weglassen, und stattdessen als separaten Button einbauen, um Objekten ohne Assets es dann hinzubla       
                
                from bpy.props import StringProperty, BoolProperty
                from pathlib import Path

                def get_glob_files(folder, suffix, recursive=True):
                    s = f'**/*{suffix}'  if recursive else f'*{suffix}'
                    return [str(fp) for fp in Path(folder).glob(s) if fp.is_file()]

                # test
                #folder_path = "C:\\SuperMarioGravity\\WORKSPACE\\01_Galaxien"
                folder_path = BlendFilesFolder
                print(get_glob_files(folder_path, '.blend'))
                #directory = folder_path
                for blend in get_glob_files(folder_path, '.blend'):
                    try:

                        # path to the blend
                        #filepath = (self.directory, '.blend') #Kann man auch Library statt Blend Datei durchsuchen?
                        filepath = blend
                        print("Lese von dieser Blend Datei:")
                        print(blend)
                        
                        if filepath == bpy.data.filepath:
                            print("Not allow load library from current file")
                            # Don't append current file, It will crash blender even the code inside the try:
                            #return
                        else:
                            # name of collection(s) to append or link
                            coll_name = ObjektName
                            # append, set to true to keep the link to the original file
                            link = True
                            # link all collections starting with 'objekttest'
                            with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                                data_to.collections = [c for c in data_from.collections if c.startswith(coll_name)]
                            # link collection to selected Empty
                            bpy.context.object.instance_type = 'COLLECTION'
                            bpy.context.object.instance_collection = bpy.data.collections[ObjektName]
                    except:
                        print("Dieses Asset wurde in der Library nicht gefunden:")
                        print(ObjektName)
                        pass
        
        
        

        if "Zone ID" in bpy.context.collection:
            ZoneID = bpy.context.collection["Zone ID"]
            ZonePrefix = "  (Z" + str(ZoneID) + ")"
            if ZoneID == 0:
                ZonePrefix = ""
            obj = bpy.context.active_object # Erstellte Obj is the active one
            bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
            bpy.data.collections['Objects' + ZonePrefix].objects.link(obj)# add it to our specific collection
        return {'FINISHED'}
    
    
class GalaxyMapAddMapPart(bpy.types.Operator): #ADD MapPart
   """Add MapPart to scene"""
   bl_idname = "galaxymap2.galaxyaddmappart" 
   bl_label = "Map Part" 
   def execute(self, context):
        AssetSearch = bpy.context.workspace["Asset Searching Enabled"]
        BlendFilesFolder = bpy.context.workspace["Workspace (for searching in Blend files)"]
        MapAssetBlendFile = bpy.context.workspace["Map Assets Blend file"]
        
        if bpy.context.workspace["Asset Searching Enabled"] == 0:
            AssetSearch = False
        else:
            AssetSearch = True
        
        #bpy.ops.wm.console_toggle() #Zum CMD Fenster springen. Geht manchmal eh net....
        #ObjektName = input("Enter Object Name: ")
        ObjektName = bpy.context.workspace["Add this object"]
        print(ObjektName)
        
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD')
        
        bpy.context.view_layer.objects.active.name = ObjektName
        #bpy.context.object["Object Name"] = ObjektName
        bpy.context.object["Link ID"] = -1
        bpy.context.object["MoveConditionType"] = 0
        bpy.context.object["RotateSpeed"] = 0
        bpy.context.object["RotateAngle"] = 0
        bpy.context.object["RotateAxis"] = 0
        bpy.context.object["RotateAccelType"] = 0
        bpy.context.object["RotateStopTime"] = 0
        bpy.context.object["RotateType"] = 0
        bpy.context.object["ShadowType"] = 0
        bpy.context.object["SignMotionType"] = 0
        bpy.context.object["PressType"] = 0
        bpy.context.object["Speed Scale"] = 1
        bpy.context.object["Camera Set ID"] = -1
        bpy.context.object["Far Clip"] = -1
        
        bpy.context.object["Obj_Arg0"] = -1
        bpy.context.object["Obj_Arg1"] = -1
        bpy.context.object["Obj_Arg2"] = -1
        bpy.context.object["Obj_Arg3"] = -1
        
        bpy.context.object["SW_APPEAR"] = -1
        bpy.context.object["SW_DEAD"] = -1
        bpy.context.object["SW_A"] = -1
        bpy.context.object["SW_B"] = -1
        bpy.context.object["SW_AWAKE"] = -1
        bpy.context.object["SW_PARAM"] = -1
        
        bpy.context.object["Cast Group ID"] = -1
        bpy.context.object["View Group ID"] = -1
        bpy.context.object["Model ID"] = -1
        bpy.context.object["Path ID"] = -1
        bpy.context.object["Clipping Group ID"] = -1
        bpy.context.object["Group ID"] = -1
        bpy.context.object["Cutscene Group ID"] = -1
        bpy.context.object["Linked MapParts ID"] = -1
        bpy.context.object["Linked Object ID"] = -1
        bpy.context.object["Parent Object ID"] = -1

        bpy.context.object["Layer"] = "Common"
        
        bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
        
        if AssetSearch == True:
            ### WIP - Linke Assets von anderen Blender Dateien ###    
            ##Idee: Das weglassen, und stattdessen als separaten Button einbauen, um Objekten ohne Assets es dann hinzubla       
            
            try:
                bpy.context.object.instance_type = 'COLLECTION'
                bpy.context.object.instance_collection = bpy.data.collections[ObjektName]
            except:
                print("Asset nicht in aktiver Blenderdatei")

                from bpy.props import StringProperty, BoolProperty
                from pathlib import Path

                def get_glob_files(folder, suffix, recursive=True):
                    s = f'**/*{suffix}'  if recursive else f'*{suffix}'
                    return [str(fp) for fp in Path(folder).glob(s) if fp.is_file()]

                # test
                #folder_path = "C:\\SuperMarioGravity\\WORKSPACE\\01_Galaxien"
                folder_path = BlendFilesFolder
                print(get_glob_files(folder_path, '.blend'))
                #directory = folder_path
                for blend in get_glob_files(folder_path, '.blend'):
                    try:

                        # path to the blend
                        #filepath = (self.directory, '.blend') #Kann man auch Library statt Blend Datei durchsuchen?
                        filepath = blend
                        print("Lese von dieser Blend Datei:")
                        print(blend)
                        
                        if filepath == bpy.data.filepath:
                            print("Not allow load library from current file")
                            # Don't append current file, It will crash blender even the code inside the try:
                            #return
                        else:
                            # name of collection(s) to append or link
                            coll_name = ObjektName
                            # append, set to true to keep the link to the original file
                            link = True
                            # link all collections starting with 'objekttest'
                            with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                                data_to.collections = [c for c in data_from.collections if c.startswith(coll_name)]
                            # link collection to selected Empty
                            bpy.context.object.instance_type = 'COLLECTION'
                            bpy.context.object.instance_collection = bpy.data.collections[ObjektName]
                    except:
                        print("Dieses Asset wurde in der Library nicht gefunden:")
                        print(ObjektName)
                        pass




        if "Zone ID" in bpy.context.collection:
            ZoneID = bpy.context.collection["Zone ID"]
            ZonePrefix = "  (Z" + str(ZoneID) + ")"
            if ZoneID == 0:
                ZonePrefix = ""
            obj = bpy.context.active_object # Erstellte Obj is the active one
            bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
            bpy.data.collections['MapParts' + ZonePrefix].objects.link(obj)# add it to our specific collection
        return {'FINISHED'}

def GalaxyMapAddGravity(ObjektName): #ADD Gravity
   # """Add Gravity to scene"""
   # bl_idname = "galaxymap3.galaxyaddgravity" 
   # bl_label = "Gravity" 
   # def execute(self, context):
    import bpy
    import math
    import csv
    import sys
    import os
    import shutil
    import subprocess
    C = bpy.context
    import struct
    import requests
    import os.path
    AssetSearch = bpy.context.workspace["Asset Searching Enabled"]
    BlendFilesFolder = bpy.context.workspace["Workspace (for searching in Blend files)"]
    MapAssetBlendFile = bpy.context.workspace["Map Assets Blend file"]
    
    # print("==========================")
    # ObjektName = input("Which Gravity type? \n 0 = Planar \n 1 = Sphere \n 2 = Cube \n 3 = Cylinder \n 4 = Disk \n 5 = Donut \n 6 = Cone \n 7 = Barrel \n 8 = Wire : ")
    
    # ObjektName = str(ObjektName) 
    
    if ObjektName == "0":
        ObjektName = "GlobalPlaneGravity"
    if ObjektName == "1":
        ObjektName = "GlobalPointGravity"
    if ObjektName == "2":
        ObjektName = "GlobalCubeGravity"
    if ObjektName == "3":
        ObjektName = "GlobalSegmentGravity"
    if ObjektName == "4":
        ObjektName = "GlobalDiskGravity"
    if ObjektName == "5":
        ObjektName = "GlobalDiskTorusGravity"
    if ObjektName == "6":
        ObjektName = "GlobalConeGravity"
    if ObjektName == "7":
        ObjektName = "GlobalBarrelGravity"
    if ObjektName == "8":
        ObjektName = "GlobalWireGravity"
    
    name = ObjektName
    
    bpy.ops.object.volume_add(align='WORLD')
    
    bpy.context.view_layer.objects.active.name = name
    #bpy.context.object["Object Name"] = name
    bpy.context.object["Link ID"] = 0
    
    bpy.context.object["Range"] = 500.0
    bpy.context.object["Distance"] = 0.0
    bpy.context.object["Priority"] = 0
    bpy.context.object["Inverse"] = -1
    bpy.context.object["Power"] = "Normal"
    bpy.context.object["Gravity_type"] = "Normal"
    bpy.context.object["SW_APPEAR"] = -1
    bpy.context.object["SW_DEAD"] = -1
    bpy.context.object["SW_A"] = -1
    bpy.context.object["SW_B"] = -1
    bpy.context.object["SW_AWAKE"] = -1
    
    bpy.context.object["Linked Area ID"] = -1
    bpy.context.object["Path ID"] = -1
    bpy.context.object["Clipping Group ID"] = -1
    bpy.context.object["Group ID"] = -1
    bpy.context.object["Cutscene Group ID"] = -1
    bpy.context.object["Linked MapParts ID"] = -1
    bpy.context.object["Linked Object ID"] = -1
    
    bpy.context.object["Layer"] = "Common"
    
    bpy.context.object.lock_scale[0] = True
    bpy.context.object.lock_scale[1] = True
    bpy.context.object.lock_scale[2] = True

    bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
    
    Obj_arg0 = -1
    Obj_arg1 = -1
    Obj_arg2 = -1
    Obj_arg3 = -1
    
    CommonPath_ID = -1
    
    #############################################
    #Geometry Node linken. Komplizierter Dreck
    
    obj = bpy.context.object #geht das so
    #file_path = "C:\\SuperMarioGravity\\WORKSPACE\\04_Library\\GravityTypes.blend"
    file_path = MapAssetBlendFile
    
    Gravity_type = name
    
    node_name = Gravity_type #"GlobalCubeGravity" #test
    
    
    if Gravity_type == "GlobalPlaneGravityInBox":
        node_name = "GlobalPlaneGravity"
        
    if Gravity_type == "GlobalPlaneGravityInCylinder":
        node_name = "GlobalPlaneGravity"
    
    if Gravity_type == "ZeroGravityBox":
        node_name = "GlobalPlaneGravity"
        
    if Gravity_type == "ZeroGravityCylinder":
        node_name = "GlobalPlaneGravity"
        
    if Gravity_type == "ZeroGravitySphere":
        node_name = "GlobalPlaneGravity"
        
    
    link = True
    
    from os.path import join as os_path_join

    inner_path = "NodeTree"
    node_groups = bpy.data.node_groups


    bpy.ops.wm.append(
        filepath=os_path_join(file_path, inner_path, node_name),
        directory=os_path_join(file_path, inner_path),
        filename=node_name,
        link=link)


    #modifier=bpy.context.object.modifiers.new("GRAVITY", "NODES")
    #modifier=bpy.context.view_layer.objects.active.modifiers.new(type='NODES')
    
    #bpy.context.object.modifiers.new(type='NODES')
    #bpy.context.object.modifiers["GeometryNodes"].name = "GRAVITY"
    #bpy.context.object.modifiers["GRAVITY"].node_group = Gravity_type
    
    modifier=bpy.context.object.modifiers.new("GRAVITY", "NODES")
    
    try:
        modifier.node_group = bpy.data.node_groups[node_name]
    except:
        modifier.node_group = bpy.data.node_groups["GlobalPlaneGravity"] #Falls es nen ungueltigen Objektnamen nutzt
    

    bpy.context.object.modifiers["GRAVITY"]["Input_2"] = float(500)

        
        
    #########################################################
    
    if "Zone ID" in bpy.context.collection:
        ZoneID = bpy.context.collection["Zone ID"]
        ZonePrefix = "  (Z" + str(ZoneID) + ")"
        if ZoneID == 0:
            ZonePrefix = ""
        obj = bpy.context.active_object # Erstellte Obj is the active one
        bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
        bpy.data.collections['Gravities' + ZonePrefix].objects.link(obj)# add it to our specific collection
        
        
        #return {'FINISHED'}

class GalaxyMapAddArea(bpy.types.Operator): 
   """Add Area to scene"""
   bl_idname = "galaxymap4.galaxyaddarea" 
   bl_label = "Area" 
   def execute(self, context):
        AssetSearch = bpy.context.workspace["Asset Searching Enabled"]
        BlendFilesFolder = bpy.context.workspace["Workspace (for searching in Blend files)"]
        MapAssetBlendFile = bpy.context.workspace["Map Assets Blend file"]
        
        #bpy.ops.wm.console_toggle() #Zum CMD Fenster springen. Geht manchmal eh net....
        #name = input("Enter Object Name: ")
        name = bpy.context.workspace["Add this object"]
        print(name)
        
        #AreaShapeNo = input("Enter Shape Form: ")
        AreaShapeNo = '0'
        print(name)
        
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD')

        bpy.context.view_layer.objects.active.name = name
        #bpy.context.object["Object Name"] = name
        bpy.context.object["Link ID"] = -1
        bpy.context.object["Obj_Arg0"] = -1
        bpy.context.object["Obj_Arg1"] = -1
        bpy.context.object["Obj_Arg2"] = -1
        bpy.context.object["Obj_Arg3"] = -1
        bpy.context.object["Obj_Arg4"] = -1
        bpy.context.object["Obj_Arg5"] = -1
        bpy.context.object["Obj_Arg6"] = -1
        bpy.context.object["Obj_Arg7"] = -1
        bpy.context.object["Priority"] = 0
        bpy.context.object["SW_APPEAR"] = -1
        bpy.context.object["SW_A"] = -1
        bpy.context.object["SW_B"] = -1
        bpy.context.object["SW_AWAKE"] = -1
        
        bpy.context.object["Linked Area ID"] = -1
        #bpy.context.object["Shape ID"] = AreaShapeNo
        bpy.context.object["Path ID"] = -1
        bpy.context.object["Clipping Group ID"] = -1
        bpy.context.object["Group ID"] = -1
        bpy.context.object["Cutscene Group ID"] = -1
        bpy.context.object["Linked MapParts ID"] = -1
        bpy.context.object["Linked Object ID"] = -1
        
        bpy.context.object["Layer"] = "Common"
        
        bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
        
        ########################################### COLLECTION LINK
        
        try:

            if AreaShapeNo == '0':
                AreaShapeCOL = "AreaShape 0  Cube" #Dem Emtpy eine Collection Instanz zuweisen
            if AreaShapeNo == '1':
                AreaShapeCOL = "AreaShape 1  Cube Middle" #Dem Emtpy eine Collection Instanz zuweisen    
            if AreaShapeNo == '2':
                AreaShapeCOL = "AreaShape 2  Sphere" #Dem Emtpy eine Collection Instanz zuweisen
            if AreaShapeNo == '3':
                AreaShapeCOL = "AreaShape 3  Cylinder" #Dem Emtpy eine Collection Instanz zuweisen
            if AreaShapeNo == '4':
                AreaShapeCOL = "AreaShape 4  Half Sphere" #Dem Emtpy eine Collection Instanz zuweisen

            #folder = bpy.path.abspath("//")

            # get all blend files in the folder
            #blends = [f for f in os.listdir(folder) if f.endswith(".blend")]

            #for blend in blends:

            # path to the blend
            filepath = MapAssetBlendFile
            # name of collection(s) to append or link
            coll_name = AreaShapeCOL #FIX oder
            # append, set to true to keep the link to the original file
            link = True
            # link all collections lose an die Blenderdatei
            with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 0  Cube")]
            
            with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 1  Cube Middle")]
            
            with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 2  Sphere")]
                
            with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 3  Cylinder")]
                
            with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 4  Half Sphere")]
                
            # link collection to selected Empty
            bpy.context.object.instance_type = 'COLLECTION'
            bpy.context.object.instance_collection = bpy.data.collections[AreaShapeCOL]
            

            
        except:
            print("KEIN ZUGRIFF AUF DIE BLEND DATEI")
            print(name)
            pass
        
        #################################  COLLECTION LINK END
        
        if "Zone ID" in bpy.context.collection:
            ZoneID = bpy.context.collection["Zone ID"]
            ZonePrefix = "  (Z" + str(ZoneID) + ")"
            if ZoneID == 0:
                ZonePrefix = ""
            obj = bpy.context.active_object # Erstellte Obj is the active one
            bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
            bpy.data.collections['Areas' + ZonePrefix].objects.link(obj)# add it to our specific collection
        
        return {'FINISHED'}

class GalaxyMapAddCamera(bpy.types.Operator): 
   """Add Camera to scene"""
   bl_idname = "galaxymap5.galaxyaddcamera" 
   bl_label = "Camera Area" 
   def execute(self, context):
        AssetSearch = bpy.context.workspace["Asset Searching Enabled"]
        BlendFilesFolder = bpy.context.workspace["Workspace (for searching in Blend files)"]
        MapAssetBlendFile = bpy.context.workspace["Map Assets Blend file"]
        
        
        name = "CameraArea"
        
        #AreaShapeNo = input("Enter Shape Form: ")
        AreaShapeNo = '0'
        
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD')
        
        bpy.context.object.instance_type = 'COLLECTION'

        bpy.context.view_layer.objects.active.name = name
        #bpy.context.object["Object Name"] = name
        bpy.context.object["Link ID"] = 0
        bpy.context.object["Camera ID"] = 0
        bpy.context.object["Obj_Arg1"] = -1
        bpy.context.object["Priority"] = 0
        bpy.context.object["Affected Contexts"] = -1
        bpy.context.object["Interpolate In (Unused)"] = 0
        bpy.context.object["Interpolate Out (Unused)"] = 0
        bpy.context.object["SW_APPEAR"] = -1
        bpy.context.object["SW_A"] = -1
        bpy.context.object["SW_B"] = -1
        bpy.context.object["SW_AWAKE"] = -1
        bpy.context.object["Validity"] = "Valid"
        bpy.context.object["Linked Area ID"] = -1
        #bpy.context.object["Shape ID"] = AreaShapeNo
        bpy.context.object["Linked MapParts ID"] = -1
        bpy.context.object["Linked Object ID"] = -1
        
        bpy.context.object["Layer"] = "Common"
        
        bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
        
        ########################################### COLLECTION LINK
        
        try:

            if AreaShapeNo == '0':
                AreaShapeCOL = "AreaShape 0  Cube" #Dem Emtpy eine Collection Instanz zuweisen
            if AreaShapeNo == '1':
                AreaShapeCOL = "AreaShape 1  Cube Middle" #Dem Emtpy eine Collection Instanz zuweisen    
            if AreaShapeNo == '2':
                AreaShapeCOL = "AreaShape 2  Sphere" #Dem Emtpy eine Collection Instanz zuweisen
            if AreaShapeNo == '3':
                AreaShapeCOL = "AreaShape 3  Cylinder" #Dem Emtpy eine Collection Instanz zuweisen
            if AreaShapeNo == '4':
                AreaShapeCOL = "AreaShape 4  Half Sphere" #Dem Emtpy eine Collection Instanz zuweisen

            #folder = bpy.path.abspath("//")

            # get all blend files in the folder
            #blends = [f for f in os.listdir(folder) if f.endswith(".blend")]

            #for blend in blends:

            # path to the blend
            filepath = MapAssetBlendFile
            # name of collection(s) to append or link
            coll_name = AreaShapeCOL #FIX oder
            # append, set to true to keep the link to the original file
            link = True
            # link all collections lose an die Blenderdatei
            with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 0  Cube")]
            
            with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 1  Cube Middle")]
            
            with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 2  Sphere")]
                
            with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 3  Cylinder")]
                
            with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
                data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 4  Half Sphere")]
                
            # link collection to selected Empty
            bpy.context.object.instance_type = 'COLLECTION'
            bpy.context.object.instance_collection = bpy.data.collections[AreaShapeCOL]
            

            
        except:
            print("KEIN ZUGRIFF AUF DIE BLEND DATEI")
            print(name)
            pass
        
        #################################  COLLECTION LINK END
        
        if "Zone ID" in bpy.context.collection:
            ZoneID = bpy.context.collection["Zone ID"]
            ZonePrefix = "  (Z" + str(ZoneID) + ")"
            if ZoneID == 0:
                ZonePrefix = ""
            obj = bpy.context.active_object # Erstellte Obj is the active one
            bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
            bpy.data.collections['Cameras' + ZonePrefix].objects.link(obj)# add it to our specific collection
        
        return {'FINISHED'}

class GalaxyMapAddStart(bpy.types.Operator): 
   """Add Spawn to scene"""
   bl_idname = "galaxymap6.galaxyaddstart" 
   bl_label = "Spawn" 
   def execute(self, context):
        AssetSearch = bpy.context.workspace["Asset Searching Enabled"]
        BlendFilesFolder = bpy.context.workspace["Workspace (for searching in Blend files)"]
        MapAssetBlendFile = bpy.context.workspace["Map Assets Blend file"]
        
        if bpy.context.workspace["Asset Searching Enabled"] == 0:
            AssetSearch = False
        else:
            AssetSearch = True
        
        name = "Mario"
        
        bpy.ops.object.empty_add(type='PLAIN_AXES', radius=100, align='WORLD')
        
        bpy.context.view_layer.objects.active.name = name
        #bpy.context.object["Object Name"] = name  #Nee, soll eh immer "Mario" sein
        bpy.context.object["Spawn ID"] = 0
        bpy.context.object["Entrance Type"] = -1
        bpy.context.object["Camera ID"] = -1
                    
        bpy.context.object["Layer"] = "Common"
        
        bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
        
        if "Zone ID" in bpy.context.collection:
            ZoneID = bpy.context.collection["Zone ID"]
            ZonePrefix = "  (Z" + str(ZoneID) + ")"
            if ZoneID == 0:
                ZonePrefix = ""
            obj = bpy.context.active_object # Erstellte Obj is the active one
            bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
            bpy.data.collections['Spawns' + ZonePrefix].objects.link(obj)# add it to our specific collection
        
        return {'FINISHED'}

def GalaxyMapAddCutscene(name): 
   # """Add Cutscene Object to scene"""
   # bl_idname = "galaxymap7.galaxyaddcutscene" 
   # bl_label = "Cutscene" 
   # def execute(self, context):
    #AssetSearch = bpy.context.workspace["Asset Searching Enabled"]
    #BlendFilesFolder = bpy.context.workspace["Workspace (for searching in Blend files)"]
    #MapAssetBlendFile = bpy.context.workspace["Map Assets Blend file"]
    
    
    #name = input("Cutscene (0) or CutsceneCast (1)?: ")
    
    if name == "0":
        name = "DemoGroup"
    else:
        name = "DemoSubGroup"
    
    bpy.ops.object.empty_add(type='CUBE', radius=50, align='WORLD')
    
    bpy.context.view_layer.objects.active.name = name
    #bpy.context.object["Object Name"] = ""
    
    bpy.context.object["Cutscene Name"] = "YourDemo"
    bpy.context.object["Sheet Name"] = "YourDemo"
    bpy.context.object["Link ID"] = 0
    bpy.context.object["SW_APPEAR"] = -1
    bpy.context.object["SW_DEAD"] = -1
    bpy.context.object["SW_A"] = -1
    bpy.context.object["SW_B"] = -1
    bpy.context.object["Skippable"] = -1
    
    bpy.context.object["Layer"] = "Common"
    
    bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
    
    if "Zone ID" in bpy.context.collection:
        ZoneID = bpy.context.collection["Zone ID"]
        ZonePrefix = "  (Z" + str(ZoneID) + ")"
        if ZoneID == 0:
            ZonePrefix = ""
        obj = bpy.context.active_object # Erstellte Obj is the active one
        bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
        bpy.data.collections['Cutscenes' + ZonePrefix].objects.link(obj)# add it to our specific collection
        
        #return {'FINISHED'}

class GalaxyMapAddPosition(bpy.types.Operator): 
   """Add Misc Position to scene"""
   bl_idname = "galaxymap8.galaxyaddposition" 
   bl_label = "Position" 
   def execute(self, context):
        #AssetSearch = bpy.context.workspace["Asset Searching Enabled"]
        #BlendFilesFolder = bpy.context.workspace["Workspace (for searching in Blend files)"]
        #MapAssetBlendFile = bpy.context.workspace["Map Assets Blend file"]
        
        
        #ObjektName = input("Enter Object Name: ")
        #print(ObjektName)
        
        bpy.ops.object.empty_add(type='SINGLE_ARROW', radius=50, align='WORLD')
        
        bpy.context.view_layer.objects.active.name = "GeneralPos"
        #bpy.context.object["Object Name"] = ""
        bpy.context.object["Linked Object ID"] = -1
        bpy.context.object["Position Name"] = "Undefined"
                    
        bpy.context.object["Layer"] = "Common"
        
        bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
        
        if "Zone ID" in bpy.context.collection:
            ZoneID = bpy.context.collection["Zone ID"]
            ZonePrefix = "  (Z" + str(ZoneID) + ")"
            if ZoneID == 0:
                ZonePrefix = ""
            obj = bpy.context.active_object # Erstellte Obj is the active one
            bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
            bpy.data.collections['Positions' + ZonePrefix].objects.link(obj)# add it to our specific collection
        
        return {'FINISHED'}

class GalaxyMapAddDebug(bpy.types.Operator): 
   """Add unused Debug object to scene"""
   bl_idname = "galaxymap9.galaxyadddebug" 
   bl_label = "Debug" 
   def execute(self, context):
        AssetSearch = bpy.context.workspace["Asset Searching Enabled"]
        BlendFilesFolder = bpy.context.workspace["Workspace (for searching in Blend files)"]
        MapAssetBlendFile = bpy.context.workspace["Map Assets Blend file"]
        
        if bpy.context.workspace["Asset Searching Enabled"] == 0:
            AssetSearch = False
        else:
            AssetSearch = True
        
        
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD')
        
        bpy.context.view_layer.objects.active.name = "DebugMovePos"
        #bpy.context.object["Object Name"] = ""
        bpy.context.object["Link ID"] = 0
                    
        bpy.context.object["Layer"] = "Common"
        
        bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
        
        if "Zone ID" in bpy.context.collection:
            ZoneID = bpy.context.collection["Zone ID"]
            ZonePrefix = "  (Z" + str(ZoneID) + ")"
            if ZoneID == 0:
                ZonePrefix = ""
            obj = bpy.context.active_object # Erstellte Obj is the active one
            bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
            bpy.data.collections['Debug' + ZonePrefix].objects.link(obj)# add it to our specific collection
        
        return {'FINISHED'}

class GalaxyMapAddPath(bpy.types.Operator): 
   """Add Path to scene"""
   bl_idname = "galaxymap10.galaxyaddpath" 
   bl_label = "Path" 
   def execute(self, context):
        AssetSearch = bpy.context.workspace["Asset Searching Enabled"]
        BlendFilesFolder = bpy.context.workspace["Workspace (for searching in Blend files)"]
        MapAssetBlendFile = bpy.context.workspace["Map Assets Blend file"]
        
        if bpy.context.workspace["Asset Searching Enabled"] == 0:
            AssetSearch = False
        else:
            AssetSearch = True
        
        bpy.ops.curve.primitive_bezier_curve_add(radius=1, enter_editmode=False, align='WORLD')
        
        bpy.context.object.data.name = str("X") #Pfad ID
        
        
        bpy.context.view_layer.objects.active.name = "GalaxyPath"
        bpy.context.object["Name Alternative"] = ""
        bpy.context.object["PathArg0 (Posture Type)"] = -1
        bpy.context.object["PathArg1 (Stop Motion Type)"] = -1
        bpy.context.object["PathArg2 (Guide Type)"] = -1
        bpy.context.object["PathArg3"] = -1
        bpy.context.object["PathArg4 (Initial Position Type)"] = -1
        bpy.context.object["PathArg5"] = -1
        bpy.context.object["PathArg6"] = -1
        bpy.context.object["PathArg7"] = -1
        bpy.context.object["Usage"] = "General"
        
        bpy.context.object.rotation_mode = 'XZY' #Richtiger Rotationsmodus
        
        if "Zone ID" in bpy.context.collection:
            ZoneID = bpy.context.collection["Zone ID"]
            ZonePrefix = "  (Z" + str(ZoneID) + ")"
            if ZoneID == 0:
                ZonePrefix = ""
                
            bpy.context.object.data.name = str("X"+ZonePrefix) #Pfad ID
            obj = bpy.context.active_object # Erstellte Obj is the active one
            bpy.ops.collection.objects_remove_all()# Remove object from all collections not used in a scene
            bpy.data.collections['Paths' + ZonePrefix].objects.link(obj)# add it to our specific collection
        
        return {'FINISHED'}

def GalaxyMapChangeAreaShape(AreaShapeNo): 
    #AssetSearch = bpy.context.workspace["Asset Searching Enabled"]
    #BlendFilesFolder = bpy.context.workspace["Workspace (for searching in Blend files)"]
    MapAssetBlendFile = bpy.context.workspace["Map Assets Blend file"]
    
    #AreaShapeNo = '0'
    
    ########################################### COLLECTION LINK
    
    try:

        if AreaShapeNo == '0':
            AreaShapeCOL = "AreaShape 0  Cube" #Dem Emtpy eine Collection Instanz zuweisen
        if AreaShapeNo == '1':
            AreaShapeCOL = "AreaShape 1  Cube Middle" #Dem Emtpy eine Collection Instanz zuweisen    
        if AreaShapeNo == '2':
            AreaShapeCOL = "AreaShape 2  Sphere" #Dem Emtpy eine Collection Instanz zuweisen
        if AreaShapeNo == '3':
            AreaShapeCOL = "AreaShape 3  Cylinder" #Dem Emtpy eine Collection Instanz zuweisen
        if AreaShapeNo == '4':
            AreaShapeCOL = "AreaShape 4  Half Sphere" #Dem Emtpy eine Collection Instanz zuweisen

        #folder = bpy.path.abspath("//")

        # get all blend files in the folder
        #blends = [f for f in os.listdir(folder) if f.endswith(".blend")]

        #for blend in blends:

        # path to the blend
        filepath = MapAssetBlendFile
        # name of collection(s) to append or link
        coll_name = AreaShapeCOL #FIX oder
        # append, set to true to keep the link to the original file
        link = True
        # link all collections lose an die Blenderdatei
        with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
            data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 0  Cube")]
        
        with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
            data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 1  Cube Middle")]
        
        with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
            data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 2  Sphere")]
            
        with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
            data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 3  Cylinder")]
            
        with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
            data_to.collections = [c for c in data_from.collections if c.startswith("AreaShape 4  Half Sphere")]
            
        # link collection to selected Empty
        bpy.context.object.instance_type = 'COLLECTION'
        bpy.context.object.instance_collection = bpy.data.collections[AreaShapeCOL]
        

        
    except:
        print("KEIN ZUGRIFF AUF DIE BLEND DATEI")
        print(name)
        pass
    
    #################################  COLLECTION LINK END

class GalaxyMapAddPathPointSetup(bpy.types.Operator): 
   """Add Path Point Setup to selected path"""
   bl_idname = "galaxymap77.galaxyaddpathsetup" 
   bl_label = "Add Path Point Setup" 
   def execute(self, context):
        AssetSearch = bpy.context.workspace["Asset Searching Enabled"]
        BlendFilesFolder = bpy.context.workspace["Workspace (for searching in Blend files)"]
        MapAssetBlendFile = bpy.context.workspace["Map Assets Blend file"]
        
        #############################################
        #Geometry Node linken.
        obj = bpy.context.object
        file_path = MapAssetBlendFile
        node_name = "PointArgs1"
        link = True
        
        Point_ID = get_selected_spline_pointid()
        Point_ID_int = Point_ID
        Point_ID = str(Point_ID)
        #Point_ID = "0"
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        from os.path import join as os_path_join

        inner_path = "NodeTree"
        node_groups = bpy.data.node_groups


        bpy.ops.wm.append(
            filepath=os_path_join(file_path, inner_path, node_name),
            directory=os_path_join(file_path, inner_path),
            filename=node_name,
            link=link)


        modifier=bpy.context.object.modifiers.new(Point_ID, "NODES")
        
        modifier.node_group = bpy.data.node_groups['PointArgs1']
        
        #########################################################
        bpy.context.object.modifiers[Point_ID]["Input_16"] = Point_ID_int #nur optisch, dieser Punkt
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

#### Switches ####

class GalaxyMapNewSwitch_A(bpy.types.Operator):
   """Generate new switch id"""
   bl_idname = "galaxymap201.galaxyaddswitcha" 
   bl_label = "get free switch id" 
   def execute(self, context):
        if bpy.context.object["SW_A"] == -1:
            Switch = "SW_A"
            GiveFreeSwitchID(Switch, False)
        else:
            self.report({'INFO'}, "Switch ID not empty! - Replace with -1")
        return {'FINISHED'}
        
class GalaxyMapNewSwitch_B(bpy.types.Operator):
   """Generate new switch id"""
   bl_idname = "galaxymap202.galaxyaddswitchb" 
   bl_label = "get free switch id" 
   def execute(self, context):
        if bpy.context.object["SW_B"] == -1:
            Switch = "SW_B"
            GiveFreeSwitchID(Switch, False)
        else:
            self.report({'INFO'}, "Switch ID not empty! - Replace with -1")
        return {'FINISHED'}
        
class GalaxyMapNewSwitch_Appear(bpy.types.Operator):
   """Generate new switch id"""
   bl_idname = "galaxymap203.galaxyaddswitchappear" 
   bl_label = "get free switch id" 
   def execute(self, context):
        if bpy.context.object["SW_APPEAR"] == -1:
            Switch = "SW_APPEAR"
            GiveFreeSwitchID(Switch, False)
        else:
            self.report({'INFO'}, "Switch ID not empty! - Replace with -1")
        return {'FINISHED'}
        
class GalaxyMapNewSwitch_Dead(bpy.types.Operator):
   """Generate new switch id"""
   bl_idname = "galaxymap204.galaxyaddswitchdead" 
   bl_label = "get free switch id" 
   def execute(self, context):
        if bpy.context.object["SW_DEAD"] == -1:
            Switch = "SW_DEAD"
            GiveFreeSwitchID(Switch, False)
        else:
            self.report({'INFO'}, "Switch ID not empty! - Replace with -1")
        return {'FINISHED'}
        
class GalaxyMapNewSwitch_Awake(bpy.types.Operator):
   """Generate new switch id"""
   bl_idname = "galaxymap205.galaxyaddswitchawake" 
   bl_label = "get free switch id" 
   def execute(self, context):
        if bpy.context.object["SW_AWAKE"] == -1:
            Switch = "SW_AWAKE"
            GiveFreeSwitchID(Switch, False)
        else:
            self.report({'INFO'}, "Switch ID not empty! - Replace with -1")
        return {'FINISHED'}
        
class GalaxyMapNewSwitch_Param(bpy.types.Operator):
   """Generate new switch id"""
   bl_idname = "galaxymap206.galaxyaddswitchparam" 
   bl_label = "get free switch id" 
   def execute(self, context):
        if bpy.context.object["SW_PARAM"] == -1:
            Switch = "SW_PARAM"
            GiveFreeSwitchID(Switch, False)
        else:
            self.report({'INFO'}, "Switch ID not empty! - Replace with -1")
        return {'FINISHED'}
        
### Full Galaxy Switch IDs:

class GalaxyMapNewSwitch_A_FullGalaxy(bpy.types.Operator):
   """Generate new switch id"""
   bl_idname = "galaxymap301.galaxyaddswitchafull" 
   bl_label = "get free switch id" 
   def execute(self, context):
        if bpy.context.object["SW_A"] == -1:
            Switch = "SW_A"
            GiveFreeSwitchID(Switch, True)
        else:
            self.report({'INFO'}, "Switch ID not empty! - Replace with -1")
        return {'FINISHED'}
        
class GalaxyMapNewSwitch_B_FullGalaxy(bpy.types.Operator):
   """Generate new switch id"""
   bl_idname = "galaxymap302.galaxyaddswitchbfull" 
   bl_label = "get free switch id" 
   def execute(self, context):
        if bpy.context.object["SW_B"] == -1:
            Switch = "SW_B"
            GiveFreeSwitchID(Switch, True)
        else:
            self.report({'INFO'}, "Switch ID not empty! - Replace with -1")
        return {'FINISHED'}
        
class GalaxyMapNewSwitch_Appear_FullGalaxy(bpy.types.Operator):
   """Generate new switch id"""
   bl_idname = "galaxymap303.galaxyaddswitchappearfull" 
   bl_label = "get free switch id" 
   def execute(self, context):
        self.report({'INFO'}, "Button wurde gedrückt!")
        if bpy.context.object["SW_APPEAR"] == -1:
            Switch = "SW_APPEAR"
            GiveFreeSwitchID(Switch, True)
        else:
            self.report({'INFO'}, "Switch ID not empty! - Replace with -1")
        return {'FINISHED'}
        
class GalaxyMapNewSwitch_Dead_FullGalaxy(bpy.types.Operator):
   """Generate new switch id"""
   bl_idname = "galaxymap304.galaxyaddswitchdeadfull" 
   bl_label = "get free switch id" 
   def execute(self, context):
        self.report({'INFO'}, "Button wurde gedrückt!")
        if bpy.context.object["SW_DEAD"] == -1:
            Switch = "SW_DEAD"
            GiveFreeSwitchID(Switch, True)
        else:
            self.report({'INFO'}, "Switch ID not empty! - Replace with -1")
        return {'FINISHED'}
        
class GalaxyMapNewSwitch_Awake_FullGalaxy(bpy.types.Operator):
   """Generate new switch id"""
   bl_idname = "galaxymap305.galaxyaddswitchawakefull" 
   bl_label = "get free switch id" 
   def execute(self, context):
        self.report({'INFO'}, "Button wurde gedrückt!")
        if bpy.context.object["SW_AWAKE"] == -1:
            Switch = "SW_AWAKE"
            GiveFreeSwitchID(Switch, True)
        else:
            self.report({'INFO'}, "Switch ID not empty! - Replace with -1")
        return {'FINISHED'}
        
class GalaxyMapNewSwitch_Param_FullGalaxy(bpy.types.Operator):
   """Generate new switch id"""
   bl_idname = "galaxymap306.galaxyaddswitchparamfull" 
   bl_label = "get free switch id" 
   def execute(self, context):
        self.report({'INFO'}, "Button wurde gedrückt!")
        if bpy.context.object["SW_PARAM"] == -1:
            Switch = "SW_PARAM"
            GiveFreeSwitchID(Switch, True)
        return {'FINISHED'}
        
###Substarters

class GalaxyMapAddGravity_Planar(bpy.types.Operator):
    """A gravity area that attracts objects towards a plane \n A gravity area that attracts objects towards collision triangles."""
    bl_idname = "galaxymap11.galaxyadd_globalplanegravity"
    bl_label = "Planar/Zero" 
    def execute(self, context):
        ObjektName = str(0)
        GalaxyMapAddGravity(ObjektName)
        return {'FINISHED'}

class GalaxyMapAddGravity_Sphere(bpy.types.Operator):
    """A gravity area that attracts objects towards its origin."""
    bl_idname = "galaxymap12.galaxyadd_globalpointgravity"
    bl_label = "Spherical" 
    def execute(self, context):
        ObjektName = str(1)
        GalaxyMapAddGravity(ObjektName)
        return {'FINISHED'}

class GalaxyMapAddGravity_Cube(bpy.types.Operator):
    """A gravity area for a cube-shaped planet that allows movement on all six faces."""
    bl_idname = "galaxymap13.galaxyadd_globalcubegravity"
    bl_label = "Cubic" 
    def execute(self, context):
        ObjektName = str(2)
        GalaxyMapAddGravity(ObjektName)
        return {'FINISHED'}

class GalaxyMapAddGravity_Cylinder(bpy.types.Operator):
    """A gravity area that pulls objects towards the lateral surface of the cylinder."""
    bl_idname = "galaxymap14.galaxyadd_globalsegmentgravity"
    bl_label = "Cylindrical" 
    def execute(self, context):
        ObjektName = str(3)
        GalaxyMapAddGravity(ObjektName)
        return {'FINISHED'}

class GalaxyMapAddGravity_Disk(bpy.types.Operator):
    """A gravity area for a disk-shaped planet."""
    bl_idname = "galaxymap15.galaxyadd_globaldiskgravity"
    bl_label = "Disk" 
    def execute(self, context):
        ObjektName = str(4)
        GalaxyMapAddGravity(ObjektName)
        return {'FINISHED'}

class GalaxyMapAddGravity_Donut(bpy.types.Operator):
    """A gravity area for a torus-shaped planet."""
    bl_idname = "galaxymap16.galaxyadd_globaldisktorusgravity"
    bl_label = "Torus (Donut)" 
    def execute(self, context):
        ObjektName = str(5)
        GalaxyMapAddGravity(ObjektName)
        return {'FINISHED'}

class GalaxyMapAddGravity_Cone(bpy.types.Operator):
    """A gravity area for a cone-shaped planet."""
    bl_idname = "galaxymap17.galaxyadd_globalconegravity"
    bl_label = "Cone" 
    def execute(self, context):
        ObjektName = str(6)
        GalaxyMapAddGravity(ObjektName)
        return {'FINISHED'}

class GalaxyMapAddGravity_Barrel(bpy.types.Operator):
    """A gravity area that revolves around a barrel-shaped planet. \n Objects are pulled sideways along the cylinder. """
    bl_idname = "galaxymap18.galaxyadd_globalbarrelgravity"
    bl_label = "Barrel (sideways)" 
    def execute(self, context):
        ObjektName = str(7)
        GalaxyMapAddGravity(ObjektName)
        return {'FINISHED'}

class GalaxyMapAddGravity_Wire(bpy.types.Operator):
    """A gravity area that uses a path to define several points of gravity."""
    bl_idname = "galaxymap19.galaxyadd_globalwiregravity"
    bl_label = "Wire (via path)" 
    def execute(self, context):
        ObjektName = str(8)
        GalaxyMapAddGravity(ObjektName)
        return {'FINISHED'}


class GalaxyMapAddCutscene_Normal(bpy.types.Operator):
    """A basic in-stage cutscene."""
    bl_idname = "galaxymap20.galaxyadd_cutscene"
    bl_label = "Basic Cutscene" 
    def execute(self, context):
        name = str(0)
        GalaxyMapAddCutscene(name)
        return {'FINISHED'}
        
class GalaxyMapAddCutscene_Sub(bpy.types.Operator):
    """An object used to connect a cutscene across multiple zones."""
    bl_idname = "galaxymap21.galaxyadd_cutscenesub"
    bl_label = "Sub Cutscene" 
    def execute(self, context):
        name = str(1)
        GalaxyMapAddCutscene(name)
        return {'FINISHED'}
      

class GalaxyMapChangeAreaShape_0(bpy.types.Operator):
    """Cubic area with pivot on the bottom"""
    bl_idname = "smgmaparea0.changeto0"
    bl_label = "To Cube" 
    def execute(self, context):
        AreaShapeNo = str(0)
        GalaxyMapChangeAreaShape(AreaShapeNo)
        return {'FINISHED'}
        
class GalaxyMapChangeAreaShape_1(bpy.types.Operator):
    """Cubic area with pivot in the middle"""
    bl_idname = "smgmaparea1.changeto1"
    bl_label = "To Cube (with pivot in center)" 
    def execute(self, context):
        AreaShapeNo = str(1)
        GalaxyMapChangeAreaShape(AreaShapeNo)
        return {'FINISHED'}
        
class GalaxyMapChangeAreaShape_2(bpy.types.Operator):
    """Spherical range"""
    bl_idname = "smgmaparea2.changeto2"
    bl_label = "To Sphere" 
    def execute(self, context):
        AreaShapeNo = str(2)
        GalaxyMapChangeAreaShape(AreaShapeNo)
        return {'FINISHED'}
        
class GalaxyMapChangeAreaShape_3(bpy.types.Operator):
    """Cylindrial range"""
    bl_idname = "smgmaparea3.changeto3"
    bl_label = "To Cylinder" 
    def execute(self, context):
        AreaShapeNo = str(3)
        GalaxyMapChangeAreaShape(AreaShapeNo)
        return {'FINISHED'}
        
class GalaxyMapChangeAreaShape_4(bpy.types.Operator):
    """Dome-shaped range"""
    bl_idname = "smgmaparea4.changeto4"
    bl_label = "To hemispherical form" 
    def execute(self, context):
        AreaShapeNo = str(4)
        GalaxyMapChangeAreaShape(AreaShapeNo)
        return {'FINISHED'}



      
###LAYOUT SUBMENU

class GalaxyMapOperator13(bpy.types.Operator): #nur zum starten vom layout
    """Add Object infos"""
    bl_idname = "objecttrala.galaxymap_operator13"
    bl_label = "Add properties to selected asset (collection)" 
    def execute(self, context):
        bpy.ops.wm.call_menu(name=LayoutSMGMapMenu1.bl_idname)
        return {'FINISHED'}

class GalaxyMap_LayoutStarter2(bpy.types.Operator): #nur zum starten vom layout
    """Add Object"""
    bl_idname = "galaxymaplayout2.layoutstarter2"
    bl_label = "Add Gravity" 
    def execute(self, context):
        bpy.ops.wm.call_menu(name=LayoutSMGMap_AddGravityPanel.bl_idname)
        return {'FINISHED'}
        
class GalaxyMap_LayoutStarter3(bpy.types.Operator): #nur zum starten vom layout
    """Add Object"""
    bl_idname = "galaxymaplayout3.layoutstarter3"
    bl_label = "Add Cutscene Object" 
    def execute(self, context):
        bpy.ops.wm.call_menu(name=LayoutSMGMap_AddCutscenePanel.bl_idname)
        return {'FINISHED'}
        
class GalaxyMap_LayoutStarter4(bpy.types.Operator): #nur zum starten vom layout
    """Add Object"""
    bl_idname = "galaxymaplayout4.layoutstarter4"
    bl_label = "Change Area Shape" 
    def execute(self, context):
        bpy.ops.wm.call_menu(name=LayoutSMGMap_ChangeAreaShapePanel.bl_idname)
        return {'FINISHED'}
    
class GalaxyMapOperator40(bpy.types.Operator): #nur zum starten vom layout
    """Add Object"""
    bl_idname = "objectwerf.galaxymap_layoutstarter2"
    bl_label = "Add Galaxy Object" 
    def execute(self, context):
        bpy.ops.wm.call_menu(name=LayoutSMGMap_AddObjPanel.bl_idname)
        return {'FINISHED'}

class GalaxyMap_AddObjProps(bpy.types.Operator):
    """Add properties to selected asset (type: object)"""
    bl_idname = "galaxymap50.add_obj_props"
    bl_label = "General object" 
    def execute(self, context):
    
        #bpy.context.object["Object Name"] = ""
        bpy.context.object["Link ID"] = 0
        bpy.context.object["Obj_Arg0"] = -1
        bpy.context.object["Obj_Arg1"] = -1
        bpy.context.object["Obj_Arg2"] = -1
        bpy.context.object["Obj_Arg3"] = -1
        bpy.context.object["Obj_Arg4"] = -1
        bpy.context.object["Obj_Arg5"] = -1
        bpy.context.object["Obj_Arg6"] = -1
        bpy.context.object["Obj_Arg7"] = -1
        bpy.context.object["Camera Set ID"] = -1
        bpy.context.object["SW_APPEAR"] = -1
        bpy.context.object["SW_DEAD"] = -1
        bpy.context.object["SW_A"] = -1
        bpy.context.object["SW_B"] = -1
        bpy.context.object["SW_AWAKE"] = -1
        bpy.context.object["SW_PARAM"] = -1
        bpy.context.object["Message ID"] = -2
        bpy.context.object["Speed Scale"] = 1
        bpy.context.object["Cast Group ID"] = -1
        bpy.context.object["View Group ID"] = -1
        bpy.context.object["Model ID"] = -1
        bpy.context.object["Path ID"] = -1
        bpy.context.object["Clipping Group ID"] = -1
        bpy.context.object["Group ID"] = -1
        bpy.context.object["Cutscene Group ID"] = -1
        bpy.context.object["Linked MapParts ID"] = -1
        bpy.context.object["Linked Object ID"] = -1
        bpy.context.object["Generator Object ID"] = -1
        bpy.context.object["Layer"] = "Common"
        return {'FINISHED'}
 
class GalaxyMap_AddMapPartProps(bpy.types.Operator):
    """Add Object"""
    bl_idname = "galaxymap51.add_mappart_props"
    bl_label = "Map Part Object" 
    def execute(self, context):
    
        #bpy.context.object["Object Name"] = ""
        bpy.context.object["Link ID"] = -1
        bpy.context.object["MoveConditionType"] = 0
        bpy.context.object["RotateSpeed"] = 0
        bpy.context.object["RotateAngle"] = 0
        bpy.context.object["RotateAxis"] = 0
        bpy.context.object["RotateAccelType"] = 0
        bpy.context.object["RotateStopTime"] = 0
        bpy.context.object["RotateType"] = 0
        bpy.context.object["ShadowType"] = 0
        bpy.context.object["SignMotionType"] = 0
        bpy.context.object["PressType"] = 0
        bpy.context.object["Speed Scale"] = 1
        bpy.context.object["Camera Set ID"] = -1
        bpy.context.object["Far Clip"] = -1
        
        bpy.context.object["Obj_Arg0"] = -1
        bpy.context.object["Obj_Arg1"] = -1
        bpy.context.object["Obj_Arg2"] = -1
        bpy.context.object["Obj_Arg3"] = -1
        
        bpy.context.object["SW_APPEAR"] = -1
        bpy.context.object["SW_DEAD"] = -1
        bpy.context.object["SW_A"] = -1
        bpy.context.object["SW_B"] = -1
        bpy.context.object["SW_AWAKE"] = -1
        bpy.context.object["SW_PARAM"] = -1
        
        bpy.context.object["Cast Group ID"] = -1
        bpy.context.object["View Group ID"] = -1
        bpy.context.object["Model ID"] = -1
        bpy.context.object["Path ID"] = -1
        bpy.context.object["Clipping Group ID"] = -1
        bpy.context.object["Group ID"] = -1
        bpy.context.object["Cutscene Group ID"] = -1
        bpy.context.object["Linked MapParts ID"] = -1
        bpy.context.object["Linked Object ID"] = -1
        bpy.context.object["Parent Object ID"] = -1

        bpy.context.object["Layer"] = "Common"
        return {'FINISHED'} 

###LAYOUT -----------------------------------------------------

def get_selected_spline_point():
    obj = bpy.context.active_object
    if obj and obj.type == 'CURVE':
        curve = obj.data
        for spline in curve.splines:
            for i, point in enumerate(spline.points if spline.type == 'NURBS' else spline.bezier_points):
                if point.select_control_point:
                    return point, spline.type
    return None, None

def get_selected_spline_pointid():
    obj = bpy.context.active_object
    if obj and obj.type == 'CURVE' and obj.data.splines:
        for spline in obj.data.splines:
            for i, point in enumerate(spline.bezier_points):  # Für Bezier-Kurven
                if point.select_control_point:
                    return i  # Gibt den Index des gewählten Punktes zurück
            for i, point in enumerate(spline.points):  # Für normale Splines
                if point.select:
                    return i
    return None

import re

def get_base_object_name(objname):
    return re.sub(r"\.\d{3}$", "", objname) if objname else ""
    
    
class LayoutSMGMapPanel(bpy.types.Panel):


    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Map Tools"
    bl_idname = "SCENE_GalaxyMapTool_layout" 
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Mario Galaxy"

    def draw(self, context):
        ### Initialize Name Slots for entering names:
        if not "Galaxy Name" in bpy.context.workspace:
            bpy.context.workspace["Galaxy Name"] = "YourGalaxy"
        if not "Zone Name" in bpy.context.workspace:
            bpy.context.workspace["Zone Name"] = "YourZone"
        if not "Asset Searching Enabled" in bpy.context.workspace:
            bpy.context.workspace["Asset Searching Enabled"] = 0

        if not "Object Type" in bpy.context.workspace:
            bpy.context.workspace["Object Type"] = 0

        if not "Add this object" in bpy.context.workspace:
            bpy.context.workspace["Add this object"] = ""
        ### Initialize paths for tools:
        if not "WiiExplorer Folder Path" in bpy.context.workspace:
            bpy.context.workspace["WiiExplorer Folder Path"] = "C:/WiiExplorer.V1.5.0.5/"
        if not "LaunchCamPlus Folder Path" in bpy.context.workspace:
            bpy.context.workspace["LaunchCamPlus Folder Path"] = "C:/LaunchCamPlus.V2.5.2.0/"
        if not "StageData Folder Path" in bpy.context.workspace:
            bpy.context.workspace["StageData Folder Path"] = "C:/SMG2/StageData/"
        
        ### Map Assets
        if not "Map Assets Blend file" in bpy.context.workspace:
            bpy.context.workspace["Map Assets Blend file"] = "C:/GalaxyMapAssets.blend"
        if not "Workspace (for searching in Blend files)" in bpy.context.workspace:
            bpy.context.workspace["Workspace (for searching in Blend files)"] = "C:/MyBlenderFiles/"
        if not "Object Database" in bpy.context.workspace:
            bpy.context.workspace["Object Database"] = "C:/Whitehole/objectdb.xml"

        
        #Layout Name Stuff:
        for col in bpy.data.collections:
            if "World Number" in col:
                LayoutMapName = col.name
            else:
                LayoutMapName = "No Galaxy Map found!"
        
        if "Zone ID" in bpy.context.collection:
            LayoutMapZoneName = bpy.context.collection.name
        else:
            LayoutMapZoneName = "No valid Zone selected"

        #Panel Settings:
        if "Display Notes from SMG Database" not in bpy.context.workspace:
            bpy.context.workspace["Display Notes from SMG Database"] = True


        #WiiExplorerPathFolder
        #CameraEditorPath
        layout = self.layout
        scene = context.scene
        
        
        layout.label(text="EXPORT")
        
        split = layout.split() #Splitte Rows
        # First column
        col = split.column(align=False)
        col.scale_y = 1.5
        col.operator("objecto.galaxymap_operator3", icon='EXPORT')
        col.operator("objectu.galaxymap_operator4", icon='EXPORT')
        # Second column
        col = split.column(align=False)
        col.scale_y = 1.5
        col.label(text="EXPORT: " + LayoutMapName)
        col.label(text="EXPORT: " + LayoutMapZoneName)
        
        
        
        row = layout.row()
        row.scale_y = 1.2
        row.operator("objecthihi.galaxymap_operator8", icon='EXPORT') 
        
        
        layout.label(text="IMPORT")
        
        # First column
        split = layout.split() #Splitte Rows
        col = split.column(align=False)
        col.scale_y = 1.5
        col.operator("object.galaxymap_operator1", icon='IMPORT')
        col.operator("objecti.galaxymap_operator2", icon='IMPORT')
        # Second column, aligned
        col = split.column(align=False)
        col.scale_y = 1.5
        col.prop(bpy.context.workspace, '["Galaxy Name"]')
        col.prop(bpy.context.workspace, '["Zone Name"]')
        
        row = layout.row()
        row.scale_y = 1
        row = layout.prop(bpy.context.workspace, '["Asset Searching Enabled"]', icon='VIEWZOOM')



		
        row = layout.row()
        row.scale_y = 2
        
        layout.label(text="Create New")

        col = layout.column(align=True)  # Sorgt dafür, dass die Buttons direkt aufeinanderliegen
        col.operator("objecta.galaxymap_operator5", icon='ADD')  # New Zone
        col.operator("objectbla.galaxymap_operator9", icon='PLUS')  # New Galaxy
        col.operator("objectbob.galaxymap_operator10", icon='RNA_ADD')  # New Mission


        
        layout.label(text="Map Tools")
        col = layout.column(align=True)
        col.operator("objectwerf.galaxymap_layoutstarter2", icon='PLUS') #Add object        
        col.operator("galaxymaplayout4.layoutstarter4", icon='MOD_LINEART') #change area shape
        col.operator("objecte.galaxymap_operator7", icon='VIS_SEL_11') #update layer info
        col.prop(bpy.context.workspace, '["Add this object"]')
        split = layout.split() #Splitte Rows
        col = split.column(align=True)
        col.operator("objecty.galaxymap_operator6", icon='CAMERA_DATA') #camera edit
        col = split.column(align=True)
        col.label(text="Edit: " + LayoutMapZoneName)

        
        layout.label(text="Paths")
        col = layout.column(align=True)
        col.prop(bpy.context.workspace, '["StageData Folder Path"]')
        col.prop(bpy.context.workspace, '["Map Assets Blend file"]')
        col.prop(bpy.context.workspace, '["WiiExplorer Folder Path"]')
        col.prop(bpy.context.workspace, '["LaunchCamPlus Folder Path"]')
        col.prop(bpy.context.workspace, '["Workspace (for searching in Blend files)"]')
        col.prop(bpy.context.workspace, '["Object Database"]')

        layout.label(text="Asset Tools")
        row = layout.row()
        row.scale_y = 1.2
        row.operator("objecttrala.galaxymap_operator13", icon='PREFERENCES') #add properties for empty object

class LayoutSMGMapObjectPanel(bpy.types.Panel):


    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Object Settings"
    bl_idname = "SCENE_GalaxyMapObject_layout" 
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Mario Galaxy"

    def draw(self, context): #General Object
    
        obj = context.object
        if obj is None:
            layout.label(text="No Objekt selected")
            return
    
        
        ### Initialize Name Slots for entering names:
        if "Model ID" in bpy.context.object:
            if not "RotateAccelType" in bpy.context.object:
                layout = self.layout
                scene = context.scene
                
                ### ARGUMENT NAMEN AUS OBJEKT DATABASE NEHMEN
                
                obj = context.object

                if obj is None:
                    layout.label(text="Kein Objekt ausgewählt")
                    return
                
                if obj.instance_collection == None:
                    #obj_name = (obj["Object Name"]) #Nehme Text aus der 'Object Name' property    
                    #obj_name = obj.get("Object Name", "Unknown")
                    obj_name = get_base_object_name(obj.name)

                else:
                    obj_name = (obj.instance_collection.name) #Nehme Namen der Collection als Objektnamen
                    #obj_name = obj.get(instance_collection.name, "Unknown")
                
                #obj_name = obj.get("Object Name", "Unknown")
                
                display_name, labels, notes = load_labels_from_xml(obj_name, 8, False)
                ##########
                
                layout.label(text=f"--- {display_name} ---")
                layout.prop(bpy.context.workspace, '["Display Notes from SMG Database"]')
                if bpy.context.workspace["Display Notes from SMG Database"] == True:
                    if notes:
                        import textwrap
                        #layout.label(text="Notes:")
                        #layout.box().label(text=notes, icon='INFO')  # Fügt einen Rahmen um den Notiztext
                        
                        layout.label(text="Notes:")
                        box = layout.box()
                        lines = notes.split("\n")
                        #lines2= ArgInfo.split("\n")
                        col = box.column(align=True)
                        for line in lines:
                            words = line.split()
                            wrapped_lines = [" ".join(words[i:i+9]) for i in range(0, len(words), 9)]
                            
                            for wrapped_line in wrapped_lines:
                                col.label(text=wrapped_line)
                    

                    
                row = layout.row()
                row.scale_y = 1.2
                row = layout.prop(bpy.context.object, '["Layer"]')
                
                
                layout.label(text="Settings")
                col = layout.column(align=True)
                col.prop(bpy.context.object, '["Link ID"]')
                col.prop(bpy.context.object, '["Model ID"]')
                col.prop(bpy.context.object, '["Path ID"]')
                col.prop(bpy.context.object, '["Camera Set ID"]')
                col.prop(bpy.context.object, '["Message ID"]')
                col.prop(bpy.context.object, '["Speed Scale"]')
                col.prop(bpy.context.object, '["Generator Object ID"]')
                col.prop(bpy.context.object, '["Linked Object ID]')
                col.prop(bpy.context.object, '["Linked MapParts ID"]')
                

                layout.label(text="Arguments")
                col = layout.column(align=True)
                for i in range(len(labels)):
                    col.prop(obj, f'["Obj_Arg{i}"]', text=labels[i])
                

                
                layout.label(text="Switches")
                row = layout.row()
                row.alignment = 'LEFT'
                # Erste Spalte für die SW-Werte (größer)
                col1 = row.column(align=True)
                col1.scale_x = 2  # Macht die erste Spalte etwas größer
                col1.prop(context.object, '["SW_APPEAR"]', text="SW_APPEAR")
                col1.prop(context.object, '["SW_DEAD"]', text="SW_DEAD")
                col1.prop(context.object, '["SW_A"]', text="SW_A")
                col1.prop(context.object, '["SW_B"]', text="SW_B")
                col1.prop(context.object, '["SW_AWAKE"]', text="SW_AWAKE")
                col1.prop(context.object, '["SW_PARAM"]', text="SW_PARAM")

                # Geteilte Spalten für Z und G
                split = row.split(factor=0.35)  # Teilt den verbleibenden Platz
                col2 = split.column(align=True)
                col2.scale_x = 1
                col2.operator("galaxymap203.galaxyaddswitchappear", text="Z")
                col2.operator("galaxymap204.galaxyaddswitchdead", text="Z")
                col2.operator("galaxymap201.galaxyaddswitcha", text="Z")
                col2.operator("galaxymap202.galaxyaddswitchb", text="Z")
                col2.operator("galaxymap205.galaxyaddswitchawake", text="Z")
                col2.operator("galaxymap206.galaxyaddswitchparam", text="Z")

                col3 = split.column(align=True)
                col3.scale_x = 0.004
                col3.operator("galaxymap303.galaxyaddswitchappearfull", text="G")
                col3.operator("galaxymap304.galaxyaddswitchdeadfull", text="G")
                col3.operator("galaxymap301.galaxyaddswitchafull", text="G")
                col3.operator("galaxymap302.galaxyaddswitchbfull", text="G")
                col3.operator("galaxymap305.galaxyaddswitchawakefull", text="G")
                col3.operator("galaxymap306.galaxyaddswitchparamfull", text="G")


                layout.label(text="Groups")
                col = layout.column(align=True)
                col.prop(bpy.context.object, '["Group ID"]')
                col.prop(bpy.context.object, '["Clipping Group ID"]')
                col.prop(bpy.context.object, '["View Group ID"]')
                col.prop(bpy.context.object, '["Cutscene Group ID"]')
                col.prop(bpy.context.object, '["Cast Group ID"]')

#    def draw(self, context): #MapPart Object
        if "RotateStopTime" in bpy.context.object:
            layout = self.layout
            scene = context.scene
            
            ### ARGUMENT NAMEN AUS OBJEKT DATABASE NEHMEN
            
            obj = context.object

            if obj is None:
                layout.label(text="Kein Objekt ausgewählt")
                return
            
            if obj.instance_collection == None:
                obj_name = get_base_object_name(obj.name)
            else:
                obj_name = (obj.instance_collection.name) #Nehme Namen der Collection als Objektnamen
                #obj_name = obj.get(instance_collection.name, "Unknown")
            
            #obj_name = obj.get("Object Name", "Unknown")
            
            display_name, labels, notes = load_labels_from_xml(obj_name, 8, False)
            ##########
            layout.label(text=f"--- {display_name} ---")
            layout.prop(bpy.context.workspace, '["Display Notes from SMG Database"]')
            if bpy.context.workspace["Display Notes from SMG Database"] == True:
                if notes:
                    import textwrap
                    #layout.label(text="Notes:")
                    #layout.box().label(text=notes, icon='INFO')  # Fügt einen Rahmen um den Notiztext
                    
                    layout.label(text="Notes:")
                    box = layout.box()
                    lines = notes.split("\n")
                    
                    col = box.column(align=True)
                    for line in lines:
                        words = line.split()
                        wrapped_lines = [" ".join(words[i:i+9]) for i in range(0, len(words), 9)]
                        
                        for wrapped_line in wrapped_lines:
                            col.label(text=wrapped_line)
            row = layout.row()
            row.scale_y = 1.2
            row = layout.prop(bpy.context.object, '["Layer"]')
            
            
            layout.label(text="MapPart Settings")
            col = layout.column(align=True)
            col.prop(bpy.context.object, '["MoveConditionType"]')
            col.prop(bpy.context.object, '["RotateSpeed"]')
            col.prop(bpy.context.object, '["RotateAngle"]')
            col.prop(bpy.context.object, '["RotateAxis"]')
            col.prop(bpy.context.object, '["RotateAccelType"]')
            col.prop(bpy.context.object, '["RotateStopTime"]')
            col.prop(bpy.context.object, '["RotateType"]')
            col.prop(bpy.context.object, '["ShadowType]')
            col.prop(bpy.context.object, '["SignMotionType"]')
            col.prop(bpy.context.object, '["PressType"]')
            col.prop(bpy.context.object, '["FarClip"]')
            
            # layout.label(text="Arguments")
            # col = layout.column(align=True)
            # col.prop(bpy.context.object, '["Obj_Arg0"]')
            # col.prop(bpy.context.object, '["Obj_Arg1"]')
            # col.prop(bpy.context.object, '["Obj_Arg2"]')
            # col.prop(bpy.context.object, '["Obj_Arg3"]')
            


            layout.label(text="Arguments")
            
            col = layout.column(align=True)
            for i in range(len(labels)):
                col.prop(obj, f'["Obj_Arg{i}"]', text=labels[i])
            


            layout.label(text="Switches")
            row = layout.row()
            row.alignment = 'LEFT'
            # Erste Spalte für die SW-Werte (größer)
            col1 = row.column(align=True)
            col1.scale_x = 2  # Macht die erste Spalte etwas größer
            col1.prop(context.object, '["SW_APPEAR"]', text="SW_APPEAR")
            col1.prop(context.object, '["SW_DEAD"]', text="SW_DEAD")
            col1.prop(context.object, '["SW_A"]', text="SW_A")
            col1.prop(context.object, '["SW_B"]', text="SW_B")
            col1.prop(context.object, '["SW_AWAKE"]', text="SW_AWAKE")
            col1.prop(context.object, '["SW_PARAM"]', text="SW_PARAM")

            # Geteilte Spalten für Z und G
            split = row.split(factor=0.35)  # Teilt den verbleibenden Platz
            col2 = split.column(align=True)
            col2.scale_x = 1
            col2.operator("galaxymap203.galaxyaddswitchappear", text="Z")
            col2.operator("galaxymap204.galaxyaddswitchdead", text="Z")
            col2.operator("galaxymap201.galaxyaddswitcha", text="Z")
            col2.operator("galaxymap202.galaxyaddswitchb", text="Z")
            col2.operator("galaxymap205.galaxyaddswitchawake", text="Z")
            col2.operator("galaxymap206.galaxyaddswitchparam", text="Z")

            col3 = split.column(align=True)
            col3.scale_x = 0.004
            col3.operator("galaxymap303.galaxyaddswitchappearfull", text="G")
            col3.operator("galaxymap304.galaxyaddswitchdeadfull", text="G")
            col3.operator("galaxymap301.galaxyaddswitchafull", text="G")
            col3.operator("galaxymap302.galaxyaddswitchbfull", text="G")
            col3.operator("galaxymap305.galaxyaddswitchawakefull", text="G")
            col3.operator("galaxymap306.galaxyaddswitchparamfull", text="G")
            
            layout.label(text="Settings")
            col = layout.column(align=True)
            col.prop(bpy.context.object, '["Link ID"]')
            col.prop(bpy.context.object, '["Model ID"]')
            col.prop(bpy.context.object, '["Path ID"]')
            col.prop(bpy.context.object, '["Camera Set ID"]')
            col.prop(bpy.context.object, '["Speed Scale"]')
            col.prop(bpy.context.object, '["Parent Object ID"]')
            col.prop(bpy.context.object, '["Linked Object ID]')
            col.prop(bpy.context.object, '["Linked MapParts ID"]')
            

            layout.label(text="Groups")
            col = layout.column(align=True)
            col.prop(bpy.context.object, '["Group ID"]')
            col.prop(bpy.context.object, '["Clipping Group ID"]')
            col.prop(bpy.context.object, '["View Group ID"]')
            col.prop(bpy.context.object, '["Cutscene Group ID"]')
            col.prop(bpy.context.object, '["Cast Group ID"]')

#    def draw(self, context): #Area
        ### Initialize Name Slots for entering names:
        if "Linked Area ID" in bpy.context.object:
            if not "Power" in bpy.context.object:
                if not "Interpolate In (Unused)" in bpy.context.object:
                    layout = self.layout
                    scene = context.scene
                    
                    ### ARGUMENT NAMEN AUS OBJEKT DATABASE NEHMEN
                    
                    obj = context.object

                    if obj is None:
                        layout.label(text="Kein Objekt ausgewählt")
                        return
                    
                    #obj_name = obj.get("Object Name", "Unknown")
                    obj_name = get_base_object_name(obj.name)
                    
                    display_name, labels, notes = load_labels_from_xml(obj_name, 8, False)
                    ##########
                    layout.label(text=f"--- {display_name} ---")
                    
                    layout.prop(bpy.context.workspace, '["Display Notes from SMG Database"]')
                    if bpy.context.workspace["Display Notes from SMG Database"] == True:
                        if notes:
                            import textwrap
                            #layout.label(text="Notes:")
                            #layout.box().label(text=notes, icon='INFO')  # Fügt einen Rahmen um den Notiztext
                            
                            layout.label(text="Notes:")
                            box = layout.box()
                            lines = notes.split("\n")
                            
                            col = box.column(align=True)
                            for line in lines:
                                words = line.split()
                                wrapped_lines = [" ".join(words[i:i+9]) for i in range(0, len(words), 9)]
                                
                                for wrapped_line in wrapped_lines:
                                    col.label(text=wrapped_line)
                    
                    row = layout.row()
                    row.scale_y = 1.2
                    row = layout.prop(bpy.context.object, '["Layer"]')
                    
                    
                    layout.label(text="Settings")
                    row = layout.row()
                    row.scale_y = 1.2
                    row.operator("galaxymaplayout4.layoutstarter4", icon='MOD_LINEART') #change area shape
                    col = layout.column(align=True) 
                    col.prop(bpy.context.object, '["Link ID"]')
                    col.prop(bpy.context.object, '["Path ID"]')
                    col.prop(bpy.context.object, '["Priority"]')
                    col.prop(bpy.context.object, '["Linked Area ID"]')
                    col.prop(bpy.context.object, '["Linked Object ID"]')
                    col.prop(bpy.context.object, '["Linked MapParts ID"]')
                    
                    # layout.label(text="Arguments")
                    # col = layout.column(align=True) 
                    # col.prop(bpy.context.object, '["Obj_Arg0"]')
                    # col.prop(bpy.context.object, '["Obj_Arg1"]')
                    # col.prop(bpy.context.object, '["Obj_Arg2"]')
                    # col.prop(bpy.context.object, '["Obj_Arg3"]')
                    # col.prop(bpy.context.object, '["Obj_Arg4"]')
                    # col.prop(bpy.context.object, '["Obj_Arg5"]')
                    # col.prop(bpy.context.object, '["Obj_Arg6"]')
                    # col.prop(bpy.context.object, '["Obj_Arg7"]')
                    

                    layout.label(text="Arguments")
                    
                    col = layout.column(align=True)
                    for i in range(len(labels)):
                        col.prop(obj, f'["Obj_Arg{i}"]', text=labels[i])
                    

                    
                    layout.label(text="Switches")
                    row = layout.row()
                    row.alignment = 'LEFT'
                    # Erste Spalte für die SW-Werte (größer)
                    col1 = row.column(align=True)
                    col1.scale_x = 2  # Macht die erste Spalte etwas größer
                    col1.prop(context.object, '["SW_APPEAR"]', text="SW_APPEAR")
                    col1.prop(context.object, '["SW_A"]', text="SW_A")
                    col1.prop(context.object, '["SW_B"]', text="SW_B")
                    col1.prop(context.object, '["SW_AWAKE"]', text="SW_AWAKE")

                    # Geteilte Spalten für Z und G
                    split = row.split(factor=0.35)  # Teilt den verbleibenden Platz
                    col2 = split.column(align=True)
                    col2.scale_x = 1
                    col2.operator("galaxymap203.galaxyaddswitchappear", text="Z")
                    col2.operator("galaxymap201.galaxyaddswitcha", text="Z")
                    col2.operator("galaxymap202.galaxyaddswitchb", text="Z")
                    col2.operator("galaxymap205.galaxyaddswitchawake", text="Z")

                    col3 = split.column(align=True)
                    col3.scale_x = 0.004
                    col3.operator("galaxymap303.galaxyaddswitchappearfull", text="G")
                    col3.operator("galaxymap301.galaxyaddswitchafull", text="G")
                    col3.operator("galaxymap302.galaxyaddswitchbfull", text="G")
                    col3.operator("galaxymap305.galaxyaddswitchawakefull", text="G")
                    
                    layout.label(text="Groups")
                    col = layout.column(align=True) 
                    col.prop(bpy.context.object, '["Group ID"]')
                    col.prop(bpy.context.object, '["Clipping Group ID"]')
                    col.prop(bpy.context.object, '["Cutscene Group ID"]')

#    def draw(self, context): #Camera Area
        ### Initialize Name Slots for entering names:
        if "Camera ID" in bpy.context.object:
            if not "Entrance Type" in bpy.context.object:
                layout = self.layout
                scene = context.scene
                
                display_name, labels, notes = load_labels_from_xml("CameraArea", 8, False)
                ##########
                
                layout.label(text=f"--- {display_name} ---")
                layout.prop(bpy.context.workspace, '["Display Notes from SMG Database"]')
                if bpy.context.workspace["Display Notes from SMG Database"] == True:
                    if notes:
                        import textwrap
                        #layout.label(text="Notes:")
                        #layout.box().label(text=notes, icon='INFO')  # Fügt einen Rahmen um den Notiztext
                        
                        layout.label(text="Notes:")
                        box = layout.box()
                        lines = notes.split("\n")
                        
                        col = box.column(align=True)
                        for line in lines:
                            words = line.split()
                            wrapped_lines = [" ".join(words[i:i+9]) for i in range(0, len(words), 9)]
                            
                            for wrapped_line in wrapped_lines:
                                col.label(text=wrapped_line)
                
                row = layout.row()
                row.scale_y = 1.2
                row = layout.prop(bpy.context.object, '["Layer"]')
                
                
                layout.label(text="Settings")
                row = layout.row()
                row.scale_y = 1.2
                row.operator("galaxymaplayout4.layoutstarter4", icon='MOD_LINEART') #change area shape
                col = layout.column(align=True) 
                col.prop(bpy.context.object, '["Link ID"]')
                col.prop(bpy.context.object, '["Linked Area ID"]')
                col.prop(bpy.context.object, '["Linked Object ID]')
                col.prop(bpy.context.object, '["Linked MapParts ID"]')
                col.prop(bpy.context.object, '["Validity"]')
                
                layout.label(text="Arguments")
                col = layout.column(align=True) 
                col.prop(bpy.context.object, '["Camera ID"]')
                col.prop(bpy.context.object, '["Obj_Arg1"]')
                col.prop(bpy.context.object, '["Priority"]')
                col.prop(bpy.context.object, '["Affected Contexts"]')
                
                layout.label(text="Switches")
                row = layout.row()
                row.alignment = 'LEFT'
                # Erste Spalte für die SW-Werte (größer)
                col1 = row.column(align=True)
                col1.scale_x = 2  # Macht die erste Spalte etwas größer
                col1.prop(context.object, '["SW_APPEAR"]', text="SW_APPEAR")
                col1.prop(context.object, '["SW_A"]', text="SW_A")
                col1.prop(context.object, '["SW_B"]', text="SW_B")
                col1.prop(context.object, '["SW_AWAKE"]', text="SW_AWAKE")

                # Geteilte Spalten für Z und G
                split = row.split(factor=0.35)  # Teilt den verbleibenden Platz
                col2 = split.column(align=True)
                col2.scale_x = 1
                col2.operator("galaxymap203.galaxyaddswitchappear", text="Z")
                col2.operator("galaxymap201.galaxyaddswitcha", text="Z")
                col2.operator("galaxymap202.galaxyaddswitchb", text="Z")
                col2.operator("galaxymap205.galaxyaddswitchawake", text="Z")

                col3 = split.column(align=True)
                col3.scale_x = 0.004
                col3.operator("galaxymap303.galaxyaddswitchappearfull", text="G")
                col3.operator("galaxymap301.galaxyaddswitchafull", text="G")
                col3.operator("galaxymap302.galaxyaddswitchbfull", text="G")
                col3.operator("galaxymap305.galaxyaddswitchawakefull", text="G")


#    def draw(self, context): #Spawns
        ### Initialize Name Slots for entering names:
        if "Entrance Type" in bpy.context.object:
            layout = self.layout
            scene = context.scene
            
            display_name, labels, notes = load_labels_from_xml("Mario", 8, False)
            ##########
            
            layout.label(text=f"--- {display_name} ---")
            layout.prop(bpy.context.workspace, '["Display Notes from SMG Database"]')
            if bpy.context.workspace["Display Notes from SMG Database"] == True:
                if notes:
                    import textwrap
                    #layout.label(text="Notes:")
                    #layout.box().label(text=notes, icon='INFO')  # Fügt einen Rahmen um den Notiztext
                    
                    layout.label(text="Notes:")
                    box = layout.box()
                    lines = notes.split("\n")
                    
                    col = box.column(align=True)
                    for line in lines:
                        words = line.split()
                        wrapped_lines = [" ".join(words[i:i+9]) for i in range(0, len(words), 9)]
                        
                        for wrapped_line in wrapped_lines:
                            col.label(text=wrapped_line)
            
            row = layout.row()
            row.scale_y = 1.2
            row = layout.prop(bpy.context.object, '["Layer"]')
            
            
            layout.label(text="Settings")
            col = layout.column(align=True) 
            col.prop(bpy.context.object, '["Entrance Type"]')
            col.prop(bpy.context.object, '["Spawn ID"]')
            col.prop(bpy.context.object, '["Camera ID"]')
            col.prop(bpy.context.object, '["Camera Set ID"]')

#    def draw(self, context): #Cutscenes
        ### Initialize Name Slots for entering names:
        if "Cutscene Name" in bpy.context.object:
            layout = self.layout
            scene = context.scene
            
            ### ARGUMENT NAMEN AUS OBJEKT DATABASE NEHMEN
            
            obj = context.object

            if obj is None:
                layout.label(text="Kein Objekt ausgewählt")
                return
               
            #obj_name = obj.get("Object Name", "Unknown")
            obj_name = get_base_object_name(obj.name)
            
            display_name, labels, notes = load_labels_from_xml(obj_name, 8, False)
            ##########
            
            layout.label(text=f"--- {display_name} ---")
            layout.prop(bpy.context.workspace, '["Display Notes from SMG Database"]')
            if bpy.context.workspace["Display Notes from SMG Database"] == True:
                if notes:
                    import textwrap
                    #layout.label(text="Notes:")
                    #layout.box().label(text=notes, icon='INFO')  # Fügt einen Rahmen um den Notiztext
                    
                    layout.label(text="Notes:")
                    box = layout.box()
                    lines = notes.split("\n")
                    
                    col = box.column(align=True)
                    for line in lines:
                        words = line.split()
                        wrapped_lines = [" ".join(words[i:i+9]) for i in range(0, len(words), 9)]
                        
                        for wrapped_line in wrapped_lines:
                            col.label(text=wrapped_line)
            
            row = layout.row()
            row.scale_y = 1.2
            row = layout.prop(bpy.context.object, '["Layer"]')
            
            layout.label(text="Switches")
            row = layout.row()
            row.alignment = 'LEFT'
            # Erste Spalte für die SW-Werte (größer)
            col1 = row.column(align=True)
            col1.scale_x = 2  # Macht die erste Spalte etwas größer
            col1.prop(context.object, '["SW_APPEAR"]', text="SW_APPEAR")
            col1.prop(context.object, '["SW_DEAD"]', text="SW_DEAD")
            col1.prop(context.object, '["SW_A"]', text="SW_A")
            col1.prop(context.object, '["SW_B"]', text="SW_B")

            # Geteilte Spalten für Z und G
            split = row.split(factor=0.35)  # Teilt den verbleibenden Platz
            col2 = split.column(align=True)
            col2.scale_x = 1
            col2.operator("galaxymap203.galaxyaddswitchappear", text="Z")
            col2.operator("galaxymap204.galaxyaddswitchdead", text="Z")
            col2.operator("galaxymap201.galaxyaddswitcha", text="Z")
            col2.operator("galaxymap202.galaxyaddswitchb", text="Z")

            col3 = split.column(align=True)
            col3.scale_x = 0.004
            col3.operator("galaxymap303.galaxyaddswitchappearfull", text="G")
            col3.operator("galaxymap304.galaxyaddswitchdeadfull", text="G")
            col3.operator("galaxymap301.galaxyaddswitchafull", text="G")
            col3.operator("galaxymap302.galaxyaddswitchbfull", text="G")

            
            layout.label(text="Settings")
            col = layout.column(align=True) 
            col.prop(bpy.context.object, '["Cutscene Name"]')
            col.prop(bpy.context.object, '["Sheet Name"]')
            col.prop(bpy.context.object, '["Skippable"]')
            col.prop(bpy.context.object, '["Link ID"]')

#    def draw(self, context): #Positions
        ### Initialize Name Slots for entering names:
        if "Position Name" in bpy.context.object:
            layout = self.layout
            scene = context.scene
            
            ### ARGUMENT NAMEN AUS OBJEKT DATABASE NEHMEN
            
            obj = context.object

            if obj is None:
                layout.label(text="Kein Objekt ausgewählt")
                return
              
            #obj_name = obj.get("Object Name", "Unknown")
            obj_name = get_base_object_name(obj.name)
            
            display_name, labels, notes = load_labels_from_xml(obj_name, 8, False)
            ##########
            
            layout.label(text=f"--- {display_name} ---")
            layout.prop(bpy.context.workspace, '["Display Notes from SMG Database"]')
            if bpy.context.workspace["Display Notes from SMG Database"] == True:
                if notes:
                    import textwrap
                    #layout.label(text="Notes:")
                    #layout.box().label(text=notes, icon='INFO')  # Fügt einen Rahmen um den Notiztext
                    
                    layout.label(text="Notes:")
                    box = layout.box()
                    lines = notes.split("\n")
                    
                    col = box.column(align=True)
                    for line in lines:
                        words = line.split()
                        wrapped_lines = [" ".join(words[i:i+9]) for i in range(0, len(words), 9)]
                        
                        for wrapped_line in wrapped_lines:
                            col.label(text=wrapped_line)
            
            row = layout.row()
            row.scale_y = 1.2
            row = layout.prop(bpy.context.object, '["Layer"]')
            
            layout.label(text="Settings")
            col = layout.column(align=True) 
            col.prop(bpy.context.object, '["Position Name"]')
            col.prop(bpy.context.object, '["Linked Object ID"]')
            
#    def draw(self, context): #Debug
        ### Initialize Name Slots for entering names:
        if "Link ID" in bpy.context.object:
            if not "SW_APPEAR" in bpy.context.object:
                layout = self.layout
                scene = context.scene
            
            
                row = layout.row()
                row.scale_y = 1.2
                row = layout.prop(bpy.context.object, '["Layer"]')
            
                layout.label(text="Settings")
                row = layout.row()
                row.scale_y = 1.2
                row = layout.prop(bpy.context.object, '["Link ID"]')
            
#    def draw(self, context): #Paths
        ### Initialize Name Slots for entering names:
        if "PathArg0 (Posture Type)" in bpy.context.object:
            layout = self.layout
            scene = context.scene
            
            
            row = layout.row()
            row.scale_y = 1.2
            row = layout.prop(bpy.context.object, '["Layer"]') #ID muss noch
            
            row = layout.row()
            row.scale_y = 1.2
            row = layout.prop(bpy.context.object, '["Usage"]')
            
            layout.label(text="Path Arguments")
            col = layout.column(align=True)
            col.prop(bpy.context.object, '["PathArg0 (Posture Type)"]', text="Posture Type")
            col.prop(bpy.context.object, '["PathArg1 (Stop Motion Type)"]', text="Posture Type")
            col.prop(bpy.context.object, '["PathArg2 (Guide Type)"]', text="Guide Type")
            col.prop(bpy.context.object, '["PathArg3"]')
            col.prop(bpy.context.object, '["PathArg4 (Initial Position Type)"]', text="Initial Position Type")
            col.prop(bpy.context.object, '["PathArg5"]')
            col.prop(bpy.context.object, '["PathArg6"]')
            col.prop(bpy.context.object, '["PathArg7"]')
            
            layout.label(text="Point Settings")
            # row = layout.row()
            # row.scale_y = 1.2
            # row.operator("galaxymap77.galaxyaddpathsetup", icon='MOD_LINEART')
            
            point, spline_type = get_selected_spline_point()
            if point:
                index = get_selected_spline_pointid()
                if index is not None:
                    layout.label(text=f"[ ID: {index}] ")
                # Radius Berechnung
                PointStopArg = -1 if point.radius >= 1.0 else round(float(point.radius) * 10000)  #point.radius * 1000
                PointSpeedArg = int(round((math.degrees(point.tilt))))
                

                if str(index) in context.object.modifiers:
                    if bpy.context.object.modifiers[str(index)]["Input_10"] == 0:
                        col = layout.column(align=True)
                        col.label(text="Speed:")
                        split = layout.split() #Splitte Rows
                        col = split.column(align=True)
                        col.prop(point, "tilt", text="Movement Speed", icon="SORTTIME")
                        col.prop(point, "radius", text="Stop Time", icon="TRACKING_CLEAR_FORWARDS")
                        col = split.column(align=True)
                        col.label(text=f"Speed: {PointSpeedArg}")
                        col.label(text=f"Stop: {PointStopArg}")
                        col = layout.column(align=True)
                        col.prop(bpy.context.object.modifiers[str(index)], '["Input_4"]', icon="SORTTIME", text="Acceleration Time")

                        col.label(text="Rotation:")
                        col.prop(bpy.context.object.modifiers[str(index)], '["Input_5"]', text="Speed", icon="MOD_TIME")
                        col.prop(bpy.context.object.modifiers[str(index)], '["Input_6"]', text="Angle", icon="TRACKING_REFINE_FORWARDS")
                        split = layout.split() #Splitte Rows
                        col = split.column(align=True)
                        col.prop(bpy.context.object.modifiers[str(index)], '["Input_7"]', text="Axis", icon="CON_ROTLIMIT")
                        col.prop(bpy.context.object.modifiers[str(index)], '["Input_9"]', text="Type", icon="TRACKING_BACKWARDS")
                        col = split.column(align=True)
                        if bpy.context.object.modifiers[str(index)]["Input_7"] == 0:
                            col.label(text=f"X Axis")
                        else:
                            if bpy.context.object.modifiers[str(index)]["Input_7"] == 1:
                                col.label(text=f"Y Axis")
                            else:
                                if bpy.context.object.modifiers[str(index)]["Input_7"] == 2:
                                    col.label(text=f"Z Axis")
                                else:
                                    col.label(text=f"Axis not set")
                        if bpy.context.object.modifiers[str(index)]["Input_9"] == -1:
                            col.label(text=f"Stop and Rotate")
                        else:
                            if bpy.context.object.modifiers[str(index)]["Input_9"] == 1:
                                col.label(text=f"Rotate between points")
                            else:
                                col.label(text=f"Tyoe not set")
                        col = layout.column(align=True)
                        row = layout.row()
                        row.scale_y = 1.2
                        row.prop(bpy.context.object.modifiers[str(index)], '["Input_10"]', text="Speed Type [Speed]", icon="TRACKING_CLEAR_FORWARDS")
                    else: #1
                        col = layout.column(align=True)
                        col.label(text="Speed:")
                        split = layout.split() #Splitte Rows
                        col = split.column(align=True)
                        col.prop(point, "tilt", text="Movement Time", icon="SORTTIME")
                        col.prop(point, "radius", text="Stop Time", icon="TRACKING_CLEAR_FORWARDS")
                        col = split.column(align=True)
                        col.label(text=f"Frames: {PointSpeedArg}")
                        col.label(text=f"Stop: {PointStopArg}")
                        col = layout.column(align=True)
                        col.prop(bpy.context.object.modifiers[str(index)], '["Input_4"]', icon="SORTTIME", text="Acceleration Time")
                        col.label(text="Rotation:")
                        col.prop(bpy.context.object.modifiers[str(index)], '["Input_5"]', text="Time", icon="MOD_TIME")
                        col.prop(bpy.context.object.modifiers[str(index)], '["Input_6"]', text="Angle", icon="TRACKING_REFINE_FORWARDS")
                        split = layout.split() #Splitte Rows
                        col = split.column(align=True)
                        col.prop(bpy.context.object.modifiers[str(index)], '["Input_7"]', text="Axis", icon="CON_ROTLIMIT")
                        col.prop(bpy.context.object.modifiers[str(index)], '["Input_9"]', text="Type", icon="TRACKING_BACKWARDS")
                        col = split.column(align=True)
                        if bpy.context.object.modifiers[str(index)]["Input_7"] == 0:
                            col.label(text=f"X Axis")
                        else:
                            if bpy.context.object.modifiers[str(index)]["Input_7"] == 1:
                                col.label(text=f"Y Axis")
                            else:
                                if bpy.context.object.modifiers[str(index)]["Input_7"] == 2:
                                    col.label(text=f"Z Axis")
                                else:
                                    col.label(text=f"Axis not set")
                        if bpy.context.object.modifiers[str(index)]["Input_9"] == -1:
                            col.label(text=f"Stop and Rotate")
                        else:
                            if bpy.context.object.modifiers[str(index)]["Input_9"] == 1:
                                col.label(text=f"Rotate between points")
                            else:
                                col.label(text=f"Tyoe not set")
                        col = layout.column(align=True)
                        row = layout.row()
                        row.scale_y = 1.2
                        row.prop(bpy.context.object.modifiers[str(index)], '["Input_10"]', text="Speed Type [Time]", icon="TRACKING_CLEAR_FORWARDS")
                else:
                    col = layout.column(align=True)
                    split = layout.split() #Splitte Rows
                    col = split.column(align=True)
                    col.prop(point, "tilt", text="Speed", icon="SORTTIME")
                    col.prop(point, "radius", text="Stop Time", icon="TRACKING_CLEAR_FORWARDS")
                    col = split.column(align=True)
                    col.label(text=f"Result: {PointSpeedArg}")
                    col.label(text=f"Result: {PointStopArg}")
                    layout.label(text="")
                    row = layout.row()
                    row.scale_y = 1.2
                    row.operator("galaxymap77.galaxyaddpathsetup", icon='MOD_LINEART', text="Add complex point settings")
                #col.prop(bpy.context.object.modifiers["GRAVITY"], '["Input_3"]', text="Distance")
                

            else:
                layout.label(text="No Point Selected")
            

 #Gravity
        ### Initialize Name Slots for entering names:
        if "Inverse" in bpy.context.object:
            layout = self.layout
            scene = context.scene
            
            ### ARGUMENT NAMEN AUS OBJEKT DATABASE NEHMEN
            
            obj = context.object

            if obj is None:
                layout.label(text="Kein Objekt ausgewählt")
                return
            
            #obj_name = obj.get("Object Name", "Unknown")
            
            obj_name = obj.modifiers["GRAVITY"].node_group.name
            if obj.modifiers["GRAVITY"].node_group.name == "GlobalPlaneGravity":
				#Sphere
                if obj.modifiers["GRAVITY"]["Input_10"] == 0:
                    if obj.modifiers["GRAVITY"]["Input_11"] == 0:
                        obj_name = "GlobalPlaneGravity"
                    else:
                        obj_name = "ZeroGravitySphere"
				#Cube
                if obj.modifiers["GRAVITY"]["Input_10"] == 1:
                    if obj.modifiers["GRAVITY"]["Input_11"] == 0:
                        obj_name = "GlobalPlaneGravityInBox"
                    else:
                        obj_name = "ZeroGravityBox"
				#Cylinder
                if obj.modifiers["GRAVITY"]["Input_10"] == 2:
                    if obj.modifiers["GRAVITY"]["Input_11"] == 0:
                        obj_name = "GlobalPlaneGravityInCylinder"
                    else:
                        obj_name = "ZeroGravityCylinder"
            
            display_name, labels, notes = load_labels_from_xml(obj_name, 4, True)
            
            ##########
                        
            layout.label(text=f"--- {display_name} ---")
            layout.prop(bpy.context.workspace, '["Display Notes from SMG Database"]')
            if bpy.context.workspace["Display Notes from SMG Database"] == True:
                if notes:
                    import textwrap
                    #layout.label(text="Notes:")
                    #layout.box().label(text=notes, icon='INFO')  # Fügt einen Rahmen um den Notiztext
                    
                    layout.label(text="Notes:")
                    box = layout.box()
                    lines = notes.split("\n")
                    
                    col = box.column(align=True)
                    for line in lines:
                        words = line.split()
                        wrapped_lines = [" ".join(words[i:i+9]) for i in range(0, len(words), 9)]
                        
                        for wrapped_line in wrapped_lines:
                            col.label(text=wrapped_line)
            
            row = layout.row()
            row.scale_y = 1.2
            row = layout.prop(bpy.context.object, '["Layer"]')
            
            
            layout.label(text="Settings")
            col = layout.column(align=True)
            col.prop(bpy.context.object, '["Link ID"]')
            col.prop(bpy.context.object, '["Path ID"]')
            col.prop(bpy.context.object, '["Linked Area ID"]')
            col.prop(bpy.context.object, '["Linked Object ID]')
            col.prop(bpy.context.object, '["Linked MapParts ID"]')
            
            layout.label(text="Gravity Settings")
            col = layout.column(align=True)
            col.prop(bpy.context.object, '["Power"]')
            col.prop(bpy.context.object, '["Priority"]')
            col.prop(bpy.context.object, '["Inverse"]')
            col.prop(bpy.context.object, '["Type"]')
            col.prop(bpy.context.object.modifiers["GRAVITY"], '["Input_2"]', text="Range")
            col.prop(bpy.context.object.modifiers["GRAVITY"], '["Input_3"]', text="Distance")
            
            col = layout.column(align=True)
            for i in range(len(labels)):
                inputbla = i + 4
                col.prop(obj.modifiers["GRAVITY"], f'["Input_{inputbla}"]', text=labels[i])
            
            
            
            col.prop(bpy.context.object.modifiers["GRAVITY"], '["Input_8"]', text="Scale")
            
            if obj.modifiers["GRAVITY"].node_group.name == "GlobalWireGravity":
                col.prop(bpy.context.object.modifiers["GRAVITY"], '["Input_9"]', text="Path ID")
            
            row = layout.row()
            row.scale_y = 1.2
            row = layout.prop(bpy.context.object.modifiers["GRAVITY"], '["Input_10"]', text="Shape (Only planar)")
            
            row = layout.row()
            row.scale_y = 1.2
            row = layout.prop(bpy.context.object.modifiers["GRAVITY"], '["Input_11"]', text="Zero Gravity? (Only planar)")
            
            
            

            
            
            layout.label(text="Switches")
            row = layout.row()
            row.alignment = 'LEFT'
            # Erste Spalte für die SW-Werte (größer)
            col1 = row.column(align=True)
            col1.scale_x = 2  # Macht die erste Spalte etwas größer
            col1.prop(context.object, '["SW_APPEAR"]', text="SW_APPEAR")
            col1.prop(context.object, '["SW_DEAD"]', text="SW_DEAD")
            col1.prop(context.object, '["SW_A"]', text="SW_A")
            col1.prop(context.object, '["SW_B"]', text="SW_B")
            col1.prop(context.object, '["SW_AWAKE"]', text="SW_AWAKE")

            # Geteilte Spalten für Z und G
            split = row.split(factor=0.35)  # Teilt den verbleibenden Platz
            col2 = split.column(align=True)
            col2.scale_x = 1
            col2.operator("galaxymap203.galaxyaddswitchappear", text="Z")
            col2.operator("galaxymap204.galaxyaddswitchdead", text="Z")
            col2.operator("galaxymap201.galaxyaddswitcha", text="Z")
            col2.operator("galaxymap202.galaxyaddswitchb", text="Z")
            col2.operator("galaxymap205.galaxyaddswitchawake", text="Z")

            col3 = split.column(align=True)
            col3.scale_x = 0.004
            col3.operator("galaxymap303.galaxyaddswitchappearfull", text="G")
            col3.operator("galaxymap304.galaxyaddswitchdeadfull", text="G")
            col3.operator("galaxymap301.galaxyaddswitchafull", text="G")
            col3.operator("galaxymap302.galaxyaddswitchbfull", text="G")
            col3.operator("galaxymap305.galaxyaddswitchawakefull", text="G")
            
            layout.label(text="Groups")
            col = layout.column(align=True)
            col.prop(bpy.context.object, '["Group ID"]')
            col.prop(bpy.context.object, '["Clipping Group ID"]')
            col.prop(bpy.context.object, '["Cutscene Group ID"]')




class LayoutSMGMapScenarioPanel(bpy.types.Panel):


    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Scenario"
    bl_idname = "SCENE_GalaxyMapScenario_layout" 
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Mario Galaxy"

    def draw(self, context):
    
        if "Comet Time Limit" in bpy.context.view_layer:
        
            layout = self.layout
            scene = context.scene
        
            layout.label(text="Settings")
            split = layout.split() #Splitte Rows
            col = split.column(align=True)
            col.prop(bpy.context.view_layer, '["ScenarioNo"]')
            col = split.column(align=True)
            col.prop(bpy.context.view_layer, '["ScenarioName"]')
            
            row = layout.row()
            row.scale_y = 1.2
            row = layout.prop(bpy.context.view_layer, '["StarMask"]')
            
            col = layout.column(align=True) 
            col.prop(bpy.context.view_layer, '["Scenario Type"]')
            col.prop(bpy.context.view_layer, '["Power Star Trigger"]')
            col.prop(bpy.context.view_layer, '["Comet"]')
            col.prop(bpy.context.view_layer, '["Comet Time Limit"]')
            col.prop(bpy.context.view_layer, '["LuigiModeTimer (unused)"]')
            
            layout.label(text="Zone Layer Display")
            layout.label(text="(Select Zone Collection)")
            

            if "Zone ID" in bpy.context.collection:
                if bpy.context.collection.name in bpy.context.view_layer:

                    ZoneMaskName = bpy.context.collection.name
                    row = layout.row()
                    row.scale_y = 1.2
                    row = layout.prop(bpy.context.view_layer, '["' + ZoneMaskName + '"]')
                else:
                    row = layout.row()
                    row.scale_y = 1.2
                    row = layout.label(text="Zone not in scenario!")
                    row = layout.row()
                    row.scale_y = 1.2
                    row.operator("scenario55.addzone", icon='ADD') #new zone

        else:
            layout = self.layout
            scene = context.scene
        
            layout.label(text="View Layer is no guilty Galaxy mission")
            
            
class LayoutSMGMapMenu1(bpy.types.Menu):
    bl_label = "Add Mario Galaxy Object Properties for your collection asset"
    bl_idname = "OBJECT_MT_simple_custom_menu1"

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("galaxymap50.add_obj_props")
        row = layout.row()
        row.operator("galaxymap51.add_mappart_props")

class LayoutSMGMap_AddObjPanel(bpy.types.Menu):
    bl_label = "Add Mario Galaxy Object"
    bl_idname = "OBJECT_MT_simple_custom_menu2"

    def draw(self, context):
        layout = self.layout
        
        if "Zone ID" in bpy.context.collection:
            LayoutZoneName = bpy.context.collection.name
        else:
            LayoutZoneName = "NO VALID ZONE SELECTED"
         
        if "Asset Searching Enabled" in bpy.context.workspace:
            if bpy.context.workspace["Asset Searching Enabled"] == 1: 
                LayoutAssetSearch = "Enabled"
            else:
                LayoutAssetSearch = "Disabled"
        else:
            LayoutAssetSearch = "Disabled"
         
         
         
        layout.label(text="To Zone: "+LayoutZoneName, icon='OUTLINER_COLLECTION')
        layout.label(text="Asset Searching "+LayoutAssetSearch, icon='VIEWZOOM')
        #layout.prop(bpy.context.workspace, '["Add this object"]')
        #layout.prop(bpy.context.workspace, '["Asset Searching Enabled"]')
        layout.operator("galaxymap1.galaxyaddobj", icon='GHOST_DISABLED')
        layout.operator("galaxymap2.galaxyaddmappart", icon='AUTO')
        # use an operator enum property to populate a sub-menu #Kapier ich nicht
        # layout.operator_menu_enum("galaxymap3.galaxyaddgravity",
                                  # property="type",
                                  # text="Gravity",
                                  # ) 
        layout.operator("galaxymap4.galaxyaddarea", icon='MATCUBE')
        layout.operator("galaxymap5.galaxyaddcamera", icon='CAMERA_DATA')
        layout.operator("galaxymap6.galaxyaddstart", icon='ARMATURE_DATA')
        #layout.operator("galaxymap7.galaxyaddcutscene", icon='SEQUENCE')
        layout.operator("galaxymaplayout3.layoutstarter3", icon='FILE_MOVIE')
        layout.operator("galaxymap8.galaxyaddposition", icon='IMPORT')
        layout.operator("galaxymap9.galaxyadddebug", icon='MODIFIER_OFF')
        #layout.operator("GalaxyMap9.AddDebug")
        layout.operator("galaxymap10.galaxyaddpath", icon='MOD_CURVE')
        
        #layout.operator("galaxymap3.galaxyaddgravity", icon='PIVOT_CURSOR')
        #layout.operator("smgmap2.addgravityselect", icon='PIVOT_CURSOR')
        layout.operator("galaxymaplayout2.layoutstarter2", icon='PIVOT_CURSOR')
        
class LayoutSMGMap_AddObjPanelStarter(bpy.types.Menu):
    bl_label = "komm"
    bl_idname = "ewwewe.OBJECT_MT_simple_custom_menu3"

    def draw(self, context):
        print("sack")
        #bpy.ops.wm.call_menu(name=LayoutSMGMap_AddObjPanel.bl_idname)
        
class LayoutSMGMap_AddGravityPanel(bpy.types.Menu):
    """Gravity"""
    bl_label = "Gravity"
    bl_idname = "smgmap2.addgravityselect"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Gravity", icon='PROP_OFF')
        layout.operator("galaxymap11.galaxyadd_globalplanegravity", icon='ALIGN_BOTTOM')
        layout.operator("galaxymap12.galaxyadd_globalpointgravity", icon='META_BALL')
        layout.operator("galaxymap13.galaxyadd_globalcubegravity", icon='META_CUBE')
        layout.operator("galaxymap14.galaxyadd_globalsegmentgravity", icon='META_CAPSULE')
        layout.operator("galaxymap15.galaxyadd_globaldiskgravity", icon='META_ELLIPSOID')
        layout.operator("galaxymap16.galaxyadd_globaldisktorusgravity", icon='MESH_TORUS')
        layout.operator("galaxymap17.galaxyadd_globalconegravity", icon='CONE')
        layout.operator("galaxymap18.galaxyadd_globalbarrelgravity", icon='MESH_CYLINDER')
        layout.operator("galaxymap19.galaxyadd_globalwiregravity", icon='MOD_SKIN')

class LayoutSMGMap_AddCutscenePanel(bpy.types.Menu):
    bl_label = "Cutscene"
    bl_idname = "smgmap3.addcutsceneselect"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Select cutscene type", icon='WORLD_DATA')
        layout.operator("galaxymap20.galaxyadd_cutscene", icon='SEQUENCE')
        layout.operator("galaxymap21.galaxyadd_cutscenesub", icon='FILE_MOVIE')

class LayoutSMGMap_ChangeAreaShapePanel(bpy.types.Menu):
    bl_label = "Change Area Shape"
    bl_idname = "smgmap10.changeareashape"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Select new shape", icon='WORLD_DATA')
        layout.operator("smgmaparea0.changeto0", icon='CUBE')
        #layout.operator("smgmaparea1.changeto1", icon='LIGHTPROBE_CUBEMAP') # Alte Blenderversion
        layout.operator("smgmaparea1.changeto1", icon='LIGHTPROBE_SPHERE')
        layout.operator("smgmaparea2.changeto2", icon='SPHERE')
        layout.operator("smgmaparea3.changeto3", icon='MESH_CYLINDER')
        layout.operator("smgmaparea4.changeto4", icon='MOD_SOFT')

###Register -----------------------------------------------------

def register():
    bpy.utils.register_class(GalaxyMapOperator1)
    bpy.utils.register_class(GalaxyMapOperator2)
    bpy.utils.register_class(GalaxyMapOperator3)
    bpy.utils.register_class(GalaxyMapOperator4)
    bpy.utils.register_class(GalaxyMapOperator5)
    bpy.utils.register_class(GalaxyMapOperator6)
    bpy.utils.register_class(GalaxyMapOperator7)
    bpy.utils.register_class(GalaxyMapOperator8)
    bpy.utils.register_class(GalaxyMapOperator9)
    bpy.utils.register_class(GalaxyMapOperator10)
    bpy.utils.register_class(GalaxyMapOperator11)
    bpy.utils.register_class(GalaxyMapOperator12)
    bpy.utils.register_class(GalaxyMapOperator13)
    
    #bpy.utils.register_class(GalaxyMapOperator20)
    bpy.utils.register_class(GalaxyMapOperator40)
    
    bpy.utils.register_class(GalaxyMapAddObject)
    bpy.utils.register_class(GalaxyMapAddMapPart)
    #bpy.utils.register_class(GalaxyMapAddGravity)
    bpy.utils.register_class(GalaxyMapAddArea)
    bpy.utils.register_class(GalaxyMapAddCamera)
    bpy.utils.register_class(GalaxyMapAddStart)
    #bpy.utils.register_class(GalaxyMapAddCutscene)
    bpy.utils.register_class(GalaxyMapAddPosition)
    bpy.utils.register_class(GalaxyMapAddDebug)
    bpy.utils.register_class(GalaxyMapAddPath)
    bpy.utils.register_class(GalaxyMapAddPathPointSetup)
    
    bpy.utils.register_class(GalaxyMap_AddMapPartProps)
    bpy.utils.register_class(GalaxyMap_AddObjProps)
    
    
    bpy.utils.register_class(AddZoneToScenario)
    
    bpy.utils.register_class(WM_OT_myOp)
    

    bpy.utils.register_class(LayoutSMGMapPanel)
    bpy.utils.register_class(LayoutSMGMapObjectPanel)
    bpy.utils.register_class(LayoutSMGMapMenu1)
    bpy.utils.register_class(LayoutSMGMap_AddObjPanel)
    bpy.utils.register_class(LayoutSMGMap_AddObjPanelStarter)
    bpy.utils.register_class(LayoutSMGMap_AddGravityPanel)
    bpy.utils.register_class(LayoutSMGMap_AddCutscenePanel)
    bpy.utils.register_class(LayoutSMGMap_ChangeAreaShapePanel)
    bpy.utils.register_class(LayoutSMGMapScenarioPanel)
    
    
    
    bpy.utils.register_class(GalaxyMap_LayoutStarter2)
    bpy.utils.register_class(GalaxyMap_LayoutStarter3)
    bpy.utils.register_class(GalaxyMap_LayoutStarter4)

    bpy.utils.register_class(GalaxyMapAddGravity_Planar)
    bpy.utils.register_class(GalaxyMapAddGravity_Sphere)
    bpy.utils.register_class(GalaxyMapAddGravity_Cube)
    bpy.utils.register_class(GalaxyMapAddGravity_Cylinder)
    bpy.utils.register_class(GalaxyMapAddGravity_Disk)
    bpy.utils.register_class(GalaxyMapAddGravity_Donut)
    bpy.utils.register_class(GalaxyMapAddGravity_Cone)
    bpy.utils.register_class(GalaxyMapAddGravity_Barrel)
    bpy.utils.register_class(GalaxyMapAddGravity_Wire)
    bpy.utils.register_class(GalaxyMapAddCutscene_Normal)
    bpy.utils.register_class(GalaxyMapAddCutscene_Sub)
    
    bpy.utils.register_class(GalaxyMapChangeAreaShape_0)
    bpy.utils.register_class(GalaxyMapChangeAreaShape_1)
    bpy.utils.register_class(GalaxyMapChangeAreaShape_2)
    bpy.utils.register_class(GalaxyMapChangeAreaShape_3)
    bpy.utils.register_class(GalaxyMapChangeAreaShape_4)
    
    

    bpy.utils.register_class(GalaxyMapNewSwitch_A)
    bpy.utils.register_class(GalaxyMapNewSwitch_B)
    bpy.utils.register_class(GalaxyMapNewSwitch_Appear)
    bpy.utils.register_class(GalaxyMapNewSwitch_Dead)
    bpy.utils.register_class(GalaxyMapNewSwitch_Awake)
    bpy.utils.register_class(GalaxyMapNewSwitch_Param)
    
    bpy.utils.register_class(GalaxyMapNewSwitch_A_FullGalaxy)
    bpy.utils.register_class(GalaxyMapNewSwitch_B_FullGalaxy)
    bpy.utils.register_class(GalaxyMapNewSwitch_Appear_FullGalaxy)
    bpy.utils.register_class(GalaxyMapNewSwitch_Dead_FullGalaxy)
    bpy.utils.register_class(GalaxyMapNewSwitch_Awake_FullGalaxy)
    bpy.utils.register_class(GalaxyMapNewSwitch_Param_FullGalaxy)
    
    #bpy.types.VIEW3D_MT_object.append(menu_func)
    #bpy.utils.register_class(GalaxyMapInitialize)
    
def unregister():
    bpy.utils.unregister_class(GalaxyMapOperator1)
    bpy.utils.unregister_class(GalaxyMapOperator2)
    bpy.utils.unregister_class(GalaxyMapOperator3)
    bpy.utils.unregister_class(GalaxyMapOperator4)
    bpy.utils.unregister_class(GalaxyMapOperator5)
    bpy.utils.unregister_class(GalaxyMapOperator6)
    bpy.utils.unregister_class(GalaxyMapOperator7)
    bpy.utils.unregister_class(GalaxyMapOperator8)
    bpy.utils.unregister_class(GalaxyMapOperator9)
    bpy.utils.unregister_class(GalaxyMapOperator10)
    bpy.utils.unregister_class(GalaxyMapOperator11)
    bpy.utils.unregister_class(GalaxyMapOperator12)
    bpy.utils.unregister_class(GalaxyMapOperator13)
    
    #bpy.utils.unregister_class(GalaxyMapOperator20)
    bpy.utils.unregister_class(GalaxyMapOperator40)
    
    bpy.utils.unregister_class(GalaxyMapAddObject)
    bpy.utils.unregister_class(GalaxyMapAddMapPart)
    #bpy.utils.unregister_class(GalaxyMapAddGravity)
    bpy.utils.unregister_class(GalaxyMapAddArea)
    bpy.utils.unregister_class(GalaxyMapAddCamera)
    bpy.utils.unregister_class(GalaxyMapAddStart)
    #bpy.utils.unregister_class(GalaxyMapAddCutscene)
    bpy.utils.unregister_class(GalaxyMapAddPosition)
    bpy.utils.unregister_class(GalaxyMapAddDebug)
    bpy.utils.unregister_class(GalaxyMapAddPath)
    bpy.utils.register_class(GalaxyMapAddPathPointSetup)
    bpy.utils.unregister_class(GalaxyMapAddCutscene_Normal)
    bpy.utils.unregister_class(GalaxyMapAddCutscene_Sub)
    
    bpy.utils.register_class(GalaxyMapChangeAreaShape_0)
    bpy.utils.register_class(GalaxyMapChangeAreaShape_1)
    bpy.utils.register_class(GalaxyMapChangeAreaShape_2)
    bpy.utils.register_class(GalaxyMapChangeAreaShape_3)
    bpy.utils.register_class(GalaxyMapChangeAreaShape_4)
    
    bpy.utils.unregister_class(GalaxyMap_AddMapPartProps)
    bpy.utils.unregister_class(GalaxyMap_AddObjProps)
    
    bpy.utils.unregister_class(AddZoneToScenario)
    
    bpy.utils.unregister_class(WM_OT_myOp)


    bpy.utils.unregister_class(LayoutSMGCMapPanel)
    bpy.utils.unregister_class(LayoutSMGMapObjectPanel)
    bpy.utils.unregister_class(LayoutSMGMapMenu1)
    bpy.utils.unregister_class(LayoutSMGMap_AddObjPanel)
    bpy.utils.unregister_class(LayoutSMGMap_AddObjPanelStarter)
    bpy.utils.unregister_class(LayoutSMGMap_AddGravityPanel)
    bpy.utils.unregister_class(LayoutSMGMap_AddCutscenePanel)
    bpy.utils.unregister_class(LayoutSMGMap_ChangeAreaShapePanel)
    bpy.utils.unregister_class(LayoutSMGMapScenarioPanel)
    
    
    bpy.utils.unregister_class(GalaxyMap_LayoutStarter2)
    bpy.utils.unregister_class(GalaxyMap_LayoutStarter3)
    bpy.utils.unregister_class(GalaxyMap_LayoutStarter4)
    
    bpy.utils.unregister_class(GalaxyMapAddGravity_Planar)
    bpy.utils.unregister_class(GalaxyMapAddGravity_Sphere)
    bpy.utils.unregister_class(GalaxyMapAddGravity_Cube)
    bpy.utils.unregister_class(GalaxyMapAddGravity_Cylinder)
    bpy.utils.unregister_class(GalaxyMapAddGravity_Disk)
    bpy.utils.unregister_class(GalaxyMapAddGravity_Donut)
    bpy.utils.unregister_class(GalaxyMapAddGravity_Cone)
    bpy.utils.unregister_class(GalaxyMapAddGravity_Barrel)
    bpy.utils.unregister_class(GalaxyMapAddGravity_Wire)
    
    
    bpy.utils.unregister_class(GalaxyMapNewSwitch_A)
    bpy.utils.unregister_class(GalaxyMapNewSwitch_B)
    bpy.utils.unregister_class(GalaxyMapNewSwitch_Appear)
    bpy.utils.unregister_class(GalaxyMapNewSwitch_Dead)
    bpy.utils.unregister_class(GalaxyMapNewSwitch_Awake)
    bpy.utils.unregister_class(GalaxyMapNewSwitch_Param)
    
    bpy.utils.unregister_class(GalaxyMapNewSwitch_A_FullGalaxy)
    bpy.utils.unregister_class(GalaxyMapNewSwitch_B_FullGalaxy)
    bpy.utils.unregister_class(GalaxyMapNewSwitch_Appear_FullGalaxy)
    bpy.utils.unregister_class(GalaxyMapNewSwitch_Dead_FullGalaxy)
    bpy.utils.unregister_class(GalaxyMapNewSwitch_Awake_FullGalaxy)
    bpy.utils.unregister_class(GalaxyMapNewSwitch_Param_FullGalaxy)
    
    #bpy.types.VIEW3D_MT_object.remove(menu_func)
    #bpy.utils.unregister_class(GalaxyMapInitialize)
    

if __name__ == "__main__":
    register()
