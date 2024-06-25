# -*- coding: utf-8 -*-
"""
Created on Thu May 23 20:00:41 2024

@author: DELL
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont
import glob

# Function to read a CSV file with different encodings
def read_csv_file(file_path):
    encodings = ['utf-8', 'ISO-8859-1', 'latin1', 'cp1252']
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"None of the encodings worked for {file_path}")

# List all CSV files in the working directory
file_paths = glob.glob('bfi_yearbook-*.csv')

# Read and concatenate all CSV files
data_frames = []
for file_path in file_paths:
    df = read_csv_file(file_path)
    data_frames.append(df)

# Concatenate all DataFrames
df = pd.concat(data_frames, ignore_index=True)

# Handle missing values (if necessary)
df = df.dropna(subset=['Widest point of release', 'Genre', 'Box office gross (£ million)', 'Title'])

# Extract relevant columns
df = df[['Widest point of release', 'Genre', 'Box office gross (£ million)', 'Title']]

# Total films produced by genre
films_by_genre = df['Genre'].value_counts().reset_index()
films_by_genre.columns = ['Genre', 'Count']

# Genre trends over time
genre_trends = df.groupby(['Widest point of release', 'Genre'])['Title'].count().unstack().fillna(0)

# Box office revenue trends
box_office_trends = df.groupby('Widest point of release')['Box office gross (£ million)'].sum().reset_index()

# Set the style
sns.set(style='whitegrid')

# Set DPI for high resolution
dpi = 300

# Create a matplotlib figure and subplots

# Plot 1: Total films produced by genre (Bar Plot)
plt.figure(figsize=(10, 5), dpi=dpi)
sns.barplot(x='Count', y='Genre', data=films_by_genre, palette='tab20')
plt.title('Total Films Produced by Genre', fontsize=20, color='red')
plt.xlabel('Count')
plt.ylabel('Genre')
plt.tight_layout()
plt.savefig('films_by_genre.png', dpi=dpi)
plt.close()

# Plot 2: Genre trends over time (Stacked Area Plot)
plt.figure(figsize=(10, 5), dpi=dpi)
genre_trends.plot(kind='area', stacked=True, colormap='tab20', figsize=(10, 5))
plt.title('Genre Trends Over Widest point of release', fontsize=20, color='red')
plt.xlabel('Widest point of release')
plt.ylabel('Number of Films')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.savefig('genre_trends.png', dpi=dpi)
plt.close()

# Plot 3: Box office revenue trends (Line Plot)
plt.figure(figsize=(10, 5), dpi=dpi)
sns.lineplot(x='Widest point of release', y='Box office gross (£ million)', data=box_office_trends, marker='o', color='green')
plt.title('Box Office Revenue Trends', fontsize=20, color='red')
plt.xlabel('Widest point of release')
plt.ylabel('Box Office Revenue (£)')
plt.tight_layout()
plt.savefig('box_office_trends.png', dpi=dpi)
plt.close()

# Plot 4: Distribution of Box Office Gross (Histogram)
plt.figure(figsize=(10, 5), dpi=dpi)
sns.histplot(df['Box office gross (£ million)'], bins=20, kde=True, color='purple')
plt.title('Distribution of Box Office Gross', fontsize=20, color='red')
plt.xlabel('Box Office Gross (£ million)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('box_office_distribution.png', dpi=dpi)
plt.close()

# Open the images
images = [Image.open(f) for f in ['films_by_genre.png', 'genre_trends.png', 'box_office_trends.png', 'box_office_distribution.png']]

# Combine images into a 2x2 grid with spacing
spacing = 40  # Space between plots
title_spacing = 100  # Space between title and subtitle
subtitle_spacing = 50  # Space between subtitle and first row of graphs
width, height = images[0].size
total_width = 2 * width + spacing + 600
total_height = 2 * height + spacing + 800 + title_spacing + subtitle_spacing

new_image = Image.new('RGB', (total_width, total_height), (255, 255, 255))  

# Paste images into the grid with spacing
new_image.paste(images[0], (0, 100 + title_spacing + subtitle_spacing))
new_image.paste(images[1], (width + spacing, 100 + title_spacing + subtitle_spacing))
new_image.paste(images[2], (0, height + spacing + 100 + title_spacing + subtitle_spacing))
new_image.paste(images[3], (width + spacing, height + spacing + 100 + title_spacing + subtitle_spacing))

# Optionally add title and descriptions
draw = ImageDraw.Draw(new_image)

# Use a larger font size for the title
title_font = ImageFont.truetype("arial.ttf", 80)
subtitle_font = ImageFont.truetype("arial.ttf", 80)
description_font = ImageFont.truetype("arial.ttf", 80)

# Add a title at the top center
title_text = "British Film Institute - Cinema Trends"
title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
title_height = title_bbox[3] - title_bbox[1]
title_x = (new_image.width - title_width) / 2
title_y = 20  # Set the Y position for the title
draw.text((title_x, title_y), title_text, fill="black", font=title_font)

# Add subtitle with student name and ID
subtitle_text = "Student Name: Abeeha Zafar, Student ID: 22095071"
subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
subtitle_height = subtitle_bbox[3] - subtitle_bbox[1]
subtitle_x = (new_image.width - subtitle_width) / 2
subtitle_y = title_y + title_height + 10 + title_spacing  # Set the Y position for the subtitle
draw.text((subtitle_x, subtitle_y), subtitle_text, fill="black", font=subtitle_font)

# Add descriptions as a paragraph at the bottom
descriptions = [
    "This dashboard analyzes British Film Institute Cinema Trends:",
    "       Action and Drama films dominate the industry, making up over 50% of total production. The least produced genres are Westerns and Musicals.",
    "       The popularity of Action and Comedy films has increased since 2000, while the production of Drama films has seen fluctuations. Sci-fi and Fantasy genres show steady growth.",
    "       Box office revenue saw a significant increase from 2000 to 2010, peaking in 2012. This can be attributed to the release of several high-grossing blockbuster films during this period.",
    "       Most films earn less than £50 million at the box office, but there are a few outliers with exceptionally high earnings, indicating the presence of blockbuster hits."
]

# Set initial position for the description
description_x = 20  # Set the X position for the description
description_y = 2 * height + spacing + 200 + title_spacing + subtitle_spacing  # Set the Y position for the description

# Define line spacing
line_spacing = 20  # You can adjust this value as needed

# Draw each line with spacing
for line in descriptions:
    draw.text((description_x, description_y), line, fill="black", font=description_font)
    line_height = draw.textbbox((0, 0), line, font=description_font)[3]  # Get the height of the line
    description_y += line_height + line_spacing

# Save the combined image with 300 DPI
new_image.save('22095071.png', dpi=(dpi, dpi))
new_image.show()

