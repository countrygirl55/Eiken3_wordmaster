import streamlit as st
import sqlite3
import pandas as pd
import random
import os
import re
import csv
import json
import base64

# Set up page config
st.set_page_config(
    page_title="英検3級 単語マスター v31",
    page_icon="📖",
    layout="centered"
)

# Embed base64 sounds
CHIME_B64 = "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"
BUZZER_B64 = "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vDi6OLk4uDi3OLU4tDizOLE4sDivOK04rDirOKk4qDinOKU4pDijOKE4oDifOJ44nDibOJo4mDiXOJY4lDiTOG7HcMdxx3LHdMd1x3bHeMd5x3rHe8d9x37Hf8eBx4LHg8eFx4bHh8eJx4rHi8eNx47Hj8eQx5LHk8eUx5bHl8eYx5rHm8ecx57HYThgOF84XThcOFs4WThYOFc4VThUOFM4UThQOE84TjhMOEs4SjhIOEc4RjhEOEM4QjhAOD84Pjg9ODs4Ojg5ODc4Njg1ODM4MjjPx9HH0sfTx9TH1sfXx9jH2sfbx9zH3sffx+DH4cfjx+TH5cfnx+jH6cfrx+zH7cfux/DH8cfyx/TH9cf2x/jH+cf6x/vH/ccCOAE4/zf+N/03+zf6N/k3+Df2N/U39DfyN/E38DfuN+037DfrN+k36DfnN+U35DfjN+E34DffN9433DfbN9o32DfXN9Y31DfTNy7IL8gxyDLIM8g1yDbIN8g5yDrIO8g8yD7IP8hAyELIQ8hEyEXIR8hIyEnIS8hMyE3IT8hQyFHIUshUyFXIVshYyFnIWshbyF3IojehN583njedN5w3mjeZN5g3ljeVN5Q3kjeRN5A3jzeNN4w3izeJN4g3hzeGN4Q3gzeCN4A3fzd+N303ezd6N3k3dzd2N3U3dDeOyI/IkMiSyJPIlMiVyJfImMiZyJvInMidyJ7IoMihyKLIpMilyKbIp8ipyKrIq8ityK7Ir8iwyLLIs8i0yLbIt8i4yLnIu8hEN0M3QTdANz83Pjc8Nzs3Ojc4Nzc3Njc1NzM3MjcxNy83LjctNyw3KjcpNyg3JzclNyQ3IzchNyA3HzceNxw3GzcaNxg3FzcWN+vI7cjuyO/I8cjyyPPI9Mj2yPfI+Mj5yPvI/Mj9yP/IAMkByQLJBMkFyQbJCMkJyQrJC8kNyQ7JD8kQyRLJE8kUyRbJF8kYyRnJ5TbkNuM24jbgNt823jbcNts22jbZNtc21jbVNtQ20jbRNtA2zjbNNsw2yzbJNsg2xzbGNsQ2wzbCNsA2vza+Nr02uza6Nrk2uDZKyUvJTMlOyU/JUMlRyVPJVMlVyVbJWMlZyVrJXMldyV7JX8lhyWLJY8lkyWbJZ8loyWnJa8lsyW3Jb8lwyXHJcsl0yXXJdsmJNoc2hjaFNoQ2gjaBNoA2fjZ9Nnw2ezZ5Nng2dzZ2NnQ2czZyNnE2bzZuNm02bDZqNmk2aDZmNmU2ZDZjNmE2YDZfNl42XDZbNqbJp8mpyarJq8msya7Jr8mwybLJs8m0ybXJt8m4ybnJusm8yb3Jvsm/ycHJwsnDycTJxsnHycjJycnLyczJzcnPydDJ0cnSydTJKzYqNik2JzYmNiU2JDYiNiE2IDYfNh02HDYbNho2GDYXNhY2FTYTNhI2ETYQNg42DTYMNgs2CTYINgc2BjYENgM2AjYBNv81/jUDygXKBsoHygjKCsoLygzKDcoPyhDKEcoSyhTKFcoWyhfKGcoayhvKHMoeyh/KIMohyiPKJMolyibKKMopyirKK8otyi7KL8rQNc41zTXMNcs1yTXINcc1xjXENcM1wjXBNb81vjW9Nbw1ujW5Nbg1tzW1NbQ1szWyNbA1rzWuNa01qzWqNak1qDWnNaU1pDWjNV7KYMphymLKY8plymbKZ8poymrKa8psym3Kb8pwynHKcsp0ynXKdsp3ynnKesp7ynzKfsp/yoDKgcqDyoTKhcqGyojKicqKyovKdDVyNXE1cDVvNW01bDVrNWo1aDVnNWY1ZTVjNWI1YTVgNV41XTVcNVs1WTVYNVc1VjVVNVM1UjVRNVA1TjVNNUw1SzVJNUg1RzW6yrzKvcq+yr/KwcrCysPKxMrFysfKyMrJysrKzMrNys7Kz8rRytLK08rUytbK18rYytnK2srcyt3K3srfyuHK4srjyuTK5soZNRg1FzUWNRQ1EzUSNRE1DzUONQ01DDUKNQk1CDUHNQY1BDUDNQI1ATX/NP40/TT8NPo0+TT4NPc09jT0NPM08jTxNO807jTtNBTLFssXyxjLGcsayxzLHcseyx/LIcsiyyPLJMsmyyfLKMspyyrLLMstyy7LL8sxyzLLM8s0yzXLN8s4yznLOss8yz3LPss/y0DLvjS9NLw0uzS5NLg0tzS2NLQ0szSyNLE0sDSuNK00rDSrNKk0qDSnNKY0pTSjNKI0oTSgNJ40nTScNJs0mjSYNJc0ljSVNJM0kjRvy3DLcctzy3TLdct2y3fLect6y3vLfMt+y3/LgMuBy4LLhMuFy4bLh8uJy4rLi8uMy43Lj8uQy5HLksuUy5XLlsuXy5jLmstlNGQ0YzRiNGA0XzReNF00WzRaNFk0WDRXNFU0VDRTNFI0UTRPNE40TTRMNEo0STRINEc0RjRENEM0QjRBNEA0PjQ9NDw0OzQ5NMjLycvKy8vLzcvOy8/L0MvRy9PL1MvVy9bL2MvZy9rL28vcy97L38vgy+HL4svky+XL5svny+jL6svry+zL7cvvy/DL8cvyy/PLCzQKNAk0CDQHNAU0BDQDNAI0ATT/M/4z/TP8M/sz+TP4M/cz9jP1M/Mz8jPxM/Az7jPtM+wz6zPqM+gz5zPmM+Uz5DPiM+Ez4DMhzCLMJMwlzCbMJ8wozCrMK8wszC3MLswwzDHMMswzzDTMNsw3zDjMOcw6zDzMPcw+zD/MQMxCzEPMRMxFzEbMSMxJzErMS8y0M7IzsTOwM68zrjOsM6szqjOpM6gzpjOlM6QzozOiM6AznzOeM50znDOaM5kzmDOXM5YzlDOTM5IzkTOQM44zjTOMM4szijOIM3nMesx7zHzMfsx/zIDMgcyCzITMhcyGzIfMiMyKzIvMjMyNzI7MkMyRzJLMk8yUzJbMl8yYzJnMmsybzJ3MnsyfzKDMocyjzKTMWzNaM1kzVzNWM1UzVDNTM1EzUDNPM04zTTNLM0ozSTNIM0czRjNEM0MzQjNBM0AzPjM9MzwzOzM6MzgzNzM2MzUzNDMyMzEzMDPRzNLM08zVzNbM18zYzNnM28zczN3M3szfzOHM4szjzOTM5czmzOjM6czqzOvM7MzuzO/M8MzxzPLM9Mz1zPbM98z4zPnM+8wEMwMzAjMBM/8y/jL9Mvwy+zL6Mvgy9zL2MvUy9DLyMvEy8DLvMu4y7TLrMuoy6TLoMucy5TLkMuMy4jLhMuAy3jLdMtwy2zLaMijNKc0qzSvNLM0tzS/NMM0xzTLNM801zTbNN804zTnNOs08zT3NPs0/zUDNQs1DzUTNRc1GzUfNSc1KzUvNTM1NzU7NUM1RzVLNrTKsMqoyqTKoMqcypjKlMqMyojKhMqAynzKeMpwymzKaMpkymDKWMpUylDKTMpIykTKPMo4yjTKMMosyijKIMocyhjKFMoQygzJ/zYDNgc2CzYPNhM2GzYfNiM2JzYrNjM2NzY7Nj82QzZHNk82UzZXNls2XzZjNms2bzZzNnc2ezZ/Noc2izaPNpM2lzabNqM1XMlYyVTJUMlMyUTJQMk8yTjJNMkwySjJJMkgyRzJGMkUyQzJCMkEyQDI/Mj4yPDI7MjoyOTI4MjcyNTI0MjMyMjIxMjAyLjItMtTN1c3WzdfN2c3azdvN3M3dzd7N4M3hzeLN483kzeXN583ozenN6s3rzezN7s3vzfDN8c3yzfPN9c32zffN+M35zfrN/M39zf7NATIAMv8x/jH8Mfsx+jH5Mfgx9zH1MfQx8zHyMfEx8DHuMe0x7DHrMeox6THnMeYx5THkMeMx4jHhMd8x3jHdMdwx2zHaMdgx"

# Embed backup dictionary
BACKUP_WORDS = [
  {
    "番号": 1,
    "単語": "look",
    "品詞": "動詞",
    "訳語": "～に見える、見る",
    "レベル": "A"
  },
  {
    "番号": 2,
    "単語": "take",
    "品詞": "動詞",
    "訳語": "(時間などが）かかる、（乗り物）に乗る、〜を持っていく、（試験・授業など）を受ける",
    "レベル": "A"
  },
  {
    "番号": 3,
    "単語": "make A B",
    "品詞": "動詞",
    "訳語": "AをBにする、～を作る、～を行う",
    "レベル": "A"
  },
  {
    "番号": 4,
    "単語": "see",
    "品詞": "動詞",
    "訳語": "～が見える、〜を見る、～に会う、わかる",
    "レベル": "A"
  },
  {
    "番号": 5,
    "単語": "watch",
    "品詞": "動詞",
    "訳語": "〜を（注意して）見る",
    "レベル": "A"
  },
  {
    "番号": 6,
    "単語": "give 人 もの",
    "品詞": "動詞",
    "訳語": "（人）に（もの）を与える",
    "レベル": "A"
  },
  {
    "番号": 7,
    "単語": "work",
    "品詞": "動詞",
    "訳語": "働く、（機械などが）働く、（作業を）する",
    "レベル": "A"
  },
  {
    "番号": 8,
    "単語": "call A B",
    "品詞": "動詞",
    "訳語": "AをBと呼ぶ、電話する",
    "レベル": "A"
  },
  {
    "番号": 9,
    "単語": "enjoy",
    "品詞": "動詞",
    "訳語": "〜を楽しむ",
    "レベル": "A"
  },
  {
    "番号": 10,
    "単語": "find",
    "品詞": "動詞",
    "訳語": "〜を見つける、～とわかる",
    "レベル": "A"
  },
  {
    "番号": 11,
    "単語": "practice",
    "品詞": "動詞",
    "訳語": "〜を練習する",
    "レベル": "A"
  },
  {
    "番号": 12,
    "単語": "tell 人 もの・こと",
    "品詞": "動詞",
    "訳語": "（人）に（もの・こと）を話す",
    "レベル": "A"
  },
  {
    "番号": 13,
    "単語": "leave",
    "品詞": "動詞",
    "訳語": "〜を置き忘れる、～を残す、～を出発する",
    "レベル": "A"
  },
  {
    "番号": 14,
    "単語": "need",
    "品詞": "動詞",
    "訳語": "〜を必要とする",
    "レベル": "A"
  },
  {
    "番号": 15,
    "単語": "say",
    "品詞": "動詞",
    "訳語": "〜と言う、書いてある",
    "レベル": "A"
  },
  {
    "番号": 16,
    "単語": "finish",
    "品詞": "動詞",
    "訳語": "〜を終える、～が終わる",
    "レベル": "A"
  },
  {
    "番号": 17,
    "単語": "sell",
    "品詞": "動詞",
    "訳語": "〜を売る",
    "レベル": "A"
  },
  {
    "番号": 18,
    "単語": "clean",
    "品詞": "動詞",
    "訳語": "〜をきれいにする、～を掃除する",
    "レベル": "A"
  },
  {
    "番号": 19,
    "単語": "wait",
    "品詞": "動詞",
    "訳語": "待つ",
    "レベル": "A"
  },
  {
    "番号": 20,
    "単語": "become",
    "品詞": "動詞",
    "訳語": "〜になる",
    "レベル": "A"
  },
  {
    "番号": 21,
    "単語": "show 人 もの",
    "品詞": "動詞",
    "訳語": "（人）に（もの）を見せる、〜を見せる",
    "レベル": "A"
  },
  {
    "番号": 22,
    "単語": "join",
    "品詞": "動詞",
    "訳語": "～に加わる、～に参加する",
    "レベル": "A"
  },
  {
    "番号": 23,
    "単語": "bring",
    "品詞": "動詞",
    "訳語": "～をのもってくる、連れてくる",
    "レベル": "A"
  },
  {
    "番号": 24,
    "単語": "move",
    "品詞": "動詞",
    "訳語": "動く、〜を動かす、引っ越す",
    "レベル": "A"
  },
  {
    "番号": 25,
    "単語": "put",
    "品詞": "動詞",
    "訳語": "〜を置く",
    "レベル": "A"
  },
  {
    "番号": 26,
    "単語": "drive",
    "品詞": "動詞",
    "訳語": "～を車で送る、運転する",
    "レベル": "A"
  },
  {
    "番号": 27,
    "単語": "rain",
    "品詞": "動詞",
    "訳語": "雨が降る",
    "レベル": "A"
  },
  {
    "番号": 28,
    "単語": "win",
    "品詞": "動詞",
    "訳語": "～に勝つ、～を勝ち取る",
    "レベル": "A"
  },
  {
    "番号": 29,
    "単語": "speak",
    "品詞": "動詞",
    "訳語": "～を話す",
    "レベル": "A"
  },
  {
    "番号": 30,
    "単語": "travel",
    "品詞": "動詞",
    "訳語": "旅行する",
    "レベル": "A"
  },
  {
    "番号": 31,
    "単語": "hope",
    "品詞": "動詞",
    "訳語": "～を望む、～を願う",
    "レベル": "A"
  },
  {
    "番号": 32,
    "単語": "ride",
    "品詞": "動詞",
    "訳語": "〜に乗る",
    "レベル": "A"
  },
  {
    "番号": 33,
    "単語": "sound",
    "品詞": "動詞",
    "訳語": "〜に聞こえる、音がする",
    "レベル": "A"
  },
  {
    "番号": 34,
    "単語": "wear",
    "品詞": "動詞",
    "訳語": "〜を着ている、身につけている",
    "レベル": "A"
  },
  {
    "番号": 35,
    "単語": "train",
    "品詞": "名詞",
    "訳語": "列車、電車",
    "レベル": "A"
  },
  {
    "番号": 36,
    "単語": "hour",
    "品詞": "名詞",
    "訳語": "（１）時間、（複で）営業時間",
    "レベル": "A"
  },
  {
    "番号": 37,
    "単語": "weekend",
    "品詞": "名詞",
    "訳語": "週末",
    "レベル": "A"
  },
  {
    "番号": 38,
    "単語": "restaurant",
    "品詞": "名詞",
    "訳語": "料理店、レストラン",
    "レベル": "A"
  },
  {
    "番号": 39,
    "単語": "food",
    "品詞": "名詞",
    "訳語": "食べ物、料理",
    "レベル": "A"
  },
  {
    "番号": 40,
    "単語": "month",
    "品詞": "名詞",
    "訳語": "月",
    "レベル": "A"
  },
  {
    "番号": 41,
    "単語": "station",
    "品詞": "名詞",
    "訳語": "駅、（警察や消防などの）署",
    "レベル": "A"
  },
  {
    "番号": 42,
    "単語": "festival",
    "品詞": "名詞",
    "訳語": "祭り",
    "レベル": "A"
  },
  {
    "番号": 43,
    "単語": "ticket",
    "品詞": "名詞",
    "訳語": "切符",
    "レベル": "A"
  },
  {
    "番号": 44,
    "単語": "minute",
    "品詞": "名詞",
    "訳語": "分、ちょっとの間",
    "レベル": "A"
  },
  {
    "番号": 45,
    "単語": "trip",
    "品詞": "名詞",
    "訳語": "旅行",
    "レベル": "A"
  },
  {
    "番号": 46,
    "単語": "movie",
    "品詞": "名詞",
    "訳語": "映画",
    "レベル": "A"
  },
  {
    "番号": 47,
    "単語": "parent",
    "品詞": "名詞",
    "訳語": "親、（複で）両親",
    "レベル": "A"
  },
  {
    "番号": 48,
    "単語": "lesson",
    "品詞": "名詞",
    "訳語": "レッスン、授業",
    "レベル": "A"
  },
  {
    "番号": 49,
    "単語": "kind",
    "品詞": "名詞",
    "訳語": "種類",
    "レベル": "A"
  },
  {
    "番号": 50,
    "単語": "money",
    "品詞": "名詞",
    "訳語": "お金",
    "レベル": "A"
  },
  {
    "番号": 51,
    "単語": "job",
    "品詞": "名詞",
    "訳語": "仕事",
    "レベル": "A"
  },
  {
    "番号": 52,
    "単語": "place",
    "品詞": "名詞",
    "訳語": "場所",
    "レベル": "A"
  },
  {
    "番号": 53,
    "単語": "office",
    "品詞": "名詞",
    "訳語": "オフィス、事務所、会社",
    "レベル": "A"
  },
  {
    "番号": 54,
    "単語": "science",
    "品詞": "名詞",
    "訳語": "科学、理科",
    "レベル": "A"
  },
  {
    "番号": 55,
    "単語": "meating",
    "品詞": "名詞",
    "訳語": "会合、会議",
    "レベル": "A"
  },
  {
    "番号": 56,
    "単語": "concert",
    "品詞": "名詞",
    "訳語": "コンサート、演奏会",
    "レベル": "A"
  },
  {
    "番号": 57,
    "単語": "plan",
    "品詞": "名詞",
    "訳語": "計画、予定",
    "レベル": "A"
  },
  {
    "番号": 58,
    "単語": "child",
    "品詞": "名詞",
    "訳語": "子ども",
    "レベル": "A"
  },
  {
    "番号": 59,
    "単語": "vacation",
    "品詞": "名詞",
    "訳語": "休み、休暇",
    "レベル": "A"
  },
  {
    "番号": 60,
    "単語": "history",
    "品詞": "名詞",
    "訳語": "歴史",
    "レベル": "A"
  },
  {
    "番号": 61,
    "単語": "contest",
    "品詞": "名詞",
    "訳語": "コンテスト",
    "レベル": "A"
  },
  {
    "番号": 62,
    "単語": "library",
    "品詞": "名詞",
    "訳語": "図書館",
    "レベル": "A"
  },
  {
    "番号": 63,
    "単語": "last",
    "品詞": "形容詞",
    "訳語": "この前の、最後の",
    "レベル": "A"
  },
  {
    "番号": 64,
    "単語": "next",
    "品詞": "形容詞",
    "訳語": "次の",
    "レベル": "A"
  },
  {
    "番号": 65,
    "単語": "famous",
    "品詞": "形容詞",
    "訳語": "有名な",
    "レベル": "A"
  },
  {
    "番号": 66,
    "単語": "popular",
    "品詞": "形容詞",
    "訳語": "人気のある",
    "レベル": "A"
  },
  {
    "番号": 67,
    "単語": "sure",
    "品詞": "形容詞",
    "訳語": "確かな、確信して",
    "レベル": "A"
  },
  {
    "番号": 68,
    "単語": "favorite",
    "品詞": "形容詞",
    "訳語": "お気に入りの、大好きな",
    "レベル": "A"
  },
  {
    "番号": 69,
    "単語": "other",
    "品詞": "形容詞",
    "訳語": "他の",
    "レベル": "A"
  },
  {
    "番号": 70,
    "単語": "late",
    "品詞": "形容詞",
    "訳語": "遅い、遅れた",
    "レベル": "A"
  },
  {
    "番号": 71,
    "単語": "special",
    "品詞": "形容詞",
    "訳語": "特別な",
    "レベル": "A"
  },
  {
    "番号": 72,
    "単語": "different",
    "品詞": "形容詞",
    "訳語": "異なる、様々な、別の",
    "レベル": "A"
  },
  {
    "番号": 73,
    "単語": "sorry",
    "品詞": "形容詞",
    "訳語": "申し訳なく思って、気の毒に思って",
    "レベル": "A"
  },
  {
    "番号": 74,
    "単語": "free",
    "品詞": "形容詞",
    "訳語": "自由な、暇な、無料の",
    "レベル": "A"
  },
  {
    "番号": 75,
    "単語": "busy",
    "品詞": "形容詞",
    "訳語": "忙しい",
    "レベル": "A"
  },
  {
    "番号": 76,
    "単語": "first",
    "品詞": "副詞",
    "訳語": "最初に、最初の、第一に",
    "レベル": "A"
  },
  {
    "番号": 77,
    "単語": "often",
    "品詞": "副詞",
    "訳語": "よく、しばしば",
    "レベル": "A"
  },
  {
    "番号": 78,
    "単語": "also",
    "品詞": "副詞",
    "訳語": "〜もまた",
    "レベル": "A"
  },
  {
    "番号": 79,
    "単語": "tonight",
    "品詞": "副詞",
    "訳語": "今夜（は）",
    "レベル": "A"
  },
  {
    "番号": 80,
    "単語": "usually",
    "品詞": "副詞",
    "訳語": "たいてい、いつもは",
    "レベル": "A"
  },
  {
    "番号": 81,
    "単語": "well",
    "品詞": "副詞",
    "訳語": "上手に、十分に、よく",
    "レベル": "A"
  },
  {
    "番号": 82,
    "単語": "hard",
    "品詞": "副詞",
    "訳語": "熱心に、激しく",
    "レベル": "A"
  },
  {
    "番号": 83,
    "単語": "just",
    "品詞": "副詞",
    "訳語": "ちょうど、ただ、たった今",
    "レベル": "A"
  },
  {
    "番号": 84,
    "単語": "early",
    "品詞": "副詞",
    "訳語": "早く",
    "レベル": "A"
  },
  {
    "番号": 85,
    "単語": "still",
    "品詞": "副詞",
    "訳語": "まだ、それでも、今でも",
    "レベル": "A"
  },
  {
    "番号": 86,
    "単語": "together",
    "品詞": "副詞",
    "訳語": "一緒に",
    "レベル": "A"
  },
  {
    "番号": 87,
    "単語": "ago",
    "品詞": "副詞",
    "訳語": "（今から）〜前に",
    "レベル": "A"
  },
  {
    "番号": 88,
    "単語": "by",
    "品詞": "前置詞",
    "訳語": "～で、～によって、〜のそばに、〜までには",
    "レベル": "A"
  },
  {
    "番号": 89,
    "単語": "around",
    "品詞": "前置詞",
    "訳語": "〜の周りに、あちこちで",
    "レベル": "A"
  },
  {
    "番号": 90,
    "単語": "during",
    "品詞": "前置詞",
    "訳語": "〜の間中",
    "レベル": "A"
  },
  {
    "番号": 91,
    "単語": "over",
    "品詞": "前置詞",
    "訳語": "〜の上に、〜を越えて",
    "レベル": "A"
  },
  {
    "番号": 92,
    "単語": "when",
    "品詞": "接続詞",
    "訳語": "〜のとき、～するとき",
    "レベル": "A"
  },
  {
    "番号": 93,
    "単語": "because",
    "品詞": "接続詞",
    "訳語": "なぜなら～なので",
    "レベル": "A"
  },
  {
    "番号": 94,
    "単語": "before",
    "品詞": "接続詞/前置詞",
    "訳語": "〜の前に、~する前に",
    "レベル": "A"
  },
  {
    "番号": 95,
    "単語": "if",
    "品詞": "接続詞",
    "訳語": "もし～なら",
    "レベル": "A"
  },
  {
    "番号": 96,
    "単語": "than ～",
    "品詞": "接続詞/前置詞",
    "訳語": "～よりも",
    "レベル": "A"
  },
  {
    "番号": 97,
    "単語": "one",
    "品詞": "代名詞",
    "訳語": "もの、ひとつ、人",
    "レベル": "A"
  },
  {
    "番号": 98,
    "単語": "all",
    "品詞": "代名詞/副詞",
    "訳語": "すべて、すべては",
    "レベル": "A"
  },
  {
    "番号": 99,
    "単語": "could",
    "品詞": "助動詞",
    "訳語": "〜できた",
    "レベル": "A"
  },
  {
    "番号": 100,
    "単語": "should",
    "品詞": "助動詞",
    "訳語": "〜すべきだ、～したほうがよい",
    "レベル": "A"
  },
  {
    "番号": 101,
    "単語": "forget",
    "品詞": "動詞",
    "訳語": "～を忘れる",
    "レベル": "A"
  },
  {
    "番号": 102,
    "単語": "break",
    "品詞": "動詞",
    "訳語": "～を割る、～を壊す、～を折る",
    "レベル": "A"
  },
  {
    "番号": 103,
    "単語": "learn",
    "品詞": "動詞",
    "訳語": "～を学ぶ、～を習う",
    "レベル": "A"
  },
  {
    "番号": 104,
    "単語": "close",
    "品詞": "動詞",
    "訳語": "～を閉める、～が閉まる",
    "レベル": "A"
  },
  {
    "番号": 105,
    "単語": "hold",
    "品詞": "動詞",
    "訳語": "（会・パーティなど）を開く、～を持つ",
    "レベル": "A"
  },
  {
    "番号": 106,
    "単語": "decide",
    "品詞": "動詞",
    "訳語": "～を決める",
    "レベル": "A"
  },
  {
    "番号": 107,
    "単語": "grow",
    "品詞": "動詞",
    "訳語": "～を栽培する、～を育てる、育つ",
    "レベル": "A"
  },
  {
    "番号": 108,
    "単語": "try",
    "品詞": "動詞",
    "訳語": "～を試す、～を試みる、努力する",
    "レベル": "A"
  },
  {
    "番号": 109,
    "単語": "happen",
    "品詞": "動詞",
    "訳語": "起こる",
    "レベル": "A"
  },
  {
    "番号": 110,
    "単語": "lose",
    "品詞": "動詞",
    "訳語": "〜を失う、～を失くす、～に負ける",
    "レベル": "A"
  },
  {
    "番号": 111,
    "単語": "arrive",
    "品詞": "動詞",
    "訳語": "到着する",
    "レベル": "A"
  },
  {
    "番号": 112,
    "単語": "send 人 もの",
    "品詞": "動詞",
    "訳語": "人にものを送る、～を送る",
    "レベル": "A"
  },
  {
    "番号": 113,
    "単語": "borrow",
    "品詞": "動詞",
    "訳語": "～を借りる",
    "レベル": "A"
  },
  {
    "番号": 114,
    "単語": "build",
    "品詞": "動詞",
    "訳語": "〜を建てる、～を作る",
    "レベル": "A"
  },
  {
    "番号": 115,
    "単語": "draw",
    "品詞": "動詞",
    "訳語": "（絵・図）を書く、線を引く、引っぱる",
    "レベル": "A"
  },
  {
    "番号": 116,
    "単語": "hear",
    "品詞": "動詞",
    "訳語": "聞こえる、〜を聞く、～を聞いて知る",
    "レベル": "A"
  },
  {
    "番号": 117,
    "単語": "carry",
    "品詞": "動詞",
    "訳語": "〜を運ぶ、～を持ち歩く",
    "レベル": "A"
  },
  {
    "番号": 118,
    "単語": "check",
    "品詞": "動詞",
    "訳語": "〜を確認する、～を調べる",
    "レベル": "A"
  },
  {
    "番号": 119,
    "単語": "pay",
    "品詞": "動詞",
    "訳語": "（お金を）払う",
    "レベル": "A"
  },
  {
    "番号": 120,
    "単語": "marry 人",
    "品詞": "動詞",
    "訳語": "人と結婚する",
    "レベル": "A"
  },
  {
    "番号": 121,
    "単語": "miss",
    "品詞": "動詞",
    "訳語": "乗り物に送れる、～をしそこなう、寂しく思う",
    "レベル": "A"
  },
  {
    "番号": 122,
    "単語": "remember",
    "品詞": "動詞",
    "訳語": "～を思い出す、～を覚えている",
    "レベル": "A"
  },
  {
    "番号": 123,
    "単語": "turn",
    "品詞": "動詞",
    "訳語": "～を曲がる、～を回す、まわる",
    "レベル": "A"
  },
  {
    "番号": 124,
    "単語": "beach",
    "品詞": "名詞",
    "訳語": "海辺、浜辺、砂浜",
    "レベル": "A"
  },
  {
    "番号": 125,
    "単語": "fun",
    "品詞": "名詞",
    "訳語": "楽しみ",
    "レベル": "A"
  },
  {
    "番号": 126,
    "単語": "idea",
    "品詞": "名詞",
    "訳語": "考え、アイデア",
    "レベル": "A"
  },
  {
    "番号": 127,
    "単語": "present",
    "品詞": "名詞",
    "訳語": "プレゼント",
    "レベル": "A"
  },
  {
    "番号": 128,
    "単語": "company",
    "品詞": "名詞",
    "訳語": "会社",
    "レベル": "A"
  },
  {
    "番号": 129,
    "単語": "event",
    "品詞": "名詞",
    "訳語": "行事、イベント",
    "レベル": "A"
  },
  {
    "番号": 130,
    "単語": "bike",
    "品詞": "名詞",
    "訳語": "自転車",
    "レベル": "A"
  },
  {
    "番号": 131,
    "単語": "store",
    "品詞": "名詞",
    "訳語": "店",
    "レベル": "A"
  },
  {
    "番号": 132,
    "単語": "street",
    "品詞": "名詞",
    "訳語": "通り",
    "レベル": "A"
  },
  {
    "番号": 133,
    "単語": "thing",
    "品詞": "名詞",
    "訳語": "もの、こと",
    "レベル": "A"
  },
  {
    "番号": 134,
    "単語": "glasses",
    "品詞": "名詞",
    "訳語": "メガネ",
    "レベル": "A"
  },
  {
    "番号": 135,
    "単語": "a.m.",
    "品詞": "名詞",
    "訳語": "午前",
    "レベル": "A"
  },
  {
    "番号": 136,
    "単語": "computer",
    "品詞": "名詞",
    "訳語": "コンピュータ",
    "レベル": "A"
  },
  {
    "番号": 137,
    "単語": "country",
    "品詞": "名詞",
    "訳語": "国、いなか",
    "レベル": "A"
  },
  {
    "番号": 138,
    "単語": "p.m.",
    "品詞": "名詞",
    "訳語": "午後",
    "レベル": "A"
  },
  {
    "番号": 139,
    "単語": "problem",
    "品詞": "名詞",
    "訳語": "問題",
    "レベル": "A"
  },
  {
    "番号": 140,
    "単語": "pumpkin",
    "品詞": "名詞",
    "訳語": "かぼちゃ",
    "レベル": "A"
  },
  {
    "番号": 141,
    "単語": "zoo",
    "品詞": "名詞",
    "訳語": "動物園",
    "レベル": "A"
  },
  {
    "番号": 142,
    "単語": "floor",
    "品詞": "名詞",
    "訳語": "床、階",
    "レベル": "A"
  },
  {
    "番号": 143,
    "単語": "museum",
    "品詞": "名詞",
    "訳語": "博物館、美術館",
    "レベル": "A"
  },
  {
    "番号": 144,
    "単語": "way",
    "品詞": "名詞",
    "訳語": "方法、道、やり方、方向",
    "レベル": "A"
  },
  {
    "番号": 145,
    "単語": "band",
    "品詞": "名詞",
    "訳語": "音楽のバンド",
    "レベル": "A"
  },
  {
    "番号": 146,
    "単語": "clothes",
    "品詞": "名詞",
    "訳語": "衣服",
    "レベル": "A"
  },
  {
    "番号": 147,
    "単語": "speech",
    "品詞": "名詞",
    "訳語": "スピーチ、演説",
    "レベル": "A"
  },
  {
    "番号": 148,
    "単語": "weather",
    "品詞": "名詞",
    "訳語": "天気、天候",
    "レベル": "A"
  },
  {
    "番号": 149,
    "単語": "supermarket",
    "品詞": "名詞",
    "訳語": "スーパーマーケット",
    "レベル": "A"
  },
  {
    "番号": 150,
    "単語": "uncle",
    "品詞": "名詞",
    "訳語": "おじ",
    "レベル": "A"
  },
  {
    "番号": 151,
    "単語": "newspaper",
    "品詞": "名詞",
    "訳語": "新聞",
    "レベル": "A"
  },
  {
    "番号": 152,
    "単語": "photo",
    "品詞": "名詞",
    "訳語": "写真",
    "レベル": "A"
  },
  {
    "番号": 153,
    "単語": "star",
    "品詞": "名詞",
    "訳語": "星、スター",
    "レベル": "A"
  },
  {
    "番号": 154,
    "単語": "grandparent",
    "品詞": "名詞",
    "訳語": "祖父、祖母  （複で）祖父母",
    "レベル": "A"
  },
  {
    "番号": 155,
    "単語": "holiday",
    "品詞": "名詞",
    "訳語": "休日、祝日",
    "レベル": "A"
  },
  {
    "番号": 156,
    "単語": "hospital",
    "品詞": "名詞",
    "訳語": "病院",
    "レベル": "A"
  },
  {
    "番号": 157,
    "単語": "pie",
    "品詞": "名詞",
    "訳語": "パイ",
    "レベル": "A"
  },
  {
    "番号": 158,
    "単語": "plane",
    "品詞": "名詞",
    "訳語": "飛行機",
    "レベル": "A"
  },
  {
    "番号": 159,
    "単語": "poster",
    "品詞": "名詞",
    "訳語": "ポスター",
    "レベル": "A"
  },
  {
    "番号": 160,
    "単語": "prize",
    "品詞": "名詞",
    "訳語": "賞、賞品",
    "レベル": "A"
  },
  {
    "番号": 161,
    "単語": "report",
    "品詞": "名詞",
    "訳語": "報告書、レポート",
    "レベル": "A"
  },
  {
    "番号": 162,
    "単語": "sir",
    "品詞": "名詞",
    "訳語": "お客様、先生",
    "レベル": "A"
  },
  {
    "番号": 163,
    "単語": "stop",
    "品詞": "名詞",
    "訳語": "停留所、止まること",
    "レベル": "A"
  },
  {
    "番号": 164,
    "単語": "dish",
    "品詞": "名詞",
    "訳語": "皿、料理",
    "レベル": "A"
  },
  {
    "番号": 165,
    "単語": "doctor",
    "品詞": "名詞",
    "訳語": "医者、博士",
    "レベル": "A"
  },
  {
    "番号": 166,
    "単語": "e-mail",
    "品詞": "名詞",
    "訳語": "電子メール",
    "レベル": "A"
  },
  {
    "番号": 167,
    "単語": "gym",
    "品詞": "名詞",
    "訳語": "体育館",
    "レベル": "A"
  },
  {
    "番号": 168,
    "単語": "sandwich",
    "品詞": "名詞",
    "訳語": "サンドイッチ",
    "レベル": "A"
  },
  {
    "番号": 169,
    "単語": "right",
    "品詞": "形容詞",
    "訳語": "右の、正しい",
    "レベル": "A"
  },
  {
    "番号": 170,
    "単語": "most",
    "品詞": "形容詞",
    "訳語": "大部分の、もっとも多くの",
    "レベル": "A"
  },
  {
    "番号": 171,
    "単語": "better",
    "品詞": "形容詞",
    "訳語": "よりよい",
    "レベル": "A"
  },
  {
    "番号": 172,
    "単語": "little",
    "品詞": "形容詞",
    "訳語": "少しの",
    "レベル": "A"
  },
  {
    "番号": 173,
    "単語": "delicious",
    "品詞": "形容詞",
    "訳語": "とてもおいしい",
    "レベル": "A"
  },
  {
    "番号": 174,
    "単語": "ready",
    "品詞": "形容詞",
    "訳語": "準備ができた",
    "レベル": "A"
  },
  {
    "番号": 175,
    "単語": "sick",
    "品詞": "形容詞",
    "訳語": "病気の、気分の悪い",
    "レベル": "A"
  },
  {
    "番号": 176,
    "単語": "expensive",
    "品詞": "形容詞",
    "訳語": "高価な",
    "レベル": "A"
  },
  {
    "番号": 177,
    "単語": "best",
    "品詞": "形容詞",
    "訳語": "もっともよい、もっとも上手な",
    "レベル": "A"
  },
  {
    "番号": 178,
    "単語": "difficult",
    "品詞": "形容詞",
    "訳語": "難しい",
    "レベル": "A"
  },
  {
    "番号": 179,
    "単語": "interesting",
    "品詞": "形容詞",
    "訳語": "おもしろい、興味深い",
    "レベル": "A"
  },
  {
    "番号": 180,
    "単語": "another",
    "品詞": "形容詞",
    "訳語": "もう一つの、別の",
    "レベル": "A"
  },
  {
    "番号": 181,
    "単語": "beautiful",
    "品詞": "形容詞",
    "訳語": "美しい",
    "レベル": "A"
  },
  {
    "番号": 182,
    "単語": "enough",
    "品詞": "形容詞",
    "訳語": "十分な、十分に",
    "レベル": "A"
  },
  {
    "番号": 183,
    "単語": "French",
    "品詞": "形容詞",
    "訳語": "フランスの、フランス語、フランス人の",
    "レベル": "A"
  },
  {
    "番号": 184,
    "単語": "fItalian",
    "品詞": "形容詞",
    "訳語": "イタリアの、イタリア人の、イタリア語",
    "レベル": "A"
  },
  {
    "番号": 185,
    "単語": "cheap",
    "品詞": "形容詞",
    "訳語": "安っぽい",
    "レベル": "A"
  },
  {
    "番号": 186,
    "単語": "Chinese",
    "品詞": "形容詞",
    "訳語": "中国の、中国人の、中国語",
    "レベル": "A"
  },
  {
    "番号": 187,
    "単語": "important",
    "品詞": "形容詞",
    "訳語": "重要な",
    "レベル": "A"
  },
  {
    "番号": 188,
    "単語": "ever",
    "品詞": "副詞",
    "訳語": "かつて、これまでに",
    "レベル": "A"
  },
  {
    "番号": 189,
    "単語": "outside",
    "品詞": "副詞",
    "訳語": "外に、〜の外部に、外側で",
    "レベル": "A"
  },
  {
    "番号": 190,
    "単語": "never",
    "品詞": "副詞",
    "訳語": "一度も～ない、決して～ない",
    "レベル": "A"
  },
  {
    "番号": 191,
    "単語": "again",
    "品詞": "副詞",
    "訳語": "再び、また",
    "レベル": "A"
  },
  {
    "番号": 192,
    "単語": "later",
    "品詞": "副詞",
    "訳語": "あとで",
    "レベル": "A"
  },
  {
    "番号": 193,
    "単語": "yet",
    "品詞": "副詞",
    "訳語": "まだ～ない、もう",
    "レベル": "A"
  },
  {
    "番号": 194,
    "単語": "each",
    "品詞": "副詞",
    "訳語": "ひとつにつき、それぞれの",
    "レベル": "A"
  },
  {
    "番号": 195,
    "単語": "once",
    "品詞": "副詞",
    "訳語": "一度、かつて",
    "レベル": "A"
  },
  {
    "番号": 196,
    "単語": "already",
    "品詞": "副詞",
    "訳語": "すでに、もう",
    "レベル": "A"
  },
  {
    "番号": 197,
    "単語": "until",
    "品詞": "前置詞",
    "訳語": "〜までずっと",
    "レベル": "A"
  },
  {
    "番号": 198,
    "単語": "something",
    "品詞": "代名詞",
    "訳語": "何か、あるもの",
    "レベル": "A"
  },
  {
    "番号": 199,
    "単語": "anything",
    "品詞": "代名詞",
    "訳語": "何でも、何も～ない",
    "レベル": "A"
  },
  {
    "番号": 200,
    "単語": "must",
    "品詞": "助動詞",
    "訳語": "～しなければならない",
    "レベル": "A"
  },
  {
    "番号": 201,
    "単語": "begin",
    "品詞": "動詞",
    "訳語": "〜を始める、始まる",
    "レベル": "A"
  },
  {
    "番号": 202,
    "単語": "catch",
    "品詞": "動詞",
    "訳語": "〜を捕まえる、～に間に合う",
    "レベル": "A"
  },
  {
    "番号": 203,
    "単語": "invite",
    "品詞": "動詞",
    "訳語": "招待する",
    "レベル": "A"
  },
  {
    "番号": 204,
    "単語": "feel",
    "品詞": "動詞",
    "訳語": "体調・気分を感じる",
    "レベル": "A"
  },
  {
    "番号": 205,
    "単語": "choose",
    "品詞": "動詞",
    "訳語": "〜を選ぶ",
    "レベル": "A"
  },
  {
    "番号": 206,
    "単語": "hike",
    "品詞": "動詞/名詞",
    "訳語": "ハイキングをする",
    "レベル": "A"
  },
  {
    "番号": 207,
    "単語": "keep",
    "品詞": "動詞",
    "訳語": "〜を保つ、～を持ち続ける、～を取っておく、動物などを飼う",
    "レベル": "A"
  },
  {
    "番号": 208,
    "単語": "worry",
    "品詞": "動詞",
    "訳語": "心配する、心配させる",
    "レベル": "A"
  },
  {
    "番号": 209,
    "単語": "camp",
    "品詞": "動詞",
    "訳語": "キャンプする",
    "レベル": "A"
  },
  {
    "番号": 210,
    "単語": "celebrate",
    "品詞": "動詞",
    "訳語": "～を祝う",
    "レベル": "A"
  },
  {
    "番号": 211,
    "単語": "guess",
    "品詞": "動詞",
    "訳語": "～だと思う、推測する",
    "レベル": "A"
  },
  {
    "番号": 212,
    "単語": "pass",
    "品詞": "動詞",
    "訳語": "～に合格する、～を手渡す",
    "レベル": "A"
  },
  {
    "番号": 213,
    "単語": "relax",
    "品詞": "動詞",
    "訳語": "くつろぐ",
    "レベル": "A"
  },
  {
    "番号": 214,
    "単語": "spend",
    "品詞": "動詞",
    "訳語": "（お金・時間を）費やす、過ごす",
    "レベル": "A"
  },
  {
    "番号": 215,
    "単語": "camera",
    "品詞": "名詞",
    "訳語": "カメラ",
    "レベル": "A"
  },
  {
    "番号": 216,
    "単語": "cousin",
    "品詞": "名詞",
    "訳語": "いとこ",
    "レベル": "A"
  },
  {
    "番号": 217,
    "単語": "grandmother",
    "品詞": "名詞",
    "訳語": "祖母",
    "レベル": "A"
  },
  {
    "番号": 218,
    "単語": "mountain",
    "品詞": "名詞",
    "訳語": "山",
    "レベル": "A"
  },
  {
    "番号": 219,
    "単語": "space",
    "品詞": "名詞",
    "訳語": "宇宙、空間",
    "レベル": "A"
  },
  {
    "番号": 220,
    "単語": "theater",
    "品詞": "名詞",
    "訳語": "劇場、映画館",
    "レベル": "A"
  },
  {
    "番号": 221,
    "単語": "wallet",
    "品詞": "名詞",
    "訳語": "財布",
    "レベル": "A"
  },
  {
    "番号": 222,
    "単語": "bookstore",
    "品詞": "名詞",
    "訳語": "書店",
    "レベル": "A"
  },
  {
    "番号": 223,
    "単語": "college",
    "品詞": "名詞",
    "訳語": "（単科）大学",
    "レベル": "A"
  },
  {
    "番号": 224,
    "単語": "color",
    "品詞": "名詞",
    "訳語": "色",
    "レベル": "A"
  },
  {
    "番号": 225,
    "単語": "dictionary",
    "品詞": "名詞",
    "訳語": "辞書",
    "レベル": "A"
  },
  {
    "番号": 226,
    "単語": "dollar",
    "品詞": "名詞",
    "訳語": "ドル",
    "レベル": "A"
  },
  {
    "番号": 227,
    "単語": "garden",
    "品詞": "名詞",
    "訳語": "庭",
    "レベル": "A"
  },
  {
    "番号": 228,
    "単語": "husband",
    "品詞": "名詞",
    "訳語": "夫",
    "レベル": "A"
  },
  {
    "番号": 229,
    "単語": "key",
    "品詞": "名詞",
    "訳語": "鍵",
    "レベル": "A"
  },
  {
    "番号": 230,
    "単語": "nurse",
    "品詞": "名詞",
    "訳語": "看護師",
    "レベル": "A"
  },
  {
    "番号": 231,
    "単語": "pool",
    "品詞": "名詞",
    "訳語": "プール",
    "レベル": "A"
  },
  {
    "番号": 232,
    "単語": "writer",
    "品詞": "名詞",
    "訳語": "作家、書く人",
    "レベル": "A"
  },
  {
    "番号": 233,
    "単語": "aunt",
    "品詞": "名詞",
    "訳語": "おば",
    "レベル": "A"
  },
  {
    "番号": 234,
    "単語": "classroom",
    "品詞": "名詞",
    "訳語": "教室",
    "レベル": "A"
  },
  {
    "番号": 235,
    "単語": "gift",
    "品詞": "名詞",
    "訳語": "贈り物",
    "レベル": "A"
  },
  {
    "番号": 236,
    "単語": "group",
    "品詞": "名詞",
    "訳語": "グループ",
    "レベル": "A"
  },
  {
    "番号": 237,
    "単語": "line",
    "品詞": "名詞",
    "訳語": "線、列",
    "レベル": "A"
  },
  {
    "番号": 238,
    "単語": "member",
    "品詞": "名詞",
    "訳語": "一員",
    "レベル": "A"
  },
  {
    "番号": 239,
    "単語": "passage",
    "品詞": "名詞",
    "訳語": "文章の一節",
    "レベル": "A"
  },
  {
    "番号": 240,
    "単語": "university",
    "品詞": "名詞",
    "訳語": "（総合）大学",
    "レベル": "A"
  },
  {
    "番号": 241,
    "単語": "wedding",
    "品詞": "名詞",
    "訳語": "結婚式",
    "レベル": "A"
  },
  {
    "番号": 242,
    "単語": "wife",
    "品詞": "名詞",
    "訳語": "妻",
    "レベル": "A"
  },
  {
    "番号": 243,
    "単語": "word",
    "品詞": "名詞",
    "訳語": "単語",
    "レベル": "A"
  },
  {
    "番号": 244,
    "単語": "airport",
    "品詞": "名詞",
    "訳語": "空港",
    "レベル": "A"
  },
  {
    "番号": 245,
    "単語": "apartment",
    "品詞": "名詞",
    "訳語": "アパート",
    "レベル": "A"
  },
  {
    "番号": 246,
    "単語": "building",
    "品詞": "名詞",
    "訳語": "建物",
    "レベル": "A"
  },
  {
    "番号": 247,
    "単語": "coat",
    "品詞": "名詞",
    "訳語": "（衣服の）コート",
    "レベル": "A"
  },
  {
    "番号": 248,
    "単語": "farm",
    "品詞": "名詞",
    "訳語": "農場",
    "レベル": "A"
  },
  {
    "番号": 249,
    "単語": "part",
    "品詞": "名詞",
    "訳語": "部分、役目",
    "レベル": "A"
  },
  {
    "番号": 250,
    "単語": "phone",
    "品詞": "名詞",
    "訳語": "電話",
    "レベル": "A"
  },
  {
    "番号": 251,
    "単語": "son",
    "品詞": "名詞",
    "訳語": "息子",
    "レベル": "A"
  },
  {
    "番号": 252,
    "単語": "textbook",
    "品詞": "名詞",
    "訳語": "教科書",
    "レベル": "A"
  },
  {
    "番号": 253,
    "単語": "tournament",
    "品詞": "名詞",
    "訳語": "トーナメント、選手権試合",
    "レベル": "A"
  },
  {
    "番号": 254,
    "単語": "vegetable",
    "品詞": "名詞",
    "訳語": "野菜",
    "レベル": "A"
  },
  {
    "番号": 255,
    "単語": "area",
    "品詞": "名詞",
    "訳語": "区域、地域",
    "レベル": "A"
  },
  {
    "番号": 256,
    "単語": "bakery",
    "品詞": "名詞",
    "訳語": "パン屋",
    "レベル": "A"
  },
  {
    "番号": 257,
    "単語": "business",
    "品詞": "名詞",
    "訳語": "商売、仕事",
    "レベル": "A"
  },
  {
    "番号": 258,
    "単語": "cafeteria",
    "品詞": "名詞",
    "訳語": "カフェテリア、セルフサービスの食堂",
    "レベル": "A"
  },
  {
    "番号": 259,
    "単語": "daughter",
    "品詞": "名詞",
    "訳語": "娘",
    "レベル": "A"
  },
  {
    "番号": 260,
    "単語": "health",
    "品詞": "名詞",
    "訳語": "健康",
    "レベル": "A"
  },
  {
    "番号": 261,
    "単語": "information",
    "品詞": "名詞",
    "訳語": "情報",
    "レベル": "A"
  },
  {
    "番号": 262,
    "単語": "internet",
    "品詞": "名詞",
    "訳語": "インターネット",
    "レベル": "A"
  },
  {
    "番号": 263,
    "単語": "lake",
    "品詞": "名詞",
    "訳語": "湖",
    "レベル": "A"
  },
  {
    "番号": 264,
    "単語": "pizza",
    "品詞": "名詞",
    "訳語": "ピザ",
    "レベル": "A"
  },
  {
    "番号": 265,
    "単語": "police",
    "品詞": "名詞",
    "訳語": "警察",
    "レベル": "A"
  },
  {
    "番号": 266,
    "単語": "reason",
    "品詞": "名詞",
    "訳語": "理由",
    "レベル": "A"
  },
  {
    "番号": 267,
    "単語": "sale",
    "品詞": "名詞",
    "訳語": "セール、特売",
    "レベル": "A"
  },
  {
    "番号": 268,
    "単語": "snack",
    "品詞": "名詞",
    "訳語": "おやつ、軽食",
    "レベル": "A"
  },
  {
    "番号": 269,
    "単語": "stadium",
    "品詞": "名詞",
    "訳語": "スタジアム",
    "レベル": "A"
  },
  {
    "番号": 270,
    "単語": "main",
    "品詞": "形容詞",
    "訳語": "主な、主要な",
    "レベル": "A"
  },
  {
    "番号": 271,
    "単語": "angry",
    "品詞": "形容詞",
    "訳語": "怒っている",
    "レベル": "A"
  },
  {
    "番号": 272,
    "単語": "own",
    "品詞": "形容詞/動詞",
    "訳語": "自分自身の、所有する",
    "レベル": "A"
  },
  {
    "番号": 273,
    "単語": "professional",
    "品詞": "形容詞",
    "訳語": "プロの、専門家の",
    "レベル": "A"
  },
  {
    "番号": 274,
    "単語": "sad",
    "品詞": "形容詞",
    "訳語": "悲しい",
    "レベル": "A"
  },
  {
    "番号": 275,
    "単語": "both",
    "品詞": "形容詞",
    "訳語": "両方の",
    "レベル": "A"
  },
  {
    "番号": 276,
    "単語": "dear",
    "品詞": "形容詞",
    "訳語": "親愛なる～さま",
    "レベル": "A"
  },
  {
    "番号": 277,
    "単語": "excited",
    "品詞": "形容詞",
    "訳語": "わくわくして",
    "レベル": "A"
  },
  {
    "番号": 278,
    "単語": "sunny",
    "品詞": "形容詞",
    "訳語": "晴れた",
    "レベル": "A"
  },
  {
    "番号": 279,
    "単語": "cute",
    "品詞": "形容詞",
    "訳語": "かわいい",
    "レベル": "A"
  },
  {
    "番号": 280,
    "単語": "fine",
    "品詞": "形容詞",
    "訳語": "結構な、晴れた、元気な",
    "レベル": "A"
  },
  {
    "番号": 281,
    "単語": "glad",
    "品詞": "形容詞",
    "訳語": "うれしい",
    "レベル": "A"
  },
  {
    "番号": 282,
    "単語": "healthy",
    "品詞": "形容詞",
    "訳語": "健康的な",
    "レベル": "A"
  },
  {
    "番号": 283,
    "単語": "heavy",
    "品詞": "形容詞",
    "訳語": "重い、激しい",
    "レベル": "A"
  },
  {
    "番号": 284,
    "単語": "same",
    "品詞": "形容詞",
    "訳語": "（the をつけて）同じ",
    "レベル": "A"
  },
  {
    "番号": 285,
    "単語": "Spanish",
    "品詞": "形容詞/名詞",
    "訳語": "スペインの、スペイン人の、スペイン語",
    "レベル": "A"
  },
  {
    "番号": 286,
    "単語": "tired",
    "品詞": "形容詞",
    "訳語": "疲れた",
    "レベル": "A"
  },
  {
    "番号": 287,
    "単語": "wrong",
    "品詞": "形容詞",
    "訳語": "間違った、調子が悪い",
    "レベル": "A"
  },
  {
    "番号": 288,
    "単語": "strong",
    "品詞": "形容詞",
    "訳語": "強い、丈夫な",
    "レベル": "A"
  },
  {
    "番号": 289,
    "単語": "exciting",
    "品詞": "形容詞",
    "訳語": "わくわくさせる",
    "レベル": "A"
  },
  {
    "番号": 290,
    "単語": "nervous",
    "品詞": "形容詞",
    "訳語": "緊張した",
    "レベル": "A"
  },
  {
    "番号": 291,
    "単語": "surprised",
    "品詞": "形容詞",
    "訳語": "驚いて、びっくりして",
    "レベル": "A"
  },
  {
    "番号": 292,
    "単語": "soon",
    "品詞": "副詞",
    "訳語": "すぐに、まもなく",
    "レベル": "A"
  },
  {
    "番号": 293,
    "単語": "twice",
    "品詞": "副詞",
    "訳語": "2回、2倍、2度",
    "レベル": "A"
  },
  {
    "番号": 294,
    "単語": "far",
    "品詞": "副詞/形容詞",
    "訳語": "遠くに、遠い",
    "レベル": "A"
  },
  {
    "番号": 295,
    "単語": "sometimes",
    "品詞": "副詞",
    "訳語": "時々",
    "レベル": "A"
  },
  {
    "番号": 296,
    "単語": "almost",
    "品詞": "副詞",
    "訳語": "ほとんど、もう少しで",
    "レベル": "A"
  },
  {
    "番号": 297,
    "単語": "instead",
    "品詞": "副詞",
    "訳語": "代わりに",
    "レベル": "A"
  },
  {
    "番号": 298,
    "単語": "maybe",
    "品詞": "副詞",
    "訳語": "たぶん",
    "レベル": "A"
  },
  {
    "番号": 299,
    "単語": "since",
    "品詞": "接続詞/前置詞",
    "訳語": "〜以来ずっと",
    "レベル": "A"
  },
  {
    "番号": 300,
    "単語": "while",
    "品詞": "接続詞",
    "訳語": "〜の間、〜するうちに",
    "レベル": "A"
  },
  {
    "番号": 301,
    "単語": "change",
    "品詞": "動詞",
    "訳語": "～を変える、変わる",
    "レベル": "B"
  },
  {
    "番号": 302,
    "単語": "hurry",
    "品詞": "動詞",
    "訳語": "急ぐ",
    "レベル": "B"
  },
  {
    "番号": 303,
    "単語": "hurt",
    "品詞": "動詞",
    "訳語": "～を傷つける、けがをさせる、痛む",
    "レベル": "B"
  },
  {
    "番号": 304,
    "単語": "introduce",
    "品詞": "動詞",
    "訳語": "〜を紹介する",
    "レベル": "B"
  },
  {
    "番号": 305,
    "単語": "sleep",
    "品詞": "動詞",
    "訳語": "眠る",
    "レベル": "B"
  },
  {
    "番号": 306,
    "単語": "snow",
    "品詞": "動詞",
    "訳語": "雪が降る",
    "レベル": "B"
  },
  {
    "番号": 307,
    "単語": "bake",
    "品詞": "動詞",
    "訳語": "（オーブンで）パンなどを焼く",
    "レベル": "B"
  },
  {
    "番号": 308,
    "単語": "believe",
    "品詞": "動詞",
    "訳語": "～を信じる",
    "レベル": "B"
  },
  {
    "番号": 309,
    "単語": "contact",
    "品詞": "動詞",
    "訳語": "～に連絡を取る",
    "レベル": "B"
  },
  {
    "番号": 310,
    "単語": "order",
    "品詞": "動詞",
    "訳語": "～を注文する",
    "レベル": "B"
  },
  {
    "番号": 311,
    "単語": "perform",
    "品詞": "動詞",
    "訳語": "～を上演する、～を演じる、～を演奏する",
    "レベル": "B"
  },
  {
    "番号": 312,
    "単語": "return",
    "品詞": "動詞",
    "訳語": "～を返す、戻る",
    "レベル": "B"
  },
  {
    "番号": 313,
    "単語": "save",
    "品詞": "動詞",
    "訳語": "～を救う、～を貯める、節約する",
    "レベル": "B"
  },
  {
    "番号": 314,
    "単語": "collect",
    "品詞": "動詞",
    "訳語": "～を集める",
    "レベル": "B"
  },
  {
    "番号": 315,
    "単語": "cost",
    "品詞": "動詞",
    "訳語": "費用がかかる",
    "レベル": "B"
  },
  {
    "番号": 316,
    "単語": "design",
    "品詞": "動詞",
    "訳語": "～をデザインする",
    "レベル": "B"
  },
  {
    "番号": 317,
    "単語": "enter",
    "品詞": "動詞",
    "訳語": "～に入る",
    "レベル": "B"
  },
  {
    "番号": 318,
    "単語": "throw",
    "品詞": "動詞",
    "訳語": "～を投げる",
    "レベル": "B"
  },
  {
    "番号": 319,
    "単語": "understand",
    "品詞": "動詞",
    "訳語": "～を理解する",
    "レベル": "B"
  },
  {
    "番号": 320,
    "単語": "badminton",
    "品詞": "名詞",
    "訳語": "バドミントン",
    "レベル": "B"
  },
  {
    "番号": 321,
    "単語": "bottle",
    "品詞": "名詞",
    "訳語": "ビン",
    "レベル": "B"
  },
  {
    "番号": 322,
    "単語": "cafe",
    "品詞": "名詞",
    "訳語": "喫茶店",
    "レベル": "B"
  },
  {
    "番号": 323,
    "単語": "cookie",
    "品詞": "名詞",
    "訳語": "クッキー",
    "レベル": "B"
  },
  {
    "番号": 324,
    "単語": "end",
    "品詞": "名詞",
    "訳語": "終わり",
    "レベル": "B"
  },
  {
    "番号": 325,
    "単語": "grade",
    "品詞": "名詞",
    "訳語": "成績、学年、等級",
    "レベル": "B"
  },
  {
    "番号": 326,
    "単語": "grandfather",
    "品詞": "名詞",
    "訳語": "祖父",
    "レベル": "B"
  },
  {
    "番号": 327,
    "単語": "hall",
    "品詞": "名詞",
    "訳語": "ホール、会館、集会所、役所",
    "レベル": "B"
  },
  {
    "番号": 328,
    "単語": "letter",
    "品詞": "名詞",
    "訳語": "手紙、文字",
    "レベル": "B"
  },
  {
    "番号": 329,
    "単語": "parade",
    "品詞": "名詞",
    "訳語": "パレード",
    "レベル": "B"
  },
  {
    "番号": 330,
    "単語": "performance",
    "品詞": "名詞",
    "訳語": "上演、演技、演奏",
    "レベル": "B"
  },
  {
    "番号": 331,
    "単語": "salad",
    "品詞": "名詞",
    "訳語": "サラダ",
    "レベル": "B"
  },
  {
    "番号": 332,
    "単語": "website",
    "品詞": "名詞",
    "訳語": "ウェブサイト",
    "レベル": "B"
  },
  {
    "番号": 333,
    "単語": "actor",
    "品詞": "名詞",
    "訳語": "俳優",
    "レベル": "B"
  },
  {
    "番号": 334,
    "単語": "animal",
    "品詞": "名詞",
    "訳語": "動物",
    "レベル": "B"
  },
  {
    "番号": 335,
    "単語": "astronaut",
    "品詞": "名詞",
    "訳語": "宇宙飛行士",
    "レベル": "B"
  },
  {
    "番号": 336,
    "単語": "chocolate",
    "品詞": "名詞",
    "訳語": "チョコレート",
    "レベル": "B"
  },
  {
    "番号": 337,
    "単語": "comedy",
    "品詞": "名詞",
    "訳語": "喜劇、コメディー",
    "レベル": "B"
  },
  {
    "番号": 338,
    "単語": "fruit",
    "品詞": "名詞",
    "訳語": "くだもの",
    "レベル": "B"
  },
  {
    "番号": 339,
    "単語": "future",
    "品詞": "名詞",
    "訳語": "未来、将来",
    "レベル": "B"
  },
  {
    "番号": 340,
    "単語": "goal",
    "品詞": "名詞",
    "訳語": "ゴールによる得点、ゴール、目標",
    "レベル": "B"
  },
  {
    "番号": 341,
    "単語": "hobby",
    "品詞": "名詞",
    "訳語": "趣味",
    "レベル": "B"
  },
  {
    "番号": 342,
    "単語": "license",
    "品詞": "名詞",
    "訳語": "免許証、免許",
    "レベル": "B"
  },
  {
    "番号": 343,
    "単語": "locker",
    "品詞": "名詞",
    "訳語": "ロッカー",
    "レベル": "B"
  },
  {
    "番号": 344,
    "単語": "machine",
    "品詞": "名詞",
    "訳語": "機械",
    "レベル": "B"
  },
  {
    "番号": 345,
    "単語": "magazine",
    "品詞": "名詞",
    "訳語": "雑誌",
    "レベル": "B"
  },
  {
    "番号": 346,
    "単語": "model",
    "品詞": "名詞",
    "訳語": "模型、型、モデル",
    "レベル": "B"
  },
  {
    "番号": 347,
    "単語": "notice",
    "品詞": "名詞",
    "訳語": "掲示、通知",
    "レベル": "B"
  },
  {
    "番号": 348,
    "単語": "paper",
    "品詞": "名詞",
    "訳語": "紙",
    "レベル": "B"
  },
  {
    "番号": 349,
    "単語": "question",
    "品詞": "名詞",
    "訳語": "質問",
    "レベル": "B"
  },
  {
    "番号": 350,
    "単語": "recipe",
    "品詞": "名詞",
    "訳語": "料理の作り方、調理法",
    "レベル": "B"
  },
  {
    "番号": 351,
    "単語": "rule",
    "品詞": "名詞",
    "訳語": "規則、ルール",
    "レベル": "B"
  },
  {
    "番号": 352,
    "単語": "season",
    "品詞": "名詞",
    "訳語": "季節、時期",
    "レベル": "B"
  },
  {
    "番号": 353,
    "単語": "sofa",
    "品詞": "名詞",
    "訳語": "ソファ",
    "レベル": "B"
  },
  {
    "番号": 354,
    "単語": "tour",
    "品詞": "名詞",
    "訳語": "（観光などの）旅行、ツアー",
    "レベル": "B"
  },
  {
    "番号": 355,
    "単語": "video",
    "品詞": "名詞",
    "訳語": "ビデオ、映像",
    "レベル": "B"
  },
  {
    "番号": 356,
    "単語": "winner",
    "品詞": "名詞",
    "訳語": "優勝者、勝利者",
    "レベル": "B"
  },
  {
    "番号": 357,
    "単語": "accident",
    "品詞": "名詞",
    "訳語": "事故",
    "レベル": "B"
  },
  {
    "番号": 358,
    "単語": "answer",
    "品詞": "名詞",
    "訳語": "答え、返事",
    "レベル": "B"
  },
  {
    "番号": 359,
    "単語": "bank",
    "品詞": "名詞",
    "訳語": "銀行",
    "レベル": "B"
  },
  {
    "番号": 360,
    "単語": "copy",
    "品詞": "名詞",
    "訳語": "コピー、複写",
    "レベル": "B"
  },
  {
    "番号": 361,
    "単語": "dentist",
    "品詞": "名詞",
    "訳語": "歯医者、歯科医",
    "レベル": "B"
  },
  {
    "番号": 362,
    "単語": "farmer",
    "品詞": "名詞",
    "訳語": "農場経営者",
    "レベル": "B"
  },
  {
    "番号": 363,
    "単語": "horse",
    "品詞": "名詞",
    "訳語": "馬",
    "レベル": "B"
  },
  {
    "番号": 364,
    "単語": "junior high school",
    "品詞": "名詞",
    "訳語": "中学校",
    "レベル": "B"
  },
  {
    "番号": 365,
    "単語": "kitchen",
    "品詞": "名詞",
    "訳語": "台所",
    "レベル": "B"
  },
  {
    "番号": 366,
    "単語": "race",
    "品詞": "名詞",
    "訳語": "レース、競争",
    "レベル": "B"
  },
  {
    "番号": 367,
    "単語": "sign",
    "品詞": "名詞",
    "訳語": "看板、掲示",
    "レベル": "B"
  },
  {
    "番号": 368,
    "単語": "snowboard",
    "品詞": "名詞",
    "訳語": "スノーボードの板",
    "レベル": "B"
  },
  {
    "番号": 369,
    "単語": "subject",
    "品詞": "名詞",
    "訳語": "（eメールなどの）件名",
    "レベル": "B"
  },
  {
    "番号": 370,
    "単語": "tiger",
    "品詞": "名詞",
    "訳語": "虎",
    "レベル": "B"
  },
  {
    "番号": 371,
    "単語": "toy",
    "品詞": "名詞",
    "訳語": "おもちゃ",
    "レベル": "B"
  },
  {
    "番号": 372,
    "単語": "visitor",
    "品詞": "名詞",
    "訳語": "訪問者、観光客",
    "レベル": "B"
  },
  {
    "番号": 373,
    "単語": "crowded",
    "品詞": "形容詞",
    "訳語": "混雑した",
    "レベル": "B"
  },
  {
    "番号": 374,
    "単語": "easy",
    "品詞": "形容詞",
    "訳語": "簡単な",
    "レベル": "B"
  },
  {
    "番号": 375,
    "単語": "fast",
    "品詞": "形容詞",
    "訳語": "速い",
    "レベル": "B"
  },
  {
    "番号": 376,
    "単語": "half",
    "品詞": "形容詞",
    "訳語": "半分の",
    "レベル": "B"
  },
  {
    "番号": 377,
    "単語": "hungry",
    "品詞": "形容詞",
    "訳語": "空腹の",
    "レベル": "B"
  },
  {
    "番号": 378,
    "単語": "afraid",
    "品詞": "形容詞",
    "訳語": "怖がって、恐れて",
    "レベル": "B"
  },
  {
    "番号": 379,
    "単語": "cloudy",
    "品詞": "形容詞",
    "訳語": "くもった",
    "レベル": "B"
  },
  {
    "番号": 380,
    "単語": "dirty",
    "品詞": "形容詞",
    "訳語": "汚れた、汚い",
    "レベル": "B"
  },
  {
    "番号": 381,
    "単語": "funny",
    "品詞": "形容詞",
    "訳語": "面白い、おかしい、こっけいな",
    "レベル": "B"
  },
  {
    "番号": 382,
    "単語": "poor",
    "品詞": "形容詞",
    "訳語": "貧しい、下手な",
    "レベル": "B"
  },
  {
    "番号": 383,
    "単語": "such",
    "品詞": "形容詞",
    "訳語": "そのような、このような",
    "レベル": "B"
  },
  {
    "番号": 384,
    "単語": "warm",
    "品詞": "形容詞",
    "訳語": "あたたかい",
    "レベル": "B"
  },
  {
    "番号": 385,
    "単語": "international",
    "品詞": "形容詞",
    "訳語": "国際的な",
    "レベル": "B"
  },
  {
    "番号": 386,
    "単語": "wet",
    "品詞": "形容詞",
    "訳語": "しめった、濡れた",
    "レベル": "B"
  },
  {
    "番号": 387,
    "単語": "alone",
    "品詞": "副詞",
    "訳語": "一人で",
    "レベル": "B"
  },
  {
    "番号": 388,
    "単語": "else",
    "品詞": "副詞",
    "訳語": "そのほかに",
    "レベル": "B"
  },
  {
    "番号": 389,
    "単語": "however",
    "品詞": "副詞",
    "訳語": "しかしながら",
    "レベル": "B"
  },
  {
    "番号": 390,
    "単語": "part-time",
    "品詞": "副詞",
    "訳語": "パートタイムで、非常勤で",
    "レベル": "B"
  },
  {
    "番号": 391,
    "単語": "abroad",
    "品詞": "副詞",
    "訳語": "海外で",
    "レベル": "B"
  },
  {
    "番号": 392,
    "単語": "finally",
    "品詞": "副詞",
    "訳語": "ついに、最後に",
    "レベル": "B"
  },
  {
    "番号": 393,
    "単語": "someday",
    "品詞": "副詞",
    "訳語": "いつか、そのうちに",
    "レベル": "B"
  },
  {
    "番号": 394,
    "単語": "either",
    "品詞": "副詞",
    "訳語": "～もまた･･･ない",
    "レベル": "B"
  },
  {
    "番号": 395,
    "単語": "even",
    "品詞": "副詞",
    "訳語": "～でさえ、さらに",
    "レベル": "B"
  },
  {
    "番号": 396,
    "単語": "beside",
    "品詞": "前置詞",
    "訳語": "～のそばに、～と並んで",
    "レベル": "B"
  },
  {
    "番号": 397,
    "単語": "through",
    "品詞": "前置詞",
    "訳語": "～を通り抜けて、～を通して",
    "レベル": "B"
  },
  {
    "番号": 398,
    "単語": "herself",
    "品詞": "代名詞",
    "訳語": "彼女自身を",
    "レベル": "B"
  },
  {
    "番号": 399,
    "単語": "anyone",
    "品詞": "代名詞",
    "訳語": "誰か、だれも～ない",
    "レベル": "B"
  },
  {
    "番号": 400,
    "単語": "myself",
    "品詞": "代名詞",
    "訳語": "私自身を",
    "レベル": "B"
  },
  {
    "番号": 401,
    "単語": "climb",
    "品詞": "動詞",
    "訳語": "～に登る",
    "レベル": "B"
  },
  {
    "番号": 402,
    "単語": "cover",
    "品詞": "動詞",
    "訳語": "～を覆う",
    "レベル": "B"
  },
  {
    "番号": 403,
    "単語": "die",
    "品詞": "動詞",
    "訳語": "死ぬ",
    "レベル": "B"
  },
  {
    "番号": 404,
    "単語": "follow",
    "品詞": "動詞",
    "訳語": "～に従う、ついていく",
    "レベル": "B"
  },
  {
    "番号": 405,
    "単語": "hit",
    "品詞": "動詞",
    "訳語": "～にぶつかる、～をぶつける、打つ",
    "レベル": "B"
  },
  {
    "番号": 406,
    "単語": "injure",
    "品詞": "動詞",
    "訳語": "～にけがをさせる、傷つける",
    "レベル": "B"
  },
  {
    "番号": 407,
    "単語": "lend",
    "品詞": "動詞",
    "訳語": "～を貸す",
    "レベル": "B"
  },
  {
    "番号": 408,
    "単語": "plant",
    "品詞": "動詞",
    "訳語": "～を植える",
    "レベル": "B"
  },
  {
    "番号": 409,
    "単語": "receive",
    "品詞": "動詞",
    "訳語": "～を受け取る",
    "レベル": "B"
  },
  {
    "番号": 410,
    "単語": "start",
    "品詞": "動詞",
    "訳語": "～を始める、始まる",
    "レベル": "B"
  },
  {
    "番号": 411,
    "単語": "steal",
    "品詞": "動詞",
    "訳語": "〜を盗む",
    "レベル": "B"
  },
  {
    "番号": 412,
    "単語": "taste",
    "品詞": "動詞",
    "訳語": "～の味がする",
    "レベル": "B"
  },
  {
    "番号": 413,
    "単語": "cry",
    "品詞": "動詞",
    "訳語": "泣く、叫ぶ",
    "レベル": "B"
  },
  {
    "番号": 414,
    "単語": "fall",
    "品詞": "動詞",
    "訳語": "落ちる",
    "レベル": "B"
  },
  {
    "番号": 415,
    "単語": "fix",
    "品詞": "動詞",
    "訳語": "〜を修理する",
    "レベル": "B"
  },
  {
    "番号": 416,
    "単語": "invent",
    "品詞": "動詞",
    "訳語": "～を発明する",
    "レベル": "B"
  },
  {
    "番号": 417,
    "単語": "kill",
    "品詞": "動詞",
    "訳語": "～を殺す",
    "レベル": "B"
  },
  {
    "番号": 418,
    "単語": "paint",
    "品詞": "動詞",
    "訳語": "～を絵具で描く、絵具を塗る",
    "レベル": "B"
  },
  {
    "番号": 419,
    "単語": "serve",
    "品詞": "動詞",
    "訳語": "（食事など）を出す、仕える",
    "レベル": "B"
  },
  {
    "番号": 420,
    "単語": "adult",
    "品詞": "名詞",
    "訳語": "大人",
    "レベル": "B"
  },
  {
    "番号": 421,
    "単語": "bathroom",
    "品詞": "名詞",
    "訳語": "浴室、トイレ",
    "レベル": "B"
  },
  {
    "番号": 422,
    "単語": "bicycle",
    "品詞": "名詞",
    "訳語": "自転車",
    "レベル": "B"
  },
  {
    "番号": 423,
    "単語": "captain",
    "品詞": "名詞",
    "訳語": "キャプテン、船長、機長",
    "レベル": "B"
  },
  {
    "番号": 424,
    "単語": "church",
    "品詞": "名詞",
    "訳語": "教会",
    "レベル": "B"
  },
  {
    "番号": 425,
    "単語": "coach",
    "品詞": "名詞",
    "訳語": "コーチ、監督、指導者",
    "レベル": "B"
  },
  {
    "番号": 426,
    "単語": "comic",
    "品詞": "名詞",
    "訳語": "漫画本",
    "レベル": "B"
  },
  {
    "番号": 427,
    "単語": "doughnut",
    "品詞": "名詞",
    "訳語": "ドーナツ",
    "レベル": "B"
  },
  {
    "番号": 428,
    "単語": "dress",
    "品詞": "名詞",
    "訳語": "ドレス",
    "レベル": "B"
  },
  {
    "番号": 429,
    "単語": "experience",
    "品詞": "名詞",
    "訳語": "経験",
    "レベル": "B"
  },
  {
    "番号": 430,
    "単語": "gate",
    "品詞": "名詞",
    "訳語": "門",
    "レベル": "B"
  },
  {
    "番号": 431,
    "単語": "horror",
    "品詞": "名詞",
    "訳語": "ホラー、恐怖",
    "レベル": "B"
  },
  {
    "番号": 432,
    "単語": "language",
    "品詞": "名詞",
    "訳語": "言語",
    "レベル": "B"
  },
  {
    "番号": 433,
    "単語": "nature",
    "品詞": "名詞",
    "訳語": "自然",
    "レベル": "B"
  },
  {
    "番号": 434,
    "単語": "noon",
    "品詞": "名詞",
    "訳語": "正午",
    "レベル": "B"
  },
  {
    "番号": 435,
    "単語": "owner",
    "品詞": "名詞",
    "訳語": "所有者",
    "レベル": "B"
  },
  {
    "番号": 436,
    "単語": "person",
    "品詞": "名詞",
    "訳語": "人",
    "レベル": "B"
  },
  {
    "番号": 437,
    "単語": "pond",
    "品詞": "名詞",
    "訳語": "池",
    "レベル": "B"
  },
  {
    "番号": 438,
    "単語": "price",
    "品詞": "名詞",
    "訳語": "価格、値段",
    "レベル": "B"
  },
  {
    "番号": 439,
    "単語": "schedule",
    "品詞": "名詞",
    "訳語": "予定",
    "レベル": "B"
  },
  {
    "番号": 440,
    "単語": "staff",
    "品詞": "名詞",
    "訳語": "職員、スタッフ",
    "レベル": "B"
  },
  {
    "番号": 441,
    "単語": "stage",
    "品詞": "名詞",
    "訳語": "舞台、ステージ",
    "レベル": "B"
  },
  {
    "番号": 442,
    "単語": "uniform",
    "品詞": "名詞",
    "訳語": "制服、ユニフォーム",
    "レベル": "B"
  },
  {
    "番号": 443,
    "単語": "volunteer",
    "品詞": "名詞",
    "訳語": "ボランティアをする人",
    "レベル": "B"
  },
  {
    "番号": 444,
    "単語": "award",
    "品詞": "名詞",
    "訳語": "賞、賞品",
    "レベル": "B"
  },
  {
    "番号": 445,
    "単語": "basket",
    "品詞": "名詞",
    "訳語": "かご",
    "レベル": "B"
  },
  {
    "番号": 446,
    "単語": "boss",
    "品詞": "名詞",
    "訳語": "上司",
    "レベル": "B"
  },
  {
    "番号": 447,
    "単語": "classmate",
    "品詞": "名詞",
    "訳語": "同級生、クラスメート",
    "レベル": "B"
  },
  {
    "番号": 448,
    "単語": "court",
    "品詞": "名詞",
    "訳語": "（テニスなどの）コート、法廷",
    "レベル": "B"
  },
  {
    "番号": 449,
    "単語": "dessert",
    "品詞": "名詞",
    "訳語": "デザート",
    "レベル": "B"
  },
  {
    "番号": 450,
    "単語": "dream",
    "品詞": "名詞",
    "訳語": "夢",
    "レベル": "B"
  },
  {
    "番号": 451,
    "単語": "environment",
    "品詞": "名詞",
    "訳語": "環境",
    "レベル": "B"
  },
  {
    "番号": 452,
    "単語": "exam",
    "品詞": "名詞",
    "訳語": "試験、テスト",
    "レベル": "B"
  },
  {
    "番号": 453,
    "単語": "fashion",
    "品詞": "名詞",
    "訳語": "ファッション、流行",
    "レベル": "B"
  },
  {
    "番号": 454,
    "単語": "field",
    "品詞": "名詞",
    "訳語": "野原、競技場、グラウンド",
    "レベル": "B"
  },
  {
    "番号": 455,
    "単語": "forest",
    "品詞": "名詞",
    "訳語": "森、森林",
    "レベル": "B"
  },
  {
    "番号": 456,
    "単語": "hole",
    "品詞": "名詞",
    "訳語": "穴",
    "レベル": "B"
  },
  {
    "番号": 457,
    "単語": "kilogram",
    "品詞": "名詞",
    "訳語": "キログラム",
    "レベル": "B"
  },
  {
    "番号": 458,
    "単語": "life",
    "品詞": "名詞",
    "訳語": "生涯、生活、命",
    "レベル": "B"
  },
  {
    "番号": 459,
    "単語": "meat",
    "品詞": "名詞",
    "訳語": "肉",
    "レベル": "B"
  },
  {
    "番号": 460,
    "単語": "meter",
    "品詞": "名詞",
    "訳語": "メートル",
    "レベル": "B"
  },
  {
    "番号": 461,
    "単語": "mind",
    "品詞": "名詞",
    "訳語": "心、精神",
    "レベル": "B"
  },
  {
    "番号": 462,
    "単語": "package",
    "品詞": "名詞",
    "訳語": "小包、小荷物",
    "レベル": "B"
  },
  {
    "番号": 463,
    "単語": "painting",
    "品詞": "名詞",
    "訳語": "絵画、絵を描くこと",
    "レベル": "B"
  },
  {
    "番号": 464,
    "単語": "platform",
    "品詞": "名詞",
    "訳語": "プラットフォーム、ホーム",
    "レベル": "B"
  },
  {
    "番号": 465,
    "単語": "project",
    "品詞": "名詞",
    "訳語": "研究課題、計画、事業",
    "レベル": "B"
  },
  {
    "番号": 466,
    "単語": "road",
    "品詞": "名詞",
    "訳語": "道路",
    "レベル": "B"
  },
  {
    "番号": 467,
    "単語": "rock",
    "品詞": "名詞",
    "訳語": "岩、ロック音楽",
    "レベル": "B"
  },
  {
    "番号": 468,
    "単語": "scientist",
    "品詞": "名詞",
    "訳語": "科学者",
    "レベル": "B"
  },
  {
    "番号": 469,
    "単語": "score",
    "品詞": "名詞",
    "訳語": "点数",
    "レベル": "B"
  },
  {
    "番号": 470,
    "単語": "shape",
    "品詞": "名詞",
    "訳語": "形",
    "レベル": "B"
  },
  {
    "番号": 471,
    "単語": "side",
    "品詞": "名詞",
    "訳語": "側、側面",
    "レベル": "B"
  },
  {
    "番号": 472,
    "単語": "sightseeing",
    "品詞": "名詞",
    "訳語": "観光",
    "レベル": "B"
  },
  {
    "番号": 473,
    "単語": "steak",
    "品詞": "名詞",
    "訳語": "ステーキ",
    "レベル": "B"
  },
  {
    "番号": 474,
    "単語": "stomachache",
    "品詞": "名詞",
    "訳語": "腹痛、胃痛",
    "レベル": "B"
  },
  {
    "番号": 475,
    "単語": "dark",
    "品詞": "形容詞",
    "訳語": "暗い",
    "レベル": "B"
  },
  {
    "番号": 476,
    "単語": "foreign",
    "品詞": "形容詞",
    "訳語": "外国の",
    "レベル": "B"
  },
  {
    "番号": 477,
    "単語": "full",
    "品詞": "形容詞",
    "訳語": "満員の、いっぱいの、満腹で",
    "レベル": "B"
  },
  {
    "番号": 478,
    "単語": "local",
    "品詞": "形容詞",
    "訳語": "その土地の、地元の",
    "レベル": "B"
  },
  {
    "番号": 479,
    "単語": "silent",
    "品詞": "形容詞",
    "訳語": "静かな、無言の",
    "レベル": "B"
  },
  {
    "番号": 480,
    "単語": "snowy",
    "品詞": "形容詞",
    "訳語": "雪の降る、雪の多い",
    "レベル": "B"
  },
  {
    "番号": 481,
    "単語": "true",
    "品詞": "形容詞",
    "訳語": "本当の、真実の",
    "レベル": "B"
  },
  {
    "番号": 482,
    "単語": "wonderful",
    "品詞": "形容詞",
    "訳語": "素晴らしい",
    "レベル": "B"
  },
  {
    "番号": 483,
    "単語": "bright",
    "品詞": "形容詞",
    "訳語": "光り輝く、明るい",
    "レベル": "B"
  },
  {
    "番号": 484,
    "単語": "careful",
    "品詞": "形容詞",
    "訳語": "注意深い、気を付ける",
    "レベル": "B"
  },
  {
    "番号": 485,
    "単語": "fresh",
    "品詞": "形容詞",
    "訳語": "新鮮な",
    "レベル": "B"
  },
  {
    "番号": 486,
    "単語": "million",
    "品詞": "形容詞",
    "訳語": "100万の",
    "レベル": "B"
  },
  {
    "番号": 487,
    "単語": "national",
    "品詞": "形容詞",
    "訳語": "国民の、国立の、全国的な",
    "レベル": "B"
  },
  {
    "番号": 488,
    "単語": "rich",
    "品詞": "形容詞",
    "訳語": "裕福な、豊かな、金持ちの",
    "レベル": "B"
  },
  {
    "番号": 489,
    "単語": "several",
    "品詞": "形容詞",
    "訳語": "数個の、いくつかの",
    "レベル": "B"
  },
  {
    "番号": 490,
    "単語": "thirsty",
    "品詞": "形容詞",
    "訳語": "のどが渇いた",
    "レベル": "B"
  },
  {
    "番号": 491,
    "単語": "below",
    "品詞": "副詞",
    "訳語": "下に",
    "レベル": "B"
  },
  {
    "番号": 492,
    "単語": "everywhere",
    "品詞": "副詞",
    "訳語": "あらゆる所に、どこでも、いたるところに",
    "レベル": "B"
  },
  {
    "番号": 493,
    "単語": "anytime",
    "品詞": "副詞",
    "訳語": "いつでも",
    "レベル": "B"
  },
  {
    "番号": 494,
    "単語": "anywhere",
    "品詞": "副詞",
    "訳語": "どこかへ、どこにも～ない",
    "レベル": "B"
  },
  {
    "番号": 495,
    "単語": "carefully",
    "品詞": "副詞",
    "訳語": "注意深く",
    "レベル": "B"
  },
  {
    "番号": 496,
    "単語": "inside",
    "品詞": "前置詞",
    "訳語": "〜のなかに",
    "レベル": "B"
  },
  {
    "番号": 497,
    "単語": "across",
    "品詞": "前置詞",
    "訳語": "～を渡って、～を横切って",
    "レベル": "B"
  },
  {
    "番号": 498,
    "単語": "behind",
    "品詞": "前置詞",
    "訳語": "〜の後ろに",
    "レベル": "B"
  },
  {
    "番号": 499,
    "単語": "without",
    "品詞": "前置詞",
    "訳語": "〜なしで、～しないで",
    "レベル": "B"
  },
  {
    "番号": 500,
    "単語": "someone",
    "品詞": "代名詞",
    "訳語": "誰か、ある人",
    "レベル": "B"
  },
  {
    "番号": 501,
    "単語": "burn",
    "品詞": "動詞",
    "訳語": "燃える、～を燃やす",
    "レベル": "B"
  },
  {
    "番号": 502,
    "単語": "cross",
    "品詞": "動詞",
    "訳語": "～を横断する、～を渡る",
    "レベル": "B"
  },
  {
    "番号": 503,
    "単語": "cut",
    "品詞": "動詞",
    "訳語": "～を切る",
    "レベル": "B"
  },
  {
    "番号": 504,
    "単語": "exchange",
    "品詞": "動詞",
    "訳語": "～を交換する",
    "レベル": "B"
  },
  {
    "番号": 505,
    "単語": "explain",
    "品詞": "動詞",
    "訳語": "～を説明する",
    "レベル": "B"
  },
  {
    "番号": 506,
    "単語": "imagine",
    "品詞": "動詞",
    "訳語": "～を想像する",
    "レベル": "B"
  },
  {
    "番号": 507,
    "単語": "mean",
    "品詞": "動詞",
    "訳語": "～を意味する",
    "レベル": "B"
  },
  {
    "番号": 508,
    "単語": "pull",
    "品詞": "動詞",
    "訳語": "～を引く",
    "レベル": "B"
  },
  {
    "番号": 509,
    "単語": "reach",
    "品詞": "動詞",
    "訳語": "～に着く、～に届く",
    "レベル": "B"
  },
  {
    "番号": 510,
    "単語": "shut",
    "品詞": "動詞",
    "訳語": "～を閉める、閉まる",
    "レベル": "B"
  },
  {
    "番号": 511,
    "単語": "smell",
    "品詞": "動詞",
    "訳語": "～のにおいがする、～のにおいをかぐ",
    "レベル": "B"
  },
  {
    "番号": 512,
    "単語": "action",
    "品詞": "名詞",
    "訳語": "行動、アクション",
    "レベル": "B"
  },
  {
    "番号": 513,
    "単語": "actress",
    "品詞": "名詞",
    "訳語": "女優",
    "レベル": "B"
  },
  {
    "番号": 514,
    "単語": "belt",
    "品詞": "名詞",
    "訳語": "ベルト",
    "レベル": "B"
  },
  {
    "番号": 515,
    "単語": "body",
    "品詞": "名詞",
    "訳語": "体",
    "レベル": "B"
  },
  {
    "番号": 516,
    "単語": "butter",
    "品詞": "名詞",
    "訳語": "バター",
    "レベル": "B"
  },
  {
    "番号": 517,
    "単語": "button",
    "品詞": "名詞",
    "訳語": "ボタン",
    "レベル": "B"
  },
  {
    "番号": 518,
    "単語": "capital",
    "品詞": "名詞",
    "訳語": "首都",
    "レベル": "B"
  },
  {
    "番号": 519,
    "単語": "center",
    "品詞": "名詞",
    "訳語": "中心、中央、センター",
    "レベル": "B"
  },
  {
    "番号": 520,
    "単語": "century",
    "品詞": "名詞",
    "訳語": "世紀",
    "レベル": "B"
  },
  {
    "番号": 521,
    "単語": "convenience store",
    "品詞": "名詞",
    "訳語": "コンビニ",
    "レベル": "B"
  },
  {
    "番号": 522,
    "単語": "culture",
    "品詞": "名詞",
    "訳語": "文化",
    "レベル": "B"
  },
  {
    "番号": 523,
    "単語": "customer",
    "品詞": "名詞",
    "訳語": "店の客",
    "レベル": "B"
  },
  {
    "番号": 524,
    "単語": "date",
    "品詞": "名詞",
    "訳語": "日付",
    "レベル": "B"
  },
  {
    "番号": 525,
    "単語": "elementary school",
    "品詞": "名詞",
    "訳語": "小学校",
    "レベル": "B"
  },
  {
    "番号": 526,
    "単語": "elevator",
    "品詞": "名詞",
    "訳語": "エレベーター",
    "レベル": "B"
  },
  {
    "番号": 527,
    "単語": "fact",
    "品詞": "名詞",
    "訳語": "事実",
    "レベル": "B"
  },
  {
    "番号": 528,
    "単語": "fever",
    "品詞": "名詞",
    "訳語": "熱",
    "レベル": "B"
  },
  {
    "番号": 529,
    "単語": "flight",
    "品詞": "名詞",
    "訳語": "飛行機の便、飛行",
    "レベル": "B"
  },
  {
    "番号": 530,
    "単語": "fridge",
    "品詞": "名詞",
    "訳語": "冷蔵庫",
    "レベル": "B"
  },
  {
    "番号": 531,
    "単語": "grandson",
    "品詞": "名詞",
    "訳語": "孫息子",
    "レベル": "B"
  },
  {
    "番号": 532,
    "単語": "horizon",
    "品詞": "名詞",
    "訳語": "地平線、水平線",
    "レベル": "B"
  },
  {
    "番号": 533,
    "単語": "interview",
    "品詞": "名詞",
    "訳語": "面接、面談",
    "レベル": "B"
  },
  {
    "番号": 534,
    "単語": "kid",
    "品詞": "名詞",
    "訳語": "こども",
    "レベル": "B"
  },
  {
    "番号": 535,
    "単語": "living room",
    "品詞": "名詞",
    "訳語": "居間",
    "レベル": "B"
  },
  {
    "番号": 536,
    "単語": "medal",
    "品詞": "名詞",
    "訳語": "メダル",
    "レベル": "B"
  },
  {
    "番号": 537,
    "単語": "memory",
    "品詞": "名詞",
    "訳語": "思い出、記憶力",
    "レベル": "B"
  },
  {
    "番号": 538,
    "単語": "middle",
    "品詞": "名詞",
    "訳語": "まんなか、中央",
    "レベル": "B"
  },
  {
    "番号": 539,
    "単語": "mirror",
    "品詞": "名詞",
    "訳語": "鏡",
    "レベル": "B"
  },
  {
    "番号": 540,
    "単語": "mushroom",
    "品詞": "名詞",
    "訳語": "きのこ",
    "レベル": "B"
  },
  {
    "番号": 541,
    "単語": "musician",
    "品詞": "名詞",
    "訳語": "音楽家、ミュージシャン",
    "レベル": "B"
  },
  {
    "番号": 542,
    "単語": "mystery",
    "品詞": "名詞",
    "訳語": "推理小説、ミステリー",
    "レベル": "B"
  },
  {
    "番号": 543,
    "単語": "panda",
    "品詞": "名詞",
    "訳語": "パンダ",
    "レベル": "B"
  },
  {
    "番号": 544,
    "単語": "power",
    "品詞": "名詞",
    "訳語": "力、動力",
    "レベル": "B"
  },
  {
    "番号": 545,
    "単語": "program",
    "品詞": "名詞",
    "訳語": "番組、計画",
    "レベル": "B"
  },
  {
    "番号": 546,
    "単語": "queen",
    "品詞": "名詞",
    "訳語": "女王、王妃",
    "レベル": "B"
  },
  {
    "番号": 547,
    "単語": "social studies",
    "品詞": "名詞",
    "訳語": "社会科",
    "レベル": "B"
  },
  {
    "番号": 548,
    "単語": "soldier",
    "品詞": "名詞",
    "訳語": "兵士、陸軍軍人",
    "レベル": "B"
  },
  {
    "番号": 549,
    "単語": "stew",
    "品詞": "名詞",
    "訳語": "シチュー",
    "レベル": "B"
  },
  {
    "番号": 550,
    "単語": "sugar",
    "品詞": "名詞",
    "訳語": "砂糖",
    "レベル": "B"
  },
  {
    "番号": 551,
    "単語": "suit",
    "品詞": "名詞",
    "訳語": "スーツ",
    "レベル": "B"
  },
  {
    "番号": 552,
    "単語": "swimsuit",
    "品詞": "名詞",
    "訳語": "（女性用のワンピース姿の）水着",
    "レベル": "B"
  },
  {
    "番号": 553,
    "単語": "symbol",
    "品詞": "名詞",
    "訳語": "象徴",
    "レベル": "B"
  },
  {
    "番号": 554,
    "単語": "tooth",
    "品詞": "名詞",
    "訳語": "歯",
    "レベル": "B"
  },
  {
    "番号": 555,
    "単語": "tourist",
    "品詞": "名詞",
    "訳語": "観光客、旅行者",
    "レベル": "B"
  },
  {
    "番号": 556,
    "単語": "type",
    "品詞": "名詞",
    "訳語": "型、タイプ",
    "レベル": "B"
  },
  {
    "番号": 557,
    "単語": "waiter",
    "品詞": "名詞",
    "訳語": "（男性の）ウェイター",
    "レベル": "B"
  },
  {
    "番号": 558,
    "単語": "war",
    "品詞": "名詞",
    "訳語": "戦争",
    "レベル": "B"
  },
  {
    "番号": 559,
    "単語": "aquarium",
    "品詞": "名詞",
    "訳語": "水族館",
    "レベル": "B"
  },
  {
    "番号": 560,
    "単語": "barbecue",
    "品詞": "名詞",
    "訳語": "バーベキュー",
    "レベル": "B"
  },
  {
    "番号": 561,
    "単語": "firework",
    "品詞": "名詞",
    "訳語": "花火 （複で）花火の打ち上げ",
    "レベル": "B"
  },
  {
    "番号": 562,
    "単語": "hill",
    "品詞": "名詞",
    "訳語": "丘、低い山",
    "レベル": "B"
  },
  {
    "番号": 563,
    "単語": "homestay",
    "品詞": "名詞",
    "訳語": "ホームステイ",
    "レベル": "B"
  },
  {
    "番号": 564,
    "単語": "hometown",
    "品詞": "名詞",
    "訳語": "生まれ故郷",
    "レベル": "B"
  },
  {
    "番号": 565,
    "単語": "musical",
    "品詞": "名詞",
    "訳語": "ミュージカル",
    "レベル": "B"
  },
  {
    "番号": 566,
    "単語": "president",
    "品詞": "名詞",
    "訳語": "大統領、会長、学長",
    "レベル": "B"
  },
  {
    "番号": 567,
    "単語": "rocket",
    "品詞": "名詞",
    "訳語": "ロケット",
    "レベル": "B"
  },
  {
    "番号": 568,
    "単語": "shrine",
    "品詞": "名詞",
    "訳語": "神社",
    "レベル": "B"
  },
  {
    "番号": 569,
    "単語": "statue",
    "品詞": "名詞",
    "訳語": "像、彫像",
    "レベル": "B"
  },
  {
    "番号": 570,
    "単語": "suitcase",
    "品詞": "名詞",
    "訳語": "スーツケース",
    "レベル": "B"
  },
  {
    "番号": 571,
    "単語": "sweater",
    "品詞": "名詞",
    "訳語": "セーター",
    "レベル": "B"
  },
  {
    "番号": 572,
    "単語": "tradition",
    "品詞": "名詞",
    "訳語": "伝統",
    "レベル": "B"
  },
  {
    "番号": 573,
    "単語": "worker",
    "品詞": "名詞",
    "訳語": "働く人、労働者",
    "レベル": "B"
  },
  {
    "番号": 574,
    "単語": "billion",
    "品詞": "形容詞",
    "訳語": "10億の",
    "レベル": "B"
  },
  {
    "番号": 575,
    "単語": "boring",
    "品詞": "形容詞",
    "訳語": "退屈な",
    "レベル": "B"
  },
  {
    "番号": 576,
    "単語": "central",
    "品詞": "形容詞",
    "訳語": "中央の、中心の",
    "レベル": "B"
  },
  {
    "番号": 577,
    "単語": "clear",
    "品詞": "形容詞",
    "訳語": "澄んだ、晴れた",
    "レベル": "B"
  },
  {
    "番号": 578,
    "単語": "clever",
    "品詞": "形容詞",
    "訳語": "賢い、利口な",
    "レベル": "B"
  },
  {
    "番号": 579,
    "単語": "deep",
    "品詞": "形容詞",
    "訳語": "深い",
    "レベル": "B"
  },
  {
    "番号": 580,
    "単語": "enjoyable",
    "品詞": "形容詞",
    "訳語": "楽しい、面白い",
    "レベル": "B"
  },
  {
    "番号": 581,
    "単語": "final",
    "品詞": "形容詞",
    "訳語": "最終の、最後の",
    "レベル": "B"
  },
  {
    "番号": 582,
    "単語": "loud",
    "品詞": "形容詞",
    "訳語": "音や声が大きい",
    "レベル": "B"
  },
  {
    "番号": 583,
    "単語": "lucky",
    "品詞": "形容詞",
    "訳語": "運のよい",
    "レベル": "B"
  },
  {
    "番号": 584,
    "単語": "narrow",
    "品詞": "形容詞",
    "訳語": "狭い",
    "レベル": "B"
  },
  {
    "番号": 585,
    "単語": "perfect",
    "品詞": "形容詞",
    "訳語": "完璧な、完全な",
    "レベル": "B"
  },
  {
    "番号": 586,
    "単語": "short",
    "品詞": "形容詞",
    "訳語": "短い、背の低い",
    "レベル": "B"
  },
  {
    "番号": 587,
    "単語": "simple",
    "品詞": "形容詞",
    "訳語": "簡単な、質素な",
    "レベル": "B"
  },
  {
    "番号": 588,
    "単語": "tight",
    "品詞": "形容詞",
    "訳語": "きつい",
    "レベル": "B"
  },
  {
    "番号": 589,
    "単語": "top",
    "品詞": "形容詞",
    "訳語": "一番上の",
    "レベル": "B"
  },
  {
    "番号": 590,
    "単語": "usual",
    "品詞": "形容詞",
    "訳語": "いつもの、ふつうの",
    "レベル": "B"
  },
  {
    "番号": 591,
    "単語": "whole",
    "品詞": "形容詞",
    "訳語": "全体の",
    "レベル": "B"
  },
  {
    "番号": 592,
    "単語": "actually",
    "品詞": "副詞",
    "訳語": "実は、実際に",
    "レベル": "B"
  },
  {
    "番号": 593,
    "単語": "anymore",
    "品詞": "副詞",
    "訳語": "今はもう～ない",
    "レベル": "B"
  },
  {
    "番号": 594,
    "単語": "anyway",
    "品詞": "副詞",
    "訳語": "とにかく、いずれにしても",
    "レベル": "B"
  },
  {
    "番号": 595,
    "単語": "luckily",
    "品詞": "副詞",
    "訳語": "幸運にも",
    "レベル": "B"
  },
  {
    "番号": 596,
    "単語": "pretty",
    "品詞": "副詞",
    "訳語": "かなり、とても",
    "レベル": "B"
  },
  {
    "番号": 597,
    "単語": "quickly",
    "品詞": "副詞",
    "訳語": "素早く、早く、すぐに",
    "レベル": "B"
  },
  {
    "番号": 598,
    "単語": "sometime",
    "品詞": "副詞",
    "訳語": "いつか、かつて",
    "レベル": "B"
  },
  {
    "番号": 599,
    "単語": "between",
    "品詞": "前置詞",
    "訳語": "二つの間に",
    "レベル": "B"
  },
  {
    "番号": 600,
    "単語": "as",
    "品詞": "前置詞",
    "訳語": "～として",
    "レベル": "B"
  },
  {
    "番号": 601,
    "単語": "attend",
    "品詞": "動詞",
    "訳語": "〜に出席する、通う",
    "レベル": "C"
  },
  {
    "番号": 602,
    "単語": "boil",
    "品詞": "動詞",
    "訳語": "〜を沸騰させる、茹でる",
    "レベル": "C"
  },
  {
    "番号": 603,
    "単語": "cancel",
    "品詞": "動詞",
    "訳語": "予約・注文などを取り消す、中止する",
    "レベル": "C"
  },
  {
    "番号": 604,
    "単語": "continue",
    "品詞": "動詞",
    "訳語": "～を続ける、続く",
    "レベル": "C"
  },
  {
    "番号": 605,
    "単語": "laugh",
    "品詞": "動詞",
    "訳語": "笑う",
    "レベル": "C"
  },
  {
    "番号": 606,
    "単語": "prepare",
    "品詞": "動詞",
    "訳語": "準備する",
    "レベル": "C"
  },
  {
    "番号": 607,
    "単語": "protect",
    "品詞": "動詞",
    "訳語": "〜を保護する",
    "レベル": "C"
  },
  {
    "番号": 608,
    "単語": "push",
    "品詞": "動詞",
    "訳語": "〜を押す",
    "レベル": "C"
  },
  {
    "番号": 609,
    "単語": "recycle",
    "品詞": "動詞",
    "訳語": "～を再生利用する、リサイクルする",
    "レベル": "C"
  },
  {
    "番号": 610,
    "単語": "rest",
    "品詞": "動詞",
    "訳語": "休む、休憩する",
    "レベル": "C"
  },
  {
    "番号": 611,
    "単語": "share",
    "品詞": "動詞",
    "訳語": "〜を共有する、～を分け合う",
    "レベル": "C"
  },
  {
    "番号": 612,
    "単語": "smile",
    "品詞": "動詞",
    "訳語": "ほほえむ",
    "レベル": "C"
  },
  {
    "番号": 613,
    "単語": "touch",
    "品詞": "動詞",
    "訳語": "〜に触れる、～に触る",
    "レベル": "C"
  },
  {
    "番号": 614,
    "単語": "activity",
    "品詞": "名詞",
    "訳語": "活動",
    "レベル": "C"
  },
  {
    "番号": 615,
    "単語": "address",
    "品詞": "名詞",
    "訳語": "住所、メールのアドレス",
    "レベル": "C"
  },
  {
    "番号": 616,
    "単語": "advice",
    "品詞": "名詞",
    "訳語": "助言、アドバイス",
    "レベル": "C"
  },
  {
    "番号": 617,
    "単語": "air",
    "品詞": "名詞",
    "訳語": "空気",
    "レベル": "C"
  },
  {
    "番号": 618,
    "単語": "alarm",
    "品詞": "名詞",
    "訳語": "目覚まし時計、警報機",
    "レベル": "C"
  },
  {
    "番号": 619,
    "単語": "block",
    "品詞": "名詞",
    "訳語": "町の一区画",
    "レベル": "C"
  },
  {
    "番号": 620,
    "単語": "bridge",
    "品詞": "名詞",
    "訳語": "橋",
    "レベル": "C"
  },
  {
    "番号": 621,
    "単語": "ceremony",
    "品詞": "名詞",
    "訳語": "式、儀式",
    "レベル": "C"
  },
  {
    "番号": 622,
    "単語": "chance",
    "品詞": "名詞",
    "訳語": "機会",
    "レベル": "C"
  },
  {
    "番号": 623,
    "単語": "chef",
    "品詞": "名詞",
    "訳語": "シェフ、料理長",
    "レベル": "C"
  },
  {
    "番号": 624,
    "単語": "costume",
    "品詞": "名詞",
    "訳語": "衣装",
    "レベル": "C"
  },
  {
    "番号": 625,
    "単語": "difference",
    "品詞": "名詞",
    "訳語": "違い",
    "レベル": "C"
  },
  {
    "番号": 626,
    "単語": "energy",
    "品詞": "名詞",
    "訳語": "エネルギー",
    "レベル": "C"
  },
  {
    "番号": 627,
    "単語": "entrance",
    "品詞": "名詞",
    "訳語": "入口",
    "レベル": "C"
  },
  {
    "番号": 628,
    "単語": "figure",
    "品詞": "名詞",
    "訳語": "図、図表、人物、数字",
    "レベル": "C"
  },
  {
    "番号": 629,
    "単語": "flag",
    "品詞": "名詞",
    "訳語": "旗",
    "レベル": "C"
  },
  {
    "番号": 630,
    "単語": "garbage",
    "品詞": "名詞",
    "訳語": "ごみ",
    "レベル": "C"
  },
  {
    "番号": 631,
    "単語": "glove",
    "品詞": "名詞",
    "訳語": "手袋、野球などのグローブ",
    "レベル": "C"
  },
  {
    "番号": 632,
    "単語": "guide",
    "品詞": "名詞",
    "訳語": "ガイド、案内人",
    "レベル": "C"
  },
  {
    "番号": 633,
    "単語": "hamburger",
    "品詞": "名詞",
    "訳語": "ハンバーガー",
    "レベル": "C"
  },
  {
    "番号": 634,
    "単語": "headache",
    "品詞": "名詞",
    "訳語": "頭痛",
    "レベル": "C"
  },
  {
    "番号": 635,
    "単語": "height",
    "品詞": "名詞",
    "訳語": "高さ、身長",
    "レベル": "C"
  },
  {
    "番号": 636,
    "単語": "hero",
    "品詞": "名詞",
    "訳語": "英雄、男性の主人公",
    "レベル": "C"
  },
  {
    "番号": 637,
    "単語": "island",
    "品詞": "名詞",
    "訳語": "島",
    "レベル": "C"
  },
  {
    "番号": 638,
    "単語": "jazz",
    "品詞": "名詞",
    "訳語": "ジャズ",
    "レベル": "C"
  },
  {
    "番号": 639,
    "単語": "jeans",
    "品詞": "名詞",
    "訳語": "ジーンズ",
    "レベル": "C"
  },
  {
    "番号": 640,
    "単語": "judge",
    "品詞": "名詞",
    "訳語": "審査員、審判員",
    "レベル": "C"
  },
  {
    "番号": 641,
    "単語": "juice",
    "品詞": "名詞",
    "訳語": "ジュース",
    "レベル": "C"
  },
  {
    "番号": 642,
    "単語": "leaf",
    "品詞": "名詞",
    "訳語": "葉",
    "レベル": "C"
  },
  {
    "番号": 643,
    "単語": "manager",
    "品詞": "名詞",
    "訳語": "支配人、管理者、経営者",
    "レベル": "C"
  },
  {
    "番号": 644,
    "単語": "meal",
    "品詞": "名詞",
    "訳語": "食事",
    "レベル": "C"
  },
  {
    "番号": 645,
    "単語": "message",
    "品詞": "名詞",
    "訳語": "伝言、メッセージ",
    "レベル": "C"
  },
  {
    "番号": 646,
    "単語": "midnight",
    "品詞": "名詞",
    "訳語": "夜中の12時、真夜中",
    "レベル": "C"
  },
  {
    "番号": 647,
    "単語": "novel",
    "品詞": "名詞",
    "訳語": "長編の小説",
    "レベル": "C"
  },
  {
    "番号": 648,
    "単語": "oil",
    "品詞": "名詞",
    "訳語": "油",
    "レベル": "C"
  },
  {
    "番号": 649,
    "単語": "oven",
    "品詞": "名詞",
    "訳語": "オーブン",
    "レベル": "C"
  },
  {
    "番号": 650,
    "単語": "page",
    "品詞": "名詞",
    "訳語": "ページ",
    "レベル": "C"
  },
  {
    "番号": 651,
    "単語": "pancake",
    "品詞": "名詞",
    "訳語": "パンケーキ",
    "レベル": "C"
  },
  {
    "番号": 652,
    "単語": "passenger",
    "品詞": "名詞",
    "訳語": "乗客",
    "レベル": "C"
  },
  {
    "番号": 653,
    "単語": "peace",
    "品詞": "名詞",
    "訳語": "平和",
    "レベル": "C"
  },
  {
    "番号": 654,
    "単語": "planet",
    "品詞": "名詞",
    "訳語": "惑星",
    "レベル": "C"
  },
  {
    "番号": 655,
    "単語": "pocket",
    "品詞": "名詞",
    "訳語": "ポケット",
    "レベル": "C"
  },
  {
    "番号": 656,
    "単語": "point",
    "品詞": "名詞",
    "訳語": "得点、地点、要点",
    "レベル": "C"
  },
  {
    "番号": 657,
    "単語": "promise",
    "品詞": "名詞",
    "訳語": "約束",
    "レベル": "C"
  },
  {
    "番号": 658,
    "単語": "radio",
    "品詞": "名詞",
    "訳語": "ラジオ",
    "レベル": "C"
  },
  {
    "番号": 659,
    "単語": "scarf",
    "品詞": "名詞",
    "訳語": "スカーフ、マフラー",
    "レベル": "C"
  },
  {
    "番号": 660,
    "単語": "scene",
    "品詞": "名詞",
    "訳語": "場面",
    "レベル": "C"
  },
  {
    "番号": 661,
    "単語": "sight",
    "品詞": "名詞",
    "訳語": "視力、視界、光景",
    "レベル": "C"
  },
  {
    "番号": 662,
    "単語": "stomach",
    "品詞": "名詞",
    "訳語": "胃、腹部",
    "レベル": "C"
  },
  {
    "番号": 663,
    "単語": "storm",
    "品詞": "名詞",
    "訳語": "嵐、暴風雨",
    "レベル": "C"
  },
  {
    "番号": 664,
    "単語": "support",
    "品詞": "名詞",
    "訳語": "支援、支持",
    "レベル": "C"
  },
  {
    "番号": 665,
    "単語": "system",
    "品詞": "名詞",
    "訳語": "制度、系統、体系",
    "レベル": "C"
  },
  {
    "番号": 666,
    "単語": "telephone",
    "品詞": "名詞",
    "訳語": "電話",
    "レベル": "C"
  },
  {
    "番号": 667,
    "単語": "tie",
    "品詞": "名詞",
    "訳語": "ネクタイ",
    "レベル": "C"
  },
  {
    "番号": 668,
    "単語": "trouble",
    "品詞": "名詞",
    "訳語": "面倒な状況、悩み事",
    "レベル": "C"
  },
  {
    "番号": 669,
    "単語": "voice",
    "品詞": "名詞",
    "訳語": "声",
    "レベル": "C"
  },
  {
    "番号": 670,
    "単語": "wish",
    "品詞": "名詞",
    "訳語": "（複で）（幸福・健康などを)祈願する言葉、願い、望み",
    "レベル": "C"
  },
  {
    "番号": 671,
    "単語": "broken",
    "品詞": "形容詞",
    "訳語": "折れた、壊れた",
    "レベル": "C"
  },
  {
    "番号": 672,
    "単語": "comfortable",
    "品詞": "形容詞",
    "訳語": "快適な、心地よい",
    "レベル": "C"
  },
  {
    "番号": 673,
    "単語": "dangerous",
    "品詞": "形容詞",
    "訳語": "危険な",
    "レベル": "C"
  },
  {
    "番号": 674,
    "単語": "excellent",
    "品詞": "形容詞",
    "訳語": "優れた、優秀な",
    "レベル": "C"
  },
  {
    "番号": 675,
    "単語": "familiar",
    "品詞": "形容詞",
    "訳語": "見慣れた、よく知られた",
    "レベル": "C"
  },
  {
    "番号": 676,
    "単語": "helpful",
    "品詞": "形容詞",
    "訳語": "役立つ",
    "レベル": "C"
  },
  {
    "番号": 677,
    "単語": "noisy",
    "品詞": "形容詞",
    "訳語": "騒がしい",
    "レベル": "C"
  },
  {
    "番号": 678,
    "単語": "Olympic",
    "品詞": "形容詞",
    "訳語": "オリンピックの",
    "レベル": "C"
  },
  {
    "番号": 679,
    "単語": "peaceful",
    "品詞": "形容詞",
    "訳語": "穏やかな、平和な",
    "レベル": "C"
  },
  {
    "番号": 680,
    "単語": "powerful",
    "品詞": "形容詞",
    "訳語": "強力な",
    "レベル": "C"
  },
  {
    "番号": 681,
    "単語": "public",
    "品詞": "形容詞",
    "訳語": "公共の、公の",
    "レベル": "C"
  },
  {
    "番号": 682,
    "単語": "quiet",
    "品詞": "形容詞",
    "訳語": "静かな",
    "レベル": "C"
  },
  {
    "番号": 683,
    "単語": "round",
    "品詞": "形容詞",
    "訳語": "丸い",
    "レベル": "C"
  },
  {
    "番号": 684,
    "単語": "scared",
    "品詞": "形容詞",
    "訳語": "おびえた、怖がった",
    "レベル": "C"
  },
  {
    "番号": 685,
    "単語": "shy",
    "品詞": "形容詞",
    "訳語": "恥ずかしがりの、内気な",
    "レベル": "C"
  },
  {
    "番号": 686,
    "単語": "smart",
    "品詞": "形容詞",
    "訳語": "利口な",
    "レベル": "C"
  },
  {
    "番号": 687,
    "単語": "thick",
    "品詞": "形容詞",
    "訳語": "厚い、濃い",
    "レベル": "C"
  },
  {
    "番号": 688,
    "単語": "traditional",
    "品詞": "形容詞",
    "訳語": "伝統的な",
    "レベル": "C"
  },
  {
    "番号": 689,
    "単語": "upset",
    "品詞": "形容詞",
    "訳語": "動揺した",
    "レベル": "C"
  },
  {
    "番号": 690,
    "単語": "wide",
    "品詞": "形容詞",
    "訳語": "幅の広い",
    "レベル": "C"
  },
  {
    "番号": 691,
    "単語": "cheaply",
    "品詞": "副詞",
    "訳語": "安く",
    "レベル": "C"
  },
  {
    "番号": 692,
    "単語": "easily",
    "品詞": "副詞",
    "訳語": "簡単に、容易に",
    "レベル": "C"
  },
  {
    "番号": 693,
    "単語": "safely",
    "品詞": "副詞",
    "訳語": "安全に、無事に",
    "レベル": "C"
  },
  {
    "番号": 694,
    "単語": "sincerely",
    "品詞": "副詞",
    "訳語": "敬具",
    "レベル": "C"
  },
  {
    "番号": 695,
    "単語": "softly",
    "品詞": "副詞",
    "訳語": "やさしく、柔らかに、穏やかに",
    "レベル": "C"
  },
  {
    "番号": 696,
    "単語": "straight",
    "品詞": "副詞",
    "訳語": "まっすぐに",
    "レベル": "C"
  },
  {
    "番号": 697,
    "単語": "upstairs",
    "品詞": "副詞",
    "訳語": "上の階へ",
    "レベル": "C"
  },
  {
    "番号": 698,
    "単語": "above",
    "品詞": "前置詞",
    "訳語": "～の上に",
    "レベル": "C"
  },
  {
    "番号": 699,
    "単語": "against",
    "品詞": "前置詞",
    "訳語": "～に対抗して、～に反対して",
    "レベル": "C"
  },
  {
    "番号": 700,
    "単語": "among",
    "品詞": "前置詞",
    "訳語": "～の中で、～の間で",
    "レベル": "C"
  },
  {
    "番号": 701,
    "単語": "count",
    "品詞": "動詞",
    "訳語": "〜を数える",
    "レベル": "C"
  },
  {
    "番号": 702,
    "単語": "kick",
    "品詞": "動詞",
    "訳語": "～を蹴る",
    "レベル": "C"
  },
  {
    "番号": 703,
    "単語": "set",
    "品詞": "動詞",
    "訳語": "～を用意する、～を整える、～をセットする",
    "レベル": "C"
  },
  {
    "番号": 704,
    "単語": "spread",
    "品詞": "動詞",
    "訳語": "〜を広げる、広がる",
    "レベル": "C"
  },
  {
    "番号": 705,
    "単語": "surf",
    "品詞": "動詞",
    "訳語": "サーフィンをする、ホームページなどを見tてまわる",
    "レベル": "C"
  },
  {
    "番号": 706,
    "単語": "raise",
    "品詞": "動詞",
    "訳語": "～を上げる、～を育てる",
    "レベル": "C"
  },
  {
    "番号": 707,
    "単語": "add",
    "品詞": "動詞",
    "訳語": "～を加える",
    "レベル": "C"
  },
  {
    "番号": 708,
    "単語": "appear",
    "品詞": "動詞",
    "訳語": "現れる",
    "レベル": "C"
  },
  {
    "番号": 709,
    "単語": "attack",
    "品詞": "動詞",
    "訳語": "～を攻撃する",
    "レベル": "C"
  },
  {
    "番号": 710,
    "単語": "control",
    "品詞": "動詞",
    "訳語": "～を操作する、～を支配する、～を管理する",
    "レベル": "C"
  },
  {
    "番号": 711,
    "単語": "deliver",
    "品詞": "動詞",
    "訳語": "〜を配達する",
    "レベル": "C"
  },
  {
    "番号": 712,
    "単語": "expect",
    "品詞": "動詞",
    "訳語": "～を待ち受ける、～を予期する",
    "レベル": "C"
  },
  {
    "番号": 713,
    "単語": "express",
    "品詞": "動詞",
    "訳語": "〜を表現する",
    "レベル": "C"
  },
  {
    "番号": 714,
    "単語": "fight",
    "品詞": "動詞",
    "訳語": "～と戦う、けんかする",
    "レベル": "C"
  },
  {
    "番号": 715,
    "単語": "fit",
    "品詞": "動詞",
    "訳語": "～にぴったり合う",
    "レベル": "C"
  },
  {
    "番号": 716,
    "単語": "hang",
    "品詞": "動詞",
    "訳語": "〜を掛ける",
    "レベル": "C"
  },
  {
    "番号": 717,
    "単語": "jog",
    "品詞": "動詞",
    "訳語": "ジョギングする",
    "レベル": "C"
  },
  {
    "番号": 718,
    "単語": "knock",
    "品詞": "動詞",
    "訳語": "ノックする",
    "レベル": "C"
  },
  {
    "番号": 719,
    "単語": "mix",
    "品詞": "動詞",
    "訳語": "～を混ぜる、混ざる",
    "レベル": "C"
  },
  {
    "番号": 720,
    "単語": "oversleep",
    "品詞": "動詞",
    "訳語": "寝過ごす",
    "レベル": "C"
  },
  {
    "番号": 721,
    "単語": "record",
    "品詞": "動詞",
    "訳語": "～を録画する、～を記録する",
    "レベル": "C"
  },
  {
    "番号": 722,
    "単語": "repeat",
    "品詞": "動詞",
    "訳語": "～を繰り返して言う",
    "レベル": "C"
  },
  {
    "番号": 723,
    "単語": "seem",
    "品詞": "動詞",
    "訳語": "〜ように見える、～のように思われる",
    "レベル": "C"
  },
  {
    "番号": 724,
    "単語": "shake",
    "品詞": "動詞",
    "訳語": "～を振る、揺れる",
    "レベル": "C"
  },
  {
    "番号": 725,
    "単語": "shock",
    "品詞": "動詞",
    "訳語": "〜にショックを与える",
    "レベル": "C"
  },
  {
    "番号": 726,
    "単語": "shout",
    "品詞": "動詞",
    "訳語": "怒鳴る、叫ぶ",
    "レベル": "C"
  },
  {
    "番号": 727,
    "単語": "spell",
    "品詞": "動詞",
    "訳語": "～をつづる",
    "レベル": "C"
  },
  {
    "番号": 728,
    "単語": "waste",
    "品詞": "動詞",
    "訳語": "～を無駄に使う",
    "レベル": "C"
  },
  {
    "番号": 729,
    "単語": "wonder",
    "品詞": "動詞",
    "訳語": "〜かなと思う",
    "レベル": "C"
  },
  {
    "番号": 730,
    "単語": "ballet",
    "品詞": "名詞",
    "訳語": "バレエ",
    "レベル": "C"
  },
  {
    "番号": 731,
    "単語": "bit",
    "品詞": "名詞",
    "訳語": "（ a bit で）少し",
    "レベル": "C"
  },
  {
    "番号": 732,
    "単語": "carnival",
    "品詞": "名詞",
    "訳語": "カーニバル、お祭り騒ぎ",
    "レベル": "C"
  },
  {
    "番号": 733,
    "単語": "carpenter",
    "品詞": "名詞",
    "訳語": "大工",
    "レベル": "C"
  },
  {
    "番号": 734,
    "単語": "cracker",
    "品詞": "名詞",
    "訳語": "クラッカー",
    "レベル": "C"
  },
  {
    "番号": 735,
    "単語": "drawing",
    "品詞": "名詞",
    "訳語": "線画、スケッチ、図面",
    "レベル": "C"
  },
  {
    "番号": 736,
    "単語": "engine",
    "品詞": "名詞",
    "訳語": "エンジン",
    "レベル": "C"
  },
  {
    "番号": 737,
    "単語": "exit",
    "品詞": "名詞",
    "訳語": "出口",
    "レベル": "C"
  },
  {
    "番号": 738,
    "単語": "fan",
    "品詞": "名詞",
    "訳語": "ファン",
    "レベル": "C"
  },
  {
    "番号": 739,
    "単語": "flour",
    "品詞": "名詞",
    "訳語": "小麦粉",
    "レベル": "C"
  },
  {
    "番号": 740,
    "単語": "gentleman",
    "品詞": "名詞",
    "訳語": "ジェントルマン、男の方",
    "レベル": "C"
  },
  {
    "番号": 741,
    "単語": "ghost",
    "品詞": "名詞",
    "訳語": "幽霊",
    "レベル": "C"
  },
  {
    "番号": 742,
    "単語": "guest",
    "品詞": "名詞",
    "訳語": "招かれた客",
    "レベル": "C"
  },
  {
    "番号": 743,
    "単語": "guy",
    "品詞": "名詞",
    "訳語": "（複で）みんな、奴、男",
    "レベル": "C"
  },
  {
    "番号": 744,
    "単語": "habit",
    "品詞": "名詞",
    "訳語": "習慣",
    "レベル": "C"
  },
  {
    "番号": 745,
    "単語": "handle",
    "品詞": "名詞",
    "訳語": "取手、柄",
    "レベル": "C"
  },
  {
    "番号": 746,
    "単語": "heart",
    "品詞": "名詞",
    "訳語": "心臓、心",
    "レベル": "C"
  },
  {
    "番号": 747,
    "単語": "hockey",
    "品詞": "名詞",
    "訳語": "ホッケー",
    "レベル": "C"
  },
  {
    "番号": 748,
    "単語": "joke",
    "品詞": "名詞",
    "訳語": "冗談",
    "レベル": "C"
  },
  {
    "番号": 749,
    "単語": "kilometer",
    "品詞": "名詞",
    "訳語": "キロメートル",
    "レベル": "C"
  },
  {
    "番号": 750,
    "単語": "knee",
    "品詞": "名詞",
    "訳語": "ひざ",
    "レベル": "C"
  },
  {
    "番号": 751,
    "単語": "lady",
    "品詞": "名詞",
    "訳語": "ご婦人、淑女",
    "レベル": "C"
  },
  {
    "番号": 752,
    "単語": "leader",
    "品詞": "名詞",
    "訳語": "リーダー、指導者",
    "レベル": "C"
  },
  {
    "番号": 753,
    "単語": "mall",
    "品詞": "名詞",
    "訳語": "ショッピングセンター 商店街",
    "レベル": "C"
  },
  {
    "番号": 754,
    "単語": "marathon",
    "品詞": "名詞",
    "訳語": "マラソン",
    "レベル": "C"
  },
  {
    "番号": 755,
    "単語": "meaning",
    "品詞": "名詞",
    "訳語": "意味",
    "レベル": "C"
  },
  {
    "番号": 756,
    "単語": "mouse",
    "品詞": "名詞",
    "訳語": "ハツカネズミ",
    "レベル": "C"
  },
  {
    "番号": 757,
    "単語": "parking",
    "品詞": "名詞",
    "訳語": "駐車（場）、駐車できる場所",
    "レベル": "C"
  },
  {
    "番号": 758,
    "単語": "photographer",
    "品詞": "名詞",
    "訳語": "写真家",
    "レベル": "C"
  },
  {
    "番号": 759,
    "単語": "purpose",
    "品詞": "名詞",
    "訳語": "目的",
    "レベル": "C"
  },
  {
    "番号": 760,
    "単語": "radish",
    "品詞": "名詞",
    "訳語": "ラディッシュ、大根",
    "レベル": "C"
  },
  {
    "番号": 761,
    "単語": "reporter",
    "品詞": "名詞",
    "訳語": "通信員、記者",
    "レベル": "C"
  },
  {
    "番号": 762,
    "単語": "ring",
    "品詞": "名詞",
    "訳語": "指輪、輪",
    "レベル": "C"
  },
  {
    "番号": 763,
    "単語": "sailor",
    "品詞": "名詞",
    "訳語": "船員",
    "レベル": "C"
  },
  {
    "番号": 764,
    "単語": "salesclerk",
    "品詞": "名詞",
    "訳語": "店員、販売員",
    "レベル": "C"
  },
  {
    "番号": 765,
    "単語": "service",
    "品詞": "名詞",
    "訳語": "サービス、接客、公共事業、業務",
    "レベル": "C"
  },
  {
    "番号": 766,
    "単語": "shell",
    "品詞": "名詞",
    "訳語": "貝がら",
    "レベル": "C"
  },
  {
    "番号": 767,
    "単語": "snake",
    "品詞": "名詞",
    "訳語": "ヘビ",
    "レベル": "C"
  },
  {
    "番号": 768,
    "単語": "spot",
    "品詞": "名詞",
    "訳語": "場所、地点",
    "レベル": "C"
  },
  {
    "番号": 769,
    "単語": "subway",
    "品詞": "名詞",
    "訳語": "地下鉄",
    "レベル": "C"
  },
  {
    "番号": 770,
    "単語": "sunglasses",
    "品詞": "名詞",
    "訳語": "サングラス",
    "レベル": "C"
  },
  {
    "番号": 771,
    "単語": "surprise",
    "品詞": "名詞",
    "訳語": "予期しない驚き、驚くべきこと",
    "レベル": "C"
  },
  {
    "番号": 772,
    "単語": "teammate",
    "品詞": "名詞",
    "訳語": "チームメイト",
    "レベル": "C"
  },
  {
    "番号": 773,
    "単語": "televison",
    "品詞": "名詞",
    "訳語": "テレビ",
    "レベル": "C"
  },
  {
    "番号": 774,
    "単語": "toilet",
    "品詞": "名詞",
    "訳語": "トイレ",
    "レベル": "C"
  },
  {
    "番号": 775,
    "単語": "track",
    "品詞": "名詞",
    "訳語": "鉄道の線路、駅の～番線",
    "レベル": "C"
  },
  {
    "番号": 776,
    "単語": "turtle",
    "品詞": "名詞",
    "訳語": "ウミガメ",
    "レベル": "C"
  },
  {
    "番号": 777,
    "単語": "whale",
    "品詞": "名詞",
    "訳語": "クジラ",
    "レベル": "C"
  },
  {
    "番号": 778,
    "単語": "wind",
    "品詞": "名詞",
    "訳語": "風",
    "レベル": "C"
  },
  {
    "番号": 779,
    "単語": "yard",
    "品詞": "名詞",
    "訳語": "庭",
    "レベル": "C"
  },
  {
    "番号": 780,
    "単語": "army",
    "品詞": "名詞",
    "訳語": "軍隊、陸軍",
    "レベル": "C"
  },
  {
    "番号": 781,
    "単語": "decoration",
    "品詞": "名詞",
    "訳語": "飾り、装飾",
    "レベル": "C"
  },
  {
    "番号": 782,
    "単語": "pollution",
    "品詞": "名詞",
    "訳語": "汚染、公害",
    "レベル": "C"
  },
  {
    "番号": 783,
    "単語": "amazing",
    "品詞": "形容詞",
    "訳語": "驚くべき",
    "レベル": "C"
  },
  {
    "番号": 784,
    "単語": "British",
    "品詞": "形容詞",
    "訳語": "イギリスの、イギリス人の",
    "レベル": "C"
  },
  {
    "番号": 785,
    "単語": "correct",
    "品詞": "形容詞",
    "訳語": "正しい",
    "レベル": "C"
  },
  {
    "番号": 786,
    "単語": "dry",
    "品詞": "形容詞",
    "訳語": "乾いた",
    "レベル": "C"
  },
  {
    "番号": 787,
    "単語": "front",
    "品詞": "形容詞",
    "訳語": "正面の、前の",
    "レベル": "C"
  },
  {
    "番号": 788,
    "単語": "lovely",
    "品詞": "形容詞",
    "訳語": "美しい、かわいらしい",
    "レベル": "C"
  },
  {
    "番号": 789,
    "単語": "northern",
    "品詞": "形容詞",
    "訳語": "北の、北部の",
    "レベル": "C"
  },
  {
    "番号": 790,
    "単語": "real",
    "品詞": "形容詞",
    "訳語": "本当の、現実の",
    "レベル": "C"
  },
  {
    "番号": 791,
    "単語": "solar",
    "品詞": "形容詞",
    "訳語": "太陽の",
    "レベル": "C"
  },
  {
    "番号": 792,
    "単語": "strange",
    "品詞": "形容詞",
    "訳語": "奇妙な、見知らぬ",
    "レベル": "C"
  },
  {
    "番号": 793,
    "単語": "weak",
    "品詞": "形容詞",
    "訳語": "弱い",
    "レベル": "C"
  },
  {
    "番号": 794,
    "単語": "native",
    "品詞": "形容詞",
    "訳語": "その土地固有の、生まれた土地の",
    "レベル": "C"
  },
  {
    "番号": 795,
    "単語": "slowly",
    "品詞": "副詞",
    "訳語": "ゆっくりと、遅く",
    "レベル": "C"
  },
  {
    "番号": 796,
    "単語": "badly",
    "品詞": "副詞",
    "訳語": "悪く、ひどく",
    "レベル": "C"
  },
  {
    "番号": 797,
    "単語": "online",
    "品詞": "副詞",
    "訳語": "オンラインで、インターネットで",
    "レベル": "C"
  },
  {
    "番号": 798,
    "単語": "along",
    "品詞": "前置詞",
    "訳語": "～に沿って",
    "レベル": "C"
  },
  {
    "番号": 799,
    "単語": "everybody",
    "品詞": "代名詞",
    "訳語": "みんな、誰でも",
    "レベル": "C"
  },
  {
    "番号": 800,
    "単語": "ourselves",
    "品詞": "代名詞",
    "訳語": "私たち自身を",
    "レベル": "C"
  },
  {
    "番号": 801,
    "単語": "act",
    "品詞": "動詞",
    "訳語": "〜を演じる、行動する",
    "レベル": "C"
  },
  {
    "番号": 802,
    "単語": "cause",
    "品詞": "動詞",
    "訳語": "〜を引き起こす、～の原因となる",
    "レベル": "C"
  },
  {
    "番号": 803,
    "単語": "destroy",
    "品詞": "動詞",
    "訳語": "〜を破壊する",
    "レベル": "C"
  },
  {
    "番号": 804,
    "単語": "disappear",
    "品詞": "動詞",
    "訳語": "消える、姿を消す、見えなくなる",
    "レベル": "C"
  },
  {
    "番号": 805,
    "単語": "discover",
    "品詞": "動詞",
    "訳語": "〜を発見する",
    "レベル": "C"
  },
  {
    "番号": 806,
    "単語": "escape",
    "品詞": "動詞",
    "訳語": "逃げる",
    "レベル": "C"
  },
  {
    "番号": 807,
    "単語": "exercise",
    "品詞": "動詞",
    "訳語": "運動する",
    "レベル": "C"
  },
  {
    "番号": 808,
    "単語": "fail",
    "品詞": "動詞",
    "訳語": "試験に落ちる、失敗する",
    "レベル": "C"
  },
  {
    "番号": 809,
    "単語": "feed",
    "品詞": "動詞",
    "訳語": "～にエサを与える",
    "レベル": "C"
  },
  {
    "番号": 810,
    "単語": "hide",
    "品詞": "動詞",
    "訳語": "隠れる、〜を隠す",
    "レベル": "C"
  },
  {
    "番号": 811,
    "単語": "lay",
    "品詞": "動詞",
    "訳語": "卵を産む、～を横たえる、～を置く",
    "レベル": "C"
  },
  {
    "番号": 812,
    "単語": "lead",
    "品詞": "動詞",
    "訳語": "～を率いる、導く",
    "レベル": "C"
  },
  {
    "番号": 813,
    "単語": "offer",
    "品詞": "動詞",
    "訳語": "〜を提供する、申し出る、～を差し出す",
    "レベル": "C"
  },
  {
    "番号": 814,
    "単語": "produce",
    "品詞": "動詞",
    "訳語": "～を生産する",
    "レベル": "C"
  },
  {
    "番号": 815,
    "単語": "realize",
    "品詞": "動詞",
    "訳語": "〜と気づく、実現する",
    "レベル": "C"
  },
  {
    "番号": 816,
    "単語": "shine",
    "品詞": "動詞",
    "訳語": "輝く",
    "レベル": "C"
  },
  {
    "番号": 817,
    "単語": "smoke",
    "品詞": "動詞",
    "訳語": "煙草を吸う",
    "レベル": "C"
  },
  {
    "番号": 818,
    "単語": "solve",
    "品詞": "動詞",
    "訳語": "～を解決する、～を解く",
    "レベル": "C"
  },
  {
    "番号": 819,
    "単語": "survive",
    "品詞": "動詞",
    "訳語": "～を生き残る",
    "レベル": "C"
  },
  {
    "番号": 820,
    "単語": "adventure",
    "品詞": "名詞",
    "訳語": "冒険",
    "レベル": "C"
  },
  {
    "番号": 821,
    "単語": "age",
    "品詞": "名詞",
    "訳語": "年齢",
    "レベル": "C"
  },
  {
    "番号": 822,
    "単語": "arm",
    "品詞": "名詞",
    "訳語": "腕",
    "レベル": "C"
  },
  {
    "番号": 823,
    "単語": "athlete",
    "品詞": "名詞",
    "訳語": "運動選手",
    "レベル": "C"
  },
  {
    "番号": 824,
    "単語": "bottom",
    "品詞": "名詞",
    "訳語": "底、下部",
    "レベル": "C"
  },
  {
    "番号": 825,
    "単語": "castle",
    "品詞": "名詞",
    "訳語": "城",
    "レベル": "C"
  },
  {
    "番号": 826,
    "単語": "ceiling",
    "品詞": "名詞",
    "訳語": "天井",
    "レベル": "C"
  },
  {
    "番号": 827,
    "単語": "closet",
    "品詞": "副詞",
    "訳語": "クローゼット、押し入れ",
    "レベル": "C"
  },
  {
    "番号": 828,
    "単語": "corner",
    "品詞": "名詞",
    "訳語": "角",
    "レベル": "C"
  },
  {
    "番号": 829,
    "単語": "course",
    "品詞": "名詞",
    "訳語": "講座、コース、進路",
    "レベル": "C"
  },
  {
    "番号": 830,
    "単語": "custom",
    "品詞": "名詞",
    "訳語": "慣習",
    "レベル": "C"
  },
  {
    "番号": 831,
    "単語": "department store",
    "品詞": "名詞",
    "訳語": "デパート、百貨店",
    "レベル": "C"
  },
  {
    "番号": 832,
    "単語": "director",
    "品詞": "名詞",
    "訳語": "監督、指導者",
    "レベル": "C"
  },
  {
    "番号": 833,
    "単語": "discount",
    "品詞": "名詞",
    "訳語": "割引",
    "レベル": "C"
  },
  {
    "番号": 834,
    "単語": "doghouse",
    "品詞": "名詞",
    "訳語": "犬小屋",
    "レベル": "C"
  },
  {
    "番号": 835,
    "単語": "drugstore",
    "品詞": "名詞",
    "訳語": "薬局、ドラッグストア",
    "レベル": "C"
  },
  {
    "番号": 836,
    "単語": "ear",
    "品詞": "名詞",
    "訳語": "耳",
    "レベル": "C"
  },
  {
    "番号": 837,
    "単語": "examination",
    "品詞": "名詞",
    "訳語": "試験",
    "レベル": "C"
  },
  {
    "番号": 838,
    "単語": "factory",
    "品詞": "名詞",
    "訳語": "工場",
    "レベル": "C"
  },
  {
    "番号": 839,
    "単語": "fair",
    "品詞": "名詞",
    "訳語": "見本市、品評会",
    "レベル": "C"
  },
  {
    "番号": 840,
    "単語": "fire",
    "品詞": "名詞",
    "訳語": "火事、火",
    "レベル": "C"
  },
  {
    "番号": 841,
    "単語": "furniture",
    "品詞": "名詞",
    "訳語": "家具",
    "レベル": "C"
  },
  {
    "番号": 842,
    "単語": "god",
    "品詞": "名詞",
    "訳語": "神",
    "レベル": "C"
  },
  {
    "番号": 843,
    "単語": "government",
    "品詞": "名詞",
    "訳語": "政府",
    "レベル": "C"
  },
  {
    "番号": 844,
    "単語": "grass",
    "品詞": "名詞",
    "訳語": "草、芝生",
    "レベル": "C"
  },
  {
    "番号": 845,
    "単語": "hallway",
    "品詞": "名詞",
    "訳語": "屋内の通路、廊下、玄関",
    "レベル": "C"
  },
  {
    "番号": 846,
    "単語": "host",
    "品詞": "名詞",
    "訳語": "受け入れ側、（客をもてなす）主人",
    "レベル": "C"
  },
  {
    "番号": 847,
    "単語": "hurricane",
    "品詞": "名詞",
    "訳語": "ハリケーン",
    "レベル": "C"
  },
  {
    "番号": 848,
    "単語": "instrument",
    "品詞": "名詞",
    "訳語": "楽器、精密な機械",
    "レベル": "C"
  },
  {
    "番号": 849,
    "単語": "land",
    "品詞": "名詞",
    "訳語": "陸、土地",
    "レベル": "C"
  },
  {
    "番号": 850,
    "単語": "list",
    "品詞": "名詞",
    "訳語": "リスト、表",
    "レベル": "C"
  },
  {
    "番号": 851,
    "単語": "medicine",
    "品詞": "名詞",
    "訳語": "薬",
    "レベル": "C"
  },
  {
    "番号": 852,
    "単語": "neighbor",
    "品詞": "名詞",
    "訳語": "近所の人",
    "レベル": "C"
  },
  {
    "番号": 853,
    "単語": "noise",
    "品詞": "名詞",
    "訳語": "物音、騒音",
    "レベル": "C"
  },
  {
    "番号": 854,
    "単語": "opinion",
    "品詞": "名詞",
    "訳語": "意見",
    "レベル": "C"
  },
  {
    "番号": 855,
    "単語": "safety",
    "品詞": "名詞",
    "訳語": "安全",
    "レベル": "C"
  },
  {
    "番号": 856,
    "単語": "science fiction",
    "品詞": "名詞",
    "訳語": "SF、空想科学小説",
    "レベル": "C"
  },
  {
    "番号": 857,
    "単語": "scissors",
    "品詞": "名詞",
    "訳語": "はさみ",
    "レベル": "C"
  },
  {
    "番号": 858,
    "単語": "secret",
    "品詞": "名詞",
    "訳語": "秘密",
    "レベル": "C"
  },
  {
    "番号": 859,
    "単語": "section",
    "品詞": "名詞",
    "訳語": "売り場などのコーナー、一部分、区分、部門",
    "レベル": "C"
  },
  {
    "番号": 860,
    "単語": "sentence",
    "品詞": "名詞",
    "訳語": "文",
    "レベル": "C"
  },
  {
    "番号": 861,
    "単語": "stamp",
    "品詞": "名詞",
    "訳語": "切手",
    "レベル": "C"
  },
  {
    "番号": 862,
    "単語": "state",
    "品詞": "名詞",
    "訳語": "（アメリカなどの）州、国家、状態",
    "レベル": "C"
  },
  {
    "番号": 863,
    "単語": "tool",
    "品詞": "名詞",
    "訳語": "道具",
    "レベル": "C"
  },
  {
    "番号": 864,
    "単語": "trick",
    "品詞": "名詞",
    "訳語": "芸当、いたずら",
    "レベル": "C"
  },
  {
    "番号": 865,
    "単語": "typhoon",
    "品詞": "名詞",
    "訳語": "台風",
    "レベル": "C"
  },
  {
    "番号": 866,
    "単語": "view",
    "品詞": "名詞",
    "訳語": "眺め、景色",
    "レベル": "C"
  },
  {
    "番号": 867,
    "単語": "village",
    "品詞": "名詞",
    "訳語": "村",
    "レベル": "C"
  },
  {
    "番号": 868,
    "単語": "wood",
    "品詞": "名詞",
    "訳語": "木材 、（複で）森",
    "レベル": "C"
  },
  {
    "番号": 869,
    "単語": "damage",
    "品詞": "名詞",
    "訳語": "被害、損害",
    "レベル": "C"
  },
  {
    "番号": 870,
    "単語": "enemy",
    "品詞": "名詞",
    "訳語": "敵",
    "レベル": "C"
  },
  {
    "番号": 871,
    "単語": "importance",
    "品詞": "名詞",
    "訳語": "重要性",
    "レベル": "C"
  },
  {
    "番号": 872,
    "単語": "resort",
    "品詞": "名詞",
    "訳語": "行楽地",
    "レベル": "C"
  },
  {
    "番号": 873,
    "単語": "skill",
    "品詞": "名詞",
    "訳語": "技能、技術",
    "レベル": "C"
  },
  {
    "番号": 874,
    "単語": "speed",
    "品詞": "名詞",
    "訳語": "速度、スピード",
    "レベル": "C"
  },
  {
    "番号": 875,
    "単語": "asleep",
    "品詞": "形容詞",
    "訳語": "眠って、眠り込んで",
    "レベル": "C"
  },
  {
    "番号": 876,
    "単語": "common",
    "品詞": "形容詞",
    "訳語": "よくある、共通の",
    "レベル": "C"
  },
  {
    "番号": 877,
    "単語": "daily",
    "品詞": "形容詞",
    "訳語": "日常の、毎日の",
    "レベル": "C"
  },
  {
    "番号": 878,
    "単語": "female",
    "品詞": "形容詞",
    "訳語": "女性の、雌の",
    "レベル": "C"
  },
  {
    "番号": 879,
    "単語": "friendly",
    "品詞": "形容詞",
    "訳語": "親しみやすい、親切な",
    "レベル": "C"
  },
  {
    "番号": 880,
    "単語": "homesick",
    "品詞": "形容詞",
    "訳語": "ホームシックの、故郷を恋しがる",
    "レベル": "C"
  },
  {
    "番号": 881,
    "単語": "human",
    "品詞": "形容詞",
    "訳語": "人人間の",
    "レベル": "C"
  },
  {
    "番号": 882,
    "単語": "latest",
    "品詞": "形容詞",
    "訳語": "最新の",
    "レベル": "C"
  },
  {
    "番号": 883,
    "単語": "lonely",
    "品詞": "形容詞",
    "訳語": "ひとりぼっちの、さみしい",
    "レベル": "C"
  },
  {
    "番号": 884,
    "単語": "natural",
    "品詞": "形容詞",
    "訳語": "自然の",
    "レベル": "C"
  },
  {
    "番号": 885,
    "単語": "necessary",
    "品詞": "形容詞",
    "訳語": "必要な",
    "レベル": "C"
  },
  {
    "番号": 886,
    "単語": "useful",
    "品詞": "形容詞",
    "訳語": "役に立つ",
    "レベル": "C"
  },
  {
    "番号": 887,
    "単語": "wild",
    "品詞": "形容詞",
    "訳語": "野生の",
    "レベル": "C"
  },
  {
    "番号": 888,
    "単語": "alive",
    "品詞": "形容詞",
    "訳語": "生きている",
    "レベル": "C"
  },
  {
    "番号": 889,
    "単語": "huge",
    "品詞": "形容詞",
    "訳語": "巨大な",
    "レベル": "C"
  },
  {
    "番号": 890,
    "単語": "low",
    "品詞": "形容詞",
    "訳語": "低い",
    "レベル": "C"
  },
  {
    "番号": 891,
    "単語": "male",
    "品詞": "形容詞",
    "訳語": "男性の、雄の",
    "レベル": "C"
  },
  {
    "番号": 892,
    "単語": "polite",
    "品詞": "形容詞",
    "訳語": "礼儀正しい",
    "レベル": "C"
  },
  {
    "番号": 893,
    "単語": "serious",
    "品詞": "形容詞",
    "訳語": "重大な、まじめな",
    "レベル": "C"
  },
  {
    "番号": 894,
    "単語": "southern",
    "品詞": "形容詞",
    "訳語": "南の、南部の",
    "レベル": "C"
  },
  {
    "番号": 895,
    "単語": "especially",
    "品詞": "副詞",
    "訳語": "特に",
    "レベル": "C"
  },
  {
    "番号": 896,
    "単語": "somewhere",
    "品詞": "副詞",
    "訳語": "どこかに",
    "レベル": "C"
  },
  {
    "番号": 897,
    "単語": "suddenly",
    "品詞": "副詞",
    "訳語": "突然",
    "レベル": "C"
  },
  {
    "番号": 898,
    "単語": "toward",
    "品詞": "前置詞",
    "訳語": "〜に向かって、～の方へ",
    "レベル": "C"
  },
  {
    "番号": 899,
    "単語": "although",
    "品詞": "接続詞",
    "訳語": "〜だけれども",
    "レベル": "C"
  },
  {
    "番号": 900,
    "単語": "nothing",
    "品詞": "代名詞",
    "訳語": "何も～ない",
    "レベル": "C"
  }
]

# Database file
DB_PATH = "eiken_study.db"

# ----------------- DATABASE MANAGEMENT -----------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if old table structure without user_id in weaknesses exists
    try:
        cursor.execute("SELECT user_id FROM weaknesses LIMIT 1")
    except sqlite3.OperationalError:
        # Table doesn't exist or is old schema, let's recreate database safely
        cursor.execute("DROP TABLE IF EXISTS weaknesses")
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("DROP TABLE IF EXISTS overcome_words")
        
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT UNIQUE,
        password TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weaknesses (
        user_id INTEGER,
        word_id INTEGER,
        PRIMARY KEY (user_id, word_id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS overcome_words (
        user_id INTEGER,
        word_id INTEGER,
        PRIMARY KEY (user_id, word_id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    conn.close()

def register_user(nickname, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (nickname, password) VALUES (?, ?)", (nickname.strip(), password.strip()))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def login_user(nickname, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE nickname = ? AND password = ?", (nickname.strip(), password.strip()))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

def add_weakness(user_id, word_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO weaknesses (user_id, word_id) VALUES (?, ?)", (user_id, word_id))
    # Remove from overcome if added to weakness
    cursor.execute("DELETE FROM overcome_words WHERE user_id = ? AND word_id = ?", (user_id, word_id))
    conn.commit()
    conn.close()

def remove_weakness(user_id, word_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM weaknesses WHERE user_id = ? AND word_id = ?", (user_id, word_id))
    conn.commit()
    conn.close()

def get_weaknesses(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT word_id FROM weaknesses WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

def add_overcome(user_id, word_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO overcome_words (user_id, word_id) VALUES (?, ?)", (user_id, word_id))
    # Remove from weaknesses if added to overcome
    cursor.execute("DELETE FROM weaknesses WHERE user_id = ? AND word_id = ?", (user_id, word_id))
    conn.commit()
    conn.close()

def get_overcome_count(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM overcome_words WHERE user_id = ?", (user_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Initialize database
init_db()

# ----------------- CSV LOADER AND RESTORER -----------------
def restore_csv_file():
    # If eiken_words.csv is corrupted or missing, self-heal automatically
    with open("eiken_words.csv", "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["番号", "単語", "品詞", "訳語", "レベル"])
        writer.writeheader()
        for w in BACKUP_WORDS:
            writer.writerow(w)

@st.cache_data
def load_all_words():
    # Safe self-healing load
    if not os.path.exists("eiken_words.csv"):
        restore_csv_file()
        
    try:
        words = []
        # Support utf-8-sig to automatically handle BOM safely
        with open("eiken_words.csv", "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            if not headers:
                raise ValueError("CSV is empty")
            
            # Clean headers (strip spaces and BOM symbols if any)
            headers = [h.strip().replace("\ufeff", "") for h in headers]
            
            # Map column indices
            try:
                idx_num = headers.index("番号")
                idx_word = headers.index("単語")
                idx_pos = headers.index("品詞")
                idx_meaning = headers.index("訳語")
                idx_level = headers.index("レベル")
            except ValueError:
                # If column names mismatch, trigger self-heal and retry cp932
                restore_csv_file()
                return BACKUP_WORDS
                
            for row in reader:
                if not row or len(row) < len(headers):
                    continue
                words.append({
                    "番号": int(row[idx_num].strip()),
                    "単語": row[idx_word].strip(),
                    "品詞": row[idx_pos].strip(),
                    "訳語": row[idx_meaning].strip(),
                    "レベル": row[idx_level].strip()
                })
        return words
    except Exception as e:
        # Fallback to embedded backup
        restore_csv_file()
        return BACKUP_WORDS

ALL_WORDS = load_all_words()

# ----------------- HELPER: SPELLING HINT GENERATOR -----------------
def get_spelling_hint(word, difficulty):
    # Cleans "make A B" -> "make", "give 人 もの" -> "give"
    clean_word = word.split(' ')[0]
    clean_word = re.sub(r"[^a-zA-Z\s'-]", "", clean_word).strip()
    
    if difficulty == "EASY":
        hint = []
        for i, char in enumerate(clean_word):
            if not char.isalpha():
                hint.append(char)
            elif i == 0 or i == len(clean_word) - 1:
                hint.append(char)
            else:
                hint.append("＿")
        return " ".join(hint)
    elif difficulty == "MIDDLE":
        hint = []
        for i, char in enumerate(clean_word):
            if not char.isalpha():
                hint.append(char)
            elif i == 0:
                hint.append(char)
            else:
                hint.append("＿")
        return " ".join(hint)
    else: # HARD
        hint = []
        for char in clean_word:
            if not char.isalpha():
                hint.append(char)
            else:
                hint.append("＿")
        return " ".join(hint)

# ----------------- JS INJECTORS FOR AUTO FOCUS -----------------
def inject_focus_script(current_index):
    # Perfect targeted auto focus script inside sandbox context
    js_code = f'''
    <script>
    setTimeout(function() {{
        try {{
            var doc = window.parent.document;
            var inputs = doc.querySelectorAll('input');
            for (var i = 0; i < inputs.length; i++) {{
                var inp = inputs[i];
                if (inp.id && inp.id.includes("spell_input_" + {current_index})) {{
                    inp.focus();
                    inp.select();
                    break;
                }}
            }}
        }} catch(err) {{
            console.log("Focus error: " + err);
        }}
    }}, 150);
    </script>
    '''
    st.components.v1.html(js_code, height=0)

# ----------------- EXIT DIALOG POPUP RENDERING -----------------
def render_exit_button():
    st.write("---")
    if st.session_state.get("confirm_exit", False):
        st.markdown('<div class="small-btn">', unsafe_allow_html=True)
        st.warning("本当に終了しますか？ここまでの学習状況（克服・弱点リスト）はデータベースに同期されています。")
        conf_cols = st.columns(2)
        with conf_cols[0]:
            if st.button("はい、終了します", type="primary", use_container_width=True):
                st.session_state.confirm_exit = False
                st.session_state.mode = "TOP"
                st.rerun()
        with conf_cols[1]:
            if st.button("いいえ、続けます", use_container_width=True):
                st.session_state.confirm_exit = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="small-btn">', unsafe_allow_html=True)
        if st.button("🚪 クイズを中断してTOPへ戻る", use_container_width=True):
            st.session_state.confirm_exit = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- STYLING AND CUSTOM GRAPHICS -----------------
st.markdown("""
<style>
    /* Styling elements matching high quality specification */
    .stButton>button {
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.2s ease;
    }
    .flashcard {
        border: 2px solid #e0e0e0;
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        background-color: #ffffff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        min-height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    .flashcard-pos {
        color: #888888;
        font-size: 16px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .flashcard-eng {
        color: #1e3d59;
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 15px;
        letter-spacing: 0.5px;
    }
    .flashcard-meaning {
        color: #ff6e40;
        font-size: 26px;
        font-weight: bold;
        margin-top: 10px;
    }
    /* 30% Smaller Action Buttons block */
    .small-btn .stButton>button {
        font-size: 13px !important;
        padding: 4px 8px !important;
        min-height: auto !important;
        font-weight: normal !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE INITS -----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "nickname" not in st.session_state:
    st.session_state.nickname = ""
if "weak_ids" not in st.session_state:
    st.session_state.weak_ids = []
if "mode" not in st.session_state:
    st.session_state.mode = "TOP"
if "quiz_words" not in st.session_state:
    st.session_state.quiz_words = []
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "answer_checked" not in st.session_state:
    st.session_state.answer_checked = False
if "confirm_exit" not in st.session_state:
    st.session_state.confirm_exit = False
if "card_flipped" not in st.session_state:
    st.session_state.card_flipped = False
if "speech_enabled" not in st.session_state:
    st.session_state.speech_enabled = True

# ----------------- SCREEN: LOGIN / SIGNUP -----------------
if not st.session_state.logged_in:
    st.title("🔑 英検3級 ログイン・新規登録")
    tab_log, tab_reg = st.tabs(["🔒 ログイン", "📝 新規アカウント登録"])
    
    with tab_log:
        l_nick = st.text_input("ニックネーム", key="log_nick", placeholder="ニックネームを入力してください")
        l_pwd = st.text_input("パスワード (8桁の数字)", type="password", key="log_pwd", placeholder="例: 12345678")
        if st.button("ログイン", type="primary", use_container_width=True):
            if len(l_pwd.strip()) != 8 or not l_pwd.strip().isdigit():
                st.error("パスワードは【半角数字のぴったり8桁】で入力してください。")
            else:
                uid = login_user(l_nick, l_pwd)
                if uid is not None:
                    st.session_state.logged_in = True
                    st.session_state.user_id = uid
                    st.session_state.nickname = l_nick.strip()
                    st.session_state.weak_ids = get_weaknesses(uid)
                    st.success(f"ようこそ、{st.session_state.nickname} さん！")
                    st.rerun()
                else:
                    st.error("ニックネームまたはパスワードが正しくありません。")
                    
    with tab_reg:
        r_nick = st.text_input("ご希望のニックネーム", key="reg_nick", placeholder="例: エイケン太郎")
        r_pwd = st.text_input("パスワード (半角数字8桁)", type="password", key="reg_pwd", placeholder="例: 98765432")
        if st.button("新規登録する", use_container_width=True):
            if not r_nick.strip():
                st.error("ニックネームを入力してください。")
            elif len(r_pwd.strip()) != 8 or not r_pwd.strip().isdigit():
                st.error("パスワードは【半角数字のぴったり8桁】のみ受け付けます。")
            else:
                if register_user(r_nick, r_pwd):
                    st.success("アカウントを登録しました！ログインタブからログインしてください。")
                else:
                    st.error("このニックネームは既に使用されています。別の名前をお試しください。")

# ----------------- SCREEN: STUDY MAIN TOP -----------------
elif st.session_state.mode == "TOP":
    st.title("📖 英検3級 単語マスター v31")
    
    # Header user bar
    col_u1, col_u2 = st.columns([3, 1])
    with col_u1:
        st.subheader(f"👋 こんにちは、{st.session_state.nickname} さん！")
    with col_u2:
        if st.button("🚪 ログアウト", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.nickname = ""
            st.session_state.weak_ids = []
            st.rerun()
            
    # Calculate progress for SVG Donut chart
    total_db_words = len(ALL_WORDS)
    if total_db_words == 0:
        total_db_words = 900
    overcome_count = get_overcome_count(st.session_state.user_id)
    progress_percent = min(100.0, (overcome_count / total_db_words) * 100.0)
    
    # Draw lightweight circular donut chart using safe SVG injection
    stroke_dash = progress_percent * 2.827  # Circumference of r=45 is 2 * pi * 45 = 282.7
    donut_svg = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 15px;">
        <svg width="160" height="160" viewBox="0 0 120 120">
            <!-- Background circle -->
            <circle cx="60" cy="60" r="45" fill="none" stroke="#f0f0f0" stroke-width="12" />
            <!-- Active progress stroke -->
            <circle cx="60" cy="60" r="45" fill="none" stroke="#4caf50" stroke-width="12"
                    stroke-dasharray="282.7" stroke-dashoffset="{282.7 - stroke_dash}"
                    stroke-linecap="round" transform="rotate(-90 60 60)" />
            <!-- Centered progress text -->
            <text x="60" y="65" font-family="sans-serif" font-size="18" font-weight="bold" fill="#333333" text-anchor="middle">
                {progress_percent:.1f}%
            </text>
        </svg>
        <div style="font-weight: bold; margin-top: 10px; color: #555555; font-size: 15px;">
            克服（習得済み）単語数: {overcome_count} / {total_db_words} 語
        </div>
    </div>
    """
    st.components.v1.html(donut_svg, height=210)
    
    # Load weaknesses
    st.session_state.weak_ids = get_weaknesses(st.session_state.user_id)
    weak_count = len(st.session_state.weak_ids)
    
    st.write("---")
    st.subheader("🎯 学習メニュー設定")
    
    # Toggle switch for voice auto speech synthesis
    st.session_state.speech_enabled = st.toggle("🔊 自動音声読み上げ (女性ネイティブ)", value=st.session_state.speech_enabled)
    
    # 1. Mode selection
    mode_choice = st.selectbox(
        "学習モードを選択:",
        ["🎴 フラッシュカード (暗記)", "🎯 英⇛日 4択テスト", "⌨️ 日⇛英 スペル練習"]
    )
    
    # 2. Scope selection
    scope_options = ["すべて (1〜900番)", "レベルAリスト (1〜300番)", "レベルBリスト (301〜600番)", "レベルCリスト (601〜900番)", "番号指定"]
    if weak_count > 0:
        scope_options.insert(0, f"🔥 弱点克服モード (登録中: {weak_count}語)")
        
    scope_choice = st.selectbox("出題範囲を選択:", scope_options)
    
    # Safe range input if 番号指定 is selected
    start_num, end_num = 1, 900
    if scope_choice == "番号指定":
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            start_num = st.number_input("開始番号", min_value=1, max_value=900, value=1)
        with col_r2:
            end_num = st.number_input("終了番号", min_value=1, max_value=900, value=100)
            
    # 3. Spelling difficulty
    difficulty_choice = "EASY"
    if mode_choice == "⌨️ 日⇛英 スペル練習":
        difficulty_choice = st.selectbox("ヒント難易度:", ["EASY", "MIDDLE", "HARD"])
        
    st.write("---")
    
    # Start button
    if st.button("🚀 学習をスタートする！", type="primary", use_container_width=True):
        selected_words = []
        
        if "🔥 弱点克服モード" in scope_choice:
            selected_words = [w for w in ALL_WORDS if w["番号"] in st.session_state.weak_ids]
        elif scope_choice == "すべて (1〜900番)":
            selected_words = ALL_WORDS.copy()
        elif scope_choice == "レベルAリスト (1〜300番)":
            selected_words = [w for w in ALL_WORDS if w["レベル"] == "A"]
        elif scope_choice == "レベルBリスト (301〜600番)":
            selected_words = [w for w in ALL_WORDS if w["レベル"] == "B"]
        elif scope_choice == "レベルCリスト (601〜900番)":
            selected_words = [w for w in ALL_WORDS if w["レベル"] == "C"]
        elif scope_choice == "番号指定":
            selected_words = [w for w in ALL_WORDS if start_num <= w["番号"] <= end_num]
            
        if not selected_words:
            st.error("選択された出題範囲に単語がありません。")
        else:
            # Always shuffle randomly on start
            random.shuffle(selected_words)
            st.session_state.quiz_words = selected_words
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.session_state.mode = mode_choice
            st.session_state.spell_difficulty = difficulty_choice
            st.session_state.answer_checked = False
            st.session_state.confirm_exit = False
            st.session_state.card_flipped = False
            st.rerun()

# ----------------- MODE: FLASHCARD -----------------
elif st.session_state.mode == "🎴 フラッシュカード (暗記)":
    current_index = st.session_state.quiz_index
    total_q = len(st.session_state.quiz_words)
    
    if current_index >= total_q:
        st.success("🎉 すべてのカードを学習しました！")
        if st.button("学習トップに戻る", type="primary", use_container_width=True):
            st.session_state.mode = "TOP"
            st.rerun()
    else:
        st.subheader(f"🎴 暗記フラッシュカード ({current_index + 1} / {total_q})")
        
        current_word = st.session_state.quiz_words[current_index]
        word_id = current_word["番号"]
        word_eng = current_word["単語"]
        word_pos = current_word["品詞"]
        word_meaning = current_word["訳語"]
        
        # Trigger native female neural speech voice automatic playback on loading
        # Only speech if speech_enabled is True
        clean_speech_word = word_eng.split(' ')[0]
        clean_speech_word = re.sub(r"[^a-zA-Z\s'-]", "", clean_speech_word).strip()
        
        if st.session_state.speech_enabled:
            speech_js = f'''
            <script>
            try {{
                var msg = new SpeechSynthesisUtterance("{clean_speech_word}");
                msg.lang = "en-US";
                msg.rate = 0.95;
                msg.pitch = 1.0;
                
                // Find beautiful natural female neural voice
                var voices = window.speechSynthesis.getVoices();
                var femaleVoice = null;
                for (var i = 0; i < voices.length; i++) {{
                    var v = voices[i];
                    var name = v.name.toLowerCase();
                    var lang = v.lang.toLowerCase();
                    if (lang.includes("en-us") || lang.includes("en-gb")) {{
                        if (name.includes("natural") || name.includes("neural") || name.includes("aria") || name.includes("jenny") || name.includes("samantha") || name.includes("google")) {{
                            if (name.includes("female") || name.includes("aria") || name.includes("jenny") || name.includes("samantha") || name.includes("zira")) {{
                                femaleVoice = v;
                                break;
                            }}
                        }}
                    }}
                }}
                if (femaleVoice) {{
                    msg.voice = femaleVoice;
                }}
                window.speechSynthesis.speak(msg);
            }} catch(err) {{
                console.log("TTS error: " + err);
            }}
            </script>
            '''
            st.components.v1.html(speech_js, height=0)
            
        # Draw card layout matching v29
        card_html = f'''
        <div class="flashcard">
            <div class="flashcard-pos">[{word_pos}] (No. {word_id})</div>
            <div class="flashcard-eng">{word_eng}</div>
        '''
        if st.session_state.card_flipped:
            card_html += f'<div class="flashcard-meaning">{word_meaning}</div>'
        card_html += '</div>'
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Sound playback helper if "Speak" button is manually triggered
        # Note: Manual button always speaks, even if speech_enabled is OFF
        manual_speech_js = f'''
        <script>
        try {{
            var msg = new SpeechSynthesisUtterance("{clean_speech_word}");
            msg.lang = "en-US";
            msg.rate = 0.95;
            msg.pitch = 1.0;
            var voices = window.speechSynthesis.getVoices();
            var femaleVoice = null;
            for (var i = 0; i < voices.length; i++) {{
                var v = voices[i];
                var name = v.name.toLowerCase();
                if (v.lang.toLowerCase().includes("en")) {{
                    if (name.includes("natural") || name.includes("neural") || name.includes("aria") || name.includes("jenny") || name.includes("samantha")) {{
                        femaleVoice = v;
                        break;
                    }}
                }}
            }}
            if (femaleVoice) msg.voice = femaleVoice;
            window.speechSynthesis.speak(msg);
        }} catch(err) {{}}
        </script>
        '''
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            if st.button("🔊 英単語の音声を聞く", use_container_width=True):
                st.components.v1.html(manual_speech_js, height=0)
        with col_f2:
            if not st.session_state.card_flipped:
                if st.button("🔄 タップして裏返す", type="primary", use_container_width=True):
                    st.session_state.card_flipped = True
                    st.rerun()
            else:
                if st.button("🔄 タップして表に戻す", type="primary", use_container_width=True):
                    st.session_state.card_flipped = False
                    st.rerun()
                    
        st.write("---")
        
        # Control panel (reduced 30% spacing/weight)
        st.markdown('<div class="small-btn">', unsafe_allow_html=True)
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            if st.button("⬅️ 前のカード", use_container_width=True):
                if current_index > 0:
                    st.session_state.quiz_index -= 1
                    st.session_state.card_flipped = False
                    st.rerun()
        with col_c2:
            if st.button("❌ まだ覚えていない", use_container_width=True):
                # Add to weaknesses
                add_weakness(st.session_state.user_id, word_id)
                if current_index < total_q - 1:
                    st.session_state.quiz_index += 1
                else:
                    st.session_state.quiz_index += 1
                st.session_state.card_flipped = False
                st.rerun()
        with col_c3:
            if st.button("✅ 覚えた！次のカード", use_container_width=True):
                # Save overcome progress
                add_overcome(st.session_state.user_id, word_id)
                if current_index < total_q - 1:
                    st.session_state.quiz_index += 1
                else:
                    st.session_state.quiz_index += 1
                st.session_state.card_flipped = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Render exit dialog button
        render_exit_button()

# ----------------- MODE: 4-CHOICE MULTIPLE CHOICE -----------------
elif st.session_state.mode == "🎯 英⇛日 4択テスト":
    current_index = st.session_state.quiz_index
    total_q = len(st.session_state.quiz_words)
    
    if current_index >= total_q:
        st.success(f"🎉 テスト完了！スコア: {st.session_state.quiz_score} / {total_q}")
        if st.button("学習トップに戻る", type="primary", use_container_width=True):
            st.session_state.mode = "TOP"
            st.rerun()
    else:
        st.subheader(f"🎯 4択テスト ({current_index + 1} / {total_q})")
        
        current_word = st.session_state.quiz_words[current_index]
        word_id = current_word["番号"]
        word_eng = current_word["単語"]
        word_pos = current_word["品詞"]
        word_meaning = current_word["訳語"]
        
        # Native Female Voice automatic playback for 4-Choice
        clean_speech_word = word_eng.split(' ')[0]
        clean_speech_word = re.sub(r"[^a-zA-Z\s'-]", "", clean_speech_word).strip()
        
        if st.session_state.speech_enabled and not st.session_state.answer_checked:
            speech_js = f'''
            <script>
            try {{
                var msg = new SpeechSynthesisUtterance("{clean_speech_word}");
                msg.lang = "en-US";
                msg.rate = 0.95;
                msg.pitch = 1.0;
                var voices = window.speechSynthesis.getVoices();
                var femaleVoice = null;
                for (var i = 0; i < voices.length; i++) {{
                    var v = voices[i];
                    var name = v.name.toLowerCase();
                    if (v.lang.toLowerCase().includes("en")) {{
                        if (name.includes("natural") || name.includes("neural") || name.includes("aria") || name.includes("jenny") || name.includes("samantha")) {{
                            femaleVoice = v;
                            break;
                        }}
                    }}
                }}
                if (femaleVoice) msg.voice = femaleVoice;
                window.speechSynthesis.speak(msg);
            }} catch(err) {{}}
            </script>
            '''
            st.components.v1.html(speech_js, height=0)
            
        # Draw targeted English word with large font
        st.markdown(f'''
        <div class="flashcard">
            <div class="flashcard-pos">[{word_pos}] (No. {word_id})</div>
            <div class="flashcard-eng">{word_eng}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # 4-Choice options caching (Perfect Index Syncing)
        options_key = f"opts_current_index_{current_index}"
        if options_key not in st.session_state:
            # Pick 3 wrong options from backup list safely
            wrong_candidates = [w["訳語"] for w in ALL_WORDS if w["訳語"] != word_meaning]
            wrong_choices = random.sample(wrong_candidates, 3)
            choices = wrong_choices + [word_meaning]
            random.shuffle(choices)
            st.session_state[options_key] = choices
            
        choices = st.session_state[options_key]
        
        # Render choice buttons
        selected_answer = None
        for i, choice in enumerate(choices):
            if st.button(f" {i+1}.  {choice}", key=f"choice_{current_index}_{i}", use_container_width=True, disabled=st.session_state.answer_checked):
                selected_answer = choice
                
        # If an option was selected, trigger evaluation and play base64 sound
        if selected_answer is not None:
            st.session_state.answer_checked = True
            st.session_state.selected_choice = selected_answer
            if selected_answer == word_meaning:
                st.session_state.quiz_score += 1
                st.session_state.is_correct = True
                add_overcome(st.session_state.user_id, word_id)
                # Play base64 beautiful chime
                sound_html = f'<audio autoplay src="data:audio/wav;base64,{CHIME_B64}"></audio>'
                st.components.v1.html(sound_html, height=0)
            else:
                st.session_state.is_correct = False
                add_weakness(st.session_state.user_id, word_id)
                # Play base64 buzzer
                sound_html = f'<audio autoplay src="data:audio/wav;base64,{BUZZER_B64}"></audio>'
                st.components.v1.html(sound_html, height=0)
                
        # Show correctness result
        if st.session_state.answer_checked:
            if st.session_state.is_correct:
                st.success(f"⭕ 正解！ 「{word_meaning}」")
            else:
                st.error(f"❌ 不正解！ あなたの選択: {st.session_state.selected_choice}  (正解: {word_meaning})")
                
            if st.button("次の問題に進む ➡️", type="primary", use_container_width=True):
                st.session_state.answer_checked = False
                st.session_state.quiz_index += 1
                st.rerun()
                
        # Render exit dialog button
        render_exit_button()

# ----------------- MODE: SPELLING TYPING PRACTICE -----------------
elif st.session_state.mode == "⌨️ 日⇛英 スペル練習":
    current_index = st.session_state.quiz_index
    total_q = len(st.session_state.quiz_words)
    
    if current_index >= total_q:
        st.success(f"🎉 練習完了！スコア: {st.session_state.quiz_score} / {total_q}")
        if st.button("学習トップに戻る", type="primary", use_container_width=True):
            st.session_state.mode = "TOP"
            st.rerun()
    else:
        st.subheader(f"⌨️ 日⇛英 スペル練習 ({current_index + 1} / {total_q})")
        
        current_word = st.session_state.quiz_words[current_index]
        word_id = current_word["番号"]
        word_eng = current_word["単語"]
        word_pos = current_word["品詞"]
        word_meaning = current_word["訳語"]
        
        # Clean answer for spelling matching
        correct_spelling = word_eng.split(' ')[0]
        correct_spelling_clean = re.sub(r"[^a-zA-Z\s'-]", "", correct_spelling).strip()
        
        # Draw question card
        st.markdown(f'''
        <div class="flashcard">
            <div class="flashcard-pos">[{word_pos}] (No. {word_id})</div>
            <div class="flashcard-eng" style="color: #ff6e40; font-size: 32px;">{word_meaning}</div>
            <div style="font-size: 20px; font-weight: bold; color: #555555; margin-top: 10px;">
                ヒント ({st.session_state.spell_difficulty}): {get_spelling_hint(word_eng, st.session_state.spell_difficulty)}
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Main text input field for typing answer
        user_input = st.text_input(
            "英単語を入力してください:",
            key=f"spell_input_{current_index}",
            placeholder="ここに英単語を入力してEnterを押してください",
            disabled=st.session_state.answer_checked
        )
        
        # Automatic JavaScript Focus Lock on input load
        if not st.session_state.answer_checked:
            inject_focus_script(current_index)
            
        # Check answer if user pressed Enter
        if user_input and not st.session_state.answer_checked:
            user_answer_clean = user_input.strip().lower()
            correct_clean = correct_spelling_clean.lower()
            
            st.session_state.answer_checked = True
            st.session_state.user_typed = user_input.strip()
            
            if user_answer_clean == correct_clean:
                st.session_state.quiz_score += 1
                st.session_state.is_correct = True
                add_overcome(st.session_state.user_id, word_id)
                # Play Base64 Chime sound
                sound_html = f'<audio autoplay src="data:audio/wav;base64,{CHIME_B64}"></audio>'
                st.components.v1.html(sound_html, height=0)
            else:
                st.session_state.is_correct = False
                add_weakness(st.session_state.user_id, word_id)
                # Play Base64 Buzzer sound
                sound_html = f'<audio autoplay src="data:audio/wav;base64,{BUZZER_B64}"></audio>'
                st.components.v1.html(sound_html, height=0)
                st.rerun()
                
        # Show evaluation feedback screen
        if st.session_state.answer_checked:
            # Automatic Female Neural speech playback on showing result
            clean_speech_word = word_eng.split(' ')[0]
            clean_speech_word = re.sub(r"[^a-zA-Z\s'-]", "", clean_speech_word).strip()
            if st.session_state.speech_enabled:
                speech_js = f'''
                <script>
                try {{
                    var msg = new SpeechSynthesisUtterance("{clean_speech_word}");
                    msg.lang = "en-US";
                    msg.rate = 0.95;
                    msg.pitch = 1.0;
                    var voices = window.speechSynthesis.getVoices();
                    var femaleVoice = null;
                    for (var i = 0; i < voices.length; i++) {{
                        var v = voices[i];
                        var name = v.name.toLowerCase();
                        if (v.lang.toLowerCase().includes("en")) {{
                            if (name.includes("natural") || name.includes("neural") || name.includes("aria") || name.includes("jenny") || name.includes("samantha")) {{
                                femaleVoice = v;
                                break;
                            }}
                        }}
                    }}
                    if (femaleVoice) msg.voice = femaleVoice;
                    window.speechSynthesis.speak(msg);
                }} catch(err) {{}}
                </script>
                '''
                st.components.v1.html(speech_js, height=0)
                
            if st.session_state.is_correct:
                st.success(f"⭕ 正解！「{word_eng}」")
            else:
                st.error(f"❌ 不正解！ あなたの入力: {st.session_state.user_typed} (正解: {word_eng})")
                
            # Keep manual voice repetition button for spelling feedback
            manual_speech_js = f'''
            <script>
            try {{
                var msg = new SpeechSynthesisUtterance("{clean_speech_word}");
                msg.lang = "en-US";
                msg.rate = 0.95;
                msg.pitch = 1.0;
                var voices = window.speechSynthesis.getVoices();
                var femaleVoice = null;
                for (var i = 0; i < voices.length; i++) {{
                    var v = voices[i];
                    var name = v.name.toLowerCase();
                    if (v.lang.toLowerCase().includes("en")) {{
                        if (name.includes("natural") || name.includes("neural") || name.includes("aria") || name.includes("jenny") || name.includes("samantha")) {{
                            femaleVoice = v;
                            break;
                        }}
                    }}
                }}
                if (femaleVoice) msg.voice = femaleVoice;
                window.speechSynthesis.speak(msg);
            }} catch(err) {{}}
            </script>
            '''
            if st.button("🔊 正解の音声を聞く", use_container_width=True):
                st.components.v1.html(manual_speech_js, height=0)
                
            if st.button("次の問題に進む ➡️", type="primary", use_container_width=True):
                st.session_state.answer_checked = False
                st.session_state.quiz_index += 1
                st.rerun()
                
        # Render exit dialog button
        render_exit_button()
