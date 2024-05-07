#学習に用いるパラメーターを設定する
#学習に用いるデータの種類・ファイル名を決定する

#0505現在　データは　
#27*7　150フレーム で構成
#最親ディレクトリMREの下にdatasetがありそこに
#{モーション名}/{モーション名}N.txt
#N=ファイル番号　0からスタート



#ここにモーション名ライブラリを作成 key=motion名 val=ファイル数
fp="../dataset/"
motions={
    0:"walk",
    1:"suburi",
    2:"udehuri"
}


#学習パラメータ
learn_par={
    "Lnum_s":0, #学習の添え字スタート　この値を含む添え字から
    "Lnum_e":10,#この値の添え字(含まない)までを読み込み
    "Tnum_s":10,#テストの添え字スタート　この値を含む添え字から
    "Tnum_e":15,#この値の添え字(含まない)までを読み込み
    "fra_s":0,  #使用するフレームのスタート
    "fra_e":120, #使用するフレームのエンド
    "fra_seq":20,#セクションのフレーム数
}