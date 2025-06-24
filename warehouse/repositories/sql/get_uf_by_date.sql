SELECT valor_uf::DOUBLE PRECISION AS valor_uf, fecha
FROM flesan_procesos.api_uf_utm
WHERE fecha <= DATE_TRUNC('month', %(fecha)s::date) - interval '1 day'
ORDER BY fecha DESC
LIMIT 1;
