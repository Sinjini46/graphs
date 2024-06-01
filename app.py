from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio
import json

app = Flask(__name__)

@app.route('/')
def index():
    # Load your JSON data
    with open('eve.json', 'r') as file:
        data = [json.loads(line) for line in file]

    # Convert to DataFrame
    df = pd.json_normalize(data)

    # Plot 1: Number of Alerts by Source IP
    src_ip_counts = df['src_ip'].value_counts().head(10)
    fig1 = px.bar(x=src_ip_counts.index, y=src_ip_counts.values, title='Number of Alerts by Source IP')
    fig1.update_layout(template='plotly_dark')
    plot1 = pio.to_html(fig1, full_html=False)

    # Plot 2: Number of Alerts by Destination Port
    dest_port_counts = df['dest_port'].value_counts().head(10)
    fig2 = px.bar(x=dest_port_counts.index, y=dest_port_counts.values, title='Number of Alerts by Destination Port')
    fig2.update_layout(template='plotly_dark')
    plot2 = pio.to_html(fig2, full_html=False)

    # Plot 3: Alerts Over Time
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    alerts_over_time = df.set_index('timestamp').resample('D').size()
    fig3 = px.line(x=alerts_over_time.index, y=alerts_over_time.values, title='Alerts Over Time')
    fig3.update_layout(template='plotly_dark')
    plot3 = pio.to_html(fig3, full_html=False)

    return render_template('index.html', plot1=plot1, plot2=plot2, plot3=plot3)

if __name__ == '__main__':
    app.run(debug=True)
