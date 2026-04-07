"""
Realistic music streaming trends data generator.
Covers top genres by region, artist popularity, playlist performance,
and audio feature correlations (tempo, energy, danceability).
"""
import random
import sqlite3
import pandas as pd

random.seed(99)

REGIONS = ["United States", "United Kingdom", "Brazil", "India",
           "Germany", "Japan", "Mexico", "Australia", "Canada", "South Korea"]

GENRES = ["Pop", "Hip-Hop/Rap", "R&B", "Latin", "Electronic/Dance",
          "Rock", "K-Pop", "Bollywood", "Country", "Jazz/Soul"]

# Realistic top artists per genre
ARTISTS = {
    "Pop":               ["Taylor Swift", "Harry Styles", "Dua Lipa", "Ed Sheeran", "Olivia Rodrigo"],
    "Hip-Hop/Rap":       ["Drake", "Kendrick Lamar", "Travis Scott", "Post Malone", "Cardi B"],
    "R&B":               ["The Weeknd", "SZA", "Frank Ocean", "H.E.R.", "Bryson Tiller"],
    "Latin":             ["Bad Bunny", "J Balvin", "Ozuna", "Karol G", "Maluma"],
    "Electronic/Dance":  ["David Guetta", "Calvin Harris", "Martin Garrix", "Marshmello", "Kygo"],
    "Rock":              ["Imagine Dragons", "Twenty One Pilots", "Coldplay", "Foo Fighters", "Arctic Monkeys"],
    "K-Pop":             ["BTS", "BLACKPINK", "Stray Kids", "TWICE", "aespa"],
    "Bollywood":         ["Arijit Singh", "Shreya Ghoshal", "Jubin Nautiyal", "Neha Kakkar", "Armaan Malik"],
    "Country":           ["Morgan Wallen", "Luke Combs", "Zach Bryan", "Carrie Underwood", "Kane Brown"],
    "Jazz/Soul":         ["Kendrick Lamar", "Lizzo", "Leon Bridges", "Norah Jones", "Gregory Porter"],
}

# Genre popularity weight by region
REGION_GENRE_WEIGHTS = {
    "United States":  [0.22, 0.20, 0.13, 0.08, 0.07, 0.10, 0.03, 0.01, 0.10, 0.06],
    "United Kingdom": [0.24, 0.14, 0.10, 0.05, 0.12, 0.14, 0.04, 0.02, 0.04, 0.11],
    "Brazil":         [0.15, 0.12, 0.08, 0.30, 0.09, 0.08, 0.03, 0.01, 0.06, 0.08],
    "India":          [0.12, 0.06, 0.06, 0.05, 0.07, 0.06, 0.05, 0.40, 0.02, 0.11],
    "Germany":        [0.20, 0.12, 0.08, 0.06, 0.20, 0.15, 0.04, 0.01, 0.04, 0.10],
    "Japan":          [0.18, 0.09, 0.07, 0.04, 0.14, 0.12, 0.18, 0.02, 0.03, 0.13],
    "Mexico":         [0.14, 0.11, 0.07, 0.32, 0.08, 0.10, 0.03, 0.01, 0.05, 0.09],
    "Australia":      [0.23, 0.14, 0.10, 0.06, 0.10, 0.14, 0.04, 0.01, 0.08, 0.10],
    "Canada":         [0.21, 0.19, 0.12, 0.07, 0.09, 0.11, 0.04, 0.01, 0.07, 0.09],
    "South Korea":    [0.16, 0.08, 0.07, 0.04, 0.12, 0.08, 0.32, 0.01, 0.02, 0.10],
}


def generate_genre_streams():
    """Monthly genre stream counts by region (millions) over 12 months."""
    rows = []
    gid = 1
    months = [f"2023-{m:02d}" for m in range(1, 13)]
    for region in REGIONS:
        weights = REGION_GENRE_WEIGHTS[region]
        for month in months:
            total = random.uniform(800, 3500)  # total streams in millions
            for i, genre in enumerate(GENRES):
                streams = round(total * weights[i] * random.uniform(0.9, 1.1), 1)
                rows.append({"stream_id": gid, "region": region, "month": month,
                              "genre": genre, "streams_millions": streams})
                gid += 1
    return pd.DataFrame(rows)


def generate_artist_popularity():
    """Artist monthly popularity scores (0-100) and stream estimates."""
    rows = []
    aid = 1
    months = [f"2023-{m:02d}" for m in range(1, 13)]
    for genre, artists in ARTISTS.items():
        for rank, artist in enumerate(artists, 1):
            base_pop = max(30, 95 - rank * 8 + random.randint(-5, 5))
            for month in months:
                seasonal = 1.0
                if month in ["2023-11", "2023-12"]:
                    seasonal = 1.12  # holiday boost
                popularity = min(100, round(base_pop * seasonal + random.uniform(-3, 3)))
                streams = round(popularity * random.uniform(18, 35), 0)
                rows.append({"artist_id": aid, "artist": artist, "genre": genre,
                              "month": month, "popularity_score": popularity,
                              "estimated_streams_m": streams})
                aid += 1
    return pd.DataFrame(rows)


def generate_playlists():
    """Playlist performance metrics."""
    PLAYLISTS = [
        ("Today's Top Hits",    "Pop",              "curated",  92),
        ("RapCaviar",           "Hip-Hop/Rap",      "curated",  90),
        ("Hot Country",         "Country",          "curated",  82),
        ("Latin Hits",          "Latin",            "curated",  88),
        ("mint",                "Electronic/Dance", "curated",  85),
        ("New Music Friday",    "Pop",              "curated",  87),
        ("Peaceful Piano",      "Jazz/Soul",        "mood",     78),
        ("Workout Anthems",     "Pop",              "mood",     80),
        ("Morning Motivation",  "Pop",              "mood",     76),
        ("Chill Hits",          "Pop",              "mood",     83),
        ("K-Pop Daebak",        "K-Pop",            "curated",  86),
        ("Bollywood Butter",    "Bollywood",        "curated",  75),
        ("Rock Classics",       "Rock",             "curated",  81),
        ("Viva Latino",         "Latin",            "curated",  89),
        ("Party Hits",          "Pop",              "mood",     84),
    ]
    rows = []
    for pid, (name, genre, ptype, base_score) in enumerate(PLAYLISTS, 1):
        followers = round(base_score * random.uniform(0.8, 1.5) * 1_000, 0)
        avg_streams = round(followers * random.uniform(0.04, 0.12), 0)
        skip_rate = round(random.uniform(0.12, 0.38), 3)
        saves = round(avg_streams * random.uniform(0.05, 0.18), 0)
        rows.append({"playlist_id": pid, "playlist_name": name, "genre": genre,
                     "type": ptype, "quality_score": base_score,
                     "followers_k": followers, "avg_daily_streams": avg_streams,
                     "skip_rate": skip_rate, "saves_per_day": saves})
    return pd.DataFrame(rows)


def generate_audio_features():
    """Track-level audio features for top songs (tempo, energy, danceability, valence)."""
    TRACKS = [
        ("Anti-Hero",           "Taylor Swift",     "Pop"),
        ("Rich Flex",           "Drake",            "Hip-Hop/Rap"),
        ("Flowers",             "Miley Cyrus",      "Pop"),
        ("Ella Baila Sola",     "Eslabon Armado",   "Latin"),
        ("Kill Bill",           "SZA",              "R&B"),
        ("Creepin'",            "Metro Boomin",     "Hip-Hop/Rap"),
        ("Calm Down",           "Rema",             "Pop"),
        ("Chemical",            "Post Malone",      "Pop"),
        ("Cruel Summer",        "Taylor Swift",     "Pop"),
        ("Unholy",              "Sam Smith",        "Pop"),
        ("STAY",                "The Kid LAROI",    "Pop"),
        ("My Universe",         "Coldplay",         "Rock"),
        ("About Damn Time",     "Lizzo",            "Pop"),
        ("Levitating",          "Dua Lipa",         "Pop"),
        ("As It Was",           "Harry Styles",     "Pop"),
    ]
    rows = []
    for tid, (title, artist, genre) in enumerate(TRACKS, 1):
        tempo = round(random.uniform(85, 165), 1)
        energy = round(random.uniform(0.35, 0.97), 3)
        danceability = round(random.uniform(0.40, 0.95), 3)
        valence = round(random.uniform(0.20, 0.92), 3)
        acousticness = round(random.uniform(0.01, 0.65), 3)
        rows.append({"track_id": tid, "title": title, "artist": artist,
                     "genre": genre, "tempo_bpm": tempo, "energy": energy,
                     "danceability": danceability, "valence": valence,
                     "acousticness": acousticness})
    return pd.DataFrame(rows)


def save_to_db(genre_df, artist_df, playlist_df, audio_df, db_path="outputs/data.db"):
    conn = sqlite3.connect(db_path)
    genre_df.to_sql("genre_streams",    conn, if_exists="replace", index=False)
    artist_df.to_sql("artist_popularity", conn, if_exists="replace", index=False)
    playlist_df.to_sql("playlists",     conn, if_exists="replace", index=False)
    audio_df.to_sql("audio_features",   conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()


def query(sql, db_path="outputs/data.db"):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df
