SELECT valor_uf::double precision AS valor_uf, fecha
FROM flesan_procesos.api_uf_utm
WHERE fecha <= '2025-09-10'::date
ORDER BY fecha DESC
LIMIT 1;
