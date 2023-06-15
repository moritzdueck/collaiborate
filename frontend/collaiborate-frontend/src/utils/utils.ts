export const layers = [
    {value: 0, label: "Input", type: 'input', color: "var(--yellow)"},
    {value: 1, label: "(0): Conv2d", type: 'convolution', color: "var(--purple)"},
    {value: 2, label: "(1): ReLU", type: 'relu', color: "var(--teal)"},
    {value: 3, label: "(2): MaxPool2d", type: 'max-pooling', color: "var(--orange)"},
    {value: 4, label: "(3): Conv2d", type: 'convolution', color: "var(--purple)"},
    {value: 5, label: "(4): ReLU", type: 'relu', color: "var(--teal)"},
    {value: 6, label: "(5): MaxPool2d", type: 'max-pooling', color: "var(--orange)"},
    {value: 7, label: "(6): Conv2d", type: 'convolution', color: "var(--purple)"},
    {value: 8, label: "(7): ReLU", type: 'relu', color: "var(--teal)"},
    {value: 9, label: "(8): MaxPool2d", type: 'max-pooling', color: "var(--orange)"},
    {value: 10, label: "(9): Flatten", type: 'flatten', color: "var(--blue)"},
    {value: 11, label: "(10): Linear", type: 'linear', color: "var(--red)"},
    {value: 12, label: "(11): ReLU", type: 'relu', color: "var(--teal)"},
    {value: 13, label: "(12): Linear", type: 'linear', color: "var(--red)"},
]

export const classes = ['airplane', 'apple', 'bee', 'car', 'dragon', 'mosquito', 'moustache', 'mouth', 'pear', 'piano', 'pineapple', 'smiley face', 'train', 'umbrella', 'wine bottle']

export const samples: { [key: number]: { label: string } } = {
    110635: {
        label: "car",
    },
    101647: {
        label: "wine bottle",
    },
    272791: {
        label: "bee",
    },
    271551: {
        label: "mosquito",
    },
    185767: {
        label: "pineapple",
    },
    146028: {
        label: "airplane",
    },
    115656: {
        label: "train",
    },
}


export function getLayerInfo(index: number) {
    return layers.find(layer => layer.value === index)
}

const apiUrl = import.meta.env.VITE_APIURL

export function getNeighborhoodForSample(index: number){

    if(Object.keys(samples).includes(""+index)){
        return fetch("src/assets/precomputed/" + index + '.json?json')
    }
    return fetch(apiUrl + "neighborhood/" + index)
}