# Expandable AI LLM
## What is it?
Well, it's exactly what it sounds like, an expandable AI LLM  
You can add your own prompts or use the pre-baked fun prompts  
It's easy to use and simple to set up and add your own models  
It also can provide logs!

## How to use
### I have an API key
1. Place your API key in `config.json`  
2. Run `pip install -r requirements.txt` from the folder you placed the files in  
3. Run `python llm.py`  

### I do not have an API key  
1. Get an API key from the [Google AI App Studio](https://aistudio.google.com/app/apikey)  
2. Place your API key in `config.json`  
3. Run `pip install -r requirements.txt` from the folder you placed the files in  
4. Run `python llm.py`  

## How to add new models
Copy this template and paste it into `models.json`:
```json
"name": [
    {
      "role": "user",
      "parts": [
        "prompt"
      ]
    },
    {
      "role": "model",
      "parts": [
        "​"
      ]
    }
  ]
```
Replace `name` with the name of your model  
Replace `prompt` with the starting prompt, this will determine how the model behaves

Make sure to format the json file correctly  
Now, run `python llm.py`
