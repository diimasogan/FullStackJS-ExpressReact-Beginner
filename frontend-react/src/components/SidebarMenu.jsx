//import NavLink dan useNavigate dari react router dom
import { NavLink, useNavigate } from "react-router-dom";

//import hook react
import React, { useContext } from "react";

// import Cookies from js-cookie
import Cookies from 'js-cookie'

//import context
import { AuthContext } from '../context/AuthContext';

//inisial nama untuk avatar
export const initials = (name = '') => name.trim().split(/\s+/).slice(0, 2).map((w) => w[0]?.toUpperCase()).join('') || '?';

//ambil data user yang sedang login dari cookie
export const currentUser = () => {
    try { return JSON.parse(Cookies.get('user') || '{}'); } catch { return {}; }
};

export default function SidebarMenu() {

    // Menggunakan hook `useNavigate` untuk navigasi
    const navigate = useNavigate();

    //destructure context "setIsAuthenticated"
    const { setIsAuthenticated } = useContext(AuthContext);

    const user = currentUser();

    // method to handle logout
    const logout = () => {

        //remove token and user on cookies
        Cookies.remove('token');
        Cookies.remove('user');

        //assign false to state "isAuthenticated"
        setIsAuthenticated(false);

        // redirect to login
        navigate("/login", { replace: true });
    }

    return (
        <div className="side-card">
            <div className="side-user">
                <div className="avatar">{initials(user.name)}</div>
                <div><b>{user.name || 'User'}</b><span>{user.email}</span></div>
            </div>
            <div className="side-title">Main menu</div>
            <nav className="side-nav">
                <NavLink to="/admin/dashboard"><i className="bi bi-grid-1x2"></i>Dashboard</NavLink>
                <NavLink to="/admin/users"><i className="bi bi-people"></i>Users</NavLink>
                <a onClick={logout} className="logout" role="button"><i className="bi bi-box-arrow-right"></i>Logout</a>
            </nav>
        </div>
    )
}
