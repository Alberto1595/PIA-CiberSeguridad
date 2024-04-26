import nmap
from CreatePDF import create_pdf

def scanning(begin, end, target):
    scanner = nmap.PortScanner()
    results = ["Puerto","Estado"]

    for i in range(begin, end + 1):
        res = scanner.scan(target, str(i))
        state = res["scan"][target]["tcp"][i]["state"]
        results.append([f'Port {i}', state])

    title = f"Resultados del escaneo de puertos {target}"
    create_pdf(results,title)

scanning(10,30, "148.234.88.122")