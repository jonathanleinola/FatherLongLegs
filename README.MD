# Father Long Legs

## Esittely

Father long Legs on Tasohyppelypeli, jossa pelaaja ohjaa hahmoa (Father Long Legs) kentän läpi hyppimällä erilaisten esteiden ja tasojen päälle.
Hahmo on hämähäkki, jonka tarkoitus on suoriutua kentistä mahdollisimman nopeasti.

## Tiedosto- ja kansiorakenne

Kansiorakenne koostuu kahdesta pääkansiosta /doc- ja /src-kansioista. 
Kaikki ohjelmaan liittyvät dokumentaatiot löytyvät /doc kansiosta ja ohjelmaan liittyvät koodit löytyvät /src kansiosta.
Pääohjelma on nimeltään game.py ja sitä ajamalla pääsee pelaamaan peliä. Kenttäeditori on nimeltään leveleditor.py.

Eri kentät ovat .txt tiedostoina /src/levels/ kansiossa ja erilaiset äänet ovat /src/sounds/ kansiossa.

## Asennusohje

  - Mitä kirjastoja ohjelma tarvitsee (Pygame)
  - Kirjastojen asennusohje:
      - python3 -m pip install -U pygame --user

## Käyttöohje

  - Miten ohjelmaa ajetaan
   
Pääohjelma käynnistetään ajamalla game.py tiedostoa. Kenttäeditori käynnistetään ajamalla leveleditor.py tiedostoa.

  - Mahdolliset asetustiedostot ja niiden käyttö

Kentät löytyvät /src/levels/ kansiosta ja niitä voi muokata haluamansa mukaan suoraan editorista tai käyttämällä kenttäeditoria.
Kentät ovat tekstitiedostoina ja tasojen määrittely on siinä riveittäin. 
Tasot luodaan siten, että ensimmäinen alkio kertoo esteen leveyden, toinen alkio korkeuden, kolmas alkio x- ja neljäs alkio y-koordinaatit.
