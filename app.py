from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Função para buscar informações no banco de dados
def buscar_resposta(pergunta):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()

    pergunta = pergunta.lower()

    if "película automotiva" in pergunta:
        cursor.execute("SELECT disponibilidade, preco FROM produtos WHERE tipo='Película Automotiva'")
        resultado = cursor.fetchone()
        if resultado:
            return f"Temos disponível! Preço: R${resultado[1]}"
    elif "localização" in pergunta:
        return "Estamos localizados na Rua Exemplo, nº 123 - Centro"
    elif "promoção" in pergunta:
        cursor.execute("SELECT nome, preco FROM produtos WHERE promocao=1")
        promocoes = cursor.fetchall()
        if promocoes:
            return "Temos as seguintes promoções:\n" + "\n".join([f"{p[0]} por R${p[1]}" for p in promocoes])
        else:
            return "No momento não temos promoções ativas."
    
    return "Desculpe, não entendi sua pergunta. Tente novamente com outras palavras."

@app.route("/perguntar", methods=["POST"])
def responder():
    dados = request.get_json()
    pergunta = dados.get("pergunta", "")
    resposta = buscar_resposta(pergunta)
    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(debug=True)
