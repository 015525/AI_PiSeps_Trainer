# AI_piSeps_trainer
A computer vision project aims to make a virtual trainer for piSeps exercise using 33 landmarks detected by  pose estimation upper body model to count the curls while exercising , detect the current working hand , detect the wrong position for the elbow , check if the weight is heavy , detect the Wright posture of the body while exercising, and make a simple schedule for making a complete exercise 

### If a wrong position for the elbow is detected :- 
  AI trainer displays a  warning message  
  The counter stops counting 

### If the weight is heavy and trainer is in the first 6 curls :- 
  The AI trainer suggests a lighter weight

### If the weight is heavy and trainer is in the last 4 curls :-
  The AI trainer gives a support message

It only works when the detected hand is the same as the desired hand 

AI trainer can be used as a training assistant in gym halls or as an alternative for doing proper exercise at home .

### Technology used :-
    mediapipe
    opencv
    numpy
    time 
    playsound 

## For complete demo video :-
https://youtu.be/WBskiMZVvh4
