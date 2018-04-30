from __future__ import print_function
import json
import subprocess
import argparse
import cv2
import video_frame as vf


class BFrame(object):
    def __repr__(self, *args, **kwargs):
        return "B"
    
    def __str__(self, *args, **kwargs):
        return repr(self)


class PFrame(object):
    def __repr__(self, *args, **kwargs):
        return "P"

    def __str__(self, *args, **kwargs):
        return repr(self)


class IFrame(object):
    
    def __init__(self):
        self.key_frame = False

    def __repr__(self, *args, **kwargs):
        if self.key_frame:
            return "I"
        else:
            return "i"
        
    def __str__(self, *args, **kwargs):
        return repr(self)


class GOP(object):
    
    def __init__(self):
        self.closed = False
        self.frames = []
        
    def add_frame(self, frame):
        self.frames.append(frame)
        
        if isinstance(frame, IFrame) and frame.key_frame:
            self.closed = True
            
    def __repr__(self, *args, **kwargs):
        frames_repr = ''
        
        for frame in self.frames:
            frames_repr += str(frame)
        
        gtype = 'CLOSED' if self.closed else 'OPEN'
        
        return 'GOP: {frames} {count} {gtype}'.format(frames=frames_repr, 
                                                      count=len(self.frames), 
                                                      gtype=gtype)


parser = argparse.ArgumentParser(description='Dump GOP structure of video file')
parser.add_argument('filename', help='video file to parse')
parser.add_argument('-e', '--ffprobe-exec', dest='ffprobe_exec', 
                    help='ffprobe executable. (default: %(default)s)',
                    default='ffprobe')

args = parser.parse_args()

command = '"{ffexec}" -show_frames -print_format json "{filename}"'\
                .format(ffexec=args.ffprobe_exec, filename=args.filename)
                
response_json = subprocess.check_output(command, shell=True, stderr=None)

frames = json.loads(response_json)["frames"]


gop_count = 0
gops = []
# gop = GOP()
# gops.append(gop)

for jframe in frames:
    if jframe["media_type"] == "video":
        gops.append(jframe["pict_type"])

print(len(gops))


cap = cv2.VideoCapture(args.filename)
frames = list()
i = 0
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        frames.append([frame, gops[i]])
        i = i + 1
    else:
        break

print(frames[0])
cap.release()

mbs = list()
for i in range(len(frames)):
    if frames[i][1] == 'I':
        mbs.append(vf.getMacroblocks(frames[i]))
# getMacroblocks(frames[0])
print(mbs[0])

# fd = vf.calculateSFD(mbs[1], mbs[0])
# print(fd)