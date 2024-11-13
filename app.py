from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def buscar_produtos(termo):
    url = f'https://api.mercadolibre.com/sites/MLB/search?q={termo}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        dados = response.json()
        produtos = []
        for item in dados['results']:
            produto = {
                'nome': item['title'],
                'preco': item['price'],
                'link': item['permalink'],
                'imagem': item['thumbnail']
            }
            produtos.append(produto)
        produtos.sort(key=lambda x: x['preco'])
        return produtos
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []

@app.route("/", methods=["GET", "POST"])
def index():
    produtos = []
    if request.method == "POST":
        termo = request.form.get("termo")
        if termo:
            produtos = buscar_produtos(termo)
    return render_template("index.html", produtos=produtos)

if __name__ == "__main__":
    app.run(debug=True)
