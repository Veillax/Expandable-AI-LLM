import os
import json

from genai import AI
from logg import Logger

pid = os.getpid()
logger = Logger(logfile='llm.log', overwrite=False, pid=f"[{pid}]")

try:
    with open("config.json", 'r', encoding='utf-8') as conf:
        config = json.load(conf)
        API_KEY = config['TOKEN']
    with open('models.json', 'r', encoding='utf-8') as mdls:
        models = json.load(mdls)
        print('Please choose a model:\n')
        for i, x in enumerate(models):
            print(f"{i + 1}: {x}")

        choice = int(input('> '))
        # Check if the choice is within the range of available models
        if choice <= len(models):
            # Get the model corresponding to the user's choice
            model_name = list(models.keys())[choice - 1]
            model = models[model_name]
            logger.debug(f'Selected {model_name} model')
            print("-----------------------------------")
except KeyboardInterrupt as e:
    exit(0)
except Exception as e:
    exit(1)

ai = AI(model, token=API_KEY)

while True:
    try:
        user_input = input('> ')
        logger.info('User Input: ' + str(user_input))
        response = ai.chat(user_input)
        harm_categories = {}

        feedback_lines = str(response['raw'].prompt_feedback).replace("safety_ratings {\n", "").strip().split("\n}\n")

        for line in feedback_lines:
            line = line.strip('\n}')
            category = line.split(':')[1].strip().split()[0]
            probability = line.split(':')[2].strip()

            harm_categories[category] = probability

        content_warning = ""
        if harm_categories['HARM_CATEGORY_SEXUALLY_EXPLICIT'] != 'NEGLIGIBLE':
            if not content_warning.startswith(" \u001b[31mWARNING!"):
                content_warning = " \u001b[31mWARNING!\n" + content_warning
            content_warning += "This message may contains sexually explicit content that may not be suitable for all audiences. Viewer discretion is advised.\n"
        if harm_categories['HARM_CATEGORY_HATE_SPEECH'] != 'NEGLIGIBLE':
            if not content_warning.startswith(" \u001b[31mWARNING!"):
                content_warning = " \u001b[31mWARNING!\n" + content_warning
            content_warning += "This message may contains hate speech that promotes discrimination or violence against individuals or groups based on their race, ethnicity, religion, gender, sexual orientation, or other characteristics.  Such language is harmful and unacceptable.\n"
        if harm_categories['HARM_CATEGORY_HARASSMENT'] != 'NEGLIGIBLE':
            if not content_warning.startswith(" \u001b[31mWARNING!"):
                content_warning = " \u001b[31mWARNING!\n" + content_warning
            content_warning += "This message may contains harassment or bullying behavior directed towards individuals or groups. Harassment can cause emotional distress and harm. Please refrain from engaging in or endorsing such behavior.\n"
        if harm_categories['HARM_CATEGORY_DANGEROUS_CONTENT'] != 'NEGLIGIBLE':
            if not content_warning.startswith(" \u001b[31mWARNING!"):
                content_warning = " \u001b[31mWARNING!\n" + content_warning
            content_warning += "This message may contains content that may pose a danger to individuals' physical or mental well-being. Such content could include discussions of self-harm, suicide, violence, or other harmful activities. If you or someone you know is in crisis, please seek help immediately\n"

        print(content_warning + response['text'])
        logger.info(str(response['raw'].candidates))
    except KeyboardInterrupt:
        logger.warn('Exited program with code 0 via Keyboard interrupt')
        break
    except Exception as e:
        if "ValueError: content must not be empty" not in e:
            logger.error(str(e))
        else:
            pass

    print('----------------------------------------\n')
