import openpyxl
import json
from datetime import datetime

def parse_focus(focus_str):
    if focus_str and isinstance(focus_str, str):
        match = focus_str.split('-')[0].strip()
        try:
            return int(match)
        except:
            return 3
    return 3

wb = openpyxl.load_workbook('时间统计.xlsx')
sheet = wb.active

print(f"Excel headers: {[cell.value for cell in sheet[1]]}")

topics_set = set()
activities_dict = {}
contents_dict = {}
details_dict = {}
records = []

for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
    if not row[0]:
        continue

    excel_date = row[0]
    start_time = row[1]
    end_time = row[2]
    focus_str = row[3]
    topic = row[4]
    activity = row[5]
    content = row[6]
    progress = row[7]

    if isinstance(excel_date, datetime):
        date_str = excel_date.strftime('%Y-%m-%d')
    else:
        date_str = str(excel_date) if excel_date else ''

    if hasattr(start_time, 'strftime'):
        start_time_str = start_time.strftime('%H:%M')
    else:
        start_time_str = str(start_time) if start_time else '00:00'

    if hasattr(end_time, 'strftime'):
        end_time_str = end_time.strftime('%H:%M')
    else:
        end_time_str = str(end_time) if end_time else '00:00'

    focus = parse_focus(focus_str)

    if topic and topic not in topics_set:
        topics_set.add(topic)
        activities_dict[topic] = []

    if topic and activity and activity not in activities_dict.get(topic, []):
        if topic not in activities_dict:
            activities_dict[topic] = []
        activities_dict[topic].append(activity)

    content_key = f"{topic}|{activity}" if topic and activity else None
    if content_key and content:
        if content_key not in contents_dict:
            contents_dict[content_key] = []
        if content not in contents_dict[content_key]:
            contents_dict[content_key].append(content)

    detail_key = f"{topic}|{activity}|{content}" if topic and activity and content else None
    if detail_key and progress:
        if detail_key not in details_dict:
            details_dict[detail_key] = []
        if progress not in details_dict[detail_key]:
            details_dict[detail_key].append(progress)

    record = {
        'id': f"{datetime.now().strftime('%Y%m%d%H%M%S')}{row_idx:04d}",
        'date': date_str,
        'startTime': start_time_str,
        'endTime': end_time_str,
        'focus': focus,
        'activity': topic or '',
        'detail1': activity or '',
        'detail2': content or '',
        'detail3': progress or '',
        'note': '',
        'createdAt': datetime.now().isoformat()
    }
    records.append(record)
    print(f"Row {row_idx}: [{topic}] {activity} - {content} ({progress})")

output = {
    'records': records,
    'categories': {
        'topics': sorted(list(topics_set)),
        'activities': activities_dict,
        'contents': contents_dict,
        'details': details_dict
    }
}

with open('time_tracker_data.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully imported:")
print(f"  - {len(records)} records")
print(f"  - {len(topics_set)} topics")
print(f"  - {sum(len(v) for v in activities_dict.values())} activities")
print(f"  - {sum(len(v) for v in contents_dict.values())} contents")
print(f"  - {sum(len(v) for v in details_dict.values())} details")