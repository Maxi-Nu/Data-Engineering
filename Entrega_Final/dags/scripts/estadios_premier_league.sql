CREATE TABLE IF NOT EXISTS mxxn13_coderhouse.estadios_premier_league
(
	id_estadio INTEGER NOT NULL  ENCODE az64
	,nombre_estadio VARCHAR(256)   ENCODE lzo
	,ciudad VARCHAR(256)   ENCODE lzo
	,PRIMARY KEY (id_estadio)
)
;