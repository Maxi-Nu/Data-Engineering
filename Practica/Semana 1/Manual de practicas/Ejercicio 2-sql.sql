--A)
SELECT COUNT(1)'LLAMADAS TOTALES',SUM(productsold)'VENTAS TOTALES'
  FROM [MAIN].[dbo].[calls] A join MAIN.dbo.customers B
  ON A.customerid=B.customerid
  WHERE B.occupation LIKE '%ENGINEER%'
  ORDER BY 1

--B)
SELECT COUNT(1)'LLAMADAS TOTALES',SUM(productsold)'VENTAS TOTALES'
  FROM [MAIN].[dbo].[calls] A join MAIN.dbo.customers B
  ON A.customerid=B.customerid
  ORDER BY 1