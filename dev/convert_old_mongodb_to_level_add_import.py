import json

guild_id = int(input("Guild id to extract from: "))
path = input("File path for json file: ")
output_path = input("File path for output: ")

with open(path, encoding="utf8") as f:
    data = json.load(f)

print(data)

output = ""

for doc in data:
    print(doc.get("id"))
    if (user_id := doc.get("id")) and doc.get("guildid") == guild_id:
        user_id = doc.get("id")
        xp = doc.get("xp")
        output += f"{user_id},{xp}\n"

print(output)

with open(output_path, "w") as f:
    f.write(output)
