import arcpy
import numpy as np

"""
-coords would be the coordinates of a polyline (could potentially work for polygon boundaries as well
 - These are the coordinates for a single polyline - NOT A MULTIPART FEATURE
-eps is the epsilon value that you want to generalize the line using - it uses whatever the units of the polyline are, so use a projection that uses units of ft/m.

Timings using a UTM based lined with 630 (cl) vertices are below:
*All timings used the following settings : %timeit -r 4 | (mean ± std. dev. of 4 runs, 10 loops each)
  %timeit -r 4 rdp(cl.coordinates()[0],500)| 42 ms ± 379 µs per loop 
  %timeit -r 4 rdp(cl.coordinates()[0],100)| 57.2 ms ± 599 µs per loop 
  %timeit -r 4 rdp(cl.coordinates()[0],10) | 83.3 ms ± 478 µs per loop 
  %timeit -r 4 rdp(cl.coordinates()[0],5)  | 86.9 ms ± 469 µs per loop
  %timeit -r 4 rdp(cl.coordinates()[0],2)  | 103 ms ± 652 µs per loop
  
ESRI's is faster, but mine has more panache.
"""
def rdp(coords,eps):
    p1, p2  = arcpy.Point(*coords[0]), arcpy.Point(*coords[-1])
    seLine  = arcpy.Polyline(arcpy.Array([p1,p2]))
    othPts  = [arcpy.Point(*x) for x in coords[1:-1]]
    maxInd  = np.argmax([seLine.distanceTo(pt) for pt in othPts]) if othPts else None
    maxDist = seLine.distanceTo(othPts[maxInd]) if maxInd else 0
    
    if maxDist > eps:
        l = rdp(coords[:maxInd+1],eps)
        r = rdp(coords[maxInd:],eps)        
        return np.vstack((l[:-1], r))
    else:
        return [coords[0],coords[-1]]
