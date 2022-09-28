# Microsoft Learn to Epub

This tool converts Microsoft Learn certifications paths to epub

## How to use

To make the epub you need the link of the certification in this case AZ-500
- Chose a language
  ```python 
    lang = 'es'
    language = 'es-mx'
    path_url = 'https://docs.microsoft.com/api/lists/studyguide/certification/certification.azure-security-engineer?locale=%s' % language
    base_url = 'https://docs.microsoft.com/%s' % language
  ```
- Run `main.py` 


- With `Prettier` format the files created by the script 

  ```npx prettier --write ./epub_base/EPUB/```


- And with `make-epub.py` create the EPUB file

  ```
  python make-epub.py epub_base file_name.epub
  ```
  
Note: 
To install Prettier with node

- For local installation `npm install prettier`