import hunspell
from bs4 import BeautifulSoup
import requests
import re
from flask import Flask, render_template, request

app = Flask(__name__)

spellchecker = hunspell.HunSpell(
    "./marathi_words_updates.oxt_FILES/dicts/mr_IN.dic",
    "./marathi_words_updates.oxt_FILES/dicts/mr_IN.aff",
)
words = list()

@app.route('/')
def index():
    return render_template("index.html")


def mycheck(myword):
    if spellchecker.spell(myword) is False:
        try:
            word_result = {
                'original_word': myword,
                'corrected_word': spellchecker.suggest(myword)[0]
            }
            words.append(word_result)
            return
        except:
            pass


@app.route('/process', methods=['POST', 'GET'])
def process():
    if request.method == 'POST':
        url = request.form['url']
        print(url)
        headers = requests.utils.default_headers()
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()

        p = re.compile(r"[^\u0900-\u097F\n]")
        for line in text.splitlines():
            cleaned = p.sub(" ", line)
            if cleaned.strip():
                for i in cleaned.split():
                    mycheck(i)
        return render_template("success.html", words=words)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
