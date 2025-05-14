import telebot
from telebot import types
import random
import os
from  threading import Thread
from flask import Flask
import sqlite3
from dotenv import load_dotenv

load_dotenv("api.env")

# Функция для отправки фото
def send_photo_safe(chat_id, photo_path, caption):
    try:
        with open(photo_path, 'rb') as photo:
            bot.send_photo(chat_id, photo, caption=caption)
        return True
    except FileNotFoundError:
        bot.send_message(chat_id, caption) 
        return False
    except Exception as e:
        print(f"Ошибка при отправке фото: {e}")
        bot.send_message(chat_id, caption)
        return False
    
db = sqlite3.connect("users.db", check_same_thread=False)
cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    score INTEGER DEFAULT 0,
    attempts INTEGER DEFAULT 0
)""")
db.commit()
API_TOKEN = os.getenv("TG_TOKEN") 
bot = telebot.TeleBot(API_TOKEN)

quiz_questions = [
    {
        "question": "Из какого материала делали берестяные грамоты?",
        "options": ["Кора березы", "Пергамент", "Глина", "Металл"],
        "correct_answer": 0,
        
    },
    {
        "question": "В каком городе найдены древнейшие берестяные грамоты?",
        "options": [ "Киев", "Новгород", "Москва", "Владимир"],
        "correct_answer": 1
    },
    {
        "question": "Какое метательное оружие было основным до появления огнестрельного?",
        "options": ["Лук", "Меч", "Копьё", "Топор"],
        "correct_answer": 0
    },
    {
        "question": "Из чего делали древнерусские луки?",
        "options": ["Только из дерева", "Из дерева, рога и сухожилий", "Из металла и кожи", "Из камня и кости"],
        "correct_answer": 1
    },
    {
        "question": "Какой максимальный вес могли метать 'великие пороки'?",
        "options": ["До 50 кг", "До 100 кг", "До 200 кг", "До 500 кг"],
        "correct_answer": 2
    },
    {
        "question": "Как назывались суда, которые можно было перетаскивать волоком между реками?",
        "options": ["Струги", "Чайки", "Барки", "Ладьи"],
        "correct_answer": 3
    },
    {
        "question": "Какой материал НЕ использовался при изготовлении кольчуг?",
        "options": ["Железные кольца", "Клепаные соединения", "Сварные элементы", "Золотая проволока"],
        "correct_answer": 3
    },
    {
        "question": "Какой регион Руси славился белокаменным строительством?",
        "options": ["Владимиро-Суздальское княжество", "Новгородская земля", "Смоленское княжество", "Киевское княжество"],
        "correct_answer": 0
    },
    {
        "question": "Сколько весила готовая кольчуга?",
        "options": ["8-16 кг", "1-2 кг", "6-7 кг", "20-25 кг"],
        "correct_answer": 0
    },
    {
        "question": "Какие прялки украшали солнечными символами?",
        "options": ["Южнорусские", "Северные", "Центральной России", "Украинские"],
        "correct_answer": 1
    },
    {
        "question": "Из какого дерева чаще всего плели лапти?",
        "options": ["Дуб", "Сосна", "Липа", "Бук"],
        "correct_answer": 2
    },
    {
        "question": "Сколько времени уходило на изготовление одной кольчуги?",
        "options": ["от 3 до 6 месяцев", "от 1 до 2 недель", "от 6 до 12 месяцев", "более года"],
        "correct_answer": 0
    },
    {
        "question": "Какой князь начал белокаменное строительство?",
        "options": ["Ярослав Мудрый", "Юрий Долгорукий", "Владимир Мономах", "Александр Невский"],
        "correct_answer": 1
    },
    {
        "question": "Как называлась книга, написанная на Руси, содержащая свод церковных правил и уставов? ",
        "options": ["Слово о полку Игореве", "Повесть временных лет", "Кормчая книга", "Русская Правда"],
        "correct_answer": 2
    },
    {
        "question": "Какие стрелы использовались против доспехов?",
        "options": ["Срезни", "Бронебойные", "Зажигательные", "Охотничьи"],
        "correct_answer": 1
    },
    
    {
        "question": "Где найдено больше всего берестяных грамот?",
        "options": ["Владимир", "Киев", "Великий Новгород", "Москва"],
        "correct_answer": 2
    },
    {
        "question": "Сколько лык использовали для зимних лаптей?",
        "options": ["3", "5", "7", "9"],
        "correct_answer": 2
    },
    {
        "question": "Как называлось приспособление, которое использовали на Руси для переноски воды и других жидкостей, состоящее из деревянной дуги с крючками и двух ведер?",
        "options": ["Коромысло", "Штанга", "Перкладина", "Водонос"],
        "correct_answer": 0
    },
    {
        "question": "Какое дерево НЕ использовали для изготовления прялок?",
        "options": ["Липа", "Осина", "Берёза", "Сосна"],
        "correct_answer": 3
    },
    {
        "question": "Какой тип судов мог перевозить до 20 тонн груза?",
        "options": ["Струг", "Ладья", "Чёлн", "Байдара"],
        "correct_answer": 1
    },
     {
        "question": "Какой диаметр проволоки использовался для ковки кольчужных колец?",
        "options": ["1-2 мм", "3-5 мм", "15-20 мм", "7-12 мм"],
        "correct_answer": 3
    },
    {
        "question": "На какое максимальное расстояние могли метать груз великие пороки?",
        "options": ["до 200 метров", "до 250 метров", "до 500 метров", "до 800 метров"],
        "correct_answer": 3
    },
    {
        "question": "Во сколько лет детей начинали учить плетению лаптей?",
        "options": ["7-8 лет", "9-10 лет", "5-6 лет", "11-12 лет"],
        "correct_answer": 0
    },
    {
        "question": "Как назывались передвижные осадные орудия?",
        "options": ["Гуляй-город", "Пороки", "Тараны", "Вежи"],
        "correct_answer": 1
    },
]

# Глобальные переменные для викторины
user_data = {}  # Хранит данные пользователей: {user_id: {"score": 0, "current_question": 0, "questions": []}}

# /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    user_data[user_id] = {"score": 0, "current_question": 0, "questions": []}
    
    bot.send_message(
        message.chat.id,
        "🏰 Добро пожаловать в бота о средневековых изобретениях Руси!\n"
        "Выберите действие:",
        reply_markup=create_main_menu()
    )



# Данные об изобретениях с локальными путями к изображениям
inventions = {
    "Лук и стрелы": {
        "description": "Лук и стрелы известны на территории будущей Руси с глубокой древности. Археологические находки свидетельствуют, что ими пользовались ещё племена восточных славян, финно-угров и балтов в раннем Средневековье. Позже, в эпоху Древней Руси (IX–XIII вв.), лук стал одним из основных видов оружия как у пеших воинов, так и у конницы. Русские луки были сложносоставными – их изготавливали из дерева (береза, ясень), рога и сухожилий, что делало их мощными и гибкими. Такой лук мог пробивать доспехи на расстоянии до 200 метров.\nСтрелы были разных типов:\n• Бронебойные (с узким наконечником для пробивания доспехов)\n• Срезни (широкие наконечники для поражения незащищённых частей тела)\n• Зажигательные (использовались при осадах)\n",
        "photo_path": "images/bow.jpg"  # Путь к локальному файлу
    },
    "Берестяные грамоты": {
        "description": ("Берестяные грамоты — письма и записи на коре берёзы, памятники письменности Древней Руси XI—XV веков. Найдено более тысячи грамот в Великом Новгороде и ещё более сотни в других городах России, Украины и Белоруссии. Известны также находки русских берестяных грамот XVI—XVII веков в Поволжье, Сибири и на Дальнем Востоке России. Берестяные грамоты представляют первостепенный интерес как источники по истории общества и повседневной жизни средневековых людей, а также по истории восточнославянских языков."),
        "photo_path": "images/beresta.png"
    },
    "Колокола": {
        "description": ("Колокола появились на Руси после Крещения (988 г.) и быстро стали важной частью церковной и городской жизни. Их звон сопровождал богослужения, оповещал о пожарах и вражеских набегах, созывал народ на вече. Колокола на Руси отливали из колокольной меди и олова или бронзы, из серебра. Чем чище были олово и медь, тем лучше было качество звука."),
        "photo_path": "images/tsar.jpg"
    },
    "Белокаменное строительство": {
        "description":"""белокаменное строительство – это кладка из аккуратно отесанных известняковых блоков. В Киевской Руси из белого камня не строили. Не были ничего подобного ни в Чернигове, ни в Новогороде, ни в Рязани, ни в одном другом русском княжестве, кроме Галицкого. Везде строили из кирпича (плинфы), либо смешанную кладку использовали. А во Владимиро-Суздальском княжестве в домонгольский период (до 1238 года) абсолютное большинство крупных построек было белокаменными. Московские князья в послемонгольское время до середины XV века также капитальное строительство вели в белокаменной технике. А начал белокаменное строительство Юрий Долгорукий, несмотря на то, что и в Византии, откуда на Русь пришли традиции строительства христианских храмов, строили из кирпича либо в смешанной технике.
""",
        "photo_path": "images/cof.jpg"
    },
    "Кольчуга": {
        "description": 'Кольчуга была одним из главных защитных доспехов русских воинов на протяжении многих веков - с IX по XVII столетие. Этот гибкий доспех из множества металлических колец носили князья, дружинники и профессиональные воины. В отличие от тяжелых рыцарских лат Западной Европы, русская кольчуга обеспечивала хорошую подвижность, что было особенно важно в степных сражениях и быстрых конных атаках. Первые кольчуги появились на Руси в IX-X веках под влиянием кочевников - хазар и печенегов. Уже к XI-XIII векам они стали массовым доспехом княжеских дружинников. Изготовление кольчуги было долгим и трудоемким процессом. Мастера сначала ковали из железной проволоки тысячи колец диаметром 7-12 мм, затем каждое кольцо особым образом продевали в четыре соседних по схеме "4 в 1". Часть колец сваривали для прочности, часть склепывали. На изготовление одной кольчуги уходило от 3 до 6 месяцев кропотливой работы! Готовая кольчуга весила 8-16 кг',
        "photo_path": "images/kol.jpg"
    },
    "Мельницы": {
        "photo_path": "images/mel.jpg",
        "description": "Мельницы в средневековой Руси были важным элементом сельской экономики и играли значительную роль в жизни людей того времени. Они использовались для помола зерна, что было ключевым процессом в производстве муки для хлеба — основного продукта питания.\nВ средневековой Руси использовались два типа мельниц:\nВодяные мельницы — работали за счёт силы течения реки. Вода направлялась на лопасти колеса, которое приводил в движение механизм для помола зерна.\nВетряные мельницы — использовали силу ветра для вращения лопастей, которые, в свою очередь, приводили в движение мельничные камни.\nМельницы позволяли массово перемалывать зерно, что обеспечивало население мукой и способствовало развитию сельского хозяйства и торговли. Мельницы часто строились на возвышенностях или вблизи рек, чтобы максимально эффективно использовать доступные природные ресурсы."
    },
    "Метательные машины": {
        "photo_path": "images/porok.jpg",
        "description": "На руси имелось общее название метательных машин - пороки — это древнерусские метательные машины, использовавшиеся в основном при осаде и обороне крепостей в X–XV веках. Они представляли собой камнемётные или стреломётные орудия, работавшие по принципу рычага или противовеса.Применялись при обороне и осаде вражеских крепостей. Разделялись на малые и великие пороки. Последние могли метать груз (камень, бревно и другое) весом до 200 килограмм на расстояние до 800 метров."
    },
    "Деревянное зодчество": {
        "photo_path" : 'images/Kizhi.jpg',
        "description": "Русское деревянное зодчество — сложившееся на Руси направление традиционной архитектуры, имеющее устойчивые и ярко выраженные конструктивно-технические и архитектурно-художественные особенности, которые определяются деревом как основным материалом. Конструктивная основа русского деревянного зодчества — сруб из необтёсанных брёвен. Декором служила резьба по дереву, размещавшаяся на конструктивно значимых элементах. Среди традиционных построек выделяются деревянные клетские, шатровые, ярусные, кубоватые и многоглавые церкви, которые вместе с крестьянскими избами, хоромами, хозяйственными, крепостными и инженерными постройками определяли облик традиционного русского поселения."
    },
    "Ладья":{
        "photo_path": "images/ladia.jpg",
        "description": "Ладья — древнерусское и поморское парусно-вёсельное морское и речное судно, предназначенное для гражданских и военных целей. При преодолении естественных или искусственных препятствий, недоступных для судоходства, ладьи тащились волоком. Наиболее ранние свидетельства использования в Древней Руси клинкерных дощатых судов ладейного типа прослеживаются с IX века по находкам в Старой Ладоге досок судовой обшивки, железных заклёпок и Т-образной стойки судового навеса. Согласно письменным источникам, Древнерусское государство в IX веке обладало флотом, состоящим из как минимум 200 ладей.Длина ладей составляла около 25 метров, ширина около 8 метров. Грузоподъёмность — до 20 тонн. Ладья имела вёсла и парус."
    },
    "Сани":{
        "photo_path": "images/sani.jpg",
        "description": "Сани– это повозка на полозьях, легко скользящих по снегу. Само слово «сани» появилось в русском языке, а оттуда уже перекочевало в латышский, венгерский, румынский. Самой распространенной считается версия происхождения «саней» от слова «сань», что означало «змея». С этим пресмыкающимся сравнивали след от полозьев. Сани были усовершенствованной версией волокуши — конструкции из двух жердей, соединенных между собой. Задние концы волочились по земле, а к передним привязывали животное: собаку, лошадь, быка, оленя. На Руси сани считались даже более престижным средством передвижения, чем колесные повозки. Вплоть до начала XVIII века на особенно торжественные мероприятия знать и высшие духовные лица выезжали на санях даже летом. онструкция саней с годами улучшилась: из перекрещенных жердей сани превратились в ладью с загнутыми полозьями. В них обычно запрягали одну лошадь, верхом на которой ехал кучер. По саням можно было определить степень знатности их владельца. Богаче всего, конечно, украшали царские."
    },
    "Колесные повозки": 
    {   "photo_path": "images/pov.jpg",
        "description": 'Колесные повозки на Руси появились в глубокой древности, став важнейшим средством передвижения и перевозки грузов в бесснежный период года. Эти четырехколесные конструкции, медленные и неуклюжие, тем не менее прекрасно справлялись с перевозкой урожая, дров по грунтовым дорогам. Славяне, в отличие от других народов, предпочитали более практичные грузовые возы. С развитием Древнерусского государства в X-XV веках колесный транспорт значительно усовершенствовался. Под влиянием Византии и европейских стран на Руси появились более легкие повозки со спицевыми колесами. Для знати стали делать специальные крытые колымаги - прообраз будущих карет. Простые же крестьяне продолжали пользоваться традиционными телегами, которые в разных регионах имели свои особенности: на юге делали более легкие повозки для степных дорог, а в северных лесах - массивные, с широкими колесами для болотистой местности.'
    },
    "Прялка":{
        "description": "Прялки на Руси являлась настоящим символом женского труда и народной культуры. Эти незамысловатые приспособления состаяли из вертикальной стойки с лопастью и горизонтального донца, на котором сидела пряха. Основным материалом для изготовления прялок служили липа, осина или берёза - мягкие породы дерева, легко поддающиеся обработке. Интересно, что в разных регионах Руси сложились свои традиционные формы и украшения прялок: на севере их покрывали сложной резьбой с солнечными символами и коньками, в Центральной России преобладала геометрическая резьба, а в южных губерниях часто встречалась яркая роспись цветочными узорами. Технология прядения на русских прялках оставалась неизменной веками: пряха левой рукой вытягивала волокно из кудели (подготовленной шерсти или льна), а правой вращала веретено, на которое наматывалась готовая нить. Этот труд занимал долгие зимние вечера - чтобы спрясть нить на одну рубаху, требовалось около двух недель кропотливой работы.",
        "photo_path": "images/pryalka.jpg"
    },
    "Лапти":
    {   "photo_path": "images/lapti.jpg",
        "description": "Лапти – это обувь, которую на протяжении многих веков носили крестьяне на Руси. Плели лапти из коры  лиственных деревьев: липы, березы, вяза, дуба, ракиты…Самыми прочными и удобными считались лыковые лапти, изготовленные из липового лыка, а самыми плохими — ивовые коверзни и мочалыжники. Лапти назывались по числу лыковых полос, использованных в плетении: пятерик, шестерик, семерик. В семь лык обычно плели зимние лапти. Для прочности, тепла и красоты лапти проплетали вторично, для чего применяли пеньковые веревки. С этой же целью иногда пришивали кожаную подметку. Плели лапти, как правило, мужчины и мальчики-подростки. Это считалось исключительно мужским занятием, женщинам доверяли только «ковырять» подошвы. Умение женщины сплести хороший лапоть вызывало недоверие мужчин и особое уважение односельчанок. Обучать мальчиков плетению лаптей начинали рано, в 7 – 8 лет, а к 10-12 годам подросток мог сплести лапти не хуже взрослого."
    }
    
}
#main menu
def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📜 Список изобретений"),
        types.KeyboardButton("🎮 Викторина"), 
        types.KeyboardButton("🏆 Таблица участников"),
        types.KeyboardButton("ℹ️ О боте"),  
        
    )
    return markup

# invention's menu
def create_categories_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Военные изобретения", callback_data="cat_military"),
        types.InlineKeyboardButton("Строительство и архитектура", callback_data="cat_construction"),
        types.InlineKeyboardButton("Транспорт", callback_data="cat_transport"),
        types.InlineKeyboardButton("Быт", callback_data="cat_life")
    )
    return markup

# military's menu
def create_military_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Лук и стрелы", callback_data="inv_Лук и стрелы"),
        types.InlineKeyboardButton("Кольчуга", callback_data="inv_Кольчуга"),
        types.InlineKeyboardButton("Метательные машины", callback_data="inv_Метательные машины"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_categories")
    )
    return markup

# building's menu
def create_construction_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        
        types.InlineKeyboardButton("Деревянное зодчество", callback_data="inv_Деревянное зодчество"),
        types.InlineKeyboardButton("Мельницы", callback_data="inv_Мельницы"),
        types.InlineKeyboardButton("Белокаменное строительство", callback_data="inv_Белокаменное строительство"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_categories")
    )
    return markup

# transport's menu
def create_transport_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Ладьи", callback_data="inv_Ладья"),
        types.InlineKeyboardButton("Сани", callback_data="inv_Сани"),
        types.InlineKeyboardButton("Колесные повозки", callback_data="inv_Колесные повозки"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_categories")
    )
    return markup

# life menu
def create_life_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Берестяные грамоты", callback_data="inv_Берестяные грамоты"),
        types.InlineKeyboardButton("Прялка", callback_data="inv_Прялка"),
        types.InlineKeyboardButton("Лапти", callback_data="inv_Лапти"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_categories")
    )
    return markup

# Обработчик кнопки "Список изобретений"
@bot.message_handler(func=lambda msg: msg.text == "📜 Список изобретений")
def show_inventions(message):
    bot.send_message(
        message.chat.id,
        "🔍 Выберите категорию изобретений:",
        reply_markup=create_categories_menu()
    )


@bot.message_handler(func=lambda msg: msg.text == "🏆 Таблица участников")
def show_table(message):
    try:
        # Получаем данные, сортированные по убыванию баллов
        cursor.execute("""
            SELECT user_id, first_name, last_name, username, score, attempts 
            FROM users 
            WHERE score > 0
            ORDER BY score DESC, attempts DESC
            LIMIT 20
        """)
        top_users = cursor.fetchall()
        
        if not top_users:
            bot.send_message(message.chat.id, "Пока никто не прошел викторину!")
            return

        # Формируем таблицу
        table = "🏆 ТОП-20 участников 🏆\n\n"
        table += "№ | Участник | Баллы | Попытки\n"
        table += "―|――――――――|―――――|――――――\n"
        
        for i, user in enumerate(top_users, 1):
            user_id, first_name, last_name, username, score, attempts = user
            
            # Формируем отображаемое имя
            name_parts = []
            if first_name:
                name_parts.append(first_name)
            if last_name:
                name_parts.append(last_name)
            if not name_parts and username:
                name_parts.append(f"@{username}")
            
            display_name = " ".join(name_parts) if name_parts else f"ID: {user_id}"
            
            table += f"{i} | {display_name[:15]} | {score}/24 | {attempts}\n"
        
        bot.send_message(message.chat.id, f"<pre>{table}</pre>", parse_mode="HTML")
        
    except Exception as e:
        print(f"Ошибка при выводе таблицы: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка при загрузке таблицы лидеров")

        
# Обработчик callback-запросов для категорий
@bot.callback_query_handler(func=lambda call: call.data.startswith("cat_"))
def handle_category_selection(call):
    category = call.data[4:]
    
    if category == "military":
        bot.edit_message_text(
            "🏹 Военные изобретения:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=create_military_menu()
        )
    elif category == "construction":
        bot.edit_message_text(
            "🏗 Строительные изобретения:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=create_construction_menu()
        )
    elif category == "transport":
        bot.edit_message_text(
            "🚜 Транспортные изобретения:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=create_transport_menu()
        )
    elif category == "life":
        bot.edit_message_text(
            "🏠 Быт и повседневная жизнь:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=create_life_menu()
        )

# Обработчик кнопки "Назад"
@bot.callback_query_handler(func=lambda call: call.data == "back_to_categories")
def handle_back_button(call):
    bot.edit_message_text(
        "🔍 Выберите категорию изобретений:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=create_categories_menu()
    )

# Обработчик для изобретений (остается без изменений)
@bot.callback_query_handler(func=lambda call: call.data.startswith("inv_"))
def send_invention_info(call):
    invention = call.data[4:]
    if invention in inventions:
        data = inventions[invention]
        caption = f"🏛 *{invention.capitalize()}*\n\n{data['description']}"
        
        if 'photo_path' in data:
            if isinstance(data['photo_path'], list):
                for photo in data["photo_path"]:
                    send_photo_safe(call.message.chat.id, photo, caption)
                    caption = None
            else:
                send_photo_safe(call.message.chat.id, data["photo_path"], caption)
        else:
            bot.send_message(call.message.chat.id, caption, parse_mode="Markdown")

# Запуск викторины
@bot.message_handler(func=lambda msg: msg.text == "🎮 Викторина")
def start_quiz(message):
    user_id = message.chat.id
    user_data[user_id] = {
        "score": 0,
        "current_question": 0,
        "questions": random.sample(quiz_questions, 24)
    }
    
    send_quiz_question(user_id)

# Отправка вопроса викторины
def send_quiz_question(user_id):
    data = user_data[user_id]
    question_num = data["current_question"]
    question_data = data["questions"][question_num]
    
    markup = types.InlineKeyboardMarkup()
    for i, option in enumerate(question_data["options"]):
        markup.add(types.InlineKeyboardButton(option, callback_data=f"quiz_{i}"))
    
    # Отправляем вопрос
    
    try:
            bot.send_photo(
                user_id,
                photo=question_data["image"],
                caption=f"❓ Вопрос {question_num + 1}/24:\n\n{question_data['question']}",
                reply_markup=markup
            )
            return
    except:
            pass
    
    bot.send_message(
        user_id,
        f"❓ Вопрос {question_num + 1}/24:\n\n{question_data['question']}",
        reply_markup=markup
    )

# Обработка ответа на викторину
@bot.callback_query_handler(func=lambda call: call.data.startswith("quiz_"))
def handle_quiz_answer(call):
    user_id = call.message.chat.id
    chosen_option = int(call.data[5:])
    data = user_data[user_id]
    question_data = data["questions"][data["current_question"]]
    
    # Проверка ответа
    if chosen_option == question_data["correct_answer"]:
        data["score"] += 1
        feedback = "✅ Верно!"
    else:
        correct_answer = question_data["options"][question_data["correct_answer"]]
        feedback = f"❌ Неверно! Правильный ответ: {correct_answer}"
    
    # Отправляем feedback
    bot.send_message(user_id, feedback)
    
    # Переход к следующему вопросу или завершение
    data["current_question"] += 1
    if data["current_question"] <24:
        send_quiz_question(user_id)
    else:
        show_quiz_results(user_id)

# Показ результатов викторины
def show_quiz_results(user_id):
    score = user_data[user_id]["score"]
    
    try:
        # Получаем информацию о пользователе
        user = bot.get_chat(user_id)
        if score >=21:
            result = "🎉 Отлично! Вы настоящий знаток!"
        elif score >= 15:
            result = "👍 Хороший результат!"
        else:
            result = "📚 Вам есть куда расти!"
        bot.send_message(
        user_id,
        f"🏆 Викторина завершена!\n\n"
        f"Ваш результат: {score}/24\n\n"
        f"{result}\n\n")
        # Обновляем данные в БД
        cursor.execute("""
            INSERT OR REPLACE INTO users 
            (user_id, username, first_name, last_name, score, attempts) 
            VALUES (?, ?, ?, ?, ?, COALESCE((SELECT attempts FROM users WHERE user_id = ?), 0) + 1)
            """, 
            [user_id, user.username, user.first_name, user.last_name, score, user_id])
        db.commit()
        
        # Получаем позицию в рейтинге
        cursor.execute("""
            SELECT COUNT(*) + 1 FROM users 
            WHERE score > ? OR (score = ? AND attempts < (SELECT attempts FROM users WHERE user_id = ?))
            """, [score, score, user_id])
        position = cursor.fetchone()[0]
        
    except Exception as e:
        print(f"Ошибка при сохранении результатов: {e}")
        position = "N/A"

# Информация о боте
@bot.message_handler(func=lambda msg: msg.text == "ℹ️ О боте")
def about_bot(message):
    bot.send_message(
        message.chat.id,
        "🤖 *Бот о средневековых изобретениях Руси*\n\n"
        "Здесь вы можете:\n"
        "• Узнать о древнерусских изобретениях 📜\n"
        "• Проверить знания в викторине 🎮\n\n"
        "Авторы: Саламатов Максим, Кувшинников Влад, Кузьмин Никита",
        parse_mode="Markdown",
        reply_markup=create_main_menu()
    )
'''
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run_flask).start()
'''
if __name__ == "__main__":
    print("Бот запущен!")
    #keep_alive()
    bot.infinity_polling() 
