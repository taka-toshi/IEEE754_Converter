import math
import struct

import numpy as np
import pandas as pd
import pyperclip
import streamlit as st
import sympy


# 10進数の数字をIEEE754形式のバイナリに変換する関数
def decimal_to_binary(decimal):
    return bin(struct.unpack('!Q', struct.pack('!d', decimal))[0])[2:].zfill(64)

# バイナリを16進数に変換する関数
def binary_to_hex(binary):
    return hex(int(binary, 2))

# IEEE754形式のバイナリを10進数の数字に変換する関数
def binary_to_decimal(binary):
    if len(binary) != 64:
        raise ValueError("Binary string must be 64 bits (8 bytes).")
    decimal = struct.unpack('!d', struct.pack('!Q', int(binary, 2)))[0]
    return decimal

# メイン部分
st.title('IEEE754 Converter')
st.markdown('#### 10進数の数字・数式(int,float型を返す式)を入力してください。')
n = st.text_input('ex. math.pi * ((1e-2)+(2**3)/0.3)*0.1', value=0.1,
                  help="pythonのeval関数に対応しています。\n\n"
                  +"math,numpy,pandasモジュールの使用が可能です。\n\n"
                  + "例：float(math.pi * np.sin(0.5) * pd.DataFrame([1,2,3]).sum())") # float(np.sum(np.full(10, 0.1)))

# nの式を計算する
n = str(n)
n = n.replace(' ', '')
try:
    en = eval(n)
    if type(en) != float and type(en) != int:
        st.error(type(en))
        raise ValueError('計算式が正しくありません。')
except:
    st.error('計算式が正しくありません。')
    st.stop()

s = decimal_to_binary(en)
s1 = s
s2 = s

st.write('変換結果')
s1 = '&ensp;'.join([s1[i:i + 4] for i in range(0, len(s1), 4)])
st.write(s1, unsafe_allow_html=True)

# s1 を16進数で表現
s3 = binary_to_hex(s2)
s3 = s3[2:] # s3から 0xを削除
s3 = ' &ensp;&ensp;&ensp; '.join([s3[i:i + 1] for i in range(0, len(s3), 1)])
s3 = '&ensp;&ensp;&ensp;' + s3 + '&ensp;&ensp;&ensp;'
st.write(s3, unsafe_allow_html=True)

c1 , c2 = st.columns(2)
copy = c1.button('クリップボードにコピー')
if copy:
    pyperclip.copy(s)
    c2.info('クリップボードにコピーしました。')

# 区切り線
st.markdown('***')
st.markdown('#### IEEE754形式のバイナリを入力してください。')

b = st.text_input('ex. 0011111110111001100110011001100110011001100110011001100110011010', value=s)

replace_list = [' ',' ','　',' ']
for r in replace_list:
    b = b.replace(r, '')

st.write('変換結果')
try:
    d = binary_to_decimal(str(b))
    st.write(str(d))
except:
    st.error('Binary string must be 64 bits (8 bytes).')


# nの式を正確に計算する sympyを使う
try:
    n = sympy.sympify(n) # 数式を計算
    v1 = n.evalf() # 浮動小数点数に変換
except:
    v1 = 0.1

st.write('上記の変換結果と一致するか確認します。')
ans = st.text_input('答えを入力してください。', value=str(v1),
                    help="式でも構いませんが、計算結果が一致するか確認することを目的としているため、オススメしません。\n\n"
                   + "pythonのeval関数に対応しています。\n\n"
                  +"math,numpy,pandasモジュールの使用が可能です。\n\n")
try:
    ans = eval(ans)
    if type(ans) != float and type(ans) != int:
        st.error(type(ans))
        raise ValueError('計算式が正しくありません。')
except:
    st.error('計算式が正しくありません。')
    st.stop()
evaluation = eval(str(d)+"=="+str(ans))
st.write(evaluation)