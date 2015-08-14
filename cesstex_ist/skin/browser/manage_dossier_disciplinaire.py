# -*- coding: utf-8 -*-

#import datetime
#import time
#import random
import os
from sqlalchemy import desc
from mailer import Mailer
#from LocalFS import LocalFS
from Products.Five import BrowserView
from zope.interface import implements
from zope.component import getMultiAdapter
from z3c.sqlalchemy import getSAWrapper
#from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from Products.CMFPlone.utils import normalizeString
from Products.CMFCore.utils import getToolByName
#from Products.CMFPlone import PloneMessageFactory as _
#from Products.AddRemoveWidget.AddRemoveWidget import AddRemoveWidget
#from Products.Archetypes.atapi import LinesField
#from Products.Archetypes.Renderer import renderer
#from Products.Archetypes.atapi import BaseContent
from interfaces import IManageDossierDisciplinaire
#from collective.captcha.browser.captcha import Captcha
from cesstex.db.pgsql.baseTypes import Etudiant, \
                                       Professeur, \
                                       DossierDisciplinaire, \
                                       EvenementActe, \
                                       EvenementActeDocument, \
                                       EtatPublication, \
                                       EvenementActeLogModification, \
                                       LogOperation


class ManageDossierDisciplinaire(BrowserView):
    implements(IManageDossierDisciplinaire)

#### ENVOI DES MAILS ####
    def sendMail(self, sujet, message, destinataires):
        """
        envoi de mail à clpsbw admin
        """
        mailer = Mailer("localhost", "alain.meurant@affinitic.be")
        mailer.setSubject(sujet)
        mailer.setRecipients(destinataires)
        mail = message
        #print mail
        mailer.sendAllMail(mail)

    def sendMailForNewDossier(self, elevePk):
        """
        envoi d'un mail lors de la création d'un nouveau dossier disciplinaire
        """
        eleve = self.getElevesByPk(elevePk)
        destinataires = ''

        if eleve.titulaire01:
            destinataires = eleve.titulaire01.prof_email + ','
            titulaire01 = '%s %s' % (eleve.titulaire01.prof_prenom, eleve.titulaire01.prof_nom)
        else:
            titulaire01 = ' - '
        if eleve.titulaire02:
            destinataires = destinataires + eleve.titulaire02.prof_email + ','
            titulaire02 = '%s %s' % (eleve.titulaire02.prof_prenom, eleve.titulaire02.prof_nom)
        else:
            titulaire02 = ' - '
        if eleve.educateurReferent:
            destinataires = destinataires + eleve.educateurReferent.prof_email + ','
            educateurReferent = '%s %s' % (eleve.educateurReferent.prof_prenom, eleve.educateurReferent.prof_nom)
        else:
            educateurReferent = ' - '
        destinataires = destinataires + 'j.montero@saintemarielalouviere.be' + ',' + 'c.bocquet@saintemarielalouviere.be' + ','
        destinataires = destinataires + 'alain.meurant@affinitic.be'

        portalUrl = getToolByName(self.context, 'portal_url')()
        urlDossier = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-evenement-au-dossier?elevePk=%s" % (portalUrl, elevePk)

        sujet = "[ISM  :: dossier disciplinaire]"
        message = u"""<font color='#FF0000'><b>:: Ajout d'un nouveau dossier disciplinaire ::</b></font><br /><br />
                      Bonjour, <br />
                      Un nouveau dossier disciplinaire vient d'être créé.<br />
                      Il s'agit de l'étudiant:<br />
                      <ul>
                        <li>Nom : <font color='#ff9c1b'><b>%s</b></font></li>
                        <li>Prénom : <font color='#ff9c1b'><b>%s</b></font></li>
                        <li>Classe :  <font color='#ff9c1b'><b>%s</b></font></li>
                        <li>Titutlaire 1 : <font color='#ff9c1b'><b>%s </b></font></li>
                        <li>Titutlaire 2 : <font color='#ff9c1b'><b>%s </b></font></li>
                        <li>Educateur : <font color='#ff9c1b'><b>%s </b></font></li>
                      </ul>
                      <hr />
                      Le dossier est accessible en cliquant <a href="%s">ici</a>
                   """ % (eleve.eleve_nom, \
                          eleve.eleve_prenom, \
                          eleve.eleve_classe, \
                          titulaire01, \
                          titulaire02, \
                          educateurReferent, \
                          urlDossier)
        self.sendMail(sujet, message.encode('utf-8'), destinataires)

    def sendMailForNewEvenementActe(self, elevePk):
        """
        envoi d'un mail lors de la création d'un nouvel événement acté
        """
        eleve = self.getElevesByPk(elevePk)
        destinataires = ''

        if eleve.titulaire01:
            destinataires = eleve.titulaire01.prof_email + ','
            titulaire01 = '%s %s' % (eleve.titulaire01.prof_prenom, eleve.titulaire01.prof_nom)
        else:
            titulaire01 = ' - '
        if eleve.titulaire02:
            destinataires = destinataires + eleve.titulaire02.prof_email + ','
            titulaire02 = '%s %s' % (eleve.titulaire02.prof_prenom, eleve.titulaire02.prof_nom)
        else:
            titulaire02 = ' - '
        if eleve.educateurReferent:
            destinataires = destinataires + eleve.educateurReferent.prof_email + ','
            educateurReferent = '%s %s' % (eleve.educateurReferent.prof_prenom, eleve.educateurReferent.prof_nom)
        else:
            educateurReferent = ' - '
        destinataires = destinataires + 'j.montero@saintemarielalouviere.be' + ',' + 'c.bocquet@saintemarielalouviere.be' + ','
        destinataires = destinataires + 'alain.meurant@affinitic.be'

        portalUrl = getToolByName(self.context, 'portal_url')()
        urlDossier = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-evenement-au-dossier?elevePk=%s" % (portalUrl, elevePk)
        sujet = "[ISM  :: dossier disciplinaire]"
        message = u"""<font color='#FF0000'><b>:: Ajout d'un nouvel événement acté ::</b></font><br /><br />
                      Bonjour, <br />
                      Un nouvel événement acté vient d'être ajouté au dossier de
                      l'étudiant:<br />
                      <ul>
                        <li>Nom : <font color='#ff9c1b'><b>%s</b></font></li>
                        <li>Prénom : <font color='#ff9c1b'><b>%s</b></font></li>
                        <li>Classe :  <font color='#ff9c1b'><b>%s</b></font></li>
                        <li>Titutlaire 1 : <font color='#ff9c1b'><b>%s </b></font></li>
                        <li>Titutlaire 2 : <font color='#ff9c1b'><b>%s </b></font></li>
                        <li>Edicateur : <font color='#ff9c1b'><b>%s </b></font></li>
                      </ul>
                      <hr />
                      Le dossier est accessible en cliquant <a href="%s">ici</a>
                   """ % (eleve.eleve_nom, \
                          eleve.eleve_prenom, \
                          eleve.eleve_classe, \
                          titulaire01, \
                          titulaire02, \
                          educateurReferent, \
                          urlDossier)
        self.sendMail(sujet, message.encode('utf-8'), destinataires)

    def sendMailForModyfingEvenementActe(self, elevePk):
        """
        envoi d'un mail lors de la création d'un nouvel événement acté
        """
        eleve = self.getElevesByPk(elevePk)
        destinataires = ''
        if eleve.titulaire01:
            destinataires = eleve.titulaire01.prof_email + ','
            titulaire01 = '%s %s' % (eleve.titulaire01.prof_prenom, eleve.titulaire01.prof_nom)
        else:
            titulaire01 = ' - '
        if eleve.titulaire02:
            destinataires = destinataires + eleve.titulaire02.prof_email + ','
            titulaire02 = '%s %s' % (eleve.titulaire02.prof_prenom, eleve.titulaire02.prof_nom)
        else:
            titulaire02 = ' - '
        if eleve.educateurReferent:
            destinataires = destinataires + eleve.educateurReferent.prof_email + ','
            educateurReferent = '%s %s' % (eleve.educateurReferent.prof_prenom, eleve.educateurReferent.prof_nom)
        else:
            educateurReferent = ' - '
        destinataires = destinataires + 'j.montero@saintemarielalouviere.be' + ',' + 'c.bocquet@saintemarielalouviere.be' + ','
        destinataires = destinataires + 'alain.meurant@affinitic.be'

        portalUrl = getToolByName(self.context, 'portal_url')()
        urlDossier = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-evenement-au-dossier?elevePk=%s" % (portalUrl, elevePk)
        sujet = "[ISM  :: dossier disciplinaire]"
        message = u"""<font color='#FF0000'><b>:: Modification d'un événement acté ::</b></font><br /><br />
                      Bonjour, <br />
                      Un événement acté vient d'être modifié dans le dossier de
                      l'étudiant:<br />
                      <ul>
                        <li>Nom : <font color='#ff9c1b'><b>%s</b></font></li>
                        <li>Prénom : <font color='#ff9c1b'><b>%s</b></font></li>
                        <li>Classe :  <font color='#ff9c1b'><b>%s</b></font></li>
                        <li>Titutlaire 1 : <font color='#ff9c1b'><b>%s </b></font></li>
                        <li>Titutlaire 2 : <font color='#ff9c1b'><b>%s </b></font></li>
                        <li>Edicateur : <font color='#ff9c1b'><b>%s </b></font></li>
                      </ul>
                      <hr />
                      Le dossier est accessible en cliquant <a href="%s">ici</a>
                   """ % (eleve.eleve_nom, \
                          eleve.eleve_prenom, \
                          eleve.eleve_classe, \
                          titulaire01, \
                          titulaire02, \
                          educateurReferent, \
                          urlDossier)
        self.sendMail(sujet, message.encode('utf-8'), destinataires)


#### ETAT PUBLICATION ####
    def getAllEtatPublication(self):
        """
        recuperation de tous les états de publication (privé, visible membre)
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EtatPublication)
        query = query.order_by(EtatPublication.etat_titre)
        allEtatPublication = query.all()
        return allEtatPublication


#### PROFESSEURS ####
    def getAllProfesseurs(self, statutProf, ecole):
        """
        recuperation de tous les professseurs
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Professeur)
        query = query.filter(Professeur.prof_ecole_fk == ecole)
        query = query.filter(Professeur.prof_statut_fk == statutProf)
        query = query.order_by(Professeur.prof_nom)
        allProfesseurs = query.all()
        return allProfesseurs

    def getProfesseurByLogin(self, loginProf):
        """
        recuperation de tous les professseurs
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Professeur)
        query = query.filter(Professeur.prof_login == loginProf)
        professeur = query.one()
        return professeur

    def getProfesseurByPk(self, profPk):
        """
        recuperation du prof selon sa Pk
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Professeur)
        query = query.filter(Professeur.prof_pk == profPk)
        professeur = query.one()
        return professeur

    def getAuteurPk(self):
        ismTools = getMultiAdapter((self.context, self.request), name="manageISM")
        loginProf = ismTools.getUserAuthenticated()
        professeur = self.getProfesseurByLogin(loginProf)
        professeurPk = professeur.prof_pk
        return professeurPk


#### ELEVES ####
    def getAllEleves(self):
        """
        recuperation de tous les élèves qui ont un dossier disciplinaire
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Etudiant)
        query = query.order_by(Etudiant.eleve_nom)
        allEleves = query.all()
        return allEleves

    def getElevesByPk(self, elevePk=None):
        """
        recuperation d'un élève selon sa pk
        """
        if not elevePk:
            fields = self.request.form
            elevePk = fields.get('elevePk', None)

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Etudiant)
        query = query.filter(Etudiant.eleve_pk == elevePk)
        eleveByPk = query.one()
        return eleveByPk

    def getEleveByLeffeSearch(self, searchString):
        """
        table pg etudiant
        recuperation d'une eleve via le livesearch
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Etudiant)
        query = query.filter(Etudiant.eleve_nom.ilike("%%%s%%" % searchString))
        query = query.order_by(Etudiant.eleve_nom)
        for elem in query.all():
            anneeDossier = elem.dossierEleve[0].dosdis_annee_scolaire
            classeEleve = elem.eleve_classe
            if elem.dossierEleve[0].dosdis_actif == True:
                etatDossier = "Actif"
            if elem.dossierEleve[0].dosdis_actif == False:
                etatDossier = "Inactif"
        eleve = ["%s, %s - [%s - %s - %s]" % ((elem.eleve_nom).upper(), elem.eleve_prenom, classeEleve, anneeDossier, etatDossier) for elem in query.all()]
        return eleve

    def getSearchingEleve(self, elevePk=None):
        """
        table pg eleve
        recuperation d'un auteur selon la pk
        la pk peut arriver via le form en hidden ou via un lien construit,
         (cas du listing de resultat de moteur de recherche)
        je teste si la pk arrive par param, si pas je prends celle du form
        """
        fields = self.request.form
        eleveNom = fields.get('eleveNom', None)

        if not elevePk:
            elevePk = fields.get('eleve_pk')

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Etudiant)
        if eleveNom:
            eleveNom = eleveNom.split(',')
            eleveNom = eleveNom[0]
            eleveNom = eleveNom.decode('utf-8')
            query = query.filter(Etudiant.eleve_nom == eleveNom)
        if elevePk:
            query = query.filter(Etudiant.eleve_pk == elevePk)
        allEleves = query.all()
        return allEleves

    def insertEleve(self):
        """
        insère un nouvel élève dans la table etudaint
        insère un nouveau dossier dans la table dossier liè à cet élève
        """
        fields = self.request.form

        eleveNom = fields.get('nomEleve', None)
        elevePrenom = fields.get('prenomEleve', None)
        eleveClasse = fields.get('classeEleve', None)
        titulaire01Pk = fields.get('titulaire01Pk', None)
        titulaire02Pk = fields.get('titulaire02Pk', None)
        educateurReferent = fields.get('educateurReferent', None)
        auteurPk = self.getAuteurPk()

        if not titulaire02Pk:
            titulaire02Pk = None

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        newEntry = Etudiant(eleve_nom=eleveNom,
                            eleve_prenom=elevePrenom,
                            eleve_classe=eleveClasse,
                            eleve_prof_titulaire_01_fk=titulaire01Pk,
                            eleve_prof_titulaire_02_fk=titulaire02Pk,
                            eleve_educateur_referent_fk=educateurReferent)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)
        elevePk = newEntry.eleve_pk

        self.insertDossier(elevePk, eleveNom, eleveClasse)

        self.insertLogOperation('insertEleve', auteurPk)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le nouveau dossier concernant l'élève %s  a bien été créé !" % (eleveNom)
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-dossier-disciplinaire" % (portalUrl)
        self.request.response.redirect(url)
        return ''

    def updateEleve(self):
        """
        mise à jour des données d'un élève dans la table etudaint
        """
        fields = self.request.form

        elevePk = fields.get('elevePk', None)
        eleveNom = fields.get('nomEleve', None)
        elevePrenom = fields.get('prenomEleve', None)
        eleveClasse = fields.get('classeEleve', None)
        titulaire01Pk = fields.get('titulaire01Pk', None)
        titulaire02Pk = fields.get('titulaire02Pk', None)
        educateurReferent = fields.get('educateurReferent', None)
        auteurPk = self.getAuteurPk()

        if not titulaire02Pk:
            titulaire02Pk = None

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Etudiant)
        query = query.filter(Etudiant.eleve_pk == elevePk)
        eleve = query.one()
        eleve.eleve_nom = unicode(eleveNom, 'utf-8')
        eleve.eleve_prenom = unicode(elevePrenom, 'utf-8')
        eleve.eleve_classe = unicode(eleveClasse, 'utf-8')
        eleve.eleve_prof_titulaire_01_fk = titulaire01Pk
        eleve.eleve_prof_titulaire_02_fk = titulaire02Pk
        eleve.eleve_educateur_referent_fk = educateurReferent

        session.flush()

        self.insertLogOperation('updateEleve', auteurPk)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le dossier concernant l'élève %s  a bien été modifié !" % (eleveNom)
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-dossier-disciplinaire" % (portalUrl)
        self.request.response.redirect(url)
        return ''

    def deleteEleve(self, elevePk=None):
        """
        suppression d'un eleve dans la table etudiant
        """
        if not elevePk:
            fields = self.request.form
            elevePk = fields.get('elevePk')

        auteurPk = self.getAuteurPk()

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Etudiant)
        query = query.filter(Etudiant.eleve_pk == elevePk)
        eleve = query.one()
        session.delete(eleve)
        session.flush()

        self.insertLogOperation('deleteEleve', auteurPk)

        return ''



#### DOSSIERS DISCIPLINAIRES ####
    def getDossierId(self, elevePk, eleveNom, eleveClasse):
        """
        genere une id de dossier
        """
        ismTools = getMultiAdapter((self.context, self.request), name="manageISM")
        num = ismTools.getTimeStamp()
        dossierId = "ISM-%s-%s-%s-%s" % (elevePk, eleveNom, eleveClasse, num)
        return dossierId


    def getAllDossiers(self):
        """
        recuperation de tous les dossiers disciplinaires
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(DossierDisciplinaire)
        allDossiers = query.one()
        return allDossiers

    def getDossierByEleve(self, elevePk):
        """
        recuperation du dossier disciplinaire d'un student
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(DossierDisciplinaire)
        query = query.filter(DossierDisciplinaire.dosdis_eleve_fk == elevePk)
        dossierEleve = query.one()
        return dossierEleve

    def insertDossier(self, elevePk, eleveNom, eleveClasse):
        """
        insère un nouveau dossier disciplinaire
        """
        ismTools = getMultiAdapter((self.context, self.request), name="manageISM")
        dossierDisciplianireID = self.getDossierId(elevePk, eleveNom, eleveClasse)
        dossierDisciplianireAnneeScolaire = ismTools.getAnneeCourante()
        dossierDisciplianireElevePk = elevePk
        auteurPk = self.getAuteurPk()

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        newEntry = DossierDisciplinaire(dosdis_id=dossierDisciplianireID,
                                        dosdis_annee_scolaire=dossierDisciplianireAnneeScolaire,
                                        dosdis_actif=True,
                                        dosdis_eleve_fk=dossierDisciplianireElevePk,
                                        dosdis_auteur_fk=auteurPk)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)
        dossierDisciplinairePk = newEntry.dosdis_pk

        self.insertLogOperation('insertDossier', auteurPk, dossierDisciplinairePk)

        self.sendMailForNewDossier(elevePk)

        return ''

    def deleteDossierDisciplinaire(self):
        """
        Supprimer un dossier disciplinaire et ses event actés
        """
        fields = self.request.form

        dossierDisciplinairePk = fields.get('dossierDisciplinairePk')
        elevePk = fields.get('elevePk')
        #evenementActePk = fields.get('evenementActePk', None)
        auteurPk = self.getAuteurPk()

        self.deleteEvenementActeByDossierDisciplinaire(dossierDisciplinairePk)
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(DossierDisciplinaire)
        query = query.filter(DossierDisciplinaire.dosdis_pk == dossierDisciplinairePk)
        dossierDisciplinaire = query.one()
        session.delete(dossierDisciplinaire)
        session.flush()
        self.deleteEleve(elevePk)

        self.insertLogOperation('deleteDossierDisciplinaire', auteurPk, dossierDisciplinairePk)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le dossier disciplinaire et les événements qui lui sont liés ont bien été supprimés !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-dossier-disciplinaire" % (portalUrl)
        self.request.response.redirect(url)
        return ''

#### EVENEMENTS ACTES POUR UN DOSSIER ####
    def getAllEvenementByDossier(self, dossierDisciplinairePk):
        """
        recuperation de tous événements actés pour un dossier disciplinaire
        d'un élève
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActe)
        query = query.filter(EvenementActe.eventact_dossier_diciplinaire_fk == dossierDisciplinairePk)
        query = query.order_by(desc(EvenementActe.eventact_date_creation))
        AllEvenements = query.all()
        return AllEvenements

    def getEvenementByPk(self, evenementActePk):
        """
        recuperation d'un événement acté szlon sa pk
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActe)
        query = query.filter(EvenementActe.eventact_pk == evenementActePk)
        evenementActe = query.one()
        return evenementActe

    def getNombreEvenementActeByDossier(self, dossierDisciplinairePk):
        """
        Somme de tous les evenements actes pour un dossier
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActe)
        query = query.filter(EvenementActe.eventact_dossier_diciplinaire_fk == dossierDisciplinairePk)
        evenementActe = query.all()
        nombreEvenementActe = len(evenementActe)
        return nombreEvenementActe

    def getNombreEvenementActeByEleve(self, eleveDossierPk):
        """
        Somme de tous les evenements actes pour un élève
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActe)
        query = query.filter(EvenementActe.eventact_dossier_diciplinaire_fk == eleveDossierPk)
        evenementActe = query.all()
        nombreEvenementActe = len(evenementActe)
        return nombreEvenementActe


    def insertEvenementActe(self):
        """
        insère un nouveau dossier disciplinaire
        """
        fields = self.request.form

        elevePk = fields.get('elevePk')
        evenement = fields.get('evenement', None)
        sanction = fields.get('sanction', None)
        intervenant = fields.get('intervenant', None)
        etatPublication = fields.get('etatPublication', None)
        dossierDisciplinairePk = fields.get('dossierDisciplinairePk', None)
        evenementActeDocument = fields.get('fichierAttache', None)
        auteurPk = self.getAuteurPk()

        #donne un numero d'ordre d'affichage a l'event
        nombreEvenementActeDossier = self.getNombreEvenementActeByDossier(dossierDisciplinairePk)
        evenementNumeroOrdre = nombreEvenementActeDossier + 1

        if evenementActeDocument:
            eventactDocumentAttache = True
        else:
            eventactDocumentAttache = False

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        newEntry = EvenementActe(eventact_evenement=evenement,
                                 eventact_sanction=sanction,
                                 eventact_intervenant=intervenant,
                                 eventact_etat_publication_fk=etatPublication,
                                 eventact_document_attache=eventactDocumentAttache,
                                 eventact_numero_ordre=evenementNumeroOrdre,
                                 eventact_auteur_creation_fk=auteurPk,
                                 eventact_dossier_diciplinaire_fk=dossierDisciplinairePk)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)
        evenementActePk = newEntry.eventact_pk

        if evenementActeDocument:
            self.addEvenementActeDocument(evenementActePk, dossierDisciplinairePk)

        if int(etatPublication) == 2:
            self.sendMailForNewEvenementActe(elevePk)

        self.insertLogOperation('insertEvenementActe', auteurPk, dossierDisciplinairePk, evenementActePk)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le nouvel événement a bien été ajouté !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-evenement-au-dossier?elevePk=%s" % (portalUrl, elevePk)
        self.request.response.redirect(url)
        return ''

    def updateEvenementActe(self):
        """
        Updates un événement acté lié à un dossier
        """
        fields = self.request.form
        elevePk = fields.get('elevePk')
        evenementActePk = fields.get('evenementActePk', None)
        evenement = fields.get('evenement', None)
        sanction = fields.get('sanction', None)
        intervenant = fields.get('intervenant', None)
        dossierDisciplinairePk = fields.get('dossierDisciplinairePk', None)
        etatPublication = fields.get('etatPublication', None)
        auteurPk = self.getAuteurPk()


        fields = self.context.REQUEST
        evenementActeDocument = getattr(fields, 'fichierAttache', None)
        if evenementActeDocument:
            eventactDocumentAttache = True
            self.addEvenementActeDocument(evenementActePk, dossierDisciplinairePk)
        else:
            nombreEvenementActeDocument = self.getEvenementActeDocumentByEventActPk(evenementActePk)
            if nombreEvenementActeDocument > 1:
                eventactDocumentAttache = True
            else:
                eventactDocumentAttache = False

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActe)
        query = query.filter(EvenementActe.eventact_pk == evenementActePk)
        evenementActe = query.one()
        evenementActe.eventact_evenement = unicode(evenement, 'utf-8')
        evenementActe.eventact_sanction = unicode(sanction, 'utf-8')
        evenementActe.eventact_intervenant = unicode(intervenant, 'utf-8')
        evenementActe.eventact_document_attache = eventactDocumentAttache,
        evenementActe.eventact_etat_publication_fk = etatPublication
        session.flush()

        self.insertLogOperation('updateEvenementActe', auteurPk, dossierDisciplinairePk, evenementActePk)

        self.insertLogModificationEvenementActe(evenementActePk)

        if int(etatPublication) == 2:
            self.sendMailForModyfingEvenementActe(elevePk)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"L'événement a bien été modifié !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-evenement-au-dossier?elevePk=%s" % (portalUrl, elevePk)
        self.request.response.redirect(url)
        return ''

    def deleteEvenementActe(self):
        """
        Supprimer un événement acté lié à un dossier
        """
        fields = self.request.form

        elevePk = fields.get('elevePk')
        evenementActePk = fields.get('evenementActePk', None)
        dossierDisciplinairePk = fields.get('dossierDisciplinairePk', None)
        auteurPk = self.getAuteurPk()

        self.deleteLogModificationEvenementActe()
        self.deleteAllEvenementActeDocumentByEvenementPk()

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActe)
        query = query.filter(EvenementActe.eventact_pk == evenementActePk)
        evenementActe = query.one()
        session.delete(evenementActe)
        session.flush()

        self.insertLogOperation('deleteEvenementActe', auteurPk, dossierDisciplinairePk, evenementActePk)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"L'événement a bien été supprimé !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-evenement-au-dossier?elevePk=%s" % (portalUrl, elevePk)
        self.request.response.redirect(url)
        return ''

    def deleteEvenementActeByDossierDisciplinaire(self, dossierDisciplinairePk):
        """
        Supprimer les événements actés lié à un dossier
        """
        self.deleteLogModificationEvenementActe()
        self.deleteAllEvenementActeDocumentByDossierDisciplinairePk()

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActe)
        query = query.filter(EvenementActe.eventact_dossier_diciplinaire_fk == dossierDisciplinairePk)
        allEvenementsActes = query.all()
        for evenementActe in allEvenementsActes:
            evenementActePk = evenementActe.eventact_pk
            self.deleteLogModificationEvenementActe(evenementActePk)
            session.delete(evenementActe)
        session.flush()

        auteurPk = self.getAuteurPk()
        self.insertLogOperation('deleteEvenementActeByDossierDisciplinaire', auteurPk, dossierDisciplinairePk)
        return ''


#### GESTION DES DOCUMENTS ATTACHES ####
    def getAllEvenementActeDocument(self):
        """
        table pg evenement_acte_document
        recuperation de tous les document d'un evenement acte
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActeDocument)
        return query.all()

    def getEvenementActeDocumentByEventActPk(self, evenementPk):
        """
        table pg evenement_acte_document
        recuperation des catalogues PDF d'un operateur
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActeDocument)
        query = query.filter(EvenementActeDocument.eventactdoc_eventact_fk == evenementPk)
        return query.all()

    def addEvenementActeDocument(self, evenementActePk, dossierDisciplinairePk):
        """
        ajout d'un fichier dans le localfs 'localfs_ism_event_act'
        comme document lié à une eventment acte
        """
        ismTools = getMultiAdapter((self.context, self.request), name="manageISM")
        dateCreation = ismTools.getTimeStamp()
        auteurPk = self.getAuteurPk()

        fields = self.context.REQUEST
        evenementActeDocument = getattr(fields, 'fichierAttache')
        dossierDisciplinairePk = getattr(fields, 'dossierDisciplinairePk')

        lfsEventActe = getattr(self.context, 'localfs_ism_event_act')
        lfs = getattr(lfsEventActe, 'localfs_ism_event_act')
        filename, ext = os.path.splitext(evenementActeDocument.filename)
        normalizedFilename = normalizeString(filename, encoding='utf-8')
        nomFichier = '%s_dd%s_ev%s%s' % (normalizedFilename, dossierDisciplinairePk, evenementActePk, ext)
        lfs.manage_upload(evenementActeDocument, id=nomFichier)

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        newEntry = EvenementActeDocument(eventactdoc_date_creation=dateCreation,
                                         eventactdoc_auteur_creation=auteurPk,
                                         eventactdoc_nom_fichier=nomFichier,
                                         eventactdoc_auteur_creation_fk=auteurPk,
                                         eventactdoc_eventact_fk=evenementActePk,
                                         eventactdoc_dossier_disciplinaire_fk=dossierDisciplinairePk)
        session.add(newEntry)
        session.flush()
        self.insertLogOperation('addEvenementActeDocument', auteurPk, dossierDisciplinairePk, evenementActePk)

    def deleteEvenementActeDocumentByDocumentPk(self):
        """
        suppression d'un fichier attache a un evenement acte dans la db
        """
        fields = self.context.REQUEST
        fichierNom = getattr(fields, 'fichierNom', None)
        evenementActePk = getattr(fields, 'evenementActePk', None)
        documentPk = getattr(fields, 'documentPk', None)
        elevePk = getattr(fields, 'elevePk', None)
        dossierDisciplinaire = self.getDossierByEleve(elevePk)
        dossierDisciplinairePk = dossierDisciplinaire.dosdis_pk
        auteurPk = self.getAuteurPk()

        #suppression dans la table evenement_acte_document
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActeDocument)
        query = query.filter(EvenementActeDocument.eventactdoc_pk == documentPk)
        document = query.one()
        session.delete(document)
        session.flush()

        self.insertLogOperation('deleteEvenementActeDocumentFromDb', auteurPk, dossierDisciplinairePk, evenementActePk)
        self.deleteEvenementActeDocumentFromLfs(fichierNom, auteurPk, dossierDisciplinairePk, evenementActePk)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le pdf a bien été suprimé !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-evenement-au-dossier?elevePk=%s" % (portalUrl, elevePk)
        self.request.response.redirect(url)
        return ''

    def deleteAllEvenementActeDocumentByEvenementPk(self):
        """
        suppression des fichiers attaches a un evenement acte dans Db et LFS
        """
        fields = self.context.REQUEST
        evenementActePk = getattr(fields, 'evenementActePk', None)
        elevePk = getattr(fields, 'elevePk', None)
        dossierDisciplinaire = self.getDossierByEleve(elevePk)
        dossierDisciplinairePk = dossierDisciplinaire.dosdis_pk
        auteurPk = self.getAuteurPk()

        #suppression dans la table evenement_acte_document
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActeDocument)
        query = query.filter(EvenementActeDocument.eventactdoc_eventact_fk == evenementActePk)
        documents = query.all()

        for doc in documents:
            session.delete(doc)
            fichierNom = doc.eventactdoc_nom_fichier
            self.deleteEvenementActeDocumentFromLfs(fichierNom, auteurPk, dossierDisciplinairePk, evenementActePk)
        session.flush()
        return ''

    def deleteAllEvenementActeDocumentByDossierDisciplinairePk(self):
        """
        suppression des fichiers attachs a un dossier dans Db et LFS
        """
        fields = self.context.REQUEST
        evenementActePk = getattr(fields, 'evenementActePk', None)
        elevePk = getattr(fields, 'elevePk', None)
        dossierDisciplinaire = self.getDossierByEleve(elevePk)
        dossierDisciplinairePk = dossierDisciplinaire.dosdis_pk
        auteurPk = self.getAuteurPk()

        #suppression dans la table evenement_acte_document
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActeDocument)
        query = query.filter(EvenementActeDocument.eventactdoc_dossier_disciplinaire_fk == dossierDisciplinairePk)
        documents = query.all()

        for doc in documents:
            session.delete(doc)
            fichierNom = doc.eventactdoc_nom_fichier
            self.deleteEvenementActeDocumentFromLfs(fichierNom, auteurPk, dossierDisciplinairePk, evenementActePk)
        session.flush()
        return ''

    def deleteEvenementActeDocumentFromLfs(self, fichierNom, auteurPk, dossierDisciplinairePk, evenementActePk):
        """
        suppression d'un fichier attache a un evenement acte dans le localfs 'localfs_ism_event_act'
        """
        lfsEventActe = getattr(self.context, 'localfs_ism_event_act')
        lfs = getattr(lfsEventActe, 'localfs_ism_event_act')
        lfs.manage_delObjects(ids=[fichierNom, ])
        self.insertLogOperation('deleteEvenementActeDocumentFromLfs', auteurPk, dossierDisciplinairePk, evenementActePk)


#### LOG MODIFICATION EVENEMENTS ACTES POUR UN DOSSIER POUR AFFICHAGE HISTORIQUE ####
    def getAllLogModificationForEvenementActe(self, evenementActePk):
        """
        recuperation de tous les logs de modifications pour une événement acté
        pour un dossier disciplinaire d'un élève
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActeLogModification)
        query = query.filter(EvenementActeLogModification.eventactlogmodif_evenement_acte_fk == evenementActePk)
        query = query.order_by(EvenementActeLogModification.eventactlogmodif_date_modification)
        AllLogForEvenement = query.all()
        return AllLogForEvenement

    def insertLogModificationEvenementActe(self, evenementActePk):
        """
        insère un nouveau log pour une modification d'un événement acté
        """

        ismTools = getMultiAdapter((self.context, self.request), name="manageISM")
        auteurConnecte = ismTools.getUserAuthenticated()

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        newEntry = EvenementActeLogModification(eventactlogmodif_auteur_modification=auteurConnecte,
                                                eventactlogmodif_evenement_acte_fk=evenementActePk)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)

        return ''

    def deleteLogModificationEvenementActe(self, evenementActePk=None):
        """
        Supprimer les log de modifications d'un événement acté lors
        de la suppression de cet événement.
        """
        #elevePk = fields.get('elevePk')
        if not evenementActePk:
            fields = self.request.form
            evenementActePk = fields.get('evenementActePk', None)

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActeLogModification)
        query = query.filter(EvenementActeLogModification.eventactlogmodif_evenement_acte_fk == evenementActePk)
        evenementActeLog = query.all()
        for pk in evenementActeLog:
            session.delete(pk)
        session.flush()

        return ''


#### LOG OPERATION SUR DOSSIER ET EVENEMENT ####
    def getAllLogOperation(self):
        """
        recuperation de tous les logs d'operation
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(LogOperation)
        AllLogOperation = query.all()
        return AllLogOperation

    def insertLogOperation(self, logOperationType, auteurPk=None, dossierDisciplinairePk=None, evenementActePk=None):
        """
        insère un nouveau log pour une operation
        """

        ismTools = getMultiAdapter((self.context, self.request), name="manageISM")
        auteurConnecte = ismTools.getUserAuthenticated()

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        newEntry = LogOperation(logoperation_auteur=auteurConnecte,
                                logoperation_type_operation=logOperationType,
                                logoperation_auteur_fk=auteurPk,
                                logoperation_dosdis_fk=dossierDisciplinairePk,
                                logoperation_evenement_acte_fk=evenementActePk)
        session.add(newEntry)
        session.flush()
        return ''
