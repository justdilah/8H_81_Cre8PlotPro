# from flask import Flask, request
import json
import telegram
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup, InputMediaPhoto, ReplyKeyboardRemove,ReplyKeyboardMarkup
import requests
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, \
    CallbackQueryHandler, CallbackContext, ConversationHandler
import logging
import os
from itertools import cycle

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

global bot
global TOKEN
TOKEN = "6752671463:AAESLDYm24_zbbNm5cUH11ViBy1v69H4EoY"


# EXPECT_FEELINGS, TRIGGERED, SAD, CHOICES, ABUSE, RECOMMEND, ABUSE_ACTIONS, FEELINGS, ABUSEBOT, SHOW = range(10)

PANEL, EDIT, PANEL_ACTIONS, TEXT, TO_PARAPHASE = range(5)

PARAPHASED, DESC = map(chr, range(2))
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# State definitions for top level conversation
SELECTING_ACTION, SHARE_FEELINGS, ABUSE_ME, RECOMMEND_SHOWS, VIEW_BDAY_MSG = map(chr, range(5))
# State definitions for second level conversation
SELECTING_LEVEL, SELECTING_GENDER, SELECTING_EMOTIONS = map(chr, range(5, 8))
# State definitions for descriptions conversation
SELECTING_ST_ACTIONS, TYPING, BDAY = map(chr, range(8, 11))
# Meta states
STOPPING, SHOWING = map(chr, range(11, 13))
# Shortcut for ConversationHandler.END
END = ConversationHandler.END

# # Different constants for this example
# (
#     HAPPY,
#     SAD,
#     TRIGGERED,
#     CALM,
#     PUNCH,
#     HUG,
#     KICK,
#     SCOLD,
#     START_OVER,
#     NEXT,
#     BACK,
#     JOKE,
# ) = map(chr, range(13, 25))

photo_chat_id = ""
poster = [
    "https://pic.rutubelist.ru/video/17/b1/17b100a0bcbc6e5e8d11101cde21aca7.jpg",
    "https://funik.ru/wp-content/uploads/2018/10/6db3f15d0a21589aaa1b.jpg",
    "https://psihoman.ru/uploads/posts/2022-02/1645693727_1645693779.jpg",
]

photos = [
    os.path.abspath(os.getcwd()) + '\images\\1.jpg',
    os.path.abspath(os.getcwd()) + "\images\\2.jpg",
    os.path.abspath(os.getcwd()) + "\images\\3.jpg",
    os.path.abspath(os.getcwd()) + "\images\\4.jpg",
    os.path.abspath(os.getcwd()) + "\images\\5.jpg",
    os.path.abspath(os.getcwd()) + "\images\\6.jpg",
    os.path.abspath(os.getcwd()) + "\images\\7.jpg",
    os.path.abspath(os.getcwd()) + "\images\\8.jpg",
]

cycle_poster = cycle(photos)


# Top level conversation callbacks
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update._effective_user.username
    answer = "Hello " + username + "! " + ("🌟 Welcome to the imaginative realm of Cre8PlotPro, "
                                           "where your creativity takes center stage. "
                                           "Unleash the storyteller within using our Telegram chatbot, "
                                           "equipped with advanced AI capabilities for image and text "
                                           "generation, as well as paraphrasing—no artistic skills required. 🤖✨\n\n"
                                           "Cre8PlotPro Usage:\n\nAnswer the questions posed by our Telegram chatbot! 🤔\n\n"
                                           "0. Start your experience by typing /begin\n\n"
                                           "1. Visualize a scene and describe it to our bot—watch as it transforms your ideas into captivating visuals. "
       "🎨e.g., 'a girl with curly hair eating bread.'\n\n"
                                           "2. Craft the perfect text caption to accompany your image panel. 📝 e.g., 'This bread is delicious!'\n\n"
                                           "3. Need a grammar check and an alternative sentence? Opt for paraphrasing with a simple 'Yes' when prompted. 🔄\n\n"
                                           "4. Save your diverse panels and effortlessly share your visual tales on any social media platform you fancy. 🌐\n\n"
                                           "Happy Storytelling! 🚀✨")


    await update.message.reply_text(
        answer
    )

    # return DESC

async def provideDesc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global counter
    counter = 4
    username = update._effective_user.username
    answer = "Please describe the scene and characters for this panel."
    await update.message.reply_text(
        answer
    )
    # context.user_data[START_OVER] = False
    return TEXT

async def provideText(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global desc_user
    desc_user = update.message.text
    # num_updates = len(update["result"])
    # last_update = num_updates - 1
    # text = update["result"][last_update]["message"]["text"]
    answer = "Please input the text caption you would like to accompany your image panel. "
    await update.message.reply_text(
        answer
    )
    # context.user_data[START_OVER] = False
    return PANEL
async def showPanel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global counter, desc_user, text_user
    print(desc_user)
    print(counter)

    text_user = update.message.text
    url = 'http://127.0.0.1:8000/'

    myobj = {
                "panel": counter,
                "description": desc_user,
                "text": text_user,
                "paraphase": 0
        }

    x = requests.post(url, json=myobj)
    print(x.text)

    text = (
        "Would you like to paraphrase your text caption?"
    )

    buttons = [
        [
            InlineKeyboardButton(text="Yes", callback_data=str(PARAPHASED)),
            InlineKeyboardButton(text="No", callback_data=str(PANEL)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    username = update._effective_user.username

    folder_to_remove = "telebotcre8AI"
    relative_path = os.path.relpath(os.getcwd(), os.path.join(os.getcwd(), folder_to_remove))
    new_absolute_path = os.path.abspath(relative_path)

    # file = InputMediaPhoto(media=open(new_absolute_path + '\cre8AI\output\\panel-4.png', 'rb'))

    await update.message.reply_photo(photo=new_absolute_path + '\cre8AI\output\\panel-' +str(counter) + '.png', caption=text, reply_markup=keyboard)

    return PANEL_ACTIONS

async def editPanel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global counter
    counter-=1
    print("TEST " + str(counter))
    answer = "PLS"
    await update.message.reply_text(
        answer
    )
    return PANEL

async def paraphasedPanel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("dasdasd")
    answer = "TADA"
    await update.message.reply_text(
        answer
    )
    # context.user_data[START_OVER] = False
    return PANEL

async def originalPanel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = "Original"
    await update.message.reply_text(
        answer
    )
    # context.user_data[START_OVER] = False
    return PANEL
async def panelActionsCallBack(update: Update, context: CallbackContext):
    choice = update.callback_query.data
    text = "Looks good"
    global counter, desc_user, text_user
    print(counter)
    print(desc_user)
    print(text_user)
    if counter == 6:
        text = "You have successfully created all successfully. Goodbye"
        print(text)
    if choice == PARAPHASED:
        url = 'http://127.0.0.1:8000/'

        myobj = {
            "panel": counter,
            "description": desc_user,
            "text": text_user,
            "paraphase": 1
        }

        x = requests.post(url, json=myobj)
        print(x.text)

        text = "Panel" + str(counter) + "has been created successfully \nPlease describe the scene and characters for the next panel."
    elif choice == PANEL:
        text = "Panel" + str(counter) + "has been created successfully \nPlease describe the scene and characters for the next panel. "

    await update.callback_query.answer()
    folder_to_remove = "telebotcre8AI"
    relative_path = os.path.relpath(os.getcwd(), os.path.join(os.getcwd(), folder_to_remove))
    new_absolute_path = os.path.abspath(relative_path)

    file = InputMediaPhoto(media=open(new_absolute_path + '\cre8AI\output\\panel-' +str(counter) + '.png','rb'), caption=text)
    await update.callback_query.edit_message_media(file)
    counter += 1
    return TEXT
#
#
# async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """End Conversation by command."""
#     context.user_data[START_OVER] = False
#     await update.message.reply_text("Okay, bye.")
#
#     return END
#
#
# async def end_second_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Return to top level conversation."""
#     context.user_data[START_OVER] = True
#     await start(update, context)
#
#     return END
#
#
# async def stop_nested(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
#     """Completely end conversation from within nested conversation."""
#     await update.message.reply_text("Okay, bye.")
#
#     return STOPPING
#
#
# async def cancel(update: Update, context: CallbackContext):
#     await update.message.reply_text('Feelings Conversation cancelled by user. Bye. Send /feelings to start again')
#     return ConversationHandler.END
#
#
# async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """End conversation from InlineKeyboardButton."""
#     await update.callback_query.answer()
#
#     text = "See you around!"
#
#     # await update.message.reply_photo(photo=poster[0], caption=text)
#     file = InputMediaPhoto(media=poster[0], caption=text)
#     await update.callback_query.edit_message_media(file)
#     context.user_data[START_OVER] = False
#     return END
#

def main():
    mode = os.environ.get("MODE", "polling")

    # application -> responsible for fetching updates from the update_queue
    # Creates Updater -> fetches new updates from telegram and adds them to this queue
    application = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler('start', start)
    # forward_handler = MessageHandler(filters.FORWARDED, forward)
    # unknown_handler = MessageHandler(filters.COMMAND, unknown)
    #
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("begin", provideDesc)],
        states={
            TEXT: [MessageHandler(filters.TEXT,provideText)],
            TO_PARAPHASE: [MessageHandler(filters.Regex("^(Yes)$"), paraphasedPanel)],
            PANEL: [MessageHandler(filters.TEXT,showPanel)],
            EDIT: [CallbackQueryHandler(editPanel)],
            DESC: [CallbackQueryHandler(provideDesc)],
            PANEL_ACTIONS: [CallbackQueryHandler(panelActionsCallBack)]

        },
        fallbacks=[
            CommandHandler("stop", start),
        ],
        map_to_parent={
            # After showing data return to top level menu
            SHOWING: SHOWING,
            # Return to top level menu
            END: SELECTING_ACTION,
            # End conversation altogether
            STOPPING: END,
        },
    )
    #
    # showsBotHandler = ConversationHandler(
    #     entry_points=[CallbackQueryHandler(showMemories, pattern="^" + str(RECOMMEND_SHOWS) + "$")],
    #     states={
    #         RECOMMEND: [CallbackQueryHandler(showsCallBack)]
    #     },
    #     fallbacks=[
    #         CallbackQueryHandler(showMemories, pattern="^" + str(SHOWING) + "$"),
    #         CallbackQueryHandler(end_second_level, pattern="^" + str(END) + "$"),
    #         CommandHandler("stop", stop_nested),
    #     ],
    #     map_to_parent={
    #         # After showing data return to top level menu
    #         SHOWING: SHOWING,
    #         # Return to top level menu
    #         END: SELECTING_ACTION,
    #         # End conversation altogether
    #         STOPPING: END,
    #     },
    # )
    # sad_actions_handler = [
    #     CallbackQueryHandler(randomJoke, pattern="^" + str(JOKE) + "$"),
    #     CallbackQueryHandler(showMemories, pattern="^" + str(RECOMMEND_SHOWS) + "$")
    # ]
    # emotions_handler = [
    #     CallbackQueryHandler(sadEmotion, pattern="^" + str(SAD) + "$"),
    #     CallbackQueryHandler(triggeredEmotion, pattern="^" + str(TRIGGERED) + "$"),
    #     CallbackQueryHandler(calmEmotion, pattern="^" + str(CALM) + "$"),
    #     CallbackQueryHandler(happyEmotion, pattern="^" + str(HAPPY) + "$")
    # ]
    # feelings_conv = ConversationHandler(
    #     entry_points=[CallbackQueryHandler(askFeelings, pattern="^" + str(SHARE_FEELINGS) + "$")],
    #     states={
    #         EXPECT_FEELINGS: [CallbackQueryHandler(feelingsCallback)],
    #         SELECTING_EMOTIONS: emotions_handler,
    #         SELECTING_ST_ACTIONS: sad_actions_handler
    #     },
    #     fallbacks=[
    #         # CallbackQueryHandler(show_data, pattern="^" + str(SHOWING) + "$"),
    #         CallbackQueryHandler(end_second_level, pattern="^" + str(END) + "$"),
    #         CommandHandler("stop", stop_nested),
    #     ],
    #     map_to_parent={
    #         # After showing data return to top level menu
    #         SHOWING: SHOWING,
    #         # Return to top level menu
    #         END: SELECTING_ACTION,
    #         # End conversation altogether
    #         STOPPING: END,
    #     },
    # )
    #
    # selection_handlers = [
    #     feelings_conv,
    #     showsBotHandler,
    #     abuseBotHandler,
    #     CallbackQueryHandler(viewBdayMessage, pattern="^" + str(VIEW_BDAY_MSG) + "$"),
    #     CallbackQueryHandler(end, pattern="^" + str(END) + "$"),
    # ]
    #
    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler("start", start)],
    #     states={
    #         SHOWING: [CallbackQueryHandler(start, pattern="^" + str(END) + "$")],
    #         SELECTING_ACTION: selection_handlers,
    #         SELECTING_LEVEL: selection_handlers,
    #         STOPPING: [CommandHandler("start", start)]
    #     },
    #     fallbacks=[CommandHandler("stop", stop)],
    # )
    application.add_handler(start_handler)
    application.add_handler(conv_handler)
    # application.add_handler(unknown_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
