import os

from flask import Flask, request
from flask.helpers import send_from_directory
from flask_cors import CORS
from rag_system import RAGSystem

app = Flask(__name__, static_folder='bc-app/build', static_url_path='')
CORS(app)

rag = RAGSystem()
INIT_URL = None

@app.route("/query", methods=["POST"])
def run_query():
    app.logger.info("Calling run_query from backend.")
    data = request.get_json()
    app.logger.info("Got data")
    app.logger.info(data)

    global INIT_URL
    if not INIT_URL:
        app.logger.info("Initializing vector store for first time")
        INIT_URL = data['url']
        app.logger.info(f"INIT_URL now set to {INIT_URL}")
        rag.doc_processor.prep_vector_store(data['url'])

    rag_output = rag.query(question=data['question'])
    app.logger.info(rag_output)
    return rag_output

@app.route("/site_change", methods=["POST"])
def reset_vector_store():
    status = {"STATUS": "INTERNAL_SERVER_ERROR", "STATUS_CODE": 405}
    app.logger.info("Calling vector reset from backend.")
    data = request.get_json()
    app.logger.info("Data received in reset_vector_store backend:")
    app.logger.info(data)
    try:
        rag.doc_processor.reset_vector_store(data['url'])
        status["STATUS"] = "OK"
        status["STATUS_CODE"] = 405
        return status
    except:
        return status
    
@app.route("/")
def serve():
    return send_from_directory(app.static_folder, 'index.html')
    
if __name__ == '__main__':
    app.run()