from flask import Flask, request, json, send_file
from flask import send_from_directory
from character import generateCharacter
from cairosvg import svg2png

app = Flask(__name__, static_url_path="/")


@app.route("/")
def home_page():
    return send_from_directory("static/", "index.html")


@app.route("/character", methods=["POST"])
def getCharacter():
    figure = {"svg": generateCharacter()}

    return figure


@app.route("/download", methods=["POST"])
def downloadCharacter():
    xml = request.json["svgCode"]
    with open("character.svg", "w") as f:
        f.write(xml)
    if request.json["type"] == "svg":
        return send_file("character.svg", mimetype="image/svg+xml")
    elif request.json["type"] == "png":
        svg2png(url="character.svg", write_to="character.png")
        return send_file("character.png", mimetype="image/png")


@app.route("/api/getchar/type=<type>", methods=["GET"])
def api(type):
    response = dict()
    char = generateCharacter()
    with open("./static/char.svg", "w") as f:
        f.write(char)
    if type == "svg":
        response = {
            "status": 200,
            "type": "svg",
            "url": f"{request.scheme}://{request.host}/char.svg",
        }
    elif type == "png":
        svg2png(url="./static/char.svg", write_to="./static/char.png")
        response = {
            "status": 200,
            "type": "png",
            "url": f"{request.scheme}://{request.host}/char.png",
        }

    else:
        response = {
                "status" : "error",
                "type" : None,
                "url" : None
                }
    return response 

app.run(debug=True)
