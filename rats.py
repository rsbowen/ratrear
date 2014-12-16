import cv2, sys, os.path
import config_and_logging
#todo: proper packages

configured = config_and_logging.read_config()

#some important frames
first_rat_frame = int(configured["first_rat_frame"])
stable_camera_frame = int(configured["stable_camera_frame"])

#locations
rearing_line = int(configured["rearing_line"])
mid_line = int(configured["mid_line"])

outfile = configured["outfile"]

#debug video
# TODO: move this into configuration file
debug_video = True

logfile = configured["logfile"]
logfile_handle = file(logfile, 'w')
filename = configured["filename"]
if not os.path.isfile(filename):
  logfile_handle.write("Couldn't read filename %s\r\n"%(filename,))
  sys.exit()

cap = cv2.VideoCapture(filename)
foreground_mask = cv2.BackgroundSubtractorMOG()

logfile_handle.write("Filesize of %s was %d bytes and isOpened was %d \r\n"%(filename, os.path.getsize(filename), cap.isOpened()))

ret, frame = cap.read()
fgmask = foreground_mask.apply(frame)

outfile_handle = file(outfile, 'w');
outfile_handle.write("frame index,left_rat_pixels,right_rat_pixels\r\n")

frame_index = 0
while cap.isOpened():
  print frame_index;
  ret, frame = cap.read()
  if(frame_index < stable_camera_frame):
    foreground_mask.apply(frame, fgmask, -1)
  else:
    foreground_mask.apply(frame, fgmask, 0)

  if debug_video:
    cv2.rectangle(frame, (0,0), (mid_line, rearing_line),
                  (255,0,0), thickness=10) 
    cv2.rectangle(frame, (mid_line,0), (frame.shape[1], rearing_line),
                  (0,255,0), thickness=10) 
  if (frame_index > first_rat_frame):
    if debug_video:
      cv2.imshow('frame', cv2.resize(frame, (0,0), fx=0.25, fy=0.25))
      cv2.imshow('bg_subtract_frame', cv2.resize(fgmask, (0,0),
        fx=0.25, fy=0.25))
    fgmask_binary = fgmask > 128;
    left_rat_pixels = sum(sum(fgmask_binary[0:rearing_line, 0:mid_line]))
    right_rat_pixels = sum(sum(fgmask_binary[0:rearing_line, mid_line:]))
    outfile_handle.write("%d,%d,%d\r\n"%(frame_index, left_rat_pixels, right_rat_pixels))

  if debug_video:
    #break the loop if 'escape' is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:  break
  frame_index = frame_index+1

logfile_handle.write("Number of frames was: %d"%(frame_index,)) #todo: this might be off by one
logfile_handle.close()

outfile_handle.close()
cap.release()
cv2.destroyAllWindows()
