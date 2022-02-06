from calendar import month_name

page = 0
index_start = 14
index_end = 25
characters = 0
mayjune_day = 0
BLANK_DAYS_IN_MAY = [6, 7, 10, 12, 14, 16, 18, 23, 27, 29, 30]
BLANK_DAYS_IN_JUNE = [6, 7, 13, 20, 21, 23, 25, 27, 30]
months = []
for m in month_name[1:]:
    months += [m.upper()]


def print_hex_chars(line_in):
    """Print hex characters so I can find & remove them."""
    for c in line_in:
        print(f"{c}: {ord(c):02x}")


def find_feast_by_date(feasts, mm, dd):
    for f in feasts:
        if f["mm"] == mm and f["dd"] == dd:
            return f


feasts = []
with open("src/lff2018.txt", "r", encoding="utf-8") as f:
    current_month = 0
    previous_record = {}
    for line in f:
        if "\f" in line:
            page += 1

        # skip to beginning of index
        if page < index_start:
            continue

        # found index
        if index_start <= page and page <= index_end:
            l = line.strip().replace("\x07", "")

            if len(l) < 3:
                continue

            # Check for new month name
            if l in months:
                current_month = f"{months.index(l)+1:02}"
                # print(f"current_month={current_month}")
                mayjune_day = 0
                continue

            # May and June are messed up & need special treatment
            if current_month in ('05', '06'):
                mayjune_day += 1
                while current_month == "05" and mayjune_day in BLANK_DAYS_IN_MAY:
                    mayjune_day += 1
                while current_month == "06" and mayjune_day in BLANK_DAYS_IN_JUNE:
                    mayjune_day += 1
                if mayjune_day > 31:
                    continue
                feasts.append({
                    "mm": current_month,
                    "dd": f"{mayjune_day:02}",
                    "title": l,
                })
                print(f" found {current_month}/{mayjune_day}: {l}")
                continue

            # parse line in month -- sometimes lines have a linebreak!
            splits = l.split(" ", maxsplit=1)
            if len(splits) < 2:
                continue
            day = splits[0]
            feast = splits[1].strip()
            if day.isnumeric() and int(day) < 32:
                current_day = f"{int(day):02}"
                # print(f"{current_month}/{day}: {feast}")
                previous_record = {
                    "mm": current_month,
                    "dd": current_day,
                    "title": feast,
                }
                feasts.append(previous_record)
            else:
                previous_record["title"] += " " + l
            continue

        # Past index
        print("past index")
        break
print("{} pages processed".format(page))
print(find_feast_by_date(feasts, "04", "14"))
print(find_feast_by_date(feasts, "05", "17"))
print(find_feast_by_date(feasts, "05", "31"))
print(find_feast_by_date(feasts, "06", "15"))
print(find_feast_by_date(feasts, "06", "29"))
print("------------")
for f in feasts:
    print(f"{f['mm']}/{f['dd']}: {f['title']}")
