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
;