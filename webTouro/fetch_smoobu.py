import urllib.request
import re

url = "https://guest.smoobu.com/?t=jth6f6c7037&b=140929057"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        print("HTML length:", len(html))
        with open("smoobu_page.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Successfully saved smoobu_page.html")
except Exception as e:
    print("Error fetching URL:", e)
