import calendar
from datetime import datetime, timedelta
from env_loader import START_DATE, START_WORKER

# Worker rotation config
workers = ["Muhammadali", "Bunyod"]
rotation_days = 3  # Default shift duration

# State tracking
start_date = datetime.strptime(START_DATE, "%Y-%m-%d")
current_worker = START_WORKER
schedule = {}

def generate_schedule(start_date, start_worker):
    """Generates the work schedule from the given start date."""
    global schedule, current_worker
    year, month = start_date.year, start_date.month
    _, total_days = calendar.monthrange(year, month)
    
    schedule = {}
    current_worker = start_worker

    for day in range(1, total_days + 1):
        date = datetime(year, month, day)
        
        # Assign the worker even if it's before the start date
        schedule[date.strftime("%Y-%m-%d")] = current_worker
        
        # Rotate worker after shift duration
        if (date - start_date).days % rotation_days == rotation_days - 1:
            current_worker = workers[1] if current_worker == workers[0] else workers[0]

def create_schedule_message():
    """Creates a formatted schedule message."""
    message = f"📅 Work Schedule for {start_date.strftime('%B %Y')}\n\n"
    for date, worker in schedule.items():
        message += f"{date}: {worker}\n"
    return message

def swap_shift(extra_days):
    """Swaps the shift dynamically when both workers are working."""
    global start_date
    start_date = start_date + timedelta(days=extra_days)
    generate_schedule(start_date, current_worker)

# Generate initial schedule
generate_schedule(start_date, current_worker)
