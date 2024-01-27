import matplotlib.pyplot as plt
import numpy as np


def show(results):
    for r in results:      

        im_array = r.plot(line_width=3)  # plot a BGR numpy array of predictions
        
        plt.figure(figsize=(14,5))
        plt.suptitle('Comptage de planches')
        
        plt.subplot(1,2,1)
        plt.imshow(np.flip(im_array, axis=-1)) #np.flip(im_array, axis=-1) to correct colors
        plt.text(0, -50, f"Nombre de planches: {r.__len__()}")
        
        # On crée le np.array col0à3 coordonnées de la box, 4 et 5 milieu de chaque box, 6:confidence level
        coord = np.array(r.boxes.xyxy)
        coord = np.column_stack((coord, (coord[:,0]+coord[:,2])/2,
                                 (coord[:,1]+coord[:,3])/2,np.array(r.boxes.conf)))
        
        for i,c in enumerate(coord):
            plt.text(x=c[4], y=c[5], s=i+1)

        plt.subplot(1,2,2)
        plt.plot(coord[:,6], marker='o')
        plt.xlabel('numéro de box')
        plt.ylabel('Confidence')
        plt.grid()
        plt.savefig('./predict_image.JPG')