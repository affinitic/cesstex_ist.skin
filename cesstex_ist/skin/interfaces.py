# -*- coding: utf-8 -*-
"""
cesstex_ist.skin

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer


class IAgendaPortlet(Interface):
    """
    Interface pour le portlet agenda
    """
