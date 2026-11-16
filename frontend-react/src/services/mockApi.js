// Mock backend untuk demo live (GitHub Pages).
//
// GitHub Pages hanya bisa menyajikan file statis, jadi backend Express + Prisma + MySQL
// tidak bisa ikut berjalan. Saat build dengan VITE_DEMO=true, axios memakai adapter ini:
// setiap request dijawab di browser dengan aturan yang sama seperti controller dan
// validator di backend-express (status code, pesan, dan format error express-validator).
// Data disimpan di localStorage browser pengunjung.
import { AxiosError } from 'axios';

const DB_KEY = 'fsjs-demo-db';
const SECRET = 'demo-only-secret';
const SEED_USERS = [
    { name: 'Admin Demo', email: 'admin@demo.com', password: 'password' },
    { name: 'Dimas Agung Prakasa', email: 'dimas@demo.com', password: 'password' },
    { name: 'Siti Rahma', email: 'siti@demo.com', password: 'password' },
];

const enc = new TextEncoder();
const b64url = (str) => btoa(unescape(encodeURIComponent(str))).replace(/=+$/, '').replace(/\+/g, '-').replace(/\//g, '_');
const fromB64url = (str) => decodeURIComponent(escape(atob(str.replace(/-/g, '+').replace(/_/g, '/'))));

async function sha256(text) {
    const buf = await crypto.subtle.digest('SHA-256', enc.encode(text));
    return Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, '0')).join('');
}
// Bentuknya meniru hash bcrypt ($2a$10$...) agar respons terlihat seperti aslinya.
const hashPassword = async (pw) => '$2a$10$' + (await sha256('salt:' + pw)).slice(0, 53);
const checkPassword = async (pw, hash) => (await hashPassword(pw)) === hash;

// Token berformat JWT (header.payload.signature) dengan masa berlaku 1 jam, seperti jwt.sign(..., { expiresIn: '1h' }).
async function signToken(payload) {
    const now = Math.floor(Date.now() / 1000);
    const head = b64url(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
    const body = b64url(JSON.stringify({ ...payload, iat: now, exp: now + 3600 }));
    const sig = b64url((await sha256(`${head}.${body}.${SECRET}`)).slice(0, 43));
    return `${head}.${body}.${sig}`;
}
async function verifyToken(token) {
    const parts = String(token || '').split('.');
    if (parts.length !== 3) return null;
    const sig = b64url((await sha256(`${parts[0]}.${parts[1]}.${SECRET}`)).slice(0, 43));
    if (sig !== parts[2]) return null;
    try {
        const payload = JSON.parse(fromB64url(parts[1]));
        return payload.exp > Date.now() / 1000 ? payload : null;
    } catch {
        return null;
    }
}

/* ---------- penyimpanan ---------- */
let memoryDb = null;
async function freshDb() {
    const now = new Date().toISOString();
    const users = [];
    for (const [i, u] of SEED_USERS.entries()) {
        users.push({ id: i + 1, name: u.name, email: u.email, password: await hashPassword(u.password), createdAt: now, updatedAt: now });
    }
    return { nextId: users.length + 1, users };
}
async function load() {
    try {
        const raw = localStorage.getItem(DB_KEY);
        if (raw) return JSON.parse(raw);
    } catch { /* localStorage tidak tersedia */ }
    if (!memoryDb) memoryDb = await freshDb();
    return memoryDb;
}
function save(db) {
    memoryDb = db;
    try { localStorage.setItem(DB_KEY, JSON.stringify(db)); } catch { /* abaikan */ }
}
export async function resetDemoData() {
    const db = await freshDb();
    save(db);
}

/* ---------- validator (meniru express-validator) ---------- */
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const fieldError = (path, value, msg) => ({ type: 'field', value, msg, path, location: 'body' });

function validate(rules, body) {
    const errors = [];
    for (const [path, checks] of rules) {
        const value = body[path];
        for (const [ok, msg] of checks) {
            if (!ok(value)) { errors.push(fieldError(path, value, msg)); break; }
        }
    }
    return errors;
}
const notEmpty = (v) => v !== undefined && v !== null && String(v).trim() !== '';
const minLen6 = (v) => typeof v === 'string' && v.length >= 6;

function emailRules(db, ignoreId) {
    return ['email', [
        [notEmpty, 'Email is required'],
        [(v) => EMAIL_RE.test(String(v)), 'Email is invalid'],
        [(v) => !db.users.some((u) => u.email === v && u.id !== ignoreId), 'Email already exists'],
    ]];
}
const nameRule = ['name', [[notEmpty, 'Name is required']]];
const passwordRule = ['password', [[minLen6, 'Password must be at least 6 characters long']]];
const validationError = (errors) => [422, { success: false, message: 'Validation error', errors }];

/* ---------- route handler (meniru controllers/*.js) ---------- */
const publicUser = ({ id, name, email }) => ({ id, name, email });

async function handle(method, path, body, headers) {
    const db = await load();

    if (method === 'post' && path === '/api/register') {
        const errors = validate([nameRule, emailRules(db), passwordRule], body);
        if (errors.length) return validationError(errors);
        const now = new Date().toISOString();
        const user = { id: db.nextId++, name: body.name, email: body.email, password: await hashPassword(body.password), createdAt: now, updatedAt: now };
        db.users.push(user); save(db);
        return [201, { success: true, message: 'Register successfully', data: user }];
    }

    if (method === 'post' && path === '/api/login') {
        const errors = validate([['email', [[notEmpty, 'Email is required']]], passwordRule], body);
        if (errors.length) return validationError(errors);
        const user = db.users.find((u) => u.email === body.email);
        if (!user) return [404, { success: false, message: 'User not found' }];
        if (!(await checkPassword(body.password, user.password))) return [401, { success: false, message: 'Invalid password' }];
        const token = await signToken({ id: user.id });
        return [200, { success: true, message: 'Login successfully', data: { user: publicUser(user), token } }];
    }

    if (path === '/' && method === 'get') return [200, 'Hello World!'];

    const m = path.match(/^\/api\/admin\/users(?:\/([^/]+))?$/);
    if (!m) return [404, `Cannot ${method.toUpperCase()} ${path}`];

    // middlewares/auth.js
    const token = headers.Authorization || headers.authorization;
    if (!token) return [401, { message: 'Unauthenticated.' }];
    if (!(await verifyToken(token))) return [401, { message: 'Invalid token' }];

    const id = m[1] !== undefined ? Number(m[1]) : null;
    const idx = id === null ? -1 : db.users.findIndex((u) => u.id === id);

    if (id === null && method === 'get') {
        const users = [...db.users].sort((a, b) => b.id - a.id).map(publicUser);
        return [200, { success: true, message: 'Get all users successfully', data: users }];
    }
    if (id === null && method === 'post') {
        const errors = validate([nameRule, emailRules(db), passwordRule], body);
        if (errors.length) return validationError(errors);
        const now = new Date().toISOString();
        const user = { id: db.nextId++, name: body.name, email: body.email, password: await hashPassword(body.password), createdAt: now, updatedAt: now };
        db.users.push(user); save(db);
        return [201, { success: true, message: 'User created successfully', data: user }];
    }
    if (id !== null && method === 'get') {
        return [200, { success: true, message: `Get user By ID :${m[1]}`, data: idx >= 0 ? publicUser(db.users[idx]) : null }];
    }
    if (id !== null && method === 'put') {
        const errors = validate([nameRule, emailRules(db, id), passwordRule], body);
        if (errors.length) return validationError(errors);
        if (idx < 0) return [500, { success: false, message: 'Internal server error' }]; // Prisma update pada id yang tidak ada
        const user = { ...db.users[idx], name: body.name, email: body.email, password: await hashPassword(body.password), updatedAt: new Date().toISOString() };
        db.users[idx] = user; save(db);
        return [200, { success: true, message: 'User updated successfully', data: user }];
    }
    if (id !== null && method === 'delete') {
        if (idx < 0) return [500, { success: false, message: 'Internal server error' }];
        db.users.splice(idx, 1); save(db);
        return [200, { success: true, message: 'User deleted successfully' }];
    }
    return [404, `Cannot ${method.toUpperCase()} ${path}`];
}

/* ---------- axios adapter ---------- */
export default async function mockAdapter(config) {
    const url = new URL(config.url, config.baseURL || 'http://localhost:3000');
    const method = (config.method || 'get').toLowerCase();
    let body = config.data;
    if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
    const headers = config.headers && typeof config.headers.toJSON === 'function' ? config.headers.toJSON() : { ...config.headers };

    await new Promise((r) => setTimeout(r, 150 + Math.random() * 200)); // latensi jaringan
    const [status, data] = await handle(method, url.pathname, body || {}, headers);
    const response = { data, status, statusText: String(status), headers: { 'content-type': 'application/json' }, config, request: null };
    if (status >= 400) {
        throw new AxiosError(`Request failed with status code ${status}`, status >= 500 ? AxiosError.ERR_BAD_RESPONSE : AxiosError.ERR_BAD_REQUEST, config, null, response);
    }
    return response;
}
