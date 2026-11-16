//Layout bersama untuk halaman Login dan Register: panel brand di kiri, form di kanan
export default function AuthLayout({ title, subtitle, children }) {
    return (
        <div className="auth-wrap">
            <div className="auth-card">
                <aside className="auth-brand">
                    <div className="auth-logo"><i className="bi bi-stack"></i>FullStack JS</div>
                    <h2>Full-stack JavaScript with Express &amp; React</h2>
                    <p>One complete project: a REST API, JWT authentication and an admin dashboard to manage users.</p>
                    <ul className="auth-points">
                        <li><i className="bi bi-shield-lock"></i><div><b>Secure JWT login</b><span>Passwords hashed with bcrypt, tokens valid for 1 hour.</span></div></li>
                        <li><i className="bi bi-people"></i><div><b>User management (CRUD)</b><span>Add, edit and delete users from the admin area.</span></div></li>
                        <li><i className="bi bi-check2-circle"></i><div><b>Server-side validation</b><span>express-validator checks every input.</span></div></li>
                    </ul>
                    <div className="auth-stack"><span>React</span><span>Vite</span><span>Express</span><span>Prisma</span><span>MySQL</span></div>
                </aside>
                <section className="auth-form">
                    <h3>{title}</h3>
                    <p className="sub">{subtitle}</p>
                    {children}
                </section>
            </div>
        </div>
    );
}

//Ambil pesan error validasi untuk satu field (format express-validator: { path, msg })
export function fieldError(validation, path) {
    return validation?.errors?.find((e) => e.path === path)?.msg;
}

//Tampilkan pesan error di bawah input
export function FieldError({ message }) {
    if (!message) return null;
    return <div className="field-error"><i className="bi bi-exclamation-circle"></i>{message}</div>;
}
