from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-extensions")     

print("Inisialisasi WebDriver...")
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    print("Browser berhasil dibuka!")
except Exception as e:
    print(f"Gagal membuka browser: {e}")
    exit()

def login_twitter(username, password):
    print("Mencoba membuka halaman login Twitter...")
    driver.get("https://x.com/i/flow/login") 
    wait = WebDriverWait(driver, 20)


    try:
        print("Menunggu field username...")
        username_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='username']")))
        username_field.send_keys(username)
        username_field.send_keys(Keys.RETURN)
        print("Username dikirim.")
        time.sleep(2)
    except Exception as e:
        print(f"Gagal menemukan field username: {e}")
        driver.save_screenshot("username_error.png")
        return False


    try:
        print("Menunggu field password...")
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        print("Password dikirim.")
        time.sleep(3)
    except Exception as e:
        print(f"Gagal menemukan field password: {e}")
        driver.save_screenshot("password_error.png")
        return False

    try:
        print("Memverifikasi login...")
        wait.until(lambda driver: "x.com" in driver.current_url and "login" not in driver.current_url)
        print(f"URL saat ini: {driver.current_url}")
        if "home" in driver.current_url:
            print("Login berhasil, berada di beranda!")
        else:
            print("Login berhasil, tapi mungkin bukan beranda.")
        return True
    except Exception as e:
        print(f"Login gagal: {e}")
        driver.save_screenshot("login_error.png")
        print(f"URL saat ini: {driver.current_url}")
        return False
def scrape_tweets(query="kaburajadulu", max_tweets=200):
    print(f"Memulai scraping untuk query: {query}")
    search_url = f"https://x.com/search?q={query}&src=typed_query&f=live"
    driver.get(search_url)
    time.sleep(5)  
    tweets = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    wait = WebDriverWait(driver, 20)

    while len(tweets) < max_tweets:
        try:
            tweet_elements = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//article[@data-testid='tweet']"))
            )
            print(f"Sedang mengambil {len(tweet_elements)} tweet baru... Total saat ini: {len(tweets)}")

            for tweet in tweet_elements:
                try:
                    text_elements = tweet.find_elements(By.XPATH, ".//div[@lang]")
                    text = text_elements[0].text.replace('\n', ' ') if text_elements else ""
                    print(f"Tweet text: {text}")  
                    if not text:
                        print("Text kosong, skip tweet.")
                        continue


                    time_elem = tweet.find_element(By.XPATH, ".//time")
                    created_at = time_elem.get_attribute("datetime")
                    print(f"Created at: {created_at}")  

                    author_link = tweet.find_element(By.XPATH, ".//a[@role='link']")
                    author_id = author_link.get_attribute("href").split('/')[-1]
                    print(f"Author ID: {author_id}") 

                    tweet_data = {'id': len(tweets) + 1, 'author_id': author_id, 'created_at': created_at, 'text': text}
                    if tweet_data not in tweets:
                        tweets.append(tweet_data)
                        print(f"Tweet ditambahkan: {tweet_data}")

                except Exception as e:
                    print(f"Error saat memproses tweet: {e}")  
                    continue


            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5) 
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("Tidak ada tweet baru. Scraping selesai.")
                break
            last_height = new_height

        except Exception as e:
            print(f"Error saat scraping: {e}")
            break
    return tweets[:max_tweets] 
try:
    if login_twitter("email", "password"):  
        tweets = scrape_tweets(query="kaburajadulu", max_tweets=200)  
        csv_file = 'kaburajadulu.csv'
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'author_id', 'created_at', 'text'])
            writer.writeheader()
            writer.writerows(tweets)
        print(f"Scraping selesai! {len(tweets)} tweet berhasil disimpan ke {csv_file}")
    else:
        print("Login gagal, scraping tidak dilanjutkan.")

except Exception as e:
    print(f"Terjadi error: {e}")

finally:
    driver.quit()
    print("Browser ditutup.")