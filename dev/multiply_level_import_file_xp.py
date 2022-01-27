input_path = input("Import file path: ")
multiplier = input("Multiply amount by: ")
multiplier = int(multiplier)
export_path = input("Export file path: ")

with open(input_path, "r") as f:
    lines = f.readlines()

output = ""

error_lines = []
for i, line in enumerate(lines):
    try:
        user, xp = line.split(",")
        output += f"{user},{int(xp)*multiplier}\n"
    except Exception as e:
        print(f"Error adding xp from file on line {i+1}: {e}")

with open(export_path, "w") as f:
    f.write(output)

print("done")
