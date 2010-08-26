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

from dateventure import ilmoitus
from dateventure import alignment
from dateventure import palaute
from dateventure import time

# Shows the default main page
class Showetusivu(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
          template_values={"url":users.create_logout_url("/")}
        else:
          template_values={"loginurl":users.create_login_url("/")}
        path = os.path.join(os.path.dirname(__file__),'etusivu.html')
        self.response.out.write(template.render(path,template_values))        

# Shows the announcement adding page
class addIlmoitus(webapp.RequestHandler):
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


# Throws the announcement data into the datastore
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


# Shows the user's own announcements -page
class omatIlmoitukset(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
	if not user:
	  self.redirect(users.create_login_url(self.request.uri))
	else:
	  # Get the current datetime
	  timeVar = time()
	  timeVar.put()
	  
	  # Gets the user's own date announcements
          ilmoitusVar = ilmoitus.gql("WHERE Ilmoittaja = :y AND Poistettu = False AND Datetime > :t ORDER BY Datetime ASC", y = user, t = timeVar.datetime)
          records = ilmoitusVar.fetch(limit=100)
	  
	  # Gets the user's own date responses
	  query = ilmoitus.gql("WHERE Vastaaja = :x AND Poistettu = False AND Datetime > :t ORDER BY Datetime ASC", x = user, t = timeVar.datetime)
	  responses = query.fetch(limit=100)

          template_values = { 'records': records, 'responses': responses, "nickname":user.nickname(),"url":users.create_logout_url("/")}
          path=os.path.join(os.path.dirname(__file__),'omat_ilmoitukset.html')
          self.response.out.write(template.render(path,template_values))


# This will delete the announcement
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


# This will review the details and ask the user if they really want to delete the date announcement.
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


# Modify the announcement -page
class modify(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
	if not user:
	    self.redirect(users.create_login_url(self.request.uri))
	else: 
	    path=os.path.join(os.path.dirname(__file__),'modify.html')	
	    postKey = self.request.get('key')
	    ilmoitusVar = Model.get(postKey)
	    date = str(ilmoitusVar.Datetime.day) + "." + str(ilmoitusVar.Datetime.month) + "." + str(ilmoitusVar.Datetime.year)
	    template_values = {"url":users.create_logout_url("/"), 'Age':ilmoitusVar.Age, 'Olen':ilmoitusVar.Olen, 'Etsin':ilmoitusVar.Etsin, 'location':ilmoitusVar.Paikka, 'description':ilmoitusVar.Kuvaus, 'key':postKey, 'hour':ilmoitusVar.Datetime.hour, 'minute':ilmoitusVar.Datetime.minute, 'date':date}
	    self.response.out.write(template.render(path,template_values))

# modifies the announcement
class modifyAction (webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        ilmoitusVar = Model.get(self.request.get('key'))

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
        self.redirect('/modified')

  



# Shows the view with all date announcements, which are not deleted and the datetime has not passed.
class browseAnnouncements(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
	  self.redirect(users.create_login_url(self.request.uri))
	else:
 	  checkExpired()
	  
	  timeVar = time()
	  timeVar.put()
	  
          user = users.get_current_user()
          ilmoitusVar = ilmoitus.gql("WHERE Poistettu = :y ORDER BY Datetime DESC", y = False, t = timeVar.datetime)
          records = ilmoitusVar.fetch(limit=100)
          template_values = { 'records': records,"nickname":user.nickname(),"url":users.create_logout_url("/")}
          path=os.path.join(os.path.dirname(__file__),'browse_announcements.html')
          self.response.out.write(template.render(path,template_values))

# Checks all the announcements, if they are expired
def checkExpired():
    records = ilmoitus.all()
    timeVar = time()
    timeVar.put()

    for x in records:
        if not x.Expired and x.Datetime < timeVar.datetime:
	    x.Expired = True
	    x.put()


# Shows the feedback adding page.
class feedbackView(webapp.RequestHandler):
    def get(self):
	user=users.get_current_user()
        if user:
          template_values={'Olen': alignment, "url":users.create_logout_url("/")}
        else:
          template_values={'Olen': alignment, "loginurl":users.create_login_url("/")}
	path=os.path.join(os.path.dirname(__file__),'palaute.html')
	self.response.out.write(template.render(path,template_values))
	

# Puts the feedback data into the datastore
class feedbackAction(webapp.RequestHandler):
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
            palauteVar.hyodyllisyysRating = int(self.request.get('hyodyllisyysrating'))

        palauteVar.kaytettavyys = self.request.get('kaytettavyys')
	if self.request.get('kaytettavyysrating') != "valitse":
	    palauteVar.kaytettavyysRating = int(self.request.get('kaytettavyysrating'))


	palauteVar.kehitys = self.request.get('kehitys')
	palauteVar.vapaaSana = self.request.get('vapaasana')
	
	# pannaan kantaan ja muistetaan ylistaa palautteenantajaaa
	palauteVar.put()
	self.redirect('/kiitos')


# Feedback form's "thank you" -page
class kiitos(webapp.RequestHandler):
    def get(self):
        path=os.path.join(os.path.dirname(__file__),'kiitos.html')
        template_values = {}
	self.response.out.write(template.render(path,template_values))


# Shows the confirmation page, that the date announcement was successfully added
class kuittaus(webapp.RequestHandler):
    def get(self):
	user = users.get_current_user
        path=os.path.join(os.path.dirname(__file__),'kuittaus.html')
        template_values = {"url":users.create_logout_url("/")}
	self.response.out.write(template.render(path,template_values))

# Shows the confirmation page, that the date announcement was successfully modified
class modified(webapp.RequestHandler):
    def get(self):
	user = users.get_current_user
        path=os.path.join(os.path.dirname(__file__),'modified.html')
        template_values = {"url":users.create_logout_url("/")}
	self.response.out.write(template.render(path,template_values))

# Shows the FAQ-page
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
                [('/', Showetusivu),
		('/palaute', feedbackView),
		('/addpalaute', feedbackAction),
		('/kiitos', kiitos),
		('/kuittaus',kuittaus),
		('/ukk', ukk),
		('/modify', modify),
		('/modifyaction', modifyAction),
		('/modified', modified),
		('/confirm', vahvistaIlmoituksenAvaus),
		('/confirmed', ilmoitusVahvistettu),
                ('/addilmoitus',ilmoitusAction),
                ('/ilmoita',addIlmoitus),
                ('/selaa', browseAnnouncements),
		('/omatilmoitukset',omatIlmoitukset),
		('/delete', delete),
		('/confirmdelete', confirmDelete),
		('/showetusivu',Showetusivu)],
                debug=True)

    wsgiref.handlers.CGIHandler().run(application)

if __name__== "__main__":
    main()
