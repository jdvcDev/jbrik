from utils import log_utils
from tracker_core import tracker
from tracker_core import resolver

_PicRotCount = 3

def _resolve_cubestate():
    # python rubiks-cube-tracker.py -f ./resource/jbrik_img/rubiks-side-62.png
    cubestatestr = ""

    for facenum in range(1, 7):
        # Convert the photo of the face into a map of rgb values
        facemap = tracker.jbrick_tracker.convert_face_pics_to_rgb_facemap(facenum, _PicRotCount)

        # convert the map of face rgb values to cubeStateStr
        cubestatestr += resolver.jbrik_resolver.resolve_colors(facemap, _PicRotCount)

    return cubestatestr

CubeStateStr = _resolve_cubestate()
log_utils.log("\n\nInitial cube state: " + CubeStateStr)
