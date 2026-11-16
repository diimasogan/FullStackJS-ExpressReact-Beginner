"""Build the FullStackJS Express + React documentation (English + Bahasa Indonesia).

Usage:  python3 -I docs/_source/build_docs.py
Writes: docs/FullStackJS-Documentation.html, docs/id/FullStackJS-Dokumentasi.html and docs/index.html

Every text is a pair T(en, id) so both languages always have the same structure.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = {"en": ROOT / "docs" / "FullStackJS-Documentation.html",
       "id": ROOT / "docs" / "id" / "FullStackJS-Dokumentasi.html"}
LINK = {"en": "FullStackJS-Documentation.html", "id": "id/FullStackJS-Dokumentasi.html"}
PORTAL = "https://diimasogan.github.io/FullStackJS-ExpressReact-Beginner/"
REPO = "https://github.com/diimasogan/FullStackJS-ExpressReact-Beginner"
LANG = "en"


class T(tuple):
    def __new__(cls, en, id_=None):
        return super().__new__(cls, (en, en if id_ is None else id_))

    def __str__(self):
        return self[0] if LANG == "en" else self[1]


def s(x):
    return str(x) if isinstance(x, T) else x


# ---------------------------------------------------------------- building blocks
def icon(path):
    return f'<svg class="ico" viewBox="0 0 24 24">{path}</svg>'


ICONS = {
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c.8-3.5 3.6-5.5 7-5.5s6.2 2 7 5.5"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7"/>',
    "doc": '<path d="M4 4h11l5 5v11H4z"/><path d="M15 4v5h5M8 13h8M8 17h5"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
}


def card(ic, title, text, amber=False):
    return (f'<div class="card{" amber" if amber else ""}"><div class="ihead">{icon(ICONS[ic])}<h3>{s(title)}</h3></div>'
            f'<p>{s(text)}</p></div>')


def grid(cards, cols=3):
    return f'<div class="grid g{cols}">{"".join(cards)}</div>'


def table(head, rows):
    h = "".join(f"<th>{s(c)}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{s(c)}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def section(sid, title, body):
    return f'<section id="{sid}"><h2>{s(title)}</h2>{body}</section>'


def stats(items):
    return '<div class="stats">' + "".join(f'<div class="stat"><b>{n}</b><span>{s(t)}</span></div>' for n, t in items) + "</div>"


def ul(items):
    return '<ul class="clean">' + "".join(f"<li>{s(i)}</li>" for i in items) + "</ul>"


# ---------------------------------------------------------------- diagram
def architecture_svg():
    L = lambda en, id_: s(T(en, id_))
    return f"""<figure><svg viewBox="0 0 980 400" role="img" aria-label="{L('Solution architecture','Arsitektur solusi')}">
<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 10 5 0 10z" class="mk"/></marker></defs>
<g class="lane"><rect x="10" y="20" width="300" height="360" rx="14"/><text x="160" y="46" class="lt">Frontend · React + Vite</text></g>
<g class="lane"><rect x="330" y="20" width="400" height="360" rx="14"/><text x="530" y="46" class="lt">Backend · Express (port 3000)</text></g>
<g class="lane"><rect x="750" y="20" width="220" height="360" rx="14"/><text x="860" y="46" class="lt">{L('Data','Data')}</text></g>
<g class="bx"><rect x="30" y="70" width="260" height="56" rx="10"/><text x="160" y="94">{L('Pages (react-router)','Halaman (react-router)')}</text><text x="160" y="113" class="sm">Home · Register · Login · Dashboard · Users</text></g>
<g class="bx hl"><rect x="30" y="146" width="260" height="56" rx="10"/><text x="160" y="170">AuthContext + js-cookie</text><text x="160" y="189" class="sm">{L('token &amp; user stored in cookies','token &amp; user disimpan di cookie')}</text></g>
<g class="bx"><rect x="30" y="222" width="260" height="56" rx="10"/><text x="160" y="246">services/api.js (axios)</text><text x="160" y="265" class="sm">baseURL http://localhost:3000</text></g>
<g class="bx amb"><rect x="30" y="298" width="260" height="56" rx="10"/><text x="160" y="322">mockApi.js · {L('demo only','khusus demo')}</text><text x="160" y="341" class="sm">{L('same rules, runs in the browser','aturan sama, jalan di browser')}</text></g>
<g class="bx"><rect x="350" y="70" width="170" height="56" rx="10"/><text x="435" y="94">routes/index.js</text><text x="435" y="113" class="sm">/api/register · /api/login</text></g>
<g class="bx hl"><rect x="540" y="70" width="170" height="56" rx="10"/><text x="625" y="94">middlewares/auth.js</text><text x="625" y="113" class="sm">{L('verify JWT','verifikasi JWT')}</text></g>
<g class="bx"><rect x="350" y="146" width="360" height="56" rx="10"/><text x="530" y="170">utils/validators · express-validator</text><text x="530" y="189" class="sm">{L('name, e-mail format &amp; uniqueness, password ≥ 6','nama, format &amp; keunikan e-mail, password ≥ 6')}</text></g>
<g class="bx"><rect x="350" y="222" width="360" height="56" rx="10"/><text x="530" y="246">controllers · Register · Login · User</text><text x="530" y="265" class="sm">bcryptjs · jsonwebtoken (1h)</text></g>
<g class="bx"><rect x="350" y="298" width="360" height="56" rx="10"/><text x="530" y="322">Prisma Client</text><text x="530" y="341" class="sm">prisma/schema.prisma · migrations</text></g>
<g class="bx hl"><rect x="770" y="222" width="180" height="56" rx="10"/><text x="860" y="246">MySQL</text><text x="860" y="265" class="sm">db_express · users</text></g>
<g class="bx amb"><rect x="770" y="298" width="180" height="56" rx="10"/><text x="860" y="322">localStorage</text><text x="860" y="341" class="sm">{L('demo data','data demo')}</text></g>
<g class="ln"><path d="M160 126v20M160 202v20" marker-end="url(#ar)"/><path d="M290 250h20v-152h40" marker-end="url(#ar)"/><path d="M520 98h20" marker-end="url(#ar)"/>
<path d="M530 126v20M530 202v20M530 278v20" marker-end="url(#ar)"/><path d="M710 326h20v-76h40" marker-end="url(#ar)"/><path d="M160 278v20" marker-end="url(#ar)"/><path d="M290 326h20v40h440v-12h20" marker-end="url(#ar)"/></g>
</svg><figcaption>{L('Locally the React app calls the Express API on port 3000. In the live demo the same requests are answered by mockApi.js inside the browser.','Di lokal, aplikasi React memanggil API Express di port 3000. Pada demo live, request yang sama dijawab oleh mockApi.js di dalam browser.')}</figcaption></figure>"""


def code(text):
    return f'<pre class="cmd">{text}</pre>'


# ---------------------------------------------------------------- content
def content():
    return [
        section("summary", T("Executive summary", "Ringkasan eksekutif"),
            f'<p class="lead">{s(T("FullStackJS Express + React is a beginner-friendly full-stack JavaScript project: a REST API built with Express, Prisma and MySQL, and a React single-page app that registers users, logs in with a JWT and manages users through a protected admin area.", "FullStackJS Express + React adalah project full-stack JavaScript untuk pemula: REST API dengan Express, Prisma, dan MySQL, serta aplikasi React (single-page) untuk registrasi, login dengan JWT, dan mengelola user lewat area admin yang terproteksi."))}</p>'
            f'<p>{s(T("The repository also contains <code>FundamentalES6</code>, a set of small exercises on modern JavaScript that the project builds on.", "Repositori ini juga berisi <code>FundamentalES6</code>, kumpulan latihan kecil JavaScript modern yang menjadi dasar project ini."))}</p>'
            + stats([("7", T("REST endpoints", "endpoint REST")), ("7", T("React pages", "halaman React")),
                     ("JWT", T("authentication (1 hour)", "autentikasi (1 jam)")), ("23", T("ES6 exercises", "latihan ES6"))])
            + f'<p style="margin-top:18px"><a class="btn" href="{PORTAL}">{s(T("Open the live demo →", "Buka demo live →"))}</a></p>'),

        section("features", T("Features", "Fitur"),
            grid([card("users", T("Register & login", "Registrasi & login"), T("Sign up with name, e-mail and password; log in to receive a JWT that is stored in a cookie.", "Daftar dengan nama, e-mail, dan password; login untuk mendapatkan JWT yang disimpan di cookie.")),
                  card("lock", T("Protected routes", "Route terproteksi"), T("Admin pages redirect to login without a token; the API rejects requests without a valid token.", "Halaman admin mengarahkan ke login jika tidak ada token; API menolak request tanpa token yang valid.")),
                  card("list", T("User management (CRUD)", "Kelola user (CRUD)"), T("List, add, edit and delete users from the admin area.", "Lihat, tambah, ubah, dan hapus user dari area admin.")),
                  card("check", T("Server-side validation", "Validasi di server"), T("express-validator checks required fields, e-mail format, unique e-mail and password length.", "express-validator mengecek field wajib, format e-mail, e-mail unik, dan panjang password.")),
                  card("shield", T("Password hashing", "Hash password"), T("Passwords are hashed with bcrypt before they are stored.", "Password di-hash dengan bcrypt sebelum disimpan.")),
                  card("globe", T("Live demo", "Demo live"), T("The real React app runs on GitHub Pages with the backend simulated in the browser.", "Aplikasi React asli berjalan di GitHub Pages dengan backend yang disimulasikan di browser."))])),

        section("architecture", T("Architecture", "Arsitektur"), architecture_svg()
            + table([T("Layer", "Lapisan"), T("Technology", "Teknologi"), T("Folder", "Folder")], [
                ["Frontend", "React 18, Vite 5, react-router-dom 6, axios, js-cookie, Bootstrap 5", "<code>frontend-react/</code>"],
                ["Backend", "Express 4, express-validator, bcryptjs, jsonwebtoken, cors, body-parser", "<code>backend-express/</code>"],
                ["Database", "MySQL + Prisma ORM", "<code>backend-express/prisma/</code>"],
                [T("Exercises", "Latihan"), "JavaScript ES6+ (Node.js)", "<code>FundamentalES6/</code>"]])),

        section("api", T("API reference", "Referensi API"),
            f'<p>{s(T("Base URL <code>http://localhost:3000</code>. Protected endpoints expect the JWT in the <code>Authorization</code> header (the raw token, without “Bearer”).", "Base URL <code>http://localhost:3000</code>. Endpoint terproteksi membutuhkan JWT di header <code>Authorization</code> (token langsung, tanpa “Bearer”)."))}</p>'
            + table([T("Method", "Method"), T("Endpoint", "Endpoint"), T("Auth", "Auth"), T("Body", "Body"), T("Success", "Sukses")], [
                ["POST", "<code>/api/register</code>", "—", "name, email, password", "201 Register successfully"],
                ["POST", "<code>/api/login</code>", "—", "email, password", "200 { user, token }"],
                ["GET", "<code>/api/admin/users</code>", "JWT", "—", T("200 users (newest first)", "200 daftar user (terbaru dulu)")],
                ["POST", "<code>/api/admin/users</code>", "JWT", "name, email, password", "201 User created successfully"],
                ["GET", "<code>/api/admin/users/:id</code>", "JWT", "—", "200 { id, name, email }"],
                ["PUT", "<code>/api/admin/users/:id</code>", "JWT", "name, email, password", "200 User updated successfully"],
                ["DELETE", "<code>/api/admin/users/:id</code>", "JWT", "—", "200 User deleted successfully"]])
            + f'<h3 style="margin-top:24px">{s(T("Error responses", "Respons error"))}</h3>'
            + table(["HTTP", T("When", "Kapan"), T("Body", "Body")], [
                ["422", T("Validation failed", "Validasi gagal"), '<code>{ success: false, message: "Validation error", errors: [{ path, msg, ... }] }</code>'],
                ["401", T("No token / invalid or expired token / wrong password", "Tanpa token / token tidak valid atau kedaluwarsa / password salah"), '<code>Unauthenticated.</code> · <code>Invalid token</code> · <code>Invalid password</code>'],
                ["404", T("Login with an unknown e-mail", "Login dengan e-mail yang tidak terdaftar"), "<code>User not found</code>"],
                ["500", T("Database error (e.g. updating or deleting an id that does not exist)", "Error database (mis. mengubah atau menghapus id yang tidak ada)"), "<code>Internal server error</code>"]])
            + f'<h3 style="margin-top:24px">{s(T("Example", "Contoh"))}</h3>'
            + code('curl -X POST http://localhost:3000/api/login \\\n  -H "Content-Type: application/json" \\\n  -d \'{"email": "admin@demo.com", "password": "password"}\'\n\n# use the token from the response\ncurl http://localhost:3000/api/admin/users -H "Authorization: &lt;token&gt;"')),

        section("data", T("Data model & validation", "Model data & validasi"),
            table([T("Field", "Field"), T("Type", "Tipe"), T("Rule", "Aturan")], [
                ["<code>id</code>", "Int, auto increment", T("Primary key", "Primary key")],
                ["<code>name</code>", "VarChar(255)", T("Required", "Wajib")],
                ["<code>email</code>", "VarChar(255), unique", T("Required, valid format, not used by another user", "Wajib, format valid, belum dipakai user lain")],
                ["<code>password</code>", "VarChar(255)", T("At least 6 characters, stored as a bcrypt hash", "Minimal 6 karakter, disimpan sebagai hash bcrypt")],
                ["<code>createdAt</code> · <code>updatedAt</code>", "DateTime", T("Set automatically", "Diisi otomatis")]])),

        section("frontend", T("Frontend pages", "Halaman frontend"),
            table([T("Route", "Route"), T("Page", "Halaman"), T("Access", "Akses")], [
                ["<code>/</code>", "Home", T("Public", "Publik")],
                ["<code>/register</code>", "Register", T("Guests (logged-in users go to the dashboard)", "Tamu (yang sudah login diarahkan ke dashboard)")],
                ["<code>/login</code>", "Login", T("Guests", "Tamu")],
                ["<code>/admin/dashboard</code>", "Dashboard", T("Logged in", "Sudah login")],
                ["<code>/admin/users</code>", T("User list", "Daftar user"), T("Logged in", "Sudah login")],
                ["<code>/admin/users/create</code>", T("Add user", "Tambah user"), T("Logged in", "Sudah login")],
                ["<code>/admin/users/edit/:id</code>", T("Edit user", "Ubah user"), T("Logged in", "Sudah login")]])
            + f'<p style="margin-top:12px">{s(T("<code>AuthContext</code> keeps <code>isAuthenticated</code> in sync with the token cookie; the sidebar’s Logout removes the cookies and returns to the login page.", "<code>AuthContext</code> menyelaraskan <code>isAuthenticated</code> dengan cookie token; tombol Logout di sidebar menghapus cookie dan kembali ke halaman login."))}</p>'),

        section("demo", T("Live demo", "Demo live"),
            f'<p class="lead">{s(T("GitHub Pages can only serve static files, so the Express server and MySQL cannot run there. The demo build therefore swaps axios’s network adapter for <code>services/mockApi.js</code>.", "GitHub Pages hanya bisa menyajikan file statis, sehingga server Express dan MySQL tidak bisa berjalan di sana. Karena itu build demo mengganti adapter jaringan axios dengan <code>services/mockApi.js</code>."))}</p>'
            + ul([T("The React code is the same as in local development — only the transport changes.", "Kode React sama dengan saat pengembangan lokal — hanya jalur pengirimannya yang berubah."),
                  T("mockApi.js mirrors every controller and validator: the same routes, status codes, messages and express-validator error format.", "mockApi.js meniru setiap controller dan validator: route, status code, pesan, dan format error express-validator yang sama."),
                  T("Data is stored in the visitor’s browser (localStorage). <b>Reset data</b> in the demo banner restores the sample users.", "Data disimpan di browser pengunjung (localStorage). <b>Reset data</b> di banner demo mengembalikan user contoh."),
                  T("Demo login: <code>admin@demo.com</code> / <code>password</code>.", "Login demo: <code>admin@demo.com</code> / <code>password</code>."),
                  T("Built and deployed automatically by GitHub Actions (<code>.github/workflows/pages.yml</code>) with <code>VITE_DEMO=true</code>. A normal build contains no demo code.", "Di-build dan di-deploy otomatis oleh GitHub Actions (<code>.github/workflows/pages.yml</code>) dengan <code>VITE_DEMO=true</code>. Build biasa tidak berisi kode demo.")])),

        section("run", T("Run locally", "Menjalankan di lokal"),
            '<ol class="clean">' + "".join(f"<li>{s(x)}</li>" for x in [
                T("Create a MySQL database named <code>db_express</code>.", "Buat database MySQL bernama <code>db_express</code>."),
                T("Copy <code>backend-express/.env.example</code> to <code>.env</code> and set <code>DATABASE_URL</code> and <code>JWT_SECRET</code>.", "Salin <code>backend-express/.env.example</code> menjadi <code>.env</code> lalu isi <code>DATABASE_URL</code> dan <code>JWT_SECRET</code>."),
                T("Start the API (port 3000):", "Jalankan API (port 3000):")]) + "</ol>"
            + code("cd backend-express\nnpm install\nnpx prisma migrate dev\nnode index.js")
            + f'<ol class="clean" start="4"><li>{s(T("Start the React app (Vite dev server):", "Jalankan aplikasi React (Vite dev server):"))}</li></ol>'
            + code("cd frontend-react\nnpm install\nnpm run dev")
            + f'<p>{s(T("To try the demo mode locally: <code>VITE_DEMO=true npm run dev</code>.", "Untuk mencoba mode demo di lokal: <code>VITE_DEMO=true npm run dev</code>."))}</p>'),

        section("es6", "FundamentalES6",
            f'<p>{s(T("Short Node.js scripts that practise the JavaScript features used throughout the project:", "Script Node.js singkat untuk berlatih fitur JavaScript yang dipakai di seluruh project:"))}</p>'
            + '<div class="grid g3">' + "".join(f'<div class="card"><h3>{t}</h3><p>{s(d)}</p></div>' for t, d in [
                ("let · const · var", T("variable, variable2, variable3", "variable, variable2, variable3")),
                (T("Arrow functions", "Arrow function"), "ArrowFunction1 – 5"),
                (T("Template literals", "Template literal"), "TemplateStringLiteral"),
                (T("Destructuring", "Destructuring"), "Destructuring, Destructuring2, Restructuring"),
                ("Spread · Rest", "SpreadOperator 1–2, RestParameter 1–2"),
                (T("Default parameters", "Parameter default"), "DefaultParam, DefaultParam2"),
                ("Array.map", "ArrayMap"),
                ("Promise · async/await", "Promise, Promise2, AsyncAwait"),
                ("Hello World", "HelloWorld")]) + "</div>"),

        section("next", T("Known limitations & improvements", "Keterbatasan & perbaikan"),
            f'<h3>{s(T("Already improved", "Sudah diperbaiki"))}</h3>'
            + ul([T("The add and edit pages read the token when the request is sent (it used to be read once when the file loaded, so requests right after login had no token).", "Halaman tambah dan ubah membaca token saat request dikirim (sebelumnya dibaca sekali saat file dimuat, sehingga request tepat setelah login tidak membawa token)."),
                  T("The edit page sends the token when loading the user, so it also works when opened directly or refreshed.", "Halaman ubah mengirim token saat memuat data user, sehingga tetap berfungsi saat dibuka langsung atau di-refresh."),
                  T("<code>backend-express/.env</code> is no longer tracked; use <code>.env.example</code>.", "<code>backend-express/.env</code> tidak lagi disimpan di repo; gunakan <code>.env.example</code>.")])
            + f'<h3 style="margin-top:20px">{s(T("Ideas for next steps", "Ide langkah berikutnya"))}</h3>'
            + grid([card("lock", T("Hide password hashes", "Sembunyikan hash password"), T("Register, create and update return the full user including the password hash — select only id, name and e-mail.", "Register, create, dan update mengembalikan user lengkap termasuk hash password — pilih hanya id, nama, dan e-mail."), True),
                    card("shield", T("Safer token storage", "Penyimpanan token lebih aman"), T("Use an HttpOnly cookie set by the server and the standard <code>Bearer</code> scheme.", "Gunakan cookie HttpOnly yang di-set server dan skema standar <code>Bearer</code>.")),
                    card("clock", T("Handle token expiry", "Tangani token kedaluwarsa"), T("Log the user out automatically when the API answers 401.", "Logout otomatis saat API menjawab 401.")),
                    card("doc", T("Optional password on edit", "Password opsional saat ubah"), T("Allow updating name or e-mail without re-entering a password.", "Izinkan mengubah nama atau e-mail tanpa mengisi ulang password.")),
                    card("check", T("404 for unknown ids", "404 untuk id yang tidak ada"), T("Return 404 instead of 500 when a user id does not exist.", "Kembalikan 404, bukan 500, saat id user tidak ada.")),
                    card("layers", T("Deploy the backend", "Deploy backend"), T("Host the API and a managed MySQL database so the demo can use the real backend.", "Host API dan database MySQL terkelola agar demo bisa memakai backend sungguhan."))])),
    ]


# ---------------------------------------------------------------- page template
CSS = """
:root{--bg:#F5F8FB;--surface:#FFFFFF;--surface2:#ECF2F8;--ink:#14202E;--muted:#5A6878;--line:#D8E2EC;
 --navy:#10243A;--acc:#0E8AC0;--acc-ink:#0A6E9A;--acc-tint:#E1F2FA;--amber:#7A57D1;--amber-tint:#EFE9FB;--hero:#10243A;--hero-ink:#C9DDEE;--eyebrow:#61DAFB;
 --shadow:0 1px 2px rgba(16,36,58,.06),0 6px 20px rgba(16,36,58,.06)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#0A121C;--surface:#111D2B;--surface2:#16273A;--ink:#E6EEF6;--muted:#9DB0C3;
 --line:#22374E;--navy:#D2E6F5;--acc:#3BB7EA;--acc-ink:#61DAFB;--acc-tint:#12324A;--amber:#A98BF0;--amber-tint:#2A2148;--hero:#07101A;--shadow:none}}
:root[data-theme="dark"]{--bg:#0A121C;--surface:#111D2B;--surface2:#16273A;--ink:#E6EEF6;--muted:#9DB0C3;--line:#22374E;--navy:#D2E6F5;
 --acc:#3BB7EA;--acc-ink:#61DAFB;--acc-tint:#12324A;--amber:#A98BF0;--amber-tint:#2A2148;--hero:#07101A;--shadow:none}
th{background:#10243A!important}
pre.cmd{background:var(--surface2);border:1px solid var(--line);border-radius:10px;padding:12px 14px;overflow:auto;font:13px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;margin:8px 0}
"""
CSS_COMMON = """
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 "Segoe UI",Calibri,Arial,sans-serif}
a{color:var(--acc-ink)}code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.88em;background:var(--surface2);padding:1px 5px;border-radius:5px}
.wrap{max-width:1120px;margin:0 auto;padding:0 16px}
header.hero{background:var(--hero);color:#fff;padding:56px 0 44px}
.hero .eyebrow{color:var(--eyebrow);font-weight:600;letter-spacing:.06em;text-transform:uppercase;font-size:13px}
.hero h1{font:700 clamp(32px,5vw,52px)/1.1 Cambria,Georgia,serif;margin:10px 0 12px}
.hero p{color:var(--hero-ink);max-width:760px;margin:0;font-size:18px}
.hero .meta{margin-top:18px;color:var(--hero-ink);opacity:.8;font-size:14px}
nav.toc{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
nav.toc .wrap{display:flex;gap:6px;overflow-x:auto;padding-top:10px;padding-bottom:10px;align-items:center}
nav.toc a{white-space:nowrap;text-decoration:none;color:var(--muted);font-size:14px;padding:6px 10px;border-radius:999px}
nav.toc a:hover{background:var(--surface2);color:var(--ink)}
nav.toc .spacer{flex:1}
.tgl{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:6px 12px;font-size:13px;cursor:pointer;white-space:nowrap;text-decoration:none}
a.tgl{color:var(--ink)!important}
section{padding:44px 0 8px;scroll-margin-top:56px}
h2{font:700 30px/1.2 Cambria,Georgia,serif;color:var(--navy);margin:0 0 14px}
h3{font-size:18px;margin:0 0 6px;color:var(--ink)}
.lead{font-size:18px;color:var(--muted);max-width:820px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:22px}
.stat{background:var(--acc-tint);border-radius:14px;padding:18px;text-align:center}
.stat b{display:block;font:700 34px/1.1 Cambria,Georgia,serif;color:var(--acc-ink)}
.stat span{color:var(--muted);font-size:14px}
.grid{display:grid;gap:14px}.g2{grid-template-columns:repeat(2,1fr)}.g3{grid-template-columns:repeat(3,1fr)}
.card{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:20px;box-shadow:var(--shadow)}
.card p{margin:0;color:var(--muted)}
.ihead{display:flex;gap:12px;align-items:center;margin-bottom:8px}
.ico{width:40px;height:40px;flex:none;padding:9px;border-radius:50%;background:var(--acc);stroke:#fff;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.amber .ico{background:var(--amber)}
figure{margin:18px 0;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:10px;overflow:auto}
figure svg{display:block;width:100%;height:auto;min-width:720px;font-family:"Segoe UI",Calibri,Arial,sans-serif}
figcaption{color:var(--muted);font-size:14px;text-align:center;padding:6px}
svg .lane rect{fill:var(--surface2);stroke:var(--line)}svg .lt{fill:var(--muted);font-size:13px;font-weight:700;text-anchor:middle;letter-spacing:.04em;text-transform:uppercase}
svg .bx rect{fill:var(--surface);stroke:var(--line);stroke-width:1.5}svg .bx text{fill:var(--ink);font-size:14px;font-weight:600;text-anchor:middle}
svg .bx text.sm{fill:var(--muted);font-size:11.5px;font-weight:400}
svg .bx.hl rect{stroke:var(--acc);stroke-width:2;fill:var(--acc-tint)}svg .bx.amb rect{stroke:var(--amber);stroke-width:2;fill:var(--amber-tint)}
svg .bx.err rect{stroke:#D0505D;stroke-width:1.5;stroke-dasharray:5 4}
svg .ln path{fill:none;stroke:var(--acc);stroke-width:2}svg .mk{fill:var(--acc)}
ul.clean,ol.clean{padding-left:22px;margin:10px 0}ul.clean li,ol.clean li{margin:6px 0}
.note{background:var(--amber-tint);border-radius:12px;padding:14px 16px;color:var(--ink)}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--surface)}
table{border-collapse:collapse;width:100%;min-width:620px;font-size:15px}
th{background:var(--navy-th,#141B3C);color:#fff;text-align:left;padding:10px 14px;font-weight:600}
td{padding:10px 14px;border-top:1px solid var(--line);vertical-align:top}
tbody tr:nth-child(even) td{background:var(--surface2)}
.pill{display:inline-block;background:var(--acc-tint);color:var(--acc-ink);font-weight:700;border-radius:999px;padding:2px 10px;font-size:13px}
.q{font-weight:700;color:var(--navy);margin:0 0 6px!important;font-size:17px}
.starter{display:flex;gap:16px;align-items:flex-start}.starter p{margin:0 0 6px}
.snum{flex:none;width:40px;height:40px;border-radius:50%;background:var(--acc);color:#fff;font:700 18px/40px Cambria,Georgia,serif;text-align:center}
.snum.amber{background:var(--amber)}
.outcome{color:var(--acc-ink)!important;font-weight:600;margin-top:8px!important}
.uc h3{font-size:19px;margin-bottom:6px}.uc .meta{font-size:14px;margin:0 0 10px}
.ba{display:grid;grid-template-columns:1fr 1fr;gap:12px}.ba div{border-radius:12px;padding:12px 14px;font-size:15px;color:var(--ink)}
.ba span{display:block;font-weight:700;font-size:12px;letter-spacing:.06em;text-transform:uppercase;margin-bottom:4px}
.before{background:var(--surface2)}.before span{color:var(--muted)}.after{background:var(--acc-tint)}.after span{color:var(--acc-ink)}
a.btn{display:inline-block;background:var(--acc);color:#fff;text-decoration:none;font-weight:600;padding:10px 18px;border-radius:10px}
footer{padding:40px 0 60px;color:var(--muted);font-size:14px;border-top:1px solid var(--line);margin-top:40px}
body.present nav.toc{display:none}
body.present section,body.present header.hero{min-height:100vh;display:flex;flex-direction:column;justify-content:center}
body.present section{border-top:1px solid var(--line)}
@media (max-width:820px){.stats{grid-template-columns:repeat(2,1fr)}.g2,.g3{grid-template-columns:1fr}.ba{grid-template-columns:1fr}h2{font-size:26px}}
@media print{nav.toc,.tgl{display:none}section{break-inside:avoid}body{background:#fff}}
"""
JS = """<script>
(function(){var r=document.documentElement,k='doc-theme';
function set(t){if(t)r.setAttribute('data-theme',t);else r.removeAttribute('data-theme');try{localStorage.setItem(k,t)}catch(e){}}
try{var t=localStorage.getItem(k);if(t)r.setAttribute('data-theme',t)}catch(e){}
document.getElementById('theme').onclick=function(){var c=r.getAttribute('data-theme');set(c==='dark'?'light':c==='light'?'':'dark')};
document.getElementById('present').onclick=function(){document.body.classList.toggle('present')};
document.addEventListener('keydown',function(e){if(e.key==='f'&&document.body.classList.contains('present')){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen()}});
})();
</script>"""

TOC = [("summary", T("Summary", "Ringkasan")), ("features", T("Features", "Fitur")), ("architecture", T("Architecture", "Arsitektur")),
       ("api", "API"), ("data", T("Data model", "Model data")), ("frontend", "Frontend"), ("demo", T("Live demo", "Demo live")),
       ("run", T("Run locally", "Jalankan")), ("es6", "ES6"), ("next", T("Improvements", "Perbaikan"))]


def page():
    other = "id" if LANG == "en" else "en"
    other_href = ("../" + LINK["en"]) if LANG == "id" else LINK["id"]
    toc = "".join(f'<a href="#{i}">{s(t)}</a>' for i, t in TOC)
    return f"""<!doctype html>
<html lang="{LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FullStackJS Express + React</title>
<meta name="description" content="{s(T("Documentation for a beginner full-stack JavaScript project with Express, Prisma, MySQL and React.", "Dokumentasi project full-stack JavaScript pemula dengan Express, Prisma, MySQL, dan React."))}">
<style>{CSS}{CSS_COMMON}</style>
</head>
<body>
<header class="hero"><div class="wrap">
  <div class="eyebrow">{s(T("Project Documentation", "Dokumentasi Project"))}</div>
  <h1>FullStackJS Express + React</h1>
  <p>{s(T("REST API with Express, Prisma &amp; MySQL and a React single-page app with JWT login and user management", "REST API dengan Express, Prisma &amp; MySQL dan aplikasi React dengan login JWT serta manajemen user"))}</p>
  <div class="meta">{s(T("Version 1.0 · November 2026 · Learning project", "Versi 1.0 · November 2026 · Project pembelajaran"))}</div>
</div></header>
<nav class="toc" aria-label="Contents"><div class="wrap">{toc}<span class="spacer"></span>
  <a class="tgl" href="{other_href}" hreflang="{other}">{"Bahasa Indonesia" if LANG == "en" else "English"}</a>
  <button class="tgl" id="present" title="One section per screen (F = full screen)">{s(T("Presentation mode", "Mode presentasi"))}</button>
  <button class="tgl" id="theme">{s(T("Theme", "Tema"))}</button>
</div></nav>
<main class="wrap">
{"".join(content())}
</main>
<footer><div class="wrap">FullStackJS Express + React · <a href="{REPO}">GitHub</a> · <a href="{PORTAL}">{s(T("Live demo", "Demo live"))}</a></div></footer>
{JS}
</body>
</html>
"""


INDEX = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=FullStackJS-Documentation.html">
<title>FullStackJS documentation</title></head><body><a href="FullStackJS-Documentation.html">English</a> · <a href="id/FullStackJS-Dokumentasi.html">Bahasa Indonesia</a></body></html>
"""

if __name__ == "__main__":
    for LANG in ("en", "id"):
        OUT[LANG].parent.mkdir(parents=True, exist_ok=True)
        OUT[LANG].write_text(page(), encoding="utf-8")
        print("wrote", OUT[LANG].relative_to(ROOT))
    (ROOT / "docs" / "index.html").write_text(INDEX, encoding="utf-8")
    print("wrote docs/index.html")
