//import axios
import axios from 'axios';

const Api = axios.create({
    //set default endpoint API (bisa diganti lewat VITE_API_URL)
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3000'
})

//mode demo (GitHub Pages): backend disimulasikan di browser, lihat services/mockApi.js
if (import.meta.env.VITE_DEMO === 'true') {
    const { default: mockAdapter } = await import('./mockApi.js');
    Api.defaults.adapter = mockAdapter;
}

export default Api
