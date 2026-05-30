"""Smoke-test API endpoints. Usage: python scripts/test_endpoints.py [BASE_URL]"""
import json
import sys
import time
from http.cookiejar import CookieJar
import urllib.request
from urllib.error import HTTPError
from urllib.request import Request

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:5000').rstrip('/')
PASS = FAIL = 0
jar = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
_ctx = {}


def req(method, path, data=None, expect=None, label=None):
    global PASS, FAIL
    url = f'{BASE}{path}'
    body = json.dumps(data).encode() if data is not None else None
    r = Request(url, data=body, method=method)
    r.add_header('Content-Type', 'application/json')
    try:
        with opener.open(r, timeout=120) as res:
            code = res.status
            raw = res.read().decode()
    except HTTPError as e:
        code = e.code
        raw = e.read().decode()
    try:
        payload = json.loads(raw) if raw else None
    except json.JSONDecodeError:
        payload = raw[:300]

    ok = expect(code, payload) if expect else (200 <= code < 300)
    tag = 'PASS' if ok else 'FAIL'
    PASS += ok
    FAIL += not ok
    name = label or f'{method} {path}'
    print(f'  [{tag}] {name} -> {code}')
    if not ok:
        print(f'         {payload}')
    return code, payload


def login(email, password):
    jar.clear()
    req('POST', '/api/login', {'email': email, 'password': password},
        expect=lambda c, p: c == 200 and p.get('success'), label=f'login {email}')


def main():
    print(f'Testing {BASE}\n')
    suffix = int(time.time())

    req('GET', '/health', expect=lambda c, p: c == 200 and p.get('status') == 'ok')
    req('GET', '/api/departments')

    # --- Admin ---
    login('admin@admin.com', 'admin')
    req('GET', '/api/me', expect=lambda c, p: p.get('user', {}).get('role') == 'admin')
    req('GET', '/api/admin/dashboard', expect=lambda c, p: 'patients' in p)
    req('GET', '/api/admin/get_doctors', expect=lambda c, p: isinstance(p, list))
    req('GET', '/api/get_patients', expect=lambda c, p: isinstance(p, list))

    dept_name = f'Cardio{suffix}'
    code, dep = req('POST', '/api/admin/add_department',
                    {'dpt_name': dept_name, 'description': 'Test'},
                    expect=lambda c, p: c in (201, 409))
    req('GET', '/api/departments', expect=lambda c, p: isinstance(p, list) and len(p) >= 0)

    doc_email = f'doc{suffix}@test.com'
    code, _ = req('POST', '/api/admin/add_doctor', {
        'name': 'Dr Test',
        'experience': '5',
        'email': doc_email,
        'gender': 'Male',
        'phone_no': '9876543210',
        'password': 'docpass123',
        'department': dept_name,
    }, expect=lambda c, p: c in (201, 400))

    req('POST', '/api/logout')

    # --- Patient signup & flow ---
    pat_email = f'pat{suffix}@test.com'
    req('POST', '/api/signup', {
        'email': pat_email,
        'password': 'patpass123',
        'confirm_password': 'patpass123',
        'Full_name': 'Test Patient',
        'Age': 25,
        'Gender': 'M',
        'Address': 'Test St',
        'PhoneNo': '1234567890',
    }, expect=lambda c, p: c == 200 and p.get('success'), label='patient signup')

    login(pat_email, 'patpass123')
    req('GET', '/api/me', expect=lambda c, p: p.get('user', {}).get('role') == 'patient')
    code, dash = req('GET', '/api/patient/dashboard', expect=lambda c, p: 'departments' in p)
    patient_id = dash.get('user_id') if isinstance(dash, dict) else None

    if patient_id:
        req('GET', f'/api/patient/{patient_id}/profile')
        req('GET', f'/api/patient/{patient_id}/treatment', expect=lambda c, p: isinstance(p, list))

    doctors = req('GET', '/api/departments')[1]
    if isinstance(doctors, list) and doctors:
        dept_id = doctors[0].get('id')
        if dept_id:
            req('GET', f'/api/patient/department/{dept_id}',
                expect=lambda c, p: c in (200, 403))

    req('POST', '/api/logout')

    # --- Doctor ---
    login(doc_email, 'docpass123')
    req('GET', '/api/me', expect=lambda c, p: p.get('user', {}).get('role') == 'doctor')
    code, dd = req('GET', '/api/doctor/dashboard', expect=lambda c, p: 'doctor_id' in p)
    doc_id = dd.get('doctor_id') if isinstance(dd, dict) else None
    if doc_id:
        req('GET', f'/api/doctor/{doc_id}/profile')
        req('GET', f'/api/doctor/availability/{doc_id}', expect=lambda c, p: isinstance(p, dict))

    req('POST', '/api/logout')

    print(f'\nDone: {PASS} passed, {FAIL} failed\n')
    return 0 if FAIL == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
