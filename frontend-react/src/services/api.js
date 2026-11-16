//import axios
import axios from 'axios';

const Api = axios.create({
    //set default endpoint API (bisa diganti lewat VITE_API_URL)
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3000'
})

//mode demo (GitHub Pages): backend disimulasikan di browser, lihat services/mockApi.js
//modul mock dimuat saat request pertama, sehingga tidak menahan aplikasi saat dimuat
if (import.meta.env.VITE_DEMO === 'true') {
    Api.defaults.adapter = async (config) => {
        const { default: mockAdapter } = await import('./mockApi.js');
        return mockAdapter(config);
    };
}

export default Api
