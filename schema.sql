DROP TABLE IF EXISTS book;

CREATE TABLE book (
    cover VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    descr VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    publisher VARCHAR NOT NULL,
    pub_date DATE NOT NULL,
    genres VARCHAR NOT NULL,
    lang VARCHAR NOT NULL,
    pages INT NOT NULL,
    comp VARCHAR NOT NULL,
    price DECIMAL NOT NULL,
    rating FLOAT NOT NULL,
    tot_rat INT NOT NULL
);