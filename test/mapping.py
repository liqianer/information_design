import pymysql

db = pymysql.connect("localhost", "root", "1997syx", "tag", use_unicode=True, charset ="utf8")
cursor = db.cursor()

wfile1 = open("ambiguity.txt", "w", encoding="utf-8")
# wfile2 = open("mapping.txt", "w", encoding="utf-8")
saveList = []

with open("urlList.txt", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        mUrl, movieName = line.split("\t")
        nmovieName = movieName.split("/")[0]
        if nmovieName:
            sql = 'SELECT * FROM movie_info WHERE name LIKE "{nmovieName}%"'.format(nmovieName=nmovieName)
            print(sql)
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                if len(results) == 0:
                    continue

                elif len(results) == 1:
                    for row in results:
                        movieInfo = "\t".join(row)
                        if(row[1] not in saveList):
                            wfile2.write("%s\t%s\n"%(mUrl, movieInfo))
                            saveList.append(row[1])
                        else:
                            wfile1.write("%s\t%s\n"%(mUrl, movieInfo))

                elif len(results) <= 3 and len(results) > 1:
                    for row in results:
                        movieInfo = "\t".join(row)
                        wfile1.write("%s\t%s\t%s\n"%(mUrl, movieName, movieInfo))

            except Exception as e:
                print(e)

wfile1.close()
wfile2.close()
cursor.close()