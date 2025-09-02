# 🔎 edu.in Random Subdomain Liveness Scanner

একটি **Asynchronous Python Tool** যা র‍্যান্ডম `.edu.in` সাবডোমেইন জেনারেট করে,  
তারপর DNS ও HTTP চেক করে দেখে কোন ডোমেইনগুলো **লাইভ** আছে।  
লাইভ ডোমেইনগুলোকে `edu_site_found.txt` ফাইলে সেভ করে।  
এটি সম্পূর্ণভাবে **asyncio + aiohttp** ভিত্তিক, খুব দ্রুত ও কার্যকর।

---

## ✨ Features

✅ র‍্যান্ডম `.edu.in` সাবডোমেইন জেনারেট করে  
✅ DNS রেজল্যুশন চেক করে  
✅ HTTP/HTTPS লিভনেস চেক করে  
✅ কোনো ডুপ্লিকেট ডোমেইন সেভ হয় না  
✅ কালারফুল আউটপুট (Colorama)  
✅ কাস্টমাইজেবল সাবডোমেইন লেন্থ, ব্যাচ সাইজ, কনকারেন্সি, টাইমআউট  
✅ লাইভ ডোমেইনগুলো আলাদা ফাইলে সেভ হয়  

---

## 📂 Project Structure

```
EduScanner/
│
├── edu_scanner.py       # মূল স্ক্রিপ্ট
├── edu_site_found.txt   # লাইভ ডোমেইন লিস্ট (অটো জেনারেটেড)
└── README.md            # ডকুমেন্টেশন
```

---

## ⚡ Installation

### **১. রিপোজিটরি ক্লোন করো**
```bash
git clone https://github.com/nusaibnull/EduScanner.git
cd EduScanner
```

### **২. ডিপেন্ডেন্সি ইন্সটল করো**
```bash
pip install aiohttp colorama
```

---

## 🚀 Usage

### **বেসিক রান**
```bash
python3 scanner.py
```

ডিফল্টভাবে স্ক্রিপ্ট:
- প্রতি ব্যাচে **২০০** র‍্যান্ডম সাবডোমেইন জেনারেট করবে
- সাবডোমেইনের দৈর্ঘ্য হবে **৩ অক্ষর**
- একসাথে **১০০টি ওয়ার্কার** রান করবে
- প্রতিটি রিকোয়েস্টের টাইমআউট হবে **৬ সেকেন্ড**
- লাইভ ডোমেইনগুলো `edu_site_found.txt` ফাইলে সেভ হবে
- **১০০০** লাইভ ডোমেইন পাওয়ার পর থেমে যাবে

---

### **অ্যাডভান্সড ইউজেজ**

```bash
python3 edu_scanner.py --count 500 --length 4 --concurrency 200 --timeout 8 --target 2000 --output live_edu_sites.txt
```

#### **অপশনগুলোর ব্যাখ্যা:**

| Flag            | ডিফল্ট | বর্ণনা |
|-----------------|--------|---------|
| `--count`      | 200    | প্রতি ব্যাচে কতগুলো সাবডোমেইন জেনারেট হবে |
| `--length`     | 3      | সাবডোমেইনের দৈর্ঘ্য (অক্ষর সংখ্যা) |
| `--concurrency`| 100    | একসাথে কয়টা ওয়ার্কার চলবে |
| `--timeout`    | 6      | HTTP রিকোয়েস্টের টাইমআউট (সেকেন্ড) |
| `--target`     | 1000   | কতগুলো লাইভ ডোমেইন খুঁজে পেলে থামবে |
| `--output`     | edu_site_found.txt | লাইভ ডোমেইন সেভ করার ফাইল |

---

## 🛠️ How It Works

### **১. র‍্যান্ডম সাবডোমেইন জেনারেট করা**
```python
def make_domain(length: int) -> str:
    return "".join(random.choice(ALPHABET) for _ in range(length)) + ".edu.in"
```
- যেমন, ৩ অক্ষরের জন্য উদাহরণ: `abc.edu.in`, `xyz.edu.in`

---

### **২. DNS রেজল্যুশন চেক**
```python
await loop.getaddrinfo(host, 80, type=socket.SOCK_STREAM)
```
- ডোমেইন রেজলভ না হলে স্কিপ করে দেয়।

---

### **৩. HTTP/HTTPS লিভনেস চেক**
```python
async with session.get(url, allow_redirects=True, timeout=timeout)
```
- HTTPS, HTTP, এবং `www.` প্রিফিক্সসহ একাধিকভাবে চেষ্টা করে।
- ২০০ ≤ status < ৪০০ হলে ডোমেইন **লাইভ** ধরা হয়।

---

### **৪. ডুপ্লিকেট এভয়েড**
- পুরনো `edu_site_found.txt` থেকে আগের ডোমেইনগুলো লোড করে।
- নতুন কোনো ডোমেইন লাইভ হলে তবেই সেভ হয়।

---

### **৫. কালারফুল আউটপুট**
- 🟢 **লাইভ ডোমেইন** → সবুজ
- 🟡 **DNS OK, কিন্তু HTTP ডাউন** → হলুদ
- 🔴 **DNS Fail** → লাল

---

## 📄 Example Output

```
[+] LIVE (1/1000): abc.edu.in
[!] DNS ok, HTTP not alive: xyz.edu.in
[-] DNS fail: pqr.edu.in
```

---

## ⚠️ Disclaimer

> **শুধুমাত্র রিসার্চ, সিকিউরিটি টেস্টিং ও এডুকেশনাল উদ্দেশ্যে ব্যবহার করুন।**  
> কোনো অননুমোদিত ডোমেইন স্ক্যান, হ্যাকিং বা আক্রমণ আইনত দণ্ডনীয়।  
> ডেভেলপার কোনো ক্ষতির জন্য দায়ী নয়।

---

## 👨‍💻 Author

**nullBr@!N**   
