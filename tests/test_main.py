import schedule
from deepseek_daily_newsletter import main

def test_job_scheduled():
    schedule.clear()
    main.setup_scheduler()
    jobs = schedule.get_jobs()
    # Check for a job scheduled every Monday at 08:00
    found = False
    import datetime
    for job in jobs:
        if job.unit == 'weeks' and job.at_time == datetime.time(8, 0) and job.start_day == 'monday':
            found = True
    assert found, "No job scheduled for Monday at 08:00"
