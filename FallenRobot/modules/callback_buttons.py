from telegram import Update, ChatPermissions, ParseMode
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram.utils.helpers import mention_html

from FallenRobot import dispatcher
from FallenRobot.modules.helper_funcs.chat_status import (
    bot_admin,
    can_restrict,
    connection_status,
    is_user_admin,
    user_admin,
)
from FallenRobot.modules.helper_funcs.extraction import extract_user_and_text
from FallenRobot.modules.log_channel import loggable


@connection_status
@bot_admin
@can_restrict
@user_admin
@loggable
def unban_button(update: Update, context: CallbackContext) -> str:
    query = update.callback_query
    user = update.effective_user
    chat = update.effective_chat
    message = update.effective_message
    
    if not query.data:
        return ""
        
    match = query.data.split("=")
    if len(match) != 2:
        return ""
        
    target_user_id = int(match[1])
    
    if not is_user_admin(chat, user.id):
        query.answer("⚠️ You don't have enough rights to unmute people", show_alert=True)
        return ""
        
    try:
        member = chat.get_member(target_user_id)
    except:
        query.answer("This user is not in this chat!", show_alert=True)
        return ""
        
    try:
        chat.unban_member(target_user_id)
        query.answer("✅ Unbanned!")
        
        log = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#UNBANNED\n"
            f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"
        )
        
        message.edit_text(
            f"<b>Unbanned!</b>\n"
            f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}\n"
            f"<b>By:</b> {mention_html(user.id, user.first_name)}",
            parse_mode=ParseMode.HTML,
        )
        
        return log
        
    except Exception as err:
        query.answer(f"Error: {err}", show_alert=True)
        return ""


@connection_status
@bot_admin
@can_restrict
@user_admin
@loggable
def unmute_button(update: Update, context: CallbackContext) -> str:
    query = update.callback_query
    user = update.effective_user
    chat = update.effective_chat
    message = update.effective_message
    
    if not query.data:
        return ""
        
    match = query.data.split("=")
    if len(match) != 2:
        return ""
        
    target_user_id = int(match[1])
    
    if not is_user_admin(chat, user.id):
        query.answer("⚠️ You don't have enough rights to unmute people", show_alert=True)
        return ""
        
    try:
        member = chat.get_member(target_user_id)
    except:
        query.answer("This user is not in this chat!", show_alert=True)
        return ""
        
    try:
        chat_permissions = ChatPermissions(
            can_send_messages=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_send_polls=True,
            can_change_info=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
        chat.restrict_member(target_user_id, chat_permissions)
        query.answer("✅ Unmuted!")
        
        log = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#UNMUTED\n"
            f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"
        )
        
        message.edit_text(
            f"<b>Unmuted!</b>\n"
            f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}\n"
            f"<b>By:</b> {mention_html(user.id, user.first_name)}",
            parse_mode=ParseMode.HTML,
        )
        
        return log
        
    except Exception as err:
        query.answer(f"Error: {err}", show_alert=True)
        return ""


# Handlers
UNBAN_BUTTON_HANDLER = CallbackQueryHandler(unban_button, pattern=r"unban_btn=", run_async=True)
UNMUTE_BUTTON_HANDLER = CallbackQueryHandler(unmute_button, pattern=r"unmute_btn=", run_async=True)

# Add handlers to dispatcher
dispatcher.add_handler(UNBAN_BUTTON_HANDLER)
dispatcher.add_handler(UNMUTE_BUTTON_HANDLER)


__mod_name__ = "Buttons"
__handlers__ = [
    UNBAN_BUTTON_HANDLER,
    UNMUTE_BUTTON_HANDLER,
]