import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def main():
    scratch_dir = "/Users/vanshprajapati/.gemini/antigravity-ide/brain/df71606a-1a5b-4909-868b-f499be11e281/scratch"
    os.makedirs(scratch_dir, exist_ok=True)

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1440,950')
    options.page_load_strategy = 'eager'
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    print("Launching Chrome via Selenium (page_load_strategy=eager)...")
    driver = webdriver.Chrome(options=options)

    try:
        url = "http://localhost:8089/?nopreloader=1"
        print(f"Navigating to {url}...")
        driver.get(url)
        time.sleep(1.0)

        # Remaining sections to inspect
        sections = [
            ("gallery", "09_archive_social.png"),
            ("final-cta", "10_final_cta.png"),
            ("contact", "11_footer.png")
        ]

        for sec_id, filename in sections:
            try:
                el = driver.find_element(By.ID, sec_id)
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", el)
                time.sleep(0.6)
                out_path = os.path.join(scratch_dir, filename)
                driver.save_screenshot(out_path)
                print(f"Captured: {out_path} (size: {os.path.getsize(out_path)} bytes)")
            except Exception as e:
                print(f"Error capturing {sec_id}: {e}")

        # Check browser console logs
        print("\nChecking browser console errors...")
        logs = driver.get_log('browser')
        errors = [l for l in logs if l['level'] == 'SEVERE']
        if errors:
            print(f"Console errors found ({len(errors)}):")
            for err in errors:
                print(" -", err['message'])
        else:
            print("Zero console errors!")

        # Test Mobile Viewport (375x812)
        print("\nTesting mobile viewport (375x812)...")
        driver.set_window_size(375, 812)
        time.sleep(0.5)
        # Fresh reload on mobile to test hero directly
        driver.get(url)
        time.sleep(1.0)
        mob_hero = os.path.join(scratch_dir, "mobile_01_hero.png")
        driver.save_screenshot(mob_hero)
        print(f"Captured: {mob_hero} (size: {os.path.getsize(mob_hero)} bytes)")

        # Scroll to signature
        el_sig = driver.find_element(By.ID, "signature")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", el_sig)
        time.sleep(0.6)
        mob_sig = os.path.join(scratch_dir, "mobile_02_signature.png")
        driver.save_screenshot(mob_sig)
        print(f"Captured: {mob_sig} (size: {os.path.getsize(mob_sig)} bytes)")

        # Scroll to final CTA
        el_cta = driver.find_element(By.ID, "final-cta")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", el_cta)
        time.sleep(0.6)
        mob_cta = os.path.join(scratch_dir, "mobile_03_final_cta.png")
        driver.save_screenshot(mob_cta)
        print(f"Captured: {mob_cta} (size: {os.path.getsize(mob_cta)} bytes)")

        # Check horizontal overflow across all required breakpoints
        breakpoints = [320, 360, 375, 390, 430, 768, 820, 1024, 1280, 1440]
        print("\nVerifying horizontal overflow across all breakpoints:")
        for bp in breakpoints:
            driver.set_window_size(bp, 800)
            time.sleep(0.1)
            overflow = driver.execute_script("return document.documentElement.scrollWidth > window.innerWidth;")
            print(f" - {bp}px: overflow={overflow}")

        # Check computed styles for key text elements
        print("\nChecking key typography contrast values:")
        driver.set_window_size(1440, 950)
        driver.get(url)
        time.sleep(1.0)
        hero_brand = driver.find_element(By.CLASS_NAME, "hero-brand")
        print("Hero Brand Color:", hero_brand.value_of_css_property("color"))
        
        sig_title = driver.find_element(By.CSS_SELECTOR, "#signature .section-title-large")
        print("Signature Title Color:", sig_title.value_of_css_property("color"))

        cta_title = driver.find_element(By.CLASS_NAME, "cta-brand-title")
        print("Final CTA Title Color:", cta_title.value_of_css_property("color"))

        cta_sub = driver.find_element(By.CLASS_NAME, "cta-brand-sub")
        print("Final CTA Sub Color:", cta_sub.value_of_css_property("color"))

        cta_quote = driver.find_element(By.CLASS_NAME, "cta-quote")
        print("Final CTA Quote Color:", cta_quote.value_of_css_property("color"))

        spec_vals = driver.find_elements(By.CLASS_NAME, "spec-value")
        if spec_vals:
            print("Spec Value Color:", spec_vals[0].value_of_css_property("color"), "Opacity:", spec_vals[0].value_of_css_property("opacity"))

    finally:
        driver.quit()
        print("QA Complete!")

if __name__ == "__main__":
    main()
