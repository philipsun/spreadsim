import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

from collections import OrderedDict

cmaps = OrderedDict()

cmaps['Perceptually Uniform Sequential'] = [
            'viridis', 'plasma', 'inferno', 'magma', 'cividis']

cmaps['Sequential'] = [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
cmaps['Sequential (2)'] = [
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']
cmaps['Diverging'] = [
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']

cmaps['Cyclic'] = ['twilight', 'twilight_shifted', 'hsv']
cmaps['Qualitative'] = ['Pastel1', 'Pastel2', 'Paired', 'Accent',
                        'Dark2', 'Set1', 'Set2', 'Set3',
                        'tab10', 'tab20', 'tab20b', 'tab20c']
cmaps['Miscellaneous'] = [
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
            'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral',
            'gist_ncar']


def plot_color_gradients(cmap_category, cmap_list, nrows):

    gradient = np.linspace(0, 1, 512)
    print(gradient)
    gradient = np.vstack((gradient, gradient))
    fig, axes = plt.subplots(nrows=nrows)
    fig.subplots_adjust(top=0.95, bottom=0.01, left=0.2, right=0.99)
    axes[0].set_title(cmap_category + ' colormaps', fontsize=14)

    for ax, name in zip(axes, cmap_list):
        ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap(name))
        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.01
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='right', fontsize=10)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axes:
        ax.set_axis_off()
def plotlablecolor(labledict,cmape_name='hsv'):

    colormap_dict=makecolordict(labledict,cmape_name)
    labledict=colormap_dict['labledict']
    coloridxdict = colormap_dict['coloridxdict']
    cmape_name = colormap_dict['cmap']
    fig, ax = plt.subplots()
    i = 0
    legendname = []
    rect_set = []
    rect_set0 = []
    x = 0;y = 50; yt = 51;
    cx = []
    cy = []
    ctxt = []
    cc = []
    cmhot = plt.get_cmap("Spectral")
    plt.set_cmap(cmape_name)
    for k,t in labledict.items():
        cx.append(x)
        cy.append(y)
        cc.append(coloridxdict[k])
        ctxt.append(k)

        ax.text(x, yt,
                k,
                ha='center', va='bottom',rotation=90)
        x = x + 30
    ax.scatter(cx, cy, c=cc, s=20, alpha=0.5)
    plt.show()
def plotcolormapdict(colormap_dict):
    labledict=colormap_dict['labledict']
    coloridxdict = colormap_dict['lablecolor']
    cmape_name = colormap_dict['cmap']
    fig, ax = plt.subplots()
    i = 0
    legendname = []
    rect_set = []
    rect_set0 = []
    x = 0;y = 50; yt = 51;
    cx = []
    cy = []
    ctxt = []
    cc = []
    cmhot = plt.get_cmap("Spectral")
    plt.set_cmap(cmape_name)
    for k,t in labledict.items():
        cx.append(x)
        cy.append(y)
        cc.append(coloridxdict[k])
        ctxt.append(k)

        ax.text(x, yt,
                k,
                ha='center', va='bottom',rotation=90)
        x = x + 30
    ax.scatter(cx, cy, c=cc, s=20, alpha=0.5)
    plt.show()
def testcmap():
    nrows = max(len(cmap_list) for cmap_category, cmap_list in cmaps.items())
    for cmap_category, cmap_list in cmaps.items():
        plot_color_gradients(cmap_category, cmap_list, nrows)

    plt.show()
def showcolormapRGB(cmap_name):
    gradient = np.linspace(0, 1, 256)
    #gradient = np.vstack((gradient, gradient))
    print(gradient.shape)
    rgb = cm.get_cmap(cmap_name)(gradient)[np.newaxis, :, :3]
    print(rgb.shape)
def getrgbfordict(obdict,cmap_name='hsv'):
    n = len(obdict.keys())
    gradient = np.linspace(0, 1, n) #when use 0,1,n, there will be a (1,n) vector to be produced by np.linspace
    rgb = cm.get_cmap(cmap_name)(gradient)[np.newaxis, :, :3]
    i = 0
    for key,ob in obdict.items():
        ob['cololr'] = rgb[1,i,:]
        i = i + 1
    return obdict
def makencolor(n,cmap_name='hsv'):

    gradient = np.linspace(0, 1, n) #when use 0,1,n, there will be a (1,n) vector to be produced by np.linspace
    rgb = cm.get_cmap(cmap_name)(gradient)[np.newaxis, :, :3]
    return rgb
def makecolordict(labledict,cmap_name='hsv'):
    n = len(labledict.keys())
    rgb = makencolor(n,cmap_name)
    lablecolor = {}
    colormap_dict={}
    colormap_dict['cmap']=cmap_name
    colormap_dict['labledict']=labledict
    for k,i in labledict.items():
        c = rgb[0,i,:]
        lablecolor[k]=c
    colormap_dict['lablecolor'] = lablecolor
    return colormap_dict

import sxpReadFileMan
import re
def parsestate(gpat="\'(geo_[a-z_]+)\'",cmape_name='cool'):
    src = sxpReadFileMan.ReadTextUTF('sxpNCPState.py')
    #gpat = "\'(geo_[a-z_]+)\'"
    g=re.findall(gpat,src)
    ug = []
    ugidx = {}
    k = 0
    for i,each in enumerate(g):
        if each in ug:
            continue
        else:
            ug.append(each)
        print(each)
        ugidx[each]=k
        k = k + 1
    geo_colomap=makecolordict(ugidx,cmape_name)
   # plotlablecolor(ugidx,cmape_name='cool')
    return geo_colomap
gv = [
    'geo_free','geo_kanbing','geo_home_geli','geo_zhiliao_zhuyuan','geo_zhiliao_icu','geo_zhiliao_geli','geo_si,geo_icu_si'
]
geo_colomap = parsestate(gpat="\'(geo_[a-z_]+)\'",cmape_name='cool')
health_colomap = parsestate(gpat="\'(health_[a-z_]+)\'",cmape_name='coolwarm')
def getstatdict():
    state_st ={}
    for g,v in geo_colomap['lablecolor'].items():
        state_st[g]=0
    for g,v in health_colomap['lablecolor'].items():
        state_st[g]=0
    return state_st
#plotcolormapdict(health_colomap)

def geostcolor(gv):
    nrgb = np.floor(geo_colomap['lablecolor'][gv] * 255)
    return nrgb
def healthstcolor(hv):
    nrgb = np.floor(health_colomap['lablecolor'][hv]*255)
    return nrgb
def getrandomcolor(cmap_name,n):
    rgb = makencolor(n, cmap_name='hsv')
    nrgb = np.floor(rgb[0,:,:]*255)
    ic = np.random.randint(0,n,1)

    return nrgb[ic,:]
def main():
  #  testcmap()
    showcolormapRGB('hsv')
    print(geostcolor('geo_free'))
    print(healthstcolor('health_ok'))
    for i in range(10):
        print(getrandomcolor('cool',8))
    pass



if __name__ == '__main__':
    main()