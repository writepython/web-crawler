## sudo apt-get install python-musicbrainzngs
## sed '/^$/d' output/a.csv | wc -l

import csv, musicbrainzngs

musicbrainzngs.set_useragent("Example music app", "0.1", "http://example.com/music")
x = []
with open('output/musicbrainz_us_artists_urls.csv', 'wb') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["ID", "Name", "URL"])
    f.flush()
    reader_row = 0
    with open('input/musicbrainz_us_artists.csv', 'rb') as r:
        musicbrainz_us_artists_reader = csv.reader(r)
        for row in musicbrainz_us_artists_reader:
            reader_row += 1
            musicbrainz_artist_id = row[0]
            musicbrainz_artist_name = row[1]
            try:
                result = musicbrainzngs.get_artist_by_id(musicbrainz_artist_id, includes=['url-rels'])
                url_list = result['artist']['url-relation-list']
                for url_dict in url_list:
                    target = url_dict['target']
                    if url_dict['type'] == 'official homepage':
                        print musicbrainz_artist_name, target
                        csv_writer.writerow([musicbrainz_artist_id, musicbrainz_artist_name, target])
                    elif url_dict['type'] == 'social network':
                        if 'facebook.com' in target:
                            print musicbrainz_artist_name, target                        
                            csv_writer.writerow([musicbrainz_artist_id, musicbrainz_artist_name, target])
            except:
                pass
            if str(reader_row).endswith('000'):
                f.flush()            


    ## for i in range(981):
    ##     result = musicbrainzngs.search_artists(country="US", limit=100, offset=offset)
    ##     for artist in result['artist-list']:
    ##         
    ##     print "Finished iteration %d" % i
    ##     offset += 100
    ##     if '9' in str(i):
    ##         f.flush()
