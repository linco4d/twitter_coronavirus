# Coronavirus Twitter Hashtag Analysis

You will scan all geotagged tweets sent in 2020 to monitor for the spread of the coronavirus on social media.
COVID-19 Twitter Hashtag Analysis
This project processes a large corpus of geotagged tweets from 2020 to track how public conversation around the coronavirus evolved over time. Using daily tweet files containing millions of tweets, I developed a MapReduce-style pipeline that:
Extracts language and country usage counts for specific hashtags per day.
Aggregates daily counts across all languages or countries.
Visualizes trends in tweet volume for chosen hashtags.
The primary goal was to measure the temporal spread and volume of COVID-19 related discussion on Twitter — insights relevant to social media analytics, public discourse tracking, and crisis communication research.
🔍 What the Code Does
Map Step: For each day’s geotagged tweets, count how often selected hashtags appear across languages.
Reduce Step: Combine these daily outputs into cumulative counts for each hashtag.
Visualization: Generate time-series plots showing how the usage of key hashtags changes over the year.
All core logic is implemented in Python, with outputs saved as .png charts.
📈 Generated Visualizations
Four distinct plots are produced, each providing insight into how Twitter users discussed the pandemic:
Language Distribution Bar Graphs
Bar charts showing the top languages tweeting each selected COVID-19 hashtag.
Country Distribution Bar Graphs
Bar charts e.g., showing which countries tweeted the most about specific hashtags.
Daily Usage Time Series (per hashtag)
Line plots that track hashtag frequency over the entire year with 48 evenly spaced date ticks.
Multi-hashtag Comparison Plot
A combined time-series showing trends for multiple hashtags on a single chart.
Each visualization captures a different dimension of how conversation about COVID-19 spread across space (languages, countries) and time.
🚀 Why This Matters
This project demonstrates:
Ability to work with large, real-world datasets (~1.1B tweets).
Practical application of parallel data processing (MapReduce).
Skill in data aggregation and visualization for insight extraction.

