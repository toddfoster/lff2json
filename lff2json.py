from calendar import month_name
import re

# TODO: add extra spacing to stanton, et al bio (coded but not working?)
# TODO: Capture major feasts flag (all caps in index?
# TODO: Check by hand for long lines that need manual line breaks???

DEBUG = 1
DEBUG_LEVELS = ("WARNING", "INFO", "DEBUG", "DEBUGDEBUG")

page = 0
mismatches = 0
PP_INDEX = (14, 25)
PP_ENTRIES = (31, 578)
SOJOURNER_BIO = (317, 319)
XMAS_EXTRA = (567, 568)
COLLECT_RE = re.compile('^I[^rng]')
LONG_LINES = ("about fifteen years old.", "Master be like?", "Moses of their own.",
              "on November 26, 1883.", "women’s rights speakers’ network")
EXTRA_LINE_BREAK = ("Amelia Jenks Bloomer 1818-1894", "Sojourner Truth, \"Miriam of the Later",
                    "Harriet Ross Tubman, \"Moses of Her")

characters = 0
mayjune_day = 0
BLANK_DAYS_IN_MAY = (6, 7, 10, 12, 14, 16, 18, 23, 27, 29, 30)
BLANK_DAYS_IN_JUNE = (6, 7, 13, 20, 21, 23, 25, 27, 30)
months = []
for m in month_name[1:]:
    months += [m.upper()]

def debug(message):
    """Print debug statements depending on current debug level"""
    message_level = message.split()[0].replace(":","")
    level = DEBUG_LEVELS.index(message_level)
    if level <= DEBUG:
        print(message)

def check_for_instructions(reference, mmdd, title):
    if reference[-1].isalpha() and reference[-1] not in ("a", "b", "c"):
        debug(f"INFO: scripture with instructions for {mmdd} ({title}): {reference}")

def print_hex_chars(line_in):
    """Print hex characters so I can find & remove them."""
    for c in line_in:
        print(f"{c}: {ord(c):02x}")

def find_feast_by_date_and_title(feasts, mmdd, title):
    DATES_WITH_PROBLEM_TITLES=("0126", "0525", "0720", "0909", "0927")
    for f in feasts:
        if f["mm"] == mmdd[0:2] and f["dd"] == mmdd[2:4]:
            if not title:
                return f
            if mmdd in DATES_WITH_PROBLEM_TITLES:
                return f
            debug (f"DEBUG: find_feast_by_date_and_title p.{page} - {mmdd} {title[0:4].upper()}")
            debug (f"DEBUG: ----------------------------------------- {f['title'][0:4].upper()}")
            if title[0:4].upper() == f['title'][0:4].upper():
                return f
    debug (f"WARNING: find_feast_by_date_and_title failed on {mmdd}: {title}")


feasts = []
with open("src/lff2018.txt", "r", encoding="utf-8") as f:
    current_month = 0
    previous_record = {}
    mmdd_progress = 0
    mmdd = ""
    bio = ""
    cumulative_line = ""
    recto_page_state = 0
    long_bio = False
    for line in f:
        if "\f" in line:
            page += 1
            debug (f"DEBUG: Page #{page}")
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

        def add_to_bio(existing_bio, addition):
            result = existing_bio
            if len(addition) > 3:
                if len(result) > 0 and result[-1] != "\n":
                    result += " "
                for p in EXTRA_LINE_BREAK:
                    if p in addition:
                        result += "\n"
                result += addition.strip()
                if len(addition) < 70:
                    result += "\n"
                for p in LONG_LINES:
                    if p in addition:
                        result += "\n"
            return result

        if PP_ENTRIES[0] <= page <= PP_ENTRIES[1]:
            # verso pages have bio's; recto pages have title, collects, lessons, preface
            # easiest, though, to compare against beginning of this section;
            # so even pages (0, 2, etc.) will be verso and odd pages will be recto
        
            # Stanton, et al, bio runs three pages: handle specially
            if SOJOURNER_BIO[0] <= page <= SOJOURNER_BIO[1]:
                if len(l) != 0 and l[0] != '3' and l[0:4] != "July":
                    debug(f"DEBUG: adding line: {l}")
                    bio = add_to_bio(bio, l)
                recto_page_state = 0
                mm = 7
                dd = 20
                mmdd = "0720"
                continue

            #######################################################
            ## VERSO page with bio
            #######################################################
            if page not in XMAS_EXTRA and (page - PP_ENTRIES[0]) % 2 == 0:
                previous_record = {}
                splits = l.split()
                if len(splits) == 2:
                    month = splits[0].upper()
                    if month in months: # found date at bottom of page
                        debug(f"DEBUGDEBUG: End of bio for {l}")
                        mm = months.index(month) + 1
                        dd = int (splits[1])
                        assert 0 < dd < 32, f"Bad day value {dd}: {l}"
                        mmdd = f"{mm:02}{dd:02}"
                        assert int(mmdd) >= mmdd_progress, f"Source dates out of order: {l}"
                        mmdd_progress = int(mmdd)
                        recto_page_state = 0
                    elif len(l) > 3:
                        bio = add_to_bio(bio, l)

            #######################################################
            ## RECTO
            #######################################################
            else: #recto page with title, other data
                KEEP_LOOKING_LIST=("0315", "0416", "1016")

                ####################################################
                if recto_page_state == 0: # Looking for title
                    NO_COMMA_AFTER = (" and", " of", " Lord",
                                      " Benedicta", " Blessed",
                                      "Saint Philip", " Jesus")
                    if (len(l) > 0 or mmdd in KEEP_LOOKING_LIST) and not COLLECT_RE.match(l):
                        cumulative_line += ", " + l
                        continue
                    else:
                        debug (f"DEBUGDEBUG: Found title {cumulative_line}")
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

                    previous_record = find_feast_by_date_and_title(feasts, mmdd, cumulative_line)
                    assert previous_record, f"Couldn't locate record for {mmdd} (p. {page}): {cumulative_line}"
                    
                    # Check title consistency; choose on mismatch
                    def normalize(s):
                        s =  s.upper()
                        s = s.replace(']', '')
                        s = s.replace('[', '')
                        return s
                    TITLE_MISMATCHES_TO_IGNORE = ("0114", "0126", "0210", "0219",
                                                  "0415", "0416", "0421", "1109")
                    PREFER_INDEX_TITLE = ("0201", "0205", "0214", "0315",
                                          "0628", "0728", "0909", "1014")
                    if mmdd not in TITLE_MISMATCHES_TO_IGNORE and mmdd not in PREFER_INDEX_TITLE:
                        index_title = normalize(previous_record['title'])
                        mainp_title = normalize(cumulative_line)
                        if index_title != mainp_title:
                            mismatches += 1
                            debug (f"INFO *** Mismatched name on {mmdd}:")
                            print (f"INFO *** == index -> {index_title}")
                            print (f"INFO *** == mainp -> {mainp_title}")
                    if mmdd not in PREFER_INDEX_TITLE:
                        previous_record['title'] = cumulative_line
                    previous_record['bio'] = bio.strip()
                    cumulative_line = ""
                    bio = ""

                    recto_page_state += 1
                    cumulative_line = l.strip()
                    debug (f"DEBUG found title: {previous_record['title']}")
                    continue
                
                ####################################################
                if recto_page_state == 2: # Rite I Collect
                    if "Amen" in l:
                        assert "Amen." in l, "Found Rite I collect without full stop after Amen"
                        cumulative_line += " " + l.strip()
                        cumulative_line = cumulative_line.strip().lstrip('I').strip()
                        previous_record['rite1_collect'] = cumulative_line
                        debug (f"DEBUG Found Collect I: {cumulative_line}")
                        cumulative_line = ""
                        recto_page_state += 1
                    else:
                        cumulative_line += " " + l.strip()
                    continue

                ####################################################
                if recto_page_state == 3: # Rite II Collect
                    if page == 200 and "for ever and ever." in l:
                        l += " Amen." # TYPO Missing from Collect II for Juana Inés de la Cruz
                    if page in (162, 196):
                        l += "." # TYPO Missing full stop after Amen for C. H. Brent, P. W. Cassey
                    if "Amen" in l:
                        assert "Amen." in l, f"Found Rite I collect without full stop after Amen (p. {page}: {previous_record['title']})"
                        cumulative_line += " " + l.strip()
                        cumulative_line = cumulative_line.strip().lstrip('I').strip()
                        previous_record['rite2_collect'] = cumulative_line
                        debug (f"DEBUG Found Collect II: {cumulative_line}")
                        cumulative_line = ""
                        recto_page_state += 1
                    else:
                        cumulative_line += " " + l.strip()
                    continue

                ###################################################
                # Special handling for Christmas Day pages
                if mmdd == "1225":
                    debug (f"DEBUG: Xmas page {page}: {l}")
                    if page == 566:
                        recto_page_state = 14 #special state to catch lessons for Christmas"
                        continue
                    elif page == 567:
                        if len(l) <= 3 or "December" in l:
                            continue
                        if 'notes' not in previous_record:
                            previous_record['notes'] = l.strip()
                        else:
                            previous_record['notes'] += "\n" + l.strip()
                    elif page == 568 and recto_page_state == 14:
                        if "Lessons and Psalm" in l:
                            recto_page_state = 4
                            # don't continue: fall down into that handler!
                        else:
                            previous_record['notes'] += "\n" + l.strip()
                            continue
                    elif page == 568 and recto_page_state == 9 and "Preface" not in l:
                        if len(l) <= 3 or "December" in l:
                            continue
                        if "Isaiah" in l:
                            l = "or\n" + l
                        previous_record['notes'] += "\n" + l.strip()
                        continue    

                ####################################################
                if len(l) == 0:
                    continue
                if recto_page_state == 4: # Lessons and Psalm
                    assert "Lesson" in l and "Psalm" in l, f"Unexpected line; expected 'Lessons and Psalm'; found {l} for {previous_record['title']} on {mmdd}"
                    recto_page_state += 1
                    continue

                if recto_page_state == 5: # first lesson
                    check_for_instructions(l, mmdd, previous_record['title'])
                    previous_record['first_lesson'] = l
                    recto_page_state += 1
                    continue

                if recto_page_state == 6: # Psalm
                    assert "Psalm" in l, f"Unexpected line; expected Psalm, found {l}"
                    check_for_instructions(l, mmdd, previous_record['title'])
                    previous_record['psalm'] = l
                    recto_page_state += 1
                    continue

                GOSPELS = ("MATTHEW", "MARK", "LUKE", "JOHN")
                if recto_page_state == 7: # Second / Gospel
                    check_for_instructions(l, mmdd, previous_record['title'])
                    if l.split()[0].upper() in GOSPELS:
                        previous_record['gospel'] = l
                        recto_page_state += 2
                        continue
                    else:
                        previous_record['second_lesson'] = l
                        recto_page_state += 1
                    continue

                if recto_page_state == 8: # Gospel
                    check_for_instructions(l, mmdd, previous_record['title'])
                    assert l.split()[0].upper() in GOSPELS, f"Expected Gospel, found {l}"
                    previous_record['gospel'] = l
                    recto_page_state += 1
                    continue

                if recto_page_state == 9: # Preface
                    if len(l.strip()) == 0:
                        continue
                    if "Preface" in l or "Common" in l:
                        previous_record['preface'] = l
                        recto_page_state += 1
                        continue
                    if 'notes' not in previous_record:
                        previous_record['notes'] = ""
                    previous_record['notes'] = previous_record['notes'] + "\n" + l.strip()
                    continue


debug(f"INFO {page} pages processed")
debug(f"INFO {mismatches} mismatches")
# print(find_feast_by_date_and_title(feasts, "1231", ""))
print(find_feast_by_date_and_title(feasts, "0720", ""))
#print(find_feast_by_date_and_title(feasts, "1201", "[Charles"))
#for f in feasts:
#    print(f"{f['mm']}/{f['dd']}: {f['title']}")
