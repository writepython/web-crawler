## sudo apt-get install python-musicbrainzngs
## sed '/^$/d' file.txt | wc -l

import csv, musicbrainzngs

musicbrainzngs.set_useragent("Example music app", "0.1", "http://example.com/music")
with open('/home/vagrant/a.csv', 'wb') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["ID", "Name"])
    f.flush()
    for i in range(981):
        result = musicbrainzngs.search_artists(country="US", limit=100, offset=i)
        for artist in result['artist-list']:
	        csv_writer.writerow([artist['id'], artist["name"].encode('utf-8')])
	        f.flush()
