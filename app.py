from flask import Flask, render_template, request, send_file
from geometry import distance_between_points, midpoint, slope
import plotly.graph_objects as go
from io import BytesIO
from reportlab.pdfgen import canvas

app = Flask(__name__)
history = []

@app.route("/", methods=["GET", "POST"])
def home():

    d = None
    m = None
    s = None
    error = None
    graph_html = None

    if request.method == "POST":
        try:
            x1 = float(request.form["x1"])
            y1 = float(request.form["y1"])
            x2 = float(request.form["x2"])
            y2 = float(request.form["y2"])
            action = request.form["action"]

            if action == "distance":
                d = distance_between_points(x1, y1, x2, y2)
                entry = f"({x1}, {y1}) -> ({x2}, {y2}) | D={d}"
                history.append(entry)
                if len(history) > 5:
                    history.pop(0)

            elif action == "midpoint":
                m = midpoint(x1, y1, x2, y2)
                entry = f"({x1}, {y1}) -> ({x2}, {y2}) | D={d}" 
                history.append(entry)
                if len(history) > 5:
                    history.pop(0)
            elif action == "slope":
                s = slope(x1, y1, x2, y2)
                entry = f"({x1},{y1}) -> ({x2}, {y2})"
                history.append(entry)
                if len(history) > 5:
                    history.pop(0)

            elif action == "all":
                d = distance_between_points(x1, y1, x2, y2)
                m = midpoint(x1, y1, x2, y2)
                s = slope(x1, y1, x2, y2)
                entry = f"({x1}, {y1}) -> ({x2},{y2}) | D = {d}"
                history.append(entry)
                if len(history) > 5:
                    history.pop(0)

                
    #plotly graph
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x = [x1, x2],
                y = [y1, y2],
                mode="lines+markers+text",
                text = ["A", "B"],
                textposition="top center"
            ))
            fig.update_layout(
                title="Coordinate plane",
                template="plotly_dark",
                height=400
            )
            graph_html = fig.to_html(full_html=False)
            
        except:
            error = "Please enter valid numbers only"

    return render_template(
        "index.html",
        d=d,
        m=m,
        s=s,
        error=error,
        graph_html=graph_html,
        history=history,
    )
@app.route("/download")
def download():

    buffer = BytesIO()

    p = canvas.Canvas(buffer)

    p.drawString(100,800,"GeoSolver Pro Result")

    if history:
        y = 760

        for item in history:
            p.drawString(100,y,item)
            y -= 20

    p.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="result.pdf",
        mimetype="application/pdf"
    )
if __name__ == "__main__":
    app.run(debug=True)