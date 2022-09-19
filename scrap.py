import bs4
import requests
import json


# https://docs.microsoft.com/api/lists/studyguide/certification/certification.azure-security-engineer?locale=en-us
# https://docs.microsoft.com/en-us/certifications/exams/az-500

def generateOPF(href, spine):
    f = open('index.xhtml','w', encoding='utf-8')
    text1 = """<?xml version="1.0" encoding="utf-8" standalone="no"?>
    <package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:dcterms="http://purl.org/dc/terms/" version="3.0" xml:lang="en"
	unique-identifier="pub-identifier">
	<metadata>
	</metadata>
	<manifest>  
	"""
    text2 = """		<item id="epub.embedded.font.1" href="fonts/UbuntuMono-B.ttf" media-type="application/vnd.ms-opentype"/>
		<item id="epub.embedded.font.2" href="fonts/UbuntuMono-BI.ttf" media-type="application/vnd.ms-opentype"/>
		<item id="epub.embedded.font.3" href="fonts/UbuntuMono-R.ttf" media-type="application/vnd.ms-opentype"/>
		<item id="epub.embedded.font.4" href="fonts/UbuntuMono-RI.ttf" media-type="application/vnd.ms-opentype"/>
		<item id="epub.embedded.font.5" href="fonts/FreeSerif.otf" media-type="application/vnd.ms-opentype"/>
		<item id="epub.embedded.font.6" href="fonts/FreeSansBold.otf" media-type="application/vnd.ms-opentype"/>
		</manifest>
        """
    text3 = """<spine>"""
    text4 = """</spine>
    </package>"""

    f.write(text1)
    f.write(href)
    f.write(text2)
    f.write(text3)
    f.write(spine)
    f.write(text4)
    f.close()



def getText(source, submodule_tile,title):
    f = open('./xhtml/' + title, 'w', encoding='utf-8')
    text1 = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <!DOCTYPE html>
            <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en"lang="en">
    	        <head>
    		        <title>%s</title>
    		        <link rel="stylesheet" type="text/css" href="css/epub.css" />
    	        </head>
                <body>\n""" % submodule_tile

    text2 = """</body>
        </html>
        """
    f.write(text1)
    for s in source[0].contents:
        f.write(str(s))

    f.write(text2)
    f.close()


def getModules(_url, class_type, base):
    url_request = requests.get(_url)
    soup = bs4.BeautifulSoup(url_request.text, 'html.parser').find_all(class_=class_type)
    titles = []
    content_url = []

    for content in soup:
        if '../' in content['href']:
            content_url.append(base + "/training/" + content['href'].replace("../", ""))
            titles.append(content.text.replace('\n', ''))
        else:
            content_url.append(_url + content['href'])
            titles.append(content.text.replace('\n', ''))

    return content_url, titles


def getContent(urls):
    href = ''
    spine = ''
    for url in urls:
        modules_url, modules_title = getModules(base_url + url, 'display-block text-decoration-none', base_url)

        for count0, module in enumerate(modules_url):
            sub_modules, submodules_title = getModules(module,'unit-title display-block font-size-md has-line-height-reset','')

            for count1, source in enumerate(sub_modules):
                source_code = requests.get(source)
                soup = bs4.BeautifulSoup(source_code.text, 'html.parser').find_all(
                    class_='section is-uniform position-relative')
                title = modules_title[count0].replace(' ', '-') + '-' + submodules_title[count1].replace(' ', '-') + '.xhtml'
                getText(soup, submodules_title[count1] ,title)
                href += """<item id="%s%s" href="%s" media-type="application/xhtml+xml"/>\n""" % (count0, count1, title)
                spine += """<itemref idref="%s%s"/>\n""" % (count0, count1)

    print(href)
    print(spine)
    generateOPF(href, spine)


if __name__ == '__main__':

    r = requests.get('https://docs.microsoft.com/api/lists/studyguide/certification/certification.azure-security-engineer?locale=en-us')
    base_url = 'https://docs.microsoft.com/en-us'
    modules = json.loads(r.text)
    titles = []
    urls = []

    for module in modules['items']:
        urls.append(module['data']['url'])
        titles.append(module['data']['title'])

    getContent(urls)
