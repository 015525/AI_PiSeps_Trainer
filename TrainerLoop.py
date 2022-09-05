from choiceLoop import choice
from AITrainer import aiTrainer
from Finish import finish_window

start_exercise = choice()
if start_exercise == "start exercise" :
    finished = aiTrainer()
    if finished == True :
        finish_window()





