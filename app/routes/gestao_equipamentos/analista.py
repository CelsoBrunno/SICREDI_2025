# rotas para as paginas do analista da pasta templates/Analista

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/analista/ambiente')
def ambiente():
    return render_template('Analista/AcessoAmbiente/ambiente.html')

@app.route('/analista/equipamento')
def equipamento():
    return render_template('Analista/ReservaEquipamento/equipamento.html')



