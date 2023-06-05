import openai
f = open("C:\\Users\\Ingolfur\\Documents\\myopenai_key.txt", "r")
lykill = f.readline()
openai.api_key = lykill
engines = openai.Engine.list()

response = openai.Image.create(
    prompt = "A neat logo for our database company named symmetria",
    n = 1,
    size = "1024x1024"
)
image_url = response['data'][0]['url']
print(response)
