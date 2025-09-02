#!/usr/bin/env python3
"""
TXT Duplicate Remover with Progress Bar & Colorful Output.
Author: RJ's Buddy 😎
"""
import os
import argparse
from colorama import Fore, Style, init
from tqdm import tqdm

# Colorama initialize
init(autoreset=True)

def remove_duplicates(input_file: str, output_file: str):
    # ইনপুট ফাইল চেক করব
    if not os.path.exists(input_file):
        print(f"{Fore.RED}[!] Input file not found: {input_file}{Style.RESET_ALL}")
        return

    # ফাইল পড়া
    with open(input_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    total_lines = len(lines)
    if total_lines == 0:
        print(f"{Fore.RED}[!] The file is empty: {input_file}{Style.RESET_ALL}")
        return

    print(f"{Fore.CYAN}[*] Total lines found: {total_lines}{Style.RESET_ALL}")

    seen = set()
    unique_lines = []

    # প্রগ্রেস বার সহ ডুপ্লিকেট রিমুভ
    with tqdm(total=total_lines, desc="Checking Duplicates", unit="line", colour="cyan") as pbar:
        for line in lines:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)
            pbar.update(1)

    # ইউনিক লাইন সেভ করা হবে
    with open(output_file, "w", encoding="utf-8") as f:
        for line in unique_lines:
            f.write(line + "\n")

    print(f"\n{Fore.GREEN}[✓] Done!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Unique lines saved to: {output_file}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[*] Total Unique: {len(unique_lines)} | Removed Duplicates: {total_lines - len(unique_lines)}{Style.RESET_ALL}")

def main():
    ap = argparse.ArgumentParser(description="TXT Duplicate Remover with Progress Bar")
    ap.add_argument("-i", "--input", type=str, default="edu_site_found.txt", help="Input file (default: input.txt)")
    ap.add_argument("-o", "--output", type=str, default="edu_unique_output.txt", help="Output file (default: unique_output.txt)")
    args = ap.parse_args()

    remove_duplicates(args.input, args.output)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Interrupted by user.{Style.RESET_ALL}")
