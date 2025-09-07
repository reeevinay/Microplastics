from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <html>
    <head><title>Microplastic Analysis API</title></head>
    <body>
        <h1>Microplastic Analysis API</h1>
        <p>API is running successfully!</p>
        <p>Health check: <a href="/health">/health</a></p>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'healthy',
        'message': 'Microplastic Analysis API is running',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
