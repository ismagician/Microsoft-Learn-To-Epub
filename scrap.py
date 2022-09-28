import bs4
import requests
import json
import re
import urllib.request

# https://docs.microsoft.com/api/lists/studyguide/certification/certification.azure-security-engineer?locale=en-us
# https://docs.microsoft.com/en-us/certifications/exams/az-500


def generateOPF(href, spine):

    f = open('./xhtml/package.opf','w', encoding='utf-8')
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


def generateIndex(modules_title):

    f = open('./xhtml/index.xhtml', 'w', encoding='utf-8')

    text1 = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
	<head>
	<title>Accessible EPUB 3</title>
	<link rel="stylesheet" type="text/css" href="css/epub.css" />
	</head>
	<body>
	<h1>Accessible EPUB 3</h1>
	<nav epub:type="toc" id="toc">
	<h2>Table of Contents</h2>"""

    text2 = """</nav>
	        </body>
            </html>"""

    list_index = '<ol>\n'

    for i in modules_title:
        list_index += '<li>%s</li>\n' % i
        list_index += '<ol>\n'

        for j in modules_title[i]:

            for h in j:

                list_index += '<li>\n<a href="%s">%s</a></li>\n' % (replaceSymbols(h.replace(' ', '-')+'.xhtml'), h)
                list_index += '<ol>\n'

                for k in j[h]:
                    list_index += '<li>\n<a href="%s">%s</a></li>\n' % (replaceSymbols(h.replace(' ', '-') + '-' + k.replace(' ', '-') + '.xhtml'), k)

            list_index += '</ol>\n'
        list_index += '</ol>\n'
    list_index += '</ol>\n'

    f.write(text1)
    f.write(list_index)
    f.write(text2)
    f.close()


def replaceSymbols(s):

    a, b = 'áéíóúüñ', 'aeiouun'
    trans = str.maketrans(a, b)

    return s.translate(trans)

def downloadImage(base_url, img_url):

    if img_url:
        for img in img_url:

            urllib.request.urlretrieve(base_url + img, './xhtml/images/'+img.split('/')[-1])

def getTextModule(source, module, submodules, title):

    source_text = ''
    title = replaceSymbols(title)
    f = open('./xhtml/' + title , 'w', encoding='utf-8')
    text1 = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <!DOCTYPE html>
            <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en"lang="en">
    	        <head>
    		        <title>%s</title>
    		        <link rel="stylesheet" type="text/css" href="css/epub.css" />
    	        </head>
                <body>\n""" % module

    text2 = """</body>
        </html>
        """


    for s in source[0].contents:

        source_text += str(s)


    href = re.findall('href="(.*?)"', source_text)

    if href:
        for count, i in enumerate(href):
            source_text = source_text.replace(i, replaceSymbols(module.replace(' ', '-') + '-' + submodules[count].replace(' ', '-')) + '.xhtml')

    source_text = source_text.replace('min', '')

    f.write(text1)
    f.write(source_text)
    f.write(text2)
    f.close()



def getText(source, submodule_tile, title, base_url, boolean):

    source_text = ''
    title = replaceSymbols(title)
    f = open('./xhtml/' + replaceSymbols(title), 'w', encoding='utf-8')
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


    for s in source[0].contents:

        source_text += str(s)

    img_url = re.findall('src="(.*?)"', source_text)

    if img_url:
        for i in img_url:
            source_text = source_text.replace(i, 'images/'+ i.split('/')[-1])


    if boolean:

        href_no_url = re.findall('href="/(.*?)/"', source_text)
        source_text = source_text.replace('href="/%s/"' % href_no_url[-1], '')

        href = re.findall('href="(.*?)"', source_text)

        for i in href:
            base_aux = base_url.replace(language, '').replace('.com/', '.com')
            source_text = source_text.replace('href="%s"' % i, 'href="%s"' % (base_aux + i))


    for text in text_to_delete:
        source_text = source_text.replace(text,'')

    f.write(text1)
    f.write(source_text)
    f.write(text2)
    f.close()

    return img_url

def getModules(_url, class_type, base):

    url_request = requests.get(_url)
    soup = bs4.BeautifulSoup(url_request.text, 'html.parser').find_all(class_=class_type)
    titles = []
    content_url = []

    for content in soup:
        if '../' in content['href']:
            content_url.append(base + "/training/" + content['href'].replace("../", ""))
            titles.append(content.text.replace('\n', '').replace(' ',''))
        else:
            content_url.append(_url + content['href'])
            titles.append(content.text.replace('\n', '').replace(' ',''))

    return content_url, titles


def getContent(base_url, urls, titles):

    href = ''
    spine = ''
    titles_dict = {}

    for count, url in enumerate(urls):

        modules_url, modules_title = getModules(base_url + url, 'display-block text-decoration-none', base_url)
        titles_dict[titles[count]] = []


        for count0, module in enumerate(modules_url):

            aux_dict = {}
            sub_modules, submodules_title = getModules(module,'unit-title display-block font-size-md has-line-height-reset','')
            r = requests.get(module)
            r.encoding = 'utf-8'

            soup_module = bs4.BeautifulSoup(r.text, 'html.parser').find_all(class_='column is-auto padding-none padding-sm-tablet position-relative-tablet')

            getTextModule(soup_module, modules_title[count0], submodules_title, modules_title[count0].replace(' ','-')+'.xhtml')


            href += """<item id="%s%s" href="%s" media-type="application/xhtml+xml"/>\n""" %  (count, count0, replaceSymbols(modules_title[count0].replace(' ','-')+'.xhtml'))
            spine += """<itemref idref="%s%s"/>\n""" % (count, count0)


            aux_dict[modules_title[count0]] = submodules_title
            titles_dict[titles[count]].append(aux_dict)


            for count1, source in enumerate(sub_modules):

                source_code = requests.get(source)
                source_code.encoding = 'utf-8'

                soup = bs4.BeautifulSoup(source_code.text, 'html.parser').find_all(class_='section is-uniform position-relative')
                title = replaceSymbols(modules_title[count0].replace(' ', '-') + '-' + submodules_title[count1].replace(' ', '-') + '.xhtml')
                print(source)

                if count1 == 0:

                    img_url = getText(soup, submodules_title[count1], title, base_url, True)

                elif count1 == sub_modules.__len__()-1:

                    img_url = getText(soup, submodules_title[count1], title, base_url, True)

                else:
                    img_url = getText(soup, submodules_title[count1], title, base_url, False)

                downloadImage(module, img_url)


                href += """<item id="%s%s%s" href="%s" media-type="application/xhtml+xml"/>\n""" % (count,count0, count1, title)
                spine += """<itemref idref="%s%s%s"/>\n""" % (count, count0, count1)


    generateIndex(titles_dict)

    href_index = """<item id="htmltoc" properties="nav" media-type="application/xhtml+xml" href="index.xhtml"/>\n"""
    spine_index = """<itemref idref="htmltoc" linear="yes"/>\n"""

    generateOPF(href_index + href, spine_index + spine)


if __name__ == '__main__':

    language = 'es-mx'
    r = requests.get(
        'https://docs.microsoft.com/api/lists/studyguide/certification/certification.azure-security-engineer?locale=%s' % language)
    base_url = 'https://docs.microsoft.com/%s' % language
    text_to_delete = ['<span class="visually-hidden">Completado</span>', '<span>Continuar </span>']
    main_modules = json.loads(r.text)
    main_titles = []
    urls = []

    for module in main_modules['items']:
        urls.append(module['data']['url'])
        main_titles.append(module['data']['title'])

    getContent(base_url, urls, main_titles)
