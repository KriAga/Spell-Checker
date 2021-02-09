import hunspell
from bs4 import BeautifulSoup
import requests
import re
from flask import Flask, render_template, request
import csv, nltk

app = Flask(__name__)

from collections import defaultdict
mydict = defaultdict(list)

with open("marathi_bigram_count.txt", newline='') as f:
    for row in csv.reader(f, delimiter = ' '):
        mydict[row[0].strip()].append(row[1].strip())

spellchecker = hunspell.HunSpell(
    "./marathi_words_updates.oxt_FILES/dicts/mr_IN.dic",
    "./marathi_words_updates.oxt_FILES/dicts/mr_IN.aff",
)

spellchecker_split = hunspell.HunSpell(
    "./marathi_words_updates.oxt_FILES/dicts/mr_IN.dic",
    "./marathi_words_updates.oxt_FILES/dicts/mr_IN_split.aff",
)
words = list()

@app.route('/')
def index():
    return render_template("index.html")

def mycheck(myword):
    if spellchecker.spell(myword[1]) is False and len(myword[1]) > 3:
        try:
            if len(myword[1]) > 12:
                word_result = {
                    'original_word': myword[1],
                    'corrected_word': spellchecker_split.suggest(myword[1])
                }
            else:
                word_result = {
                    'original_word': myword[1],
                    'corrected_word': spellchecker.suggest(myword[1])
                }

            result = mydict[myword[0]]

            list_one_updated = list()
            for i in word_result['corrected_word']:
                if i in result:
                    list_one_updated.append(i)

            for i in word_result['corrected_word']:
                if i not in result:
                    list_one_updated.append(i)

            words.append({'original_word': myword[1], 'corrected_word': list_one_updated[0]})
            return
        except:
            pass


@app.route('/process', methods=['POST', 'GET'])
def process():
    if request.method == 'POST':
        from collections import defaultdict
        mydict = defaultdict(list)

        with open("marathi_bigram_count.txt", newline='') as f:
            for row in csv.reader(f, delimiter = ' '):
                mydict[row[0].strip()].append(row[1].strip())
                
        url = request.form['url']
        print(url)
        headers = requests.utils.default_headers()
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        words.clear()
        p = re.compile(r"[^\u0900-\u097F\n]")
        for line in text.splitlines():
            cleaned = p.sub(" ", line)
            if cleaned.strip():
                mycheck(('NULL', cleaned.split()[0]))
                for i in nltk.bigrams(cleaned.split()):
                    mycheck(i)
        return render_template("success.html", words=words)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

