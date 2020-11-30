# coding=utf-8
# python2
# pip install pyyaml
# pip install jinja2

import os
import urllib2
import yaml
from jinja2 import Environment, FileSystemLoader

TMPL_FILE = './main.yml'
YML_FILE = './pkg.yml'
PKG_HOME_DIR = os.environ.get('PKG_HOME_DIR','/root/tmp')
PATH = os.path.dirname(os.path.abspath(__file__))
TMPL_ENV = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, '')),
    trim_blocks=False
)


def create_download_yml():
    '''Create download yml'''

    tmpl = open(TMPL_FILE, 'r')
    pkg_yml = yaml.load(tmpl)
    with open(YML_FILE, 'w') as output:
        print(PATH)
        yml = TMPL_ENV.get_template(TMPL_FILE).render(pkg_yml)
        output.write(yml)


def download_pkg(yml_file):
    '''Download package from ymal define'''

    with open(yml_file, 'r') as f:
        yml = yaml.load(f)
        downloads = yml['package']
        base = yml['base']
        for key, value in zip(downloads, downloads.values()) :
            print(value)
            item = value['file']
            print("Downloading with {0} ...".format(item))

            path = value['url'].replace("{0}".format(base[key]['url']), '')
            download_path = "{0}{1}".format(PKG_HOME_DIR, path)

            if not os.path.exists(download_path):
                os.makedirs(download_path)

            item_file = urllib2.urlopen("{0}/{1}".format(value['url'], item))
            data = item_file.read()
            with open("{0}/{1}".format(download_path, item), "wb") as code:
                code.write(data)

def main():
    create_download_yml()
    download_pkg(YML_FILE)


if __name__ == "__main__":
    main()
