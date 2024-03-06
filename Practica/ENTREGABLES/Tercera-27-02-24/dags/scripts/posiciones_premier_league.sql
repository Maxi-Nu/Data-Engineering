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
;