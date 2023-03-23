from flask import Flask, Response, request, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import io
import torch
import pandas as pd
from captum.attr import Occlusion
from backend import classes, get_model, get_grad_cam_model

app = Flask(__name__, static_folder='./frontend-build/dist/',  static_url_path='/')
api = Api(app)

val_data = np.load("val_data.npy", allow_pickle=True)

model = get_model()
grad_model = get_grad_cam_model()
occlusion = Occlusion(model)
umap_df = pd.read_csv("./umap_extended.csv")
matplotlib.use('SVG')


class UmapProjection(Resource):

    def __init__(self, **kwargs):
        self.df = kwargs['umap_df']

    def get(self, length):
        return list(self.df
                    .apply(lambda x: {'x': x[1], 'y': x[2], 'c': x[3], 'c_hat': x[5], 'id': x[0]}, axis=1))[0:length]


class UmapProjectionXY(Resource):

    def __init__(self, **kwargs):
        self.df = kwargs['umap_df']

    def get(self, length, xmin=-1, xmax=-1, ymin=-1, ymax=-1):
        return list(self.df
                    [(self.df.x > xmin) & (self.df.x < xmax) & (self.df.y > ymin) & (self.df.y < ymax)]
                    .apply(lambda x: {'x': x[1], 'y': x[2], 'c': x[3], 'c_hat': x[5], 'id': x[0]}, axis=1))[0:length]


class UmapProjectionFiltered(Resource):

    def __init__(self, **kwargs):
        self.df = kwargs['umap_df']

    def get(self, restricted_classes, length):
        filter_to_classes = list(map(lambda n: int(n), restricted_classes.split('-')))
        print(self.df.shape)
        return list(
            filter(
                lambda x: x['c'] in filter_to_classes,
                list(self.df.apply(lambda x: {'x': x[1], 'y': x[2], 'c': x[3], 'c_hat': x[5], 'id': x[0]}, axis=1))
            )
        )[0:length]


class UmapProjectionCL(Resource):

    def __init__(self, **kwargs):
        self.df = kwargs['umap_df']

    def get(self, length):
        return list(self.df
                    .apply(lambda x: {'x': x[7], 'y': x[8], 'c': x[3], 'c_hat': x[5], 'id': x[0]}, axis=1))[0:length]


class UmapProjectionCLFiltered(Resource):

    def __init__(self, **kwargs):
        self.df = kwargs['umap_df']

    def get(self, restricted_classes, length):
        filter_to_classes = list(map(lambda n: int(n), restricted_classes.split('-')))
        print(self.df.shape)
        return list(
            filter(
                lambda x: x['c'] in filter_to_classes,
                list(self.df.apply(lambda x: {'x': x[7], 'y': x[8], 'c': x[3], 'c_hat': x[5], 'id': x[0]}, axis=1))
            )
        )[0:length]


class SketchMetadata(Resource):
    def get(self, sketch_index):
        x = val_data[sketch_index][0]
        logits = model(torch.tensor(x).unsqueeze(1))
        y_hat = np.argmax(logits.detach().numpy())
        return {
            'label': classes[val_data[sketch_index][1]],
            'prediction': classes[y_hat]
        }


@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()


@app.route("/sketch/png/<int:sketch_index>")
def get_sketch(sketch_index):
    fig = plt.figure()
    plt.tight_layout()
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(val_data[sketch_index][0].reshape(28, 28, 1), cmap='Greys')
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return Response(buf, mimetype='image/png')


@app.route("/sketch/probs/<int:sketch_index>")
def get_probs(sketch_index):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 10))

    x = val_data[sketch_index][0]
    logits = model(torch.tensor(x).unsqueeze(1)).detach().numpy()
    probs = np.exp(logits) / np.exp(logits).sum()
    probs = probs[0]

    # ax2.set_ylim(0, 1)
    # ax2.bar(range(len(probs)), probs, tick_label=classes)
    # ax2.set_xticklabels(classes, rotation=90)
    ax1.set_axis_off()
    ax2.set_axis_off()

    ax2.imshow(x.reshape(28, 28, 1), cmap='Greys')

    top_pred = np.argsort(probs)

    ax1.text(0, 0.8, classes[top_pred[-1]] + ": " + "{:.2f}".format(probs[top_pred[-1]] * 100) + "%", fontsize=25)
    ax1.text(0, 0.65, classes[top_pred[-2]] + ": " + "{:.2f}".format(probs[top_pred[-2]] * 100) + "%", fontsize=25)
    ax1.text(0, 0.5, classes[top_pred[-3]] + ": " + "{:.2f}".format(probs[top_pred[-3]] * 100) + "%", fontsize=25)
    ax1.text(0, 0.35, classes[top_pred[-4]] + ": " + "{:.2f}".format(probs[top_pred[-4]] * 100) + "%", fontsize=25)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return Response(buf, mimetype='image/png')


@app.route("/sketch/vg/<int:sketch_index>")
def get_vg(sketch_index):
    x = torch.Tensor(val_data[sketch_index][0])
    x.requires_grad_()
    x_batch = x.unsqueeze(dim=0)
    logits = model(x_batch)
    logits_idx = logits.argmax()
    logits_max = logits[0, logits_idx]

    # compute gradients
    logits_max.backward()

    # plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 10))
    ax1.imshow(x.grad.reshape(28, 28, 1), cmap='Greys')
    ax1.set_axis_off()
    ax2.imshow(x.reshape(28, 28, 1).detach(), cmap='Greys')
    ax2.set_axis_off()

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return Response(buf, mimetype='image/png')


@app.route("/sketch/gradcam/<int:sketch_index>")
def get_grad_cam(sketch_index):
    x = torch.Tensor(val_data[sketch_index][0])
    x.requires_grad_()
    x_batch = x.unsqueeze(dim=0)
    logits = grad_model(x_batch)

    pred = logits.max()
    pred.backward()

    y_hat = np.argmax(logits.detach())

    gradients = grad_model.get_activations_gradient()
    pooled_gradients = torch.mean(gradients, dim=[0, 2, 3])
    activations = grad_model.get_activations(x_batch).detach()
    for i in range(32):
        activations[:, i, :, :] *= pooled_gradients[i]

    heatmap = torch.mean(activations, dim=1).squeeze()
    heatmap = np.maximum(heatmap, 0)
    heatmap /= torch.max(heatmap)

    fig, ax1 = plt.subplots(1, 1, figsize=(5, 5))
    ax1.imshow(x.reshape(28, 28, 1).detach(), cmap='Greys')
    ax1.set_axis_off()

    xmin, xmax = ax1.get_xlim()
    ymin, ymax = ax1.get_ylim()

    ax1.imshow(heatmap.squeeze(), cmap='Reds', interpolation='nearest', alpha=.5, extent=(xmin, xmax, ymin, ymax))
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return Response(buf, mimetype='image/png')


@app.route("/sketch/occlusion/<int:sketch_index>")
def get_occlusion(sketch_index):
    x = torch.Tensor(val_data[sketch_index][0])
    x.requires_grad_()
    x_batch = x.unsqueeze(dim=0)
    logits = model(x_batch)
    y_hat = np.argmax(logits.detach())

    # apply method
    attributions1 = occlusion.attribute(x_batch, target=y_hat.item(), sliding_window_shapes=(1, 3, 3))

    # plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 10))
    ax1.imshow(attributions1.squeeze().reshape(28, 28, 1), cmap='Greens', vmin=0, vmax=1)
    ax1.set_axis_off()

    ax2.imshow(x.reshape(28, 28, 1).detach(), cmap='Greys')
    ax2.set_axis_off()

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return Response(buf, mimetype='image/png')


@app.route('/')
def index():
    return app.send_static_file('index.html')


api.add_resource(SketchMetadata, "/sketch/<int:sketch_index>")

api.add_resource(UmapProjection,
                 "/umap/<int:length>",
                 resource_class_kwargs={'umap_df': umap_df})
api.add_resource(UmapProjectionXY,
                 "/umap/<int:length>/<float(signed=True):xmin>/<float(signed=True):xmax>/<float(signed=True):ymin>/<float(signed=True):ymax>",
                 resource_class_kwargs={'umap_df': umap_df})
api.add_resource(UmapProjectionCL, "/umap-cl/<int:length>", resource_class_kwargs={'umap_df': umap_df})
api.add_resource(UmapProjectionFiltered,
                 "/umap_filtered/<string:restricted_classes>/<int:length>",
                 resource_class_kwargs={'umap_df': umap_df})
api.add_resource(UmapProjectionCLFiltered,
                 "/umap-cl_filtered/<string:restricted_classes>/<int:length>",
                 resource_class_kwargs={'umap_df': umap_df})

cors = CORS(app, origins="*")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)