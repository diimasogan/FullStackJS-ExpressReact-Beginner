//Banner yang hanya tampil pada build demo (GitHub Pages)
import { resetDemoData } from '../services/mockApi';
import Cookies from 'js-cookie';

const DOCS = 'https://diimasogan.github.io/FullStackJS-ExpressReact-Beginner/docs/';

export default function DemoBanner() {
    const reset = async () => {
        await resetDemoData();
        Cookies.remove('token');
        Cookies.remove('user');
        window.location.href = import.meta.env.BASE_URL;
    };

    return (
        <div className="alert alert-warning border-0 rounded-0 mb-0 py-2 small">
            <div className="container d-flex flex-wrap gap-2 align-items-center">
                <span className="badge text-bg-dark">MODE DEMO</span>
                <span>Backend Express disimulasikan di browser. Login: <code>admin@demo.com</code> / <code>password</code></span>
                <span className="ms-auto d-flex gap-2">
                    <button type="button" onClick={reset} className="btn btn-sm btn-outline-dark py-0">Reset data</button>
                    <a href={DOCS} className="btn btn-sm btn-outline-dark py-0">Dokumentasi</a>
                    <a href="https://github.com/diimasogan/FullStackJS-ExpressReact-Beginner" className="btn btn-sm btn-dark py-0">Kode</a>
                </span>
            </div>
        </div>
    );
}
