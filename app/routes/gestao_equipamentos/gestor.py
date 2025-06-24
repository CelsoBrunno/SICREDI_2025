# rotas para as paginas do gestor da pasta templates/Gestor

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/gestor/ambiente')
def ambiente():
    return render_template('Gestor/GerenciarAmbientes/ambiente.html')

@app.route('/gestor/analistas')
def analistas():
    return render_template('Gestor/GerenciarAnalistas/analistas.html')

@app.route('/gestor/reserva')
def reserva():
    return render_template('Gestor/GerenciarReservas/reservas.html')

@app.route('/gestor/imobilizado')
def imobilizado():
    return render_template('Gestor/EquipamentosImobilizados/imobilizados.html')

@app.route('/gestor/mobilizado')
def mobilizado():
    return render_template('Gestor/EquipamentosMobilizados/mobilizados.html')


