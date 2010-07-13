from google.appengine.ext import db
from google.appengine.ext import search
from google.appengine.api import users
K_ytt_j_Sukupuolis=('Mies','Nainen','En kerro')
ilmoitus_Olens=('Mies','Nainen','En kerro')


class K_ytt_j(search.SearchableModel):
    Etunimi = db.StringProperty()
    Sukunimi = db.StringProperty()
    global K_ytt_j_Sukupuolis
    Sukupuoli = db.StringProperty(choices=K_ytt_j_Sukupuolis)
    Puhelin = db.StringProperty()
    Account = db.UserProperty(auto_current_user=True, required=True)

class ilmoitus(search.SearchableModel):
    global ilmoitus_Olens
    Olen = db.StringProperty(choices=ilmoitus_Olens)
    Paikka = db.StringProperty()
    P_iv_m_r_Aika = db.DateTimeProperty()
    Kuvaus = db.StringProperty()
    Vastattu = db.BooleanProperty(default=False)
    vKuvaus = db.StringProperty()
    Ilmoittaja = db.UserProperty(auto_current_user=True, required=True)
    def vastaa(self, vastaajaKuvaus):
      Vastattu = True
      vKuvaus = vastaajaKuvaus
      

#class selaus(search.SearchableModel):
#    Lookup_1 = db.ReferenceProperty(ilmoitus,collection_name="selaus_1_set")
