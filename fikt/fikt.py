import openai
openai.api_key = "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"
engines = openai.Engine.list()

response = openai.Image.create(
    prompt = "a shining perfect gold sphere with light beams bounsing off it in a sunset",
    n = 1,
    size = "512x512"
)
image_url = response['data'][0]['url']
print(response)