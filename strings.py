from lxml import etree

from os import walk

trans = {}
locales = []

for (dirpath, dirnames, filenames) in walk('.'):
    if dirpath == '.' or 'strings.xml' not in filenames:
        continue

    if dirpath == './values':
        locale = 'en'
    else:
        locale = '-'.join(dirpath.split('-')[1:])
    locales.append(locale)
    tree = etree.parse("%s/strings.xml" % (dirpath,))
    root = tree.getroot()
    for string in root.findall('.//string'):
        attrib = string.get('name')
        if attrib in trans:
            trans[attrib][locale] = string.text
        else:
            trans[attrib] = {locale: string.text}

import unicodecsv

with open('strings.csv', 'wb') as csvfile:
    spamwriter = unicodecsv.writer(csvfile, encoding='utf-8')
    spamwriter.writerow([''] + locales)

    for key, values in trans.items():
        spamwriter.writerow([key] + [values.get(locale, '') for locale in locales])
        
