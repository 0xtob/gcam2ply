#!/bin/bash

if [ $# -ne 5 ] ; then
    echo "Extract the depth image from a photo taken with the Lens Blur feature"
    echo "of the Google Camera app for Android and creates a 3D point cloud in."
    echo "PLY format from it."
    echo
    echo "Syntax: $0 image.jpg model.ply sensor_width_mm sensor_height_mm focal_length_mm"
    exit;
fi

DEPTHFILE=$1.depth.png
if [ `uname` = "Linux" ] ; then
    B64DECODEFLAG=d;
elif [ `uname` = "Darwin" ] ; then
    B64DECODEFLAG=D;
else
    echo "Unsupported operating system."
    exit
fi

exiftool -b -XMP:Data $1 | base64 -$B64DECODEFLAG > $DEPTHFILE
exiftool -j -XMP:Near -XMP:Far -XMP:Format $1 | ./gcam2ply.py $DEPTHFILE $3 $4 $5 > $2
