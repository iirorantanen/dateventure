from google.appengine.ext import db
from google.appengine.ext import search
from google.appengine.api import users
K_ytt_j_Sukupuolis=('Mies','Nainen','En kerro')
alignment=('Mies','Nainen','En kerro')
etsin=('Mies', 'Nainen', 'Ei')


class ilmoitus(search.SearchableModel):
    global alignment
    Olen = db.StringProperty(choices=alignment)
    Etsin = db.StringProperty(choices=etsin)
    Paikka = db.StringProperty()
    Paikkakunta = db.StringProperty(default="Turku")
    Datetime = db.DateTimeProperty()
    Date = db.DateProperty()
    Time = db.TimeProperty()
    Kuvaus = db.StringProperty()
    Vastattu = db.BooleanProperty(default=False)
    vKuvaus = db.StringProperty()
    Ilmoittaja = db.UserProperty(auto_current_user=True, required=True)
    Vastaaja = db.UserProperty()
    Age = db.IntegerProperty(default=0)

      
class palaute(search.SearchableModel):
    # Palautteen lahettajan tiedot
    sukupuoli = db.StringProperty(choices=K_ytt_j_Sukupuolis)
    ika = db.StringProperty()

    # Palautteen osat
    kayttaisitko = db.BooleanProperty()
    hyodyllisyys = db.TextProperty()
    hyodyllisyysRating = db.IntegerProperty()
    kaytettavyys = db.TextProperty()
    kaytettavyysRating = db.IntegerProperty()
    vapaaSana = db.TextProperty()
    kehitys = db.TextProperty()


    date = db.DateTimeProperty(auto_now_add=True)


    

#class selaus(search.SearchableModel):
#    Lookup_1 = db.ReferenceProperty(ilmoitus,collection_name="selaus_1_set")
