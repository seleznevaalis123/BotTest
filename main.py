import telebot
from telebot.types import LabeledPrice, ShippingOption, InlineKeyboardButton, InlineKeyboardMarkup
import config

bot = telebot.TeleBot(config.token)
currency = 'rub'

prices = [LabeledPrice(label='RoboCraft#0094 [stripeRobo]', amount=575000), LabeledPrice('TaxFee', 50000)]

shipping_options = [
    ShippingOption(id='instant', title='Fedex').add_price(LabeledPrice('Fedex', 575000 )),
    ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Local pickup', 30000))]


catalog_list = InlineKeyboardMarkup(row_width=2)
catalog_list.add(InlineKeyboardButton(text="RoboCraft🤖", url='https://grandbazar.io/ru/collection/robocraft'),
                 InlineKeyboardButton(text="EverLands🗺", url='https://grandbazar.io/ru/collection/everlands'),
                 InlineKeyboardButton(text="IFREELAND Passport☻", url='https://grandbazar.io/ru/collection/passport_freeland'))


@bot.message_handler(commands=['start'])
def command_start(message):
    bot.send_animation(message.chat.id,
                       animation="https://graphicdesignjunction.com/wp-content/uploads/2021/06/logo-animation-25.gif",
                       width=1600,
                       height=1200,)
    bot.send_message(message.chat.id,
                     "Welcome to the NFT shop."
                     " Check out our collection."
                     " Select /buy for order,"
                     " /catalog collection list,"
                     " /help support team")


@bot.message_handler(commands=['catalog'])
def catalog(message):
    bot.send_message(message.chat.id,
                     text="Check out our collections below☟",
                     reply_markup=catalog_list)


@bot.message_handler(commands=['help'])
def command_terms(message):
    bot.send_message(message.chat.id,
                     'For any question contact our support @support')


@bot.message_handler(commands=['buy'])
def command_pay(message):
    bot.send_message(message.chat.id,
                     "Insert this Card number: `4242 4242 4242 4242`"
                     "\n\nThis is your demo invoice:", parse_mode='Markdown')
    bot.send_invoice(
                     message.chat.id,   # chat_id
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
                     'Thanks for order! '.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')


bot.infinity_polling(skip_pending=True)
