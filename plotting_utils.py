import matplotlib.pyplot as plt
# Plotting
from matplotlib.markers import MarkerStyle
from PIL import Image

def save_image(image, url='../images/', name = 'default'):
    image.savefig(url + name)
#    Image.open(url + name + '.png').convert('L').save(url + name + '.png')
    
def plot_image(x, results, title="title", ylim = [0, 1.02], xlim = [2, 50.5], 
               colors="rgbmyc", file_name="name", labels=[], ylabel = "ylabel", 
               loc="better", markers=".,ov<>"):
    plt.figure(figsize=(14,13))
    plt.ylim(ylim)
    plt.xlim(xlim)
    plt.xlabel("Misclassification Cost Ratio")
    plt.ylabel(ylabel)
    plt.style.use('paper.mplstyle')
    
    filled_markers = ('<', 'D', 'o', '>', '|', 'v', 'p', 'd') #' '^', ', '>', '8', 's', 'p', '*', 'h', 'H', , 'd')
    fillstyles = ('full', 'full', 'full', 'full', 'top', 'none')
    colors = "rgbk"

    i = 0
    for record in results:
        model_name = record[1] + "-" + record[2]
        plt.plot(x, record[0], label=model_name, c=colors[i])
        marker = MarkerStyle(marker='o', fillstyle=fillstyles[i])
        plt.scatter(x, record[0], marker=marker, s=300, c=colors[i]) #, label=model_name)
        i+=1
    
    plt.xticks(x, labels, rotation='vertical')
    plt.legend(loc=loc, prop={'size':30})

    save_image(plt,'../images/', file_name)
    plt.show()