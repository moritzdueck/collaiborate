import {createApp} from 'vue'
import './style.css'
import App from './App.vue'
import PrimeVue from 'primevue/config';
import Button from 'primevue/button';
import MultiSelect from "primevue/multiselect";

import Dropdown from 'primevue/dropdown';
import "primevue/resources/themes/lara-light-blue/theme.css";
//import 'primevue/resources/themes/lara-light-teal/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';
import SplitterPanel from "primevue/splitterpanel";
import Splitter from "primevue/splitter";
import Slider from "primevue/slider";

const app = createApp(App)
app.use(PrimeVue);
app.component('Button', Button);
app.component('Dropdown', Dropdown);
app.component('MultiSelect', MultiSelect);
app.component('Splitter', Splitter);
app.component('SplitterPanel', SplitterPanel);
app.component('Slider', Slider);

app.mount('#app')