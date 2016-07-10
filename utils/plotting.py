import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
from PIL import Image
from utils import labels, axis_costs, cxlim


def _save_image(image, url='../images/', name = 'default'):
    image.savefig(url + name)
#    Image.open(url + name + '.png').convert('L').save(url + name + '.png')
    
def plot_image(results, title="title", ylim = [0, 1.1], 
               colors="rgbmyc", file_name="name", ylabel = "ylabel", 
               loc="better", markers=".,ov<>", save=True):

    label_names = []
    filled_markers = ('<', 'D', 'o', '>', '|', 'v', 'p', 'd') #' '^', ', '>', '8', 's', 'p', '*', 'h', 'H', , 'd')
    fillstyles = ('full', 'full', 'full', 'full', 'full', 'none')
    colors = "rgbyk"

    plt.figure(figsize=(14,13))
    plt.ylim(ylim)
    plt.xlim(cxlim)
    plt.xlabel("Misclassification Cost Ratio")
    plt.ylabel(ylabel)
    plt.style.use('paper.mplstyle')

    i = 0
    for record in results:
        if record[1] == "Baseline":
            model_name = record[1]
        else:
            if record[2] == "Combination":
                model_name = "UniBigrams" + "-" + record[1]
            else:
                model_name = record[2] + "-" + record[1]
        label_names.append(model_name)
        marker = MarkerStyle(marker='o', fillstyle=fillstyles[i])
        plt.scatter(axis_costs, record[0], marker=marker, s=300, c=colors[i])
        plt.plot(axis_costs, record[0], label=model_name, c=colors[i])
        i+=1
    
    plt.xticks(axis_costs, labels, rotation='vertical')
    plt.legend(loc=loc, labels=label_names ,prop={'size':30})

    if save == True:
        _save_image(plt,'../images/', file_name)
        
    plt.show()