Code for task 3 
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import pytz

# Function to check if current time is between 6 PM IST and 8 PM IST
def is_time_to_show_map():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    hour = now.hour
    # 6 PM IST is 18:00, 8 PM IST is 20:00
    return 18 <= hour < 20

# Sample data generation (in a real scenario, load from a dataset)
countries = ['USA', 'IND', 'CHN', 'JPN', 'DEU', 'GBR', 'FRA', 'BRA', 'RUS', 'CAN']
categories = ['Business', 'Education', 'Entertainment', 'Finance', 'Health', 'Lifestyle', 'Medical', 'Music', 'News', 'Photography', 'Productivity', 'Racing', 'Tools', 'Travel', 'Weather']
# Note: All categories in this list do not start with 'A', 'C', 'G', or 'S'

np.random.seed(42)  # For reproducible random data
data = []
for country in countries:
    for cat in categories:
        installs = np.random.randint(1000, 1000000)  # Random installs between 1K and 1M
        data.append([country, cat, installs])

df = pd.DataFrame(data, columns=['country', 'category', 'installs'])

# Calculate total installs per category
total_installs = df.groupby('category')['installs'].sum().reset_index()
# Get top 5 categories by total installs
top5 = total_installs.sort_values('installs', ascending=False).head(5)['category'].tolist()

# Filter data to only top 5 categories
df_filtered = df[df['category'].isin(top5)]

# Map countries to ISO3 codes for Plotly
country_codes = {
    'USA': 'USA', 'IND': 'IND', 'CHN': 'CHN', 'JPN': 'JPN',
    'DEU': 'DEU', 'GBR': 'GBR', 'FRA': 'FRA', 'BRA': 'BRA',
    'RUS': 'RUS', 'CAN': 'CAN'
}
df_filtered['iso'] = df_filtered['country'].map(country_codes)

# Identify categories where total installs exceed 1 million for highlighting
total_filtered = total_installs[total_installs['category'].isin(top5)]
highlighted = total_filtered[total_filtered['installs'] > 1000000]['category'].tolist()

# Check time condition
if is_time_to_show_map():
    # Create interactive Choropleth map with animation by category
    fig = px.choropleth(
        df_filtered,
        locations='iso',
        color='installs',
        animation_frame='category',
        color_continuous_scale='Viridis',
        title=f'Global Installs by Category (Top 5) - Highlighted Categories (>1M installs): {", ".join(highlighted) if highlighted else "None"}',
        labels={'installs': 'Number of Installs'}
         )
    # Customize for highlighting: If a category is highlighted, the animation will show it, and title indicates highlights
    # In a dashboard, you could conditionally style based on highlighted list, but for simplicity, title shows it
    fig.show()
else:
    print("The interactive Choropleth map is only available between 6 PM IST and 8 PM IST. Please check back later.")

<img width="1920" height="1080" alt="Task 3_ Output 3 1" src="https://github.com/user-attachments/assets/7bcaa226-a4b8-4a51-b5f0-133d7cf303d2" />

    RESULT :
    








TASK 4 
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# Define function to check if current time in IST is between 5 PM and 7 PM
def is_time_to_show_chart():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    hour = now.hour
    return 17 <= hour < 19

# Sample DataFrame loading (replace with your actual data loading)
# For example:
# df = pd.read_csv('app_data.csv')

# For demonstration let's create dummy data with needed columns:
data = {
    'app_name': ['GameX', 'BeautyPro', 'BizApp', 'ComicFun', 'Communicate', 'DateNow', 'EntertainX', 'SocialLife', 'EventBuzz'],
    'category': ['Game', 'Beauty', 'Business', 'Comics', 'Communication', 'Dating', 'Entertainment', 'Social', 'Event'],
    'app_size_mb': [150, 40, 110, 70, 90, 30, 200, 50, 60],
    'average_rating': [4.1, 4.0, 4.3, 3.6, 3.9, 4.2, 3.8, 4.5, 4.0],
    'installs': [200000, 75000, 65000, 100000, 300000, 90000, 110000, 70000, 80000],
    'reviews': [600, 700, 800, 650, 900, 550, 750, 850, 620],
    'sentiment_subjectivity': [0.6, 0.7, 0.55, 0.51, 0.6, 0.8, 0.75, 0.6, 0.52]
}
df = pd.DataFrame(data)

# Step: Filter Data

categories = ['Game', 'Beauty', 'Business', 'Comics', 'Communication', 'Dating', 'Entertainment', 'Social', 'Event']

df_filtered = df[
    (df['average_rating'] > 3.5) &
    (df['category'].isin(categories)) &
    (df['reviews'] > 500) &
    (~df['app_name'].str.contains('S', case=False)) &  # app name without 'S' or 's'
    (df['sentiment_subjectivity'] > 0.5) &
    (df['installs'] > 50000)
].copy()

# Step: Translate categories in display

translations = {
    'Beauty': 'सुंदरता',       # Hindi for Beauty
    'Business': 'வணிகம்',       # Tamil for Business
    'Dating': 'Dating'          # German is "Dating" same as English, or "Verabredung"
}

# Apply translation
def translate_category(cat):
    return translations.get(cat, cat)

df_filtered['category_translated'] = df_filtered['category'].apply(translate_category)

# Step: Assign colors - highlight Game in Pink, others default

def get_color(cat):
    if cat == 'Game':
        return 'pink'
    else:
        return 'blue'  # You can assign a palette if you want different colors for others

df_filtered['color'] = df_filtered['category'].apply(get_color)

# Step: Plot Bubble Chart (only if within allowed time window)

if is_time_to_show_chart():
    fig = px.scatter(
        df_filtered,
        x='app_size_mb',
        y='average_rating',
        size='installs',
        color='color',
        hover_name='app_name',
        labels={
            'app_size_mb': 'App Size (MB)',
            'average_rating': 'Average Rating'
        },
        title='Bubble Chart: App Size vs Average Rating with Installs Bubble Size',
        color_discrete_map={'pink': 'pink', 'blue': 'blue'}
    )
    # Show translated categories in legend or hover data
    fig.update_traces(
        marker=dict(sizemode='area', sizeref=2.*max(df_filtered['installs'])/(40.**2), line_width=2),
        selector=dict(mode='markers')
    )
    fig.update_layout(
        legend_title_text='Category',
    )
    # Add category_translated as custom data to show on hover
    fig.for_each_trace(
        lambda trace: trace.update(name=trace.name)
    )
    fig.show()
else:
    print("Bubble chart only visible between 5 PM and 7 PM IST. Please check back later.")

    RESULT :

    
<img width="1920" height="1080" alt="Task 4_output" src="https://github.com/user-attachments/assets/afe65c9d-c771-4802-9f7a-1857c69e4b6c" />



TASK 5 
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import pytz

# Function to check time between 6 PM and 9 PM IST
def is_time_to_show_chart():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    return 18 <= now.hour < 21

# Dummy sample data creation - replace with your actual dataset load
# Date range monthly for 6 months
date_rng = pd.date_range(start='2023-01-01', periods=6, freq='MS')

data = []
apps = [
    {'app_name': 'EntertainmentPlus', 'category': 'Entertainment', 'reviews': 600},
    {'app_name': 'ComicZone', 'category': 'Comics', 'reviews': 700},
    {'app_name': 'BusinessPro', 'category': 'Business', 'reviews': 800},
    {'app_name': 'BeautyMagic', 'category': 'Beauty', 'reviews': 900},
    {'app_name': 'EventMaster', 'category': 'Event', 'reviews': 550},
    {'app_name': 'DatingApp', 'category': 'Dating', 'reviews': 650},
]

np.random.seed(0)
for app in apps:
    for date in date_rng:
        # Random installs between 100k and 500k
        installs = np.random.randint(100000, 500000)
        data.append({
            "app_name": app["app_name"],
            "category": app["category"],
            "date": date,
            "installs": installs,
            "reviews": app["reviews"]
        })

df = pd.DataFrame(data)

# Step 1: Filter data

# Exclude app_name starting with x, y, z
df = df[~df['app_name'].str.lower().str.startswith(('x','y','z'))]

# Category starting with E, C, or B only
df = df[df['category'].str.startswith(('E','C','B'))]

# Reviews > 500
df = df[df['reviews'] > 500]

# app_name NOT containing letter 'S' (case-insensitive)
df = df[~df['app_name'].str.contains('s', case=False)]

# Step 2: Translate categories
translations = {
    'Beauty': 'सुंदरता',       # Hindi
    'Business': 'வணிகம்',       # Tamil
    'Dating': 'Verabredung'     # German (alternate for Dating)
}

def translate_category(cat):
    return translations.get(cat, cat)

df['category_translated'] = df['category'].apply(translate_category)

# Step 3: Aggregate installs by date and category
agg = df.groupby(['date', 'category_translated'])['installs'].sum().reset_index()

# Step 4: Calculate MoM % increase by category
agg.sort_values(by=['category_translated', 'date'], inplace=True)
agg['prev_installs'] = agg.groupby('category_translated')['installs'].shift(1)
agg['mom_growth_pct'] = ((agg['installs'] - agg['prev_installs']) / agg['prev_installs']) * 100

# Identify periods with > 20% growth
agg['high_growth'] = agg['mom_growth_pct'] > 20

# Prepare for plotting
categories = agg['category_translated'].unique()

# Colors for categories, highlight Entertainment or any category as needed
color_map = {
    'Entertainment': 'blue',
    'Comics': 'green',
    'வணிகம்': 'orange',  # Business in Tamil
    'सुंदरता': 'purple',  # Beauty in Hindi
    # You can extend colors here
}

default_color = 'gray'

agg['color'] = agg['category_translated'].map(color_map).fillna(default_color)

# Step 5: Plotting only if current time is between 6 PM and 9 PM IST
if is_time_to_show_chart():
    fig = go.Figure()

    for cat in categories:
        df_cat = agg[agg['category_translated'] == cat]

        # Line plot
        fig.add_trace(go.Scatter(
            x=df_cat['date'],
            y=df_cat['installs'],
            mode='lines+markers',
            name=cat,
            line=dict(color=df_cat['color'].iloc[0]),
        ))

        # Shade high growth areas (where mom_growth > 20%)
        for i in range(1, len(df_cat)):
            if df_cat['high_growth'].iloc[i]:
                fig.add_shape(type='rect',
                              x0=df_cat['date'].iloc[i-1], x1=df_cat['date'].iloc[i],
                              y0=0, y1=df_cat['installs'].max()*1.1,
                              fillcolor='rgba(255, 0, 0, 0.2)', line_width=0, layer='below')

    fig.update_layout(
        title='Total Installs Trend Over Time by Category with Highlighted Growth Periods',
        xaxis_title='Date',
        yaxis_title='Total Installs',
        hovermode='x unified'
    )
    fig.show()
else:
    print("The chart is only available between 6 PM IST and 9 PM IST. Please check back later.")

RESULT :
<img width="1920" height="1080" alt="Task 5_output" src="https://github.com/user-attachments/assets/75d5e107-9b86-44ff-9b1d-b3373b2c9c19" />








