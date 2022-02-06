from calendar import month_name

page = 0
PP_INDEX = (14, 25)
PP_ENTRIES = (31, 578)

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
        l = line.strip().replace("\x07", "")

        # skip to beginning of index
        if page < PP_INDEX[0]:
            continue

        # found index
        if PP_INDEX[0] <= page and page <= PP_INDEX[1]:
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
                #print(f" found {current_month}/{mayjune_day}: {l}")
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
        if PP_ENTRIES[0] <= page and page <= PP_ENTRIES[1]:
            # Odd pages have bio's; even pages have title, collects, lessons, preface
            # Paragraph breaks are difficult: look for period finising line before column 75?
            # Dates are at bottom of page. Check that they are in order.
            # Check that the dates & titles match data from the index.
            # States:
            # A. ODD PAGES: Gather up description, combining lines
            #    Ignore page number (2-3 digits alone on line)
            #    Find date, check in order, get record, add description
            # B. EVEN PAGES, record on hand, increment state after successful line
            # 1. get title, check against record
            # 2. Get rite1_collect
            # 3. Get rite2_collect
            # 4. Get first_lesson (note instructions after verse number)
            # 5. Get psalm
            # 6. Get second_lesson or +1 to gospel
            # 7. Get gospel
            # 8. Get preface, drop record, state to 1
            if page == PP_ENTRIES[0]:
                print(l)

        
print("{} pages processed".format(page))
print(find_feast_by_date(feasts, "04", "14"))
print(find_feast_by_date(feasts, "05", "17"))
print(find_feast_by_date(feasts, "05", "31"))
print(find_feast_by_date(feasts, "06", "15"))
print(find_feast_by_date(feasts, "06", "29"))
print("------------")
#for f in feasts:
#    print(f"{f['mm']}/{f['dd']}: {f['title']}")
