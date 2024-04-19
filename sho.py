import shodan
import json

api_key = "BbJgE38l4M3AphCUMQawgZLveCIm5y1v"
api_shodan = shodan.Shodan(api_key)

buscar = input("Término a buscar: ")


file = open("Resultados.txt", "w")
resultados = api_shodan.search(buscar)

json.dump(resultados,file)
file.close()


print("Tipo de resultados:", type(resultados + "\n"))
print("Claves de resultados:", resultados.keys() + "\n")
print("Total de resultados:", resultados["total"] + "\n")
print("Tipo de coincidencias:", type(resultados["matches"] + "\n"))
print("Número de coincidencias:", len(resultados["matches"] + "\n"))
