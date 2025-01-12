
CREATE SEQUENCE seq_id
    START 1
    INCREMENT 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--DROP TABLE kullanici;
CREATE TABLE kullanici (
  fname    varchar(15) not null, 
  lname    varchar(15) not null,
  k_id     INTEGER DEFAULT nextval('seq_id') PRIMARY KEY,
  email  varchar(50) UNIQUE,
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
  f_resim bytea,
  fragman_url varchar(100),
  primary key (f_id)
);

INSERT INTO filmler (f_id, f_adi, f_resim, fragman_url)
VALUES 
(1, 'Inception', pg_read_binary_file('images\Inception.jpg'), 'https://www.youtube.com/embed/YoHD9XEInc0?si=zlMwPIfpL6Md2HzP'),
(2, 'The Matrix', pg_read_binary_file('images\The Matrix.jpg'), 'https://www.youtube.com/embed/vKQi3bBA1y8?si=bJG8Qna4HVJ04L45'),
(3, 'The Dark Knight', pg_read_binary_file('images\The Dark Knight.jpeg'), 'https://www.youtube.com/embed/EXeTwQWrcwY?si=iqoizCT4um9brICL'),
(4, 'Interstellar',pg_read_binary_file('images\Interstellar.jpeg'), 'https://www.youtube.com/embed/zSWdZVtXT7E?si=Pnryotchw0JI6R9H'),
(5, 'Shutter Island',pg_read_binary_file('images\Shutter Island.jpg'), 'https://www.youtube.com/embed/v8yrZSkKxTA?si=FoYVy5TP7q0X4sKM'),
(6, 'Fight Club',pg_read_binary_file('images\Fight Club.jpeg'), 'https://www.youtube.com/embed/SUXWAEX2jlg?si=d18WJTefZrkubZLy'),
(7, 'Braveheart',pg_read_binary_file('images\Braveheart.jpeg'), 'https://www.youtube.com/embed/1NJO0jxBtMo?si=REWxrM1xS6X-OKod'),
(8, 'Whiplash',pg_read_binary_file('images\Whiplash.jpg'), 'https://www.youtube.com/embed/7d_jQycdQGo?si=ly-VkvoI3_63z59Y'),
(9, 'The Godfather',pg_read_binary_file('images\The Godfather.jpg'), 'https://www.youtube.com/embed/sY1S34973zA?si=mRxNVNvpIhNsAMdg'),
(10, 'Gladiator',pg_read_binary_file('images\Gladiator.jpg'), 'https://www.youtube.com/embed/P5ieIbInFpg?si=loU1wqBjEEKKpZO9');


--DROP TABLE katilimci;
CREATE TABLE katilimci (
  e_idnum integer,
  k_idnum smallint,
  primary key (e_idnum,k_idnum),
  foreign key (e_idnum) references etkinlik(e_id),
  foreign key (k_idnum) references kullanici(k_id)
);

--DROP TABLE e_film_liste;
CREATE TABLE e_film_liste (
  e_idf   smallint,
  f_idf   smallint,
  oylar   smallint CHECK (oylar <= 10),
  primary key (e_idf,f_idf),
  foreign key (e_idf) references etkinlik(e_id) ON DELETE CASCADE,
  foreign key (f_idf) references filmler(f_id)
);

CREATE TABLE davetliler (
  e_idnum integer,
  k_idnum smallint,
  primary key (e_idnum,k_idnum),
  foreign key (e_idnum) references etkinlik(e_id),
  foreign key (k_idnum) references kullanici(k_id)
);

CREATE OR REPLACE FUNCTION prevent_extra_films()
RETURNS TRIGGER AS $$
DECLARE 
	my_count smallint DEFAULT 0;
BEGIN
	SELECT count(*) into my_count
	from e_film_liste as e
	where e.e_idf = NEW.e_idf;
    IF my_count >= 5 THEN
        RAISE EXCEPTION 'Maalesef maksimum film sayısı olan 5e ulaşıldı';
    END IF;
    RAISE NOTICE 'Film eklendi';
    RETURN NEW; 
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER max_5_film
BEFORE INSERT ON e_film_liste
FOR EACH ROW
EXECUTE FUNCTION prevent_extra_films();

CREATE OR REPLACE FUNCTION kurucu_silimi()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM etkinlik WHERE kurucu_id = OLD.k_idnum AND e_id = OLD.e_idnum) THEN
      DELETE FROM katilimci WHERE e_idnum = OLD.e_idnum;
		  DELETE FROM davetliler WHERE e_idnum = OLD.e_idnum;
      DELETE FROM etkinlik WHERE e_id = OLD.e_idnum AND kurucu_id = OLD.k_idnum;
    END IF;
    RAISE NOTICE 'Katılımcı silindi';
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER kurucu_exit
AFTER DELETE ON katilimci
FOR EACH ROW
EXECUTE FUNCTION kurucu_silimi();


CREATE OR REPLACE VIEW kullanici_view AS
SELECT email, sifre_hash, k_id
FROM kullanici;

