"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """

    speedMax = {range(0,200):34, range(200,400):32, range(400,600):30, range(600,1000):28, range(1000,1300):26}
    
    if control_dist_km > brevet_dist_km:
        control_dist_km = brevet_dist_km
    
    time = 0
    distance = control_dist_km
    dist_so_far = 0
   
    for speed_range, speed in speedMax.items():
        if control_dist_km in speed_range:
            remaining = distance - dist_so_far
            time += remaining / speed
            hours = int(time)
            minutes = round((time - hours) * 60)
            if minutes == 60:
                hours += 1
                minutes = 0
            open_time = arrow.get(brevet_start_time)
            open_timeF = open_time.shift(hours=hours, minutes=minutes)
            return open_timeF.isoformat()
        else:
            seg_dist = speed_range.stop - speed_range.start
            time += seg_dist / speed
            dist_so_far += seg_dist


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    speedMin = {range(0,200):15, range(200,400):15, range(400,600):15, range(600,1000):11.428, range(1000, 1300):13.333}
    close_limits = {200:13.5, 300:20, 400:27, 600:40, 1000:75}

    if control_dist_km == 0:
        close_time = arrow.get(brevet_start_time)
        close_timeF = close_time.shift(hours=1)
        return close_timeF.isoformat()
    
    if control_dist_km >= brevet_dist_km:
        limit = close_limits[brevet_dist_km]
        close_time = arrow.get(brevet_start_time)
        close_timeF = close_time.shift(hours=limit)
        return close_timeF.isoformat()
    
    if control_dist_km <= 60:
        time_60 = (control_dist_km / 20) + 1
        close_time = arrow.get(brevet_start_time)
        close_timeF = close_time.shift(hours=time_60)
        return close_timeF.isoformat()
    
    time = 0
    distance = control_dist_km
    dist_so_far = 0
    for speed_range, speed in speedMin.items():
        if control_dist_km in speed_range:
            remaining = distance - dist_so_far
            time += remaining / speed
            hours = int(time)
            minutes = round((time - hours) * 60)
            if minutes == 60:
                hours += 1
                minutes = 0
            close_time = arrow.get(brevet_start_time)
            close_timeF = close_time.shift(hours=hours, minutes=minutes)
            return close_timeF.isoformat()
        else:
            seg_dist = speed_range.stop - speed_range.start
            time += seg_dist / speed
            dist_so_far += seg_dist

    return arrow.now().isoformat()
