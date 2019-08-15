#!/usr/bin/env python3
import irc.bot
import irc.strings
import sys, time, datetime
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

class YarcBOT(irc.bot.SingleServerIRCBot):
    def __init__(self):
        self.nickname = "YARCd"
        self.password = open("./pass", "r").read()
        irc.bot.SingleServerIRCBot.__init__(self, [("irc.freenode.net", 6667)],
                self.nickname, self.nickname)
        self.onlinesince = datetime.datetime.now()

    def ns_login(self):
        self.connection.privmsg("nickserv", "identify %s" % self.password)
        print("Sending password to NickServ")
        time.sleep(1)

    def on_nicknameinuse(self, c, e):
        print("Nickname in use")
        sys.exit(1)

    def ponline(self):
        c = datetime.datetime.now() - self.onlinesince
        d = divmod(c.days * 86400 + c.seconds, 60)
        self.connection.privmsg("#yarc", "Online for: %d days, %d hours, %d minutes and %d seconds" %
                (divmod(d[0], 3600)[0],
                 divmod(d[0], 60)[0],
                 d[0],
                 d[1]))

    def on_welcome(self, c, e):
        self.ns_login()
        print("Joining #yarc")
        c.join("#yarc")
        c.privmsg("#yarc", "OK DR OM")

    def on_privmsg(self, c, e):
        return

    def on_pubmsg(self, c, e):
        n = e.arguments[0].split(":", 1)

        if len(n) > 1 and n[0] == "yd":
            self.command(e, n[1].strip())

    def command(self, e, ar):
        args = ar.split(" ")
        c = self.connection
        nick = e.source.nick

        if args[0] == "stats":
            self.ponline()

YarcBOT().start()
