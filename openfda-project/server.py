import http.server
import http.client
import socketserver
import json


PORT = 8000
socketserver.TCPServer.allow_reuse_address = True



openfda_url="api.fda.gov"
openfda_event="/drug/label.json"
openfda_drug='&search=active_ingredient:'
openfda_company='&search=openfda.manufacturer_name:'


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def main_web(self):   #Esta es la Web principal, a partir de aquí se accede a todas las demás.
        html = '''<html>
            <head>
                <title> WEB OPENFDA </title>
            </head>
            <body style = 'background-color: blue' align='center' >
                <img src="https://wwolicymed.com/wp-content/uploads/2018/07/FDA.png">
                <h1> Bienvenido/a a la web de OpenFDA </h1>
                <h2> Drug list </h2>
                <form action = 'listDrugs' method ="get">
                    <input type = 'submit' value = 'Lista de medicamentos'>
                        Limit = <input type = 'text' name = 'limit' >
                    </input>
                </form>
                <form action = 'searchDrug' method ="get">
                    <input type = 'submit' value = 'Busca un medicamento'>
                        Drug = <input type = 'text' name = 'drug'>
                    </input>
                </form>
                <h2> Company list </h2>
                <form action = 'listCompanies' method ="get">
                    <input type = 'submit' value = 'Lista de empresas '>
                        Limit = <input type = 'text' name = 'limit' >
                    </input>
                </form>
                <form action = 'searchCompany' method ="get">
                    <input type = 'submit' value = 'Busca una empresa'>
                        Company = <input type = 'text' name = 'company'>
                    </input>
                </form>
                <h2> Warning list </h2>
                <form action = 'listWarnings' method ="get">
                    <input type = 'submit' value = 'Advertencias'>
                        Limit = <input type = 'text' name = 'limit' >
                    </input>
                </form> Practica realizada por Carlos Contreras Laguia'''
        return html


    def drugs_web(self,list_drugs):  #Web de los medicamentos
        html_drugs = '''<html>
            <head>
                <title> OpenFDA Drugs </title>
            </head>
                <body> Estos son los mediamentos recuperados:
                    <ul>'''

        for i in list_drugs:
            html_drugs += '<li>'+i+'</li>'

        html_drugs += '''</ul>
                    </body>
                    </html>'''

        return html_drugs





    def ingredient_web(self,list_ingredient):  # Web de los principios activos
        html_ingredient = '''<html>
            <head>
                <title> OpenFDA Active ingredient </title>
            </head>'''
        for a in list_ingredient:
            html_ingredient +=  '<body> El principio activo '+ a +' esta presente en: <ul>'
            break


        for i in list_ingredient:
            html_ingredient += '<li>'+i+'</li>'

        html_ingredient += '''</ul>
                    </body>
                    </html>'''

        return html_ingredient

    def companies_web(self,list_companies):  #Web de las compañias
        html_companies = '''<html>
            <head>
                <title> OpenFDA Companies </title>
            </head>
                <body> Estas son las empresas :
                    <ul>'''

        for i in list_companies:
            html_companies += '<li>'+i+'</li>'

        html_companies += '''</ul>
                    </body>
                    </html>'''

        return html_companies


    def company_web(self,list_company_search): # Esta es igual que la anterior pero con las compañias
        html_company_search = '''<html>
            <head>
                <title> Open FDA Companies </title>
            </head>'''
        for a in list_company_search:
            html_company_search +=  "<body> La informacion recuperada de la empresa "+ a +' es: <ul>'
            break


        for i in list_company_search:
            html_company_search += '<li>'+i+'</li>'

        html_company_search += '''</ul>
                    </body>
                    </html>'''

        return html_company_search


    def warning_web(self,list_warning):   #Web de las advertencias
        html_warning = '''<html>
            <head>
                <title> OpenFDA Warnings </title>
            </head>
                <body> Lea con detenimiento las adevertencias:
                    <ul>'''

        for i in list_warning:
            html_warning += '<li>'+i+'</li>'

        html_warning += '''</ul>
                    </body>
                    </html>'''

        return html_warning


    def error_web(self):  #Web del error 404
        error = '''<html>
            <head>
                <title> Error 404 </title>
            </head>
            <body>
                <h1> Error found </h1>
                No hay informacion del valor introducido
            </body>
            </html>'''

        return error


    def results(self, limit):  #Obtenemos toda la informacion de Open FDA para luego hacer las llamadas necesarias, y la guardamos en 'resultados'
        conn = http.client.HTTPSConnection(openfda_url)
        conn.request("GET", openfda_event + "?limit="+str(limit))
        print(openfda_event + "?limit="+str(limit))
        r1 = conn.getresponse()
        drugs_raw = r1.read().decode("utf8")
        data = json.loads(drugs_raw)
        resultados = data['results']
        return resultados

    def do_GET(self): # Cada vez que hay una petición GET, se invoca esta funcion. El recurso solicitado esta en self.path
        recurso_list = self.path.split("?")
        if len(recurso_list) > 1:  #Con esto controlamos si nos han pasado un parametro
            parametro = recurso_list[1]
        else:
            parametro = ""

        limit = 10 # Limite por defecto

        if parametro:
            parse_limit = parametro.split("=")
            if parse_limit[0] == "limit":  # Si el parametro es 'limit', se cambia el limite por defecto (10) por el que tu has elegido
                limit = int(parse_limit[1])
                print("Limit: {}".format(limit))

        else:
            print("Sin parametros")


        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = self.main_web()
            self.wfile.write(bytes(html, "utf8"))

        elif 'listDrugs' in self.path: # listDrugs nos devuelve la lista de los medicamentos
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            medicamentos = []
            resultados = self.results(limit)
            for resultado in resultados:
                if ('generic_name' in resultado['openfda']):
                    medicamentos.append (resultado['openfda']['generic_name'][0])
                else:
                    medicamentos.append('Desconocido')

            html_drugs = self.drugs_web(medicamentos)
            self.wfile.write(bytes(html_drugs, "utf8"))

        elif 'listCompanies' in self.path:  #listCompanies nos devuelve una lista de empresas
            self.send_response(202)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            companies = []
            resultados = self.results(limit)
            for resultado in resultados:
                if ('manufacturer_name' in resultado['openfda']):
                    companies.append (resultado['openfda']['manufacturer_name'][0])
                else:
                    companies.append('Desconocido')

            html_companies = self.companies_web(companies)
            self.wfile.write(bytes(html_companies, "utf8"))


        elif 'listWarnings' in self.path:  # listWarnings te devuelve las advertencias
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            warnings = []
            resultados = self.results(limit)
            for resultado in resultados:
                if ('warnings' in resultado):
                    warnings.append (resultado['warnings'][0])
                else:
                    warnings.append('Desconocido')

            html_warning = self.warning_web(warnings)
            self.wfile.write(bytes(html_warning, "utf8"))

        elif 'searchDrug' in self.path:  # searchDrug nos devuelve la informacion sobre un principio activo introducido
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            drug=self.path.split('=')[1]

            conn = http.client.HTTPSConnection(openfda_url)
            conn.request("GET", openfda_event + "?limit="+str(limit)+ openfda_drug + drug)
            r1 = conn.getresponse()
            drugs_raw = r1.read().decode("utf8")
            data = json.loads(drugs_raw)

            try:  # Controlamos si el valor introducido esta en OpenFDA
                resultados = data['results']

                drug = []
                for resultado in resultados:
                    if ('generic_name' in resultado['openfda']):
                        drug.append (resultado['openfda']['generic_name'][0])
                    else:
                        drug.append('Desconocido')

                html_ingredient = self.ingredient_web(drug)
                self.wfile.write(bytes(html_ingredient, "utf8"))

            except KeyError:   # En caso contrario, nos aparecerá la error_web
                error = self.error_web()
                self.wfile.write(bytes(error, "utf8"))


        elif 'searchCompany' in self.path:  # searchCompany nos devuelve la informacion sobre la empresa introducida

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            company = self.path.split('=')[1]
            conn = http.client.HTTPSConnection(openfda_url)
            conn.request("GET", openfda_event + "?limit="+str(limit)+ openfda_company + company)
            r1 = conn.getresponse()
            drugs_raw = r1.read().decode("utf8")
            data = json.loads(drugs_raw)

            try:  # Igual que en serachDrug
                resultados = data['results']

                companies = []
                for resultado in resultados:
                    companies.append(resultado['openfda']['manufacturer_name'][0])


                html_company_search = self.company_web(companies)
                self.wfile.write(bytes(html_company_search, "utf8"))

            except KeyError:
                error = self.error_web()
                self.wfile.write(bytes(error, "utf8"))





        elif 'redirect' in self.path:  # Si aparece un error(302), nos devuelve a la pagina principal
            self.send_response(302)
            self.send_header('Location', 'http://localhost:'+str(PORT))
            self.end_headers()

        elif 'secret' in self.path:  # Si aparece el error 401, te pide un inicio de sesion para acceder a sitios privados
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()

        else:  # Si se introduce mal un parametro, nos salta el error 404
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("No encontramos el recurso '{}'".format(self.path).encode())
        return


Handler = testHTTPRequestHandler  #Esta instancia atiende a las peticiones http

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Sirviendo al puerto", PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Interrumpido por el usuario")

print("")
print("Servidor parado")

