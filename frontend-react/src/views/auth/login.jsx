//import hook react
import React, { useState, useContext } from "react";

//import hook useNavigate dan Link dari react router dom
import { useNavigate, useLocation, Link } from "react-router-dom";

//import services api
import api from '../../services/api'

//import js cookie
import Cookies from 'js-cookie'

//import context
import { AuthContext } from '../../context/AuthContext';

//import layout dan helper error field
import AuthLayout, { FieldError, fieldError } from '../../components/AuthLayout';

export default function Login() {

    //navigate
    const navigate = useNavigate();

    //data dari halaman register (jika baru saja mendaftar)
    const location = useLocation();
    const justRegistered = location.state?.registered;

    //destructure context "setIsAuthenticated"
    const { setIsAuthenticated } = useContext(AuthContext);

    //define state
    const [email, setEmail] = useState(location.state?.email || "");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);

    //define state validation
    const [validation, setValidation] = useState([]);
    const [loginFailed, setLoginFailed] = useState([]);

    //function "login"
    const login = async (e) => {
        e.preventDefault();
        setLoading(true);

        //call api login
        await api.post('/api/login', {
            email: email,
            password: password,
        })
            .then(response => {

                //set token dan user ke cookie
                Cookies.set('token', response.data.data.token);
                Cookies.set('user', JSON.stringify(response.data.data.user));

                //assign true ke state "isAuthenticated"
                setIsAuthenticated(true);

                //redirect ke dashboard
                navigate("/admin/dashboard", { replace: true });
            })
            .catch(error => {

                //assign error ke state "validation" dan "loginFailed"
                setValidation(error.response.data);
                setLoginFailed(error.response.data);
            })
            .finally(() => setLoading(false));
    };

    //isi akun demo (hanya pada build demo)
    const fillDemo = () => {
        setEmail('admin@demo.com');
        setPassword('password');
    };

    const emailError = fieldError(validation, 'email');
    const passwordError = fieldError(validation, 'password');

    return (
        <AuthLayout title="Selamat datang kembali 👋" subtitle="Masuk untuk membuka dashboard admin.">

            {justRegistered && !loginFailed.message && (
                <div className="alert alert-success alert-soft"><i className="bi bi-check-circle-fill"></i>Registrasi berhasil. Silakan login dengan akun barumu.</div>
            )}

            {loginFailed.message && !loginFailed.errors && (
                <div className="alert alert-danger alert-soft"><i className="bi bi-x-circle-fill"></i>{loginFailed.message}</div>
            )}

            {import.meta.env.VITE_DEMO === 'true' && (
                <div className="demo-hint">
                    <span><i className="bi bi-info-circle me-1"></i>Akun demo: <code>admin@demo.com</code> / <code>password</code></span>
                    <button type="button" onClick={fillDemo} className="btn btn-sm btn-primary rounded-3">Isi otomatis</button>
                </div>
            )}

            <form onSubmit={login} noValidate>
                <div className="mb-3">
                    <label htmlFor="email">Email</label>
                    <div className="input-icon">
                        <i className="bi bi-envelope"></i>
                        <input id="email" type="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)}
                            className={`form-control ${emailError ? 'is-invalid' : ''}`} placeholder="nama@email.com" />
                    </div>
                    <FieldError message={emailError} />
                </div>

                <div className="mb-4">
                    <label htmlFor="password">Password</label>
                    <div className="input-icon">
                        <i className="bi bi-lock"></i>
                        <input id="password" type={showPassword ? 'text' : 'password'} autoComplete="current-password" value={password} onChange={(e) => setPassword(e.target.value)}
                            className={`form-control ${passwordError ? 'is-invalid' : ''}`} placeholder="Minimal 6 karakter" />
                        <button type="button" className="toggle-pw" onClick={() => setShowPassword(!showPassword)} aria-label={showPassword ? 'Sembunyikan password' : 'Tampilkan password'}>
                            <i className={`bi ${showPassword ? 'bi-eye-slash' : 'bi-eye'}`}></i>
                        </button>
                    </div>
                    <FieldError message={passwordError} />
                </div>

                <button type="submit" className="btn btn-primary btn-auth w-100" disabled={loading}>
                    {loading ? <><span className="spinner-border spinner-border-sm me-2"></span>Memproses…</> : <>LOGIN <i className="bi bi-arrow-right ms-1"></i></>}
                </button>
            </form>

            <p className="auth-switch">Belum punya akun? <Link to="/register">Daftar sekarang</Link></p>
        </AuthLayout>
    )
}
