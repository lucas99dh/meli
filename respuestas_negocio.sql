-- Query 1: Usuarios con cumpleaños hoy y ventas en enero 2020 superiores a 1500
SELECT 
    c.customer_id, 
    c.nombre, 
    c.apellido,
    COUNT(o.order_id) AS ventas_realizadas
FROM Customer c
JOIN Orders o ON c.customer_id = o.seller_id
WHERE 
    DAY(c.fecha_nacimiento) = DAY(CURRENT_DATE())
    AND MONTH(c.fecha_nacimiento) = MONTH(CURRENT_DATE())
    AND o.fecha_order BETWEEN '2020-01-01' AND '2020-01-31'
GROUP BY c.customer_id, c.nombre, c.apellido
HAVING COUNT(o.order_id) > 1500;

-- Query 2: Top 5 vendedores por mes en 2020 en la categoría 'Celulares'
WITH ventas_por_mes AS (
    SELECT 
        DATE_FORMAT(o.fecha_order, '%Y-%m') AS mes_año,
        c.customer_id,
        c.nombre,
        c.apellido,
        COUNT(o.order_id) AS ventas_realizadas,
        SUM(o.cantidad) AS productos_vendidos,
        SUM(o.precio * o.cantidad) AS monto_total
    FROM Orders o
    JOIN Customer c ON o.seller_id = c.customer_id
    JOIN Item i ON o.item_id = i.item_id
    JOIN Category cat ON i.category_id = cat.category_id
    WHERE 
        o.fecha_order BETWEEN '2020-01-01' AND '2020-12-31'
        AND cat.nombre = 'Celulares'
    GROUP BY mes_año, c.customer_id, c.nombre, c.apellido
)
SELECT 
    mes_año AS 'Mes-Año',
    nombre,
    apellido,
    ventas_realizadas,
    productos_vendidos,
    monto_total
FROM (
    SELECT 
        mes_año,
        nombre,
        apellido,
        ventas_realizadas,
        productos_vendidos,
        monto_total,
        ROW_NUMBER() OVER (PARTITION BY mes_año ORDER BY monto_total DESC) AS rn
    FROM ventas_por_mes
) t
WHERE rn <= 5
ORDER BY mes_año, rn;

-- Query 3: Stored Procedure para poblar la tabla Item_Status
DELIMITER $$

CREATE PROCEDURE sp_UpdateItemStatus()
BEGIN
    -- Se elimina el registro del día actual para evitar duplicados en caso de reprocesamiento
    DELETE FROM Item_Status WHERE fecha = CURDATE();
    
    -- Se insertan los registros con el estado y precio actual de cada ítem
    INSERT INTO Item_Status (item_id, precio, estado, fecha)
    SELECT 
        item_id,
        precio,
        estado,
        CURDATE() AS fecha
    FROM Item;
END$$

DELIMITER ;
