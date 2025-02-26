import google.generativeai as genai

genai.configure(api_key="AIzaSyCr1cgsTr8KbrIzWcTv6BBF7vA1Fh0Ad7E")

models = genai.list_models()
for model in models:
    print(model.name)
    