from flask import Flask, redirect,render_template,request

app=Flask(__name__)

@app.route('/')
def indexPage():
    return render_template('index.html')

@app.route('/register')
def registerPage():
    return render_template('register.html')

@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route('/registerUser',methods=['POST','GET'])
def registerUser():
    name=request.form['username']
    id=request.form['userid']
    password=request.form['password']
    print(name,id,password)
    return (redirect('/login'))

if __name__=="__main__":
    app.run(debug=True)