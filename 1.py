import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
from pathlib import Path
import PySimpleGUI as psg
right_click_menu = ['', ['Copy', 'Paste', 'Select All', 'Cut']]


matplotlib.use('TkAgg')

def make_figure(): # 初始化条用
    global  x,y
    global fig
    x = np.arange(0, 3, .01)
    y = 2 * np.sin(2 * np.pi * x)
    max_index = np.argmax(y)
    min_index = np.argmin(y)
    fig = plt.figure(facecolor="lightgray",figsize=(4, 3), dpi=100)
   
    plt.grid(True)

    plt.title(u"matplot 测试")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.plot(x,y)
    # 用来正常显示中文标签
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 用来正常显示负号
    plt.rcParams['axes.unicode_minus'] = False

    return fig

""" fig1 = matplotlib.figure.Figure(figsize=(4, 3), dpi=40)
fig2 = matplotlib.figure.Figure(figsize=(4, 3), dpi=40)
fig3 = matplotlib.figure.Figure(figsize=(4, 3), dpi=40) """
fig1=make_figure()
fig2=make_figure()
fig3=make_figure()
#fig1.add_subplot(111).plot(0, 0)
#fig2.add_subplot(111).plot(x, y)
def plot_curve(fig):
    x = np.arange(0, 3, .01)
    y = np.arange(0, 3, .01)
    ax=fig.add_axes([0,0,1,1])
    ax.plot(x,y)

def draw_figure(canvas, figure):
   tkcanvas = FigureCanvasTkAgg(figure, canvas)
   tkcanvas.draw()
   tkcanvas.get_tk_widget().pack(side='top', fill='both', expand=1)
   return tkcanvas


t1 = psg.Input(visible=False, enable_events=True, key='-C1-', font=('Arial Bold', 10), expand_x=True)

frame_layout1=sg.Column([[t1,sg.FileBrowse('Curve1',file_types=(("TXT Files", "*.txt"), ("ALL Files", "*.*"))),sg.Button('Select1')],
   [sg.Canvas(key='-F-')]])
frame_layout2=sg.Column([[sg.FileBrowse('Curve2',file_types=(("TXT Files", "*.txt"), ("ALL Files", "*.*"))),sg.Button('Select2')],
   [sg.Canvas(key='-Qe-')]])
frame_layout3=sg.Column([[sg.FileBrowse('Curve3',file_types=(("TXT Files", "*.txt"), ("ALL Files", "*.*"))),sg.Button('Select3')],
   [sg.Canvas(key='-M-')]])
                                   
layout = [[frame_layout1,frame_layout2,frame_layout3],
          [sg.Text('Select',key='-OUT-')]
          ]
  
window = sg.Window('Matplotlib In PySimpleGUI', layout, size=(800, 600), finalize=True, element_justification='left', font='Helvetica 10')

# add the plot to the window
tkcanvas = draw_figure(window['-F-'].TKCanvas, fig1)
tkcanvas = draw_figure(window['-Qe-'].TKCanvas, fig2)
tkcanvas = draw_figure(window['-M-'].TKCanvas, fig3)
while True:  # Event Loop
    event, values = window.read()       # can also be written as event, values = window()

    if event == 'Select1':
      window['-OUT-'].update('dddddddd')
    if event == '-C1-':
      file = open(t1.get())
      txt = file.read()                
      #fig3.add_subplot(111).plot(0, 0)
    plot_curve(fig3)
    tkcanvas = draw_figure(window['-M-'].TKCanvas, fig3)      
    if event is None or event == 'Exit':
        break
window.close()