import telebot
from telebot.types import LabeledPrice, ShippingOption, InlineKeyboardButton, InlineKeyboardMarkup
import config

bot = telebot.TeleBot(config.token)
currency = 'rub'

# More about Payments: https://core.telegram.org/bots/payments

prices = [LabeledPrice(label='iphone14 ProMax', amount=5750), LabeledPrice('Gift wrapping', 500)]

shipping_options = [
    ShippingOption(id='instant', title='Iphone14').add_price(LabeledPrice('iphone', 5750)),
    ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 300))]

catalog_list = InlineKeyboardMarkup(row_width=2)
catalog_list.add(InlineKeyboardButton(text="Iphone14", url='https://ldkfjg.com'),
                  InlineKeyboardButton(text="Iphone14 ProMax", url='https://ldkfjg.com'),
                  InlineKeyboardButton(text="Iphone15🚀", url='https://ldkfjg.com'))



@bot.message_handler(commands=['start'])
def command_start(message):
    bot.send_message(message.chat.id,
                     "Вас приветствует магазин Apple."
                     " Сейчас в наличии 3 товара Iphone."
                     " Выберите /buy для заказа, "
                     "/catalog Каталог товаров,"
                     " /terms Условия")


@bot.message_handler(commands=['catalog'])
def catalog(message):
    bot.send_message(message.chat.id, text="test", reply_markup=catalog_list)


@bot.message_handler(commands=['terms'])
def command_terms(message):
    bot.send_message(message.chat.id,
                     'Спасибо, что выбрали наш магазин\n'
                     'По любым вопросам обращайтесь в службу поддержки')


@bot.message_handler(commands=['buy'])
def command_pay(message):
    bot.send_message(message.chat.id,
                     "Реквизиты для тестовой карты: `4242 4242 4242 4242`"
                     "\n\nThis is your demo invoice:", parse_mode='Markdown')
    bot.send_invoice(
                     message.chat.id,  #chat_id
                     'Iphone 14 Pro Max', #title
                     'Size: 128GB', #description
                     'HAPPY FRIDAYS COUPON', #invoice_payload
                     config.provider_token, #provider_token
                     currency, #currency
                     prices, #prices
                     photo_url='https://bb-scm-prod-pim.oss-ap-southeast-5.aliyuncs.com/products/7eca1fd03f15b186b09bdb5c9a60ac0b/helix/01-APPLE-8DVPHAPPA-APPMQ9P3ID-A-Space%20Black1.jpg',
                     photo_height=1000,  # !=0/None or picture won't be shown
                     photo_width=1321,
                     photo_size=160651,
                     is_flexible=True,  # True If you need to set up Shipping Fee
                     start_parameter='iphone-example')

@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    print(shipping_query)
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                              error_message='Oh, seems like our Dog couriers are having a lunch right now. Try again later!')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'Спасибо за заказ! '.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')


bot.infinity_polling(skip_pending=True)
