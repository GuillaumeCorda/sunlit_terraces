# Sunlit Terraces - FastAPI App

## Overview
Sunlit Terraces is a FastAPI-based application that helps users find bars, cafés, and restaurants in London with sunlit terraces in real-time.

## Features
- Retrieves venue data using Google Places API.
- Determines real-time sunlight exposure based on solar position and terrace orientation.
- Interactive frontend (React) for a seamless user experience.
- Dockerized for easy deployment.

## Installation
### Prerequisites
- Python 3.10+
- Poetry for dependency management
- Docker (optional for containerized deployment)
- Node.js & npm for frontend

### Backend Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/sunlit-terraces.git
   cd sunlit-terraces
   ```
2. Install dependencies:
   ```sh
   poetry install
   ```
3. Create a `.env` file and add your API keys:
   ```sh
   GOOGLE_PLACES_API_KEY=your_google_api_key
   SOLAR_API_KEY=your_solar_api_key
   ```
4. Run the application:
   ```sh
   poetry run uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Navigate to the `frontend/` directory:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the frontend:
   ```sh
   npm start
   ```
4. Open `http://localhost:3000` to access the app.

## API Endpoints
- `GET /venues` - Fetch nearby venues with filters.
- `GET /sunlight` - Determine if a terrace is sunlit.

## Deployment
To run the application using Docker:
```sh
docker build -t sunlit-terraces .
docker run -p 8000:8000 sunlit-terraces
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first.

## License
MIT License