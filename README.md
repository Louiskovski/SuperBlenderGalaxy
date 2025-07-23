# Mario Galaxy Map Editor / Converter Addon for Blender

![screenshot](pictureC.png)

Transforms Blender into a Mario Galaxy Level Editor, taking full advantage of its asset functionality and controls.

Still pretty WIP. Make backups of your levels. Updates come regularly.

# Preparation

- Download GALAXYMAP_EDITOR-ASSETS.blend file
- Install [Pymap](https://github.com/SunakazeKun/pyjmap)
- Download [WiiExplorer](https://github.com/SuperHackio/WiiExplorer)
- Download [LaunchCamPlus](https://github.com/SuperHackio/LaunchCamPlus) (optional)
- Download the text files and place these in the same directory as the WiiExplorer.exe

Now start Blender and install the addon
- In the 3D View on the right click on the *Mario Galaxy* tab and enter the required paths at the *path* column

## Dolphin Note

You can edit and even export the level while the game is running in the Dolphin emulator. To get the level changes ingame, exit and re-enter the level.

# Importing Levels

Before doing anything, save your Blender file.

You can import full galaxies and/or individual zones. Simply enter the zone or galaxy name and click on Import Galaxy or Import Zone.
If **Asset Searching Enabled** is set to 1, the plugin searches for assets in a given folder structure using the levels object names in Blender files and links them. More about this at **Asset Usage**.

### Galaxy Level Engine Note

Support for [Galaxy Level Engine](https://github.com/SuperHackio/GalaxyLevelEngine) maps is also supported. Its relevant information can be found in the *GLE* Collection of the zone.


# Exporting Levels

If you click on **Export Galaxy**, all zones will be exported and saved into your StageData filesystem. To export a single zone, select the collection with the zone name and click on **Export Zone**

Your blender file needs to be saved in order to do this.
# Creating new levels

To create a brand new level, start with a new Blender file and click on **Create brand new galaxy**. This creates a new scene with a new scenario and a main zone. Now you can add several new zones with **Create new Zone**.

## Scenario Editing

In Blender, each scenario is divided into view layers. To edit scenario settings, go to the **Mario Galaxy -Scenario** tab under **Mario Galaxy** right in the 3D View.

- **ScenarioNo** The Mission ID
- **ScenarioName** A custom name useful for editing (ignored by the game)
- **ScenarioType** *Normal* for normal mission, *Hidden* for hidden star, part of another normal mission
- **Power Star Trigger** Name of an actor that spawns the mission's star
- **Comet** Type of comet for this mission
- **Comet Time Limit** In seconds
- **LuigiModeTimer** Unused
- **StarMask** This defines which stars from 1-6 are active, inactive. As of this version, its just displayed as a hash number, so get [this tool](https://kuribo64.net/get.php?id=0WxWiGQe9elhns2b) to get the correct values.

To export Scenariodata to your filesystem, click on **Export Scenario Info** in the Mario Galaxy Map Tools tab.

**Zone Layer Display**
Select a zone's collection in the outliner to display which layers should be visible. If the zone does not have an entry in the scenario yet, a buttom appears that will do the job.

Like Star Mask, its just displayed as a hash number as of this version, so get [this tool](https://kuribo64.net/get.php?id=0WxWiGQe9elhns2b) to get the correct values.

### Galaxy Level Engine Note
Support for [Galaxy Level Engine](https://github.com/SuperHackio/GalaxyLevelEngine) scenarios is also supported, but the export is unfinished!

## Editing

### Adding objects
To add objects, be sure that you selected the zone's collection, which you want to add your object, then go to the **Map Tools** tab and enter the object name in the *Add this object* line and click on **Add Galaxy Object** to add an object of your likeling. If Asset Searching is enabled, the plugin searches for assets in a given folder structure using your entered object name in Blender files and links them. More about this at **Asset Usage**.

### Editing objects
Select an object and go to the *Mario Galaxy - Object Settings* tab to get all editable parameters of the selected objects such as object aruments, area shapes, gravity sizes, and more.

### Paths

Paths can have parameters per point, so to edit these, go to editing mode and select the point, then go to the *Object Settings* tab to the *Point Settings* section.

To get more point settings for an extra ordinary path, click on **Add complex Point Settings**.

The Path ID is defined here. If you add a new path, you must enter a new ID here:

![screenshot](pictureB.png)

### Layer Editing

Each object, except paths, has an Layer field to control, in which scenario it is there and in which not. Set either **Common** for always being there, or LayerA - LayerP. Blender will not update the visibility immediately, so click on **Update Layer Info** in the *Mario Galaxy- Map Tools* tab

### Camera Editing

Select a zone's collection and click on **Start Camera Editor** in the *Mario Galaxy- Map Tools* tab. Be sure that you entered LaunchCamPlus' folder path unter *paths*.

You can continue editing your level while the camera editor is open. To save the camera settings, go to *File -> Save* or press *CTRL + S* in the camera editor program.

**Tipp:** [This Blender addon](https://github.com/Louiskovski/SuperMarioGalaxy_BlenderCameraPlugin) can be used in combination with SuperBlenderGalaxy. The rotations and camera positions then correspond exactly to the level. Just be sure that the camera objects created by this plugin are not in some level's category collection (i.e. “Objects” or “Cameras”) within a zone, but you can put them in the main collection (e.g. StartZone).

### Asset Usage

To use loadable model assets in the editor, you must put your 3D model into a collection and give this collection the object name to be used. If your model contains additional things that should not be visible in the editor, such as collision, deactivate the visibility in the viewport of the model/collection (via the monitor icon). Then right-click on the collection and click on **Mark As Asset**.

![screenshot](pictureA.png)

If you now add an object with the same name, or import a zone/galaxy that contains this object name, the 3D model will now be visible when:

- The asset is in the same blend file as the level

or

- The blend file with the asset is in the folder structure that was entered in *paths* under *Mario Galaxy - Map Tools*

#### Blender's Asset Browser

Your asset is then of course also in Blender's Asset Browser and you can drag it from there into your level. Be sure that you have it set to Link and not Append, otherwise it will copy the model instead of referencing it.

The disadvantage (so far), however, is that it does not automatically contain the required properties. Click on **Add properties to selected asset (collection)** under *Mario Galaxy - Map Tools* and select either **General Object** or **Map Parts Object** to add the required parameters.

You also need to be sure that the object is in the correct category in the outliner. The Asset Browser will only add it to the currently selected collection!

#### Getting original Assets to display

You can extract all assets to OBJ in order to display in the editor.

Download this zip, unzip it and follow the instructions in the ReadMe:
https://kuribo64.net/get.php?id=qJN11czWftV9nDvR

This can take about 10 minutes however.

# Plans for future versions

- Improve Pymap usage, such as not converting CSV <-> BCSV, and instead read and write BCSV directly (to make importing and exporting much faster)
- Replace WiiExplorer with PyKernel to directly read/write the ARC archives instead of extracting them to folders and then packing them (to avoid useless extra folders)
- Render BDL/BMD model (good luck with that :P)
- Or a way to extract all original assets to DAE/FBX, and then use them in the Blender Editor for assets (like The Fourth Dimension, the 3D Land Editor does)


