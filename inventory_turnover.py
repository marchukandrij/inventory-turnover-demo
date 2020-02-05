import datetime

data = []
min_date = None
max_date = None

# Loading
file_text = open('DemoData.txt', 'r', encoding='utf-8').read()
for line in file_text.splitlines():
    parts = line.split("\t")
    date_split = parts[0].split('.')
    date = datetime.date(int(date_split[2]), int(
        date_split[1]), int(date_split[0]))
    if min_date:
        min_date = min(min_date, date)
    else:
        min_date = date
    if max_date:
        max_date = max(max_date, date)
    else:
        max_date = date
    data_line = {
        'date': date,
        'nomenclature': parts[1],
        'group': parts[2],
        'summ_open': float(parts[7].replace(',', '.')),
        'summ_increase': float(parts[8].replace(',', '.')),
        'summ_decrease': float(parts[9].replace(',', '.')),
        'summ_close': float(parts[10].replace(',', '.')),
    }
    data.append(data_line)

# List of Nomenclature
nomenclature_list = set()
for data_line in data:
    nomenclature_list.add(data_line['nomenclature'])

result_set = []
# We extend data to dates without changes
day_delta = datetime.timedelta(days=1)
for nomenclature in nomenclature_list:
    start_date = min_date
    last_line = None
    for data_line in data:
        if data_line['nomenclature'] == nomenclature:
            last_line = data_line
            while last_line['date'] > start_date:
                exp_line = {
                    'date': start_date,
                    'nomenclature': last_line['nomenclature'],
                    'group': last_line['group'],
                    'summ_open': last_line['summ_open'],
                    'summ_increase': 0.0,
                    'summ_decrease': 0.0,
                    'summ_close': last_line['summ_open']
                }
                result_set.append(exp_line)
                start_date += day_delta
            result_set.append(last_line)
            start_date += day_delta
    while start_date <= max_date:
        exp_line = {
            'date': start_date,
            'nomenclature': last_line['nomenclature'],
            'group': last_line['group'],
            'summ_open': last_line['summ_close'],
            'summ_increase': 0.0,
            'summ_decrease': 0.0,
            'summ_close': last_line['summ_close']
        }
        result_set.append(exp_line)
        start_date += day_delta

# Write result
file_result = open('DemoData_expanded.txt', 'w', encoding='utf-8')
for line in result_set:
    date = line['date']
    line_str = str(date.day) + '.' + str(date.month) + \
        '.'+str(date.year) + "\t"
    line_str += line['nomenclature'] + "\t" + line['group'] + "\t"
    line_str += str(line['summ_decrease']).replace('.',',') + "\t" + \
        str(line['summ_close']).replace('.',',') + "\n"
    file_result.write(line_str)
file_result.close()
