import schedule
import time
from strategy import run_strategy
from log_data import trade_log
import logging
import json
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='simulation.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

print("📅 Bot is running. Waiting for market hours...")

# Time range settings
MARKET_OPEN = (10, 15)   # 10:15 AM
MARKET_CLOSE = (15, 30) # 3:30 PM
CHECK_INTERVAL = 60     # check every 60 seconds

def within_market_hours():
    now = datetime.now()
    # Only Monday (0) to Friday (4)
    if now.weekday() > 4:
        return False
    # Check if current time is between 9:15 and 15:30
    current_time = now.hour * 60 + now.minute
    start_minutes = MARKET_OPEN[0] * 60 + MARKET_OPEN[1]
    end_minutes = MARKET_CLOSE[0] * 60 + MARKET_CLOSE[1]
    return start_minutes <= current_time <= end_minutes

def job():
    if within_market_hours():
        logging.info("Running strategy...")
        try:
            run_strategy()
        except Exception as e:
            logging.error(f"Error in run_strategy: {e}")
    else:
        logging.debug("Outside market hours. Skipping strategy execution.")

schedule.every(CHECK_INTERVAL).seconds.do(job)

if __name__ == "__main__":
    logging.info("Starting trading simulation...")
    try:
        while True:
            schedule.run_pending()

            # Save trade log after each run (you can optimize this further)
            with open("paper_trades_log.json", "w") as f:
                json.dump(trade_log, f, indent=2)

            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        logging.info("Simulation stopped by user.")
        print("Simulation stopped by user.")
