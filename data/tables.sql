CREATE TABLE subject (
    id INTEGER PRIMARY KEY,
    name VARCHAR (200),
    fonte VARCHAR (500)
);

CREATE TABLE question (
    id INTEGER PRIMARY KEY,
    question VARCHAR (200),
    id_subject INTEGER,
    FOREIGN KEY (id_subject) REFERENCES subject(id)
);

CREATE TABLE correct_alternatives (
    id INTEGER PRIMARY KEY,
    texto VARCHAR (200),
    id_question INTEGER,
    FOREIGN KEY (id_question) REFERENCES question(id)
);

CREATE TABLE wrong_alternatives (
    id INTEGER PRIMARY KEY,
    texto VARCHAR (200),
    id_question INTEGER,
    FOREIGN KEY (id_question) REFERENCES question(id)
);