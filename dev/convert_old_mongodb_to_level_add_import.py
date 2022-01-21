import json

guild_id = int(input("Guild id to extract from: "))
path = input("File path for json file: ")
output_path = input("File path for output: ")

with open(path, encoding="utf8") as f:
    data = json.load(f)

print(data)

output = ""

for doc in data:
    if doc.get("tag") and doc.get("guildid") == guild_id:
        user_id: str = doc.get("tag")[2:-1]
        xp = doc.get("xp")
        output += f"{user_id},{xp}\n"

print(output)

with open(output_path, "w") as f:
    f.write(output)
