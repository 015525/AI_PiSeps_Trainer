from choice.choiceLoop import choice
from aiTrainer.AITrainer import aiTrainer
from finish.Finish import finish_window

start_exercise = choice()
if start_exercise == "start exercise" :
    finished = aiTrainer()
    if finished == True :
        finish_window()





