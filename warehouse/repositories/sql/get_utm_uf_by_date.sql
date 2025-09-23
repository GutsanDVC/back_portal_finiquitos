SELECT *
FROM flesan_procesos.api_uf_utm
WHERE fecha <= %(fecha)s::date
ORDER BY fecha DESC
LIMIT 1;