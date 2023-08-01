import os,copy,cv2,shutil

##论文中比较重要的图
T0=['Flow chart','Algorithm','Block diagram']
##可以做animation的图
T1=['Tables','Scatter plot','Pie chart','Graph plots','Bar plots','Box plot','Histogram','Confusion matrix']
##常见的实验结果图
T2=['Medical images','Natural images','3D objects','Tree Diagram','Venn Diagram']
##少见的实验结果图
T3=['Area chart','Bubble Chart','Contour plot','Geographic map','Heat map','Mask','Pareto charts','Polar plot','Radar chart','Sketches','Surface plot','Vector plot']


def select_for_presentation(input_dir,output_dir,figure_type_list,image_files,pre_dir):
    # print(figure_type_list)
    # print(image_files)
    t0,t1,t2,t3=[],[],[],[]
    out_list=[]
    for i in range(len(figure_type_list)):
        if figure_type_list[i] in T0:t0.append(image_files[i])
        elif figure_type_list[i] in T1:t1.append(image_files[i])
        elif figure_type_list[i] in T2:t2.append(image_files[i])
        elif figure_type_list[i] in T3:t3.append(image_files[i])
    tmp=select_in_t(t0,input_dir)
    out_list+=tmp
    tmp=select_in_t(t1,input_dir)
    # print(tmp)
    out_list+=tmp
    if len(out_list)<3:
        tmp=select_in_t(t2,input_dir)
        out_list+=tmp
        if len(out_list)<3:
            tmp=select_in_t(t3,input_dir)
            out_list+=tmp
    for file in out_list:
        # print(output_dir)
        gif=f"{output_dir}/{file}_animation.gif"
        if os.path.exists(gif):
            dst = f"{pre_dir}/{file}_animation.gif"
            shutil.copy(gif,dst)
        else:
            src = f"{input_dir}/{file}"
            dst = f"{pre_dir}/{file}"
            # print(src)
            # print(dst)
            shutil.copy(src,dst)
    
def select_in_t(t,input):
    if len(t)==1 or len(t)==2 or len(t)==0: return t
    size_list=[]
    for img_path in t:
        img=cv2.imread(os.path.join(input,img_path))
        size_list.append(img.shape[0]*img.shape[1])
    max1,max2,pos1,pos2=-1,-1,-1,-1
    for i in range(len(size_list)):
        if size_list[i]>max1:
            max1,pos1=size_list[i],i
    for i in range(len(size_list)):
        if size_list[i]>max2 and size_list[i]!=max1:
            max2,pos2=size_list[i],i
    # print(pos1,pos2)
    if pos1!=-1 and pos2!=-1:
        return [t[pos1],t[pos2]]
    elif pos2==-1: return [t[pos1]]
    