import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
df = pd.read_csv('charts.csv')

# Ensure that 'date' is recognized as a datetime object
df['date'] = pd.to_datetime(df['date'])

# Custom CSS for background image, button, and sidebar color
st.markdown(
    """
    <style>
    /* Background image */
    .stApp {
        background-image: url("https://brandingforum.org/wp-content/uploads/2023/10/spotify-logo-1024x651.webp");
        background-size: cover;
        background-position: center;
    }

    /* Sidebar styling */
    .stSidebar {
        background-color: #1DB954;
    }

    /* Button styling */
    .stButton button {
        background-color: black;
        color: white;
        border-radius: 5px;
        border: 2px solid white;
    }

    /* Text styling for white text on the dashboard */
    .stMarkdown, .stTitle, .stHeader {
        color: white;
    }

    /* Force the main content text color to white */
    .stApp .main {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app title
st.title('Spotify Data Dashboard')

# Sidebar for visualization selection
st.sidebar.title('Select Visualization')

# Default view: Show the DataFrame head(10) on app load
st.write("### First 10 rows of the Dataset")
st.dataframe(df.head(10))

# Sidebar button for viewing the entire DataFrame
if st.sidebar.button('DataFrame'):
    st.write("### Full Dataset")
    st.dataframe(df)  

# **Add a new button for showing descriptive statistics**
if st.sidebar.button('Show Data Description'):
    st.write("### Descriptive Statistics of the Dataset")
    st.write(df.describe())

# Sidebar selectbox for visualizations
option = st.sidebar.selectbox('Choose a chart:', 
                              ['Number of Songs by Region', 
                               'Distribution of Song Streams Across Regions',
                               'Average Popularity of Songs Over Time',
                               'Top 10 Songs',
                               'Top 20 Artists in the United States by Total Streams',
                               'Top 10 Songs for Billie Eilish',
                               "Billie Eilish's Songs Distribution Across Years",
                               'Top 5 Songs Over Time',
                               'Top 5 Artists Over Time'
                              ])

# Visualization 1: Number of Songs by Region
if option == 'Number of Songs by Region':
    region_counts = df['region'].value_counts(ascending=False)
    plt.figure(figsize=(15, 8))
    sns.barplot(x=region_counts.index, y=region_counts.values)
    plt.xticks(rotation=90)
    plt.xlabel('Region')
    plt.ylabel('Number of Songs')
    plt.title('Number of Songs by Region')
    plt.tight_layout()
    st.pyplot(plt.gcf())

# Visualization 2: Distribution of Song Streams Across Regions
elif option == 'Distribution of Song Streams Across Regions':
    region_streams = df.groupby('region')['streams'].sum().sort_values(ascending=False).head(20)
    plt.figure(figsize=(12, 10))
    plt.pie(region_streams.values, labels=region_streams.index, autopct='%1.1f%%')
    plt.title('Distribution of Song Streams Across Regions')
    plt.axis('equal')
    plt.tight_layout()
    st.pyplot(plt.gcf())

# Visualization 3: Average Popularity of Songs Over Time
elif option == 'Average Popularity of Songs Over Time':
    time_popularity = df.groupby('date')['streams'].mean()
    time_popularity = time_popularity.sort_index()
    plt.figure(figsize=(15, 8))
    sns.lineplot(x=time_popularity.index, y=time_popularity.values)
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Average Popularity (Streams)')
    plt.title('Average Popularity of Songs Over Time')
    plt.tight_layout()
    st.pyplot(plt.gcf())

# Visualization 4: Top 10 Songs
elif option == 'Top 10 Songs':
    top_10_songs = df.groupby('title')['streams'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 10))
    sns.barplot(x=top_10_songs.index, y=top_10_songs.values)
    plt.xticks(rotation=90)
    plt.title("Top 10 Songs")
    plt.xlabel('Song Name')
    plt.ylabel('Streams')
    plt.tight_layout()
    st.pyplot(plt.gcf())

# Visualization 5: Top 20 Artists in the United States by Total Streams
elif option == 'Top 20 Artists in the United States by Total Streams':
    top_artists = df.groupby('artist')['streams'].sum().sort_values(ascending=False).head(20)
    plt.figure(figsize=(15, 15))
    plt.pie(top_artists.values, labels=top_artists.index, autopct='%1.1f%%')
    plt.title('Top 20 Artists by Total Streams')
    plt.axis('equal')
    plt.tight_layout()
    st.pyplot(plt.gcf())

# Visualization 6: Top 10 Songs for Billie Eilish
elif option == 'Top 10 Songs for Billie Eilish':
    billie_eilish_songs = df[df['artist'] == 'Billie Eilish'].groupby('title')['streams'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(15, 15))
    sns.barplot(x=billie_eilish_songs.index, y=billie_eilish_songs.values)
    plt.xticks(rotation=90)
    plt.xlabel('Song')
    plt.ylabel('Total Streams')
    plt.title('Top 10 Billie Eilish Songs by Total Streams')
    plt.tight_layout()
    st.pyplot(plt.gcf())

# Visualization 7: Billie Eilish's Songs Distribution Across Years
elif option == "Billie Eilish's Songs Distribution Across Years":
    billie_time_year = df[df['artist'] == 'Billie Eilish'].groupby('date')['streams'].sum().sort_values(ascending=False)
    plt.figure(figsize=(15, 15))
    sns.lineplot(x=billie_time_year.index, y=billie_time_year.values)
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Total Streams')
    plt.title('Distribution of Billie Eilish Songs Across Time (Year)')
    plt.tight_layout()
    st.pyplot(plt.gcf())

# Visualization 8: Top 5 Songs Over Time
elif option == 'Top 5 Songs Over Time':
    df['year'] = df['date'].dt.year
    df['year_title'] = df['year'].astype(str) + ' - ' + df['title']

    top_songs_by_year = (
        df.groupby('year')['title']
        .value_counts()
        .groupby(level=0, group_keys=False)
        .nlargest(5)
        .reset_index(name='count')
    )

    top_songs_by_year['year_title'] = top_songs_by_year['year'].astype(str) + ' - ' + top_songs_by_year['title']

    plt.figure(figsize=(15, 9))
    palette = sns.color_palette("tab10")  

    sns.barplot(
        x='year',
        y='count',
        hue='year_title',  
        data=top_songs_by_year,
        dodge=False,
        palette=palette
    )

    plt.xticks(rotation=90)
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.title('Top 5 Songs by Year')
    plt.legend(title='Year - Song', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt.gcf())

# Visualization 9: Top 5 Artists Over Time
elif option == 'Top 5 Artists Over Time':
    df['year'] = df['date'].dt.year

    top_artists_by_year = (
        df.groupby('year')['artist']
        .value_counts()
        .groupby(level=0, group_keys=False)
        .nlargest(5)
        .reset_index(name='count')
    )

    years = top_artists_by_year['year'].unique()
    n_years = len(years)
    fig, axes = plt.subplots(n_years, 1, figsize=(10, 6 * n_years), sharex=True)

    for i, year in enumerate(years):
        sns.barplot(
            x='count',
            y='artist',
            data=top_artists_by_year[top_artists_by_year['year'] == year],
            palette="Set2",
            ax=axes[i]
        )
        axes[i].set_title(f'Top 5 Artists of {year}')
        axes[i].set_xlabel('Count')
        axes[i].set_ylabel('Artist')

    plt.tight_layout()
    st.pyplot(fig)
