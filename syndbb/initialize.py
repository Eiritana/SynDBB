#
# Copyright (c) 2017 by faggqt (https://faggqt.pw). All Rights Reserved.
# You may use, distribute and modify this code under the QPL-1.0 license.
# The full license is included in LICENSE.md, which is distributed as part of this project.
#

import syndbb, logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
from time import strftime
import traceback
# import bs4, functools, htmlmin

# Core Pages
import syndbb.views.basic

# User Pages
import syndbb.views.auth
import syndbb.views.invites
import syndbb.views.profile

# Forums, upload, pastebin, store
import syndbb.views.forums
import syndbb.views.events
import syndbb.views.store
import syndbb.views.upload
import syndbb.views.pastebin
import syndbb.views.quotedb
import syndbb.views.emoticons

# Management
import syndbb.views.admin

# Miscellaneous
import syndbb.views.irc_api
import syndbb.views.xml_feed

# def prettify(route_function):
#     @functools.wraps(route_function)
#     def wrapped(*args, **kwargs):
#         yielded_html = route_function(*args, **kwargs)
#         soup = bs4.BeautifulSoup(yielded_html, 'html.parser')
#         return soup.prettify()
#
#     return wrapped
#
# def uglify(route_function):
#     @functools.wraps(route_function)
#     def wrapped(*args, **kwargs):
#         yielded_html = route_function(*args, **kwargs)
#         minified_html = htmlmin.minify(yielded_html)
#         return minified_html
#
#     return wrapped
#
# if syndbb.app.debug:
#     syndbb.render_template = prettify(syndbb.render_template)
# else:
#     syndbb.render_template = uglify(syndbb.render_template)

#Error Logging (when not in debug mode)
if not syndbb.app.debug:
    global_log = "logs/global.log"
    summary_log = "logs/summary.log"
    log_size = 2097152
    logger = logging.getLogger('werkzeug')
    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')

    logging.basicConfig(format = logFormatStr, filename = global_log, level=logging.DEBUG)
    access_handler = RotatingFileHandler(global_log, maxBytes=log_size, backupCount=5)

    fileHandler = RotatingFileHandler(summary_log, maxBytes=log_size, backupCount=5)
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)

    logger.addHandler(access_handler)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    @syndbb.app.after_request
    def after_request(response):
        timestamp = strftime('%Y-%b-%d %H:%M:%S')
        useragent = request.user_agent
        logger.info('[%s] [%s] [%s] [%s] [%s] [%s] [%s] [%s]',
            timestamp, request.remote_addr, useragent, request.method,
            request.scheme, request.full_path, response.status, request.referrer)
        return response

    @syndbb.app.errorhandler(Exception)
    def exceptions(e):
        tb = traceback.format_exc()
        timestamp = strftime('[%Y-%b-%d %H:%M]')
        logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
            timestamp, request.remote_addr, request.method,
            request.scheme, request.full_path, tb)
        return e.status_code

#Run the main app...
if __name__ == '__main__':
    syndbb.app.run(threaded=True)
