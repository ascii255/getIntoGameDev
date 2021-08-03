from urllib.request import urlopen

#target webpage
url = "https://www.ultimate-guitar.com/top/tabs"

page = urlopen(url)
print("Opened page")
#print(f"Page is stored as {page}")

htmlRaw = page.read()
print("Read page contents")
#print(f"Page contents stored as {htmlRaw}")

htmlDecoded = htmlRaw.decode("utf-8")
print("Page contents decoded as utf-8")
#print(htmlDecoded)

#grab main block
dataStart = htmlDecoded.find("<div class=\"js-store\"")
dataEnd = htmlDecoded.find("</div>",dataStart)
#print(f"Data starts at index {dataStart} and ends at index {dataEnd}")
data = htmlDecoded[dataStart:dataEnd]
#print(data)

data = data.replace("&quot;","")
#print(data)
data = data.replace("{","\n")
#print(data)

dataStart = data.find("tabs:[\n")
dataEnd = data.find("],current_type:all", dataStart)
data = data[dataStart:dataEnd]
print(data)