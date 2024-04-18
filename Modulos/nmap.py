import nmap

begin = input("Ingresa el puerto de inicio: ")
end = input("Ingresa el purto fin: ")

target = input("Ingresa IP: ")

scanner = nmap.PortScanner

for i in range(begin,end+1):

    res = scanner.scan(target,str(i))

    res = res["scan"][target]["tcp"][i]["state"]
    print(f'port {i} is {res}')