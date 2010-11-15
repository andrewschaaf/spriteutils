
#### Add impl to PYTHONPATH

import os, sys, base64, hashlib

def parentOf(path, n=1):
    return '/'.join(path.rstrip('/').split('/')[:-n])

REPO = parentOf(os.path.abspath(__file__), n=2)

sys.path.append('%s/impl' % REPO)


#### Tests

import unittest
from unittest import TestCase
from spriteutils import *

with open('%s/examples/raw/initial.css' % REPO, 'rb') as f:
    INITIAL_CSS = f.read()



class Test_spriteImagesFromCss(TestCase):
    def runTest(self):
        y = spriteImagesFromCss({
            'css': INITIAL_CSS,
            'root': '%s/examples/djangoapp' % REPO,
        })
        assert set(y['sprite_images_map'].keys()) == set(['initial'])
        assert len(y['sprite_images_map']['initial']) == 3
        assert all(
                    re.search(r'file:///.*images/landing/signup.*\.png$', url)
                    for url in y['sprite_images_map']['initial'])


class Test_spriteCreate(TestCase):
    def runTest(self):
        y = spriteImagesFromCss({
            'css': INITIAL_CSS,
            'root': '%s/examples/djangoapp' % REPO,
        })
        imageUrls = y['sprite_images_map']['initial']
        background = [255, 0, 0, 128]
        y = spriteCreate({
            'optipng': 2,
            'background': background,
            'images': imageUrls,
        })
        png = base64.b64decode(y['png_64'])
        
        assert hashlib.sha1(png).hexdigest() == 'b6d7fa1d97727dfe1dfa7137282b4ad023bbf1e0'


#class Test_spriteHtmlViz(TestCase):
#    def runTest(self):
#        raise NotImplementedError


class Test_spriteReplace(TestCase):
    def runTest(self):
        imgsRoot = '%s/examples/djangoapp' % REPO
        y = spriteImagesFromCss({
            'css': INITIAL_CSS,
            'root': imgsRoot,
        })
        imageUrls = y['sprite_images_map']['initial']
        y = spriteCreate({
            'background': '#94E4F9',
            'images': imageUrls,
        })
        layout = y['layout']
        y = spriteReplaceCss({
            'sprite_urls': {
                'initial': 'INITIAL_SPRITE_URL',
                'registration': 'FINAL_SPRITE_URL',
            },
            'root': imgsRoot,
            'css': INITIAL_CSS,
            'layout': layout,
        })
        css = y['css']
        assert css == '\n.signup {\n    background: url("INITIAL_SPRITE_URL") 0 0;\nwidth: 182px;\nheight: 36px;\n}\n.signup:hover {\n    background: url("INITIAL_SPRITE_URL") 0 -36px;\n}\n.signup:active {\n    background: url("INITIAL_SPRITE_URL") 0 -72px;\n}\n'


if __name__ == '__main__':
    unittest.main()
