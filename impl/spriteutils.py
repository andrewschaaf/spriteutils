
import sys, os, re, base64
from spriteutils_util import json, getDataFromUrl, imgFromData, dimOfImg, buildSprite, expandUrl


def main(f):
    
    x = json.loads(sys.stdin.read())
    
    try:
        y = f(x)
    except Exception, e:
        sys.stderr.write(json.dumps({
            'exception': repr(e),#TODO: include traceback
        }))
        sys.exit(1)
    
    sys.stdout.write(json.dumps(y))


# **CSS\_SPRITE\_REGEX**
# 
# * spriteName
# * backgroundUrl
# * width (optional)
# * height (optional)
CSS_SPRITE_REGEX = r'''(?x)
    \/\*  \s*  SPRITE  \s*  (?P<spriteName>[^*\s]+)  \s*  \*\/  \s*\n\s*
    background:  \s*  url\("(?P<backgroundUrl>[^"]+)"\);  \s*\n\s*
    (?:width:  \s*  (?P<width>[0-9]+)px;  \s*\n\s*)?
    (?:height:  \s*  (?P<height>[0-9]+)px;  \s*\n)?
'''


#### spriteImagesFromCss
#<pre>{
#   "css": "...",
#   "root": "..."
#}
#{
#   "sprite_images_map": {
#       "...spritename...": [
#           "file:///...",
#           "http://...",
#       ],
#       ...
#   }
#}</pre>
def spriteImagesFromCss(x):
    
    css = x['css']
    
    d = {}
    for m in re.finditer(CSS_SPRITE_REGEX, css):
        
        spriteName = m.group('spriteName')
        backgroundUrl = m.group('backgroundUrl')
        imageUrl = expandUrl(backgroundUrl, os.path.expanduser(x['root']))
        
        if spriteName not in d:
            d[spriteName] = []
        d[spriteName].append(imageUrl)
    
    return {
        'sprite_images_map': d,
    }


#<pre>{
#    "sprite_urls": {"spriteName": [...], ...}
#    "layout": {...}
#    "root": "..."
#    "css": "..."
#}
#{
#    "css": "..."
#}</pre>
def spriteReplaceCss(x):
    
    def f(m):
        
        spriteUrl = x['sprite_urls'][m.group('spriteName')]
        backgroundUrl = m.group('backgroundUrl')
        imageUrl = expandUrl(backgroundUrl, os.path.expanduser(x['root']))
        ix, iy, iw, ih = x['layout'][imageUrl]
        
        css = 'background: url("%s") %s %s;\n' % (
                    spriteUrl,
                    '0' if ix == 0 else str(-ix) + 'px',
                    '0' if iy == 0 else str(-iy) + 'px')
        
        #TODO: match indent
        w, h = m.group('width'), m.group('height')
        if w and h:
            w, h = int(w), int(h)
            assert (w, h) == (iw, ih), [[w, h], [iw, ih]]
            css += 'width: %dpx;\nheight: %dpx;\n' % (w, h)
        
        return css
    
    return {
        'css': re.sub(CSS_SPRITE_REGEX, f, x['css']),
    }


#### spriteCreate
#<pre>{
#    "optipng": level,// optional
#    "background": "#xxxxxx" or [r, g, b, a] ([0,255]),
#    "images": [
#        "file://...",
#        "http://..."
#    ]
#}
#{
#    "png_64": "..."
#    "layout": {
#        imageUrl: [x, y, w, h],
#        ...
#    }
#}</pre>
def spriteCreate(x):
    
    # Parse <code>background</code>
    bg = x['background']
    if isinstance(bg, basestring):
        assert re.search(r'#[a-fA-F0-9]{6}', bg)
        r, g, b, a = [int(bg[i:i + 2], 16) for i in [1, 3, 5]] + [255]
    else:
        r, g, b, a = bg
    backgroundRgba = [r, g, b, a]
    
    # Load images and find their dimensions
    imgs = []
    for url in x['images']:
        data = getDataFromUrl(url)
        img = imgFromData(data)
        w, h = dimOfImg(img)
        imgs.append({
            'w': w,
            'h': h,
            'url': url,
            'data': data,
            'img': img,
        })
    
    # Choose a layout. This is a trivial stub for now.
    # It just concatenates vertically.
    layout = {}
    y = 0
    for img in imgs:
        layout[img['url']] = [0, y, img['w'], img['h']]
        y += img['h']
    
    # Build the sprite
    optipngLevel = int(x['optipng']) if 'optipng' in x else None
    png = buildSprite(backgroundRgba, imgs, layout, optipngLevel=optipngLevel)
    
    return {
        "png_64": base64.b64encode(png),
        "layout": layout,
    }


#<pre>{
#    "png_64": "...",
#    "layout": {
#        "file://...": [x, y, w, h],
#    }
#}
#{
#    "html": "..."
#}</pre>
def spriteHtmlViz(x):
    
    raise NotImplementedError
    
    return {
        
    }

