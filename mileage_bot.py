import logging
import datetime
import os
from dateutil.relativedelta import relativedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# --- LEASE DETAILS ---
# Set your specific lease information here
LEASE_START_DATE = datetime.date(2025, 4, 4)
LEASE_MONTHS = 36
TOTAL_MILES = 30300
# ---------------------

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message."""
    await update.message.reply_text(
        "Hi! I'm your lease mileage calculator. "
        "Send /mileage to see how many miles you should have driven by today."
    )


async def mileage(update: Update, context: CallbackContext) -> None:
    """Calculates and returns the target mileage for the current date."""
    today = datetime.date.today()

    # Check if the lease has started yet
    if today < LEASE_START_DATE:
        await update.message.reply_text(
            f"Your lease hasn't started yet. It begins on {LEASE_START_DATE.strftime('%B %d, %Y')}."
        )
        return

    # --- Calculation Logic ---
    # 1. Calculate the lease end date
    lease_end_date = LEASE_START_DATE + relativedelta(months=LEASE_MONTHS)
    
    # 2. Calculate the total number of days in the lease period
    total_lease_days = (lease_end_date - LEASE_START_DATE).days
    
    # 3. Calculate the daily mileage allowance
    daily_mileage_allowance = TOTAL_MILES / total_lease_days
    
    # 4. Calculate how many days have passed since the lease started
    days_passed = (today - LEASE_START_DATE).days
    
    # 5. Calculate the target mileage for today
    target_mileage_today = daily_mileage_allowance * days_passed

    # --- Create the Reply Message ---
    reply_text = (
        f"🗓️ **Lease Progress**\n"
        f"Days into lease: {days_passed} of {total_lease_days}\n\n"
        f"📈 **Mileage Details**\n"
        f"Daily allowance: {daily_mileage_allowance:.2f} miles/day\n\n"
        f"🎯 **Your target mileage for today is: {target_mileage_today:,.0f} miles**"
    )

    await update.message.reply_text(reply_text, parse_mode='Markdown')


def main() -> None:
    """Sets up and runs the bot."""
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("No TELEGRAM_TOKEN found in environment variables")

    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("mileage", mileage))

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    main()
