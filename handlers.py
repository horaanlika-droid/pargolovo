import time
import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from config import ADMIN_IDS, CHANNELS
from database import *
from scenes import scenes
from file_ids import FILE_IDS

router = Router()
bot = None

# Хранилище состояний (для ожидания ввода)
broadcast_data = {}

def set_bot(bot_instance):
    global bot
    bot = bot_instance

# ========== КЛАВИАТУРЫ ==========
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="▶️ ИГРАТЬ")],
            [KeyboardButton(text="🦴 МОЙ ПРОФИЛЬ")],
            [KeyboardButton(text="❓ ПОМОЩЬ")]
        ],
        resize_keyboard=True
    )

def get_rank(points: int) -> str:
    if points < 10:
        return "🐾 Щенок"
    elif points < 50:
        return "🐕 Псина"
    elif points < 200:
        return "🐶 Послушный пёсик"
    else:
        return "👑 Любимчик Богини"

# ========== ПОКАЗ СЦЕНЫ ==========
async def show_scene(message: Message, user_id: int, scene: dict, scene_id: str):
    if not scene:
        scene = scenes.get("prolog")
        scene_id = "prolog"
        await update_current_scene(user_id, scene_id)

    text = scene.get("text", "")
    video = scene.get("video")
    voice = scene.get("voice")
    photo = scene.get("photo")
    choices = scene.get("choices", [])
    mini_game = scene.get("mini_game")
    save_point = scene.get("save_point", False)

    # Сохранение
    if save_point:
        await update_save_point(user_id, scene_id)
        await bot.send_message(message.chat.id, "💾 Игра сохранена!")

    # ===== ОТПРАВКА ВИДЕО =====
    if video:
        await bot.send_video(chat_id=message.chat.id, video=video, caption="🎬")

    # ===== ОТПРАВКА ГОЛОСОВОГО =====
    if voice:
        icon = {
            "diary": "🎙️",
            "call": "📞",
            "voice_message": "🎤",
            "news": "📻",
            "ambient": "🔊"
        }.get(voice.get("type"), "🔊")
        caption = voice.get("caption", "")
        await bot.send_voice(
            chat_id=message.chat.id,
            voice=voice.get("file"),
            caption=f"{icon} {caption}"
        )

    # ===== ОТПРАВКА ФОТО =====
    if photo:
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text)
    else:
        await bot.send_message(chat_id=message.chat.id, text=text)

    # ===== МИНИ-ИГРА =====
    if mini_game:
        await show_mini_game(message, user_id, scene_id, mini_game)
        return

    # ===== КНОПКИ ВЫБОРА =====
    if choices:
        kb_buttons = []
        for idx, choice in enumerate(choices):
            cb_data = choice.get("callback_data")
            if not cb_data:
                cb_data = f"choice_{scene_id}_{idx}"
            if choice.get("is_fatal"):
                cb_data += "_fatal"
            kb_buttons.append([InlineKeyboardButton(text=choice["text"], callback_data=cb_data)])
        keyboard = InlineKeyboardMarkup(inline_keyboard=kb_buttons)
        await bot.send_message(
            chat_id=message.chat.id,
            text="🔻 ТВОЙ ВЫБОР:",
            reply_markup=keyboard
        )

# ========== МИНИ-ИГРЫ ==========
async def show_mini_game(message: Message, user_id: int, scene_id: str, mini_game: dict):
    game_type = mini_game.get("type")

    if game_type == "clicker":
        total = mini_game.get("steps", 5)
        await set_minigame_progress(user_id, scene_id, 0)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text=f"{mini_game.get('button_text', '🧹')} (0/{total})",
                callback_data=f"minigame_clicker_{scene_id}_1"
            )]
        ])
        await bot.send_message(
            message.chat.id,
            mini_game.get("progress_text", "Прогресс: {current}/{total}").format(current=0, total=total),
            reply_markup=keyboard
        )

    elif game_type == "choice":
        question = mini_game.get("question", "Выбери:")
        options = mini_game.get("options", [])
        kb_buttons = []
        for idx, opt in enumerate(options):
            kb_buttons.append([InlineKeyboardButton(
                text=opt.get("text", f"Вариант {idx+1}"),
                callback_data=f"minigame_choice_{scene_id}_{idx}"
            )])
        keyboard = InlineKeyboardMarkup(inline_keyboard=kb_buttons)
        await bot.send_message(message.chat.id, question, reply_markup=keyboard)

    elif game_type == "qte":
        duration = mini_game.get("duration", 5)
        await set_minigame_start(user_id, scene_id, time.time())
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text=f"🏃 Успеть! (⏱ {duration} сек.)",
                callback_data=f"minigame_qte_{scene_id}_press"
            )]
        ])
        await bot.send_message(
            message.chat.id,
            "⏳ У тебя есть {} секунд! Нажми быстро!".format(duration),
            reply_markup=keyboard
        )

# ========== ОБРАБОТЧИКИ МИНИ-ИГР ==========
@router.callback_query(F.data.startswith("minigame_clicker_"))
async def handle_minigame_clicker(callback: CallbackQuery):
    user_id = callback.from_user.id
    parts = callback.data.split("_")
    scene_id = parts[2]
    step = int(parts[3])

    scene = scenes.get(scene_id)
    if not scene or not scene.get("mini_game"):
        await callback.answer("❌ Ошибка")
        return

    mini_game = scene["mini_game"]
    total = mini_game.get("steps", 5)
    next_scene = mini_game.get("next_scene")

    current = await get_minigame_progress(user_id, scene_id)
    if current >= total:
        await callback.answer("✅ Уже готово!")
        return

    current += 1
    await set_minigame_progress(user_id, scene_id, current)

    if current >= total:
        await callback.message.edit_text(
            mini_game.get("complete_text", "✅ Готово!"),
            reply_markup=None
        )
        await update_current_scene(user_id, next_scene)
        next_scene_data = scenes.get(next_scene)
        if next_scene_data:
            await show_scene(callback.message, user_id, next_scene_data, next_scene)
        await callback.answer("✅ Задание выполнено!")
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text=f"{mini_game.get('button_text', '🧹')} ({current}/{total})",
                callback_data=f"minigame_clicker_{scene_id}_{current+1}"
            )]
        ])
        await callback.message.edit_text(
            mini_game.get("progress_text", "Прогресс: {current}/{total}").format(current=current, total=total),
            reply_markup=kb
        )
        await callback.answer()

@router.callback_query(F.data.startswith("minigame_choice_"))
async def handle_minigame_choice(callback: CallbackQuery):
    user_id = callback.from_user.id
    parts = callback.data.split("_")
    scene_id = parts[2]
    option_idx = int(parts[3])

    scene = scenes.get(scene_id)
    if not scene or not scene.get("mini_game"):
        await callback.answer("❌ Ошибка")
        return

    mini_game = scene["mini_game"]
    options = mini_game.get("options", [])
    if option_idx >= len(options):
        await callback.answer("❌ Неверный выбор")
        return

    selected = options[option_idx]

    if selected.get("correct"):
        await callback.message.edit_text("✅ Правильно!", reply_markup=None)
        next_scene = selected.get("next_scene")
        await update_current_scene(user_id, next_scene)
        next_scene_data = scenes.get(next_scene)
        if next_scene_data:
            await show_scene(callback.message, user_id, next_scene_data, next_scene)
        await callback.answer("✅ Верно!")
    else:
        fail_text = selected.get("fail_text", "❌ Неправильно. Попробуй снова.")
        await callback.message.edit_text(fail_text)
        await asyncio.sleep(1.5)
        # Перезапускаем мини-игру
        await show_mini_game(callback.message, user_id, scene_id, mini_game)
        await callback.answer("❌ Попробуй снова")

@router.callback_query(F.data.startswith("minigame_qte_"))
async def handle_minigame_qte(callback: CallbackQuery):
    user_id = callback.from_user.id
    parts = callback.data.split("_")
    scene_id = parts[2]
    action = parts[3] if len(parts) > 3 else "press"

    scene = scenes.get(scene_id)
    if not scene or not scene.get("mini_game"):
        await callback.answer("❌ Ошибка")
        return

    mini_game = scene["mini_game"]
    duration = mini_game.get("duration", 5)

    if action == "press":
        start_time = await get_minigame_start(user_id, scene_id)
        elapsed = time.time() - start_time

        if elapsed <= duration:
            await callback.message.edit_text(
                mini_game.get("success_text", "✅ Ты успела!"),
                reply_markup=None
            )
            next_scene = mini_game.get("next_scene")
            await update_current_scene(user_id, next_scene)
            next_scene_data = scenes.get(next_scene)
            if next_scene_data:
                await show_scene(callback.message, user_id, next_scene_data, next_scene)
            await callback.answer("✅ Сбежала!")
        else:
            await callback.message.edit_text(
                mini_game.get("fail_text", "❌ Ты не успела."),
                reply_markup=None
            )
            fail_scene = mini_game.get("fail_scene", "game_over")
            await update_current_scene(user_id, fail_scene)
            fail_scene_data = scenes.get(fail_scene)
            if fail_scene_data:
                await show_scene(callback.message, user_id, fail_scene_data, fail_scene)
            await callback.answer("💀 Фатально")

# ========== ОБРАБОТЧИК ВЫБОРОВ ==========
@router.callback_query(F.data.startswith("choice_"))
async def handle_choice(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data

    is_fatal = data.endswith("_fatal")
    if is_fatal:
        data = data[:-6]

    parts = data.split("_")
    scene_id = "_".join(parts[1:-1])
    choice_idx = int(parts[-1])

    scene = scenes.get(scene_id)
    if not scene:
        await callback.message.answer("❌ Сцена не найдена")
        return

    choices = scene.get("choices", [])
    if choice_idx >= len(choices):
        await callback.message.answer("❌ Неверный выбор")
        return

    selected = choices[choice_idx]
    next_scene_id = selected.get("next_scene")

    if is_fatal or selected.get("is_fatal"):
        next_scene_id = "game_over"

    # Применяем эффекты (RPG-элементы)
    effects = selected.get("effect", {})
    for key, value in effects.items():
        if key == "son_affection":
            await add_points(user_id, value * 10)
        elif key == "mother_trust":
            await add_points(user_id, value * 5)
        elif key == "edik_trust":
            await add_points(user_id, value * 5)
        elif key == "vadim_trust":
            await add_points(user_id, value * 5)
        elif key == "law_balance":
            await add_points(user_id, value * 10)
        elif key == "addiction":
            await add_points(user_id, -value * 10)
        elif key == "colony_rep":
            await add_points(user_id, value * 10)

    await update_current_scene(user_id, next_scene_id)

    try:
        await callback.message.delete()
    except:
        pass

    next_scene = scenes.get(next_scene_id)
    if next_scene:
        await show_scene(callback.message, user_id, next_scene, next_scene_id)
    else:
        await callback.message.answer("❌ Сцена не найдена")

    await callback.answer()

# ========== ЗАГРУЗКА СОХРАНЕНИЯ ==========
@router.callback_query(F.data == "load_save")
async def load_save(callback: CallbackQuery):
    user_id = callback.from_user.id
    save_scene = await get_save_point(user_id)

    if not save_scene:
        await callback.message.answer("❌ Сохранение не найдено.")
        return

    try:
        await callback.message.delete()
    except:
        pass

    scene = scenes.get(save_scene)
    if scene:
        await update_current_scene(user_id, save_scene)
        await show_scene(callback.message, user_id, scene, save_scene)
        await callback.message.answer("💾 Сохранение загружено!")
    else:
        await callback.message.answer("❌ Ошибка загрузки.")

    await callback.answer()

# ========== ПЕРЕЗАПУСК ==========
@router.callback_query(F.data == "restart_game")
async def restart_game(callback: CallbackQuery):
    user_id = callback.from_user.id
    await clear_save(user_id)
    await update_current_scene(user_id, "prolog")

    try:
        await callback.message.delete()
    except:
        pass

    first_scene = scenes.get("prolog")
    if first_scene:
        await show_scene(callback.message, user_id, first_scene, "prolog")
        await callback.message.answer("🔄 Игра перезапущена!")

    await callback.answer()

# ========== /START ==========
@router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name

    existing = await get_player(user_id)
    if not existing:
        await create_player(user_id, username)
        await update_current_scene(user_id, "prolog")

    save_exists = await has_save(user_id)
    current_scene = await get_current_scene(user_id)
    is_game_over = current_scene == "game_over"

    if save_exists and not is_game_over:
        await message.answer(
            f"🐕 Привет, {username}!\n\n"
            "💾 У тебя есть сохранённая игра!\n"
            "Хочешь продолжить?",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="💾 Продолжить", callback_data="load_save")],
                [InlineKeyboardButton(text="🔄 Новая игра", callback_data="restart_game")]
            ])
        )
        return

    if is_game_over:
        await message.answer(
            "💀 Твоя прошлая игра завершилась фатально.\n"
            "Загрузить сохранение или начать сначала?",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="💾 Загрузить", callback_data="load_save")],
                [InlineKeyboardButton(text="🔄 Новая игра", callback_data="restart_game")]
            ])
        )
        return

    await message.answer(
        f"🐕 Добро пожаловать, {username}!\n\n"
        "Нажми «▶️ ИГРАТЬ», чтобы начать.",
        reply_markup=get_main_keyboard()
    )

# ========== КНОПКА «ИГРАТЬ» ==========
@router.message(F.text == "▶️ ИГРАТЬ")
async def play_button(message: Message):
    user_id = message.from_user.id

    save_scene = await get_save_point(user_id)
    current_scene_id = await get_current_scene(user_id)

    if save_scene and current_scene_id != "game_over":
        await message.answer(
            "💾 У тебя есть сохранённая игра!\n"
            "Загрузить или начать новую?",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="💾 Загрузить", callback_data="load_save")],
                [InlineKeyboardButton(text="🔄 Новая игра", callback_data="restart_game")]
            ])
        )
        return

    if current_scene_id == "game_over":
        await message.answer(
            "💀 Твоя игра завершена фатально.\n\n"
            "Хочешь загрузить сохранение или начать сначала?",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="💾 Загрузить", callback_data="load_save")],
                [InlineKeyboardButton(text="🔄 Новая игра", callback_data="restart_game")]
            ])
        )
        return

    current_scene = scenes.get(current_scene_id)
    if not current_scene:
        current_scene = scenes.get("prolog")
        current_scene_id = "prolog"
        await update_current_scene(user_id, current_scene_id)

    await show_scene(message, user_id, current_scene, current_scene_id)

# ========== ПРОФИЛЬ ==========
@router.message(F.text == "🦴 МОЙ ПРОФИЛЬ")
async def profile_button(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    nickname = await get_nickname(user_id)
    points = await get_points(user_id)
    rank = get_rank(points)
    save_exists = await has_save(user_id)
    achievements = await get_achievements(user_id)

    display_name = nickname if nickname else username

    text = (
        f"🦴 ПРОФИЛЬ\n\n"
        f"🐕 {display_name}\n"
        f"🏆 {rank}\n"
        f"⭐ Баллы: {points}\n"
        f"💾 Сохранение: {'✅ Есть' if save_exists else '❌ Нет'}\n\n"
        f"🏅 Достижения:\n{achievements if achievements else 'пока нет'}"
    )

    await message.answer(text, reply_markup=get_main_keyboard())

# ========== ПОМОЩЬ ==========
@router.message(F.text == "❓ ПОМОЩЬ")
async def help_button(message: Message):
    await message.answer(
        "📖 ПОМОЩЬ\n\n"
        "▶️ ИГРАТЬ — начать или продолжить\n"
        "🦴 МОЙ ПРОФИЛЬ — статистика\n"
        "❓ ПОМОЩЬ — это сообщение\n\n"
        "👑 По всем вопросам: @milla_femdomqueen"
    )

# ========== АДМИН-КОМАНДЫ ==========
@router.message(Command("upload"))
async def cmd_upload(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ Нет прав")
        return

    await message.answer(
        "📤 Отправь мне любой файл (видео, фото, голосовое, аудио).\n"
        "Я пришлю тебе file_id.\n\n"
        "❌ Для отмены напиши /cancel"
    )
    broadcast_data["waiting_for_upload"] = message.from_user.id

@router.message(Command("cancel"))
async def cmd_cancel(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    if broadcast_data.get("waiting_for_upload") == message.from_user.id:
        broadcast_data.pop("waiting_for_upload", None)
        await message.answer("❌ Отменено")
    else:
        await message.answer("❌ Нет активных операций")

@router.message(F.voice | F.video | F.photo | F.audio | F.document | F.animation)
async def handle_upload(message: Message):
    user_id = message.from_user.id

    if broadcast_data.get("waiting_for_upload") != user_id:
        return

    if message.voice:
        file_id = message.voice.file_id
        media_type = "🎙️ Voice"
        extra = f" (⏱ {message.voice.duration} сек.)"
    elif message.video:
        file_id = message.video.file_id
        media_type = "🎬 Video"
        extra = f" ({message.video.width}x{message.video.height})"
    elif message.photo:
        file_id = message.photo[-1].file_id
        media_type = "📸 Photo"
        extra = f" ({message.photo[-1].width}x{message.photo[-1].height})"
    elif message.audio:
        file_id = message.audio.file_id
        media_type = "🎵 Audio"
        extra = f" ({message.audio.duration} сек.)"
    elif message.animation:
        file_id = message.animation.file_id
        media_type = "🎞️ GIF"
        extra = f" ({message.animation.width}x{message.animation.height})"
    elif message.document:
        file_id = message.document.file_id
        media_type = "📄 Document"
        extra = f" ({message.document.file_name})"
    else:
        await message.answer("❌ Неизвестный тип файла")
        return

    broadcast_data.pop("waiting_for_upload", None)

    response = (
        f"✅ {media_type} загружен!\n\n"
        f"🔑 `{file_id}`\n\n"
        f"📎 Вставь в `file_ids.py` как:\n"
        f"`\"{file_id}\"`\n\n"
        f"🔄 Чтобы получить другой file_id, снова отправь файл."
    )

    await message.answer(response, parse_mode="Markdown")

@router.message(Command("a"))
async def cmd_admin_panel(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ Нет прав")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📤 ЗАГРУЗИТЬ ФАЙЛ", callback_data="admin_upload")],
        [InlineKeyboardButton(text="📋 СПИСОК ИГРОКОВ", callback_data="admin_players")],
        [InlineKeyboardButton(text="📊 СТАТИСТИКА", callback_data="admin_stats")]
    ])
    await message.answer("🔧 АДМИН-ПАНЕЛЬ", reply_markup=keyboard)

@router.callback_query(F.data == "admin_upload")
async def admin_upload(callback: CallbackQuery):
    await callback.message.answer(
        "📤 Отправь файл сюда или используй команду /upload"
    )
    await callback.answer()

@router.callback_query(F.data == "admin_players")
async def admin_players(callback: CallbackQuery):
    players = await get_all_players()
    if not players:
        await callback.message.answer("📭 Нет игроков")
        return

    text = "👥 СПИСОК ИГРОКОВ:\n\n"
    for user_id, username, points, rolls, used in players[:20]:
        text += f"• @{username} | ⭐ {points}\n"
    await callback.message.answer(text)
    await callback.answer()

@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    stats = await get_stats()
    await callback.message.answer(f"📊 Всего игроков: {stats['total_players']}")
    await callback.answer()
