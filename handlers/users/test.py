from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.default import dynamic_reply_kb
from loader import dp
from states.test_states import TestStates

buttons = [
    ['Китай', 'Індія', 'США'],
    ['Євразія', 'Африка', 'Австралія'],
    ['Земля', 'Сатурн', 'Марс']
]
correct_answers = ['Індія', 'Євразія', 'Марс']

@dp.message_handler(commands='starttest')
async def starttest(message: types.Message, state: FSMContext):
    await message.answer('Розпочнімо міні-тест!')
    await message.answer('Перше питання: \nНайгустонаселеніша країна світу?', reply_markup=dynamic_reply_kb(buttons[0]))
    await TestStates.second_q.set()

@dp.message_handler(text=['Китай', 'Індія', 'США'], state=TestStates.second_q)
async def second_q(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Індія':
            data['first'] = "Правильна відповідь"
        else:
            data['first'] = "Неправильна відповідь. Правильна відповідь: Індія"
    await message.answer('Ваша відповідь зарахована.')
    await message.answer('Друге питання: \nЯкий континент омивають всі океани?', reply_markup=dynamic_reply_kb(buttons[1]))
    await TestStates.third_q.set()

@dp.message_handler(text=['Євразія', 'Африка', 'Австралія'], state=TestStates.third_q)
async def third(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Євразія':
            data['second'] = "Правильна відповідь"
        else:
            data['second'] = "Неправильна відповідь. Правильна відповідь: Євразія"
    await message.answer('Ваша відповідь зарахована.')
    await message.answer('Трет питання: \nТретє питання: яка планета відома як \"Червона планета\"?', reply_markup=dynamic_reply_kb(buttons[2]))
    await TestStates.result.set()

@dp.message_handler(text=['Земля', 'Сатурн', 'Марс'], state=TestStates.result)
async def result(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Марс':
            data['third'] = "Правильна відповідь"
        else:
            data['third'] = "Неправильна відповідь. Правильна відповідь: Марс"
    await message.answer('Ваша відповідь зарахована.')
    counter = 0
    async with state.proxy() as data:
        for answer in data.values():
            if answer == 'Правильна відповідь':
                counter += 1

    await message.answer(f'Вітаємо! Тест завершено. Ваш результат: {counter}/3. Хочете переглянути детальніше?', reply_markup=ReplyKeyboardMarkup().add(KeyboardButton('Так'), KeyboardButton('Ні')))
    await TestStates.choice.set()

@dp.message_handler(text=['Так', 'Ні'], state=TestStates.choice)
async def choice(message: types.Message, state: FSMContext):
    if message.text == 'Так':
        async with state.proxy() as data:
            await message.answer(f'Перше питання: {data["first"]}\nДруге питання: {data["second"]}\nТретє питання: {data["third"]}')
    await message.answer('Дякуємо за проходження!❤️')
    await state.reset_state()