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
from google.appengine.ext.db import Model
#from dateventure import selaus
from dateventure import ilmoitus
from dateventure import alignment
from dateventure import palaute

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        global ilmoitus_Olen
        if user:
            template_values={

            'Olen': alignment ,

                "nickname":user.nickname(),
                "url":users.create_logout_url("/")
            }
            theHtmlPage='etusivu.html'
        else:
            template_values={
                "loginurl":users.create_login_url("/")
            }
            theHtmlPage='etusivu.html'

        path = os.path.join(os.path.dirname(__file__),theHtmlPage)
        self.response.out.write(template.render(path,template_values))

class Showetusivu(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
          template_values={"url":users.create_logout_url("/")}
        else:
          template_values={"loginurl":users.create_login_url("/")}
        path = os.path.join(os.path.dirname(__file__),'etusivu.html')
        self.response.out.write(template.render(path,template_values))        


class Showilmoitus(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
	if not user:
	  self.redirect(users.create_login_url(self.request.uri))
        global ilmoitus_Olen
        if user:
          template_values={'Olen': alignment, "url":users.create_logout_url("/")}
        else:
          template_values={'Olen': alignment, "loginurl":users.create_login_url("/")}
        path = os.path.join(os.path.dirname(__file__),'ilmoitus.html')
        self.response.out.write(template.render(path,template_values))

class ilmoitusAction (webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        ilmoitusVar = ilmoitus()

	ilmoitusVar.Ilmoittaja = user
        OlenTemp =self.request.get('Olen')
        ilmoitusVar.Olen = self.request.get('Olen')
	etsinTemp = self.request.get('Etsin')
	ilmoitusVar.Etsin = etsinTemp
        PaikkaTemp = self.request.get('Paikka')
        if PaikkaTemp!="":
            ilmoitusVar.Paikka = self.request.get('Paikka')

        ilmoitusVar.Time = datetime.time(int(self.request.get('Hour')), int(self.request.get('Min')))

	DateTemp = self.request.get('Date')
	Date_res = DateTemp.split('.')
	ilmoitusVar.Date = datetime.date(int(Date_res[2]), int(Date_res[1]), int(Date_res[0]))
	ilmoitusVar.Datetime = datetime.datetime(int(Date_res[2]), int(Date_res[1]), int(Date_res[0]), int(self.request.get('Hour')), int(self.request.get('Min')))

#        Datetimetemp = self.request.get('Datetime')
#        if Datetimetemp!="":
#            DatetimeTemp = self.request.get('Datetime')
#            Datetime_res = DatetimeTemp.split()
#            Datetime_dt = Datetime_res[0]
#            Datetime_mnth = Datetime_res[1]
#            Datetime_yr = Datetime_res[2]
#            Datetime_selTime = Datetime_res[3]
#            Datetime_finalRes = Datetime_selTime.split(':')
#            Datetime_hr = Datetime_finalRes[0]
#            Datetime_min = Datetime_finalRes[1]
#            Datetime_sec = Datetime_finalRes[2]
#            ilmoitusVar.Datetime = datetime.datetime(int(Datetime_yr),int(Datetime_mnth),int(Datetime_dt),int(Datetime_hr),int(Datetime_min))
        KuvausTemp = self.request.get('Kuvaus')
        if KuvausTemp!="":
            ilmoitusVar.Kuvaus = self.request.get('Kuvaus')
        VastattuTemp =self.request.get('Vastattu')
        if VastattuTemp!="":
            ilmoitusVar.Vastattu = int(VastattuTemp)
	AgeTemp = self.request.get('Age')
	if AgeTemp != "":
	  ilmoitusVar.Age = int(self.request.get('Age'))

        ilmoitusVar.put()
        self.redirect('/kuittaus')



class Showomat_ilmoitukset(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
	if not user:
	  self.redirect(users.create_login_url(self.request.uri))
	else: 
          ilmoitusVar = ilmoitus.gql("WHERE Ilmoittaja = :y AND Poistettu = False ORDER BY Datetime ASC", y = user)
          records = ilmoitusVar.fetch(limit=100)
	  
	  query = ilmoitus.gql("WHERE Vastaaja = :x AND Poistettu = False ORDER BY Datetime ASC", x = user)
	  responses = query.fetch(limit=100)

          template_values = { 'records': records, 'responses': responses, "nickname":user.nickname(),"url":users.create_logout_url("/")}

	  
          path=os.path.join(os.path.dirname(__file__),'omat_ilmoitukset.html')
          self.response.out.write(template.render(path,template_values))
	  
# This will review the details and ask the user if they really want to delete the date ilmoitus.
class confirmDelete(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
	if not user:
	    self.redirect(users.create_login_url(self.request.uri))
	else: 
	    path=os.path.join(os.path.dirname(__file__),'confirmdelete.html')	
	    postKey = self.request.get('key')
	    ilmoitusVar = Model.get(postKey)
	    template_values = {"url":users.create_logout_url("/"), 'datetime':ilmoitusVar.Datetime, 'location':ilmoitusVar.Paikka, 'description':ilmoitusVar.Kuvaus, 'key':postKey }
	    self.response.out.write(template.render(path,template_values))


# This will delete the ilmoitus
class delete(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
	if not user:
	    self.redirect(users.create_login_url(self.request.uri))
	else: 
	    path=os.path.join(os.path.dirname(__file__),'deleted.html')	
	    postKey = self.request.get('key')
	    ilmoitusVar = Model.get(postKey)
	    ilmoitusVar.Poistettu = True
	    ilmoitusVar.put()
	    template_values = {"url":users.create_logout_url("/")}
	    self.response.out.write(template.render(path,template_values))  

class Showilmoitus_View(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
	  self.redirect(users.create_login_url(self.request.uri))
	else:
          user = users.get_current_user()
          ilmoitusVar = ilmoitus.gql("WHERE Vastattu = :y AND Poistettu = :y", y = False)
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
        ilmoitus_Datetime = self.request.get('Datetime')
        queryString_ilmoitus_Datetime = ""
        if ilmoitus_Datetime!="":
            queryString_ilmoitus_Datetime = " Datetime = \'" + ilmoitus_Datetime + "\'"
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
            if queryString_ilmoitus_Datetime !="":
                queryString = queryString + " AND " + queryString_ilmoitus_Datetime
        else:
            queryString = queryString + queryString_ilmoitus_Datetime
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
	user=users.get_current_user()
        if user:
          template_values={'Olen': alignment, "url":users.create_logout_url("/")}
        else:
          template_values={'Olen': alignment, "loginurl":users.create_login_url("/")}
	path=os.path.join(os.path.dirname(__file__),'palaute.html')
	self.response.out.write(template.render(path,template_values))
	

# Vie palautelomakkeesta lahetetyt tiedot tietokantaan
class palauteAction(webapp.RequestHandler):
    def post(self):
	palauteVar = palaute()

	# kerataan tiedot palautteenantajasta
	if self.request.get('ika') != "":
	    palauteVar.ika = self.request.get('ika')
	palauteVar.sukupuoli = self.request.get('sukupuoli')

	# kerataan palaute
	if self.request.get('kayttaisitko') != "":
	    palauteVar.kayttaisitko = bool(self.request.get('kayttaisitko'))

	palauteVar.hyodyllisyys = self.request.get('hyodyllisyys')
	if self.request.get('hyodyllisyysrating') != "valitse":
            palauteVar.hyodyllisyysrating = int(self.request.get('hyodyllisyysrating'))

        palauteVar.kaytettavyys = self.request.get('kaytettavyys')
	if self.request.get('kaytettavyysrating') != "valitse":
	    palauteVar.kaytettavyysRating = int(self.request.get('kaytettavyysrating'))

	palauteVar.kehitys = self.request.get('kehitys')
	
	# pannaan kantaan ja muistetaan ylistaa palautteenantajaa
	palauteVar.put()
	self.redirect('/kiitos')


# Palautelomakkeen kiitossivu
class kiitos(webapp.RequestHandler):
    def get(self):
        path=os.path.join(os.path.dirname(__file__),'kiitos.html')
        template_values = {}
	self.response.out.write(template.render(path,template_values))

class kuittaus(webapp.RequestHandler):
    def get(self):
	user = users.get_current_user
        path=os.path.join(os.path.dirname(__file__),'kuittaus.html')
        template_values = {"url":users.create_logout_url("/")}
	self.response.out.write(template.render(path,template_values))

class ukk(webapp.RequestHandler):
    def get(self):
	path=os.path.join(os.path.dirname(__file__),'ukk.html')
	template_values = {"url":users.create_logout_url("/")}
	self.response.out.write(template.render(path,template_values))

# This will review the details and ask the user if they want to set up the date.
class vahvistaIlmoituksenAvaus(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
	if not user:
	    self.redirect(users.create_login_url(self.request.uri))
	else: 
	    path=os.path.join(os.path.dirname(__file__),'confirm.html')	
	    postKey = self.request.get('key')
	    ilmoitusVar = Model.get(postKey)
	    template_values = {"url":users.create_logout_url("/"), 'key':postKey, 'datetime':ilmoitusVar.Datetime, 'age':ilmoitusVar.Age, 'gender':ilmoitusVar.Olen, 'location':ilmoitusVar.Paikka }
	    self.response.out.write(template.render(path,template_values))

# This page is shown when the date is confirmed
class ilmoitusVahvistettu(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
	if not user:
	    self.redirect(users.create_login_url(self.request.uri))
	else: 	
	    path=os.path.join(os.path.dirname(__file__),'confirmed.html')
	    postKey = self.request.get('key')
	    ilmoitusVar = Model.get(postKey)
	    ilmoitusVar.vKuvaus = self.request.get('description')
	    ilmoitusVar.Vastattu = True
	    ilmoitusVar.Vastaaja = user
	    ilmoitusVar.put()
	    template_values = {"url":users.create_logout_url("/"), 'key':postKey, 'datetime':ilmoitusVar.Datetime, 'age':ilmoitusVar.Age, 'gender':ilmoitusVar.Olen, 'location':ilmoitusVar.Paikka, 'owndescription':ilmoitusVar.vKuvaus, 'description':ilmoitusVar.Kuvaus }
	    self.response.out.write(template.render(path,template_values))

def main():
    application = webapp.WSGIApplication(
                [('/', MainPage),
		('/palaute', palaute_View),
		('/addpalaute', palauteAction),
		('/kiitos', kiitos),
		('/kuittaus',kuittaus),
		('/ukk', ukk),
		('/confirm', vahvistaIlmoituksenAvaus),
		('/confirmed', ilmoitusVahvistettu),
                ('/addilmoitus',ilmoitusAction),
                ('/showilmoitus',Showilmoitus),
                ('/showilmoitus_View',Showilmoitus_View),
                ('/sortilmoitus_View',sortilmoitus_ViewAction),
                ('/searchilmoitus_View',searchilmoitus_ViewAction),
		('/showomat_ilmoitukset',Showomat_ilmoitukset),
		('/delete', delete),
		('/confirmdelete', confirmDelete),
		('/showetusivu',Showetusivu)],
                debug=True)

    wsgiref.handlers.CGIHandler().run(application)

if __name__== "__main__":
    main()
