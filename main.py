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
from dateventure import K_ytt_j
#from dateventure import selaus
from dateventure import ilmoitus
from dateventure import K_ytt_j_Sukupuolis
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

class ShowK_ytt_j(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        global K_ytt_j_Sukupuoli
        template_values={
            'Sukupuoli': K_ytt_j_Sukupuolis ,
            "nickname":user.nickname(),
            "url":users.create_logout_url("/")
        }
        path = os.path.join(os.path.dirname(__file__),'K_ytt_j.html')
        self.response.out.write(template.render(path,template_values))

class K_ytt_jAction (webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        K_ytt_jVar = K_ytt_j()
        EtunimiTemp = self.request.get('Etunimi')
        if EtunimiTemp!="":
            K_ytt_jVar.Etunimi = self.request.get('Etunimi')
        SukunimiTemp = self.request.get('Sukunimi')
        if SukunimiTemp!="":
            K_ytt_jVar.Sukunimi = self.request.get('Sukunimi')
        SukupuoliTemp =self.request.get('Sukupuoli')
        K_ytt_jVar.Sukupuoli = self.request.get('Sukupuoli')
        PuhelinTemp = self.request.get('Puhelin')
        if PuhelinTemp!="":
            K_ytt_jVar.Puhelin = self.request.get('Puhelin')
        
        Nick = user.nickname()
        K_ytt_jVar.put()
        self.redirect('/showK_ytt_j')

class Showselaus(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        ilmoitusVar =ilmoitus.all()
        template_values={
            'Lookup_1': ilmoitusVar ,
            "nickname":user.nickname(),
            "url":users.create_logout_url("/")
        }
        path = os.path.join(os.path.dirname(__file__),'selaus.html')
        self.response.out.write(template.render(path,template_values))

class selausAction (webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        selausVar = selaus()
        Lookup_1Name = self.request.get('Lookup_1')
        query = ilmoitus.all()
        query.filter('P_iv_m_r_Aika = ',Lookup_1Name)
        results =  query.fetch(100)
        Lookup_1 = ilmoitus()
        for result in results:
            Lookup_1 = result
        if (Lookup_1.is_saved()):
            selausVar.Lookup_1 = Lookup_1

        selausVar.put()
        self.redirect('/showselaus')

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



class Showhaku_View(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        selausVar = selaus.all()
        records = selausVar.fetch(limit=100)
        template_values = { 'records': records,"nickname":user.nickname(),"url":users.create_logout_url("/")}
        path=os.path.join(os.path.dirname(__file__),'haku_View.html')
        self.response.out.write(template.render(path,template_values))


class sorthaku_ViewAction(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        selausVar = selaus.all()
        selaus_tempVal = self.request.get('SortBy')
        selaus_tempOrder = self.request.get('order')
        selausVar = db.GqlQuery("SELECT * FROM selaus ORDER BY " + selaus_tempVal+ " " + selaus_tempOrder)
        records = selausVar.fetch(limit=100)
        template_values = { 'records': records,"nickname":user.nickname(),"url":users.create_logout_url("/")}
        path=os.path.join(os.path.dirname(__file__),'haku_View.html')
        self.response.out.write(template.render(path,template_values))


class searchhaku_ViewAction(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        selausVar = selaus.all()
        selaus_Lookup_1 = self.request.get('Lookup_1')
        queryString_selaus_Lookup_1 = ""
        if selaus_Lookup_1!="":
            queryString_selaus_Lookup_1 = " Lookup_1 = \'" + selaus_Lookup_1 + "\'"
        query = "SELECT * FROM selaus WHERE "
        queryString =""
        if queryString_selaus_Lookup_1!="":
            queryString = queryString + queryString_selaus_Lookup_1

        finalQueryString = query + queryString
        if queryString !="":
            selausVar = db.GqlQuery(finalQueryString)
        records = selausVar.fetch(limit=100)
        template_values = { 'records': records,"nickname":user.nickname(),"url":users.create_logout_url("/")}
        path=os.path.join(os.path.dirname(__file__),'haku_View.html')
        self.response.out.write(template.render(path,template_values))

class ShowK_ytt_j_View(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        K_ytt_jVar = K_ytt_j.all()
        records = K_ytt_jVar.fetch(limit=100)
        template_values = { 'records': records,"nickname":user.nickname(),"url":users.create_logout_url("/")}
        path=os.path.join(os.path.dirname(__file__),'K_ytt_j_View.html')
        self.response.out.write(template.render(path,template_values))


class sortK_ytt_j_ViewAction(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        K_ytt_jVar = K_ytt_j.all()
        K_ytt_j_tempVal = self.request.get('SortBy')
        K_ytt_j_tempOrder = self.request.get('order')
        K_ytt_jVar = db.GqlQuery("SELECT * FROM K_ytt_j ORDER BY " + K_ytt_j_tempVal+ " " + K_ytt_j_tempOrder)
        records = K_ytt_jVar.fetch(limit=100)
        template_values = { 'records': records,"nickname":user.nickname(),"url":users.create_logout_url("/")}
        path=os.path.join(os.path.dirname(__file__),'K_ytt_j_View.html')
        self.response.out.write(template.render(path,template_values))


class searchK_ytt_j_ViewAction(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        K_ytt_jVar = K_ytt_j.all()
        K_ytt_j_Etunimi = self.request.get('Etunimi')
        queryString_K_ytt_j_Etunimi = ""
        if K_ytt_j_Etunimi!="":
            queryString_K_ytt_j_Etunimi = " Etunimi = \'" + K_ytt_j_Etunimi + "\'"
        K_ytt_j_Sukunimi = self.request.get('Sukunimi')
        queryString_K_ytt_j_Sukunimi = ""
        if K_ytt_j_Sukunimi!="":
            queryString_K_ytt_j_Sukunimi = " Sukunimi = \'" + K_ytt_j_Sukunimi + "\'"
        K_ytt_j_Sukupuoli = self.request.get('Sukupuoli')
        queryString_K_ytt_j_Sukupuoli = ""
        if K_ytt_j_Sukupuoli!="":
            queryString_K_ytt_j_Sukupuoli = " Sukupuoli = \'" + K_ytt_j_Sukupuoli + "\'"
        K_ytt_j_Puhelin = self.request.get('Puhelin')
        queryString_K_ytt_j_Puhelin = ""
        if K_ytt_j_Puhelin!="":
            queryString_K_ytt_j_Puhelin = " Puhelin = \'" + K_ytt_j_Puhelin + "\'"
        query = "SELECT * FROM K_ytt_j WHERE "
        queryString =""
        if queryString_K_ytt_j_Etunimi!="":
            queryString = queryString + queryString_K_ytt_j_Etunimi
        if queryString != "":
            if queryString_K_ytt_j_Sukunimi !="":
                queryString = queryString + " AND " + queryString_K_ytt_j_Sukunimi
        else:
            queryString = queryString + queryString_K_ytt_j_Sukunimi
        if queryString != "":
            if queryString_K_ytt_j_Sukupuoli !="":
                queryString = queryString + " AND " + queryString_K_ytt_j_Sukupuoli
        else:
            queryString = queryString + queryString_K_ytt_j_Sukupuoli
        if queryString != "":
            if queryString_K_ytt_j_Puhelin !="":
                queryString = queryString + " AND " + queryString_K_ytt_j_Puhelin
        else:
            queryString = queryString + queryString_K_ytt_j_Puhelin

        finalQueryString = query + queryString
        if queryString !="":
            K_ytt_jVar = db.GqlQuery(finalQueryString)
        records = K_ytt_jVar.fetch(limit=100)
        template_values = { 'records': records,"nickname":user.nickname(),"url":users.create_logout_url("/")}
        path=os.path.join(os.path.dirname(__file__),'K_ytt_j_View.html')
        self.response.out.write(template.render(path,template_values))

class Showomat_ilmoitukset(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
#        ilmoitusVar = ilmoitus.all()
        ilmoitusVar = ilmoitus.gql("WHERE Ilmoittaja = :y", y = user)
        records = ilmoitusVar.fetch(limit=100)
        template_values = { 'records': records,"nickname":user.nickname(),"url":users.create_logout_url("/")}
        path=os.path.join(os.path.dirname(__file__),'omat_ilmoitukset.html')
        self.response.out.write(template.render(path,template_values))

class Showilmoitus_View(webapp.RequestHandler):
    def get(self):
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
	user = users.get_current_user()
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
                ('/addK_ytt_j',K_ytt_jAction),
                ('/showK_ytt_j',ShowK_ytt_j),
                ('/addselaus',selausAction),
                ('/showselaus',Showselaus),
                ('/addilmoitus',ilmoitusAction),
                ('/showilmoitus',Showilmoitus),
                ('/showhaku_View',Showhaku_View),                
		('/sorthaku_View',sorthaku_ViewAction),             
	        ('/searchhaku_View',searchhaku_ViewAction),
                ('/showK_ytt_j_View',ShowK_ytt_j_View),              
	        ('/sortK_ytt_j_View',sortK_ytt_j_ViewAction),
                ('/searchK_ytt_j_View',searchK_ytt_j_ViewAction),
                ('/showilmoitus_View',Showilmoitus_View),
                ('/sortilmoitus_View',sortilmoitus_ViewAction),
                ('/searchilmoitus_View',searchilmoitus_ViewAction),
		('/Showomat_ilmoitukset',Showomat_ilmoitukset)],
                debug=True)

    wsgiref.handlers.CGIHandler().run(application)

if __name__== "__main__":
    main()
