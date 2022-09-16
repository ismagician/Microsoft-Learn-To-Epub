import bs4
import requests
import json


# https://docs.microsoft.com/api/lists/studyguide/certification/certification.azure-security-engineer?locale=en-us
# https://docs.microsoft.com/en-us/certifications/exams/az-500


def get_modules(_url, class_type, base):
    url_request = requests.get(_url)
    soup = bs4.BeautifulSoup(url_request.text, 'html.parser').find_all(class_=class_type)
    content_url = []

    for content in soup:
        if '../' in content['href']:
            content_url.append(base + "/training/" + content['href'].replace("../", ""))
        else:
            content_url.append(_url + content['href'])

    return content_url


def get_content(urls):
    for url in urls:
        modules_url = get_modules(base_url + url, 'display-block text-decoration-none', base_url)

        for module in modules_url:
            sub_modules = get_modules(module, 'unit-title display-block font-size-md has-line-height-reset', '')

            for source in sub_modules:
                source_code = requests.get(source)
                soup = bs4.BeautifulSoup(source_code.text, 'html.parser').find_all(class_='section is-uniform position-relative')
                print(source_code.text)


if __name__ == '__main__':

    r = requests.get('https://docs.microsoft.com/api/lists/studyguide/certification/certification.azure-security-engineer?locale=en-us')
    base_url = 'https://docs.microsoft.com/en-us'
    modules = json.loads(r.text)
    print(r.text)
    titles = []
    urls = []

    for module in modules['items']:
        urls.append(module['data']['url'])
        titles.append(module['data']['title'])

    get_content(urls)
