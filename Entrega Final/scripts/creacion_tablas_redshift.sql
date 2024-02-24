CREATE TABLE IF NOT EXISTS mxxn13_coderhouse.estadios_premier_league
(
	id_estadio INTEGER NOT NULL  ENCODE az64
	,nombre_estadio VARCHAR(256)   ENCODE lzo
	,ciudad VARCHAR(256)   ENCODE lzo
	,PRIMARY KEY (id_estadio)
)
DISTSTYLE AUTO
;
ALTER TABLE mxxn13_coderhouse.estadios_premier_league owner to mxxn13_coderhouse;

CREATE TABLE IF NOT EXISTS mxxn13_coderhouse.partidos_premier_league
(
	id_partido INTEGER NOT NULL  ENCODE az64
	,referi VARCHAR(256)   ENCODE lzo
	,timezone VARCHAR(256)   ENCODE lzo
	,fecha VARCHAR(256)   ENCODE lzo
	,status_par VARCHAR(256)   ENCODE lzo
	,id_eq_local INTEGER   ENCODE az64
	,eq_local_win BOOLEAN   ENCODE RAW
	,eq_local_goles INTEGER   ENCODE az64
	,id_eq_visitante INTEGER   ENCODE az64
	,eq_visitante_win BOOLEAN   ENCODE RAW
	,eq_visitante_goles INTEGER   ENCODE az64
	,resultado_final_local INTEGER   ENCODE az64
	,resultado_final_visitante INTEGER   ENCODE az64
	,resultado_extratime_local INTEGER   ENCODE az64
	,resultado_extratime_visitante INTEGER   ENCODE az64
	,penales_local INTEGER   ENCODE az64
	,penales_visitante INTEGER   ENCODE az64
	,PRIMARY KEY (id_partido)
)
DISTSTYLE AUTO
;
ALTER TABLE mxxn13_coderhouse.partidos_premier_league owner to mxxn13_coderhouse;

CREATE TABLE IF NOT EXISTS mxxn13_coderhouse.posiciones_premier_league
(
	id_eq INTEGER NOT NULL  ENCODE az64
	,name_eq VARCHAR(256) NOT NULL  ENCODE lzo
	,logo_eq VARCHAR(256)   ENCODE lzo
	,puesto INTEGER   ENCODE az64
	,puntos INTEGER   ENCODE az64
	,part_jugados INTEGER   ENCODE az64
	,part_ganados INTEGER   ENCODE az64
	,part_empatados INTEGER   ENCODE az64
	,part_perdidos INTEGER   ENCODE az64
	,goles_favor INTEGER   ENCODE az64
	,goles_contra INTEGER   ENCODE az64
	,fecha_actualizacion VARCHAR(256)   ENCODE lzo
	,fecha_ingesta VARCHAR(256)   ENCODE lzo
	,PRIMARY KEY (id_eq, name_eq)
)
DISTSTYLE AUTO
;
ALTER TABLE mxxn13_coderhouse.posiciones_premier_league owner to mxxn13_coderhouse;