from google.appengine.ext import db
from google.appengine.ext import search
from google.appengine.api import users
K_ytt_j_Sukupuolis=('Mies','Nainen','En kerro')
alignment=('Mies','Nainen','En kerro')
etsin=('Mies', 'Nainen', 'Ei')

# Deitti-ilmoitus
class ilmoitus(search.SearchableModel):
    global alignment
    Olen = db.StringProperty(choices=alignment)
    Etsin = db.StringProperty()
    Paikka = db.StringProperty()
    Paikkakunta = db.StringProperty(default="Turku")
    Datetime = db.DateTimeProperty()
    Date = db.DateProperty()
    Time = db.TimeProperty()
    Kuvaus = db.StringProperty()
    Vastattu = db.BooleanProperty(default=False)
    vKuvaus = db.StringProperty()
    Ilmoittaja = db.UserProperty()
    Vastaaja = db.UserProperty()
    Age = db.IntegerProperty(default=0)
    Poistettu = db.BooleanProperty(default=False)


# Kayttajan antama palaute
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

# Kaytetaan tamanhetkisen ajan ja paivamaaran hakemiseen
class time(search.SearchableModel):
    datetime = db.DateTimeProperty(auto_now_add=True)

