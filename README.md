# Stock Trading Simulator

A stock trading simulator built using the Alpaca API to simulate stock price movements and paper trade against an AI algorithm. The project allows users to simulate stock trading using historical market data and compare their performance with an AI-driven trading strategy.

## Features

- **Real-time Stock Price Visualization:** Market data is collected via the Alpaca API and plotted in real-time.
- **Paper Trading Simulation:** Simulate buying and selling stocks with historical market data for learning purposes.
- **AI Trading Algorithm:** The AI uses a basic strategy that learns from the market data and adjusts its investment strategy dynamically.
- **Leaderboard:** Tracks user performance and compares it against past performances using a simple hashing-based ranking system.
- **Multi-threading Support:** Enables smooth UI operation while handling stock price updates and plotting graphs.

## Technologies Used

- **Python**: Main programming language.
- **Alpaca API**: Provides real-time and historical market data.
- **Tkinter**: Python GUI library used for creating the application interface.
- **Matplotlib**: Used for plotting stock price graphs in real-time.
- **Pickle**: Used for saving and loading leaderboard data.
- **Threading**: Ensures smooth execution of UI and background tasks like data fetching and plotting.

## Installation

1. **Install dependencies**:

```
pip install alpaca-trade-api
pip install matplotlib
```

2. **Set up your Alpaca API**:
- Sign up for an [Alpaca](https://alpaca.markets/) account at Alpaca to get your API keys.
- Replace the apikey and seckey variables in the script with your own Alpaca API key and secret.

## Usage

### Run the program:

```
python3 main.py
```

The application will open a GUI window where you can:

Enter your player name and the stock symbol.
Press Start to begin the real-time stock simulation.
Use the Buy and Sell buttons to paper trade the stock during the simulation.
Track your performance against the AI in the right-hand panel.
The simulation will continue to run until the end date is reached. At the end of the game, a leaderboard will be displayed, showing the performance of all previous players.

### Example Stock Symbols:

TSLA (Tesla)
AAPL (Apple)
GM (General Motors)
NVDA (NVIDIA)
