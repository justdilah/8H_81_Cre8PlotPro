# Cre8PlotPro
### Craft Comics with a Text, Not a Sketch: Your AI Storytelling Companion Telegram Bot
> Built for NTU SCSE TechFest Hackathon 2024 
> 
> (Award Obtained: one of the Top 10 team projects)

##  Project Introduction and Demo
Link to [YouTube Video](https://youtu.be/dRdkiLh4bPc)

## Prerequisites
#### Telegram Bot
1. Obtain your own Telegram Bot Token from BotFather [website](https://t.me/botfather)
2. Insert your API key into the `telebot/app.py` into the following code:

`TOKEN = 'YOUR_API_KEY'`

#### Cre8AI
1. Obtain your own Stability AI API key from this [website](https://platform.stability.ai/account/keys).
2. Insert your API key into the `cre8AI/stability_ai.py` into the following code:

`os.environ['STABILITY_KEY'] = 'YOUR_API_KEY'`

## Execution Details
1. Open up the project in your preferred IDE and run `pip install -r requirements. txt`
2. Navigate into the `telebot` folder and run `python app.py`
3. Navigate to the `cre8AI` folder and run `uvicorn main:app --reload`
4. Open up Telegram and start using the bot! 

## References
https://huggingface.co/tuner007/pegasus_paraphrase
