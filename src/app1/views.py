from django.shortcuts import render
from django.db import connection
from datetime import datetime, time

# Create your views here.

def index(request):
    # Get selected date from request or use current date
    selected_date_str = request.GET.get('selected_date', None)
    selected_unit = request.GET.get('unit_name', None)

    try:
        if selected_date_str:
            # Parse the date from the format YYYY-MM-DD
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        else:
            # Default to current date
            selected_date = datetime.now().date()
    except ValueError:
        # If date format is invalid, default to current date
        selected_date = datetime.now().date()

    # Get all available unit names from the database
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT UnitName
            FROM ProductRecordLog
            WHERE UnitName IS NOT NULL
            ORDER BY UnitName
        """)
        available_units = [row[0] for row in cursor.fetchall()]

    # If no unit is selected but units are available, default to the first one
    if not selected_unit and available_units:
        selected_unit = available_units[0]

    # Initialize hours list and total counts
    hours_data = []
    total_pass = 0
    total_fail = 0
    total_quantity = 0

    # Loop through each hour from 8:00 to 16:00 (8 AM to 4 PM)
    for hour in range(8, 17):
        # Create datetime objects for start and end of the hour
        start_time = datetime.combine(selected_date, time(hour, 0, 0))
        end_time = datetime.combine(selected_date, time(hour, 59, 59)) if hour < 16 else datetime.combine(selected_date, time(16, 0, 0))

        # Format for display with intervals
        next_hour = hour + 1 if hour < 16 else hour

        # Format hour values with leading zeros for consistency
        start_hour_fmt = f"{hour:02d}:00"
        end_hour_fmt = f"{next_hour:02d}:00"

        # Create time interval display
        time_interval = f"{start_hour_fmt}-{end_hour_fmt}"

        # Using raw SQL to query pass data (TestSonucu = 1) for this hour
        with connection.cursor() as cursor:
            # Build query with optional unit filter
            unit_filter = " AND UnitName = %s" if selected_unit else ""
            params = [start_time, end_time]
            if selected_unit:
                params.append(selected_unit)

            # Query for pass data
            cursor.execute(f"""
                SELECT COUNT(*)
                FROM ProductRecordLog
                WHERE KayitTarihi >= %s AND KayitTarihi < %s AND TestSonucu = 1{unit_filter}
            """, params)
            pass_quantity = cursor.fetchone()[0]

            # Query for fail data
            cursor.execute(f"""
                SELECT COUNT(*)
                FROM ProductRecordLog
                WHERE KayitTarihi >= %s AND KayitTarihi < %s AND TestSonucu = 0{unit_filter}
            """, params)
            fail_quantity = cursor.fetchone()[0]

            # Calculate total for this hour
            hour_quantity = pass_quantity + fail_quantity

        # Add to totals
        total_pass += pass_quantity
        total_fail += fail_quantity
        total_quantity += hour_quantity

        # Add to hours data
        hours_data.append({
            'time_label': f"{hour}:00",
            'display_time': time_interval,
            'pass_quantity': pass_quantity,
            'fail_quantity': fail_quantity,
            'total_quantity': hour_quantity
        })

    # Format the selected date for display
    formatted_date = selected_date.strftime('%Y-%m-%d')

    context = {
        'title': "Günlük Üretim Raporu",
        'hours_data': hours_data,
        'total_pass': total_pass,
        'total_fail': total_fail,
        'total_quantity': total_quantity,
        'selected_date': formatted_date,
        'current_time': datetime.now().strftime('%H:%M:%S'),
        'available_units': available_units,
        'selected_unit': selected_unit
    }

    return render(request, 'app1/index.html', context)