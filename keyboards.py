from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


cancel_btn = "❌ Отмена"
proceed_btn = "✔ Продолжить"
confirm_btn = "✔ Все верно"

last5_btn = "🌟 Last 5ive"
all_btn = "📚 All"
search_btn = "🔎 Search"
next_btn = "🌟 Next 5ive"
about_btn = "About Me"

main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
# main_menu_keyboard.insert(KeyboardButton(last5_btn))
main_menu_keyboard.insert(KeyboardButton(all_btn))
main_menu_keyboard.insert(KeyboardButton(search_btn))
main_menu_keyboard.add(KeyboardButton(about_btn))
