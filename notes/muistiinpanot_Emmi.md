# Työpakettien etenimen ja löydöksiä

## TP 1.1
- lipas_id, lipas_loi_id lisätty points tauluun, jotta saatiin kohteita yhdistettyä keskenään
    - lipas_checked ja lipas_id myös routes taulussa
    - lipas_checked on timestamppi, milloin virma ja lipas datat on varmistettu olevan samat
- lipas_type/lipas_type_code/loi_type voidaan lisätä kunhan mapping varmistuu

Emmin ajatuksen juoksua tätä varten: JATKUU <br>
Datadumppi lippaalle uusista kohteista(täytyy saada johonkin fiksuun muotoon)
- missä muodossa data halutaan antaa sql dump, csv, json
- olen analysoinut hieman lippaan käyttöliittymää (millaisia tietoja tarvitaan)
    - boolean kentät accessibility, wc oli monessa
    - veneilynpalvelupaikka dropdown millainen veneilyn palvelupaikka

    - lisättäisiinkö virmaan boolean kentät accessibility ja wc 
        - olen antanut chatgptlle nykyisen accessibil tekstikentän ja se on määrittänyt onko saavutettava vai ei -> mielummin ei jos rajatapaus voisi toimia? täten lippaalle olisi helppo antaa datadumppi ja nykyiselle accessibil tekstikentällekin on mielestäni paikka siellä, missä tarkennetaan saavutettavuus tietoja
        - saman voisi tehdä wc:lle mutta chatgptä ei varmaan tarvita, voisi vain testata onko equipment kentässä "wc" tai vastaava
    - täytyykö lisätä columni tuolle millainen veneilynpalvelupaikka (meillä se kyll selviää aika hyvin jo virma tyypistä, mutta pitääkö tehdä lipas ystävällinen)

    - lisäksi vielä, jos on tarvetta suuremmalle saavutettavuus tiedoille (näkö-, kuulo-, liikuntavammaiset) voisi chatgptn laittaa erittelemään meidän accessibility columnin sisältöjä, kuten aikaisemmin ja erotella sieltä mahdollisesti erilaiset saavutettavuudet eri columneihin ja jos jossain lippaan kohteissa on vain yksi accessibilty kohta niin kaikki näistä vaan siihen ??

**eli mahdollisesti:**
- boolean
    - wc
    - accessibility
- teksti saavutettavuudesta
    - näkö
    - kuulo
    - liikunta

Koodi [boolean kentät](src/possible_bool_columns).

### VAI
- LIPPAASSA alla mainitut asiat ovat JSON kentässä "properties"
- ei tehdäkkään jokaiselle omaa booleania, koska niitä tulisi vähän liikaa ja kaikille liikuntapaikkatyypeille ei ole samat properties
    - pidetään schema siistimpänä
- otetaan data sellaisenaan kuin se on ulos
- accessibility boolean voitaisiin lisätä, sillä se ei ole properties kentässä
    - laitetaan scriptin läpi, joka analysoi kohtia kuten equipment, info etc.
      - luo LIPPAAN kaltaisen jäsennellyn json kentän sisältäen avainsanaosumista rakennetut properties
- erilaiset properties erilaisille liikuntapaikkatyypeillekin voitaisiin handlata alla olevan analyysin ansiosta

**tähän tyyliin:** <br> <br>
Scripti voisi ottaa huomioon eri tyypit <br>
Jos tyyppi = uimaranta, etsi: sauna, laituri, pukuhuoneet (boolean) <br>
Jos tyyppi = satama, etsi: vesipiste (kategorinen), wc (boolean), laituri (boolean) <br>

### TAI
- properties json kenttä voitaisiin lisätä meidän kantaan
    - onko niin järkevä nimenomaan sen takia, koska eri tyypeillä voi olla eri properties
    - halutaanko sekoittaa kantaa vai pitää mahd. simppelinä
    - jos tarkoituksena vain virma -> lipas datan siirto onko silloinkaan välttämätön?

### Lippaan käyttöliittymän analysointia:
**Liikuntapaikat boolean kentät**

kalastuskohde piste
- yleisöwc
- laituri

uimaranta/uimapaikka
- yleisöwc
- sauna
- laituri
- pukukopit
- suihku
- muut hyppytelineet

laavu,kota, kammi, tupa, telttailu ja leiriytyminen
- vesipiste
    - täysvuotisesti tai kausittaisesti
- yleisöwc

luontotorni, tulen/ruuanlaittopaikka
- yleisöwc

opastuspiste
- yleisöwc
- parkkipaikka

talviuimapaikka
- laituri
- sauna
- pukukopit
- suihku
- jäätymisenesto
- yleisöwc

veneilyn palvelupaikka
- laituri
- myynti/asiakaspalvelupiste
- veneen laskupaikka
- vesipiste
    - samat kuin ylempänä
- drop down hommeli
- yleisöwc

Koiraurheilualue
- Yleisö-wc
- Valaistus

Kaukalo
- valaistus
- yleisö wc
- pukukopit

Ulkoilumaja/hiihtomaja
- Myynti- tai asiakaspalvelupiste
- Välinevuokraus
- Yleisö-wc


**LOIS**
- Loi kohteilla ei ole mitään muuta täytettävää lisä infoa kuin vain esteettömyys 

## TP 1.2

## TP 1.3
- Pistekohteet saatu deduplikoitua osittais automaatiolla, lopullinen tulos tarkistettu käsin.
    - Koodi [point_deduplicator](src/point_deduplicator/virma_lipas_matched.ipynb).
    - himean alle 300 pistettä virmassa ja lippaassa
    - lipas idt näille pisteille lisätty kantaan, muilla 0
    - sama reiteille/alueille, hankalampi homma?

**Tiedonsiirto**
- Datadumppi lippaalle uusista kohteista(täytyy saada johonkin fiksuun muotoon)
- Olemassa olevat (deduplikoinnilla yhdistetyt) tarkistetaan, että datat mätsää QGIS:llä?

- Tiedonsiirtoa varten tehty Virma-Lipas tyyppi mapping table kantaan
    - saadaan kaikille virma kohteille lipas tyyppi, kunhan varmistutaan mäppäyksen oikeellisuudesta <br>
    -> Dataa pystytään ylipäätään viemään
    - Uimaranta, Uimapaikka kysymysmerkki, yhteisessä discordissa avattu tarvitaan lounaistiedon mielipide
    - Monesta-moneen taulu, tarvitaan vielä manuaalista työtä, vaikka tekisikin joinin sql:llä
    - kaikille virma-kategorioille ei saatu lipas-tyyppiä, niille annettava lipas-tyyppi käsin
    - kaupallisia palveluita ei viedä
    - virman veneenlaskupaikka on lippaan loi "boatramp", mutta mielestäni osa virman pisteistä tyypillä veneenlaskupaikka pitäisi olla lippaassa liikuntapaikka "veneilyn palvelupaikka", koska pisteissä oli niin paljon kaikkea muutakin kuin vain veneluiska, josta vene veteen (näitä oli ehkä 9, joten helppo tsekata)
    - Virman uontopolku on nyt yhdistetty lippaan luontopolun, retkeilyreitin ja kävelyreitin/ulkoilureitin kanssa voitaisko laittaa vain luontopolku -> luontopolku
        - tämä oli laitettu näin, kun aloin taulua tekemään


- liikuntapaikkojen lisäksi loi-kohteet (locations of interests)
    - ei näy lippaan käyttöliittymässä
    - Hain apilla kaiken ja tein geojsonin ja lisäsin QGIS:iin helpotti hahmottamista
    - points tauluun lisätty lipas_loi_id ja sinne kirjattu loi_idt kohteille, joilla oli vastaava lippaassa

- Tammireittien pistekohteet??
    - ei vielä lippaassa eikä virmassa

### Reitit/alueet
- ylempänä paljon asiaa pisteistä, mites reittien deduplikointi ja siirto
- lomien jälkeen?
