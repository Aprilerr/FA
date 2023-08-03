from torchvision import models
from PIL import Image
import torch.nn as  nn
import torch
import torchvision.transforms as standard_transforms

mean_std = ( [.485, .456, .406], [.229, .224, .225])
fig_class_trasform = standard_transforms.Compose([
standard_transforms.Resize((384, 384), interpolation=Image.ANTIALIAS),
standard_transforms.ToTensor(),
standard_transforms.Normalize(*mean_std)])

labelNames = ['3D objects',
    'Algorithm',
    'Area chart',
    'Bar plots',
    'Block diagram',
    'Box plot',
    'Bubble Chart',
    'Confusion matrix',
    'Contour plot',
    'Flow chart',
    'Geographic map',
    'Graph plots',
    'Heat map',
    'Histogram',
    'Mask',
    'Medical images',
    'Natural images',
    'Pareto charts',
    'Pie chart',
    'Polar plot',
    'Radar chart',
    'Scatter plot',
    'Sketches',
    'Surface plot',
    'Tables',
    'Tree Diagram',
    'Vector plot',
    'Venn Diagram']


def fig_classification(fig_class_model_path,device):
    fig_model =  models.resnext101_32x8d()
    num_features = fig_model.fc.in_features
    fc = list(fig_model.fc.children()) # Remove last layer
    fc.extend([nn.Linear(num_features, 28)]) # Add our layer with 4 outputs
    fig_model.fc = nn.Sequential(*fc)
    fig_model = fig_model.to(device)
    fig_model.load_state_dict(torch.load(fig_class_model_path, map_location=torch.device('cpu')))
    fig_model.eval()
    mean_std = ( [.485, .456, .406], [.229, .224, .225])
    fig_class_trasform = standard_transforms.Compose([
        standard_transforms.Resize((384, 384), interpolation=Image.ANTIALIAS),
        standard_transforms.ToTensor(),
        standard_transforms.Normalize(*mean_std)         ])
    return fig_model, fig_class_trasform
# For pth
# def figure_type_detection(fig_model, fig_class_trasform, img_path, device):
#     img = Image.open(img_path).convert('RGB')
#     img_tensor = fig_class_trasform(img)
#     fig_label = fig_model(img_tensor.to(device).unsqueeze(0))
#     fig_prediction = fig_label.max(1)[1]
#     out_put =labelNames[fig_prediction]
#     return out_put

# For onnx
def figure_type_detection(fig_ort_session, img_path):
    img = Image.open(img_path).convert('RGB')
    img_tensor = fig_class_trasform(img).unsqueeze(0).numpy()
    ort_inputs={'input':img_tensor}
    fig_label = fig_ort_session.run(['output'], ort_inputs)[0]
    fig_label = torch.tensor(fig_label)
    fig_prediction = fig_label.max(1)[1]
    out_put =labelNames[fig_prediction]
    return out_put

def get_prompt(figure_type):
    if figure_type=='Tables' or figure_type=='Algorithm':
        return figure_type
    elif figure_type=='Scatter plot':
        return "scatter"
    elif figure_type=='Pie chart':
        return "circle"
    elif figure_type=='Graph plots':
        return "line"
    elif figure_type=='Bar plots' or figure_type=='Box plot' or figure_type=='Histogram':
        return "column"
    elif figure_type=='Confusion matrix':
        return "square"
