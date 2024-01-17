from database import user_usage
from www import bytes_to_gb

usage = user_usage(843774957)
day_chart = []
current_delta = '00'
start_usage = 0
end_usage = 0
print(usage)

# Создаем словарь для хранения данных по каждому часу
hourly_data = {}

for item in usage:
    if item['day_marker'] != 'current_day':
        continue

    data_usage = float(bytes_to_gb(int(item['used_bytes'])))
    point_time = item['add_time'].strftime('%H')

    if point_time not in hourly_data:
        hourly_data[point_time] = [data_usage]
        print(point_time, data_usage, 'new')
    else:
        hourly_data[point_time].append(data_usage)
        print(point_time, data_usage, '*')
print(hourly_data)
new_data = []
for i in hourly_data.keys():
    new_data.append(round(hourly_data[i][-1] - hourly_data[i][0], 2))
print(new_data)
print(len(new_data))
