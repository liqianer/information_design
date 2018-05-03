from collections import defaultdict

def getRate(path):
    movies = []
    rate = defaultdict(dict)
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            items = line.split("\t")
            if items[0] not in movies:
                movies.append(items[0])
            rate[items[1]][items[0]] = items[2]
    
    return movies, rate

if __name__ == "__main__":
    path = "list.txt"
    movies, rate = getRate(path)
    with open("rate.txt", "w", encoding="utf-8") as f:
        line = "\t".join(movies)
        f.write(line + "\n")
        for user in rate:
            userRates = []
            for movie in movies:
                if movie in rate[user]:
                    userRates.append(rate[user][movie])
                else:
                    userRates.append("nan")
            line = "\t".join(userRates)
            f.write(line + "\n")
    print("Winner Winner, Chicken Dinner!")