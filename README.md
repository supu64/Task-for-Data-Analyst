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
    
