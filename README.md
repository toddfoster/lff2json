# lff2json
Parse Lesser Feasts and Fasts 2018 into json

- LFF2018 is available online in pdf form.
- pdftotext gives me plain text.
- Now I want to parse it into json for automated use by www.sharedprayers.net.
- Found dates, bio's, maybe collects in venite.app, but not scriptures.

# Process:
- x Find page separators: pdf has 584pp.: "\f"
- Parse index to LFF2018 for authoritative date & name of each feast (Pp 7--18)
- How to choose slugs? Halfway manual?
	- Find main page for each feast
	- preceding page is bio
	- page with name at top has two collects, scriptures, preface
