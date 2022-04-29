﻿# importar pacotes importantes

from fastapi import FastAPI, HTTPException # para trabalhar com a API
import sqlite3 # banco de dados
import json # trabalhar com dicionários
import requests # parte de crawlear de novo
from bs4 import BeautifulSoup # parte de crawlear de novo
import datetime # registrar a data de crawleamento

# nome para chamar o FastAPI
app = FastAPI()


## conectar com o banco de dados
con2 = sqlite3.connect("./app/livros.db", check_same_thread=False)
cursor2 = con2.cursor()


# vamos fazer com que a API peça uma categoria e um número N de livros para exibir o resultado
@app.get("/books/")
def ler_n_livros_de_tal_categoria(category: str, n_books: int = 10):
	
	
# para isso, vamos criar um filtro para que apenas a categoria desejada seja mostrada	
	selecionar = "SELECT * FROM tab_livros WHERE categoria = ?"
	lista_de_dicionarios = []
	cursor2.execute(selecionar, (category.title(),))

# tratamento de erro pro caso de o usuário digitar uma categoria não catalogada
	if category.title() not in ["Travel","Mystery","Historical Fiction","Sequential Art","Classics","Philosophy","Romance","Womens Fiction","Fiction","Childrens","Religion","Nonfiction","Music","Default","Science Fiction","Sports and Games","Add a comment","Fantasy","New Adult","Young Adult","Science","Poetry","Paranormal","Art","Psychology","Autobiography","Parenting","Adult Fiction","Humor","Horror","History","Food and Drink","Christian Fiction","Business","Biography","Thriller","Contemporary","Spirituality","Academic","Self Help","Historical","Christian","Suspense","Short Stories","Novels","Health","Politics","Cultural","Erotica","Crime"]:
		raise HTTPException(
            status_code=404,
            detail={'A categoria tem que ser alguma dessas':' "Travel","Mystery","Historical Fiction","Sequential Art","Classics","Philosophy","Romance","Womens Fiction","Fiction","Childrens","Religion","Nonfiction","Music","Default","Science Fiction","Sports and Games","Add a comment","Fantasy","New Adult","Young Adult","Science","Poetry","Paranormal","Art","Psychology","Autobiography","Parenting","Adult Fiction","Humor","Horror","History","Food and Drink","Christian Fiction","Business","Biography","Thriller","Contemporary","Spirituality","Academic","Self Help","Historical","Christian","Suspense","Short Stories","Novels","Health","Politics","Cultural","Erotica","Crime"'},
            headers={"Erro": "Ta errado aí bicho"},
        )
	
# voltando ao caso de o usuário digitar certo	
	armazenar_dados2 = cursor2.fetchall()
	for cada_livro_dessa_cat in armazenar_dados2:
		cada_dicionario_de_livro = {
        "titulo": cada_livro_dessa_cat[0],
        "descricao": cada_livro_dessa_cat[1],
        "preco": cada_livro_dessa_cat[2],
		"disponibilidade": cada_livro_dessa_cat[3],
		"categoria": cada_livro_dessa_cat[4],
        "data de crawleamento": cada_livro_dessa_cat[5]
		}
		
# adicionar os dicionários (com conteúdo de livros) a uma lista para mostrar na tela
		lista_de_dicionarios.append(cada_dicionario_de_livro)


#----------------------------------------------------------


## agora vamos definir o numero "n" de livros mostrados
	
	if len(lista_de_dicionarios) < n_books:
		mostrar_quantos_puder = len(lista_de_dicionarios)
	else:
		mostrar_quantos_puder = n_books

	lista_de_n_dicionarios_retorno = lista_de_dicionarios[:mostrar_quantos_puder]
	
#----------------------------------------------------------

# resultado da função em .json:

	return json.dumps(lista_de_n_dicionarios_retorno)




## caso queira o resultado da função sem o formato .json:

#	return lista_de_n_dicionarios_retorno



###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------

# nova função: deletar categorias do banco de dados
con3 = sqlite3.connect("./app/livros.db", check_same_thread=False)
cursor3 = con3.cursor()
@app.delete("/books2/del/")
def deletar_categoria(category:str):

	deletar_db = "DELETE FROM tab_livros WHERE categoria = ?"
	cursor3.execute(deletar_db, (category.title(),))
    # tratamento de erro pro caso de o usuário digitar uma categoria não catalogada
	if category.title() not in ["Travel","Mystery","Historical Fiction","Sequential Art","Classics","Philosophy","Romance","Womens Fiction","Fiction","Childrens","Religion","Nonfiction","Music","Default","Science Fiction","Sports and Games","Add a comment","Fantasy","New Adult","Young Adult","Science","Poetry","Paranormal","Art","Psychology","Autobiography","Parenting","Adult Fiction","Humor","Horror","History","Food and Drink","Christian Fiction","Business","Biography","Thriller","Contemporary","Spirituality","Academic","Self Help","Historical","Christian","Suspense","Short Stories","Novels","Health","Politics","Cultural","Erotica","Crime"]:
		raise HTTPException(
            status_code=404,
            detail={'A categoria tem que ser alguma dessas':' "Travel","Mystery","Historical Fiction","Sequential Art","Classics","Philosophy","Romance","Womens Fiction","Fiction","Childrens","Religion","Nonfiction","Music","Default","Science Fiction","Sports and Games","Add a comment","Fantasy","New Adult","Young Adult","Science","Poetry","Paranormal","Art","Psychology","Autobiography","Parenting","Adult Fiction","Humor","Horror","History","Food and Drink","Christian Fiction","Business","Biography","Thriller","Contemporary","Spirituality","Academic","Self Help","Historical","Christian","Suspense","Short Stories","Novels","Health","Politics","Cultural","Erotica","Crime"'},
            headers={"Erro": "Ta errado aí bicho"},
        )
	con3.commit()
	
    

	return "categoria deletada"



###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------

# função para crawlear uma única categoria
@app.post("/books3/crawlear_uma_categoria")
def crawlear_categoria(categoria_digitada : str): ## função para crawlear, tendo a categoria e seu link como parâmetros (serão especificados depois)
    import datetime
        
        # tratamento de erro pro caso de o usuário digitar uma categoria não catalogada
    if categoria_digitada.title() not in ["Travel","Mystery","Historical Fiction","Sequential Art","Classics","Philosophy","Romance","Womens Fiction","Fiction","Childrens","Religion","Nonfiction","Music","Default","Science Fiction","Sports and Games","Add a comment","Fantasy","New Adult","Young Adult","Science","Poetry","Paranormal","Art","Psychology","Autobiography","Parenting","Adult Fiction","Humor","Horror","History","Food and Drink","Christian Fiction","Business","Biography","Thriller","Contemporary","Spirituality","Academic","Self Help","Historical","Christian","Suspense","Short Stories","Novels","Health","Politics","Cultural","Erotica","Crime"]:
        raise HTTPException(
            status_code=404,
            detail={'A categoria tem que ser alguma dessas':' "Travel","Mystery","Historical Fiction","Sequential Art","Classics","Philosophy","Romance","Womens Fiction","Fiction","Childrens","Religion","Nonfiction","Music","Default","Science Fiction","Sports and Games","Add a comment","Fantasy","New Adult","Young Adult","Science","Poetry","Paranormal","Art","Psychology","Autobiography","Parenting","Adult Fiction","Humor","Horror","History","Food and Drink","Christian Fiction","Business","Biography","Thriller","Contemporary","Spirituality","Academic","Self Help","Historical","Christian","Suspense","Short Stories","Novels","Health","Politics","Cultural","Erotica","Crime"'},
            headers={"Erro": "Ta errado aí bicho"},
        )


    def crawlPage2(categoria_digitada : str, link_da_categoria):
    
        urlBase_cada_categoria = "https://books.toscrape.com/" ## essa é a url à qual serão adicionadas outras partes de link

        response_para_a_categoria = requests.get(urlBase_cada_categoria + link_da_categoria) ## adiciona à urlBase o link obtido láaa embaixo no código
        page_categoria = BeautifulSoup(response_para_a_categoria.content, 'html.parser') ## coloca em "page" o conteúdo da página lido pelo beautifulsoup

        #print(page_categoria)
    
        # iterar todos os livros listados
        for item in page_categoria.find_all('article', 'product_pod'): ## passa por todos os livros (demarcados por "article" e "product_pod")
            bookUrl = urlBase + item.find('a').attrs['href'].replace("../../../", "catalogue/") ## adiciona à urlBase o link da categoria
            bookResponse = requests.get(bookUrl) ## bota o requests pra entrar nessa nova url (de cada categoria)
            bookPage = BeautifulSoup(bookResponse.content, 'html.parser') ## usa o beautifulsoup pra ler a página como html

            paragraphs = bookPage.find("article", "product_page").find_all("p")
            title = bookPage.find('h1').text #.replace('"','\"') ## replace pra ignorar as aspas duplas
            description = paragraphs[3].text #.replace('"','\"') ## replace pra ignorar as aspas duplas
            price = paragraphs[0].text[1:]
            availability = paragraphs[1].text.strip()[10:12]
            day = str(datetime.date.today())
            print("=================================")
            print("Title: " + title)
            print("Price: " + price)
            print("In stock: " + availability)
            print("Category: " + categoria_digitada)
            print("Description: " + description)
            print("Data de Crawleamento: " + day)
        
            cursor4.execute("INSERT INTO tab_livros VALUES (?,?,?,?,?,?)",(title, description, price, availability, categoria_digitada, day))
        
        con4.commit()
        return "os dados dessa categoria foram salvos em 'db_pra_uma_categoria.db'"
    
        next = page_categoria.find("li", "next") # checar se há uma nova página
        if next is not None:
            nextLink = next.find("a").attrs["href"]
            parts = link_da_categoria.split("/") ## essa parte é pra corrigir o problema de não listar todos os livros com o botão Next
            parts[-1] = nextLink
            nextLink = "/".join(parts)
            crawlPage2(categoria_digitada.title(), nextLink)
    
    #conectar com o banco
    con4 = sqlite3.connect("./app/livros.db", check_same_thread=False)
    cursor4 = con4.cursor()




    # agora vamos pegar as informações pra botar na tabela
    response_para_categoria = requests.get("https://books.toscrape.com/index.html")
    page_para_categoria = BeautifulSoup(response_para_categoria.content, 'html.parser') ## usa o beautifulsoup pra ler o conteúdo como html 
    #print(page) ## printa pra que vejamos as <tags> pra nos orientar na busca dos dados
    urlBase = "https://books.toscrape.com/"

    # iterar por categorias

    categorias_e_links = {}

    for item in page_para_categoria.find('aside').find_all('li')[1:]: ##encontrar as categorias (marcadas por "li") e excluir a primeira (books)
        link = item.find('a').attrs['href'] ##pegar o link (marcado por "href" em "a")
        category = item.text.strip() ## a categoria é o nome escrito no item e strip é pra tirar os espaços
        categorias_e_links.update({category:link}) ## faz um dicionário com categorias e seus respectivos links
    #print(categorias_e_links)

    #agora vamos transformar o dicionario em json para facilitar a busca pelo link de uma categoria desejada
    import json
    dict_cat_link_em_json = json.dumps(categorias_e_links) ## transforma em .json
    buscar_link_da_categoria = json.loads(dict_cat_link_em_json) ## permite a busca pelo valor de uma chave
    # categoria_digitada = "suspense" # para testes
    link_da_categoria = buscar_link_da_categoria[categoria_digitada.title()] ## pega o link da categoria entre colchetes
    #print(buscar_link_da_categoria[categoria_digitada])
    crawlPage2(categoria_digitada.title(), link_da_categoria) ## chama a função de crawlear
    
    return "categoria salva"
    

###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------


con5 = sqlite3.connect("./app/livros.db", check_same_thread=False)
cursor5 = con5.cursor()

# função para mostrar livros com estoque abaixo de N (em uma única categoria)
@app.get("/books4/mostrar_livros_com_estoque_abaixo_de")
def ler_categoria_com_menos_que_n_livros(category: str, menos_de_n_em_estoque: int = 10):

# para isso, vamos criar um filtro para que apenas a categoria desejada seja mostrada	
	selecionar5 = "SELECT * FROM tab_livros WHERE categoria = ?"
	lista_de_dicionarios5 = []
	cursor5.execute(selecionar5, (category.title(),))

# tratamento de erro pro caso de o usuário digitar uma categoria não catalogada
	if category.title() not in ["Travel","Mystery","Historical Fiction","Sequential Art","Classics","Philosophy","Romance","Womens Fiction","Fiction","Childrens","Religion","Nonfiction","Music","Default","Science Fiction","Sports and Games","Add a comment","Fantasy","New Adult","Young Adult","Science","Poetry","Paranormal","Art","Psychology","Autobiography","Parenting","Adult Fiction","Humor","Horror","History","Food and Drink","Christian Fiction","Business","Biography","Thriller","Contemporary","Spirituality","Academic","Self Help","Historical","Christian","Suspense","Short Stories","Novels","Health","Politics","Cultural","Erotica","Crime"]:
		raise HTTPException(
            status_code=404,
            detail={'A categoria tem que ser alguma dessas':' "Travel","Mystery","Historical Fiction","Sequential Art","Classics","Philosophy","Romance","Womens Fiction","Fiction","Childrens","Religion","Nonfiction","Music","Default","Science Fiction","Sports and Games","Add a comment","Fantasy","New Adult","Young Adult","Science","Poetry","Paranormal","Art","Psychology","Autobiography","Parenting","Adult Fiction","Humor","Horror","History","Food and Drink","Christian Fiction","Business","Biography","Thriller","Contemporary","Spirituality","Academic","Self Help","Historical","Christian","Suspense","Short Stories","Novels","Health","Politics","Cultural","Erotica","Crime"'},
            headers={"Erro": "Ta errado aí bicho"},
        )
	
    # voltando ao caso de o usuário digitar certo	
	armazenar_dados5 = cursor5.fetchall()
	for cada_livro_dessa_cat in armazenar_dados5:
		cada_dicionario_de_livro5 = {
        "titulo": cada_livro_dessa_cat[0],
        "descricao": cada_livro_dessa_cat[1],
        "preco": cada_livro_dessa_cat[2],
		"disponibilidade": cada_livro_dessa_cat[3],
		"categoria": cada_livro_dessa_cat[4],
		"data de crawleamento": str(datetime.date.today())
		}
		dicionarios5_json = json.dumps(cada_dicionario_de_livro5) #transformando em json para facilitar a leitura dos valores de disponibilidade
		procurar_valores_de_disponibilidade = json.loads(dicionarios5_json)
#print(int(procurar_valores_de_disponibilidade["disponibilidade"]))
		if (int(procurar_valores_de_disponibilidade["disponibilidade"])) < menos_de_n_em_estoque:
				lista_de_dicionarios5.append(dicionarios5_json) # adicionar os dicionários (com conteúdo de livros) que tenham estoque menor que o informado pelo usuário
                
				# caso queira mostrar sem o formato.json, comente a linha acima e descomente a de baixo
				# lista_de_dicionarios5.append(cada_dicionario_de_livro5) # adicionar os dicionários (com conteúdo de livros) que tenham estoque menor que o informado pelo usuário


	return lista_de_dicionarios5
