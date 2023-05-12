import numpy as np
import matplotlib.pyplot as plt
import glob as gb
import os as os
import ast
const_str_area_file_name = 'area.txt'
const_str_execute_folder_path = 'C:/Users/Yu_Hwanjeong/Desktop/doing/課題/2023/01 研究室関連/07 研究-Pt修飾Ni水素発生/02 Ni単結晶のCV/0511-Ni/'

color_dict = {'ayumu':'#ED7D95','kasumi':'#E7D600','shizuku':'#01B7ED','karin':'#485EC6',
              'ai':'#FF5800','kanata':'#A664A0','setsuna':'#D8172F','emma':'#84C36E',
              'rina':'#9CA5B9','shioriko':'#37B484','mia':'#D6D5CA','lanzhu':'#F8C8C4',
              'yu':'#1D1D1D'} # 色指定(ニジガク)

plt.rcParams["font.family"] = "Times New Roman"     # 使用するフォント
plt.rcParams["font.size"] = 40                      #フォントサイズ
plt.rcParams["mathtext.fontset"] = "stix"           #使用する数学用フォント
plt.figure(figsize = (14, 9))                       #グラフのサイズを指定
plt.subplots_adjust(left=0.10, right=0.97, bottom=0.11, top=0.95) #ここまではグラフの条件指定

def drawing(x_list, y_list, str_color_name, str_lbl):
    plt.plot(x_list, y_list, color = color_dict[str_color_name], label = str_lbl)

def file_reading(str_folder_path, str_file_name): #ファイルから電位、電流をリストとして抽出する関数
    str_full_path = str_folder_path + str_file_name
    with open(str_full_path) as f:
        list_lines = f.readlines()
        int_row_num = list_lines.index("Potential/V, Current/A\n") + 1
    list_E, list_J = np.loadtxt(str_full_path, skiprows = int_row_num, delimiter = ',', unpack = True)
    return (list_E, list_J)

def area_file_generator(str_folder_path): #面積辞書ファイル生成（フォルダごとに一回実行し、手動で書き換えること）
    #Pathにarea.txt生成、手動で内容を書き換える必要あり。    
    list_file_name = os.listdir(str_folder_path)
    try:
        list_file_name.remove(const_str_area_file_name)
    except:
        pass
    
    dic_output = {} #金属名リスト
    for filename in list_file_name:
        if os.path.splitext(filename) [1] == '.txt':
            dic_output[filename] = 0.05 #金属名辞書にファイル名と基本面積のリスト追加
            print(filename + '発見')
    with open(str_folder_path + '/' + const_str_area_file_name, 'w+') as f:
        f.write(str(dic_output))
        f.close()
    print(str_folder_path + '/' + const_str_area_file_name + 'に出力されました！')

def area_file_reader(str_folder_path, str_file_name): #面積辞書から面積を数値で返還する関数
    str_area_file_path = str_folder_path + '/' + const_str_area_file_name
    dic_read = open(str_area_file_path, 'r')
    dic_area = ast.literal_eval(dic_read.read())
    f_area = float(dic_area[str_file_name])
    return (f_area)

def measure_condition_reader(str_folder_path, str_file_name): #測定条件の辞書と文字列を返還する関数
    str_full_path = str_folder_path + str_file_name
    with open(str_full_path) as f:
        lines = f.readlines()
        list_row_num = [i for i, line_s in enumerate(lines) if "Init E (V)" in line_s or "Sensitivity (A/V)" in line_s]
        int_start_row_num = list_row_num[0]                     
        int_end_row_num = list_row_num[1]
        conditions = lines[int_start_row_num : int_end_row_num + 1] #測定条件の行のリストを作成
        conditions = [[y.strip() for y in x.split("=")] for x in conditions] #"="で測定条件の要素を分割してリストを作成
        dict_cond = dict(conditions)                    #測定条件のリストを辞書にする
    str_cond = ""
    for i in dict_cond.keys():
        str_cond = str_cond + str(i) + " : " + str(dict_cond[i]) + "\n"
    return(dict_cond, str_cond)
    
def draw_file_range(str_folder_path, str_file_name, int_start, int_end, str_color_name, str_lbl):
    str_area_file_path = str_folder_path + '/' + const_str_area_file_name
    plt.xlabel("$E$ / V (v.s RHE)")
    plt.ylabel("$j$ / µA cm$^{-2}$")

    list_E, list_J = file_reading(str_folder_path, str_file_name)
    list_E = list_E[int_start:int_end]
    list_J = list_J[int_start:int_end]
    dic_read = open(str_area_file_path, 'r')
    dic_area = ast.literal_eval(dic_read.read())
    f_area = float(dic_area[str_file_name])
    list_J = list_J/f_area*1000000

    drawing(list_E, list_J, str_color_name, str_lbl)

def draw_whole_file(str_folder_path, str_file_name, str_color_name, str_lbl):
    plt.xlabel("$E$ / V (v.s RHE)")
    plt.ylabel("$j$ / µA cm$^{-2}$")

    list_E, list_J = file_reading(str_folder_path, str_file_name)
    f_area = area_file_reader(str_folder_path, str_file_name)
    list_J = list_J/f_area*1000000

    drawing(list_E, list_J, str_color_name, str_lbl)
                 
def find_all_J_by_V(str_folder_path, str_file_name, f_voltage): # 測定値中電位値と同一な電流密度を見せる関数
    list_E, list_J = file_reading(str_folder_path, str_file_name)
    f_area = area_file_reader(str_folder_path, str_file_name)
    list_position = np.where(list_E == f_voltage)[0]
    list_outputJ = list_J[list_position]/f_area
    matrix_output = np.concatenate([list_position,list_outputJ],0)
    print(matrix_output)
