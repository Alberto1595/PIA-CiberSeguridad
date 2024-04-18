import whois

url = 'https://www.elpolloloco.com.mx'
try: 
    url_info = whois.whois(url)
    for key, value in url_info.items():
        print(f"{key}: {value} ")
except Exception as e:
    print(f"error {url}: {str(e)}")