# Keskustelusovellus
Tietokannat ja web-ohjelmointi harjoitustyö

Keskustelusovellus jossa käyttäjät voivat luoda keskusteluja ja vastata keskusteluihin.
Käyttäjille on kaksi mahdollista roolia joko ylläpitäjä tai peruskäyttäjä.

Sovelluksen ominaisuuksia:
    
  - Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
  - Käyttäjä näkee sovelluksen etusivulla listan viesti ketjuista sekä jokaisen ketjun viestien määrän ja ketjun luonti ajankohdan.
  - Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
  - Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
  - Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
  - Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
  - Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
  - Ylläpitäjä voi luoda salaisen alueen, johon vain ylläpitäjillä on pääsy.


## Käynnistys ohjeet
Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon `.env`-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

```bash
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>
```
Missä `DATEBASE_URL` on muotoa `postgresql:///user`
ja `SECRET_KEY` on satunnaisesti luotu merkkijono, jonka voi luoda esim. seuraavasti:

```bash
$ python3
>>> import secrets
>>> secrets.token_hex(16)
'<salainen-avain>'
```

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```

Määritä vielä tietokannan skeema komennolla

```bash
$ psql < schema.sql
```

Nyt voit käynnistää sovelluksen komennolla

```bash
$ flask run
```


## Ylläpito oikeuksien asettamien
En keksinyt mitään järkevää tapaa tähän itse sovelluksessa, joten ylläpito oikeudet pitää asettaa muokkaamalla arova tietokannassa manuaalisesti

Seuraavasti:

```bash
$ psql
user=# UPDATE users
SET admin = TRUE
WHERE username = '<käyttäjänimi>';
```
