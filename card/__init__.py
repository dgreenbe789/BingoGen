import pathlib
import platform
import azure.functions as func
import pandas as pd
import imgkit
from random import sample

curdir = pathlib.Path(__file__).parent
staticdir = curdir / "static"
bindir = curdir / "binaries"
listdir = curdir / "lists"
dist = platform.dist()

if dist[0] == "debian":
    imgconfig = imgkit.config(wkhtmltoimage=bindir / "wkhtmltoimage")
else:
    imgconfig = None

typeDict  = {
                "conference": ["Conference Call", listdir / "conference.txt", staticdir / "conference.css"]
            }


def main(req: func.HttpRequest) -> func.HttpResponse:
    card = typeDict.get(req.params.get("type"), None)
    if card:
        phrases = open(card[1]).read().splitlines()

        opts = sample(phrases, 25)
        entries = [opts[i:i+5] for i in range(0, 25, 5)]
        df = pd.DataFrame(entries)

        html = f"""
                <h1>{card[0]} Bingo Card</h1>
                {df.to_html(index=False, header=False)}
                """

        response = imgkit.from_string(html, False, css=card[2], config=imgconfig)
        return func.HttpResponse(response, mimetype="image/png")
    else:
        return func.HttpResponse(status_code=404)
