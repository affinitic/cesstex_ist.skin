# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from zope.interface import implements
from cesstex_ist.skin.browser.interfaces import IIstInoEleveParentPageView
from plone.memoize.instance import memoize


class IstInfoEleveParentPageView(BrowserView):
    """
    gestion de la folderview du dossier IST infos élèves & parents
    """
    implements(IIstInoEleveParentPageView)

    @memoize
    def getPageText(self, pageId):
        page = getattr(self.context, pageId, None)
        if page is None:
            return
        return page.getText()

    def getIstInfoEleveParentTopSection(self):
        """
        recupère le bloc sup de la page
        """
        return self.getPageText('ist_infos_eleves_parents')
