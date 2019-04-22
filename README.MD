# Father Long Legs

## Esittely

Father long Legs on Tasohyppelypeli, jossa pelaaja ohjaa hahmoa (Father Long Legs) kent‰n l‰pi hyppim‰ll‰ erilaisten esteiden ja tasojen p‰‰lle.
Hahmo on h‰m‰h‰kki, jonka tarkoitus on suoriutua kentist‰ mahdollisimman nopeasti.

## Tiedosto- ja kansiorakenne

Kansiorakenne koostuu kahdesta p‰‰kansiosta /doc- ja /src-kansioista. 
Kaikki ohjelmaan liittyv‰t dokumentaatiot lˆytyv‰t /doc kansiosta ja ohjelmaan liittyv‰t koodit lˆytyv‰t /src kansiosta.
P‰‰ohjelma on nimelt‰‰n game.py ja sit‰ ajamalla p‰‰see pelaamaan peli‰. Kentt‰editori on nimelt‰‰n leveleditor.py.

Eri kent‰t ovat .txt tiedostoina /src/levels/ kansiossa ja erilaiset ‰‰net ovat /src/sounds/ kansiossa.

## Asennusohje

  - Mit‰ kirjastoja ohjelma tarvitsee (Pygame)
  - Kirjastojen asennusohje:
      - python3 -m pip install -U pygame --user

## K‰yttˆohje

  - Miten ohjelmaa ajetaan
	P‰‰ohjelma k‰ynnistet‰‰n ajamalla game.py tiedostoa. Kentt‰editori k‰ynnistet‰‰n ajamalla leveleditor.py tiedostoa.
  - Mahdolliset asetustiedostot ja niiden k‰yttˆ
	Kent‰t lˆytyv‰t /src/levels/ kansiosta ja niit‰ voi muokata haluamansa mukaan suoraan editorista tai k‰ytt‰m‰ll‰ kentt‰editoria.
	Kent‰t ovtat tekstitiedostoina ja tasojen m‰‰rittely on siin‰ riveitt‰in. 
	Tasot luodaan siten, ett‰ ensimm‰inen alkio kertoo esteen leveyden, toinen alkio korkeuden, kolmas alkio x- ja nelj‰s alkio y-koordinaatit.
