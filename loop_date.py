import datetime

def loop_date(start_dt, end_dt):
    
    print('start_dt={} | type={}'.format(start_dt, type(start_dt)))
    print('end_dt={} | type={}'.format(end_dt, type(end_dt)))
    
    dict_out = {}
    dict_out['str'] = []
    dict_out['int'] = []
    dict_out['dt'] = []
    
    if type(start_dt)==type(end_dt) and type(start_dt)==int:
        start_yr = start_dt // 10000
        start_mth = start_dt // 100 % 100
        start_day = start_dt % 100
        end_yr = end_dt // 10000
        end_mth = end_dt // 100 % 100
        end_day = end_dt % 100
    
    elif type(start_dt)==type(end_dt) and type(start_dt)==str:
        start_yr = start_dt[:4]
        start_mth = start_dt[4:6]
        start_day  = start_dt[-2:]
        end_yr = end_dt[:4]
        end_mth = end_dt[4:6]
        end_day  = end_dt[-2:]
    
    else:
        return 'ERROR'
    
    print(start_yr, start_mth, start_day)
    print(end_yr, end_mth, end_day)
    
    dt_start = datetime.date(int(start_yr), int(start_mth), int(start_day))
    dt_end = datetime.date(int(end_yr), int(end_mth), int(end_day))
    
    print(dt_start, dt_end)
    
    dt_diff = (dt_end - dt_start).days + 1
    
    print(dt_diff)
    
    for i in range(dt_diff):
        dt = dt_start + datetime.timedelta(days=i)
        dict_out['dt'].append(dt)
        dict_out['str'].append(dt.strftime('%Y%m%d'))
        dict_out['int'].append(int(dt.strftime('%Y%m%d')))
    
    return dict_out
