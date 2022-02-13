from calendar import month_name
import re
import json

# TEF, February 2022

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
LONG_LINES = ("in Hebrew.",
              "Epiphany in Year C.",
              "blessing of chalk:",
              "valued by the whole church.",
              "Aelred wrote his best known work",
              "love and peace with one another",
              "slaves in Ireland.",
              "lofty spirit.",
              "year 64 under Nero",
              "first bishop of that city",
              "humble, but not servile",
              "good things that are to come",
              "about fifteen years old.",
              "unwanted advances toward her",
              "Here I became one of the daughters",
              "dedicated herself to God in her youth",
              "where they are referred to as",
              "back into the Hagia Sophia",
              "rather than in schism",
              "indignantly walked out in protest",
              "September 21, 1802",
              "Moravia as Metropolitan",
              "influenced young English priests",
              "she was executed",
              "died on February 22", ## checked down to here

              "fellow Christians in trouble",
              "Holy Cross came into being",
              "retreat center of the Society",
              "preach the gospel that Jesus is the Christ",
              "command of the emperor Nero",
              "in whose service I have found",
              "Vaugham and Samuel",
              ## Ugh... poetry with line breaks! Only George Herbert is worth this!
              "soul drew back",
              "dust and sin",
              "me grow slack",
              "first entrance in",
              "sweetly questioning",
              "I lacked anything",
              "worthy to be here",
              "You shall be he",
              "the unkind, ungrateful",
              "cannot look on thee",
              "smiling did reply",
              "made the eyes but",
              "I have marred them",
              "where it doth",
              "who bore the blame",
              "then I will serve",
              "must sit down",
              "did sit and eat",
              ###
              "never believed myself worthy",
              "cause and methods",
              "proclaiming the gospel",
              "anonymous Christian woman",
              "suffer be a stumbling block",
              "masterpiece of ascetical",
              "vices and virtues with great care",
              "came to rely on a widow",
              "sacred wells and springs",
              "died in Jerusalem on March 18",
              "his own holy conduct",
              "this request was ignored",
              "the people will never perish",
              "remain at his post in the",
              "plaques brought by delegations from",
              "everywhere an ambassador",
              "until his retirement in 1929",
              # Hymn
              "morning is the love",
              "wakening and uprising",
              "sleep and darkness safely",
              "life and power and thought",
              # John Donne: Batter my heart!
              "three-person",
              "knock, breathe",
              "rise and stand",
              "break, blow, burn",
              "to another due",
              "Labor to admit",
              "your viceroy in me",
              "proves weak or",
              "dearly I love you",
              "unto your enemy",
              "Divorce me",
              "imprison me",
              "enthrall me",
              "ravish me",
              #
              "Apostle of the Wilderness",
              "1844 was on the frontier",
              #
              "three things I pray",
              "more clearly",
              "more dearly",
              "more nearly",
              #
              "consecrated place",
              "body lay",
              "against my face",
              "from the doorway",
              "By my fourty years",
              "in that desert land",
              "blissful final",
              "there on the sand",
              #
              "of Whites",
              "Mountain-Top Experience",
              "for our sake",
              "widening the range of music",
              "Great Awakening in America",
              "English colonial churches",
              "California where he",
              "color could attend",
              # didn't add for verses under Hadewijch
              "he prayed repeatedly",
              "social welfare programs",
              "gave away most of her income",
              "Rome to press further",
              "recall him to avoid",
              "spread of the early monastic",
              "died when she was in her",
              #
              "our Morningstar.",
              "bring us life again",
              "reap his fullness",
              #
              "will bury your mother",
              "being the persecutors and the oppressors",
              "apostate emperor",
              "seclusion again for healing",
              "ray of sunlight",
              "German and Swiss",
              "Protestant and Roman Catholic",
              "to a shoe",
              "Lutheran Orthodoxy of his day",
              "Associate Justice",
              "treated as a full member",
              "household was baptized",
              # no verse for Mechthild
              "public specatcle in the",
              "became centers of missionary",
              "enter into rest after the",
              "began a lifelong devotion",
              "trained as a catechist",
              "until her death on June 19",
              "saw Christ living in and through her",
              "least one other hermit",
              "stability, conversion of life",
              "Munich and Germany",
              "her interests in theology",
              "her impassioned arguments",
              "as a priest on April 25",
              "oppress and discriminate against women",
              "popularity soared as she engaged clergy",
              "sanctionmed and caused",
              "make her the equal in power",
              "women’s rights speakers’ network",
              "on November 26, 1883.",
              "Moses of their own.",
              "offered for her capture",
              "venerate the image of God",
              "Mount St. Agnes in Zwolle",
              "beauty of human friendship",
              "the different vocations of both sisters",
              "University of Freiburg",
              "went through many editions",
              "her son Louis IX",
              "hold him accountable",
              "fled France",
              "garden in disgust",
              "excerpt from her poem",
              # didn't add newlines for Hannah More's verse
              "the reviver of Geneva",
              "archbishops and popes",
              "judgment he bore patiently",
              "by Pope Vitalian",
              "Moscow in 1378",
              "Plains in 1380",
              # Didn't versify Andrewes poem
              "adopted the name of Smaragdus",
              "recognize his own child",
              "Jerome's famous",
              "one of the popular celebrations",
              "evangelistic efforts for the English",
              "connected ecumenism and evangelism",
              "Chairman of the Life and Work",
              # Didn't versify Francis
              "comes to recreate the old man",
              "feelings and consolations",
              "burned at the stake on March 21",
              "prostitute in a tavern",
              "unspeakable sadness and grief",
              "laity a voice in church",
              "thirst for missionary work",
              "chops off his nose",
              "Ammonius the Earless",
              "become a chaos of internal",
              "ascetic and missionary ideals",
              "whole tone and tendency",
              "Seabury then accepted",
              "attending the liturgies of the monastery",
              "Herman as their North Star",
              "father then entered a monastic",
              "Helfta as it continued to grow",
              "when we reached the zoo",
              "correspondence on spiritual matters",
              "kind of truth behind",
              "he had her beheaded",
              "Society of Saint Margaret",
              "largest civilian hospital",
              "Andrew the first missionary",
              "Master be like?",
              "a thousand communicants",
              "enslaved and sometimes",
              "Congregation of the Visitation",
              "little girl was healed",
              "sacrament herself",
              "released the faith",
              "ministry of a deacon",
              "Chancellor of England",
              )

EXTRA_LINE_BREAK = ("Amelia Jenks Bloomer 1818",
                    "Miriam of the Later Exodus",
                    "Moses of Her People",
                    "did sit and eat")

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

def scripture_has_instructions(reference, mmdd, title):
    found_numerals = False
    # Skip first character in case it is a numeral (e.g., 1 Corinthians)
    for c in reference[1:]:
        found_numerals = found_numerals or c.isdigit()
        if found_numerals and c.isalpha() and c not in  ("a", "b", "c"):
            debug(f"INFO: scripture with instructions for {mmdd} ({title}): {reference}")
            assert "or" in reference, f"WARNING: 'or' not in reference {reference}"
            return True
    return False

slugs = []
def make_slug(title):
    slug = title
    for i in ("PRESENTATION", "EPIPHANY", "ANNUNCIATION", "VISITATION", "TRANSFIGURATION"):
        if i in slug:
            slug = i
    for i in (",", "/", "(", " and"):
        if i in slug:
            slug = slug.split(i)[0]
    for i in ("[", "]"):
        slug = slug.replace(i, "")
    slug = slug.upper()
    if slug[0:4] == "THE ":
        slug = slug[4:]
    slug = slug.strip().replace(" ", "-")
    slug = "LFF2018-" + slug
    debug(f"DEBUG: slug = {slug}")
    assert slug not in slugs, f"ERROR: made duplicate slug {slug} for {title}"
    slugs.append(slug)
    return slug


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
        l = line.replace("\x07", "")
        l = l.replace("\u2013", '-').replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
        l = l.strip()
        # skip to beginning of index
        if page < PP_INDEX[0]:
            continue

        debug(f"DEBUGDEBUG: line = {l}")

        ###############
        # Parse index
        ###############
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

            # Check for major feast (all-caps in title)
            count_caps = 0
            for c in l:
                if c.isalpha() and c.isupper():
                    count_caps += 1
                    if count_caps > 2:
                        break
                else:
                    count_caps = 0
            major_feast = count_caps > 2

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
                    "major_feast": major_feast
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
                    "title": feast,
                    "major_feast": major_feast
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
                        dd = int(splits[1])
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

                    # Add slug
                    previous_record["slug"] = make_slug(previous_record["title"])

                    # Check title consistency; choose on mismatch
                    def normalize(s):
                        s =  s.upper()
                        s = s.replace(']', '')
                        s = s.replace('[', '')
                        return s
                    ACKNOWLEDGED_TITLE_MISMATCHES = ("0114", "0126", "0210", "0219",
                                                  "0415", "0416", "0421", "0720", "1109")
                    PREFER_INDEX_TITLE = ("0201", "0205", "0214", "0315",
                                          "0628", "0728", "0909", "1014")
                    if mmdd not in ACKNOWLEDGED_TITLE_MISMATCHES and mmdd not in PREFER_INDEX_TITLE:
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

                    bio = ""
                    cumulative_line = ""

                    recto_page_state += 1
                    cumulative_line = l.strip()
                    debug (f"DEBUG found title: {previous_record['title']}")
                    continue

                ####################################################
                # Typo: Collects for Willibrord name Boniface instead!
                if 2 <= recto_page_state <= 3 and "Willibrord" in previous_record['title']:
                    if "servant Boniface we might" in l:
                        l = l.replace("Boniface", "Willibrord")
                
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
                    if "Juana" in previous_record['title'] and "for ever and ever." in l:
                        l += " Amen." # TYPO Missing from Collect II for Juana Inés de la Cruz
                    if "Amen" in l:
                        if "Brent" in previous_record['title'] or "Cassey" in previous_record['title']:
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
                    if scripture_has_instructions(l, mmdd, previous_record['title']):
                        previous_record['notes'] = "or" + l.split("or")[1]
                        l = l.split("or")[0].strip()
                    previous_record['first_lesson'] = l
                    recto_page_state += 1
                    continue

                if recto_page_state == 6: # Psalm
                    assert "Psalm" in l, f"Unexpected line; expected Psalm, found {l}"
                    scripture_has_instructions(l, mmdd, previous_record['title'])
                    previous_record['psalm'] = l
                    recto_page_state += 1
                    continue

                GOSPELS = ("MATTHEW", "MARK", "LUKE", "JOHN")
                if recto_page_state == 7: # Second / Gospel
                    if scripture_has_instructions(l, mmdd, previous_record['title']):
                        previous_record['notes'] = "or" + l.split("or")[1]
                        l = l.split("or")[0].strip()
                    if l.split()[0].upper() in GOSPELS:
                        previous_record['gospel'] = l
                        recto_page_state += 2
                        continue
                    else:
                        previous_record['second_lesson'] = l
                        recto_page_state += 1
                    continue

                if recto_page_state == 8: # Gospel
                    if scripture_has_instructions(l, mmdd, previous_record['title']):
                        previous_record['notes'] = "or" + l.split("or")[1]
                        l = l.split("or")[0].strip()
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

debug(f"INFO: {page} pages processed")
debug(f"INFO: {mismatches} mismatches")
# print(find_feast_by_date_and_title(feasts, "0101", ""))

with open ("lff2018.json", "w") as t:
    t.write(json.dumps(feasts, indent=4))
