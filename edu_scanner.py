#!/usr/bin/env python3
"""
edu.bd random subdomain liveness scanner with colorama (No Duplicates)
"""
import argparse
import asyncio
import random
import socket
from typing import Set

import aiohttp
from colorama import init, Fore, Style

init(autoreset=True)  # colorama init

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
]

def make_domain(length: int) -> str:
    return "".join(random.choice(ALPHABET) for _ in range(length)) + ".edu.in"

async def dns_resolves(host: str) -> bool:
    loop = asyncio.get_event_loop()
    try:
        await loop.getaddrinfo(host, 80, type=socket.SOCK_STREAM)
        return True
    except Exception:
        return False

async def http_alive(session: aiohttp.ClientSession, host: str, timeout: int) -> bool:
    schemes = [
        f"https://{host}",
        f"http://{host}",
        f"https://www.{host}",
    ]
    for url in schemes:
        try:
            async with session.get(url, allow_redirects=True, timeout=timeout) as resp:
                if 200 <= resp.status < 400:
                    return True
        except Exception:
            continue
    return False


async def worker(queue: "asyncio.Queue[str]", session: aiohttp.ClientSession, timeout: int, out_file, lock: asyncio.Lock, live_counter: dict, target: int, visited_sites: Set):
    while True:
        if live_counter['count'] >= target:
            break

        host = await queue.get()
        try:
            # যদি আগে থেকেই ভিজিটেড হয়, স্কিপ করব
            if host in visited_sites:
                queue.task_done()
                continue

            if await dns_resolves(host):
                alive = await http_alive(session, host, timeout)
                if alive:
                    async with lock:
                        if live_counter['count'] < target and host not in visited_sites:
                            visited_sites.add(host)
                            out_file.write(host + "\n")
                            out_file.flush()
                            live_counter['count'] += 1
                            print(f"{Fore.GREEN}[+] LIVE ({live_counter['count']}/{target}): {host}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}[!] DNS ok, HTTP not alive: {host}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] DNS fail: {host}{Style.RESET_ALL}")
        finally:
            queue.task_done()

async def main():
    ap = argparse.ArgumentParser(description="Random edu.in subdomain liveness scanner with colorama (No Duplicates)")
    ap.add_argument("--count", type=int, default=200, help="Domains per batch (default: 200)")
    ap.add_argument("--length", type=int, default=3, help="Length of subdomain (default: 4)")
    ap.add_argument("--concurrency", type=int, default=100, help="Number of workers (default: 100)")
    ap.add_argument("--timeout", type=int, default=6, help="HTTP timeout (default: 6)")
    ap.add_argument("--output", type=str, default="edu_site_found.txt", help="Output file")
    ap.add_argument("--target", type=int, default=1000, help="Target live domains")
    args = ap.parse_args()

    print(f"[*] Target: {args.target} live domains")
    print(f"[*] Generating {args.count} random {args.length}-letter subdomains per batch")

    headers = {"User-Agent": random.choice(USER_AGENTS)}
    conn = aiohttp.TCPConnector(ssl=False, limit=0, ttl_dns_cache=300)
    timeout = aiohttp.ClientTimeout(total=None, connect=args.timeout, sock_connect=args.timeout, sock_read=args.timeout)

    queue: asyncio.Queue[str] = asyncio.Queue()
    lock = asyncio.Lock()
    live_counter = {'count': 0}
    visited_sites = set()

    # পুরোনো ফাইল থেকে ডুপ্লিকেট ডোমেইন রিড করে সেটে রাখব
    try:
        with open(args.output, "r", encoding="utf-8") as f:
            for line in f:
                visited_sites.add(line.strip())
    except FileNotFoundError:
        pass

    with open(args.output, "a", encoding="utf-8") as out_file:
        async with aiohttp.ClientSession(connector=conn, timeout=timeout, headers=headers) as session:
            workers = [asyncio.create_task(worker(queue, session, args.timeout, out_file, lock, live_counter, args.target, visited_sites)) for _ in range(args.concurrency)]
            
            while live_counter['count'] < args.target:
                for _ in range(args.count):
                    queue.put_nowait(make_domain(args.length))
                await asyncio.sleep(0.1)

            await queue.join()
            for w in workers:
                w.cancel()
            await asyncio.gather(*workers, return_exceptions=True)

    print(f"{Fore.GREEN}[✓] Done. Live domains saved to: {args.output}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Interrupted by user.{Style.RESET_ALL}")
