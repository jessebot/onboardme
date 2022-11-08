---
layout: default
parent: Python
title: Web Frameworks
description: "Python Web Frameworks"
permalink: /python/web-frameworks
---

# Python and the Web
I try to keep up with the state of python on the web, so here's some basic notes :)

## Flask
[Flask](https://flask.palletsprojects.com/) is tried and true, and a good thing to write your web routes with. It uses jinja templating and it fine. Very stable. I use this for my personal websites all the time.

## Bottle
[bottle](https://bottlepy.org/docs/stable/) is, (according to their website)
> Bottle is a fast, simple and lightweight WSGI micro web-framework for Python. It is distributed as a single file module and has no dependencies other than the Python Standard Library.
> - Routing: Requests to function-call mapping with support for clean and dynamic URLs.
> - Templates: Fast and pythonic built-in template engine and support for mako, jinja2 and cheetah templates.
> - Utilities: Convenient access to form data, file uploads, cookies, headers and other HTTP-related metadata.
> - Server: Built-in HTTP development server and support for paste, fapws3, bjoern, Google App Engine, cherrypy or any other WSGI capable HTTP server.

I used to use bottle all the time, but for a while there, they weren't really updating as much and the python community at large mentioned them less. Flask is also supported out of the box by more cloud app platforms, which is why I switched from it a couple of years ago. Bottle has a special place in my heart though, and the project is active again :)


## Pelican
[Pelican](https://getpelican.com/) is a, (according to their website)...
> static site generator, written in Python. Highlights include:
> - Write your content directly with your editor of choice in reStructuredText or Markdown formats
> - Includes a simple CLI tool to (re)generate your site
> - Easy to interface with distributed version control systems and web hooks
> - Completely static output is easy to host anywhere

I haven't used Pelican since like 2017, but it served me well in the past :shrug: specifically in being incredibly cheap to host on AWS when I worked for a startup that used AWS.

## MkDocs
[MkDocs](https://www.mkdocs.org/) is a, (according to their website)...
> fast, simple and downright gorgeous static site generator that's geared towards building project documentation. Documentation source files are written in Markdown, and configured with a single YAML configuration file. Start by reading the introductory tutorial, then check the User Guide for more information.

I've never used it, but I'm told that [Material for MKDocs](https://squidfunk.github.io/mkdocs-material/) is really good.

## Brython

[Brython](https://brython.info/) is a Python 3 implementation for client-side web programming. I haven't used it, but it seems decently fast.

## PyScript
I should look into [Pyscript.net](https://pyscript.net/), but all the demos are [so slow](https://pyscript.net/examples/), I'm uninterested right now (2022-11-08 10:02:07.0 +0100). According to their website, you can "Run Python in Your HTML".

## Dash by Plotly
[Dash](https://dash.plotly.com/introduction) is actually a python SDK to a Javascript dashboarding framework. According to their website:

> Downloaded 800,000 times per month, Dash is the original low-code framework for rapidly building data apps in Python, R, Julia, and F# (experimental).
> Through a couple of simple patterns, Dash abstracts away all of the technologies and protocols that are required to build a full-stack web app with interactive data visualization.

I've used plotly a bit with python, but have very little work with Dash at this time. It seems nice, but spin up time is not 10 minutes as described in their docs.
