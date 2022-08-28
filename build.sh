#!/bin/bash

mkdir -p build/plugin.audio.rbb
cp -r ./{LICENSE.txt,addon.py,addon.xml,resources} build/plugin.audio.rbb/
cd build
zip -0r plugin.zip plugin.audio.rbb