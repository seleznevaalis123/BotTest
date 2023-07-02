import telebot
from telebot.types import LabeledPrice, ShippingOption, InlineKeyboardButton, InlineKeyboardMarkup,\
    ReplyKeyboardMarkup, BotCommand, BotCommandScope, KeyboardButton
import config


bot = telebot.TeleBot(config.token)
currency = 'rub'

prices = [LabeledPrice(label='RoboCraft#0094 [stripeRobo]', amount=575000), LabeledPrice('TaxFee', 50000)]

shipping_options = [
    ShippingOption(id='instant', title='Fedex').add_price(LabeledPrice('Fedex', 575000)),
    ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Local pickup', 30000))]


'''catalog_list = InlineKeyboardMarkup(row_width=2)
catalog_list.add(InlineKeyboardButton(text="RoboCraft🤖", url='https://grandbazar.io/ru/collection/robocraft'),
                 InlineKeyboardButton(text="EverLands🗺", url='https://grandbazar.io/ru/collection/everlands'),
                 InlineKeyboardButton(text="IFREELAND Passport☻", url='https://grandbazar.io/ru/collection/passport_freeland'))




bot.set_my_commands(
        commands=[
            BotCommand('0094', 'RoboCraf#0057'),
            BotCommand('0058', 'RoboCraf#0058'),
            BotCommand('0059', 'RoboCraf#0059')],
        scope=BotCommandScope())'''


@bot.message_handler(commands=['start'])
def command_start(message):
    bot.send_animation(message.chat.id,
                       animation="https://graphicdesignjunction.com/wp-content/uploads/2021/06/logo-animation-25.gif",
                       width=1600,
                       height=1200,)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    menuitem1 = KeyboardButton("🍽️ORDER FOOD")
    menuitem2 = KeyboardButton("🪷SPA")
    menuitem3 = KeyboardButton("🧘‍YOGA")
    menuitem4 = KeyboardButton("📣EVENTS")
    menuitem5 = KeyboardButton("⚙️BOT SETTINGS")
    markup.add(menuitem1, menuitem2, menuitem3, menuitem4, menuitem5)
    bot.send_message(message.chat.id, "Welcome to the Official TGBot TSPA!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.text == "🪷SPA":
        mainMenu = InlineKeyboardMarkup(row_width=2)
        menuitem1 = InlineKeyboardButton(text='📞WhatsApp', url="https://wa.me")
        backbutton = InlineKeyboardButton(text="Schedule", callback_data="bot_messageone")
        mainMenu.add(menuitem1, backbutton)
        bot.send_message(message.chat.id, "Wellcome to the Spa!", reply_markup=mainMenu)


@bot.callback_query_handler
def bot_messageone(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    menuitem1 = KeyboardButton("🍽️ORDER FOOD")
    menuitem2 = KeyboardButton("🪷SPA")
    menuitem3 = KeyboardButton("🧘‍YOGA")
    menuitem5 = KeyboardButton("⚙️BOT SETTINGS")
    markup.add(menuitem1, menuitem2, menuitem3, menuitem5)
    bot.send_message(message.chat.id, "Welcome to the Official TGBot TSPA!", reply_markup=markup)


@bot.message_handler(commands=['help'])
def command_terms(message):
    bot.send_message(message.chat.id,
                     'For any question contact our support @support')


@bot.message_handler(commands=['0094'])
def command_pay(message):
    bot.send_message(message.chat.id,
                     "Insert this Card number: `4242 4242 4242 4242`"
                     "\n\nThis is your demo invoice:", parse_mode='Markdown')
    bot.send_invoice(message.chat.id,   # chat_id
                     'RoboCraft#0094 [stripeRobo]',  # title
                     'RoboCraft#0094 [stripeRobo] has generated',  # description
                     'HAPPY FRIDAYS COUPON',  # invoice_payload
                     config.provider_token,  # provider_token
                     currency,  # currency
                     prices,  # prices
                     photo_url="https://grandbazar.io/static/item/6182383f276c770013f8a0a2/59c9491f42741ce7dfcf@medium.png",
                     photo_height=490,  # !=0/None or picture won't be shown
                     photo_width=490,
                     photo_size=35069,
                     is_flexible=True,  # True If you need to set up Shipping Fee
                     start_parameter='iphone-example')


@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    print(shipping_query)
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                              error_message='Oh, Try again later!')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Someone tried to steal your card's CVV,"
                                                " try to pay again in a few minutes, we need a small rest.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'Thanks for order!♡ '.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')
    bot.send_poll(message.chat.id, question="Rate our marketplace", options=["😃", "😟", "😤"], is_anonymous=True)


bot.infinity_polling(skip_pending=True)
