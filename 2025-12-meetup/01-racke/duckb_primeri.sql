INSTALL spatial;
LOAD spatial;

-- uvoz in nalaganje razširitve: rahlo pythonski
-- uvoz dejanske rabe kmetijskih zemljišč (MKGP)
CREATE TABLE dejanska_raba_20241231 AS 
SELECT * FROM ST_Read('/home/user/.../RABA_20241231.shp');
-- 9s

-- prva poizvedba: če poznaš PostGIS je to mala malica!
SELECT count(*) FROM dejanska_raba_20241231 where st_area(geom) between 1234 and 4321;
-- 0,086s
-- 391965 poligonov ima površino med 1234 in 4321 m2

-- uvoz poligonov parcel Katastra nepremičnin (GURS)
CREATE TABLE kn_parcele_20250126 AS 
SELECT * FROM ST_Read('/home/user/.../KN_SLO_PARCELE_SLO_PARCELE_poligon.shp');
-- 28s

-- uvoz daljic parcel Katastra nepremičnin (GURS)
CREATE TABLE kn_daljice_20250126 AS 
SELECT * FROM ST_Read('/home/user/...//KN_SLO_DALJICE_DALJICE_line.shp');
-- 2m 37s

SELECT count(*) FROM kn_daljice_20250126;
-- 36962173

-- izvoz dejanske rabe v GPKG
COPY dejanska_raba_20241231 TO '/home/user/.../dejanska_raba_20241231.gpkg'
WITH (FORMAT GDAL, DRIVER 'GPKG', LAYER_CREATION_OPTIONS 'WRITE_BBOX=YES');
-- 1m 56s

-- izvoz poligonov parcel v GPKG
COPY kn_parcele_20250126 TO 'home/user/.../kn_parcele_20250126.gpkg'
WITH (FORMAT GDAL, DRIVER 'GPKG', LAYER_CREATION_OPTIONS 'WRITE_BBOX=YES');
-- 5m 52s

-- izvoz daljic parcel v GPKG
COPY kn_daljice_20250126 TO 'home/user/.../kn_daljice_20250126.gpkg'
WITH (FORMAT GDAL, DRIVER 'GPKG', LAYER_CREATION_OPTIONS 'WRITE_BBOX=YES');
-- prekinil sem po 45 min, nima smisla: GeoParquet izberi

-- združi vse geometrije z enako rabo (dissolve)
CREATE TABLE test_diss AS​
SELECT "RABA_ID",st_union(geom,geom) AS geom​
FROM raba_dejanska_raba_20241231​
GROUP BY "RABA_ID", geom;


-- razbijanje parcel glede na dejansko rabo
CREATE TABLE test_inters AS
SELECT
    a.*, b."RABA_ID" AS raba_id,
    ST_Intersection(a.geom, b.geom) AS geom
FROM
    kn_parcele_20250126 a
JOIN
    dejanska_raba_20241231 b
ON
    ST_Intersects(a.geom, b.geom);

INSTALL postgres;
LOAD postgres;

-- povezava na postgres bazo
ATTACH 'dbname=x user=x host=x password=x@' AS moj_postgres (TYPE POSTGRES);

-- test
SELECT * FROM moj_postgres.shema.moja_tabela;

​

