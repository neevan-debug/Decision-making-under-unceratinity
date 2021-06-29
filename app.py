
from flask import Flask, render_template, request, redirect
import numpy as np

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home_page():
    return render_template("home.html")


@app.route("/index", methods=["GET", "POST"])
def get_Table():
    if request.method == 'POST':
        form_data = request.form
        global dim
        dim = []
        for i in form_data.values():
            dim.append(int(i))
        return render_template("index.html", dimensions=dim)


@app.route("/results", methods=["POST", "GET"])
def results():
    if request.method == 'POST':
        form_data = request.form
        print(form_data)
        ip1 = []
        P = []
        S = []
        count = 0
        if dim[2] == 1:
            for i in form_data.values():
                if count < (dim[0])*(dim[1]):
                    ip1.append(int(i))
                    count = count + 1
                elif count >= (dim[0])*(dim[1]) and count < (dim[0]+1)*(dim[1]):
                    P.append(float(i))
                    count = count + 1
                else:
                    S.append(i)
        else:
            for i in form_data.values():
                if count < (dim[0])*(dim[1]*2):
                    if count % 2 == 0:
                        ip1.append(int(i))
                    else:
                        P.append(float(i))
                    count = count + 1
                else:
                    S.append(i)
        A = np.reshape(ip1, (dim[0], dim[1]))
        if dim[2] == 0:
            P = np.reshape(P, (dim[0], dim[1]))
        print(A)
        print(P)
        print(S)
        if request.form.get("gridRadios") == "option1":
            x = np.amax(A, 1)

        elif request.form.get("gridRadios") == "option2":
            x = np.amin(A, 1)
        
        elif request.form.get("gridRadios") == "option6":
            x = np.mean(A, axis=1)
            x = np.round(x, decimals=1)
            

        else:
            if dim[2] == 1:
                P_T = np.reshape(P, (dim[1], 1))
                x = np.dot(A, P_T)
                x = np.reshape(x, (1, dim[0]))
                x = np.round(x, decimals=1)
                x = x[0]
            else:
                x = np.multiply(A, P)
                x = np.sum(x, axis=1)
                x = np.round(x, decimals=1)
        print(x)

        message = {"option1": "You are a Optimistic person",
                   "option2": "You are a Conservative person",
                   "option3": "You are a Rational person",
                   "option5": "Your output is regret - optimal ",
                   "option6": "Your output is optimal ", }

        if request.form.get("gridRadios1") == "option4":
            op = np.where(x == max(x))
            dataToRender = message[request.form.get("gridRadios")]
            return render_template("results.html", ip=A, data=dataToRender, output=op, Selected=S, Pro=P, mat=x, dimensions=dim)

        else:
            op = np.where(x == min(x))
            dataToRender = message[request.form.get("gridRadios1")]
            return render_template("results.html", ip=A, data=dataToRender, output=op, Selected=S, Pro=P, mat=x, dimensions=dim)


if __name__ == "__main__":
    app.run(debug=True)
