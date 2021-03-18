
YouTube video for explaination is here:https://youtu.be/N6eVUQUtEqQ

Here we use mean shift algorithm to track the road lane.
# Steps:
Take first frame when lane gets detected with Hough lines.
Setup initial location of window.
Set up the ROI for tracking which is the starting bottom most point of the lane.
Setup the termination criteria, either 10 iteration or move by at least 1 pt.
Apply mean shift to get the new location.
Draw it on image.
