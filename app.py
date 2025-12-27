from flask import Flask, render_template, request
from model import analyze_financials

app = Flask(__name__)

# -------------------------------------------------
# HOME PAGE – DATA INPUT
# -------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------------------------
# ANALYSIS ROUTE – CORE LOGIC
# -------------------------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():

    # Collect 3-year financial statement data
    data = {
        "Revenue": [
            float(request.form["rev1"]),
            float(request.form["rev2"]),
            float(request.form["rev3"])
        ],
        "Profit": [
            float(request.form["profit1"]),
            float(request.form["profit2"]),
            float(request.form["profit3"])
        ],
        "Debt": [
            float(request.form["debt1"]),
            float(request.form["debt2"]),
            float(request.form["debt3"])
        ],
        "Receivables": [
            float(request.form["recv1"]),
            float(request.form["recv2"]),
            float(request.form["recv3"])
        ],
        "CFO": [
            float(request.form["cfo1"]),
            float(request.form["cfo2"]),
            float(request.form["cfo3"])
        ]
    }

    # Run AI-based forensic financial analysis
    score, risk, flags, categories, explanation, suggestions, ratios = analyze_financials(data)

    # Send outputs to result dashboard
    return render_template(
        "result.html",
        score=score,
        risk=risk,
        flags=flags,
        categories=categories,
        explanation=explanation,
        suggestions=suggestions,
        ratios=ratios,
        data=data
    )


# -------------------------------------------------
# RUN APPLICATION
# -------------------------------------------------
if __name__ == "__main__":
    app.run()
