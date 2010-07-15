import wsgiref.handlers
import cgi
import os
import logging
import datetime
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import mail
#from dateventure import selaus
from dateventure import ilmoitus
from dateventure import ilmoitus_Olens
from dateventure import palaute

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        global ilmoitus_Olen
        if user:
            template_values={

            'Olen': ilmoitus_Olens ,

                "nickname":user.nickname(),
                "url":users.create_logout_url("/")
            }
            theHtmlPage='ilmoitus.html'
        else:
            template_values={
                "loginurl":users.create_login_url("/")
            }
            theHtmlPage='loginPage.html'

        path = os.path.join(os.path.dirname(__file__),theHtmlPage)
        self.response.out.write(template.render(path,template_values))


class Showilmoitus(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        global ilmoitus_Olen
        template_values={
            'Olen': ilmoitus_Olens ,
            "nickname":user.nickname(),
            "url":users.create_logout_url("/")
        }
        path = os.path.join(os.path.dirname(__file__),'ilmoitus.html')
        self.response.out.write(template.render(path,template_values))

class ilmoitusAction (webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        ilmoitusVar = ilmoitus()
        OlenTemp =self.request.get('Olen')
        ilmoitusVar.Olen = self.request.get('Olen')
        PaikkaTemp = self.request.get('Paikka')
        if PaikkaTemp!="":
            ilmoitusVar.Paikka = self.request.get('Paikka')
        P_iv_m_r_Aikatemp = self.request.get('P_iv_m_r_Aika')
        if P_iv_m_r_Aikatemp!="":
            P_iv_m_r_AikaTemp = self.request.get('P_iv_m_r_Aika')
            P_iv_m_r_Aika_res = P_iv_m_r_AikaTemp.split()
            P_iv_m_r_Aika_dt = P_iv_m_r_Aika_res[0]
            P_iv_m_r_Aika_mnth = P_iv_m_r_Aika_res[1]
            P_iv_m_r_Aika_yr = P_iv_m_r_Aika_res[2]
            P_iv_m_r_Aika_selTime = P_iv_m_r_Aika_res[3]
            P_iv_m_r_Aika_finalRes = P_iv_m_r_Aika_selTime.split(':')
            P_iv_m_r_Aika_hr = P_iv_m_r_Aika_finalRes[0]
            P_iv_m_r_Aika_min = P_iv_m_r_Aika_finalRes[1]
#            P_iv_m_r_Aika_sec = P_iv_m_r_Aika_finalRes[2]
            ilmoitusVar.P_iv_m_r_Aika = datetime.datetime(int(P_iv_m_r_Aika_yr),int(P_iv_m_r_Aika_mnth),int(P_iv_m_r_Aika_dt),int(P_iv_m_r_Aika_hr),int(P_iv_m_r_Aika_min))
        KuvausTemp = self.request.get('Kuvaus')
        if KuvausTemp!="":
            ilmoitusVar.Kuvaus = self.request.get('Kuvaus')
        VastattuTemp =self.request.get('Vastattu')
        if VastattuTemp!="":
            ilmoitusVar.Vastattu = int(VastattuTemp)

        ilmoitusVar.put()
        self.redirect('/showilmoitus')



class Showomat_ilmoitukset(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
	if not user:
	  self.redirect(users.create_login_url(self.request.uri))
	else: 
          ilmoitusVar = ilmoitus.gql("WHERE Ilmoittaja = :y", y = user)
          records = ilmoitusVar.fetch(limit=100)
          template_values = { 'records': records,"nickname":user.nickname(),"url":users.create_logout_url("/")}
          path=os.path.join(os.path.dirname(__file__),'omat_ilmoitukset.html')
          self.response.out.write(template.render(path,template_values))

class Showilmoitus_View(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
	  self.redirect(users.create_login_url(self.request.uri))
	else:
          user = users.get_current_user()
          ilmoitusVar = ilmoitus.all()
          records = ilmoitusVar.fetch(limit=100)
          template_values = { 'records': records,"nickname":user.nickname(),"url":users.create_logout_url("/")}
          path=os.path.join(os.path.dirname(__file__),'ilmoitus_View.html')
          self.response.out.write(template.render(path,template_values))


class sortilmoitus_ViewAction(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        ilmoitusVar = ilmoitus.all()
        ilmoitus_tempVal = self.request.get('SortBy')
        ilmoitus_tempOrder = self.request.get('order')
        ilmoitusVar = db.GqlQuery("SELECT * FROM ilmoitus ORDER BY " + ilmoitus_tempVal+ " " + ilmoitus_tempOrder)
        records = ilmoitusVar.fetch(limit=100)
        template_values = { 'records': records,"nickname":user.nickname(),"url":users.create_logout_url("/")}
        path=os.path.join(os.path.dirname(__file__),'ilmoitus_View.html')
        self.response.out.write(template.render(path,template_values))


class searchilmoitus_ViewAction(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        ilmoitusVar = ilmoitus.all()
        ilmoitus_Olen = self.request.get('Olen')
        queryString_ilmoitus_Olen = ""
        if ilmoitus_Olen!="":
            queryString_ilmoitus_Olen = " Olen = \'" + ilmoitus_Olen + "\'"
        ilmoitus_Paikka = self.request.get('Paikka')
        queryString_ilmoitus_Paikka = ""
        if ilmoitus_Paikka!="":
            queryString_ilmoitus_Paikka = " Paikka = \'" + ilmoitus_Paikka + "\'"
        ilmoitus_P_iv_m_r_Aika = self.request.get('P_iv_m_r_Aika')
        queryString_ilmoitus_P_iv_m_r_Aika = ""
        if ilmoitus_P_iv_m_r_Aika!="":
            queryString_ilmoitus_P_iv_m_r_Aika = " P_iv_m_r_Aika = \'" + ilmoitus_P_iv_m_r_Aika + "\'"
        ilmoitus_Kuvaus = self.request.get('Kuvaus')
        queryString_ilmoitus_Kuvaus = ""
        if ilmoitus_Kuvaus!="":
            queryString_ilmoitus_Kuvaus = " Kuvaus = \'" + ilmoitus_Kuvaus + "\'"
        ilmoitus_Vastattu = self.request.get('Vastattu')
        queryString_ilmoitus_Vastattu = ""
        if ilmoitus_Vastattu!="":
            queryString_ilmoitus_Vastattu = " Vastattu = " + ilmoitus_Vastattu
        query = "SELECT * FROM ilmoitus WHERE "
        queryString =""
        if queryString_ilmoitus_Olen!="":
            queryString = queryString + queryString_ilmoitus_Olen
        if queryString != "":
            if queryString_ilmoitus_Paikka !="":
                queryString = queryString + " AND " + queryString_ilmoitus_Paikka
        else:
            queryString = queryString + queryString_ilmoitus_Paikka
        if queryString != "":
            if queryString_ilmoitus_P_iv_m_r_Aika !="":
                queryString = queryString + " AND " + queryString_ilmoitus_P_iv_m_r_Aika
        else:
            queryString = queryString + queryString_ilmoitus_P_iv_m_r_Aika
        if queryString != "":
            if queryString_ilmoitus_Kuvaus !="":
                queryString = queryString + " AND " + queryString_ilmoitus_Kuvaus
        else:
            queryString = queryString + queryString_ilmoitus_Kuvaus
        if queryString != "":
            if queryString_ilmoitus_Vastattu !="":
                queryString = queryString + " AND " + queryString_ilmoitus_Vastattu
        else:
            queryString = queryString + queryString_ilmoitus_Vastattu

        finalQueryString = query + queryString
        if queryString !="":
            ilmoitusVar = db.GqlQuery(finalQueryString)
        records = ilmoitusVar.fetch(limit=100)
        template_values = { 'records': records,"nickname":user.nickname(),"url":users.create_logout_url("/")}
        path=os.path.join(os.path.dirname(__file__),'ilmoitus_View.html')
        self.response.out.write(template.render(path,template_values))

# palautelomake
class palaute_View(webapp.RequestHandler):
    def get(self):
        template_values = {'Olen': ilmoitus_Olens}

	path=os.path.join(os.path.dirname(__file__),'palaute.html')
	self.response.out.write(template.render(path,template_values))
	

# Vie palautelomakkeesta lähetetyt tiedot tietokantaan
class palauteAction(webapp.RequestHandler):
    def post(self):
	palauteVar = palaute()

	# kerätään tiedot palautteenantajasta
	if self.request.get('ika') != "":
	    palauteVar.ika = int(self.request.get('ika'))
	palauteVar.sukupuoli = self.request.get('sukupuoli')

	# kerätään palaute
	if self.request.get('kayttaisitko') != "":
	    palauteVar.kayttaisitko = bool(self.request.get('kayttaisitko'))

	palauteVar.hyodyllisyys = self.request.get('hyodyllisyys')
	if self.request.get('hyodyllisyysrating') != "valitse":
            palauteVar.hyodyllisyysrating = int(self.request.get('hyodyllisyysrating'))

        palauteVar.kaytettavyys = self.request.get('kaytettavyys')
	if self.request.get('kaytettavyysrating') != "valitse":
	    palauteVar.kaytettavyysRating = int(self.request.get('kaytettavyysrating'))
	
	# pannaan kantaan ja muistetaan ylistää palautteenantajaa
	palauteVar.put()
	self.redirect('/kiitos')


# Palautelomakkeen kiitossivu
class kiitos(webapp.RequestHandler):
    def get(self):
        path=os.path.join(os.path.dirname(__file__),'kiitos.html')
        template_values = {}
	self.response.out.write(template.render(path,template_values))

def main():
    application = webapp.WSGIApplication(
                [('/', MainPage),
		('/palaute', palaute_View),
		('/addpalaute', palauteAction),
		('/kiitos', kiitos),
                ('/addilmoitus',ilmoitusAction),
                ('/showilmoitus',Showilmoitus),
                ('/showilmoitus_View',Showilmoitus_View),
                ('/sortilmoitus_View',sortilmoitus_ViewAction),
                ('/searchilmoitus_View',searchilmoitus_ViewAction),
		('/showomat_ilmoitukset',Showomat_ilmoitukset)],
                debug=True)

    wsgiref.handlers.CGIHandler().run(application)

if __name__== "__main__":
    main()
