import asyncio
import psycopg2 as sq
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher.filters import Text
from handlers import registration


balance_casino_spin=10000
class FSMcasino(StatesGroup):
    stavka=State()

async  def cancel_handler(message: types.Message,state:FSMContext):
    current_state=await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Вы вышли из казино!')


async def Start_casino(message: types.Message,state: FSMContext):
    global base, cur
    base = sq.connect(dbname='d9882ng2h7srs6', user='rixdvqeatezwpn',
                      password='60e4ac9ad7bcb8be1b8900f38fc0c70a52a69fb6dcdd59bf553c6262631f54a6', host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com')
    cur=base.cursor()
    cur.execute(f"SELECT balance FROM profile WHERE id='{message.from_user.id}'")
    for test in cur.fetchall():
        balance_v_bd=float(test[0])
    if balance_v_bd<=0:
        await message.answer('Недостаточно средст!')
        return
    if registration.IsRegistration(message.from_user.id)==False:
        await message.answer('/reg - Вначале зарегистрируйтесь!')
        return
    await message.reply('/cancel- отмена')
    await FSMcasino.stavka.set()
    # await asyncio.sleep(10)
    # wait_stavka=await state.get_data()
    # if wait_stavka.get('stavka')==None:
    #     await message.answer('Время ожидания вышло!')
    #     await state.finish()
        
async def dice_casino(message: types.Message,state: FSMContext):
    async with  state.proxy() as data:
        data['stavka']=message.text
    sdel=await state.get_data()
    stavka_sdel=sdel.get('stavka')
    if stavka_sdel.replace('.','',1).isdigit() or stavka_sdel.replace(',','',1).isdigit() :
        if registration.IsRegistration(message.from_user.id)==False:
            await message.answer('/reg - Вначале зарегистрируйтесь!')
            return
        cur.execute(f"SELECT balance FROM profile WHERE id='{message.from_user.id}'")
        for test in cur.fetchall():
            balance_v_bd=float(test[0])
        if float(stavka_sdel.replace(',','.'))<=0:
            await message.answer('Ставка ниже 0 !?')
            return 
        elif balance_v_bd<float(stavka_sdel.replace(',','.')):
            await message.answer('Недостаточно средст!')
            return 
        slot_machine_value = [
            ["bar | bar | bar"],
            ["grape | bar | bar"],
            ["lemon | bar | bar"],
            ["seven | bar | bar"],
            ["bar | grape | bar"],
            ["grape | grape | bar"],
            ["lemon | grape | bar"],
            ["seven | grape | bar"],
            ["bar | lemon | bar"],
            ["grape | lemon | bar"],
            ["lemon | lemon | bar"],
            ["seven | lemon | bar"],
            ["bar | seven | bar"],
            ["grape | seven | bar"],
            ["lemon | seven | bar"],
            ["seven | seven | bar"],
            ["bar | bar | grape"],
            ["grape | bar | grape"],
            ["lemon | bar | grape"],
            ["seven | bar | grape"],
            ["bar | grape | grape"],
            ["grape | grape | grape"],
            ["lemon | grape | grape"],
            ["seven | grape | grape"],
            ["bar | lemon | grape"],
            ["grape | lemon | grape"],
            ["lemon | lemon | grape"],
            ["seven | lemon | grape"],
            ["bar | seven | grape"],
            ["grape | seven | grape"],
            ["lemon | seven | grape"],
            ["seven | seven | grape"],
            ["bar | bar | lemon"],
            ["grape | bar | lemon"],
            ["lemon | bar | lemon"],
            ["seven | bar | lemon"],
            ["bar | grape | lemon"],
            ["grape | grape | lemon"],
            ["lemon | grape | lemon"],
            ["seven | grape | lemon"],
            ["bar | lemon | lemon"],
            ["grape | lemon | lemon"],
            ["lemon | lemon | lemon"],
            ["seven | lemon | lemon"],
            ["bar | seven | lemon"],
            ["grape | seven | lemon"],
            ["lemon | seven | lemon"],
            ["seven | seven | lemon"],
            ["bar | bar | seven"],
            ["grape | bar | seven"],
            ["lemon | bar | seven"],
            ["seven | bar | seven"],
            ["bar | grape | seven"],
            ["grape | grape | seven"],
            ["lemon | grape | seven"],
            ["seven | grape | seven"],
            ["bar | lemon | seven"],
            ["grape | lemon | seven"],
            ["lemon | lemon | seven"],
            ["seven | lemon | seven"],
            ["bar | seven | seven"],
            ["grape | seven | seven"],
            ["lemon | seven | seven"],
            ["seven | seven | seven"],
        ]
        casino = await message.answer_dice('🎰')
        # print(slot_machine_value[casino.dice.value-1])
        if slot_machine_value[casino.dice.value-1]==slot_machine_value[1] or slot_machine_value[casino.dice.value-1]==slot_machine_value[21] \
            or slot_machine_value[casino.dice.value-1]==slot_machine_value[42]:
            stavka_ucht=float(stavka_sdel.replace(',','.')) * 3.5
            itog=(balance_v_bd-float(stavka_sdel.replace(',','.')))+stavka_ucht
            await asyncio.sleep(2)
            # await message.reply(slot_machine_value[casino.dice.value-1])
            await message.reply(f'Ставка: {stavka_sdel}\nВы выиграли: {stavka_ucht}\nБаланс: {itog}')
            cur.execute(f"UPDATE profile SET balance='{itog}' WHERE id='{message.from_user.id}'")
            base.commit()
        elif slot_machine_value[casino.dice.value-1]==slot_machine_value[63]:
            stavka_ucht=float(stavka_sdel.replace(',','.')) * 3.5
            itog=(balance_v_bd-float(stavka_sdel.replace(',','.')))+stavka_ucht
            await asyncio.sleep(2)
            # await message.reply(slot_machine_value[casino.dice.value-1])
            await message.reply(f'Ставка: {stavka_sdel}\nВы выиграли: {stavka_ucht}\nБаланс: {itog}')
            cur.execute(f"UPDATE profile SET balance='{itog}' WHERE id='{message.from_user.id}'")
            base.commit()
        else:
            itog=balance_v_bd-float(stavka_sdel.replace(',','.'))
            await asyncio.sleep(2)
            # await message.reply(slot_machine_value[casino.dice.value-1])
            await message.reply(f'Вы проиграли: {stavka_sdel}\nБаланс: {itog}')
            cur.execute(f"UPDATE profile SET balance='{itog}' WHERE id='{message.from_user.id}'")
            base.commit()
        await state.finish()
    else:
        await message.answer('Некорректная ставка!?')
        return


def register_handlers_casino(dp: Dispatcher):
    dp.register_message_handler(Start_casino, commands=['casino','казино'],start=None)
    dp.register_message_handler(cancel_handler, state="*", commands =['отмена','cancel'])
    dp.register_message_handler(cancel_handler,Text(equals=['отмена','cancel'], ignore_case=True),state="*")
    dp.register_message_handler(dice_casino, state = FSMcasino.stavka)
