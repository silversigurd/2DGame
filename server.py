from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Renderiza el archivo HTML desde la carpeta templates

if __name__ == '__main__':
    app.run(debug=True)
