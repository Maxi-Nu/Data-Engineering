/*
1)Extraer agentes cuyo nombre empieza por M o termina en O.
2)Escribir una consulta que produzca una lista, en orden alfabético, de todas las distintas ocupaciones en la tabla Customer que 
    contengan la palabra "Engineer".
3)Escribir una consulta que devuelva el ID del cliente, su nombre y una columna nueva llamada “Mayor30” que contenga "Sí" si el cliente 
    tiene más de 30 años y "No" en caso contrario.
4)Escribir una consulta que devuelva todas las llamadas realizadas a clientes de la profesión de ingeniería y muestre si son mayores o menores de 30, así como si 
    terminaron comprando el producto de esa llamada
5)Escribir dos consultas: 
    1. Una que calcule las ventas totales y las llamadas totales realizadas a los clientes de la profesión de ingeniería.
    2. Otra que calcule las mismas métricas para toda la base de clientes
6)Escribir una consulta que devuelva 
    ✓ Para cada agente: el nombre del agente, la cantidad de llamadas, las llamadas más largas y más cortas, la duración promedio de las llamadas y la cantidad total de 
    productos vendidos. 
    ✓ Nombra las columnas: AgentName, NCalls, Shortest, Longest, AvgDuration y TotalSales
    ✓ Luego ordenar la tabla por: AgentName en orden alfabético.
7) Escribir una consulta que extraiga dos métricas del desempeño de los agentes de ventas que le interesan a su empresa: 
    1. Para cada agente, cuántos segundos en promedio les toma vender un producto cuando tienen éxito.
    2. Para cada agente, cuántos segundos en promedio permanecen en el teléfono antes de darse por vencidos cuando no tienen éxito
*/

--1)
SELECT NAME 
FROM dbo.agents
WHERE UPPER(name) like 'M%' OR UPPER(name) like '%O'
--2)
SELECT DISTINCT occupation
FROM dbo.customers
WHERE occupation like '%ENGINEER%'
order by 1 asc
--3)
SELECT DISTINCT customerid,name,case when Age>30 then 'SI' else 'NO' end as Mayor30 ,age
FROM dbo.customers
--4)
SELECT a.callid as ID_llamada,case when b.Age>30 then 'SI' else 'NO' end as Mayor30 ,case when a.productsold>=1 then 'SI' else 'NO' end as Compro
FROM dbo.calls a left join dbo.customers b on a.customerid=b.customerid
WHERE b.occupation like '%ENGINEER%'
order by 1 asc
--5)
SELECT count(1) llamadasTotales ,sum(a.productsold)ventasTotales 
FROM dbo.calls a left join dbo.customers b on a.customerid=b.customerid
WHERE b.occupation like '%ENGINEER%'
--
SELECT count(1) llamadasTotales ,sum(a.productsold)ventasTotales 
FROM dbo.calls a left join dbo.customers b on a.customerid=b.customerid
--6)
SELECT b.name nombre,count(1) CantLlamadas,max(duration) LLamadaMasLarga,MIN(duration) LlamadaMasCorta,AVG(duration) Promedio,SUM(productsold) CantVentas
FROM dbo.calls a left join dbo.agents b on a.agentid=b.agentid
GROUP by b.name
--7)
SELECT b.name nombre,count(1) CantLlamadas,max(duration) LLamadaMasLarga,MIN(duration) LlamadaMasCorta,AVG(duration) Promedio,SUM(productsold) CantVentas
FROM dbo.calls a left join dbo.agents b on a.agentid=b.agentid
GROUP by b.name