import os
import json
import asyncio
import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from pydantic import BaseModel, Field
import argparse
from deep_translator import GoogleTranslator
from slugify import slugify
import time
from enum import Enum

# Строга типізація таксономії. Це гарантує, що LLM не вигадає неіснуючу папку.
class TargetDir(str, Enum):
    fundamentals = "fundamentals" # Психологія, принципи, верифікація/валідація
    sdlc = "sdlc" # Agile, Waterfall, V-модель, стадії розробки
    test_levels = "test_levels" # Модульне, інтеграційне, системне, приймальне
    test_types = "test_types" # Функціональне, регресійне, димне, навантажувальне
    test_design = "test_design" # Техніки дизайну, матриці покриття
    test_management = "test_management" # Тест-плани, стратегії, баг-репорти
    web_technologies = "web_technologies" # HTML, HTTP, TCP/IP, Cookie, мікросервіси/моноліт
    api_testing = "api_testing" # JSON, API комунікація
    databases = "databases" # SQL для тестування
    automation_tools = "automation_tools" # Git, CI/CD, XPath, вибір інструментів
    trash = "trash" # Чиста розробка (ООП, RxJava, Android Studio) або залізо

class ArticleDecision(BaseModel):
    id: int
    keep: bool = Field(
        description="True для всього, що стосується QA, включаючи мережеві протоколи та архітектуру. False ТІЛЬКИ для глибокої розробки (RxJava, ООП) або нерелевантних тем."
    )
    target_dir: TargetDir = Field(
        description="Вибір папки згідно зі строгою таксономією. Якщо keep=False, обов'язково 'trash'."
    )

class BatchDecision(BaseModel):
    decisions: list[ArticleDecision]

def get_intelligent_name(ukr_text: str, url: str) -> str:
    try:
        eng_text = GoogleTranslator(source='uk', target='en').translate(ukr_text)
        safe = slugify(eng_text)
    except Exception:
        safe = slugify(ukr_text)
        
    if not safe:
        safe = slugify(url.split('/')[-2]) if url.endswith('/') else slugify(url.split('/')[-1])
        if not safe:
            safe = f"unnamed-article-{hash(url) % 10000}"
    return safe

async def discover(start_url: str, output_file: str):
    print(f"[*] Етап розвідки: Завантажуємо {start_url}")
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(start_url, follow_redirects=True)
        soup = BeautifulSoup(resp.text, 'lxml')
        
        menu = soup.find('ul', class_='innermenu')
        if not menu:
            print("[!] Не знайдено навігаційне меню.")
            return
            
        links = menu.find_all('a')
        discovered = []
        seen_urls = set()
        
        for a in links:
            url = a.get('href')
            title = a.get_text(strip=True)
            if not url or url == '#' or url in seen_urls:
                continue
            seen_urls.add(url)
            discovered.append({"url": url, "title": title})
            
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in discovered:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        print(f"[+] Знайдено унікальних статей: {len(discovered)}. Збережено у {output_file}")

def classify(input_file: str, output_file: str):
    print(f"[*] Етап класифікації: Читаємо {input_file}")
    api_key = os.environ.get("GEMINI_API_KEY")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        articles = [json.loads(line) for line in f]
        
    classified = []
    
    if not api_key:
        print("[!] GEMINI_API_KEY відсутній. Перервано.")
        return
        
    print("[+] Запуск реальної LLM (Google GenAI) з Batch-обробкою...")
    from google import genai
    from google.genai import types
    client = genai.Client()
    
    for i, a in enumerate(articles):
        a['id'] = i
        
    chunk_size = 30
    request_times = []
    
    for i in range(0, len(articles), chunk_size):
        current_time = time.time()
        request_times = [t for t in request_times if current_time - t < 60]
        
        if len(request_times) >= 4:
            sleep_time = 60 - (current_time - request_times[0])
            if sleep_time > 0:
                print(f"[*] Обмеження API (5 RPM): очікування {sleep_time:.1f} сек...")
                time.sleep(sleep_time)
                # Після очікування ліміт скидається для найстарішого запиту
        
        request_times.append(time.time())
        
        chunk = articles[i:i+chunk_size]
        prompt_data = [{"id": a['id'], "title": a['title'], "url": a['url']} for a in chunk]
        
        prompt = f"Analyze these articles for a QA Engineer Knowledge Base.\n\n{json.dumps(prompt_data, ensure_ascii=False)}"
        
        print(f"[*] Відправляємо пакет {i//chunk_size + 1} ({len(chunk)} статей)...")
        try:
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=BatchDecision,
                    temperature=0.1
                ),
            )
            res_dict = json.loads(response.text)
            decision_map = {d['id']: d for d in res_dict['decisions']}
            
            for a in chunk:
                d = decision_map.get(a['id'])
                if d:
                    a['keep'] = d['keep']
                    a['target_dir'] = d['target_dir']
                else:
                    a['keep'] = False
                    a['target_dir'] = 'error'
                
                classified.append(a)
                status = "v" if a['keep'] else "x"
                print(f"  {status} {a['title'][:45]}... -> {a['target_dir']}")
                
        except Exception as e:
            print(f"[!] Помилка пакета: {e}")
            for a in chunk:
                a['keep'] = False
                a['target_dir'] = 'error'
                classified.append(a)
            
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in classified:
            item.pop('id', None)
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    print(f"[+] Класифікацію завершено. Маніфест згенеровано: {output_file}")

async def download_article(client, item, base_dir):
    if not item.get("keep"):
        return
        
    url = item['url']
    target_dir = os.path.join(base_dir, item['target_dir'])
    os.makedirs(target_dir, exist_ok=True)
    
    try:
        resp = await client.get(url, follow_redirects=True)
        soup = BeautifulSoup(resp.text, 'lxml')
        
        title_tag = soup.find('h1')
        title_ukr = title_tag.get_text(strip=True) if title_tag else item['title']
        safe_filename = get_intelligent_name(title_ukr, url)
        
        content_container = soup.find('div', class_='single-knowledge-base-content')
        if not content_container:
            return
            
        for unwanted in content_container.find_all(['script', 'style', 'noscript', 'meta', 'link', 'iframe']):
            unwanted.decompose()
        for sidebar in content_container.find_all('div', class_=['sidebar', 'sidebar-mobile', 'menu-block']):
            sidebar.decompose()
            
        markdown_text = md(str(content_container), heading_style="ATX")
        
        filepath = os.path.join(target_dir, f"{safe_filename}.md")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {title_ukr}\n\n**Source:** {url}\n\n---\n\n{markdown_text}")
        print(f"[+] Збережено: {safe_filename}.md -> {target_dir}")
    except Exception as e:
        print(f"[!] Помилка завантаження {url}: {e}")

async def download(input_file: str, base_dir: str):
    print(f"[*] Етап завантаження: Читаємо маніфест {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        articles = [json.loads(line) for line in f if json.loads(line).get("keep")]
        
    print(f"[*] Схвалено статей: {len(articles)}. Починаємо паралельне завантаження...")
    async with httpx.AsyncClient(timeout=20.0, limits=httpx.Limits(max_connections=5)) as client:
        tasks = [download_article(client, a, base_dir) for a in articles]
        await asyncio.gather(*tasks)
    print(f"[+] Усі файли успішно завантажені!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI-Driven ETL Pipeline CLI")
    parser.add_argument('action', choices=['discover', 'classify', 'download'])
    parser.add_argument('--url', default="https://qalight.ua/baza-znan/")
    parser.add_argument('--input', default="raw_discovery.jsonl")
    parser.add_argument('--output', default="manifest.jsonl")
    parser.add_argument('--outdir', default="../dataset_v2")
    
    args = parser.parse_args()
    
    if args.action == 'discover':
        asyncio.run(discover(args.url, args.output))
    elif args.action == 'classify':
        classify(args.input, args.output)
    elif args.action == 'download':
        asyncio.run(download(args.input, args.outdir))
