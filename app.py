from flask import Flask, Response, stream_with_context, request
from flask_cors import cross_origin
from dotenv import load_dotenv

from agent import ask_ollama, ask_ollama_stream

load_dotenv()

app = Flask(__name__)

@app.route("/api/chat/stream", methods=["POST"])
@cross_origin()
def chat_stream():
    body = request.get_json()
    if not body or "user_prompt" not in body or "chat_id" not in body:
        return Response("Invalid request", status=400)
    
    user_prompt = body["user_prompt"]
    chat_id = body["chat_id"]

    def generate():
        for chunk in ask_ollama_stream(prompt=user_prompt, session_id=chat_id):
            # Stream as Server-Sent Events (SSE) format
            output = chunk.get("messages", None)
            if output:
                yield f"data: {output[0].content}\n\n".encode("utf-8")

    return Response(stream_with_context(generate()), mimetype="text/event-stream")

@app.route("/api/chat", methods=["POST"])
@cross_origin()
def chat():
    body = request.get_json()
    if not body or "user_prompt" not in body or "chat_id" not in body:
        return Response("Invalid request", status=400)
    
    user_prompt = body["user_prompt"]
    chat_id = body["chat_id"]

    llm_resp = ask_ollama(user_prompt, session_id=chat_id)
    answer = llm_resp["output"]
    
    result = {"answer": answer}

    return result

if __name__ == "__main__":
    app.run(port=5000, threaded=True)


