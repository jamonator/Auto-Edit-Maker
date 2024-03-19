# Converts time from (0:00) formate into seconds

def parse_timestamp(timestamp_str):
    """Parse timestamp string in format '9:23' to seconds."""
    if timestamp_str is None:
        return 0  # Return 0 seconds if timestamp_str is None
    hours, minutes = map(int, timestamp_str.split(':'))
    return hours * 60 + minutes