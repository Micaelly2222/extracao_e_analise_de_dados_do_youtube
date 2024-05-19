-- KPIs para Monitoramento do Processo de Venda

-- 1. Total de Vendas por Categoria de Produto
WITH TotalSales AS (
    SELECT 
        p.product_category_name,
        SUM(o.price) AS category_sales
    FROM 
        OrderFact o
    JOIN 
        ProductDimension p ON o.product_id = p.product_id
    GROUP BY 
        p.product_category_name
),
TotalOverallSales AS (
    SELECT 
        SUM(category_sales) AS overall_sales
    FROM 
        TotalSales
)
SELECT 
    t.product_category_name,
    t.category_sales,
    (t.category_sales / o.overall_sales) * 100 AS category_sales_percentage
FROM 
    TotalSales t, TotalOverallSales o
ORDER BY 
    t.category_sales DESC;

-- 2. Número de Pedidos e Clientes por Estado
WITH StateOrders AS (
    SELECT 
        c.customer_state,
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(DISTINCT o.customer_id) AS total_customers
    FROM 
        OrderFact o
    JOIN 
        CustomerDimension c ON o.customer_id = c.customer_id
    GROUP BY 
        c.customer_state
)
SELECT 
    customer_state,
    total_orders,
    total_customers
FROM 
    StateOrders
ORDER BY 
    total_orders DESC;

-- 3. Média de Valor do Pedido por Mês
WITH MonthlyOrders AS (
    SELECT 
        DATE_TRUNC('month', o.order_purchase_timestamp) AS order_month,
        AVG(o.payment_value) AS average_order_value
    FROM 
        OrderFact o
    GROUP BY 
        DATE_TRUNC('month', o.order_purchase_timestamp)
),
CumulativeAverage AS (
    SELECT 
        order_month,
        average_order_value,
        AVG(average_order_value) OVER (ORDER BY order_month) AS cumulative_average_order_value
    FROM 
        MonthlyOrders
)
SELECT 
    order_month,
    average_order_value,
    cumulative_average_order_value
FROM 
    CumulativeAverage
ORDER BY 
    order_month;
