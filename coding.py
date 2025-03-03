from datetime import datetime, timedelta

for i in range(24, 49, 6):
    print(i)

start_date = datetime(2025, 3, 1)
sampled_middle_weeks = [start_date + timedelta(weeks=w) for w in range(24, 49, 6)]

for i in sampled_middle_weeks:
    print(i)
