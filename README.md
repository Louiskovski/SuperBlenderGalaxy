# Mario Galaxy Map Editor / Converter Addon for Blender
Transforms Blender into a Mario Galaxy Level Editor.
Still pretty WIP. Make backups of your levels.

# Preparation

- Download GALAXYMAP_EDITOR-ASSETS.blend file
- Install [Pymap](https://github.com/SunakazeKun/pyjmap)
- Download [WiiExplorer](https://github.com/SuperHackio/WiiExplorer)
- Download [LaunchCamPlus](https://github.com/SuperHackio/LaunchCamPlus) (optional)
- Download the text files and place these in the same directory as the WiiExplorer.exe

Now start Blender and install the addon
- In the 3D View on the right click on the *Mario Galaxy* tab and enter the required paths at the *path* column

# Importing Levels

You can either import full galaxies or individual zones. Simply enter the zone or galaxy name and click on Import Galaxy or Import Zone.
If Asset Searching Enabled is set to 1, the plugin searches for assets in a given folder structure using the levels object names in Blender files and links them. More about this at **Asset Usage**.

# Exporting Levels

If you click on **Export Galaxy**, all zones will be exported and saved into your StageData filesystem. To export a single zone, select the collection with the zone name and click on **Export Zone**

# Creating new levels

To create a brand new level, start with a new Blender file and click on **Create brand new galaxy**. This creates a new scene with a new scenario and a main zone. Now you can add several new zones with **Create new Zone**.

## Scenario Editing

In Blender, each scenario is divided into scenes. To edit scenario settings, go to 
