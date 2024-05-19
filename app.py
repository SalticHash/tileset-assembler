from flask import Flask, render_template, request, redirect
from tileset import Tileset
from collision import Collision
from werkzeug.datastructures import FileStorage
from utility import Image2Base64, Json2Base64
app = Flask(__name__)

@app.route("/", methods = ["GET"])
def index():
   return render_template("index.html")
	
@app.route("/make", methods = ["GET", "POST"])
def make():
    if request.method == "POST":
        tilefiles: list[FileStorage] = request.files.getlist("tilefiles") 

        t: Tileset = Tileset(tilefiles)
        images: dict[str: str] = {name: Image2Base64(img) for (name, img) in t.tileset_images.items()}
        
        return render_template("make.html",
            images = images,
            errors = t.errors,
            missing_tilesets = t.missing_tilesets
        )
    else:
        return redirect("/")

@app.route("/makecol", methods = ["GET", "POST"])
def makecol():
    if request.method == "POST":
        colfiles: list[FileStorage] = request.files.getlist("colfiles") 

        t: Collision = Collision(colfiles)
        files: dict[str: str] = {name: Json2Base64(json) for (name, json) in t.files.items()}
        return render_template("makecol.html",
            files = files,
            errors = t.errors
        )
    else:
        return redirect("/")

if __name__ == "__main__":
    app.run(debug = True, port=2770)