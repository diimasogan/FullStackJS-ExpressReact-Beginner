//import hook react
import React, { useState } from "react";

//import hook useNavigate dan Link dari react router dom
import { useNavigate, Link } from "react-router-dom";

//import services api
import api from '../../services/api'

//import layout dan helper error field
import AuthLayout, { FieldError, fieldError } from '../../components/AuthLayout';

//indikator kekuatan password sederhana (hanya tampilan, aturan server tetap minimal 6 karakter)
function passwordStrength(pw) {
    let score = 0;
    if (pw.length >= 6) score++;
    if (pw.length >= 10) score++;
    if (/[A-Z]/.test(pw) && /[a-z]/.test(pw)) score++;
    if (/\d/.test(pw) && /[^A-Za-z0-9]/.test(pw)) score++;
    return [
        { w: '0%', c: '#e2e8f0', t: '' },
        { w: '25%', c: '#ef4444', t: 'Weak' },
        { w: '50%', c: '#f59e0b', t: 'Fair' },
        { w: '75%', c: '#22c55e', t: 'Strong' },
        { w: '100%', c: '#16a34a', t: 'Very strong' },
    ][pw ? Math.max(score, 1) : 0];
}

export default function Register() {

    //navigate
    const navigate = useNavigate();

    //define state
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);

    //define state validation
    const [validation, setValidation] = useState([]);

    //function "register"
    const register = async (e) => {
        e.preventDefault();
        setLoading(true);

        //call api register
        await api.post('/api/register', {
            name: name,
            email: email,
            password: password,
        })
            .then(() => {

                //redirect ke halaman login (bawa email agar langsung terisi)
                navigate("/login", { state: { registered: true, email } });
            })
            .catch(error => {

                //assign error to state "validation"
                setValidation(error.response.data);
            })
            .finally(() => setLoading(false));
    };

    const strength = passwordStrength(password);
    const nameError = fieldError(validation, 'name');
    const emailError = fieldError(validation, 'email');
    const passwordError = fieldError(validation, 'password');

    return (
        <AuthLayout title="Create an account ✨" subtitle="It’s free and takes less than a minute.">

            {validation.message && !validation.errors && (
                <div className="alert alert-danger alert-soft"><i className="bi bi-x-circle-fill"></i>{validation.message}</div>
            )}

            <form onSubmit={register} noValidate>
                <div className="mb-3">
                    <label htmlFor="name">Full name</label>
                    <div className="input-icon">
                        <i className="bi bi-person"></i>
                        <input id="name" type="text" autoComplete="name" value={name} onChange={(e) => setName(e.target.value)}
                            className={`form-control ${nameError ? 'is-invalid' : ''}`} placeholder="Full name" />
                    </div>
                    <FieldError message={nameError} />
                </div>

                <div className="mb-3">
                    <label htmlFor="email">Email</label>
                    <div className="input-icon">
                        <i className="bi bi-envelope"></i>
                        <input id="email" type="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)}
                            className={`form-control ${emailError ? 'is-invalid' : ''}`} placeholder="name@email.com" />
                    </div>
                    <FieldError message={emailError} />
                </div>

                <div className="mb-4">
                    <label htmlFor="password">Password</label>
                    <div className="input-icon">
                        <i className="bi bi-lock"></i>
                        <input id="password" type={showPassword ? 'text' : 'password'} autoComplete="new-password" value={password} onChange={(e) => setPassword(e.target.value)}
                            className={`form-control ${passwordError ? 'is-invalid' : ''}`} placeholder="At least 6 characters" />
                        <button type="button" className="toggle-pw" onClick={() => setShowPassword(!showPassword)} aria-label={showPassword ? 'Hide password' : 'Show password'}>
                            <i className={`bi ${showPassword ? 'bi-eye-slash' : 'bi-eye'}`}></i>
                        </button>
                    </div>
                    <div className="pw-meter"><i style={{ width: strength.w, background: strength.c }}></i></div>
                    {password && <small style={{ color: strength.c, fontWeight: 600 }}>{strength.t}</small>}
                    <FieldError message={passwordError} />
                </div>

                <button type="submit" className="btn btn-primary btn-auth w-100" disabled={loading}>
                    {loading ? <><span className="spinner-border spinner-border-sm me-2"></span>Creating account…</> : <>SIGN UP <i className="bi bi-arrow-right ms-1"></i></>}
                </button>
            </form>

            <p className="auth-switch">Already have an account? <Link to="/login">Log in here</Link></p>
        </AuthLayout>
    )
}
