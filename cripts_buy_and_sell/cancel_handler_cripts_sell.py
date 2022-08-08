from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext



async  def cancel_handler_sell(callback: types.CallbackQuery,state:FSMContext):
    cripts_sell_cancel=callback.data.split('_')[4]
    if callback.from_user.id == int(cripts_sell_cancel):
        await callback.message.delete()
        current_state=await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await callback.message.answer('Вы отказались от продажи!')
        await callback.answer()
    else:
        await callback.answer(text='Не твое сообщени!', show_alert=True)


def register_handlers_cancel_handler_sell(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_handler_sell,lambda callback: callback.data.startswith('cancel_state_cripts_sell_'),state="*")
