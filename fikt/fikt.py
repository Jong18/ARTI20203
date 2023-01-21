import openai
f = open("C:\\Users\\Ingolfur\\Documents\\myopenai_key.txt", "r")
lykill = f.readline()
openai.api_key = lykill
engines = openai.Engine.list()

response = openai.Image.create(
    prompt = "a shining perfect gold sphere with light beams bounsing off it in a sunset",
    n = 1,
    size = "512x512"
)
image_url = response['data'][0]['url']
print(response)

sets = {12}
asdf = [{"mis","can","can"},{"can"},{"mis","mis"},"right"]
asd = [{"can","mis","can"},{"can"},{"mis","mis"},"left"]
print(sets)