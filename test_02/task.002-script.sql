select 
    cash, 
    sum(case when operationtype then amount else 0 end) as sales_amount,
    sum(case when not operationtype THEN amount else 0 end) as returns_amount
from 
    public.erpi_purchase
where 
    shop = :theshop
    and operday = :theoperday
group by 
    cash
order by 
    cash;