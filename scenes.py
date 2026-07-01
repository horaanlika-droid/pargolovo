from file_ids import FILE_IDS

scenes = {
    # ============================================================
    # ГЛАВА 1: «Зелёный — значит хороший»
    # ============================================================

    "prolog": {
        "text": "Ночь. Петербург. Снег идёт. Ты стоишь на крыше и смотришь вниз. Город мерцает огнями. Ты — Ира. Тебе 34. Ты — королева этого города. Но завтра всё изменится.",
        "video": FILE_IDS.get("video_prolog"),
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_001"),
            "caption": "🎙️ Диктофон Иры..."
        },
        "photo": FILE_IDS.get("choice_prolog"),
        "choices": [
            {"text": "🎵 Спуститься в клуб", "next_scene": "rave"},
            {"text": "🧪 Поехать в лабораторию", "next_scene": "lab"}
        ]
    },

    "rave": {
        "text": "Ты в клубе. Неон разрезает дым. Музыка бьёт по венам. Ты танцуешь, но внутри — пустота. Ты ищешь что-то, чего не можешь найти.",
        "video": FILE_IDS.get("video_rave"),
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_002"),
            "caption": "🎙️ Я здесь, чтобы забыть..."
        },
        "photo": FILE_IDS.get("choice_rave"),
        "save_point": True,
        "choices": [
            {"text": "💊 Взять таблетку", "next_scene": "game_over", "is_fatal": True},
            {"text": "🚪 Выйти из клуба", "next_scene": "call_mother"}
        ]
    },

    "call_mother": {
        "text": "Твой телефон вибрирует. На экране — «МАМА». Ты смотришь на экран и чувствуешь, как внутри всё сжимается.",
        "photo": FILE_IDS.get("choice_phone_mother"),
        "voice": {
            "type": "call",
            "file": FILE_IDS.get("call_mother_001"),
            "caption": "📞 Звонок от матери..."
        },
        "choices": [
            {"text": "📞 Ответить", "next_scene": "talk_to_mother"},
            {"text": "📱 Сбросить", "next_scene": "lab"}
        ]
    },

    "talk_to_mother": {
        "text": "Мать: «Ира, ты опять кололась?» Ты молчишь. Слышно только её холодный голос. Она знает. Она всегда знает.",
        "voice": {
            "type": "call",
            "file": FILE_IDS.get("call_mother_002"),
            "caption": "📞 Разговор с матерью..."
        },
        "photo": FILE_IDS.get("photo_mother"),
        "choices": [
            {"text": "😔 Сказать правду", "next_scene": "lab", "effect": {"mother_trust": -1}},
            {"text": "🤥 Соврать", "next_scene": "lab", "effect": {"mother_trust": -2}}
        ]
    },

    "lab": {
        "text": "Ты в лаборатории. Колбы, весы, лакмус. Всё на месте. Ты проверяешь партию — зелёный. Всё правильно. Но внутри пустота.",
        "video": FILE_IDS.get("video_lab"),
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_003"),
            "caption": "🎙️ Зелёный. Значит, хороший..."
        },
        "photo": FILE_IDS.get("choice_lab"),
        "save_point": True,
        "choices": [
            {"text": "🔬 Проверить партию", "next_scene": "check_batch"},
            {"text": "📞 Позвонить Эдику", "next_scene": "edik_voice"}
        ]
    },

    "check_batch": {
        "text": "Ты опускаешь лакмус. Зелёный. Идеальный. Но ты чувствуешь только усталость. Деньги есть. Есть всё. Кроме смысла.",
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_004"),
            "caption": "🎙️ Всё правильно... но почему пусто?"
        },
        "photo": FILE_IDS.get("photo_lab_batch"),
        "choices": [
            {"text": "📦 Забрать закладку", "next_scene": "stash"},
            {"text": "💉 Сделать укол", "next_scene": "shoot_choice"}
        ]
    },

    "shoot_choice": {
        "text": "Ты смотришь на шприц. Внутри — твой единственный друг. Ты знаешь, что это неправильно. Но ты не можешь остановиться.",
        "photo": FILE_IDS.get("choice_shoot"),
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_shoot"),
            "caption": "🎙️ Я не могу остановиться..."
        },
        "choices": [
            {"text": "💉 Сделать укол", "next_scene": "shoot_effect", "is_fatal": True},
            {"text": "🚫 Убрать шприц", "next_scene": "stash"}
        ]
    },

    "shoot_effect": {
        "text": "Ты делаешь укол. Тепло разливается по телу. Ты закрываешь глаза. Всё становится проще. Ты — королева. Ты — ничто.",
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_shoot_effect"),
            "caption": "🎙️ Пустота..."
        },
        "photo": FILE_IDS.get("photo_shoot"),
        "choices": [
            {"text": "📦 Забрать закладку", "next_scene": "stash"},
            {"text": "💀 Продолжить", "next_scene": "game_over", "is_fatal": True}
        ]
    },

    "edik_voice": {
        "text": "Приходит голосовое от Эдика. Ты нажимаешь «воспроизвести». Его голос дрожит.",
        "photo": FILE_IDS.get("choice_phone_edik"),
        "voice": {
            "type": "voice_message",
            "file": FILE_IDS.get("voice_edik_001"),
            "caption": "🎤 Эдик в панике..."
        },
        "choices": [
            {"text": "📞 Позвонить Эдику", "next_scene": "edik_panic"},
            {"text": "🔇 Игнорировать", "next_scene": "stash"}
        ]
    },

    "edik_panic": {
        "text": "Ты звонишь Эдику. Он кричит: «Ирка, кронштадтские едут! Они всё знают!» Ты слышишь, как дрожит его голос. Он боится. Ты тоже.",
        "video": FILE_IDS.get("video_edik_panic"),
        "voice": {
            "type": "call",
            "file": FILE_IDS.get("call_edik_001"),
            "caption": "📞 Эдик: «Они едут!»"
        },
        "photo": FILE_IDS.get("photo_edik"),
        "choices": [
            {"text": "🗣️ Успокоить Эдика", "next_scene": "stash", "effect": {"edik_trust": 1}},
            {"text": "😡 Кричать на Эдика", "next_scene": "stash", "effect": {"edik_trust": -1}}
        ]
    },

    "stash": {
        "text": "Ты едешь за закладкой. Гаражи, снег, железная дорога. Ты одна. Или тебе только кажется?",
        "video": FILE_IDS.get("video_stash"),
        "voice": {
            "type": "ambient",
            "file": FILE_IDS.get("ambient_stash"),
            "caption": "🔊 Тишина..."
        },
        "photo": FILE_IDS.get("choice_stash"),
        "save_point": True,
        "choices": [
            {"text": "🔍 Проверить, не следят ли", "next_scene": "paranoia"},
            {"text": "🚗 Забрать и уехать", "next_scene": "stash_take"}
        ]
    },

    "paranoia": {
        "text": "Ты сидишь в машине. Уже три часа. Ты смотришь на гаражи и понимаешь: закладка там. Но ты не выходишь. Ты боишься.",
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_paranoia"),
            "caption": "🎙️ Я сижу здесь уже три часа..."
        },
        "photo": FILE_IDS.get("choice_paranoia"),
        "choices": [
            {"text": "🚗 Выйти к гаражам", "next_scene": "stash_find", "is_fatal": True},
            {"text": "🚗 Уехать", "next_scene": "stash_take"}
        ]
    },

    "stash_find": {
        "text": "Ты выходишь из машины. Снег хрустит. Тишина. Ты идёшь к гаражам. Где закладка? Ты не помнишь. Паранойя затуманила разум.",
        "photo": FILE_IDS.get("photo_garages"),
        "voice": {
            "type": "ambient",
            "file": FILE_IDS.get("ambient_snow"),
            "caption": "🔊 Снег хрустит..."
        },
        "mini_game": {
            "type": "choice",
            "question": "Где лежит закладка?",
            "options": [
                {"text": "🚗 Гараж №14", "correct": False, "fail_text": "❌ Пусто. Ты перепутала."},
                {"text": "🚗 Гараж №15", "correct": True, "next_scene": "stash_take"},
                {"text": "🚗 Гараж №16", "correct": False, "fail_text": "❌ Там стоит машина. Не та."}
            ]
        }
    },

    "stash_take": {
        "text": "Ты забираешь закладку. Деньги в руках. Но ты ничего не чувствуешь. Ты — королева пустоты.",
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_stash_take"),
            "caption": "🎙️ Тысячи в руках. Пустота внутри..."
        },
        "photo": FILE_IDS.get("photo_money"),
        "choices": [
            {"text": "📱 Позвонить сыну", "next_scene": "call_son"},
            {"text": "💉 Сделать укол", "next_scene": "shoot_choice"}
        ]
    },

    "call_son": {
        "text": "Ты набираешь номер сына. Слышишь его голос. Он говорит: «Мама, привет». Слёзы наворачиваются. Ты молчишь.",
        "photo": FILE_IDS.get("choice_phone_son"),
        "voice": {
            "type": "call",
            "file": FILE_IDS.get("call_son_001"),
            "caption": "📞 Сын: «Мама, привет...»"
        },
        "save_point": True,
        "choices": [
            {"text": "❤️ Сказать, что любишь", "next_scene": "chapter1_end", "effect": {"son_affection": 2}},
            {"text": "😢 Сказать, что скоро вернёшься", "next_scene": "chapter1_end", "effect": {"son_affection": 1}}
        ]
    },

    "chapter1_end": {
        "text": "Ты кладёшь трубку. Снег идёт. Город мерцает. Ты — королева. Но корона тяжелеет.",
        "video": FILE_IDS.get("video_chapter1_end"),
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_chapter1_end"),
            "caption": "🎙️ Корона тяжелеет..."
        },
        "choices": [
            {"text": "➡️ ПРОДОЛЖИТЬ", "next_scene": "chapter2_start"}
        ]
    },

    # ============================================================
    # ГЛАВА 2: «Королева Парголово»
    # ============================================================

    "chapter2_start": {
        "text": "Прошло несколько недель. Деньги рекой. Ты — королева Парголово. У тебя есть крыша, клиенты, уважение. Но цена растёт.",
        "video": FILE_IDS.get("video_chapter2_start"),
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_chapter2"),
            "caption": "🎙️ Деньги рекой... но цена растёт..."
        },
        "choices": [
            {"text": "➡️ ПРОДОЛЖИТЬ", "next_scene": "vadim_arrives"}
        ]
    },

    "vadim_arrives": {
        "text": "В дверь стучат. Ты открываешь. На пороге — Василий. Он улыбается. Но в глазах — лёд.",
        "video": FILE_IDS.get("video_vadim_arrives"),
        "voice": {
            "type": "voice_message",
            "file": FILE_IDS.get("voice_vadim_001"),
            "caption": "🎤 Василий: «Ирина, мы по делу»"
        },
        "photo": FILE_IDS.get("photo_vadim"),
        "save_point": True,
        "choices": [
            {"text": "💪 Согласиться на сделку", "next_scene": "vadim_deal", "effect": {"law_balance": -1}},
            {"text": "🚫 Отказаться", "next_scene": "vadim_conflict", "effect": {"law_balance": 1}}
        ]
    },

    "vadim_deal": {
        "text": "Ты смотришь на Василия. Ты знаешь — сделка с дьяволом. Но ты соглашаешься. 20 литров в месяц. Ты — часть системы.",
        "video": FILE_IDS.get("video_vadim_deal"),
        "voice": {
            "type": "voice_message",
            "file": FILE_IDS.get("voice_vadim_002"),
            "caption": "🎤 Василий: «Договорились»"
        },
        "photo": FILE_IDS.get("choice_handshake"),
        "choices": [
            {"text": "🤝 Пожать руку", "next_scene": "money_flow"},
            {"text": "😤 Уйти молча", "next_scene": "money_flow", "effect": {"vadim_trust": -1}}
        ]
    },

    "vadim_conflict": {
        "text": "Ты отказываешься. Василий улыбается. «Ты пожалеешь, Ирина», — говорит он. И уходит. Ты знаешь — это не конец.",
        "video": FILE_IDS.get("video_vadim_leave"),
        "voice": {
            "type": "voice_message",
            "file": FILE_IDS.get("voice_vadim_threat"),
            "caption": "🎤 Василий: «Ты пожалеешь»"
        },
        "choices": [
            {"text": "➡️ ПРОДОЛЖИТЬ", "next_scene": "money_flow"}
        ]
    },

    "money_flow": {
        "text": "Дни и ночи сливаются в один бесконечный поток. Деньги, люди, закладки. Ты покупаешь машину. Ты покупаешь вещи. Ты покупаешь иллюзию.",
        "video": FILE_IDS.get("video_money_flow"),
        "voice": {
            "type": "news",
            "file": FILE_IDS.get("news_001"),
            "caption": "📻 В новостях говорят о нарколабораториях..."
        },
        "choices": [
            {"text": "📺 Смотреть новости", "next_scene": "news_lab"},
            {"text": "📱 Выключить", "next_scene": "mother_discovers"}
        ]
    },

    "news_lab": {
        "text": "Ты смотришь новости. Диктор говорит о нарколабораториях в Парголово. Ты смотришь на экран и понимаешь — это про тебя.",
        "voice": {
            "type": "news",
            "file": FILE_IDS.get("news_002"),
            "caption": "📻 Новости: «В Парголово обнаружена нарколаборатория»"
        },
        "choices": [
            {"text": "➡️ ПРОДОЛЖИТЬ", "next_scene": "mother_discovers"}
        ]
    },

    "mother_discovers": {
        "text": "Мать находит у тебя шприц. Она смотрит на тебя. В её глазах — боль и отвращение. Ты пытаешься что-то сказать, но слова не идут.",
        "voice": {
            "type": "call",
            "file": FILE_IDS.get("call_mother_003"),
            "caption": "📞 Мать: «Ты убиваешь себя»"
        },
        "photo": FILE_IDS.get("photo_mother_angry"),
        "choices": [
            {"text": "😔 Признаться", "next_scene": "mother_cuts_off", "effect": {"mother_trust": -2}},
            {"text": "🤥 Соврать", "next_scene": "son_visits", "effect": {"mother_trust": -3}}
        ]
    },

    "mother_cuts_off": {
        "text": "Мать говорит: «Ты больше не моя дочь». Она закрывает дверь. Ты слышишь, как щёлкает замок. Ты теряешь последнюю нить.",
        "voice": {
            "type": "call",
            "file": FILE_IDS.get("call_mother_cut"),
            "caption": "📞 Мать: «Ты больше не моя дочь»"
        },
        "photo": FILE_IDS.get("photo_closed_door"),
        "choices": [
            {"text": "➡️ ПРОДОЛЖИТЬ", "next_scene": "son_visits"}
        ]
    },

    "son_visits": {
        "text": "Сын приезжает к тебе. Он уже взрослый. Он смотрит на тебя. Ты пытаешься улыбнуться. Он говорит: «Мама, я скучаю». Ты плачешь.",
        "video": FILE_IDS.get("video_son_visits"),
        "voice": {
            "type": "call",
            "file": FILE_IDS.get("call_son_002"),
            "caption": "📞 Сын: «Мама, я скучаю»"
        },
        "photo": FILE_IDS.get("photo_son"),
        "save_point": True,
        "choices": [
            {"text": "❤️ Провести время с сыном", "next_scene": "chapter2_end", "effect": {"son_affection": 2}},
            {"text": "💼 Уйти на дело", "next_scene": "chapter2_end", "effect": {"son_affection": -1}}
        ]
    },

    "chapter2_end": {
        "text": "Ты стоишь на крыше. Город внизу. Ты — королева. Но корона сжимает голову. Ты знаешь — это только начало.",
        "video": FILE_IDS.get("video_chapter2_end"),
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_chapter2_end"),
            "caption": "🎙️ Корона сжимает голову..."
        },
        "choices": [
            {"text": "➡️ ПРОДОЛЖИТЬ", "next_scene": "chapter3_start"}
        ]
    },

    # ============================================================
    # ГЛАВА 3: «Сделка с дьяволом»
    # ============================================================

    "chapter3_start": {
        "text": "Ты всё глубже увязаешь в этом мире. Деньги, власть, страх. Ты больше не контролируешь ситуацию. Ситуация контролирует тебя.",
        "video": FILE_IDS.get("video_chapter3_start"),
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_chapter3"),
            "caption": "🎙️ Я больше не контролирую..."
        },
        "choices": [
            {"text": "➡️ ПРОДОЛЖИТЬ", "next_scene": "vadim_demand"}
        ]
    },

    "vadim_demand": {
        "text": "Василий звонит. Он требует больше. 30 литров в месяц. Ты понимаешь — это ловушка. Если ты откажешься — ты труп. Если согласишься — ты раб.",
        "voice": {
            "type": "call",
            "file": FILE_IDS.get("call_vadim_002"),
            "caption": "📞 Василий: «30 литров в месяц»"
        },
        "photo": FILE_IDS.get("choice_vadim_demand"),
        "choices": [
            {"text": "💪 Согласиться", "next_scene": "edik_breaks", "effect": {"vadim_trust": -1, "law_balance": -1}},
            {"text": "🚫 Отказаться", "next_scene": "kronstadt_visit", "effect": {"vadim_trust": -2}}
        ]
    },

    "edik_breaks": {
        "text": "Эдик сдаёт тебя кронштадтским. Ты узнаёшь об этом от общего знакомого. Ты чувствуешь предательство. Холод. Пустоту.",
        "voice": {
            "type": "voice_message",
            "file": FILE_IDS.get("voice_edik_002"),
            "caption": "🎤 Эдик: «Прости, Ирка... я не хотел»"
        },
        "photo": FILE_IDS.get("photo_edik_betrayal"),
        "choices": [
            {"text": "😡 Разорвать с Эдиком", "next_scene": "kronstadt_visit", "effect": {"edik_trust": -3}},
            {"text": "🤝 Простить", "next_scene": "kronstadt_visit", "effect": {"edik_trust": -1}}
        ]
    },

    "kronstadt_visit": {
        "text": "Ты в гостинице. Стук в дверь. Кронштадтские приехали. Ты слышишь голоса за дверью. У тебя есть несколько секунд.",
        "video": FILE_IDS.get("video_kronstadt"),
        "voice": {
            "type": "ambient",
            "file": FILE_IDS.get("ambient_knock"),
            "caption": "🔊 Стук в дверь..."
        },
        "photo": FILE_IDS.get("choice_hotel_door"),
        "mini_game": {
            "type": "qte",
            "duration": 5,
            "button_text": "🏃 Убежать!",
            "success_text": "✅ Ты выпрыгнула в окно!",
            "fail_text": "❌ Они ворвались. Фатально.",
            "fail_scene": "game_over",
            "next_scene": "kronstadt_escape_success"
        }
    },

    "kronstadt_escape_success": {
        "text": "Ты выпрыгиваешь в окно. Падаешь в сугроб. Снег обжигает лицо. Ты слышишь крики за спиной. Ты бежишь. Ты жива.",
        "video": FILE_IDS.get("video_escape"),
        "voice": {
            "type": "ambient",
            "file": FILE_IDS.get("ambient_run"),
            "caption": "🔊 Ты бежишь..."
        },
        "choices": [
            {"text": "📱 Позвонить Эдику", "next_scene": "edik_final"},
            {"text": "🚗 Уехать", "next_scene": "arrest_premonition"}
        ]
    },

    "edik_final": {
        "text": "Ты звонишь Эдику. Он не отвечает. Ты понимаешь — он мёртв. Или сбежал. Теперь ты одна.",
        "voice": {
            "type": "call",
            "file": FILE_IDS.get("call_edik_dead"),
            "caption": "📞 Эдик не отвечает..."
        },
        "choices": [
            {"text": "➡️ ПРОДОЛЖИТЬ", "next_scene": "arrest_premonition"}
        ]
    },

    "arrest_premonition": {
        "text": "Ты сидишь в машине. Снег идёт. Ты смотришь в зеркало и видишь своё лицо. Уставшее. Пустое. Ты знаешь — они придут.",
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_premonition"),
            "caption": "🎙️ Я знаю — они придут..."
        },
        "photo": FILE_IDS.get("choice_arrest_premonition"),
        "choices": [
            {"text": "➡️ ПРОДОЛЖИТЬ", "next_scene": "chapter3_end"}
        ]
    },

    "chapter3_end": {
        "text": "Ты знаешь — это конец. Или начало. Всё зависит от того, как ты это назовёшь.",
        "video": FILE_IDS.get("video_chapter3_end"),
        "voice": {
            "type": "news",
            "file": FILE_IDS.get("news_003"),
            "caption": "📻 Новости: «Крупная нарколаборатория раскрыта»"
        },
        "choices": [
            {"text": "➡️ ПРОДОЛЖИТЬ", "next_scene": "chapter4_start"}
        ]
    },

    # ============================================================
    # ГЛАВА 4: «Падение»
    # ============================================================

    "chapter4_start": {
        "text": "Январь 2013. Ты едешь к другу. На пассажирском — капуста и тесто. Ты думаешь о пирожках. Ты не знаешь, что это твой последний день свободы.",
        "video": FILE_IDS.get("video_chapter4_start"),
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_chapter4"),
            "caption": "🎙️ Последний день свободы..."
        },
        "choices": [
            {"text": "➡️ ПРОДОЛЖИТЬ", "next_scene": "arrest"}
        ]
    },

    "arrest": {
        "text": "Мигалки. Машины ГНК. Тебя блокируют. Ты смотришь на них и улыбаешься. Ты открываешь бутират и выпиваешь всё. Ты начинаешь танцевать.",
        "video": FILE_IDS.get("video_arrest"),
        "voice": {
            "type": "ambient",
            "file": FILE_IDS.get("ambient_arrest"),
            "caption": "🔊 Мигалки. Снег. Крики."
        },
        "photo": FILE_IDS.get("choice_arrest"),
        "save_point": True,
        "choices": [
            {"text": "💃 Танцевать", "next_scene": "arrest_dance"},
            {"text": "😐 Сдаться", "next_scene": "gnk_cell"}
        ]
    },

    "arrest_dance": {
        "text": "Ты танцуешь на снегу. В тапочках-свинках. Без шнурков. Ты смеёшься. Ты — королева. Даже в наручниках.",
        "video": FILE_IDS.get("video_arrest_dance"),
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_arrest_dance"),
            "caption": "🎙️ Я — королева. Даже в наручниках."
        },
        "photo": FILE_IDS.get("photo_arrest_dance"),
        "choices": [
            {"text": "➡️ ПРОДОЛЖИТЬ", "next_scene": "gnk_cell"}
        ]
    },

    "gnk_cell": {
        "text": "Ты в камере ГНК. Без шнурков. Ты просишь курить. Надзирательница говорит: «Помой полы — получишь сигарету».",
        "voice": {
            "type": "ambient",
            "file": FILE_IDS.get("ambient_gnk_cell"),
            "caption": "🔊 Камера ГНК..."
        },
        "photo": FILE_IDS.get("photo_gnk_cell"),
        "mini_game": {
            "type": "clicker",
            "steps": 5,
            "button_text": "🧹 Тереть шваброй",
            "progress_text": "🧹 Прогресс: {current}/{total}",
            "complete_text": "✅ Полы чистые. Ты получила сигарету.",
            "fail_text": "❌ Ты устала. Попробуй снова.",
            "timeout": 30,
            "next_scene": "interrogation"
        }
    },

    "interrogation": {
        "text": "Следователь: «Будешь сдавать всех, с кем работала». Ты смотришь на него. Ты знаешь — это твой шанс. Или ловушка.",
        "voice": {
            "type": "call",
            "file": FILE_IDS.get("call_interrogation"),
            "caption": "📞 Следователь: «Сдавай всех»"
        },
        "photo": FILE_IDS.get("choice_interrogation"),
        "choices": [
            {"text": "🤫 Молчать", "next_scene": "court", "effect": {"law_balance": 1}},
            {"text": "🗣️ Сдать вымышленных людей", "next_scene": "court", "effect": {"law_balance": -1}}
        ]
    },

    "court": {
        "text": "Суд. Ты в клетке. Ты смотришь на сына. Он смотрит на тебя. Судья читает приговор: «8 лет колонии общего режима».",
        "video": FILE_IDS.get("video_court"),
        "voice": {
            "type": "ambient",
            "file": FILE_IDS.get("ambient_court"),
            "caption": "🔊 Зал суда..."
        },
        "photo": FILE_IDS.get("photo_court"),
        "choices": [
            {"text": "😐 Принять", "next_scene": "sentence"},
            {"text": "😭 Упасть в обморок", "next_scene": "sentence"}
        ]
    },

    "sentence": {
        "text": "Ты слышишь приговор. 8 лет. Ты не плачешь. Ты смотришь на сына. Он вырастет без тебя. Это самое страшное наказание.",
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_sentence"),
            "caption": "🎙️ 8 лет..."
        },
        "photo": FILE_IDS.get("photo_sentence"),
        "choices": [
            {"text": "➡️ ПРОДОЛЖИТЬ", "next_scene": "sizo"}
        ]
    },

    "sizo": {
        "text": "Ты в СИЗО. Металлическая дверь закрывается. Ты слышишь лязг. Ты понимаешь — это твоя новая жизнь.",
        "video": FILE_IDS.get("video_sizo"),
        "voice": {
            "type": "ambient",
            "file": FILE_IDS.get("ambient_sizo"),
            "caption": "🔊 Металлический лязг..."
        },
        "photo": FILE_IDS.get("photo_sizo"),
        "choices": [
            {"text": "➡️ ПРОДОЛЖИТЬ", "next_scene": "colony_arrival"}
        ]
    },

    "colony_arrival": {
        "text": "Ты в колонии. Женщины смотрят на тебя. Ты бросаешь матрас. Ты говоришь: «Привет, девочки. Я — Ира. 228-я».",
        "video": FILE_IDS.get("video_colony"),
        "voice": {
            "type": "ambient",
            "file": FILE_IDS.get("ambient_colony"),
            "caption": "🔊 Колония..."
        },
        "photo": FILE_IDS.get("photo_colony"),
        "choices": [
            {"text": "💪 Драться", "next_scene": "colony_fight", "effect": {"colony_rep": 1}},
            {"text": "🤝 Принять правила", "next_scene": "colony_life", "effect": {"colony_rep": -1}}
        ]
    },

    "colony_fight": {
        "text": "Ты дерёшься с цыганами. Ты ломаешь палец. Ты выигрываешь. Тебя уважают. Ты — не жертва.",
        "video": FILE_IDS.get("video_colony_fight"),
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_colony_fight"),
            "caption": "🎙️ Я сломала палец. Но не сломалась."
        },
        "photo": FILE_IDS.get("photo_colony_fight"),
        "choices": [
            {"text": "➡️ ПРОДОЛЖИТЬ", "next_scene": "colony_life"}
        ]
    },

    "colony_life": {
        "text": "Дни превращаются в годы. Ты шьёшь, ты выживаешь, ты ждёшь. Ты знаешь — ты выйдешь. Ты обещала себе.",
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_colony_life"),
            "caption": "🎙️ Я выйду. Я обещала себе."
        },
        "photo": FILE_IDS.get("photo_colony_life"),
        "choices": [
            {"text": "➡️ ПРОДОЛЖИТЬ", "next_scene": "chapter4_end"}
        ]
    },

    "chapter4_end": {
        "text": "Восемь лет. Ты выжила. Ты — не та, кем была. Ты — Ира. И ты идёшь дальше.",
        "video": FILE_IDS.get("video_chapter4_end"),
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_chapter4_end"),
            "caption": "🎙️ Я — Ира. И я иду дальше."
        },
        "choices": [
            {"text": "➡️ ПРОДОЛЖИТЬ", "next_scene": "chapter5_start"}
        ]
    },

    # ============================================================
    # ГЛАВА 5: «Зелёный навсегда»
    # ============================================================

    "chapter5_start": {
        "text": "2020. Ты выходишь на свободу. Снег идёт. Ты вдыхаешь воздух. Ты — свободна. Но что дальше?",
        "video": FILE_IDS.get("video_freedom"),
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_freedom"),
            "caption": "🎙️ Я свободна. Что дальше?"
        },
        "photo": FILE_IDS.get("photo_freedom"),
        "choices": [
            {"text": "➡️ ПРОДОЛЖИТЬ", "next_scene": "job_search"}
        ]
    },

    "job_search": {
        "text": "Ты ищешь работу. Ты идёшь по собеседованиям. Ты слышишь «нет» снова и снова. Ты не сдаёшься.",
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_job_search"),
            "caption": "🎙️ «Нет» снова и снова..."
        },
        "photo": FILE_IDS.get("photo_job_search"),
        "choices": [
            {"text": "💪 Продолжать искать", "next_scene": "sewing"},
            {"text": "😞 Сдаться", "next_scene": "bad_end"}
        ]
    },

    "sewing": {
        "text": "Ты находишь работу. Ты шьёшь одежду для собак. Это не наркотики. Это — жизнь. Ты начинаешь заново.",
        "video": FILE_IDS.get("video_sewing"),
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_sewing"),
            "caption": "🎙️ Я шью одежду для собак. Это — жизнь."
        },
        "photo": FILE_IDS.get("photo_sewing"),
        "choices": [
            {"text": "📱 Позвонить сыну", "next_scene": "son_final_call"},
            {"text": "✉️ Написать матери", "next_scene": "mother_letter"}
        ]
    },

    "son_final_call": {
        "text": "Ты звонишь сыну. Он взрослый. Он говорит: «Мама, я горжусь тобой». Ты плачешь. В первый раз за много лет — от счастья.",
        "voice": {
            "type": "call",
            "file": FILE_IDS.get("call_son_final"),
            "caption": "📞 Сын: «Мама, я горжусь тобой»"
        },
        "photo": FILE_IDS.get("photo_son_adult"),
        "choices": [
            {"text": "❤️ Обнять сына", "next_scene": "ideal_end", "effect": {"son_affection": 5}},
            {"text": "😢 Сказать, что скучала", "next_scene": "neutral_end", "effect": {"son_affection": 3}}
        ]
    },

    "mother_letter": {
        "text": "Ты пишешь письмо матери. Ты просишь прощения. Ты не знаешь, прочитает ли она. Но ты пытаешься.",
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_mother_letter"),
            "caption": "🎙️ Я пишу письмо матери..."
        },
        "photo": FILE_IDS.get("photo_letter"),
        "choices": [
            {"text": "✉️ Отправить письмо", "next_scene": "neutral_end", "effect": {"mother_trust": 2}},
            {"text": "🔥 Сжечь письмо", "next_scene": "bad_end", "effect": {"mother_trust": -3}}
        ]
    },

    "temptation_final": {
        "text": "Ты видишь зелёный цвет. Лакмусовая бумажка. Запах знакомого раствора. Всё внутри кричит: «Вернись!» Ты колеблешься.",
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_temptation"),
            "caption": "🎙️ Зелёный... Он зовёт меня..."
        },
        "photo": FILE_IDS.get("choice_temptation"),
        "choices": [
            {"text": "💪 Устоять", "next_scene": "ideal_end", "effect": {"addiction": -5}},
            {"text": "💉 Сдаться", "next_scene": "bad_end", "effect": {"addiction": 5}}
        ]
    },

    # ============================================================
    # ФИНАЛЫ
    # ============================================================

    "ideal_end": {
        "text": "🏆 ИДЕАЛЬНЫЙ ФИНАЛ.\n\nТы выбрала жизнь. Ты выбрала сына. Ты выбрала свободу. Ты — Ира. Ты — та, кто выжила. Та, кто не вернулась в прошлое. Зелёный остался в прошлом. А ты — здесь. И это — победа.",
        "video": FILE_IDS.get("video_ideal_end"),
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_ideal"),
            "caption": "🎙️ Я выбрала жизнь. Это победа."
        },
        "photo": FILE_IDS.get("photo_ideal_end"),
        "choices": []
    },

    "neutral_end": {
        "text": "🔸 НЕЙТРАЛЬНЫЙ ФИНАЛ.\n\nТы не стала королевой. Ты не сломалась. Ты просто выжила. Ты живёшь дальше. Это не победа, но это не поражение. Ты — та, кто идёт дальше.",
        "video": FILE_IDS.get("video_neutral_end"),
        "voice": {
            "type": "diary",
            "file": FILE_IDS.get("diary_neutral"),
            "caption": "🎙️ Я иду дальше..."
        },
        "photo": FILE_IDS.get("photo_neutral_end"),
        "choices": []
    },

    "bad_end": {
        "text": "💀 ПЛОХОЙ ФИНАЛ.\n\nТы не выдержала. Ты вернулась. Ты потеряла всё. Сына, себя, свободу. Зелёный победил. Ты — королева пустоты. Навсегда.",
        "video": FILE_IDS.get("video_bad_end"),
        "voice": {
            "type": "news",
            "file": FILE_IDS.get("news_bad_end"),
            "caption": "📻 Труп женщины найден в Парголово..."
        },
        "photo": FILE_IDS.get("photo_bad_end"),
        "choices": []
    },

    "game_over": {
        "text": "💀 ИГРА ОКОНЧЕНА.\n\nИра погибла. Фатальный выбор. Но у тебя есть сохранение!",
        "video": FILE_IDS.get("video_gameover"),
        "voice": {
            "type": "news",
            "file": FILE_IDS.get("news_gameover"),
            "caption": "📻 Срочная новость: в Петербурге обнаружено тело..."
        },
        "photo": FILE_IDS.get("photo_gameover"),
        "choices": [
            {"text": "🔄 ЗАГРУЗИТЬ СОХРАНЕНИЕ", "callback_data": "load_save"},
            {"text": "🔁 НАЧАТЬ ЗАНОВО", "callback_data": "restart_game"}
        ]
    }
}
