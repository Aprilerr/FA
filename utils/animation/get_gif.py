import numpy as np
import cv2
import imageio.v2 as imageio
import random



def animation_select(image,box_list,figure_type):
    if figure_type=='Scatter plot':
        return scatter_animation(image,box_list)
    elif figure_type=='Pie chart':
        return pie_animation(image,box_list)
    elif figure_type=='Graph plots':
        return line_animation(image,box_list)
    elif figure_type=='Bar plots' or figure_type=='Box plot' or figure_type=='Histogram':
        return bar_animation(image,box_list)
    elif figure_type=='Confusion matrix':
        return matrix_animation(image,box_list)


def pie_animation(image,bounding_box_list): #pie animation
    num=36
    box_list,img_list=[],[]
    for box in bounding_box_list:
        x, y, x1, y1 = box
        x,y,x1,y1 = int(x),int(y),int(x1),int(y1)
        a,b=int((x1+x)/2),int((y1+y)/2)
        w,h=a-x,b-y
        box_list.append([x,y,x1,y1,w,h,a,b])
    for i in range(num):
        for box in box_list:
            cv2.ellipse(image,(box[6],box[7]),(box[4],box[5]),0,i*10,(i+1)*10,(255,255,255),-1)
        image_io_img = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)
        img_list.insert(0,image_io_img)
    return img_list

def line_animation(image,bounding_box_list):#line animation
    num=20
    box_list,img_list=[],[]
    for box in bounding_box_list:
        x, y, x1, y1 = box
        x,y,x1,y1 = int(x),int(y),int(x1),int(y1)
        w,h =x1 -x,y1-y
        box_list.append([x,y,x1,y1,w,h])
    for i in range(num):
        for box in box_list:
            dw,dh=int(box[4]*(i+1)/num),int(box[5]*(i+1)/num)
            cv2.rectangle(image,(box[2]-dw,box[1]),(box[2],box[3]),(255,255,255), -1)
        image_io_img = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)
        img_list.insert(0,image_io_img)
    return img_list

def scatter_animation(image,bounding_box_list): #scatter plot animation
    print("Get pixels list")
    img = image
    img_list,pixel_list=[],[]
    # 遍历图像像素
    height, width = img.shape[:2]
    for y in range(height):
        for x in range(width):
            # 获取像素值
            pixel = img[y, x]
            if set(pixel)==set([0,0,0]) or set(pixel)==set([255,255,255]):
                continue
            else:
                pixel_list.append([y,x])
    print("Get frames.")
    random.shuffle(pixel_list)
    num=20
    pixel_list_len=len(pixel_list)
    for i in range(num):
        for index in range(int(i*pixel_list_len/20),int((i+1)*pixel_list_len/20)):
            if index>=pixel_list_len: continue
            y,x=pixel_list[index][0],pixel_list[index][1]
            img[y,x]=[255,255,255]
        image_io_img = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        img_list.insert(0,image_io_img)
    return img_list

def matrix_animation(image,bounding_box_list):#confusion matrix animation
    num=20
    box_list,img_list=[],[]
    for box in bounding_box_list:
        x, y, x1, y1 = box
        x,y,x1,y1 = int(x),int(y),int(x1),int(y1)
        w,h =x1 -x,y1-y
        box_list.append([x,y,x1,y1,w,h])
    for i in range(num):
        for box in box_list:
            dw,dh=int(box[4]*(i+1)/num),int(box[5]*(i+1)/num)
            cv2.rectangle(image,(box[2]-dw,box[3]-dh),(box[2],box[3]),(255,255,255), -1)
        image_io_img = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)
        img_list.insert(0,image_io_img)
    return img_list


def bar_animation(image,bounding_box_list):#bar animation
    img_list=[]
    for box in bounding_box_list:
        x, y, x1, y1 = box
        x,y,x1,y1 = int(x),int(y),int(x1),int(y1)
        # Draw a filled rectangle on the image
        cv2.rectangle(image, (x, y), (x1, y1), (255,255,255), -1)
        image_io_img = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)
        img_list.insert(0,image_io_img)
    return img_list


def get_gif(file_path,output_dir,figure_type,duration,box_list):
    # print("Load the json file.")
    image = cv2.imread(file_path)
    out_name=file_path.split('/')[-1]
    img_list=[]
    if type(box_list)!=list:
        box_list=list(box_list)
        box_list.sort(key=lambda x:x[0],reverse=True)
    # print("Get frames.")
    img_list=animation_select(image,box_list,figure_type)
    img_list.append(imageio.imread(file_path))
    imageio.mimsave(f"{output_dir}/{out_name}_animation.gif", img_list, duration=duration)
    print("animation.gif has saved.")


