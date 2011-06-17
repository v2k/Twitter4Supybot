###
# Copyright (c) 2011, robbe
#
# needs twitter-1.4.2-py2.5.egg -> http://pypi.python.org/pypi/twitter/1.4.2
# installed and authed appropriately
# Use twglobal only on private ircd server, deprecated on IRCnet for example
#
# 2011-06-17 version 0.10
# 
# Thanks to
# Copyright (c) 2002-2005, Jeremiah Fincher
# Copyright (c) 2009, James Vega
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
###

import os
import subprocess
from datetime import date
import supybot.conf as conf
import supybot.utils as utils
import supybot.world as world
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks


class CdbTwitterDB(object):
    def __init__(self, filename):
        self.dbs = {}
        cdb = conf.supybot.databases.types.cdb
        for service in ['friends','global','replies']:
            dbname = filename.replace('.db', service.capitalize() + '.db')
            self.dbs[service] = cdb.connect(dbname)

    def get(self, service, twitt):
        return self.dbs[service][twitt]

    def set(self, service, twitt, twittID):
        self.dbs[service][twitt] = twittID

    def close(self):
        for service in self.dbs:
            self.dbs[service].close()

    def flush(self):
        for service in self.dbs:
            self.dbs[service].flush()

TwitterDB = plugins.DB('Twitter', {'cdb': CdbTwitterDB})


class Twitter(callbacks.Plugin):
    """This plugin is for accessing a Twitter account"""
    threaded = False
    
    def __init__(self, irc):
        self.__parent = super(Twitter, self)
        self.__parent.__init__(irc)
        self.lastRequest = ""
        self.db = TwitterDB()

    def die(self):
        self.db.close()

    def __call__(self, irc, msg):
        self.__parent.__call__(irc, msg)
        irc = callbacks.SimpleProxy(irc, msg)

    def twversion(self, irc, msg, args):
        """Returns version of this plugin"""
        irc.reply("TwitterPlugin v0.10")

    def twfriends(self, irc, msg, args):
        """takes no arguments
        call cmdline-tool and return a status lines from Twitter->friends
        """
        cmdTwitter =  self.registryValue('command')
        cmdTwitter += ' ' + self.registryValue('optionsF')
        if cmdTwitter:
            args = [cmdTwitter]
            try:
                inst = subprocess.Popen(args, close_fds=True,
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        stdin=file(os.devnull))
            except OSError, e:
                irc.error('It seems the configured twitter command was '
                          'not available.', Raise=True)
            (out, err) = inst.communicate()
            inst.wait()
            lines = out.splitlines()
            lines = map(str.rstrip, lines)
            lines = filter(None, lines)
            neues = []
            for x in lines:
                # for each line in lines, frist try to get the last if exists
                try:
                    last = neues.pop()
                except IndexError:
                    last = ""
                # check timestamp at linestart, append to last if none
                now = date.today()
                if x.startswith(now.strftime('%Y')):
                    if len(last)>0:
                        neues.append(last)
                    neues.append(x)
                else:
                    if len(last)>0:
                        last += ' ' + x
                        neues.append(last)
                    else:
                        irc.error('No Last and no Timestamp-Error', Raise=True)

            # Now store new lines in db to avoid posting dupes
            for x in neues:
                try:
                    twID = self.db.get('friends', x)
                except KeyError:
                    # self.log.debug('friends: line not in db-Cache!')
                    # self.db.set('friends', x, x[0:6] )
                    self.db.set('friends', x, x[5:25] )
                    irc.reply(x)
                    
        else:
            irc.error('The Twitter.twfriends command is not configured. If is '
                      'installed, reconfigure the '
                      'supybot.plugins.Twitter.command and optionsF '
                      'variable appropriately.')


    def twglobal(self, irc, msg, args):
        """takes no arguments
        call cmdline-tool and return a status line from Twitter->global
        """
        cmdTwitter =  self.registryValue('command')
        cmdTwitter += ' ' + self.registryValue('optionsG')
        self.log.debug('twglobal: cmdline %s', cmdTwitter)
        if cmdTwitter:
            args = [cmdTwitter]
            try:
                inst = subprocess.Popen(args, close_fds=True,
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        stdin=file(os.devnull))
            except OSError, e:
                irc.error('It seems the configured twitter command was '
                          'not available.', Raise=True)
            (out, err) = inst.communicate()
            inst.wait()
            lines = out.splitlines()
            lines = map(str.rstrip, lines)
            lines = filter(None, lines)
            neues = []
            for x in lines:
                # for each line in lines, frist try to get the last if exists
                try:
                    last = neues.pop()
                except IndexError:
                    last = ""
                # check timestamp at linestart, append to last if none
                now = date.today()
                if x.startswith(now.strftime('%Y')):
                    if len(last)>0:
                        neues.append(last)
                    neues.append(x)
                else:
                    if len(last)>0:
                        last += ' ' + x
                        neues.append(last)
                    else:
                        irc.error('No Last and no Timestamp-Error', Raise=True)
            # Now store new lines in db to avoid posting dupes
            for x in neues:
                try:
                    twID = self.db.get('global', x)
                except KeyError:
                    # self.log.debug('friends: line not in db-Cache!')
                    self.db.set('friends', x, x[5:25] )
                    irc.reply(x)
                    # irc.reply('\x03'+'11,14'+x)

        else:
            irc.error('The Twitter.twglobal command is not configured. If is '
                      'installed, reconfigure the '
                      'supybot.plugins.Twitter.command and optionsG '
                      'variable appropriately.')


    def twreplies(self, irc, msg, args):
        """takes no arguments
        call cmdline-tool and return a status lines from Twitter->replies
        """
        cmdTwitter =  self.registryValue('command')
        cmdTwitter += ' ' + self.registryValue('optionsR')
        if cmdTwitter:
            args = [cmdTwitter]
            try:
                inst = subprocess.Popen(args, close_fds=True,
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        stdin=file(os.devnull))
            except OSError, e:
                irc.error('It seems the configured twitter command was '
                          'not available.', Raise=True)
            (out, err) = inst.communicate()
            inst.wait()
            lines = out.splitlines()
            lines = map(str.rstrip, lines)
            lines = filter(None, lines)
            neues = []
            for x in lines:
                # for each line in lines, frist try to get the last if exists
                try:
                    last = neues.pop()
                except IndexError:
                    last = ""
                # check timestamp at linestart, append to last if none
                now = date.today()
                if x.startswith(now.strftime('%Y')):
                    if len(last)>0:
                        neues.append(last)
                    neues.append(x)
                else:
                    if len(last)>0:
                        last += ' ' + x
                        neues.append(last)
                    else:
                        irc.error('No Last and no Timestamp-Error', Raise=True)
            # Now store new lines in db to avoid posting dupes
            for x in neues:
                try:
                    twID = self.db.get('replies', x)
                except KeyError:
                    # self.log.debug('friends: line not in db-Cache!')
                    self.db.set('friends', x, x[5:25] )
                    irc.reply(x)

        else:
            irc.error('The Twitter.twreplies command is not configured. If is '
                      'installed, reconfigure the '
                      'supybot.plugins.Twitter.command and optionsR '
                      'variable appropriately.')



Class = Twitter


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
