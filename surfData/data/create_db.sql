BEGIN TRANSACTION;
DROP TABLE IF EXISTS "General";
CREATE TABLE IF NOT EXISTS "General" (
	"id"	INTEGER UNIQUE,
	"timestamp"	TEXT UNIQUE,
	"id_oleaje"	INTEGER,
	"id_marea"	INTEGER,
	"id_viento"	INTEGER,
	"id_temperatura"	INTEGER,
	"foto1"	BLOB,
	"foto2"	BLOB,
	"foto3"	BLOB,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "Oleaje";
CREATE TABLE IF NOT EXISTS "Oleaje" (
	"id"	INTEGER NOT NULL UNIQUE,
	"periodo_de_pico"	INTEGER,
	"periodo_medio"	INTEGER,
	"direccion_procedencia"	INTEGER,
	"altura"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "Marea";
CREATE TABLE IF NOT EXISTS "Marea" (
	"id"	INTEGER NOT NULL UNIQUE,
	"nivel"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "Viento";
CREATE TABLE IF NOT EXISTS "Viento" (
	"id"	INTEGER NOT NULL UNIQUE,
	"velocidad_media"	REAL,
	"direccion_procedencia"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "Temperatura";
CREATE TABLE IF NOT EXISTS "Temperatura" (
	"id"	INTEGER NOT NULL UNIQUE,
	"temp_agua"	REAL,
	"temp_aire"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
COMMIT;
