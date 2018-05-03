with open("rate.txt", encoding="utf-8") as f:
    for line in f:
        items = line.split("\t")
        print(len(items))