from flask import Flask, render_template, request, jsonify
import pickle
from marshmallow import Schema, fields, ValidationError


app=Flask(__name__,template_folder='template')


# load the model from disk
loaded_model = pickle.load(open('finalized_model.pkl', 'rb'))


class IRISDataSchema(Schema):
    SL = fields.Float(required=True)
    SW = fields.Float(required=True)
    PL = fields.Float(required=True)
    PW = fields.Float(required=True)


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
    schema = IRISDataSchema()
    try:
        # Validate request body against schema data types
        result = schema.load(form_param)

    except ValidationError as error:
        # Return a nice message if validation fails
        return jsonify(error.messages), 400

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