from flask import Flask

app = Flask(__name__)

app.debug = True  # Force debug mode
app.env = 'development'

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run()