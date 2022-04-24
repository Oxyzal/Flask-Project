from flask import *
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio import start_server, config, platform
import flask

import json

import pandas as pd

import numpy_financial

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def CalculerMensualité():
    if request.method == 'POST':
        #put_button("Retour",onclick = lambda: run_js('window.location.reload()'), color="dark")    
        C = int(request.form.get('montant'))
        T = str(request.form.get('interet'))
        T = T.replace(",",".")
        T = float(T)
        N2 = int(request.form.get('temps'))
        N = N2*12
        ASSU = str(request.form.get('assurance'))
        ASSU = ASSU.replace(",",".")
        ASSU = float(ASSU)
        t = (T / 12) 
        q = 1 + t / 100 # calcul du coefficient multiplicateur associé à une hausse de t%
        M = (q**N * (C) * (1 - q) / (1 - q**N)) + C*((ASSU/100)/12)
        #print("Votre mensualité sera de {0:.2f} euros".format(M))
        I = N * M - C # calcul des intérêts versés
        #put_text(f"Votre mensulaité sera de {M} euros")
        #put_text(f"Le montant total des intérêts versés sera de {I} euros")
        T2 = T*1/100
        rng = pd.date_range("01-01-2021", periods=N, freq='MS')
        rng.name = "Date"
        df = pd.DataFrame(index=rng, columns=['Mensualité', 'Capital Amorti', 'Intérêts', 'Capital restant dû'], dtype='float')
        df.reset_index(inplace=True)
        df.index += 1
        df.index.name = "Periode (Mois)"

        df["Mensualité"] = -1 * numpy_financial.pmt(T2/12, N, C)+ C*((ASSU/100)/12)
        df["Capital Amorti"] = -1 * numpy_financial.ppmt(T2/12,df.index,N, C)
        df["Intérêts"] = -1 * numpy_financial.ipmt(T2/12,df.index, N, C) 
        df = df.round(2)

        df["Capital restant dû"] = 0
        df.loc[1, "Capital restant dû"] = C - df.loc[1, "Capital Amorti"]

        for period in range(2, len(df)+1):
            previous_balance = df.loc[period-1, "Capital restant dû"]
            principal_paid = df.loc[period, "Capital Amorti"]
            
            if previous_balance == 0:
                df.loc[period, ["Mensualité", 'Capital Amorti', "Intérêts", "Capital restant dû"]] == 0
                continue
            elif principal_paid <= previous_balance:
                df.loc[period, "Capital restant dû"] = previous_balance - principal_paid
        
        df["Date"] = pd.to_datetime(df["Date"],format='%d-%m-%Y')

        #put_text("TABLEAU D'AMORTISSEMENT").style('color: dark; font-size: 20px; font-weight:bold;')
        #put_collapse('Voir le tableau', [put_html(df.to_html(border = 0))])

        return render_template('index.html.jinja', tableau=int(I) , test=int(M),capital = C, temps = N2, interet = T, assurance = ASSU)

    elif request.method == 'GET':
        return render_template('index.html.jinja', capital = 5000, temps = 1, interet = 1.5, assurance = 1.5)

def main():
    CalculerMensualité()


if __name__ == '__main__':
    #platform.start_server(main, port=8080, debug=True,remote_access=True,reconnect_timeout = True) 
    platform.flask.start_server(main,port=8080, debug=False,remote_access=True,session_expire_seconds=None)




def me_api():
    tableau = get_current_tableau()
    return {
        "Mensualité": tableau.mensualite,
        "Capital Amorti": tableau.capital,
        "Intérêts": tableau.interet,
        "Capital restant dû" : tableau.restant
    }



