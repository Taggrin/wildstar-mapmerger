# WildStar Map Merger

This script allows you to merge WildStar map tilesets into one image. When extracting the maps from the game files with [WildStar Studio](https://bitbucket.org/Celess/wildstar-studio-f2p), they are split in 512x512 px tiles, indexed by hexvalue. Just load in these images and within seconds the image will be reconstructed.

This script makes use of the [Python Image Library](https://pillow.readthedocs.io/en/5.3.x/), so make sure to have this installed before you proceed.
<br>Created in Python 2.7.15

Feel free to use for extracting purposes. Nexus Forever!
<br>Created by Taggrin (a.k.a. Larcer), 23/09/2018
<br><br><br>

**Instructions**
* Launch WildStar Studio, available through link above
* Load -> ClientData.index (found in your WildStar/Patch directory)
* Select "maps" or a subselection of it
* Extract filtered -> only extract .tex files with convert to .bmp enabled
* Launch mapmerger.py
* Give the path to the tileset and give it a minute...
* Enjoy your merged images, they appear in the Out directory
