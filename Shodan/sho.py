import shodan

api_key = "q3COBv0xQPZd7n1VFYSTu1F7GybsmeC9"
api_shodan = shodan.Shodan(api_key)

buscar = input("Término a buscar: ")

resultados = api_shodan.search(buscar)

print("Tipo de resultados:", type(resultados))
print("Claves de resultados:", resultados.keys())
print("Total de resultados:", resultados["total"])
print("Tipo de coincidencias:", type(resultados["matches"]))
print("Número de coincidencias:", len(resultados["matches"]))
