from calendar import month_name

page = 0
index_start = 14
index_end = 25
characters = 0

months = []
for m in month_name[1:]:
    months += [m.upper()]


def print_hex_chars(line_in):
    """Print hex characters so I can find & remove them."""
    for c in line_in:
        print(f"{c}: {ord(c):02x}")


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

            # Check for new month name
            if l in months:
                current_month = months.index(l) + 1
                print(f"current_month={current_month}")
                continue
            if current_month < 0:
                continue  # just in case

            # parse line in month -- sometimes lines have a linebreak!
            splits = l.split(" ", maxsplit=1)
            if len(splits) < 2:
                continue
            day = splits[0]
            feast = splits[1].strip()
            if day.isnumeric() and int(day) < 32:
                print(f"{int(current_month):02}/{int(day):02}: {feast}")
            continue

        # Past index
        print("past index")
        break
print("{} pages processed".format(page))
