import argparse
import os,copy,glob,json
import easyocr
from utils.classification.figure_classification import *
from utils.GDINO.groundingdino.util.inference import load_model, load_image, predict, annotate, Model
from utils.animation.get_gif import *
from utils.animation.table_animation import *
from utils.animation.select_presentation import *
from app.config import config



if __name__ == "__main__":
    #Parser
    parser = argparse.ArgumentParser("FIGA", add_help=True)
    ## GSAM
    parser.add_argument("--config_file", type=str, default="utils/GDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py", help="path to config file")
    parser.add_argument("--grounded_checkpoint", default="utils/pretrained_models/GSAM/groundingdino_swint_ogc.pth",type=str, help="path to checkpoint file")
    parser.add_argument("--box_threshold", type=float, default=0.3, help="box threshold")
    parser.add_argument("--text_threshold", type=float, default=0.25, help="text threshold")
    parser.add_argument("--device", type=str, default="cpu", help="running on cpu only!, default=False")
    ##DocFigure classification
    parser.add_argument("--classifier", type=str, default="utils/pretrained_models/classification/epoch_9_loss_0.04706_testAcc_0.96867_X_resnext101_docSeg.pth")
    #animation
    parser.add_argument("--duration", type=int, default=100, help="duration")
    #IO
    parser.add_argument("--input", type=str, required=True, help="path to image file")
    parser.add_argument("--output_dir", type=str, default=config["SYS"]["OUT"], help="output directory")
    parser.add_argument("--presentation_dir", type=str, default=os.path.join(config["SYS"]["OUT"],"presentation"), help="output directory for presentation")
    args = parser.parse_args()

    # make dir
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(args.presentation_dir, exist_ok=True)
    #classification model initial
    fig_model, fig_class_trasform = fig_classification(args.classifier,args.device)
    
    #GDINO initial
    model = load_model(args.config_file, args.grounded_checkpoint, args.device)
    #OCR initial
    reader = easyocr.Reader(['ch_sim','en'],gpu=True)

    #get image path
    image_files = [file for file in os.listdir(args.input) if file.endswith((".jpg", ".png", ".jpeg"))]
    figure_type_list=[]
    #Processing
    for img_path in image_files:
        try:
    #figure type detections
            img_file=os.path.join(args.input,img_path)
            print(f"Processing {img_path}.")
            figure_type=figure_type_detection(fig_model, fig_class_trasform, img_file, args.device)
            figure_type_list.append(figure_type)
            # print(figure_type)
            if figure_type not in ['Tables','Algorithm','Scatter plot','Pie chart','Graph plots','Bar plots','Box plot','Histogram','Confusion matrix']:
                continue
            if figure_type=='Tables' or figure_type=='Algorithm':
                table_gif(img_file,args.duration,reader,args.output_dir)
                continue
            if figure_type=='scatter':
                get_gif(img_file,args.output_dir,figure_type,args.duration,[])
                continue
        #figure obeject detection
            text_prompt = get_prompt(figure_type)
            image_pil, image = load_image(img_file)
            # run grounding dino model
            boxes, logits, phrases = predict(model,image,text_prompt,args.box_threshold,args.text_threshold,args.device)
            detected_boxes=get_box(image_pil,copy.deepcopy(boxes))      
            #
            get_gif(img_file,args.output_dir,figure_type,args.duration,detected_boxes)
            #figure animation
        except Exception as e:
            print(e)
            continue
    select_for_presentation(args.input,args.output_dir,figure_type_list,image_files,args.presentation_dir)