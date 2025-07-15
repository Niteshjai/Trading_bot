import schedule
import time
from Trading_bot.strategy import run_strategy     
from Trading_bot.log_data import trade_log            
import logging
import json
from datetime import datetime

# ------------------ Logging Setup ------------------ #
logging.basicConfig(
    filename='simulation.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

print("📅 Bot is running. Waiting for market hours...")

# ------------------ Market Hours ------------------ #
MARKET_OPEN = (10, 15)    # 10:15 AM
MARKET_CLOSE = (15, 30)   # 3:30 PM
CHECK_INTERVAL = 60       # seconds between job checks

def within_market_hours():
    """Check if current time is during market hours (Mon–Fri, 10:15–15:30)."""
    now = datetime.now()

    # Weekend
    if now.weekday() > 4:
        return False

    # Convert times to total minutes since midnight
    current_minutes = now.hour * 60 + now.minute
    start_minutes = MARKET_OPEN[0] * 60 + MARKET_OPEN[1]
    end_minutes = MARKET_CLOSE[0] * 60 + MARKET_CLOSE[1]

    return start_minutes <= current_minutes <= end_minutes

def job():
    """Run strategy if within market hours."""
    if within_market_hours():
        logging.info("Running strategy...")
        try:
            run_strategy()
        except Exception as e:
            logging.error(f"Error in run_strategy: {e}")
    else:
        logging.debug("Outside market hours. Skipping strategy execution.")

# Schedule job every CHECK_INTERVAL seconds
schedule.every(CHECK_INTERVAL).seconds.do(job)

# ------------------ Main Execution Loop ------------------ #
if __name__ == "__main__":
    logging.info("Starting trading simulation...")
    try:
        while True:
            schedule.run_pending()

            # Save the trade log after each execution cycle
            with open("paper_trades_log.json", "w") as f:
                json.dump(trade_log, f, indent=2)

            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        logging.info("Simulation stopped by user.")
        print("🛑 Simulation stopped by user.")
