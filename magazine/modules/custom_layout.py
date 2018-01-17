#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

def navbar(auth_navbar):
    bar = auth_navbar
    user = bar["user"]

    if not user:
        login = A(current.T("Login"),
                  _href=bar["login"],
                  _rel="nofollow")
        return LI(login)
    else:
        logout = A(current.T("Logout %s" % (user)),
                   _href=bar["logout"], 
                   _rel="nofollow")
        return LI(logout)
