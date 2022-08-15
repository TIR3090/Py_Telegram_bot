import asyncio
import random
import aiosqlite as aoisq
# import psycopg2 as sq



async def cripts_price_change():
    while True:
        global base, cur
        # base = sq.connect(dbname='d9882ng2h7srs6', user='rixdvqeatezwpn',
        #                   password='60e4ac9ad7bcb8be1b8900f38fc0c70a52a69fb6dcdd59bf553c6262631f54a6', host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com')
        # cur=base.cursor()
        base =await aoisq.connect("data_base/data_casino_keeper.db")
        cur=await base.cursor()
        await cur.execute(f"SELECT * FROM cripts")
        json_valute={}
        for cripts_bd in await cur.fetchall():
            json_valute[cripts_bd[0]]={
                'name':cripts_bd[1],
                'usd':cripts_bd[2],
                'chy':cripts_bd[3],
            }
        bitcoin_usd_price=json_valute['14']['usd']+round(random.uniform(-20,20),3)
        ethereum_usd_price=json_valute['15']['usd']+round(random.uniform(-20,20),3)
        valute_chy_price=json_valute['1']['chy']+round(random.uniform(-10,10),3)
        bitcoin_chy_price=bitcoin_usd_price*valute_chy_price
        ethereum_chy_price=ethereum_usd_price*valute_chy_price
        await cur.execute(f"UPDATE cripts SET usd='{round(bitcoin_usd_price,3)}',chy='{round(bitcoin_chy_price,3)}' WHERE id='14'")
        await cur.execute(f"UPDATE cripts SET usd='{round(ethereum_usd_price,3)}',chy='{round(ethereum_chy_price,3)}' WHERE id='15'")
        await cur.execute(f"UPDATE cripts SET chy='{round(valute_chy_price,3)}' WHERE id='1'")
        await base.commit()
        
        
        await asyncio.sleep(180)