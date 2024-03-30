
from aiogram import Dispatcher, Bot, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from klava import klava
from config import TOKEN

import time
import datetime



bot = Bot(TOKEN)
dp = Dispatcher(bot, storage= MemoryStorage())

baza = {}

class state_baza(StatesGroup):
    name = State()
    description = State()
    deadline = State()
    frequency = State()


@dp.message_handler(commands= ['start'], state='*')
async def start(message:types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.chat.id, f'Hi {message.chat.full_name}', reply_markup=klava)



@dp.message_handler(text= '> CREATE <', state='*')
async def create(message:types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Print name task: ')
    await state_baza.name.set()




@dp.message_handler(text= '>LIST<', state='*')
async def list_task(message:types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    text_list = "TASK LIST:\n"
    
    for task_id, task_data in baza[user_id].items():
        text_list += f'''
        TASK {task_id}:
        name = {task_data['name']}
        description = {task_data['description']}
        deadline = {task_data['deadline']}
        frequency = {task_data['frequency']}
        \n
        '''
    
    await bot.send_message(message.chat.id, text_list)




@dp.message_handler(state= state_baza.name)
async def save_name(message: types.message, state: FSMContext):
    user_id = message.from_user.id
    name = message.text
    
    task_id = 1
    async with state.proxy() as data:
        data['task_id'] = task_id
    

    
    if user_id not in baza:
        baza[user_id] = {}
    
    while True:
        if task_id not in baza[user_id]:
            baza[user_id][task_id] = {}
            break
        else:
            task_id += 1
    
    baza[user_id][task_id]['name'] = name
    
    await bot.send_message(message.chat.id, f'Name task "{baza[user_id][task_id]['name']}" is saved')
    await state_baza.next()
    await bot.send_message(message.chat.id, 'Print description task: ')



@dp.message_handler(state= state_baza.description)
async def save_description(message: types.message, state: FSMContext):
    user_id = message.from_user.id
    description = message.text
    
    task_id = 0
    async with state.proxy() as data:
        task_id = data['task_id']
    
    baza[user_id][task_id]['description'] = description
    await bot.send_message(message.chat.id, f'description "{baza[user_id][task_id]['description']}" is saved')
    await state_baza.next()
    await bot.send_message(message.chat.id, 'Print deadline task "YYYY/MM/DD/HH/MM": ')


@dp.message_handler(state= state_baza.deadline)
async def save_deadline(message: types.message, state: FSMContext):
    user_id = message.from_user.id
    
    task_id = 0
    async with state.proxy() as data:
        task_id = data['task_id']
    
    while True:
        deadline = message.text
        try:
            deadline = datetime.datetime.strptime(message.text, '%Y/%m/%d/%H/%M')
            break
        except ValueError:
            await bot.send_message(message.chat.id, 'Print deadline task "YYYY/MM/DD/HH/MM" again: ')
            await state_baza.deadline.set()
            return
    
    baza[user_id][task_id]['deadline'] = deadline
    await bot.send_message(message.chat.id, f'deadline "{baza[user_id][task_id]['deadline']}" is saved')
    await state_baza.next()
    await bot.send_message(message.chat.id, 'Print the frequency of notifications in seconds: ')
    
    
@dp.message_handler(state= state_baza.frequency)
async def save_frequency(message: types.message, state: FSMContext):
    user_id = message.from_user.id
    
    task_id = 0
    async with state.proxy() as data:
        task_id = data['task_id']
    
    while True:
        frequency = message.text
        try:
            frequency = int(message.text)
            break
        except ValueError:
            await bot.send_message(message.chat.id, 'Print the numbers: ')
            await state_baza.frequency.set()
            return
    
    
    baza[user_id][task_id]['frequency'] = frequency
    await bot.send_message(message.chat.id, f'frequency "{baza[user_id][task_id]['frequency']}" is saved')
    await state.finish()





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


