--EJERCICIO 1
-- 1. Crear tablas:
CREATE TABLE Customers (
CustomerID INT PRIMARY KEY,
FirstName VARCHAR(50),
LastName VARCHAR(50),
Email VARCHAR(100),
Phone VARCHAR(20)
);
CREATE TABLE Orders (
OrderID INT PRIMARY KEY,
CustomerID INT,
OrderDate DATE,
TotalAmount DECIMAL(10,2),
FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);
CREATE TABLE OrderItems (
OrderItemID INT PRIMARY KEY,
OrderID INT,
ProductID INT,
Quantity INT,8
Price DECIMAL(10,2),
FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);
CREATE TABLE Products (
ProductID INT PRIMARY KEY,
ProductName VARCHAR(100),
Category VARCHAR(50),
Price DECIMAL(10,2)
);
-- 2. Insertar Data:
INSERT INTO Customers (CustomerID, FirstName, LastName, Email,
Phone)
VALUES (1, 'John', 'Doe', 'john.doe@example.com', '1234567890');
INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount)
VALUES (1, 1, '2022-01-01', 100.00);
INSERT INTO OrderItems (OrderItemID, OrderID, ProductID, Quantity,
Price)
VALUES (1, 1, 1, 2, 50.00);
INSERT INTO Products (ProductID, ProductName, Category, Price)
VALUES (1, 'Product A', 'Category A', 50.00);
--3. Hacer algunas modificaciones:
UPDATE Customers
SET Phone = '9876543210'
WHERE CustomerID = 1;
INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount)
VALUES (2, 1, '2022-02-01', 200.00);
INSERT INTO OrderItems (OrderItemID, OrderID, ProductID, Quantity,
Price)
VALUES (2, 2, 1, 3, 50.00);

--EJERCICIO 2 

CREATE TABLE Sales (
SalesID INT PRIMARY KEY,
ProductID INT,
DateID INT,
CustomerID INT,
Quantity INT,
Amount DECIMAL(10,2)
);
CREATE TABLE Products (
ProductID INT PRIMARY KEY,
ProductName VARCHAR(100),
Category VARCHAR(50)
);
CREATE TABLE Dates (
DateID INT PRIMARY KEY,
Date DATE,
DayOfWeek VARCHAR(20),
Month VARCHAR(20),
Year INT
);
CREATE TABLE Customers (
CustomerID INT PRIMARY KEY,
FirstName VARCHAR(50),
LastName VARCHAR(50),
Email VARCHAR(100),
Phone VARCHAR(20)
);
INSERT INTO Sales (SalesID, ProductID, DateID, CustomerID, Quantity,
Amount)
VALUES (1, 1, 1, 1, 2, 100.00);
INSERT INTO Products (ProductID, ProductName, Category)
VALUES (1, 'Product A', 'Category A');
INSERT INTO Dates (DateID, Date, DayOfWeek, Month, Year)
VALUES (1, '2022-01-01', 'Saturday', 'January', 2022);
INSERT INTO Customers (CustomerID, FirstName, LastName, Email, Phone)
VALUES (1, 'John', 'Doe', 'john.doe@example.com', '1234567890');

--1
SELECT SUM(Quantity*Amount),B.Category
  FROM [MAIN].[dbo].[Sales] A JOIN [MAIN].[dbo].[Products] B on A.ProductID=B.ProductID
  GROUP BY B.Category