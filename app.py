from urllib.parse import urlparse

from flask import Flask, render_template, request
import pickle

SHORTER_SERVICES = {  # Example list of shortening services (update as needed)
   "bit.ly","tinyurl.com","goo.gl","cutt.ly","t.co" ,"is.gd","shrt.co","tiny.cc", "ow.ly", "buff.ly", "rebrand.ly",
    "bl.ocks.org","yourls.org","adfoc.us",  "bc.vc", "bit.do", "bitly.com", "bpaste.net","brnd.ly","bz.im","clck.ru",
     "clk.sh", "da.gd","db.tt","dbrd.co","dis.gd","dly.hk","dnurl.com","doyour.ws","drve.me","du.tl","dwz.io",
    "ebook.io", "ever.io","fb.me",  "ff.im","fh.st","ft.tt", "goo.gl",  "goo.to","gurl.me","gv.co",
    "hex.io","hid.re", "hm.co","hst.sh", "ht.ly", "icewarp.com", "im.ki","is.gd", "is.gd/u", "it.ly", "j.mp", "k.st", "kartOO.com", "kgs.fm",
    "kl.to", "knowyour.link", "krurl.com", "kut.tl", "leaddy.io", "li.st","link.tl", "lnk.gd", "lnkd.in", "lnki.us", "lrn.li", "lnkurl.io", 
    "loo.gl", "lyt.ly", "mcaf.ee", "mcg.io", "me.dm", "mediashare.com", "min.us", "m͎b͎l͎.͎o͎n͎l͎y͎", "mightyurl.com", "moourl.com", "mrln.io", 
    "mvb.me", "my.id", "myurl.com", "nblo.at", "neu.li", "ninj.ly", "nsfw.in", "oc.lc", "om.ly", "ow.ly", "p.tl", "paper.li", "pb.me", 
    "pic.gd", "ping.fm", "plr.to", "pnt.st", "po.st", "pow.ερ", "post.ly", "ppt.cc", "PressForward.com", 
    "prv.lu", "pu.sh", "q.gs", "qr.ae", "qtl.io", "qv.to", "rb.gy"
}

app = Flask(__name__)
model = pickle.load(open('data_final.pkl', 'rb'))


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        url = request.form['url']

        # Analyze URL features
        url_features = analyze_url(url)

        # Make prediction using the model with the extracted features
        #prediction = model.predict([url_features])
        prediction = model.predict([list(url_features.values())])

        prediction_text = "This URL is safe to open" if prediction == 1 else "This  URL is not safe to use"

        return render_template("prediction.html", prediction_text=prediction_text)
    else:
        return render_template("prediction.html")


def analyze_url(url):
    features = {}

    # Parse the URL
    parsed_url = urlparse(url)

    # Check for features
    
    features["having_IP_Address"] = 1 if parsed_url.netloc.split(".") and all(
        part.isdigit() or (len(part) == 1 and part.isalpha()) for part in parsed_url.netloc.split(".")
    ) else -1

    # URL length feature
    features["URL_Length"] = 1 if len(url) < 60 else -1

    # Shortening service presence
    features["Shortening_Service"] = 1 if parsed_url.netloc.lower() in SHORTER_SERVICES else -1
    features["having_At_Symbol"] = 1 if parsed_url.netloc and "@" in parsed_url.netloc else -1  # Check for "@" in netloc (handle empty netloc)
    # New feature: double_slash_redirecting
    features["double_slash_redirecting"] = 1 if parsed_url.netloc and parsed_url.netloc.endswith("//") else -1

    # New feature: Prefix_Suffix
    features["Prefix_Suffix"] = 1 if parsed_url.netloc and "-" in parsed_url.netloc else -1

    # New feature: having_Sub_Domain
    features["having_Sub_Domain"] = len(parsed_url.netloc.split(".")) - 2 if parsed_url.netloc else -1  # Count subdomains (excluding domain and TLD)

    # New feature: HTTPS_token
    features["HTTPS_token"] = 1 if parsed_url.scheme == 'https' else -1

    # ... Add other logic for your features (e.g., LongURL, etc.)

    return features


if __name__ == "__main__":
    app.run(debug=True)
