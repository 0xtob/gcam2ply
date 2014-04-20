#!/usr/bin/env python

import sys, os, json
import scipy
import scipy.misc

docstr = """gcam2ply.py - 2014 by Tobias Weyand (me@tobw.net)

Creates a 3D point cloud (PLY) from a depth image captured with the lens blur
feature of the Google Camera app for Android.

Usage:
  Instead of calling this script directly, use gcam2ply.sh .
  If you want to do everything by hand, here's how:

  1. Extract the depth image:
    exiftool -b -XMP:Data image.jpg | base64 -d > depth.png

  2. Generate the point cloud:
    exiftool -j -XMP:Near -XMP:Far -XMP:Format image.jpg | \
      ./gcam2ply.py depth.png $w $h $f > model.ply

  w, h, and f are the sensor with, sensor height and focal length of your
  phone's camera in mm, respectively."""


if len(sys.argv) != 5:
    print docstr
    sys.exit(0)

# Read XMP data as JSON from stdin.
jsondatastr = ''.join([l.strip() for l in sys.stdin.readlines()])
jsondata = json.loads(jsondatastr)[0]

# Parse input.
depth_filename = sys.argv[1]
sensor_width = float(sys.argv[2])
sensor_height = float(sys.argv[3])
focal_distance = float(sys.argv[4])

imagefile = jsondata['SourceFile']
depth_near = jsondata['Near']
depth_far = jsondata['Far']
depth_format = jsondata['Format']

# Read RGB image.
image = scipy.misc.imread(imagefile)

# Read depth image.
depth_image = scipy.misc.imread(depth_filename)
depth_raw = scipy.float32(depth_image[:,:,0]) / 255.0

# Convert to actual depth using the formulas from
# https://developers.google.com/depthmap-metadata/encoding
if depth_format == 'RangeLinear':
    depth = depth_raw * (depth_far - depth_near) + depth_near
elif depth_format == 'RangeInverse':
    depth = depth_far * depth_near / (depth_far - depth_raw * (depth_far - depth_near))
else:
    print 'Unsupported depth format: %s\n' % depth_format
    sys.exit()

# Compute 3D coordinates.
[img_height, img_width] = scipy.shape(depth)
pixel_width = sensor_width / img_width
pixel_height = sensor_height / img_height

[xs, ys] = scipy.meshgrid(range(img_width), range(img_height))

X = (xs * pixel_width - sensor_width / 2.0) / focal_distance * depth
Y = (ys * pixel_height - sensor_height / 2.0) / focal_distance * depth

# Print PLY to stdout.
print """ply
format ascii 1.0
element vertex %d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
property uchar alpha
element face 0
end_header""" % (img_width * img_height)

for y in xrange(img_width):
    for x in xrange(img_height):
        print '%f %f %f %d %d %d %d' % (X[x,y], Y[x,y], depth[x,y],
                                        image[x,y,0], image[x,y,1], image[x,y,2], 255)
