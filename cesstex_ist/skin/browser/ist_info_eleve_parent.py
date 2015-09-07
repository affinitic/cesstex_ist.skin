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
        return self.getPageText('edit_ist_infos_eleves_parents_icones_liens_sup')

    def getInfoEleveParentActualiteDuMoment(self):
        """
        recupère le bloc sup de la page
        """
        return self.getPageText('edit_ist_infos_eleves_parents_actualite_moment')

    def getInfoEleveParentActualiteBrevePostIt(self):
        """
        recupère le bloc sup de la page
        """
        return self.getPageText('edit_ist_infos_eleves_parents_post_it')
