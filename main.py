#!/usr/bin/env python3
import irc.bot
import irc.strings
import sys, time, datetime, fileinput
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from threading import Thread


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
        m = divmod(d[0], 60)
        h = divmod(m[0], 60)
        dd = divmod(h, 24)
        self.connection.privmsg("#yarc", "Online for: %d days, %d hours, %d minutes and %d seconds" %
                (dd[0],
                 h[1],
                 m[1],
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
    
    def print(self, c, s):
        c.privmsg("#yarc", str(s))

    def command(self, e, ar):
        args = ar.split(" ")
        c = self.connection
        nick = e.source.nick

        if args[0] == "stats":
            self.ponline()
        if args[0] == "eval":
            if nick == "_aika" and nick in self.channels["#yarc"].opers():
                try:
                    r = eval(" ".join(args[1::]))
                    c.privmsg("#yarc", str(r))
                except:
                    pass

bot = YarcBOT()
thr = Thread(target = bot.start, args = ())
thr.start()

for line in fileinput.input():
    r = eval(line)
    print(r)
