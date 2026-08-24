#!/usr/bin/env python3
"""TinyOLED local browser bridge: loopback, allow-listed, control-off by default."""
from __future__ import annotations
import email, imaplib, json, os, re, shutil, subprocess, urllib.parse, urllib.request
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HOST=os.getenv('TINY_BRIDGE_HOST','127.0.0.1'); PORT=int(os.getenv('TINY_BRIDGE_PORT','8765'))
CONTROL=os.getenv('TINY_ALLOW_CONTROL','0')=='1'
SERVICES={'ssh','nginx','docker','cron','tinyoled'}
ORIGINS={'https://seydivakkas.github.io','http://localhost','http://127.0.0.1','null'}

def run(args,timeout=8):
    p=subprocess.run(args,capture_output=True,text=True,timeout=timeout,check=False)
    return p.returncode,p.stdout.strip(),p.stderr.strip()
def require_control():
    if not CONTROL: raise PermissionError('control disabled; set TINY_ALLOW_CONTROL=1')
def allowed_origin(origin):
    return not origin or origin in ORIGINS or origin.startswith('http://localhost:') or origin.startswith('http://127.0.0.1:')
def wifi_scan():
    nets=[]
    if shutil.which('nmcli'):
        rc,out,err=run(['nmcli','-t','-f','SSID,SIGNAL,CHAN,SECURITY','dev','wifi','list'],12)
        if rc: raise RuntimeError(err or out)
        for line in out.splitlines():
            parts=line.rsplit(':',3)
            if len(parts)==4 and parts[0]: nets.append({'ssid':parts[0],'signal':int(parts[1] or 0),'channel':parts[2],'security':parts[3]})
    elif shutil.which('iwlist'):
        rc,out,err=run(['iwlist','wlan0','scan'],12)
        if rc: raise RuntimeError(err or out)
        cells=re.split(r'Cell \d+ -',out)[1:]
        for c in cells:
            ssid=re.search(r'ESSID:"(.*?)"',c); q=re.search(r'Signal level=(-?\d+) dBm',c); ch=re.search(r'Channel:(\d+)',c)
            nets.append({'ssid':ssid.group(1) if ssid else '?','signal':int(q.group(1)) if q else None,'channel':ch.group(1) if ch else None})
    else: raise RuntimeError('nmcli/iwlist unavailable')
    return {'networks':nets}
def docker_list():
    rc,out,err=run(['docker','ps','-a','--format','{{json .}}'],10)
    if rc: raise RuntimeError(err or out)
    rows=[]
    for line in out.splitlines():
        d=json.loads(line); rows.append({'id':d.get('ID'),'name':d.get('Names'),'running':str(d.get('State','')).lower()=='running','status':d.get('Status')})
    return {'containers':rows}
def systemd_list():
    rows=[]
    for name in sorted(SERVICES):
        rc,out,_=run(['systemctl','is-active',name],3); rows.append({'name':name,'active':rc==0,'state':out})
    return {'services':rows}
def ssh_alerts():
    p=Path('/var/log/auth.log')
    if not p.exists(): return {'alerts':[]}
    lines=p.read_text(errors='ignore').splitlines()[-2000:]
    ips=[]
    for line in lines:
        if 'Failed password' in line or 'authentication failure' in line:
            m=re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b',line)
            if m: ips.append(m.group(0))
    return {'alerts':[{'ip':ip,'count':n} for ip,n in Counter(ips).most_common(20)]}
def pihole_stats():
    for url in ('http://127.0.0.1/admin/api.php?summary','http://pi.hole/admin/api.php?summary'):
        try:
            with urllib.request.urlopen(url,timeout=2) as r: d=json.loads(r.read())
            return {'enabled':str(d.get('status','enabled')).lower()!='disabled','blocked':int(d.get('ads_blocked_today',0)),'queries':int(d.get('dns_queries_today',0)),'percent':float(d.get('ads_percentage_today',0))}
        except Exception: pass
    raise RuntimeError('Pi-hole API unavailable')
def storage_stats():
    d=shutil.disk_usage('/')
    return {'total':d.total,'used':d.used,'free':f'{d.free//(1024**3)}GB','used_percent':round(100*d.used/d.total,1)}
def apt_updates():
    rc,out,err=run(['apt','list','--upgradable'],15)
    if rc not in (0,): raise RuntimeError(err or out)
    lines=[x for x in out.splitlines() if x and not x.startswith('Listing')]
    return {'pending':len(lines),'security':sum('security' in x.lower() for x in lines),'last_check':'live'}
def email_unread():
    host=os.getenv('TINY_EMAIL_HOST'); user=os.getenv('TINY_EMAIL_USER'); pw=os.getenv('TINY_EMAIL_PASSWORD')
    if not all((host,user,pw)): raise RuntimeError('email env vars not configured')
    box=imaplib.IMAP4_SSL(host); box.login(user,pw); box.select('INBOX'); _,data=box.search(None,'UNSEEN'); ids=data[0].split()[-10:]; msgs=[]
    for mid in reversed(ids):
        _,raw=box.fetch(mid,'(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)])'); msg=email.message_from_bytes(raw[0][1]); msgs.append({'from':msg.get('From',''),'subject':msg.get('Subject','')})
    box.logout(); return {'unread':len(ids),'messages':msgs}
def telegram_messages():
    token=os.getenv('TINY_TELEGRAM_BOT_TOKEN')
    if not token: raise RuntimeError('Telegram token not configured')
    with urllib.request.urlopen(f'https://api.telegram.org/bot{token}/getUpdates?limit=10&timeout=0',timeout=5) as r: d=json.loads(r.read())
    msgs=[]
    for u in d.get('result',[]):
        m=u.get('message') or u.get('channel_post') or {}; frm=m.get('from',{}); msgs.append({'from':frm.get('username') or frm.get('first_name') or 'user','text':m.get('text','')})
    return {'messages':msgs[-10:]}
def gpio_list():
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM); pins=[]
    for pin in (5,6,12,13,17,18,22,23,24,26,27):
        try: pins.append({'pin':pin,'direction':'out' if GPIO.gpio_function(pin)==GPIO.OUT else 'in','value':int(GPIO.input(pin))})
        except Exception: pass
    return {'pins':pins}
def gpio_write(pin,value):
    require_control(); import RPi.GPIO as GPIO
    pin=int(pin)
    if pin not in {5,6,12,13,17,18,22,23,24,26,27}: raise ValueError('pin not allow-listed')
    GPIO.setmode(GPIO.BCM); GPIO.setup(pin,GPIO.OUT); GPIO.output(pin,GPIO.HIGH if int(value) else GPIO.LOW); return {'pin':pin,'value':int(bool(value))}
def i2c_scan(busno=1):
    import smbus2
    bus=smbus2.SMBus(int(busno)); out=[]
    try:
        for a in range(0x03,0x78):
            try: bus.read_byte(a); out.append({'address':f'0x{a:02X}','name':{0x3c:'SSD1306',0x40:'INA219',0x68:'RTC'}.get(a,'I2C')})
            except Exception: pass
    finally: bus.close()
    return {'devices':out}
def ina219_read():
    import smbus2
    bus=smbus2.SMBus(1); addr=0x40
    try:
        raw=bus.read_word_data(addr,0x02); raw=((raw>>8)|((raw<<8)&0xffff)); voltage=raw*0.001
        raw=bus.read_word_data(addr,0x04); raw=((raw>>8)|((raw<<8)&0xffff)); current=raw*0.1
        return {'voltage':voltage,'current':current,'power':voltage*current/1000}
    finally: bus.close()
def dht_read():
    import Adafruit_DHT
    h,t=Adafruit_DHT.read_retry(11,4)
    if t is None or h is None: raise RuntimeError('DHT read failed')
    return {'temperature':t,'humidity':h,'sensor':'DHT11/22'}
def plant_read():
    import spidev
    spi=spidev.SpiDev(); spi.open(0,0)
    try: r=spi.xfer2([1,0x80,0]); raw=((r[1]&3)<<8)+r[2]
    finally: spi.close()
    moisture=round(raw*100/1023); pin=int(os.getenv('TINY_PUMP_PIN','26'))
    return {'moisture':moisture,'threshold':30,'pump':False,'state':'dry' if moisture<30 else 'ok','pump_pin':pin}
def plant_pump(on):
    require_control(); import RPi.GPIO as GPIO
    pin=int(os.getenv('TINY_PUMP_PIN','26')); GPIO.setmode(GPIO.BCM); GPIO.setup(pin,GPIO.OUT); GPIO.output(pin,GPIO.HIGH if on else GPIO.LOW); return {'pump':bool(on)}
def servo_write(angle):
    require_control(); import time, RPi.GPIO as GPIO
    angle=max(0,min(180,int(angle))); pin=18; GPIO.setmode(GPIO.BCM); GPIO.setup(pin,GPIO.OUT); pwm=GPIO.PWM(pin,50); pwm.start(0)
    try: pwm.ChangeDutyCycle(angle/18+2); time.sleep(.45)
    finally: pwm.stop(); GPIO.cleanup(pin)
    return {'angle':angle,'pin':pin}
def car_drive(direction,speed):
    require_control(); import RPi.GPIO as GPIO
    direction=str(direction).lower(); states={'stop':(0,0,0,0),'forward':(1,0,1,0),'back':(0,1,0,1),'left':(0,1,1,0),'right':(1,0,0,1)}
    if direction not in states: raise ValueError('direction not allow-listed')
    pins=(23,24,5,6); GPIO.setmode(GPIO.BCM)
    for p in pins: GPIO.setup(p,GPIO.OUT)
    for p,v in zip(pins,states[direction]): GPIO.output(p,GPIO.HIGH if v else GPIO.LOW)
    return {'direction':direction,'speed':int(speed)}
def io_command(b):
    cmd=b.get('cmd')
    if cmd=='gpio.list': return gpio_list()
    if cmd=='gpio.write': return gpio_write(b['pin'],b['value'])
    if cmd=='i2c.scan': return i2c_scan(b.get('bus',1))
    if cmd=='ina219.read': return ina219_read()
    if cmd=='dht.read': return dht_read()
    if cmd=='plant.read': return plant_read()
    if cmd=='plant.pump': return plant_pump(bool(b.get('on')))
    if cmd=='servo.write': return servo_write(b.get('angle',90))
    if cmd=='car.drive': return car_drive(b.get('direction','stop'),b.get('speed',50))
    if cmd=='ups.read': return {'percent':None,'voltage':None,'charging':None,'error':'UPS adapter project-specific'}
    if cmd=='compass.read': return {'heading':None,'error':'HMC5883L adapter project-specific'}
    raise ValueError(f'unknown IO command: {cmd}')

class H(BaseHTTPRequestHandler):
    server_version='TinyOLEDBridge/1.0'
    def log_message(self,fmt,*args): print('[bridge]',self.address_string(),fmt%args)
    def cors(self):
        o=self.headers.get('Origin','')
        if allowed_origin(o): self.send_header('Access-Control-Allow-Origin',o or '*'); self.send_header('Vary','Origin')
        self.send_header('Access-Control-Allow-Headers','Content-Type'); self.send_header('Access-Control-Allow-Methods','GET,POST,OPTIONS')
    def reply(self,status,data):
        raw=json.dumps(data,ensure_ascii=False).encode(); self.send_response(status); self.cors(); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def body(self): return json.loads(self.rfile.read(int(self.headers.get('Content-Length','0') or 0)) or b'{}')
    def do_OPTIONS(self): self.send_response(204); self.cors(); self.end_headers()
    def do_GET(self):
        try:
            p=urllib.parse.urlparse(self.path).path
            routes={'/health':lambda:{'ok':True,'control':CONTROL},'/api/wifi/scan':wifi_scan,'/api/docker':docker_list,'/api/systemd':systemd_list,'/api/ssh/alerts':ssh_alerts,'/api/pihole':pihole_stats,'/api/storage':storage_stats,'/api/apt/updates':apt_updates,'/api/email/unread':email_unread,'/api/telegram/messages':telegram_messages}
            if p not in routes: return self.reply(404,{'error':'not found'})
            self.reply(200,routes[p]())
        except Exception as e: self.reply(500,{'error':str(e)})
    def do_POST(self):
        try:
            p=urllib.parse.urlparse(self.path).path; b=self.body()
            if p=='/api/io': out=io_command(b)
            elif p=='/api/commands/run':
                cmds={'uptime':['uptime','-p'],'disk':['df','-h','/'],'memory':['free','-h'],'network':['ip','-brief','address']}; args=cmds.get(b.get('id'))
                if not args: return self.reply(400,{'error':'command id not allowed'})
                rc,out,err=run(args,5); out={'output':out or err,'returncode':rc}
            elif p=='/api/wifi/connect':
                require_control(); ssid=str(b.get('ssid','')); pw=str(b.get('password','')); args=['nmcli','device','wifi','connect',ssid]+(['password',pw] if pw else []); rc,o,e=run(args,20)
                if rc: raise RuntimeError(e or o)
                out={'ok':True,'output':o}
            elif p=='/api/docker/action':
                require_control(); a=b.get('action'); cid=str(b.get('id',''))
                if a not in {'start','stop'}: raise ValueError('action not allowed')
                rc,o,e=run(['docker',a,cid],10)
                if rc: raise RuntimeError(e or o)
                out={'ok':True}
            elif p=='/api/systemd/restart':
                require_control(); s=str(b.get('service',''))
                if s not in SERVICES: raise ValueError('service not allowed')
                rc,o,e=run(['systemctl','restart',s],10)
                if rc: raise RuntimeError(e or o)
                out={'ok':True}
            elif p=='/api/power':
                require_control(); a=b.get('action')
                if a not in {'reboot','shutdown'}: raise ValueError('action not allowed')
                subprocess.Popen(['systemctl','reboot' if a=='reboot' else 'poweroff']); out={'ok':True}
            elif p=='/api/pihole/toggle':
                require_control(); enabled=bool(b.get('enabled')); args=['pihole','enable'] if enabled else ['pihole','disable']; rc,o,e=run(args,10)
                if rc: raise RuntimeError(e or o)
                out={'ok':True,'enabled':enabled}
            else: return self.reply(404,{'error':'not found'})
            self.reply(200,out)
        except PermissionError as e: self.reply(403,{'error':str(e)})
        except Exception as e: self.reply(500,{'error':str(e)})

def main():
    print(f'TinyOLED bridge http://{HOST}:{PORT} control={CONTROL}')
    ThreadingHTTPServer((HOST,PORT),H).serve_forever()
if __name__=='__main__': main()
