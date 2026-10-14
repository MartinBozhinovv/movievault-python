# 🎬 MovieVault

MovieVault is a Python desktop application for managing a personal movie collection. It allows users to search for movies, save their favorites, track watched movies, and receive movie recommendations.

## Features

- Search for movies using the OMDb API
- Add movies to a personal collection
- View movie information, ratings, and posters
- Rate movies
- Mark movies as watched or unwatched
- Get movie recommendations
- Remove movies from the collection
- Store movie data locally using SQLite

## Technologies Used

- **Python** – Application logic
- **wxPython** – Desktop graphical user interface
- **SQLite** – Local database
- **OMDb API** – Movie information and posters
- **Pillow** – Image processing
- **python-dotenv** – Environment variable management
- **certifi** – SSL certificate verification

## Installation

1. Clone the repository:

   `git clone https://github.com/MartinBozhinovv/movievault-python.git`

2. Navigate to the project directory:

   `cd movievault-python`

3. Install the dependencies:

   `pip install -r requirements.txt`

4. Create a `.env` file in the project directory and add your OMDb API key:

   `OMDB_API_KEY=your_api_key_here`

5. Run the application:

   `python main.py`

You can obtain an API key from [OMDb API](https://www.omdbapi.com/apikey.aspx).

## Database

MovieVault uses SQLite to store the user's movie collection locally.

The database and required tables are created automatically when the application starts for the first time.

## Project Purpose

This project was developed to practice Python programming, object-oriented programming, database operations, API integration, and desktop application development.

## Author

**Martin Bozhinov**

[GitHub](https://github.com/MartinBozhinovv) | [LinkedIn](https://www.linkedin.com/in/martin-bozhinov1)