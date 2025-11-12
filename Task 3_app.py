# app.py - Choropleth Dash App
import os
import pandas as pd
import pycountry
import pytz
from datetime import datetime
import plotly.express as px
from dash import Dash, html

DATA_PATH = "dataset.csv"
HIGHLIGHT_THRESHOLD = 1_000_000
IST_TZ = pytz.timezone("Asia/Kolkata")
VISIBLE_START = 18  # 6 PM IST
VISIBLE_END = 20    # 8 PM IST
EXCLUDE_PREFIXES = tuple(list("ACGS"))

def country_to_iso3(name):
    try:
        if isinstance(name, str) and len(name) == 3 and name.isalpha():
            return name.upper()
        country = pycountry.countries.lookup(name)
        return country.alpha_3
    except Exception:
        return None

df = pd.read_csv(DATA_PATH)
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce').fillna(0).astype(int)
df['Category'] = df['Category'].astype(str).str.strip()
df = df[~df['Category'].str.upper().str.startswith(EXCLUDE_PREFIXES)].copy()
df['ISO3'] = df['Country'].apply(country_to_iso3)
df = df[df['ISO3'].notna()].copy()

agg = df.groupby(['Category','ISO3'], as_index=False)['Installs'].sum()
category_totals = agg.groupby('Category', as_index=False)['Installs'].sum()
top5 = category_totals.sort_values('Installs', ascending=False).head(5)['Category'].tolist()
agg_top5 = agg[agg['Category'].isin(top5)].copy()
country_installs = agg_top5.groupby('ISO3', as_index=False)['Installs'].sum()
country_installs['highlight'] = country_installs['Installs'] > HIGHLIGHT_THRESHOLD

fig = px.choropleth(country_installs, locations='ISO3', color='Installs', projection='natural earth',
                    color_continuous_scale='Viridis', labels={'Installs':'Total Installs'})

def is_visible_now_ist():
    now_ist = datetime.now(IST_TZ)
    h = now_ist.hour
    return (h >= VISIBLE_START) and (h < VISIBLE_END)

app = Dash(__name__)

if is_visible_now_ist():
    app.layout = html.Div([html.H2("Choropleth Map - Top 5 Categories (6-8 PM IST)"),
                           html.Div(id='graph', children=[html.Iframe(srcDoc=fig.to_html(full_html=False), style={'width':'100%','height':'700px','border':'none'})])])
else:
    app.layout = html.Div([html.H2("Map hidden — visible only between 6 PM and 8 PM IST")])

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
