from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
#import org.openqa.selenium.Keys
from pynput.mouse import Button, Controller as MouseController
from pynput import mouse
import time
import random
from pynput.mouse import Listener
from pynput.keyboard import Key, Controller

class Server:
    def __init__(self, name):
        self.name = name
        self.server_channels = []
        self.previous_notifications = []
        self.new_notifications = []
        self.prev_notif_checked = False
        self.last_msg_id = ""


brave_driver_path = r"C:\Users\ranso\Desktop\Tensorflow_Projects\chromedriver-win64\chromedriver.exe"
brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

# Create a Service instance for the ChromeDriver
service = Service(brave_driver_path, port=9000)

# Create Chrome options
options = webdriver.ChromeOptions()
options.binary_location = brave_path  # Set the Brave browser path
# Chrome options
options.add_experimental_option("excludeSwitches", ["enable-logging"])
#options.add_argument("--incognito")  # Add the incognito mode argument

# Start the Brave browser
driver = webdriver.Chrome(service=service, options=options)
actions = ActionChains(driver)

### Global Variables ###
active_character = "Sebi"
cur_server = 7
keyboard = Controller() 
characters = []
available_characters = []
discord_servers = []
tabs = driver.window_handles
active_channel = "general"

MENTIONED = "mentioned_d5deea" 
MESSAGE_CLASS = "message_d5deea"
MESSAGE_CONTENT = "messageContent_f9f2ca"
DISCORD_MSG_FORM = "form_a7d72e"
DISCORD_TEXTBOX = "emptyText_d4df8b"
DISCORD_CHANNEL_CLASS = "containerDefault_f6f816"
DISCORD_CONTAINER = "containerDefault_a08117"
CURRENT_CHANNEL = "titleWrapper_fc4f04"
USERNAME_CLASS = "username_f9f2ca"

#DISCORD LOGIN INFO
USERNAME = "[Your discord username here]"
PASSWORD = "[Your discord password here]"


#Functionality
def switch_browser_window(site):
    if site == "ST":
        driver.switch_to.window(tabs[0])
    else:
        driver.switch_to.window(tabs[1])

def click_by_id(id):
    while True:
        try:
            element = driver.find_element(By.ID, id)
            element.click()
            break
        except:
            time.sleep(1)

def click_options_menu_ST():
    click_by_id("options_button")

def delete_context():
    try:
        switch_browser_window("ST")
        time.sleep(.75)
        click_options_menu_ST()
        time.sleep(.75)
        click_by_id("option_delete_mes")
        time.sleep(.75)
        #click 2nd message
        msg2 = driver.find_element(By.CSS_SELECTOR, 'div[mesid="1"]')
        msg2.click()
        time.sleep(.75)
        click_by_id("dialogue_del_mes_ok")
        time.sleep(.75)
        switch_browser_window("discord")
        time.sleep(.75)
    except:
        try:
            click_by_id('dialogue_del_mes_cancel')
        except:
            print("failed")
        switch_browser_window('discord')

def delete_last_message():
    last_message_block = driver.find_elements(By.CLASS_NAME, "last_mes")[0]
    click_options_menu_ST()
    time.sleep(.75)
    click_by_id("option_delete_mes")
    time.sleep(.75)
    last_message_block.click()
    time.sleep(.75)
    click_by_id("dialogue_del_mes_ok")
    time.sleep(.75)


def click_server(name):
    # Correct the CSS selector string
    server_loc = f'div[data-dnd-name="{name}"]'
    
    # Find the element using the corrected CSS selector
    element = driver.find_element(By.CSS_SELECTOR, server_loc)
    
    # Click the found element
    element.click()

def click_channel(name):
    channel_loc = f'li[data-dnd-name="{name}"]'

    # Find the element using the corrected CSS selector
    elements = driver.find_elements(By.CSS_SELECTOR, channel_loc)
    element = "empty"
    for el in elements:
        if DISCORD_CONTAINER not in el.get_attribute('outerHTML'):
            element = el
            break
    
    # Click the found element
    try:
        element.click()
    except:
        pass

def swipe_msg(swipe):
    switch_browser_window('ST')
    time.sleep(.5)
    text_area = driver.find_element(By.ID, "send_textarea")
    if swipe == "l":
        text_area.send_keys(Keys.LEFT)
    else:
        text_area.send_keys(Keys.RIGHT)
    

def send_enter_button(id):
    text_area = driver.find_element(By.ID, id)
    text_area.send_keys(Keys.RETURN)

def get_characters():
    return driver.find_elements(By.CLASS_NAME, "character_name_block")

def show_available_characters(chars):
    names = []
    for char in characters:
        names.append(char.get_attribute("title"))
    cleaned_names = list(map(lambda x: x[12:], filter(lambda x: x != '', names)))
    return cleaned_names

def navigate_to_characters():
    global characters
    try:
        click_by_id("rightNavDrawerIcon")
        characters = driver.find_elements(By.CLASS_NAME, "ch_name")
        return "success"
    except:
        return "fail"
    
def switch_characters():
    click_by_id("rightNavDrawerIcon")
    click_by_id("rm_button_characters")
    
def click_character(x):
    character_boxes = driver.find_elements(By.CLASS_NAME, "character_select")
    for item in character_boxes:
        item_text = item.get_attribute("outerHTML")
        if x in item_text:
            item_id = "CharID" + item.get_attribute("chid")
            click_by_id(item_id)
            click_by_id("rightNavDrawerIcon")

def get_last_message():
    try:
        last_message_block = driver.find_elements(By.CLASS_NAME, "last_mes")
        child_elements = last_message_block[0].find_elements(By.TAG_NAME, "div")
        last_message_raw = ""
        for x in child_elements:
            if x.get_attribute("class") == "mes_text":
                last_message_raw = x.get_attribute("outerHTML")
                break
        last_message = last_message_raw.replace("<div class=\"mes_text\">", "").replace("<p>", "").replace("</p>", "\n").replace("<em>", "*").replace("</em>", "*").replace("<q>", "").replace("</q>", "").replace("</div>", "").replace("<br>", "\n")
    except:
        last_message = "failed"
    return last_message

def send_message_to_character(message):  
    # Locate the text area element by its ID (or use another locating strategy)
    text_area = driver.find_element(By.ID, "send_textarea")
    # Type text into the text area
    print(message)
    for x in range(len(message)):
        if x == 0:
            while True:
                try:
                    text_area.send_keys(message[x])
                    break
                except:
                    print("can't send text yet") 
        else:
            while True:
                try:
                    # Create an ActionChain to send Ctrl+Enter
                    text_area.send_keys(" ")
                    text_area.send_keys(message[x])
                    break
                except:
                    pop_ups = driver.find_elements(By.CLASS_NAME, 'popup-button-cancel')
                    for x in pop_ups:
                        x.click()
                    print("problem")
                    time.sleep(1)
    time.sleep(1)
    
    #Send the message
    click_by_id("send_but")

def send_text_to_area(id, message):
    message_sent = "Succeeded"
    try: 
        text_area = driver.find_element(By.ID, id)
        text_area.send_keys(message)
    except:
        message_sent = "Failed"
    return message_sent

def grab_prev_notifs():
    return driver.find_elements(By.CLASS_NAME, MENTIONED)

def add_prev_notifs(server_index, message):
    discord_servers[server_index].previous_notifications.append(message)

def simulate_typing_js(driver, text, delay=100):
    js_script = """
    function simulateTyping(text, delay) {
        var inputEvent = new Event('input', { bubbles: true });
        var target = document.activeElement;
        
        function typeChar(i) {
            if (i < text.length) {
                var char = text[i];
                var charCode = char.charCodeAt(0);

                var keydownEvent = new KeyboardEvent('keydown', {
                    bubbles: true,
                    cancelable: true,
                    key: char,
                    keyCode: charCode,
                    which: charCode
                });

                var keypressEvent = new KeyboardEvent('keypress', {
                    bubbles: true,
                    cancelable: true,
                    key: char,
                    keyCode: charCode,
                    which: charCode
                });

                var keyupEvent = new KeyboardEvent('keyup', {
                    bubbles: true,
                    cancelable: true,
                    key: char,
                    keyCode: charCode,
                    which: charCode
                });

                target.dispatchEvent(keydownEvent);
                target.dispatchEvent(keypressEvent);
                target.value += char;
                target.dispatchEvent(inputEvent);
                target.dispatchEvent(keyupEvent);

                setTimeout(function() { typeChar(i + 1); }, delay);
            }
        }

        function simulateCtrlEnter() {
            var ctrlKeydownEvent = new KeyboardEvent('keydown', {
                bubbles: true,
                cancelable: true,
                key: 'Control',
                code: 'ControlLeft',
                ctrlKey: true
            });

            var enterKeydownEvent = new KeyboardEvent('keydown', {
                bubbles: true,
                cancelable: true,
                key: 'Enter',
                code: 'Enter',
                ctrlKey: true
            });

            var inputEvent = new Event('input', { bubbles: true });
            
            target.dispatchEvent(ctrlKeydownEvent);
            target.dispatchEvent(enterKeydownEvent);
            target.value += '\\n';  // Add a newline character
            target.dispatchEvent(inputEvent);

            var ctrlKeyupEvent = new KeyboardEvent('keyup', {
                bubbles: true,
                cancelable: true,
                key: 'Control',
                code: 'ControlLeft',
                ctrlKey: false
            });

            var enterKeyupEvent = new KeyboardEvent('keyup', {
                bubbles: true,
                cancelable: true,
                key: 'Enter',
                code: 'Enter',
                ctrlKey: false
            });

            target.dispatchEvent(ctrlKeyupEvent);
            target.dispatchEvent(enterKeyupEvent);
        }

        typeChar(0);
        setTimeout(simulateCtrlEnter, delay * text.length); // Simulate Ctrl+Enter after typing
    }

    simulateTyping(arguments[0], arguments[1]);
    """
    driver.execute_script(js_script, text, delay)

def paste_text_js_ST(driver, element_selector, text):
    js_script = """
    function pasteText(element, text) {
        var inputEvent = new Event('input', { bubbles: true });
        var pasteEvent = new ClipboardEvent('paste', {
            bubbles: true,
            cancelable: true,
            clipboardData: new DataTransfer()
        });
        pasteEvent.clipboardData.setData('text/plain', text);
        
        element.dispatchEvent(pasteEvent);
        element.value += text;  // Fallback in case the paste event doesn't update the value
        element.dispatchEvent(inputEvent);
    }

    var target = document.querySelector(arguments[0]);
    pasteText(target, arguments[1]);
    """
    driver.execute_script(js_script, element_selector, text)

def paste_text_js(driver, text):
    js_script = """
    function pasteText(text) {
        var target = document.activeElement;
        var inputEvent = new Event('input', { bubbles: true });
        var pasteEvent = new ClipboardEvent('paste', {
            bubbles: true,
            cancelable: true,
            clipboardData: new DataTransfer()
        });
        pasteEvent.clipboardData.setData('text/plain', text);
        
        target.dispatchEvent(pasteEvent);
        target.value += text;  // Fallback in case the paste event doesn't update the value
        target.dispatchEvent(inputEvent);
    }

    pasteText(arguments[0]);
    """
    driver.execute_script(js_script, text)

def send_arrow_key_js(driver, key='ArrowUp'):
    js_script = """
    function sendArrowKey(key) {
        var target = document.activeElement;
        
        var keydownEvent = new KeyboardEvent('keydown', {
            bubbles: true,
            cancelable: true,
            key: key,
            code: key,
            which: key === 'ArrowUp' ? 38 : (key === 'ArrowDown' ? 40 : (key === 'ArrowLeft' ? 37 : 39)),
            keyCode: key === 'ArrowUp' ? 38 : (key === 'ArrowDown' ? 40 : (key === 'ArrowLeft' ? 37 : 39)),
        });

        var keyupEvent = new KeyboardEvent('keyup', {
            bubbles: true,
            cancelable: true,
            key: key,
            code: key,
            which: key === 'ArrowUp' ? 38 : (key === 'ArrowDown' ? 40 : (key === 'ArrowLeft' ? 37 : 39)),
            keyCode: key === 'ArrowUp' ? 38 : (key === 'ArrowDown' ? 40 : (key === 'ArrowLeft' ? 37 : 39)),
        });

        target.dispatchEvent(keydownEvent);
        target.dispatchEvent(keyupEvent);
    }

    sendArrowKey(arguments[0]);
    """
    driver.execute_script(js_script, key)

def send_ctrl_a_js(driver):
    js_script = """
    function sendCtrlA() {
        var target = document.activeElement;
        
        var keydownEvent = new KeyboardEvent('keydown', {
            bubbles: true,
            cancelable: true,
            key: 'a',
            code: 'KeyA',
            which: 65,
            keyCode: 65,
            ctrlKey: true
        });

        var keypressEvent = new KeyboardEvent('keypress', {
            bubbles: true,
            cancelable: true,
            key: 'a',
            code: 'KeyA',
            which: 65,
            keyCode: 65,
            ctrlKey: true
        });

        var keyupEvent = new KeyboardEvent('keyup', {
            bubbles: true,
            cancelable: true,
            key: 'a',
            code: 'KeyA',
            which: 65,
            keyCode: 65,
            ctrlKey: true
        });

        target.dispatchEvent(keydownEvent);
        target.dispatchEvent(keypressEvent);
        target.dispatchEvent(keyupEvent);
        
        // Fallback: If the events don't trigger the selection, we can try to select all content programmatically
        if (target.select) {
            target.select();
        } else if (window.getSelection && document.createRange) {
            var range = document.createRange();
            range.selectNodeContents(target);
            var selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);
        }
    }

    sendCtrlA();
    """
    driver.execute_script(js_script)

def press_enter_js(driver):
    js_script = """
    function pressEnter() {
        var target = document.activeElement;
        var enterEvent = new KeyboardEvent('keydown', {
            bubbles: true,
            cancelable: true,
            key: 'Enter',
            keyCode: 13,
            which: 13
        });
        
        target.dispatchEvent(enterEvent);
    }

    pressEnter();
    """
    driver.execute_script(js_script)

def open_silly_tavern():
    global available_characters
    driver.get("http://127.0.0.1:8000/")
    while True:
        loaded_characters = navigate_to_characters()
        available_characters = show_available_characters(characters)
        print(f"available_characters: {available_characters}")
        if loaded_characters == "success":
            break
        else:
            time.sleep(2)
    character_to_click = "[Character] " + active_character
    click_character(character_to_click)
    time.sleep(.5)
    click_by_id("rightNavDrawerIcon")
    time.sleep(.5)
    #Fix Persona
    click_by_id("persona-management-button")
    time.sleep(.5)
    wait = WebDriverWait(driver, 10)

    # Wait for the element to be clickable and then click it
    try:
        user_persona = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#user_avatar_block .avatar-container:nth-child(3)")
        ))
    except: 
        user_persona = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#user_avatar_block .avatar-container:nth-child(1)")
        ))
    user_persona.click()
    time.sleep(.5)
    click_by_id("persona-management-button")

    open_discord()

def collect_server_notifications(index):
    click_server(discord_servers[index].name)
    delete_context()
    channel_elements = driver.find_elements(By.CSS_SELECTOR, 'ul[aria-label="Channels"]')
    print(f"Channel elements {channel_elements}")
    channels = channel_elements[0].find_elements(By.CLASS_NAME, DISCORD_CHANNEL_CLASS)
    general_name = "general"
    for serv in channels:
        try:
            channel_name = serv.get_attribute('data-dnd-name')
            discord_servers[cur_server].server_channels.append(channel_name)
            if '(voice channel)' in driver.find_element(By.CSS_SELECTOR, f'li[data-dnd-name="{channel_name}"]').get_attribute('outerHTML') or 'containerDefault_a08117' in driver.find_element(By.CSS_SELECTOR, f'li[data-dnd-name="{channel_name}"]').get_attribute('outerHTML'):
                print("Skipping Irrelevant Channel")
                continue
            click_channel(channel_name)
            time.sleep(1)
            print("Grabbing Previous notifications")
            while True:
                try:
                    prev_notifs = grab_prev_notifs()
                    for notif in prev_notifs:
                        add_prev_notifs(cur_server, notif.get_attribute("data-list-item-id"))
                    break
                except:
                    time.sleep(1)
            if channel_name == 'general-chat':
                general_name = 'general-chat'
        except:
            print("Failure")
    click_channel(general_name)

def set_nickname(name):
    global active_character
    paste_text_js(driver, "/nick ")
    time.sleep(1)
    paste_text_js(driver, name)
    press_enter_js(driver)
    active_character = name

def open_discord():
    global tabs
    global discord_servers
    driver.execute_script("window.open('');")
    tabs = driver.window_handles
    time.sleep(1)
    driver.switch_to.window(tabs[1])
    print("Opening Discord")
    driver.get('https://discord.com/login')
    while True:
        try:
            print("Checking if the page is opened")
            driver.find_elements(By.CLASS_NAME, 'discordLogo_b83a05')
            break
        except:
            print("Page not loaded yet")
            time.sleep(1)
    time.sleep(2)
    inputs = driver.find_elements(By.TAG_NAME, 'input')
    text_area = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'inputDefault_f8bc55')))
    print('Logging in to Discord')
    send_text_to_area(inputs[0].get_attribute('id'), USERNAME)
    send_text_to_area(inputs[1].get_attribute('id'), PASSWORD)
    send_enter_button(inputs[1].get_attribute('id'))
    print("Logged In")
    while True:
        try:
            print("Checking if logged in")
            driver.find_elements(By.CLASS_NAME, 'tutorialContainer_f9623d')
            break
        except:
            print("Discord not opened yet")
            time.sleep(1)
    print("Successfully logged into Discord. Grabbing Servers...")
    #server_navigator = driver.find_element(By.TAG_NAME, 'nav')
    while True:
        try:
            servers_div = driver.find_elements(By.CSS_SELECTOR, 'div[aria-label="Servers"]')
            servers = servers_div[0].find_elements(By.CLASS_NAME, "listItem_c96c45")
            break
        except:
            time.sleep(1)

    #print(server_navigator)

    #servers = driver.find_elements(By.CSS_SELECTOR, '[data-dnd-name]')
    for server in servers:
        child_elements = server.find_elements(By.CSS_SELECTOR, '[data-dnd-name]')
        discord_servers.append(Server(child_elements[0].get_attribute('data-dnd-name')))
    print(f"Servers: {discord_servers[0], discord_servers[cur_server]}\nNumber of Servers: {len(discord_servers)}")
    print(discord_servers[cur_server].name)
    collect_server_notifications(cur_server)

    print(discord_servers)
    time.sleep(2)
    set_nickname(active_character)
open_silly_tavern()

def generate_new_msg(username):
    while True:
        #Wait for message to generate
        element = driver.find_element(By.ID, "mes_stop")
        while True:
            style_attribute = element.get_attribute("style")
            if "display: none" in style_attribute:
                time.sleep(.5)
                break
            else:
                time.sleep(1)
        time.sleep(1)
        bot_response = get_last_message()
        if active_character == "The Rogue Programmer":
            return bot_response
        if ("blockquote" not in bot_response) and ("<strong>" not in bot_response) and ("User:" not in bot_response) and ("user:" not in bot_response) and ("You:" not in bot_response) and ("you:" not in bot_response) and ("\'\'\'" not in bot_response) and (len(bot_response) > 10) and (len(bot_response) < 1500) and ("says:" not in bot_response) and (f"{username}:" not in bot_response):
            bot_response = bot_response.replace("<li>", "* ").replace("</li>", "").replace("<ul>", "").replace("</ul>", "").replace("<ol>", "").replace("</ol>", "")
            return bot_response
        else:
            swipe_msg("r")
            time.sleep(1)

def send_res_to_discord(bot_response):
    switch_browser_window("discord")
    time.sleep(1)
    #text_area = driver.find_elements(By.CLASS_NAME, DISCORD_MSG_FORM)
    #Response
    try:
        paste_text_js(driver, bot_response)
        press_enter_js(driver)
    except:
        print("js script failed")

    check_new_notifs = grab_prev_notifs()
    for notif in reversed(check_new_notifs):
        if notif.get_attribute("data-list-item-id") not in discord_servers[cur_server].previous_notifications:
            discord_servers[cur_server].previous_notifications.append(notif.get_attribute("data-list-item-id"))
        else:
            break

def send_edit_to_discord(bot_response):
    switch_browser_window("discord")
    time.sleep(1)
    #text_area = driver.find_elements(By.CLASS_NAME, DISCORD_MSG_FORM)
    #Response
    bot_response = bot_response.replace("&gt;", ">").replace("&lt;", "<").replace("<ol>", "").replace("</ol>", "").replace("<li>", "").replace("</li>", "").replace(": " + username, "")
    try:
        send_arrow_key_js(driver)
        time.sleep(.5)
        send_ctrl_a_js(driver)
        time.sleep(.5)
        paste_text_js(driver, bot_response)
        press_enter_js(driver)
    except:
        print("js script failed")

    check_new_notifs = grab_prev_notifs()
    for notif in reversed(check_new_notifs):
        if notif.get_attribute("data-list-item-id") not in discord_servers[cur_server].previous_notifications:
            discord_servers[cur_server].previous_notifications.append(notif.get_attribute("data-list-item-id"))
        else:
            break
    
def sanitize_text(text):
    return ''.join(char for char in text if ord(char) < 65536)

def clear_old_notifs():
    try:
        for notif in reversed(check_new_notifs):
            if notif.get_attribute("data-list-item-id") not in discord_servers[cur_server].previous_notifications:
                discord_servers[cur_server].previous_notifications.append(notif.get_attribute("data-list-item-id"))
            else:
                break
    except:
        print("Failed to clear old notifications")

while True:
    at_mention = "@" + active_character
    time.sleep(1) #Sleep to load new page
    
    discord_servers[cur_server].previous_notifications

    check_new_notifs = grab_prev_notifs()
    if len(check_new_notifs) == 0:
        continue
    if check_new_notifs[-1].get_attribute("data-list-item-id") not in discord_servers[cur_server].previous_notifications:
        #New message detected in current server
        '''reply_button = check_new_notifs[-1].find_element(By.CSS_SELECTOR, 'div[aria-label="Reply"]')
        reply_button.click()'''

        #Grab the message:
        message_content = ""
        message_spans = check_new_notifs[-1].find_elements(By.CLASS_NAME, MESSAGE_CONTENT)[-1].find_elements(By.CSS_SELECTOR, "span, em")

        is_em_open = False
        for span in message_spans:
            if span.tag_name == 'em':
                if not is_em_open:
                    message_content += "*"
                    is_em_open = True
                else:
                    message_content += "*"
                    is_em_open = False
            elif span.tag_name == 'span':
                message_content += span.get_attribute("textContent")

        # Ensure to close any open <em> tags at the end of the message
        if is_em_open:
            message_content += "*"
########User Commands
        print(message_content)
        message_content = sanitize_text(message_content)
        if "!delcon" in message_content:
            try:
                delete_context()
                paste_text_js(driver, "Memory Deleted.")
                press_enter_js(driver)
            except:
                click_by_id("dialogue_del_mes_cancel")
                switch_browser_window('discord')
            check_new_notifs = grab_prev_notifs()
            clear_old_notifs()
            continue
        elif "!right" in message_content.lower():
            swipe_msg('r')
            time.sleep(1)
            bot_response = generate_new_msg(username)
            send_edit_to_discord(bot_response)
            continue
        elif "!left" in message_content.lower():
            swipe_msg('l')
            time.sleep(1)
            bot_response = get_last_message()
            send_edit_to_discord(bot_response)
            continue
        elif "!quit" in message_content.lower():
            paste_text_js(driver, "Shutting down...")
            time.sleep(1)
            driver.quit()
            break
        elif "!server" in message_content.lower():
            server = message_content.split(' ')
            for x in server:
                try:
                    collect_server_notifications(int(x))
                    break
                except:
                    pass
            continue
        elif "!channel" in message_content.lower():
            channel = message_content.split(' ')
            for x in channel:
                try:
                    click_channel(x)
                    active_channel = x
                    print(x)
                except:
                    pass
            delete_context()
            clear_old_notifs()
            continue
        elif "!nick" in message_content.lower():
            username = check_new_notifs[-1].find_elements(By.CLASS_NAME, USERNAME_CLASS)[-1].get_attribute("textContent")
            
            message_content = message_content.replace("!nick ", "").replace(f"@{active_character}", "")
            for x in available_characters:
                if x in message_content:
                    message_content = message_content.replace(x, "").replace("@", "")
            set_nickname(message_content)
            clear_old_notifs()
            continue
        elif "!userphone" in message_content.lower():
            pass
        username = "username not found"
        try:
            username = check_new_notifs[-1].find_elements(By.CLASS_NAME, USERNAME_CLASS)[-1].get_attribute("textContent")
            bot_response = ""
            message_content = "*" + username + " says:* " + message_content
            message_list = sanitize_text(message_content).split("\n")
            if active_channel != "chat-ai":
                try:
                    paste_text_js(driver, "@")
                    time.sleep(1)
                    paste_text_js(driver, sanitize_text(username))
                    time.sleep(1)
                    press_enter_js(driver)
                except:
                    pass
        except:
            bot_response = ""
            message_content = message_content
            message_list = sanitize_text(message_content).split("\n")
            if active_channel != "chat-ai":
                try:
                    paste_text_js(driver, "@")
                    time.sleep(1)
                    paste_text_js(driver, sanitize_text(username))
                    time.sleep(1)
                    press_enter_js(driver)
                except:
                    pass
            print("Failed to grab username")
        
        #Navigate to Silly Tavern
        switch_browser_window("ST")
        send_message_to_character(message_list)
        time.sleep(1)
        bot_response = generate_new_msg(username)
        bot_response = bot_response.replace("&gt;", ">").replace("&lt;", "<").replace("<ol>", "").replace("</ol>", "").replace("<li>", "").replace("</li>", "").replace(": " + username, "")
        #Navigate back to discord
        send_res_to_discord(bot_response)
    
    '''
    if options == "switch":
        switch_characters()
        active_character = "None"
    elif options == "quit":
        driver.quit()
        break
    '''
