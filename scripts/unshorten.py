import urllib.parse
import tldextract

from unshortenit import UnshortenIt
unshortener = UnshortenIt()


def unshorten_url(short_url):
    url = unshortener.unshorten(short_url)
    
    # Tambahan jika sumber dari adf.ly, ambil param 'dest'
    domain = tldextract.extract(short_url).domain
    if domain == 'adf':
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        dest_param = query_params.get('dest')
        if dest_param:
            dest_url = dest_param[0]
            url = dest_url

    return url


# panggil func
# print(unshorten_url('http://adf.ly/1FXRV5'))

# command line
# python -c "from scripts.unshorten import unshorten_url;print(unshorten_url('http://adf.ly/1FXRV5'))"
