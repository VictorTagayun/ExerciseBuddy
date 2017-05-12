# Exercise Buddy
## Project Description
This is a linear experience that highlights Cozmo’s unique personality. In this, the player acts as Cozmo’s personal fitness trainer. Cozmo throws a tantrum when asked to workout, after waking up. After a couple of tries, he finally gives in and starts exercising with the cube. Players can make him change pace by giving him voice commands. After it becomes too fast for him to handle, Cozmo becomes too tired and dozes off.

## Video
https://www.youtube.com/watch?v=J1WHM6k2eWc

## Implementation Details
This experience uses Python’s Speech Recognition library to get user speech input. A cube tap-input is added as a failsafe in case the speech recognition library doesn’t recognize the correct words. Cozmo SDK’s ‘move_lift’ method is used with a custom ‘changeDirection’ method being called regularly to lift the cubes up and down to simulate a workout.

## Instructions
### Installation
1. There are dependencies on other Python packages. Install them using pip. 
2. Speech Recognition Library ( pip3 install SpeechRecognition )
3. Common - ( Download it from https://github.com/Wizards-of-Coz/Common )

### Experience
This is a linear experience and requires certain inputs from the user to go through the entire experience.
Call out to Cozmo with the words ‘Cozmo’ or ‘Buddy’ or ‘Exercise’. This starts the experience and Cozmo will start throwing tantrums. Repeating this words will make him exercise after 2 times. Place the cube on his lift every time. After Cozmo starts lifting the cube (exercising), players can say ‘Faster’ or ‘Slower’ and cozmo will obey until it becomes too difficult for him. He finally dozes off and then the experience starts again.

## Thoughts for the Future
The vision of this prototype was to highlight Cozmo’s character and make him seem human-like. Throwing tantrums about working out is a very human thing and we wanted to see how it would look if Cozmo felt that way. Speech input did not work so well with Cozmo. So a cube input could be used instead. This prototype explores a linear experience where cozmo throws a tantrum every time. This could be expanded to have cozmo have a different mood every time he wakes up. Maybe one time, he is in a very cheerful mood when he wakes up and readily obeys the trainer’s commands and works out. Another time he wakes up with a bad mood and he gets angry when told what to do.
