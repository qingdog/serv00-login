import json
import asyncio
from pyppeteer import launch
from datetime import datetime, timedelta
import aiofiles
import random
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# 从环境变量中获取 Telegram Bot Token 和 Chat ID
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
# github秘密环境变量
ACCOUNTS_JSON = "./accounts.json"
# 如果使用本地指定地址的浏览器
chrome_executable_path = None
is_headless = True
if TELEGRAM_CHAT_ID == "xxx":
    chrome_executable_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    is_headless = False

# 全局浏览器实例
browser = None
# telegram消息
message = 'serv00&ct8自动化脚本运行\n'


def format_to_iso(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')


async def delay_time(ms):
    await asyncio.sleep(ms / 1000)


async def login(username, password, panel):
    global browser

    page = None  # 确保 page 在任何情况下都被定义
    service_name = 'ct8' if 'ct8' in panel else 'serv00'
    try:
        if not browser:
            browser = await launch(headless=is_headless, args=['--no-sandbox', '--disable-setuid-sandbox'],
                                   executablePath=chrome_executable_path)
        # 获取所有打开的页面
        pages = await browser.pages()
        for p in pages:
            page = p
            break
        # 全局设置导航超时时间为 60 秒
        page.setDefaultNavigationTimeout(60000*3)

        # 等待1s再打开页面
        delay = random.randint(500, 1000)
        await delay_time(delay)

        if page is None:
            page = await browser.newPage()
        url = f'https://{panel}/login/?next=/'
        await page.goto(url)

        username_input = await page.querySelector('#id_username')
        if username_input:
            # 在浏览器页面的上下文中执行 JavaScript 操作 username_input作为参数传入清空输入框
            await page.evaluate('''(input) => input.value = ""''', username_input)

        await page.type('#id_username', username)
        await page.type('#id_password', password)

        login_button = await page.querySelector('#submit')
        if login_button:
            await login_button.click()
        else:
            raise Exception('无法找到登录按钮')

        await page.waitForNavigation()

        is_logged_in = await page.evaluate('''() => {
            const logoutButton = document.querySelector('a[href="/logout/"]');
            return logoutButton !== null;
        }''')

        return is_logged_in

    except Exception as e:
        print(f'{service_name} 账号 {username} 登录时出现错误: {e}')
        return False

    finally:
        if page:
            await page.close()


async def main():
    global message
    message = 'serv00&ct8自动化脚本运行\n'

    try:
        async with aiofiles.open(f'{ACCOUNTS_JSON}', mode='r', encoding='utf-8') as f:
            accounts_json = await f.read()
        accounts = json.loads(accounts_json)
    except Exception as e:
        print(f'读取 {ACCOUNTS_JSON} 文件时出错: {e}')
        return

    for account in accounts:
        username = account['username']
        password = account['password']
        panel = account['panel']

        service_name = 'ct8' if 'ct8' in panel else 'serv00'
        # ===登录===
        is_logged_in = await login(username, password, panel)

        if is_logged_in:
            now_utc = format_to_iso(datetime.utcnow())
            now_beijing = format_to_iso(datetime.utcnow() + timedelta(hours=8))
            success_message = f'{service_name}账号 {username} 于北京时间 {now_beijing}（UTC时间 {now_utc}）登录成功！'
            message += success_message + '\n'
            print(success_message)
        else:
            message += f'{service_name}账号 {username} 登录失败，请检查{service_name}账号和密码是否正确。\n'
            print(f'{service_name}账号 {username} 登录失败，请检查{service_name}账号和密码是否正确。')

        delay = random.randint(1000, 8000)
        await delay_time(delay)

    message += f'所有{service_name}账号登录完成！'
    await send_telegram_message(message)
    print(f'所有{service_name}账号执行完成，请检查是否登录成功！')


async def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': '问题反馈❓',
                        'url': 'https://t.me/yxjsjl'
                    }
                ]
            ]
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"发送消息到Telegram失败: {response.text}")
    except Exception as e:
        print(f"发送消息到Telegram时出错: {e}")


if __name__ == '__main__':
    asyncio.run(main())
