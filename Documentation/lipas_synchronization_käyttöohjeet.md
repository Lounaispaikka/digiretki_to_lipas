# Käyttöohjeet

## Tarkoitus

Synkronoida Lippaan kohdedata Virman kohdedatan kanssa sekä seurata ja pitää kirjaa siitä, mitkä Virman kohteista on jo kokonaisuudessaan viety Lippaaseen.

### Esimerkki
Lippaassa ja Virmassa on molemmissa pistekohde ***Maskun Rivieran frisbeegolfrata***. Virman tietokantaan tulee merkitä **``Lippaan frisbeegolfradan ID``**, jotta tiedetään, mitkä kohteet eri järjestelmissä vastaavat toisiaan. Tämän lisäksi, kohteen metatiedot tulee tarkistaa Lippaassa manuaalisesti, jotta voidaan varmistua, että tiedot ovat siirtyneet Lippaaseen eheinä ja oikeellisina (esim. mitään tietoja ei puutu Lippaasta, mitä Virmassa on). 

## Ohjeet
Lounaistieto on vienyt käsin jotain kohdekokonaisuuksia Lippaaseen (esim. ***Maskun Riviera***). Virman tietokantaan tulee merkitä, että kyseiset kohteet on viety ja niiden metatiedot ovat varmistettu paikkansapitäviksi Lippaassa. Näin pystytään pitämään kirjaa siitä, mitkä kohteet on jo viety Lippaaseen ja päällekkäiseltä työltä vältytään.  

1. **Lataa tarpeelliset kerrokset QGIS:iin**
    - Virman pistekohteet
    - Virman reitit
    - Lippaan pistekohteet
    - Lippaan reitit

2. **Tunnista kohde Virmasta, jonka haluat synkronoida** (kuva)
    - esim. ***Maskun Rivieran frisbeegolfrata***
    <img width="1726" height="756" alt="image" src="https://github.com/user-attachments/assets/4417e734-40b9-4130-b0f6-23d079b144ad" />

3. **Tunnista vastaava kohde myös Lippaasta** (kuva)
    <img width="1723" height="677" alt="image" src="https://github.com/user-attachments/assets/f6619ce5-e469-4556-94fc-212a41f7b197" />

4. **Varmista, että Lippaan ja Virman vastaavien kohteiden metatiedot vastaavat toisiaan**
    - Tarkoittaen, että kaikki tiedot Virmasta ovat siirtyneet Lippaaseen, eikä mitään puutu
    - Tämän voi tarkistaa QGIS:sä kuvien mukaisesti info-työkalulla molemmissa kerroksissa tai Lipas kohteen voi myös etsiä https://lipas.fi/liikuntapaikat käyttöliittymästä ja tarkistaa, että kohteen tiedot vastaavat Virman tietoja
  
5. **Kopio vastaavan Lippaan kohteen ID**
    - Kun tiedot Lippaassa on varmistettu oikeiksi, kopioidaan kyseisen kohteen ID QGIS:sä (kuva)
    - Hiiren oikea ja copy attribute value
    <img width="684" height="538" alt="image" src="https://github.com/user-attachments/assets/d94e6b95-26f5-411e-a0b2-8b6e01e5a765" />

7. **Liitä ID Virman kohteelle**
    - Avaa Virman kerros muokkaustilassa
    - Tarvittaessa suodata arvoja, jotta oikea kohde löytyy
    - Liitä kopioitu ID Virman kenttään **```lipas_id```**, jos se on vielä tyhjä (kuvassa)
    - Jos kentässä on jo jokin ID ja se eroaa Lippaan vastaavan kohteen ID:stä (kopioitu ID), korvaa se
    - Lisää nykyinen aikaleima **```lipas_checked```** kenttään (pitäisi tulla vain painamalla kyseistä kenttää)
    <img width="1180" height="251" alt="image" src="https://github.com/user-attachments/assets/fec8c393-dc30-4ea8-9587-c85772dc619e" />

8. **Tee samat toimenpiteet kaikille kohteille, jotka Lounaistieto on jo vienyt käsin Lippaaseen**
    - Reitit ja pisteet
    - Reiteille toimenpiteet näyttävät ihan samalta, vain eri kerrokset Virmasta ja Lippaasta
  
## Lopputulos
Täten taataan, että vastaavat kohteet Virman ja Lippaan välillä on synkronoitu ```lipas_id``` kentän avulla ja ```lipas_checked``` taas pitää kirjaa siitä, milloin siirto on manuaalisesti tarkistettu ja todettu onnistuneeksi. Kun ```lipas_checked``` kenttään jollekin kohteelle on merkitty aikaleima, se tarkoittaa, että kyseinen kohde on viety kokonaisuudessaan Lippaaseen ja sen siirretyt tiedot ovat eheitä ja paikkansapitäviä, eikä sen eteen tarvitse tehdä enää toimenpiteitä. 
