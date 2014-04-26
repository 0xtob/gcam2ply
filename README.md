gcam2ply
========
![gcam2ply diagram](/diagram.png)

Creates a 3D point cloud (PLY) from a depth image captured with the lens blur
feature of the Google Camera app for Android.

Usage
-----
Make sure you have `exiftool` and `scipy` installed and call:

    ./gcam2ply.sh image.jpg model.ply $w $h $f

w, h, and f are the sensor with, sensor height and focal length of
your phone's camera in mm, respectively. For the Nexus 5, the values are
w: 4.54, h: 3.42, f: 4.0 .

Information on the Google Camera depth data is available
[here](https://developers.google.com/depthmap-metadata/reference).

Limitations
-----------
* Simple camera model: No skew, principal point at (0,0).
* Assuming 8-bit PNG depth maps.

Tips
----
* You can get much higher resolution models by changing the lens blur quality to
  high in the Google Camera app.
* For best quality, turn down the blur to minimum before saving the image.
  Otherwise, the color information in the point cloud will be blurred as well.
* Meshlab is a nice tool for viewing PLY point clouds.

[Fork me on Github](https://github.com/0xtob/gcam2ply)
