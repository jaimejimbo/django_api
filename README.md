Django server for wikipedia api parse
=====================================

This server connects to wikipedia and converts page's data to JSON format. It shows it in html body, so it can be parsed by other apps.

It allows to search over wikipedia by http parameters:

.../apijson/?uid=1;pattern=.*;busq=Google;contenido=true;results=10

uid -> user id
busq -> what to search over the wiki
pattern -> what to look for over the wiki's page
contenido -> if content must or not be downloaded.
results -> max number of results
