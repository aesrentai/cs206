from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from parse import get_facts
from sources import SearchResult, get_sources
import json

app = Flask(__name__)
CORS(app)

"""
interface Source {
    title: string;
    url: string;
    description: string;
}
interface Sources {Sources[]}
"""
@app.route('/', methods=['POST'])
def index():
    req_data = request.get_json()

    if not 'text' in req_data:
        abort(400, description='Missing or empty "text" field in request body')

    facts = get_facts(req_data["text"])
    print("FACTS")
    print(facts)
    sources_dict = {}
    for fact in facts:
        sources_dict[fact] = get_sources(fact)

    formatted_sources = []
    for fact, sources in sources_dict.items():
        formatted_source_list = []
        for source in sources:
            formatted_source_list.append({
                "title": source.title,
                "url": source.url,
                "description": source.description
            })
        #formatted_sources[fact] = formatted_source_list
        formatted_sources.append(formatted_source_list)

    #json.dumps("item": {"fact": fact, "sources"
    ret = json.dumps([{"fact": fact, "sources": sources} for fact, sources in zip(facts, formatted_sources)])
    print(ret)

    #return jsonify(formatted_sources)
    return ret

app.run(host='localhost', port=40000)
