import cv2
import imageio.v2 as imageio
import easyocr

def mask_image_with_bounding_box(image, bounding_box):
    # Extract the coordinates of the bounding box
    x, y, x1, y1 = bounding_box
    x,y,x1,y1 = int(x),int(y),int(x1),int(y1)
    # Draw a filled rectangle on the image
    cv2.rectangle(image, (x, y), (x1, y1), (255,255,255), -1)
    return image

def ocr_box(img,reader):
    result = reader.readtext(img)
    box_list=[]
    for box in result:
        x1,y1=int(box[0][0][0]),int(box[0][0][1])
        x2,y2=int(box[0][2][0]),int(box[0][2][1])
        box_list.append([x1,y1,x2,y2])
    return box_list

def table_gif(file_path,duration,reader,output_dir):
    print("Get Ocr Box.")
    image = cv2.imread(file_path)
    out_name=file_path.split('/')[-1]
    img_list=[]
    box_list=ocr_box(image,reader)
    box_list.sort(key=lambda x:(x[1],x[2]),reverse=True)
    print("Get frames.")
    for box in box_list:
        image=mask_image_with_bounding_box(image,box)
        image_io_img = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)
        img_list.insert(0,image_io_img)
    img_list.append(imageio.imread(file_path))
    imageio.mimsave(f"{output_dir}/{out_name}_animation.gif", img_list, duration=duration)
    print("animation.gif has saved.")

