
userDict = []
with open("features.txt") as f:
    content = f.readlines()
    for line in content:
        line_arr = line.split(" ")

