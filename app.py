from flask import Flask, render_template, request
import pickle


app=Flask(__name__,template_folder='template')


# load the model from disk
loaded_model = pickle.load(open('finalized_model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods = ["POST"])
def result():
    form_param = request.form.to_dict()
    sl = form_param.get('SL') 
    sw = form_param.get('SW')
    pl = form_param.get('PL')
    pw = form_param.get('PW')
    to_predict = [[sl, sw, pl, pw]]
    result = loaded_model.predict(to_predict)
    if(int(result)==0):
        prediction ='Setosa'
    elif (int(result)==1):
        prediction ='Versicolor' 
    elif (int(result)==2):
        prediction ='Virginica'   

    return(render_template("index.html", prediction=prediction))

if __name__ == "__main__":
    app.run(debug=True)