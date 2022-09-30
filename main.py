import bs4
import requests
import json
import re
import urllib.request
import os
from glob import glob


def generateOPF(href, spine):

    f = open(epub_dir + 'package.opf', 'w', encoding='utf-8')
    text1 = """<?xml version="1.0" encoding="utf-8" standalone="no"?>
    <package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:dcterms="http://purl.org/dc/terms/" version="3.0" xml:lang="%s" 
	unique-identifier="pub-identifier">
	<metadata>
	</metadata>
	<manifest>  
	""" % lang

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

    f = open(epub_dir + 'index.xhtml', 'w', encoding='utf-8')

    text1 = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="%s" lang="%s">
	<head>
	<title>Guide</title>
	<link rel="stylesheet" type="text/css" href="css/epub.css" />
	</head>
	<body>
	<h1>Guide</h1>
	<nav epub:type="toc" id="toc">
	<h2>Table of Contents</h2>""" % (lang, lang)

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

                for index, k in enumerate(j[h][0]) :
                    list_index += '<li>\n<a href="%s">%s</a></li>\n' % (replaceSymbols(h.replace(' ', '-') + '-' + j[h][1][index].replace(' ', '-') + '.xhtml'), k)

            list_index += '</ol>\n'
        list_index += '</ol>\n'
    list_index += '</ol>\n'

    f.write(text1)
    f.write(list_index)
    f.write(text2)
    f.close()


def replaceSymbols(s):

    s = s.replace(':', '')
    a, b = 'áéíóúüñ', 'aeiouun'
    trans = str.maketrans(a, b)

    return s.translate(trans)

def downloadImage(module_url, img_url):

    if img_url:
        for img in img_url:

            if not 'https' in img:
                urllib.request.urlretrieve(module_url + img, './epub_base/EPUB/images/'+ img.split('/')[-1])


def deleteTags(source_text):

    delete1 = '<span class="visually-hidden">{}</span>'
    search = re.findall('<span class="visually-hidden">(.*?)</span>', source_text)

    delete2 = '<p>\n<a class="button button-primary button-clear" data-linktype="absolute-path" {}>\n<span>{}</span>\n<span class="docon docon-chevron-right-light"></span>\n</a>\n</p>'
    search2 = re.findall('href="/[a-zA-Z]+-[a-zA-Z]+/"', source_text)

    delete3 = '<button class="button button-primary button-filled is-radiusless margin-top-xs" data-bi-name="check-answers" type="submit">{}</button>'
    search3 = re.findall('type="submit">(.*?)</button>', source_text)

    delete4 = '<p class="font-size-sm has-text-danger font-weight-semibold margin-top-xxs is-hidden" id="unanswered-question-error" role="alert">{}</p>'
    search4 = re.findall('role="alert">(.*?)</p>', source_text)

    if search:
        source_text = source_text.replace(delete1.format(search[0]), '')

    if search2:
        search_aux = re.findall('%s>\n<span>(.*?)</span>' % search2[0], source_text)
        if search_aux:
            source_text = source_text.replace(delete2.format(search2[0], search_aux[0]), '')

    if search3:
        source_text = source_text.replace(delete3.format(search3[0]), '')

    if search4:
        source_text = source_text.replace(delete4.format(search4[0]), '')

    return source_text
def getTextModule(source, module, submodules, file_name):


    source_text = ''
    file_name = replaceSymbols(file_name)
    f = open(epub_dir + file_name , 'w', encoding='utf-8')
    text1 = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <!DOCTYPE html>
            <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="%s" lang="%s">
    	        <head>
    		        <title>%s</title>
    		        <link rel="stylesheet" type="text/css" href="css/epub.css" />
    	        </head>
                <body>\n""" % (lang, lang, module)

    text2 = """</body>
        </html>
        """


    for s in source[0].contents:

        source_text += str(s)


    href = re.findall('href="(.*?)"', source_text)

    if href:
        for count, i in enumerate(href):
            source_text = source_text.replace(i, replaceSymbols(module.replace(' ', '-') + '-' + submodules[count].replace(' ', '-')) + '.xhtml')

    search = re.findall('<span class="unit-duration font-size-xs margin-top-xxs has-text-subtle">(.*?)</span>',source_text)
    source_text = source_text.replace('<span class="unit-duration font-size-xs margin-top-xxs has-text-subtle">%s</span>' % search[0], '')

    search = re.findall('<span class="add-to-collection-status">\s+[a-zA-Z]+\s+</span>', source_text)
    source_text = source_text.replace(search[0], '')

    source_text = source_text.replace(' ',' ')
    
    f.write(text1)
    f.write(source_text)
    f.write(text2)
    f.close()



def getText(source, submodule_tile, file_name, boolean):

    source_text = ''
    file_name = replaceSymbols(file_name)
    f = open(epub_dir + file_name, 'w', encoding='utf-8')

    text1 = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <!DOCTYPE html>
            <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="%s" lang="%s">
    	        <head>
    		        <title>%s</title>
    		        <link rel="stylesheet" type="text/css" href="css/epub.css" />
    	        </head>
                <body>\n""" % (lang, lang, submodule_tile)

    text2 = """</body>
        </html>
        """


    for s in source[0].contents:

        source_text += str(s)

    source_text = deleteTags(source_text)

    img_url = re.findall('src="(.*?)"', source_text)

    if img_url:

        for i in img_url:

            if not 'https' in i:
                source_text = source_text.replace(i, 'images/'+ i.split('/')[-1])
            else:
                iframe = re.findall('<iframe (.*?)</iframe>', source_text)

                for j in iframe:
                    source_text = source_text.replace('<iframe %s</iframe>' % j, '<a href="%s">Link</a>' % i)


    if boolean:

        href = re.findall('href="(.*?)"', source_text)

        for i in href:


            if not 'https' in i:
                base_aux = base_url.replace(language, '').replace('.com/', '.com')
                source_text = source_text.replace('href="%s"' % i, 'href="%s"' % (base_aux + i))

    else:


        href = re.findall('href="(.*?)"', source_text)

        for i in href:

            if not 'https' in i:

                base_aux = base_url.replace(language, '').replace('.com/', '.com')

                if 'lightbox' in i:

                    i_aux = i.replace('../../', '/training/')
                    source_text = source_text.replace('href="%s"' % i, 'href="%s"' % (base_aux + i_aux))

                else:

                    source_text = source_text.replace('href="%s"' % i, 'href="%s"' % (base_aux + i))


    source_text = source_text.replace(' ',' ')
    
    f.write(text1)
    f.write(source_text)
    f.write(text2)
    f.close()

    return img_url

def getModules(_url, class_type, base):

    url_request = requests.get(_url)
    soup = bs4.BeautifulSoup(url_request.text, 'html.parser').find_all(class_= class_type)
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


def getContent(urls, titles):

    href = ''
    spine = ''
    titles_dict = {}

    for count, url in enumerate(urls):

        modules_url, modules_title = getModules(base_url + url, 'display-block text-decoration-none', base_url)
        titles_dict[titles[count]] = []

        for count0, module in enumerate(modules_url):

            aux_dict = {}
            sub_modules, submodules_title = getModules(module,'unit-title display-block font-size-md has-line-height-reset','')
            submodules_title_short_name = [''] * submodules_title.__len__()

            for index, sub in enumerate(sub_modules):
                submodules_title_short_name[index] = sub_modules[index].split( '/')[-1]

            r = requests.get(module)
            r.encoding = 'utf-8'

            soup_module = bs4.BeautifulSoup(r.text, 'html.parser').find_all(class_='column is-auto padding-none padding-sm-tablet position-relative-tablet')

            getTextModule(soup_module, modules_title[count0], submodules_title_short_name, modules_title[count0].replace(' ','-')+'.xhtml')


            href += """<item id="%s%s" href="%s" media-type="application/xhtml+xml"/>\n""" %  (count, count0, replaceSymbols(modules_title[count0].replace(' ','-')+'.xhtml'))
            spine += """<itemref idref="%s%s"/>\n""" % (count, count0)


            aux_dict[modules_title[count0]] = [submodules_title, submodules_title_short_name]
            titles_dict[titles[count]].append(aux_dict)


            for count1, source in enumerate(sub_modules):

                source_code = requests.get(source)
                source_code.encoding = 'utf-8'

                soup = bs4.BeautifulSoup(source_code.text, 'html.parser').find_all(class_='section is-uniform position-relative')
                file_name = replaceSymbols(modules_title[count0].replace(' ', '-') + '-' + submodules_title_short_name[count1].replace(' ', '-') + '.xhtml')
                print(source)

                if count1 == 0:

                    img_url = getText(soup, submodules_title[count1], file_name, True)

                elif count1 == sub_modules.__len__()-1:

                    img_url = getText(soup, submodules_title[count1], file_name, True)

                else:
                    img_url = getText(soup, submodules_title[count1], file_name, False)

                downloadImage(module, img_url)

                href += """<item id="%s%s%s" href="%s" media-type="application/xhtml+xml"/>\n""" % (count, count0, count1, file_name)
                spine += """<itemref idref="%s%s%s"/>\n""" % (count, count0, count1)

    generateIndex(titles_dict)

    href_index = """<item id="htmltoc" properties="nav" media-type="application/xhtml+xml" href="index.xhtml"/>\n"""
    spine_index = """<itemref idref="htmltoc" linear="yes"/>\n"""

    generateOPF(href_index + href, spine_index + spine)


if __name__ == '__main__':

    lang = 'es'
    language = 'es-mx'
    path_url = 'https://learn.microsoft.com/api/lists/studyguide/exam/exam.az-500?locale=%s' % language
    base_url = 'https://learn.microsoft.com/%s' % language

    r = requests.get(path_url)
    main_modules = json.loads(r.text)
    main_titles = []
    urls = []

    images_dir = './epub_base/EPUB/images/'
    epub_dir = './epub_base/EPUB/'
    if not os.path.exists(images_dir):
        os.mkdir(images_dir)

    for file in glob(epub_dir + '*.*'):
        if os.path.isfile(file):
            os.remove(file)

    for file in glob(images_dir + '*.*'):
        if os.path.isfile(file):
            os.remove(file)

    for module in main_modules['items']:
        urls.append(module['data']['url'])
        main_titles.append(module['data']['title'])

    getContent(urls, main_titles)
