from telegram import ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from telegram.utils.helpers import mention_html

from FallenRobot import dispatcher
from FallenRobot.modules.helper_funcs.chat_status import user_admin
from FallenRobot.modules.mongo.karma_db import add_karma, get_karma, get_top_karma, reset_karma

def karma_plus(update: Update, context: CallbackContext) -> None:
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    
    # Check if message is a reply
    if not message.reply_to_message:
        return
    
    # Get the user being replied to
    target_user = message.reply_to_message.from_user
    
    # Don't allow self-karma
    if target_user.id == user.id:
        message.reply_text("Nice try, but you can't give karma to yourself!")
        return
        
    # Don't allow karma for bots
    if target_user.is_bot:
        message.reply_text("Bots don't need karma!")
        return
    
    new_karma = add_karma(chat.id, target_user.id, 1)
    message.reply_text(
        f"🔼 {mention_html(target_user.id, target_user.first_name)} now has {new_karma} karma!",
        parse_mode=ParseMode.HTML
    )

def karma_minus(update: Update, context: CallbackContext) -> None:
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    
    # Check if message is a reply
    if not message.reply_to_message:
        return
    
    # Get the user being replied to
    target_user = message.reply_to_message.from_user
    
    # Don't allow self-karma
    if target_user.id == user.id:
        message.reply_text("Nice try, but you can't reduce your own karma!")
        return
        
    # Don't allow karma for bots
    if target_user.is_bot:
        message.reply_text("Bots don't need karma!")
        return
    
    new_karma = add_karma(chat.id, target_user.id, -1)
    message.reply_text(
        f"🔽 {mention_html(target_user.id, target_user.first_name)} now has {new_karma} karma!",
        parse_mode=ParseMode.HTML
    )

def check_karma(update: Update, context: CallbackContext) -> None:
    message = update.effective_message
    chat = update.effective_chat
    
    # If command is a reply, check replied user's karma
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
    else:
        # If no reply, check mentioned user or command sender
        if len(context.args) > 0:
            try:
                target_user = context.bot.get_chat_member(chat.id, context.args[0]).user
            except:
                message.reply_text("I can't find that user.")
                return
        else:
            target_user = update.effective_user
    
    karma_points = get_karma(chat.id, target_user.id)
    message.reply_text(
        f"{mention_html(target_user.id, target_user.first_name)} has {karma_points} karma points!",
        parse_mode=ParseMode.HTML
    )

def karma_leaderboard(update: Update, context: CallbackContext) -> None:
    chat = update.effective_chat
    message = update.effective_message
    
    top_users = get_top_karma(chat.id)
    
    if not top_users:
        message.reply_text("No karma points have been awarded in this chat yet!")
        return
    
    msg = "🏆 *Karma Leaderboard* 🏆\n\n"
    for idx, user in enumerate(top_users, 1):
        try:
            member = chat.get_member(user['user_id'])
            name = member.user.first_name
            msg += f"{idx}. {name}: {user['karma']} points\n"
        except:
            continue
    
    message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

@user_admin
def reset_user_karma(update: Update, context: CallbackContext) -> None:
    message = update.effective_message
    chat = update.effective_chat
    
    if not message.reply_to_message:
        message.reply_text("Reply to someone's message to reset their karma!")
        return
        
    target_user = message.reply_to_message.from_user
    if reset_karma(chat.id, target_user.id):
        message.reply_text(f"Reset karma for {mention_html(target_user.id, target_user.first_name)}!",
                         parse_mode=ParseMode.HTML)
    else:
        message.reply_text("This user doesn't have any karma yet!")

# Command handlers
KARMA_PLUS_HANDLER = MessageHandler(Filters.regex(r"^\+\+") & Filters.reply & ~Filters.bot, karma_plus, run_async=True)
KARMA_MINUS_HANDLER = MessageHandler(Filters.regex(r"^--") & Filters.reply & ~Filters.bot, karma_minus, run_async=True)
KARMA_CHECK_HANDLER = CommandHandler("karma", check_karma, run_async=True)
KARMA_LEADERBOARD_HANDLER = CommandHandler("topkarma", karma_leaderboard, run_async=True)
KARMA_RESET_HANDLER = CommandHandler("resetkarma", reset_user_karma, run_async=True)

dispatcher.add_handler(KARMA_PLUS_HANDLER)
dispatcher.add_handler(KARMA_MINUS_HANDLER)
dispatcher.add_handler(KARMA_CHECK_HANDLER)
dispatcher.add_handler(KARMA_LEADERBOARD_HANDLER)
dispatcher.add_handler(KARMA_RESET_HANDLER)

__mod_name__ = "Kᴀʀᴍᴀ"
__help__ = """
*Karma System*

Track reputation points for users in your chat!

*Commands:*
❍ Reply to a message with `++` to give karma
❍ Reply to a message with `--` to reduce karma
❍ /karma - Check your or another user's karma
❍ /topkarma - Show karma leaderboard
❍ /resetkarma - Reset a user's karma (Admin only)
"""

__handlers__ = [
    KARMA_PLUS_HANDLER,
    KARMA_MINUS_HANDLER,
    KARMA_CHECK_HANDLER,
    KARMA_LEADERBOARD_HANDLER,
    KARMA_RESET_HANDLER,
]