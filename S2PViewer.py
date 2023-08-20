import PySimpleGUI as sg
from win32com import client
import numpy as np 
import math
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import matplotlib.pyplot as plt
# from skrf import Network
import skrf as rf
# import pickle
fontsize=18

# HFSS控制器，代码见前，略
class Handler:
    def __init__(self):
        self.oAnsoftApp = client.Dispatch('AnsoftHfss.HfssScriptInterface')
        self.oDesktop = self.oAnsoftApp.GetAppDesktop()
        self.oProject = self.oDesktop.GetActiveProject()
        self.oDesign = self.oProject.GetActiveDesign()
        self.prj_name = self.oProject.GetName()
        self.des_name = self.oDesign.GetName()
# 回调函数：对应“连接”按钮
def connect():
    global h
    h = Handler()
    #prj_name.set(h.prj_name)
   # des_name.set(h.des_name)
    

def init_figure():

    fig=plt.figure(facecolor ="lightgray",figsize=(12, 8), dpi=80)
    plt.xlabel('Frequency(GHz)',size=fontsize)
    plt.ylabel('Sparameters(dB)',size=fontsize)
    # 用来正常显示中文标签
    plt.rcParams['font.sans-serif'] = ['SimHei'] 
    # 用来正常显示负号 
    plt.rcParams['axes.unicode_minus'] = False  
    return fig

def plot_mag(sp):
    plt.clf()
    # plt.plot(x,y)
    # just plt.draw() won't do it here, strangely
    sp.frequency.unit = 'ghz'
    sp.plot_s_db()
    # sp.plot_s_db(m=0,n=0)    
    plt.xlabel('Frequency(GHz)',size=fontsize)
    plt.ylabel('Sparameters(dB)',size=fontsize)
    plt.rcParams['font.sans-serif'] = ['SimHei'] 
    plt.gcf().canvas.draw()
    return sp

def plot_mags(sps):
    plt.clf()
    # plt.plot(x,y)
    # just plt.draw() won't do it here, strangely
   
    for i in range(len(sps)):
        sps[i].frequency.unit = 'ghz'
        sps[i].plot_s_db(m=1, n=0)
        sps[i].plot_s_db(m=0, n=0)
        
    # sp.plot_s_db(m=0,n=0)    
    plt.xlabel('Frequency(GHz)',size=fontsize)
    plt.ylabel('Sparameters(dB)',size=fontsize)
    plt.rcParams['font.sans-serif'] = ['SimHei'] 
    plt.gcf().canvas.draw()


def plot_smith(sp):
    plt.clf()
    sp.frequency.unit = 'ghz'
    sp.plot_s_smith()     
    plt.rcParams['font.sans-serif'] = ['SimHei'] 
    plt.gcf().canvas.draw()

def plot_gd(sp):
    plt.clf()
    sp.frequency.unit = 'ghz'
    gd21 = abs(sp.s21.group_delay) *1e9
    gd12 = abs(sp.s12.group_delay) *1e9
    # gd11 = abs(sp.s11.group_delay) *1e9
    sp.plot(gd21,label = 'Simulation') 
    sp.plot(gd12)    
    plt.xlabel('Frequency(GHz)',size=fontsize)
    plt.ylabel('Group Delay(ns)',size=fontsize)
    plt.rcParams['font.sans-serif'] = ['SimHei'] 
    plt.gcf().canvas.draw()

def plot_phase(sp):
    plt.clf()
    sp.frequency.unit = 'ghz'
    sp.plot_s_deg() 
    plt.xlabel('Frequency(GHz)',size=fontsize)
    plt.ylabel('Phase(Deg)',size=fontsize)
    plt.rcParams['font.sans-serif'] = ['SimHei'] 
    plt.gcf().canvas.draw()



#画在canvas上，包括工具条
def draw_figure(canvas,canvas_toolbar, figure):
# def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    toolbar = NavigationToolbar2Tk(figure_canvas_agg,canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def delete_figure_agg(figure_canvas_agg):
    figure_canvas_agg.get_tk_widget().forget()
    plt.close('all') 

sg.theme('LightGreen')

t1=sg.T('',key='-TT-', size=(60, 1), justification='left')
c1=sg.Canvas(size=(640,400), key='-CANVAS-')
tool=sg.Canvas(key='-TOOLBAR-')
col1=[[sg.Input(key='-path-',enable_events=True,visible=False), sg.FileBrowse('S2P...',size=(8, 1),key='-OPEN-',file_types=(( "S2P Files", "*.s2p*"),))]]
col2=[[sg.Exit(size=(8, 1))]]

rb = []
rb.append(sg.Radio("MAG", "Response", key='mag',  enable_events=True, default=True))
rb.append(sg.Radio("PHASE", "Response", key='phase', enable_events=True,disabled=True))
rb.append(sg.Radio("GD", "Response", key='gd', enable_events=True,disabled=True))
rb.append(sg.Radio("SMITH", "Response", key='smith', enable_events=True,disabled=True))
rb.append(sg.CBox("HOLD", key='hold',  enable_events=True, default=False))
col3=[[sg.Frame("Response Type", [rb], title_color='blue')]]
tl=[[tool]] 

layout=[
        [t1],
        [sg.Column(tl,element_justification='center',expand_x=any)],
        [sg.Column([[c1]],element_justification='center',expand_x=any)],
        [sg.Column(col3,element_justification='center',expand_x=any)],
        [sg.Column(col1,element_justification='center',expand_x=any),sg.Column(col2,element_justification='center',expand_x=any)],
        
    ]

window = sg.Window('S2P Viewer', layout,finalize=True)
window.Refresh()
fig = init_figure()
fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, window['-TOOLBAR-'].TKCanvas,fig)


global sps
sps=[]
# 消息循环
while True:
    event, values = window.read()

        # 
            # filename = 's2p_list.pkl'
            #                                     # 使用pickle模块的dump()函数保存列表内容到指定文件中
            # with open(filename, 'ab') as f: 
            #     pickle.dump(sp, f)
            # with open('s2p_list.pkl', 'rb') as f:
            #     while 1:
            #         try:
            #             one_pickle_data = pickle.load(f)
            #             print(one_pickle_data)
            #         except EOFError:
            #           break
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break

    elif event == '-Button1-':
        connect()
        window['-TT-'].Update(h.des_name)
        

 
    if values['hold']==True:
        path = values['-OPEN-']
        window['-TT-'].Update('')   
        if path != '':
            sp = rf.Network(path) #            
            sps.append(sp)
            plot_mags(sps)
        window['mag'].Update(value=True)
        window['gd'].Update(disabled=True)
        window['smith'].Update(disabled=True)
        window['phase'].Update(disabled=True)
    else:
        path = values['-OPEN-']
        window['-TT-'].Update(path)     
        sp = rf.Network(path)
        plt.clf()
        plot_mag(sp) 
        sps=[]
        window['gd'].Update(disabled=False)
        window['smith'].Update(disabled=False)
        window['phase'].Update(disabled=False)
        
        if event == 'smith':
            sp = rf.Network(path) # 加载s2p文件      
            plot_smith(sp)

        elif event == 'phase':
            sp = rf.Network(path) # 加载s2p文件      
            plot_phase(sp)

        elif event == 'gd':
            sp = rf.Network(path) # 加载s2p文件      
            plot_gd(sp)

        elif event == 'mag':
            sp = rf.Network(path) # 加载s2p文件      
            plot_mag(sp)
    
window.close()