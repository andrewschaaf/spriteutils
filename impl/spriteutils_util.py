
import urllib2, re, os, tempfile, subprocess, StringIO
try:
    import json
except ImportError:
    import simplejson as json

# Python Imaging Library
import Image


#### Image-related Functions
# Note that these are the only functions that use any external image library.

def imgFromData(data):
    return Image.open(StringIO.StringIO(data))


def dimOfImg(img):
    return img.size


def buildSprite(backgroundRgba, imgs, layout, optipngLevel=None):
    
    # Find the sprite size
    spriteWidth = 0
    spriteHeight = 0
    for x, y, w, h in layout.values():
        spriteWidth = max(spriteWidth, x + w)
        spriteHeight = max(spriteHeight, y + h)
    assert spriteWidth > 0 and spriteHeight > 0
    
    # Draw the sprite
    sprite = Image.new("RGBA", (spriteWidth, spriteHeight), tuple(backgroundRgba))
    for img in imgs:
        x, y, w, h = layout[img['url']]
        sprite.paste(img['img'], (x, y))
    
    with TempDir() as td:
        
        # Save the sprite as a PNG
        path = '%s/foo.png' % td.path
        sprite.save(path)
        
        # Optimize the PNG
        if optipngLevel is not None:
            optipngLevel = int(optipngLevel)
            p = subprocess.Popen(['/usr/bin/env',
                                            'optipng',
                                            '-o%d' % optipngLevel,
                                            path],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            out, err = p.communicate()
            if p.returncode != 0:
                raise Exception('Error while running optipng!\n\n' + repr(err))
        
        # Load the PNG
        with open(path, 'rb') as f:
            png = f.read()
    
    return png


#### Misc

def expandUrl(url, localRoot):
    assert os.path.isdir(localRoot)
    if re.search(r'^http://', url):
        return url
    else:
        path = localRoot + url
        assert os.path.isfile(path), 'DNE: ' + path
        return 'file://' + path


def getDataFromUrl(url):
    if url.startswith('file://'):
        with open(url[len('file://'):], 'rb') as f:
            return f.read()
    elif url.startswith('http://'):
        return simpleGet(url)
    else:
        raise Exception('Unsupported url scheme for url ' + repr(url))


def simpleGet(url, GET=None, userAgent='Python-urllib/2.6'):
    req = urllib2.Request(url, headers={
        'User-Agent': userAgent,
    })
    response = urllib2.urlopen(req)
    b = response.read()
    return b


class TempDir:
    
    def __init__(self):
        self.path = tempfile.mkdtemp()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        subprocess.check_call(['rm', '-rf', self.path])

