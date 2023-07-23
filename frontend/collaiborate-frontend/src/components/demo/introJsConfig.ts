export const introJsConfig = {
    steps: [
        {
            title: 'Welcome!',
            intro: `Let's quickly walk through the most important aspects of this Explorer.`
        },
        {
            element: '#parallel-lines-component',
            title: 'Global neighborhood stability plot',
            intro: `
            This is the visualization we developed within the story, now you can try for yourself! You can select samples by brushing over the axis.     
            <video autoplay loop width="400">
                <source type="video/mp4" src="/videos/parallelLineVideo.mp4">
            </video>                  
            `
        },
        {
            element: '#scatter-plot-component',
            title: 'Projection View',
            position: 'top',
            intro: `
            Here we provide a UMAP projection of the 10.000 samples that are also shown in the global neighborhood stability plot. 
            You can navigate it as follows:
            
            <ul>
                <li>
                    Select Items by pressing <span class="key">⇧ Shift</span> and brush:
                    <video autoplay loop width="300">
                        <source type="video/mp4" src="/videos/scatterVideo.mp4">
                    </video>  
                </li>
                <li> 
                    Pan and zoom to explore the visualization:
                    <video autoplay loop width="300">
                        <source type="video/mp4" src="/videos/scatter2Video.mp4">
                    </video> 
                </li>
                     
            </ul>
            `
        },
        {
            element: '#samples-component',
            title: '',
            intro: "Your selected samples will be displayed here for inspection."
        },
        {
            element: '#samples-component > div:first-child',
            title: '',
            intro: "Click onto a sample to switch to the local view for this instance."
        },
        {
            element: '#projection-dropdown',
            title: 'Select a projection',
            intro: `Here you can choose between the representation used for the UMAP projection:
            <ul>
                <li>input - Uses the pixel values of each sketch</li>
                <li>last conv layer - the intermediate representations before being fed to the linear layers</li>
                <li>output - the 15 dimensional output of the network (without softmax)</li>                     
            </ul>
            `
        },
        {
            element: '#analysis-type-dropdown',
            title: 'Enrich the sample with an explanation',
            intro: "We offer some basic explainability methods on a per sample basis, that will be computed on demand."
        },
        {
            element: '#color-strategy-dropdown',
            title: 'Select color scheme',
            intro: `The samples in the projection can be colored by the following strategies:
            <ul>
                <li>by_class - using the class labels for coloring the samples</li>
                <li>by_prediction - using the predicted label for coloring the samples</li>
                <li>true/false - blue if the prediction matches the label, red otherwise</li>                     
            </ul>
            `
        },
        {
            element: '#label-dropdown',
            title: 'Filter dataset',
            intro: "You can subset the data to a specific class label."
        },
        {
            element: '#prediction-dropdown',
            title: 'Filter dataset',
            intro: "Or subset by the prediction the model has made."
        },
        {
            element: '#reset-button',
            title: 'Reset',
            intro: "Here, you can reset the sub-setting and show the whole dataset again."
        },
    ],
    tooltipClass: 'customTooltip',
    dontShowAgain: true,
}

export const localViewIntroJsConfig = {
    steps: [
        {
            element: '#local-view-menu',
            title: 'Jump to layer',
            intro: `
            Select the intermediate representation used in the visualization.
            `
        },{
            element: '#local-view-layer-pin',
            title: 'Set reference layer',
            intro: `
            The pin indicates relative to which layer the change in distance is computed.              
            `
        },{
            element: '#local-view-subset-brush',
            title: 'Subset the samples',
            intro: `
            You can subset samples depending on their change in distance by using this brush chart.    
            `
        },{
            element: '#leave-local-view-button',
            title: 'Leave',
            intro: `
            Once you are done, you can leave the local view here.              
            `
        },
    ],
    tooltipClass: 'customTooltip',
    dontShowAgain: true,
}