#!/bin/sh
cd image/
ls -F *.png | head -n -1 | xargs -r rm
cd ..