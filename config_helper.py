import cv2, sys, os.path, hashlib
import config_and_logging
#todo: proper packages

configured = config_and_logging.read_config()

# read the filename from the config file
filename = configured["filename"]
if not os.path.isfile(filename):
  logfile_handle.write("Couldn't read filename %s\r\n"%(filename,))
  sys.exit()

cap = cv2.VideoCapture(filename)

ret, frame = cap.read()

mid_line = -1
rearing_line = -1

frame_index = 0
paused = False;

print """
Controls (video window must have focus):
space pauses/resumes.
arrow keys control line location
escape ends video and prints the line locations in pixels
"""

while cap.isOpened():
  if mid_line < 0:
    mid_line = frame.shape[1]/2;
    rearing_line = frame.shape[0]/2;
  if not paused:
    ret, frame = cap.read()
  if frame==None: break
  cv2.rectangle(frame, (0,0), (mid_line, rearing_line),
                (255,0,0), thickness=10) 
  cv2.rectangle(frame, (mid_line,0), (frame.shape[1], rearing_line),
                (0,255,0), thickness=10) 
  cv2.putText(frame, "frame: %d"%(frame_index,), (0, frame.shape[1]/2), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=5, thickness=10, color=(0,255,0))
  cv2.imshow('frame', cv2.resize(frame, (0,0), fx=0.25, fy=0.25))
  #break the loop if 'escape' is pressed
  k = cv2.waitKey(30) & 0xff
  if k==27:  break #escape
  if k==32:  paused = not paused #escape
  if k==81: mid_line = max(0,mid_line-4)
  if k==82: rearing_line = max(0,rearing_line-4)
  if k==83: mid_line = min(mid_line+4,frame.shape[0])
  if k==84: rearing_line = min(rearing_line+4, frame.shape[1])
  if not paused:
    frame_index = frame_index+1

print "last frame viewed was %d and mid line is %d and rearing line is %d"%(frame_index, mid_line, rearing_line)

cap.release()
cv2.destroyAllWindows()
