import cv2

#some important frames
first_rat_frame = 343 
stable_camera_frame = 200

#locations
rearing_line = 600 #pixels from top of image
mid_line = 700 #pixels from the left

#debug video
debug_video = False

cap = cv2.VideoCapture('rats.MTS')
foreground_mask = cv2.BackgroundSubtractorMOG()

ret, frame = cap.read()
fgmask = foreground_mask.apply(frame)

f = file("output.csv", 'w');
f.write("frame index,left_rat_pixels,right_rat_pixels\r\n")

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
    f.write("%d,%d,%d\r\n"%(frame_index, left_rat_pixels, right_rat_pixels))

  if debug_video:
    #break the loop if 'escape' is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:  break
  frame_index = frame_index+1

f.close()
cap.release()
cv2.destroyAllWindows()
