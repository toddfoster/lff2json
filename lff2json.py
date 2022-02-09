from calendar import month_name

DEBUG_PAGE = 1318

page = 0
PP_INDEX = (14, 25)
PP_ENTRIES = (31, 578)
SOJOURNER_BIO = (317, 319)
EXTRA_XMAS_PP = (567, 568)

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

dates_with_problem_titles=["0126", "0525", "0909", "0927"]
def find_feast_by_date_and_title(feasts, mm, dd, title):
    for f in feasts:
        if f["mm"] == mm and f["dd"] == dd:
            if not title:
                return f
            if mm + dd in dates_with_problem_titles:
                return f
            if page >= DEBUG_PAGE:
                print (f"--find_feast_by_date_and_title p.{page} - {mm} {dd} {title}: {f['title'][0:6].upper()}")
            if title[0:4].upper() == f["title"][0:4].upper():
                return f


feasts = []
with open("src/lff2018.txt", "r", encoding="utf-8") as f:
    current_month = 0
    previous_record = {}
    mmdd_progress = 0
    bio = ""
    cumulative_line = ""
    recto_page_state = 0
    long_bio = False
    for line in f:
        if "\f" in line:
            page += 1
        l = line.strip().replace("\x07", "")

        # skip to beginning of index
        if page < PP_INDEX[0]:
            continue

        # found index
        if PP_INDEX[0] <= page <= PP_INDEX[1]:
            if len(l) < 3:
                continue

            if l.find(" or") > 0:
                print (f"Found an 'or' in index {current_month}/{l}")
                # TODO make sure these five are all parsed out correctly

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
                continue

            # parse line in month -- sometimes lines have a linebreak!
            splits = l.split(" ", maxsplit=1)
            if len(splits) < 2:
                continue
            day = splits[0]
            feast = splits[1].strip()
            if day.isnumeric() and int(day) < 32:
                current_day = f"{int(day):02}"
                previous_record = {
                    "mm": current_month,
                    "dd": current_day,
                    "title": feast
                    }
                feasts.append(previous_record)
                # There are five dates with two options for the feast;
                # in each case, the second option is listed on a second line
                # in the index. So set up an additional record for it.
                if feast.find(" or") > 0:
                    previous_record["title"] = feast.split(" or")[0]
                    feasts.append(previous_record)
                    previous_record = {
                        "mm": current_month,
                        "dd": current_day,
                        "title": ""
                        }
                    feasts.append(previous_record)
            else:
                previous_record["title"] = (previous_record["title"] + " " + l).strip()
            continue

        ############
        # Past index
        ############

        if EXTRA_XMAS_PP[0] <= page <= EXTRA_XMAS_PP[1]:
            # TODO: how to include extra collects/lessons for Xmas?
            continue

        if PP_ENTRIES[0] <= page <= PP_ENTRIES[1]:
            # verso pages have bio's; recto pages have title, collects, lessons, preface
            # easiest, though, to compare against beginning of this section;
            # so even pages (0, 2, etc.) will be verso and odd pages will be recto
        
            # Stanton, et al, bio runs three pages: handle specially
            # TODO: figure out spacing / line-breaks in the Sojourner bio
            if SOJOURNER_BIO[0] <= page <= SOJOURNER_BIO[1]:
                if len(l) > 2 and l[0] != '3' and l[0:4] != "July":
                    bio = (bio + " " + l).strip()
                continue
            
            if (page - PP_ENTRIES[0]) % 2 == 0: # verso page with bio
                previous_record = {}
                splits = l.split(" ")
                month = splits[0].upper()
                if len(splits) == 2 and month in months: # found date at bottom of page
                    mm = months.index(month) + 1
                    dd = int (splits[1])
                    assert 0 < dd < 32, f"Bad day value {dd}: {l}"
                    mmdd = mm * 100 + dd
                    assert mmdd >= mmdd_progress, f"Source dates out of order: {l}"
                    mmdd_progress = mmdd
                    recto_page_state = 0
                elif len(l) > 3:
                    bio = (bio + " " + l).strip()
            # TODO Paragraph breaks are difficult: look for period finising line before column 75?
            else: #recto page with title, other data
                if len(l) < 5:
                    continue
                if recto_page_state == 0: # Looking for title
                    previous_record = find_feast_by_date_and_title(feasts, f"{mm:02}", f"{dd:02}", l)
                    assert previous_record, f"Couldn't locate record for {mm}/{dd} {l}"
                    previous_record['bio'] = bio
                    bio = ""
                    recto_page_state += 1
                


            # TODO: Check that the dates & titles match data from the index. dates_with_problem_titles
            # 2. Get rite1_collect
            # 3. Get rite2_collect
            # 4. Get first_lesson (note instructions after verse number)
            # 5. Get psalm (assert)
            # 6. Get second_lesson or +1 to gospel
            # 7. Get gospel (assert)
            # 8. Get preface, drop record, state to 1

            


print("{} pages processed".format(page))
print(find_feast_by_date_and_title(feasts, "04", "03", ""))
#print(find_feast_by_date_and_title(feasts, "04", "14"))
#print(find_feast_by_date_and_title(feasts, "05", "17"))
#print(find_feast_by_date_and_title(feasts, "05", "31"))
#print(find_feast_by_date_and_title(feasts, "06", "15"))
#print(find_feast_by_date_and_title(feasts, "06", "29"))
#print(find_feast_by_date_and_title(feasts, "12", "17"))
print(find_feast_by_date_and_title(feasts, "12", "31", ""))
print("------------")
#for f in feasts:
#    print(f"{f['mm']}/{f['dd']}: {f['title']}")
