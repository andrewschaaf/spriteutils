## Status

Just this README committed so far -- I've got a partial implementation which I'll work on and post this weekend.

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

* Prereqs: [ImageMagick](http://www.imagemagick.org/script/index.php),
    [OptiPNG](http://optipng.sourceforge.net/) (optional), Python (2.6) or (2.5 with simplejson)
* Put this repo somewhere on your filesystem
* Optional: add <code>spriteutils/scripts</code> to your <code>PATH</code>

### Future Work

* A very smart layout engine. (The current one is a trivial stub. It just concatenates vertically)

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
            "http://.../register.png",
        ],
    }
}</pre>

## sprite-create

<pre>cat input.json | sprite-create > sprite.json
// input.json
{
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
    "url": "http://..../.../sprite.png",
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
    "sprite_urls": {
        "initial": ".../c1a2245b6b39.png",
        "registration": ".../ea274ffd321f.png",
    }
    "layout": {...see sprite-create...}
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
                background: url("http://artserver:9001/register.png");
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
        background: url("http://artserver:9001/register.png");
        width: 130px;
        height: 36px;
    }
    
    {% endspriteRoot %}

// CSS (after)
...see example input for sprite-replace-css...</pre>

Notes:

* It reads (width, height) from the image file (unless cached)
* <code>from django.core.cache import cache</code> can be used, the spriteutils caches the value <code>{"w":...,"h":...,}</code> with key <code>'spriteutils:url\_utf8\_64:mtime'</code>
* It doesn't support non-local remote files (like register.png), so you have to write that CSS manually



