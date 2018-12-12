# MTA18338 semester project
This is the GitHub repository of MTA18338's semester project for Autumn 2018.
This project requires a camera to run. The program detects the markers included in the folder, so these have to be printed in order to experience the full functionality.

The program works by loading the camera feed and then analyzing it using edge detection (Canny) and then finding contours for square objects (the markers). If it finds any, the program then warps the markers to make them quadratic using getPerspectiveTransform and warpPerspective and compares them to a database of saved templates using meanSquaredError. Each template has been rotated using warpAffine. If any match, the program sends the position of the marker to the server, the server updates the map with the new objects and sends it back to the client for display.
The client is responsible for sending the coordinates of the found objects to the server, which then draws circles in the appropriate positions of the map to be projected onto the table.

## For the *Programming of Complex Software Systems* Course
The file *contribution_by_group_members.txt* references the server-client functionality.
