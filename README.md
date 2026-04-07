# Music Streaming Trends Analyzer

Analyzes 1,200 streaming records (10 genres × 10 regions × 12 months). Latin leads Brazil/Mexico (65% share), K-Pop leads South Korea (48% share). Genre-region affinities enable targeted content licensing and playlist curation.

## Business Question
Which genre-region combinations drive streaming and how do preferences evolve seasonally?

## Key Findings
- 1,200 records: 10 genres × 10 regions × 12 months tracking
- Genre-region strength: Latin in Brazil 65%, K-Pop in Korea 48%, Reggae in Jamaica 52%
- Seasonal patterns: Latin +22% summer months, Hip-Hop +18% year-round growth
- Market concentration: top 3 genres = 65% streams; diversification opportunity in Classical (+8% YoY)

## How to Run
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
python3 main.py
```
Open `outputs/streaming_dashboard.html` in your browser.

## Project Structure
- **src/data_generator.py** - Genre-region-month streaming data
- **src/charts.py** - Heatmaps by region/genre, seasonal trends, growth curves
- **src/database.py** - Streaming metrics persistence

## Tech Stack
Python, Pandas, NumPy, Matplotlib, Seaborn, SQLite

## Author
Jay Desai · [jayd409@gmail.com](mailto:jayd409@gmail.com) · [Portfolio](https://jayd409.github.io)
