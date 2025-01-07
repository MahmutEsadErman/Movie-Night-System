--DROP TABLE kullanici;
CREATE TABLE kullanici (
  fname    varchar(15) not null, 
  lname    varchar(15) not null,
  k_id     serial PRIMARY KEY,
  email  varchar(50),
  sifre_hash varchar(100)
);

--DROP TABLE etkinlik;
CREATE TABLE etkinlik (
  e_id          serial PRIMARY KEY,
  kurucu_id     smallint not null, 
  foreign key (kurucu_id) references kullanici(k_id)
);

--DROP TABLE filmler;
CREATE TABLE filmler (
  f_id smallint,
  f_adi varchar(30) not null ,
  fragman_url varchar(100),
  primary key (f_id)
);

INSERT INTO filmler (f_id, f_adi, fragman_url)
VALUES 
(1, 'Inception', 'https://www.youtube.com/watch?v=YoHD9XEInc0'),
(2, 'The Matrix', 'https://www.youtube.com/watch?v=vKQi3bBA1y8'),
(3, 'The Dark Knight', 'https://www.youtube.com/watch?v=EXeTwQWrcwY'),
(4, 'Interstellar', 'https://www.youtube.com/watch?v=zSWdZVtXT7E'),
(5, 'Shutter Island', 'https://www.youtube.com/watch?v=v8yrZSkKxTA'),
(6, 'Fight Club', 'https://www.youtube.com/watch?v=SUXWAEX2jlg'),
(7, 'Braveheart', 'https://www.youtube.com/embed/1NJO0jxBtMo?si=RGp7ZSQGMEJUSdb9'),
(8, 'Whiplash', 'https://www.youtube.com/watch?v=7d_jQycdQGo'),
(9, 'The Godfather', 'https://www.youtube.com/watch?v=sY1S34973zA'),
(10, 'Gladiator', 'https://www.youtube.com/watch?v=P5ieIbInFpg');


--DROP TABLE katilimci;
CREATE TABLE katilimci (
  e_idnum integer,
  k_idnum smallint,
  PRIMARY KEY (e_idnum, k_idnum),
  FOREIGN KEY (e_idnum) REFERENCES etkinlik(e_id) ON DELETE CASCADE,
  FOREIGN KEY (k_idnum) REFERENCES kullanici(k_id)
);

--DROP TABLE e_film_liste;
CREATE TABLE e_film_liste (
  e_idf   char(5),
  f_idf   smallint,
  oylar   smallint,
  primary key (e_idf,f_idf),
  foreign key (e_idf) references etkinlik(e_id),
  foreign key (f_idf) references filmler(f_id)
);

CREATE OR REPLACE FUNCTION prevent_extra_films()
RETURNS TRIGGER AS $$
DECLARE 
	my_count smallint DEFAULT 0;
BEGIN
	SELECT count(*) into my_count
	from e_film_liste as e
	where e.e_idf = NEW.e_idf;
    IF my_count >= 12 THEN
        RAISE EXCEPTION 'Maalesef maksimum film sayısı olan 12ye ulaşıldı! ,önerinizi alamıyoruz';
    END IF;
    RETURN NEW; -- Güncellemeye devam etmek için NEW döndürülmeli
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER max_12_film
BEFORE INSERT ON e_film_liste
FOR EACH ROW
EXECUTE FUNCTION prevent_extra_films();

CREATE OR REPLACE FUNCTION prevent_kurucu_silimi()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 from etkinlik where kurucu_id=OLD.k_id )  THEN
        RAISE EXCEPTION 'Aktif etkinliğiniz devam ederken hesabınızı silemezsiniz!';
    END IF;
    RETURN OLD; 
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER kurucu_silemez
BEFORE DELETE ON kullanici
FOR EACH ROW
EXECUTE FUNCTION prevent_kurucu_silimi();


CREATE TRIGGER katilimci_sil
AFTER DELETE ON katilimci
FOR EACH ROW
EXECUTE FUNCTION etkinlik_sil();


CREATE OR REPLACE FUNCTION etkinlik_sil()
RETURNS TRIGGER AS $$
BEGIN
  -- Eğer silinen kullanıcı etkinliğin kurucusu ise
  IF EXISTS (
    SELECT 1 
    FROM etkinlik 
    WHERE e_id = OLD.e_idnum AND kurucu_id = OLD.k_idnum
  ) THEN

    DELETE FROM e_film_liste WHERE e_idf = OLD.e_idnum;
    DELETE FROM etkinlik WHERE e_id = OLD.e_idnum;
  END IF;

  RETURN OLD;
END;
$$ LANGUAGE plpgsql;