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
  e_adi   varchar(25) not null,
  e_id          char(5),
  kurucu_id     smallint not null, 
  primary key (e_id),
  foreign key (kurucu_id) references kullanici(k_id)
);

--DROP TABLE filmler;
CREATE TABLE filmler (
  f_id smallint,
  f_adi varchar(30) not null ,
  fragman_url varchar(100),
  primary key (f_id)
);

--DROP TABLE katilimci;
CREATE TABLE katilimci (
  e_idnum char(5),
  k_idnum smallint,
  primary key (e_idnum,k_idnum),
  foreign key (e_idnum) references etkinlik(e_id),
  foreign key (k_idnum) references kullanici(k_id)
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