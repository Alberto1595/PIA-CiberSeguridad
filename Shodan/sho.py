import shodan

api_key = "q3COBv0xQPZd7n1VFYSTu1F7GybsmeC9"
api_shodan = shodan.Shodan(api_key)

buscar = input("Término a buscar: ")


file = open("Resultados.txt", "w")
resultados = api_shodan.search(buscar)

file.write("Tipo de resultados:", type(resultados + "\n"))
file.write("Claves de resultados:", resultados.keys() + "\n")
file.write("Total de resultados:", resultados["total"] + "\n")
file.write("Tipo de coincidencias:", type(resultados["matches"] + "\n"))
file.write("Número de coincidencias:", len(resultados["matches"] + "\n"))
