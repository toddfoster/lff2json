from calendar import month_name
import re

# TODO: Capture major feasts flag (all caps in index?)



page = 0
mismatches = 0
PP_INDEX = (14, 25)
PP_ENTRIES = (31, 578)
SOJOURNER_BIO = (317, 319)
EXTRA_XMAS_PP = (567, 568)

COLLECT_RE = re.compile('^I[^rng]')

characters = 0
mayjune_day = 0
BLANK_DAYS_IN_MAY = (6, 7, 10, 12, 14, 16, 18, 23, 27, 29, 30)
BLANK_DAYS_IN_JUNE = (6, 7, 13, 20, 21, 23, 25, 27, 30)
months = []
for m in month_name[1:]:
    months += [m.upper()]

DEBUG = 1
DEBUG_LEVELS = ("WARNING", "INFO", "DEBUG", "DEBUGDEBUG")
def debug(message):
    """Print debug statements depending on current debug level"""
    message_level = message.split()[0].replace(":","")
    level = DEBUG_LEVELS.index(message_level)
    if level <= DEBUG:
        print(message)


def print_hex_chars(line_in):
    """Print hex characters so I can find & remove them."""
    for c in line_in:
        print(f"{c}: {ord(c):02x}")

DATES_WITH_PROBLEM_TITLES=("0126", "0525", "0909", "0927")
def find_feast_by_date_and_title(feasts, mm, dd, title):
    for f in feasts:
        if f["mm"] == mm and f["dd"] == dd:
            if not title:
                return f
            if mm + dd in DATES_WITH_PROBLEM_TITLES:
                return f
            debug (f"DEBUG: find_feast_by_date_and_title p.{page} - {mm} {dd} {title[0:4].upper()}")
            debug (f"DEBUG: ----------------------------------------- {f['title'][0:4].upper()}")
            if title[0:4].upper() == f['title'][0:4].upper():
                return f
    debug (f"WARNING: find_feast_by_date_and_title failed on {mm}/{dd}: {title}")


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
            debug (f"DEBUGDEBUG: Page #{page}")
        l = line.strip().replace("\x07", "")

        # skip to beginning of index
        if page < PP_INDEX[0]:
            continue

        debug(f"DEBUGDEBUG: line = {l}")
        
        # found index
        if PP_INDEX[0] <= page <= PP_INDEX[1]:
            if len(l) < 3:
                continue

            if l.find(" or") > 0:
                debug (f"INFO: Found an 'or' in index {current_month}/{l}")
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
                    previous_record["title"] = feast.split(", or")[0]
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
            # TODO Christmas has the extra pages
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
                mmdd = mm * 100 + dd
                KEEP_LOOKING_LIST=(315, 416, 1016)
                ####################################################
                if recto_page_state == 0: # Looking for title
                    NO_COMMA_AFTER = (" and", " of", " Lord",
                                      " Benedicta", " Blessed",
                                      "Saint Philip", " Jesus")
                    if (len(l) > 0 or mmdd in KEEP_LOOKING_LIST) and not COLLECT_RE.match(l):
                        cumulative_line += ", " + l
                        continue
                    else:
                        recto_page_state += 1
                        assert len(cumulative_line) > 5, f"No title found on recto page {page}: {l}"
                ####################################################
                if recto_page_state == 1: # Check Titles
                    # Clean up the assembled title
                    cumulative_line = cumulative_line.replace(',,', ',')
                    for s in NO_COMMA_AFTER:
                        cumulative_line = cumulative_line.replace(s + ",", s)
                    cumulative_line = cumulative_line.replace('  ', ' ')
                    cumulative_line = cumulative_line.replace(', , ', ', ')
                    cumulative_line = cumulative_line.strip(', ')
                    cumulative_line = cumulative_line.strip()
                    cumulative_line = cumulative_line.replace(
                        '1349,Walter', '1349, Walter')
                    cumulative_line = cumulative_line.replace(
                        'Martyr 1942', 'Martyr, 1942')
                    cumulative_line = cumulative_line.replace(
                        '[Damien] Priest', '[Damien], Priest')
                    cumulative_line = cumulative_line.replace(
                        'Cope] Monastic', 'Cope], Monastic')

                    previous_record = find_feast_by_date_and_title(
                        feasts,
                        f"{mm:02}",
                        f"{dd:02}",
                        cumulative_line
                        )
                    assert previous_record, f"Couldn't locate record for {mm}/{dd} {cumulative_line}"
                    
                    # Check title consistency; choose on mismatch
                    def normalize(s):
                        s =  s.upper()
                        s = s.replace(']', '')
                        s = s.replace('[', '')
                        return s
                    TITLE_MISMATCHES_TO_IGNORE = (114, 126, 210, 219, 415, 416, 421, 1109)
                    PREFER_INDEX_TITLE = (201, 205, 214, 315, 628, 728, 909, 1014)
                    if mmdd not in TITLE_MISMATCHES_TO_IGNORE and mmdd not in PREFER_INDEX_TITLE:
                        index_title = normalize(previous_record['title'])
                        mainp_title = normalize(cumulative_line)
                        if index_title != mainp_title:
                            mismatches += 1
                            print (f"*** Mismatched name on {mm}/{dd}:")
                            print (f"*** == index -> {index_title}")
                            print (f"*** == mainp -> {mainp_title}")
                    if mmdd not in PREFER_INDEX_TITLE:
                        previous_record['title'] = cumulative_line
                    previous_record['bio'] = bio
                    cumulative_line = ""
                    bio = ""

                    recto_page_state += 1
                    cumulative_line = l.strip()
                    continue
                
                ####################################################
                if recto_page_state == 2: # Rite I Collect
                    if l[0:2] == "II":
                        cumulative_line = cumulative_line.lstrip('I').strip()
                        previous_record['rite1_collect'] = cumulative_line
                        cumulative_line = l.lstrip('II').strip()
                        recto_page_state += 1
                    else:
                        cumulative_line += " " + l
                        cumulative_line = cumulative_line.strip()
                    continue

                ####################################################
                if recto_page_state == 3: # Rite II Collect
                    if "Amen" in l:
                        if "Amen." not in l: # Missing in Charles Henry Brent Collect II
                            l.replace("Amen", "Amen.")
                        cumulative_line += l
                        cumulative_line = cumulative_line.lstrip('I').strip()
                        previous_record['rite2_collect'] = cumulative_line
                        cumulative_line = ""
                        recto_page_state += 1
                    else:
                        cumulative_line += " " + l
                        cumulative_line = cumulative_line.strip()
                    continue


                ####################################################
                GOSPELS = ("MATTHEW", "MARK", "LUKE", "JOHN")
                if len(l) == 0:
                    continue
                if recto_page_state == 4: # Lessons and Psalm
                    assert "Lessons and Psalm" in l, f"Unexpected line; expected 'Lessons and Psalm'; found {l} for {previous_record['title']} on {previous_record['mm']}/{previous_record['dd']}"
                    recto_page_state += 1
                    continue

                # Note instructions after verse number
                if recto_page_state == 5: # first lesson
                    previous_record['first_lesson'] = l
                    recto_page_state += 1
                    continue
            # 5. Get psalm (assert)
            # 6. Get second_lesson or +1 to gospel
            # 7. Get gospel (assert)
            # 8. Get preface, drop record, state to 1

            


print(f"{page} pages processed")
print(f"{mismatches} mismatches")
#print(find_feast_by_date_and_title(feasts, "04", "03", ""))
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
