import urllib, re, sys, random

def spider(url):
    prev = [url]
    blacklist = []
    current = None
    prev_num = 0
    with open("spider.txt", 'a') as file:
        while True:
            
            if url == current:
                blacklist.append(url)
                try:
                    url = prev[prev_num]
                except IndexError:
                    print "Can't crawl", url, "trying next in list if exists..."
                prev_num -= 1
                continue
            try:
                source = urllib.urlopen(url).read()
            except:
                blacklist.append(url)
                url = prev[len(prev)-1]
                print "Blacklisted", url
                continue
            current = url
            links = re.findall("<a href.*</a>", source)
            for x in links:
                try:
                    link = ''.join(re.findall('".*"', x)).strip('"')
                    if not link.startswith("http"):
                        continue
                    if "twitter" in link and "support" in link:
                        continue
                    if '"' in link:
                        link = link.split('"')[0]
                    if link in blacklist:
                        continue
                    if link in prev:
                        continue
                    else:
                        if len(prev) >= 10000:
                            prev = prev[len(prev)-5:]
                        prev.append(link)
                    try:
                        urllib.urlopen(link)
                    except:
                        continue
                    else:
                        url = link
                        file.write(link+"\n")
                        print url
                        break
            
                except Exception, error:
                    print error
                    continue

if __name__ == "__main__":
    try:
        spider(sys.argv[1])
    except IndexError:
        print "Usage: python spider.py <url>"
