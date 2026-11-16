//import SidebarMenu dan helper avatar
import SidebarMenu, { initials, currentUser } from '../../../components/SidebarMenu';

//import hook react
import { useState, useEffect } from 'react';

//import Link dari react router dom
import { Link } from 'react-router-dom';

//import js cookie
import Cookies from 'js-cookie'

//import services api
import api from '../../../services/api';

//baca waktu kedaluwarsa token JWT (bagian payload, tanpa verifikasi)
function tokenExpiry(token) {
    try {
        const payload = JSON.parse(atob(token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')));
        return payload.exp ? new Date(payload.exp * 1000) : null;
    } catch {
        return null;
    }
}

export default function Dashboard() {

    //data user yang sedang login (dari cookie)
    const [user] = useState(currentUser);

    //data users dari API
    const [users, setUsers] = useState(null);
    const [error, setError] = useState('');

    const expiry = tokenExpiry(Cookies.get('token') || '');
    const today = new Date().toLocaleDateString('id-ID', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });

    useEffect(() => {
        //ambil daftar user untuk ringkasan
        api.defaults.headers.common['Authorization'] = Cookies.get('token');
        api.get('/api/admin/users')
            .then((response) => setUsers(response.data.data))
            .catch((err) => {
                setUsers([]);
                setError(err.response?.data?.message || 'Gagal memuat data user');
            });
    }, []);

    const minutesLeft = expiry ? Math.max(0, Math.round((expiry - Date.now()) / 60000)) : null;

    return (
        <div className="container mt-4 mb-5">
            <div className="row g-4">
                <div className="col-lg-3">
                    <SidebarMenu />
                </div>
                <div className="col-lg-9">

                    <div className="dash-hero mb-4">
                        <div className="avatar lg">{initials(user?.name)}</div>
                        <div style={{ position: 'relative', zIndex: 1 }}>
                            <p className="small mb-1">{today}</p>
                            <h4>Selamat Datang, {user?.name} 👋</h4>
                            <p>Senang melihatmu lagi. Berikut ringkasan aplikasimu hari ini.</p>
                        </div>
                        <div className="ms-auto">
                            <Link to="/admin/users/create" className="btn btn-light-soft"><i className="bi bi-person-plus me-1"></i>Tambah user</Link>
                        </div>
                    </div>

                    {error && <div className="alert alert-warning alert-soft"><i className="bi bi-exclamation-triangle-fill"></i>{error}. Coba logout lalu login kembali.</div>}

                    <div className="row g-3 mb-4">
                        <div className="col-sm-6 col-xl-4">
                            <div className="stat-card"><div className="ic ic-indigo"><i className="bi bi-people-fill"></i></div>
                                <div><p className="lbl">Total user</p>{users === null ? <div className="skeleton" style={{ width: 40, height: 24 }}></div> : <p className="val">{users.length}</p>}</div></div>
                        </div>
                        <div className="col-sm-6 col-xl-4">
                            <div className="stat-card"><div className="ic ic-sky"><i className="bi bi-envelope-fill"></i></div>
                                <div><p className="lbl">Akun kamu</p><p className="val sm">{user?.email}</p></div></div>
                        </div>
                        <div className="col-sm-12 col-xl-4">
                            <div className="stat-card"><div className="ic ic-emerald"><i className="bi bi-shield-check"></i></div>
                                <div><p className="lbl">Sesi login (JWT)</p>
                                    <p className="val sm">{expiry ? `Berakhir ${expiry.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })} · ${minutesLeft} menit lagi` : 'Aktif'}</p></div></div>
                        </div>
                    </div>

                    <div className="row g-3">
                        <div className="col-md-7">
                            <div className="panel">
                                <div className="panel-head"><h6>User terbaru</h6><Link to="/admin/users">Lihat semua <i className="bi bi-arrow-right"></i></Link></div>
                                {users === null && [1, 2, 3].map((i) => <div key={i} className="user-row"><div className="avatar sm" style={{ opacity: .3 }}></div><div className="flex-grow-1"><div className="skeleton mb-2" style={{ width: '50%' }}></div><div className="skeleton" style={{ width: '70%' }}></div></div></div>)}
                                {users?.length === 0 && !error && <p className="text-muted mb-0">Belum ada user.</p>}
                                {users?.slice(0, 5).map((u) => (
                                    <div key={u.id} className="user-row">
                                        <div className="avatar sm">{initials(u.name)}</div>
                                        <div className="flex-grow-1"><b>{u.name}{u.id === user?.id && <span className="badge text-bg-light ms-2">Kamu</span>}</b><span>{u.email}</span></div>
                                        <Link to={`/admin/users/edit/${u.id}`} className="btn btn-sm btn-light rounded-3" aria-label={`Edit ${u.name}`}><i className="bi bi-pencil"></i></Link>
                                    </div>
                                ))}
                            </div>
                        </div>
                        <div className="col-md-5">
                            <div className="panel">
                                <div className="panel-head"><h6>Aksi cepat</h6></div>
                                <div className="d-grid gap-2">
                                    <Link to="/admin/users/create" className="quick"><div className="stat-card p-0 shadow-none" style={{ height: 'auto' }}><div className="ic ic-indigo"><i className="bi bi-person-plus-fill"></i></div></div><div><b>Tambah user</b><span>Buat akun baru</span></div><i className="bi bi-arrow-right"></i></Link>
                                    <Link to="/admin/users" className="quick"><div className="stat-card p-0 shadow-none" style={{ height: 'auto' }}><div className="ic ic-amber"><i className="bi bi-table"></i></div></div><div><b>Kelola user</b><span>Ubah atau hapus user</span></div><i className="bi bi-arrow-right"></i></Link>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    )
}
