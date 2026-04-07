import sys, os
sys.path.insert(0, 'src')
os.makedirs('outputs', exist_ok=True)

from data_generator import (generate_genre_streams, generate_artist_popularity,
                             generate_playlists, generate_audio_features,
                             save_to_db, query)

print("=" * 55)
print("  Music Streaming Trends Analyzer (2023)")
print("=" * 55)

genres   = generate_genre_streams()
artists  = generate_artist_popularity()
playlists = generate_playlists()
audio    = generate_audio_features()

save_to_db(genres, artists, playlists, audio)

print(f"\n  Genre stream records : {len(genres)}")
print(f"  Artist records       : {len(artists)}")
print(f"  Playlists analyzed   : {len(playlists)}")
print(f"  Tracks (audio feats) : {len(audio)}")

# ── Top genres globally
print("\n--- Top Genres by Global Streams (2023) ---")
r1 = query("""
    SELECT genre,
           ROUND(SUM(streams_millions), 0) AS total_streams_m,
           ROUND(AVG(streams_millions), 1) AS avg_monthly_m
    FROM genre_streams
    GROUP BY genre
    ORDER BY total_streams_m DESC
""")
print(r1.to_string(index=False))

# ── Top genres by region (annual)
print("\n--- Dominant Genre per Region (2023) ---")
r2 = query("""
    SELECT region, genre, ROUND(SUM(streams_millions), 0) AS streams_m
    FROM genre_streams
    GROUP BY region, genre
    HAVING streams_m = (
        SELECT MAX(total) FROM (
            SELECT region AS r, SUM(streams_millions) AS total
            FROM genre_streams AS g2
            WHERE g2.region = genre_streams.region
            GROUP BY genre
        )
    )
    ORDER BY region
""")
print(r2.to_string(index=False))

# ── Top artists by average popularity score
print("\n--- Top 10 Artists by Average Popularity Score ---")
r3 = query("""
    SELECT artist, genre,
           ROUND(AVG(popularity_score), 1) AS avg_popularity,
           ROUND(AVG(estimated_streams_m), 0) AS avg_monthly_streams_m
    FROM artist_popularity
    GROUP BY artist
    ORDER BY avg_popularity DESC
    LIMIT 10
""")
print(r3.to_string(index=False))

# ── Playlist performance
print("\n--- Playlist Performance (by type) ---")
r4 = query("""
    SELECT type,
           COUNT(*) AS playlists,
           ROUND(AVG(followers_k), 0)       AS avg_followers_k,
           ROUND(AVG(avg_daily_streams), 0) AS avg_daily_streams,
           ROUND(AVG(skip_rate), 3)         AS avg_skip_rate
    FROM playlists
    GROUP BY type
""")
print(r4.to_string(index=False))

# ── Audio feature correlations (high energy + high danceability tracks)
print("\n--- High Energy + High Danceability Tracks ---")
r5 = query("""
    SELECT title, artist, genre,
           tempo_bpm, energy, danceability, valence
    FROM audio_features
    WHERE energy > 0.65 AND danceability > 0.65
    ORDER BY energy DESC
""")
print(r5.to_string(index=False))

print("\n✓  Analysis complete. Database saved to outputs/data.db")
