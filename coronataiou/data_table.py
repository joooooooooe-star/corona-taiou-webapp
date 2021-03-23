import io
import sqlalchemy
import pandas as pd
import matplotlib as plt
from flask import Flask, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)

engine = sqlalchemy.create_engine("sqlite:///healthdata.db")


@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure():
    query = "SELECT temperature, updated FROM daily_record WHERE name =? ORDER BY updated ASC"

    name = 'Adib'
    df = pd.read_sql_query(query, engine, params=(name,))
    temperature = df.temperature
    time = df.updated
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = time
    ys = temperature
    axis.plot(xs, ys)
    plt.ylabel = 'Date'
    plt.xlabel = 'Temperature'
    plt.title = 'Body Temperature'
    return fig


if __name__ == "__main__":
    app.run(port=2000, debug=True)





























