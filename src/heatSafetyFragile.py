#!/usr/bin/env/python3

import cv2
import numpy as np
import skimage.exposure



class heatMapper():
    
    def __init__(self):


        self.normal_img = None
        self.depth_img = None
        self.edge_img = None
        self.seg_img = None
        self.caustic_img = None

        # Threshold for seg mask
        self.thres = 80

        # Main path; path_to_ws: workspace locationa and img_files: 'GeometricalObjsBottle', 'MergedRGB', 'MultipleObjs'.
        self.main_path = 'path_to_ws/RiskTerrainModeling/Dataset/img_files/' #TODO 

        # images folder
        self.normal_folder = 'Normal/'
        self.depth_folder = 'Depth/'
        self.seg_folder = 'Seg/'
        self.heat_folder = 'Output/Heat/'
        self.caustic_folder = 'Picture_Caustic/'
        
        self.type = '.png'

        self.map_3D_xyz = None
        self.n = 5 # neibours to consider during stride

    def clean_id(self):

        self.normal_img = None
        self.depth_img = None
        self.edge_img = None
        self.seg_img = None
        self.caustic_img = None
        self.map_3D_xyz = None
        
    def routine(self):

        # Final heat
        self.heat_img = self.normal_img.copy()

        self.interpollateAreas()


        # create mask based on Seg img
        mask = self.seg_img > self.thres
        # make obj. boundaries red in the heat img
        self.heat_img[mask] = [0, 0, 255]

        # create mask based on Caustic img
        mask_2 = self.caustic_img > self.thres
        # make obj. boundaries red in the heat img
        self.heat_img[mask_2] = [0, 0, 255]

        #cv2.imshow('heat_img', self.heat_img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

    # Calculate the x, y, z world cordinate of each pixel
    def convert3D_xyz(self, depth_img):
        
        self.map_3D_xyz = np.empty([3,depth_img.shape[0], depth_img.shape[1]])
        for v in range(depth_img.shape[0]):
            for u in range(depth_img.shape[1]):
                Z = depth_img[v, u] / self.factor
                X = (u - self.cx) * Z / self.fx
                Y = ( v - self.cy) * Z /self.fy
                self.map_3D_xyz[:,v, u] = [X, Y, Z] 

    def calc_normal_xyz(self):

        height = self.map_3D_xyz.shape[0]
        width = self.map_3D_xyz.shape[1]
        pts_3d_world=self.map_3D_xyz.copy()

        f= pts_3d_world[:,1:height-1,2:width]-pts_3d_world[:,1:height-1,1:width-1]
        t= pts_3d_world[:,2:height,1:width-1]-pts_3d_world[:,1:height-1,1:width-1]
        normal_map=np.cross(f,t,axisa=0,axisb=0)
        normal_map = normal_map/np.linalg.norm(normal_map) 

        cv2.imshow('Normal Map', normal_map)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def applyNoise(self):

        random_img = self.img.copy()
        width = random_img.shape[0]
        heigh = random_img.shape[1]
        for w in range(width//2):
            for h in range(heigh//2):
                random_img[w,h] += np.random.randint(0,20)

        return random_img
    
    def  interpollateAreas(self):

        # detect suface difference
        # TODO SOS SOS SOS SOS TODO TODO TODO
        # blur or filter or convolve /fix lines verticals 
        pass

        # s = self.heat_img.strides
        # h, w, d = self.heat_img.shape
        # tmp = np.lib.stride_tricks.as_strided(self.heat_img, strides=s[:2] + s,
        #                               shape=(h , w , self.n, self.n, d)) #- self.n + 1, - self.n + 1
        # s = self.heat_img.strides
        # h, w, d = self.heat_img.shape
        # tmp = np.lib.stride_tricks.as_strided(self.heat_img, strides=s[:2] + s,
        #                               shape=(h , w , self.n, self.n, d)) #- self.n + 1, - self.n + 1


        for h in range(self.heat_img.shape[0] - self.n ):
            for w in range(self.heat_img.shape[1]- self.n ):

                box = self.heat_img[h: h + self.n, w :w + self.n, :]
                
                v0 = np.var(box[:,:,0])
                v1 = np.var(box[:,:,1])
                v2 = np.var(box[:,:,2])
                if v0 != 0:
                    self.heat_img[h,w,0] = self.heat_img[h,w,0]*v0/100
                if v1 != 0:
                    self.heat_img[h,w,1] = self.heat_img[h,w,1]*v1/100
                if v2 != 0:
                    self.heat_img[h,w,2] = self.heat_img[h,w,2]*v2/100       

        np.where(self.heat_img > 255, 255, self.heat_img)

def main():

    # create HeatMap object for specific img 
    hm = heatMapper()

    # make it in loop later
    for i in range(0,2403): #TODO set number of images id

        id = str(i)
        
        # read image
        hm.depth_img = cv2.imread(hm.main_path + hm.depth_folder + id + hm.type, cv2.IMREAD_ANYDEPTH)
        hm.normal_img = cv2.imread(hm.main_path + hm.normal_folder + id + hm.type, cv2.IMREAD_COLOR)
        hm.seg_img = cv2.imread(hm.main_path + hm.seg_folder + id + hm.type, cv2.IMREAD_GRAYSCALE)
        hm.caustic_img = cv2.imread(hm.main_path + hm.caustic_folder + id + hm.type, cv2.IMREAD_GRAYSCALE)

        # main routine process for heatmapping
        hm.routine()

        # save result of heatmap
        cv2.imwrite(hm.main_path + hm.heat_folder + id + hm.type, hm.heat_img)

        # clean images relevant to id
        hm.clean_id()

if __name__ == '__main__':
    try: 
        main()
    except Exception as e:
        print(e)
          
