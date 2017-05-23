## sudo apt-get install python-musicbrainzngs
## sed '/^$/d' output/a.csv | wc -l

import csv, musicbrainzngs

musicbrainzngs.set_useragent("Example music app", "0.1", "http://example.com/music")
x = []
with open('output/a.csv', 'wb') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["ID", "Name"])
    f.flush()
    offset = 0
    for i in range(981):
        result = musicbrainzngs.search_artists(country="US", limit=100, offset=offset)
        for artist in result['artist-list']:
            csv_writer.writerow([artist['id'], artist["name"].encode('utf-8')])
        print "Finished iteration %d" % i
        offset += 100
        if '9' in str(i):
            f.flush()
