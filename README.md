# lff2json
Parse Lesser Feasts and Fasts 2018 into json

- LFF2018 is available online in pdf form.
- pdftotext gives me plain text.
- Now I want to parse it into json for automated use by www.sharedprayers.net.
- Found dates, bio's, maybe collects in venite.app, but not scriptures.

# Process:
- x Find page separators: pdf has 584pp.: "\f"
- x Parse index to LFF2018 for authoritative date & name of each feast (Pp 7--18)
- x Verify index against pdf
- x Find main page for each feast
- x preceding page is bio
- x page with name at top has two collects, scriptures, preface
- x ad hoc cope with inconsistencies in text
- Provide slugs for easy reference?
- Proofread, especially looking for long lines that end paragraphs
