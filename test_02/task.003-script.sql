select 
    p.number as check_number,
    p.saletime as sale_datetime,
    p.amount as check_amount,
    p.discountammount as check_discount,
    case 
        when p.operationtype then 'Продажа'
        when not p.operationtype then 'Возврат'
        ELSE 'Неизвестно'
    end as check_type,
    count(pos.id) as positions_count,
    STRING_AGG(distinct pay.typeclass, ', ') as payment_types
from 
    public.erpi_purchase p
left join 
    public.erpi_positions pos on p.id = pos.id_purchase
left join 
    public.erpi_payments pay on p.id = pay.id_purchase
where 
    p.shop = :shop
    and p.operday = :operday
    and p.cash = :cash
group by 
    p.number, p.saletime, p.amount, p.discountammount, p.operationtype
order by 
    p.number;