import argparse
import os.path
import re
import sys
import time

import matrix

import cv2

"""
Get Command Line Arguments
"""

# make the parser
parser = argparse.ArgumentParser()

# add some arguments
parser.add_argument('path',
                    type=str,
                    help='Path to video file or directory of video files to display on the matrix')
parser.add_argument('-l', '--loop',
                    action='store_true',
                    help='Loop the input video(s)')
parser.add_argument('-r', '--recursive',
                    action='store_true',
                    help='If the path is a directory, recursively search subdirectories for supported video files')
parser.add_argument('-v', '--verbose',
                    action='store_true')
parser.add_argument('-d', '--debug',
                    action='store_true')
parser.add_argument('-x', '--width',
                    type=int,
                    help='Width of the matrix, in pixels',
                    required=True)
parser.add_argument('-y', '--height',
                    type=int,
                    help='Height of the matrix, in pixels',
                    required=True)
parser.add_argument('-f', '--fps',
                    type=float,
                    help='Set FPS limiter',
                    default=60.0)

# parse the arguments
args = parser.parse_args()

"""
Get Files at the Given Path 
"""

# make list to hold all potential video paths
video_paths = []

# confirm the path exists, exit if not
if not os.path.exists(args.path):
    sys.exit(f"Path '{args.path}' does not exist!")

# check if the path is a dir or a file and handle accordingly
if os.path.isfile(args.path):
    # the path is a file, just add it to the list of paths
    video_paths.append(f'{args.path}')
elif os.path.isdir(args.path):
    # the path is a directory, add all files within this directory to the list of paths
    if args.recursive:
        for dir_path, dir_name, file_names in os.walk(args.path):
            video_paths.extend([f"{dir_path}/{file_name}" for file_name in file_names])
    else:
        video_paths = [f'{args.path}{file_name}' for file_name in os.listdir(args.path)]
else:
    sys.exit(f"Path '{args.path}' exists, but is not a file or directory!");

# make regex for supported video formats
extension_regex = re.compile("^.+\\.(avi|mp4)")

# trim list of paths to only supported video formats
video_paths = [i for i in video_paths if extension_regex.match(i)]

# confirm that we still have some videos to display
if not video_paths:
    sys.exit(f'No supported files in search scope!')

"""
Matrix setup
"""

mat = matrix.Matrix(args.width, args.height, 18, serpentine=True)

"""
Translate the Videos
"""

# main loop
while True:
    # iterate through the list of videos
    for video_path in video_paths:
        # open the video file
        video = cv2.VideoCapture(video_path)

        # get some information about the video
        dimensions = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        framerate = int(video.get(cv2.CAP_PROP_FPS))

        # get the ms per frame for this video
        source_ms_per_frame = int(1000.0 / framerate)
        real_ms_per_frame = max(int(1000.0 / args.fps), source_ms_per_frame)
        if args.debug:
            print(f"[DEBUG][{video_path}]: Source Framerate:{framerate}fps // Limiter:{args.fps}fps // Real Framerate:{int((1/real_ms_per_frame)*1000.0)}fps")

        # set the initial times
        time_at_last_frame_fetch = time.time_ns()
        time_at_last_frame_used = time.time_ns()

        # set a placeholder for later
        ret = None
        frame = None

        while True:
            # calculate elapsed time
            elapsed_ms_fetch = (time.time_ns() - time_at_last_frame_fetch) / 1_000_000
            elapsed_ms_used = (time.time_ns() - time_at_last_frame_used) / 1_000_000

            # get one frame from the video if enough time has passed to go to the next frame
            if elapsed_ms_fetch >= source_ms_per_frame:
                # get the frame
                ret, frame = video.read()

                # reset the time at last frame fetch
                time_at_last_frame_fetch = time.time_ns()

            # skip this frame if we've used a frame recently enough
            if elapsed_ms_used < real_ms_per_frame:
                continue

            # use the frame if a frame was fetched
            if ret:
                # reset the time at last frame use
                time_at_last_frame_used = time.time_ns()

                # resize the frame
                img = cv2.resize(frame, (args.width, args.height))

                # display the frame on the matrix
                mat.display(img)

                # wait for cv2
                cv2.waitKey(1)

            else:
                if args.verbose:
                    f"Error reading frame from '{video_path}'! Skipping the rest of this video..."
                break

        # cleanup opencv
        video.release()
        cv2.destroyAllWindows()

    # get out of the loop if the user didn't set "--loop"
    if not args.loop:
        break
