## Status

Not implemented yet:

* sprite-html-viz
* Django tags
* Django example


## Overview

Goal: provide useful spriting tools for

* your build script
* your web app's development mode

So far, this repo consists of four command-line tools:

* <code>sprite-images-from-css</code>
* <code>sprite-create</code>
* <code>sprite-html-viz</code>
* <code>sprite-replace-css</code>

and these language bindings:

* Python: <code>from spriteutils import spriteImagesFromCss, spriteCreate, ...</code>

and these web framework helpers:

* Django tags

### Installing

* Put this repo somewhere on your filesystem
* Optional: add <code>spriteutils/scripts</code> to your <code>PATH</code>
* Prereqs:
[Python Imaging Library](http://www.pythonware.com/products/pil/),
[OptiPNG](http://optipng.sourceforge.net/) (optional),
Python (2.6) or (2.5 with [simplejson](http://pypi.python.org/pypi/simplejson))

    * If you have trouble with PIL, consider doing your work on an Ubuntu VM, SSHFS-mounted via MacFusion ([10.6.3 fix](http://rackerhacker.com/2009/08/28/fix-macfusion-on-snow-leopard/)) or equivalent. It's awesome &mdash; in the long run, you'll avoid many compilation nightmares.

### Future Work

* Find or create a very smart layout engine. (The current one is a trivial stub. It just concatenates vertically)

## sprite-images-from-css

<pre>cat input.json | sprite-images-from-css > output.json
// input.json
{
    "css": "...see sprite-replace-css...",
    "root": "~/.../myapp/images", // probably not in your public static folder
}
// output.json
{
    "sprite_images_map": {
        "initial": [
            "file:///.../signup.png",
            "file:///.../signup_hover.png",
            "file:///.../signup_active.png",
        ],
        "registration": [
            "http://.../register.gif",
        ],
    }
}</pre>

## sprite-create

<pre>cat input.json | sprite-create > sprite.json
// input.json
{
    // Optional optipng level (0-7. 2 is optipng's default and 7 is "very slow").
    // If omitted, optipng will not be used.
    "optipng": 2,
    
    "background": "#......" or [r, g, b, alpha] // 0-255
    "images": [
        "file:///.../landing/signup.png",
        "file:///.../landing/signup_hover.png",
        "file:///.../landing/signup_active.png",
        "http://.../register.gif",
    ],
}
// sprite.json
{
    "png_64": "...",
    "layout": {
        "file:///...signup.png": [0, 0, 120, 36],
        "file:///...signup_hover.png": [0, 36, 120, 36],
        "file:///...signup_active.png": [0, 72, 120, 36],
        "http://...register.gif": [0, 108, 130, 36],
    }
}</pre>

## sprite-html-viz

<pre>cat sprite.json | sprite-html-viz > output.json
// sprite.json
{
    ...see sprite-create...
}
// output.json
{
    /*
        A table of the sprite's images, with each row containing:
            the image (via a base64 data URI)
            the path from the original CSS
                as a "file://..." link to the image
    */
    "html": "..."
}</pre>


## sprite-replace-css

Note that if your app serves /images/... when in development mode, your CSS will work before or after compilation.

<pre>// input.json
{
    "root": "~/.../myapp/images",
    "sprite_urls": {
        "initial": ".../c1a2245b6b39.png",
        "registration": ".../ea274ffd321f.png",
    },
    "layout": {...see sprite-create...},
    "css": "...
            .signup {
                /* SPRITE initial */
                background: url("/images/landing/signup.png");
                width: 120px;
                height: 36px;
            }
            .signup:hover {
                /* SPRITE initial */
                background: url("/images/landing/signup_hover.png");
            }
            .signup:active {
                /* SPRITE initial */
                background: url("/images/landing/signup_active.png");
            }
            .register {
                /* SPRITE registration */
                background: url("http://artserver:9001/register.gif");
                width: 130px;
                height: 36px;
            }
            ..."
}
// output.json
{
    "css": "...
            .signup {
                background: url(".../c1a2245b6b39.png") 0 0;
                width: 120px;
                height: 36px;
            }
            .signup:hover {
                background-position: 0 -36px;
            }
            .signup:active {
                background-position: 0 -72px;
            }
            .register {
                background: url(".../ea274ffd321f.png") 0 -108px;
                width: 130px;
                height: 36px;
            }
            ..."
}</pre>


## Django tags

<pre>// CSS (before)
    
    {% spriteRoot "~/.../images" %}
    
    .signup {
        {% sprite "initial" "/images/landing/signup.png" %}
    }
    .signup:hover {
        {% spritePos "initial" "/images/landing/signup_hover.png" %}
    }
    .signup:active {
        {% spritePos "initial" "/images/landing/signup_active.png" %}
    }
    .register {
        /* SPRITE registration */
        background: url("http://artserver:9001/register.gif");
        width: 130px;
        height: 36px;
    }
    
    {% endspriteRoot %}

// CSS (after)
...see example input for sprite-replace-css...</pre>

Notes:

* It reads (width, height) from the image file (unless cached)
* <code>from django.core.cache import cache</code> can be used, the spriteutils caches the value <code>{"w":...,"h":...,}</code> with key <code>'spriteutils:url\_utf8\_64:mtime'</code>
* It doesn't support non-local remote files (like register.gif), so you have to write that CSS manually



