import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import random
from selenium.webdriver.common.action_chains import ActionChains
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import logging
import argparse
from config import Config

# Setup logging
logger = logging.getLogger(__name__)

def setup_anti_detection_driver():
    """Create a Chrome driver with enhanced anti-detection measures"""
    options = webdriver.ChromeOptions()
    
    # Enhanced User Agent - Use a recent, common one
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    
    # Enhanced anti-detection flags
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--exclude-switches=enable-automation')
    options.add_argument('--disable-extensions-except')
    options.add_argument('--disable-plugins-discovery')
    options.add_argument('--disable-default-apps')
    options.add_argument('--no-first-run')
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-renderer-backgrounding')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-features=TranslateUI')
    options.add_argument('--disable-ipc-flooding-protection')
    
    # Viewport and window settings to mimic real user
    options.add_argument('--window-size=1366,768')
    options.add_argument('--start-maximized')
    
    # Various anti-detection settings
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Additional stability options that don't trigger detection
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    
    # Memory and performance optimizations
    options.add_argument('--memory-pressure-off')
    options.add_argument('--max_old_space_size=4096')
    
    # Add proxy if configured
    if Config.PROXY_URL:
        logger.info(f"Using proxy: {Config.PROXY_URL}")
        options.add_argument(f'--proxy-server={Config.PROXY_URL}')
    
    # Required for running in Docker container
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Headless mode - use new headless if available
    if Config.HEADLESS_MODE:
        options.add_argument('--headless=new')
    
    # Set page load strategy to EAGER for faster loading
    options.page_load_strategy = 'eager'
    
    # Driver setup
    try:
        # can be done like this also :
        # webdriver_service = Service("/usr/bin/chromedriver")
        # driver = webdriver.Chrome(service=webdriver_service, options=options)
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        logger.warning(f"Local chromedriver failed: {e}, trying ChromeDriverManager")
        try:
            # Fall back to ChromeDriverManager
            webdriver_service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=webdriver_service, options=options)
        except Exception as e:
            logger.error(f"Error with Chrome: {e}")
            raise
    
    # Enhanced anti-detection script
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            // Remove webdriver traces
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // Override plugins to appear normal
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // Override languages  
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            
            Object.defineProperty(navigator, 'language', {
                get: () => 'en-US'
            });
            
            // Override permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            
            // Randomize screen properties
            Object.defineProperty(screen, 'availHeight', {
                get: () => 1040
            });
            Object.defineProperty(screen, 'availWidth', {
                get: () => 1920
            });
            
            // Hide chrome automation indicators
            window.chrome = {
                runtime: {}
            };
            
            // Spoof webGL vendor
            const getParameter = WebGLRenderingContext.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) {
                    return 'Intel Inc.';
                }
                if (parameter === 37446) {
                    return 'Intel Iris OpenGL Engine';
                }
                return getParameter(parameter);
            };
            
            // Override navigator properties
            Object.defineProperty(navigator, 'platform', {
                get: () => 'Win32'
            });
            Object.defineProperty(navigator, 'hardwareConcurrency', {
                get: () => 8
            });
            Object.defineProperty(navigator, 'deviceMemory', {
                get: () => 8
            });
        '''
    })
    
    # Add random delays to mimic human behavior
    import random
    time.sleep(random.uniform(0.5, 1.5))
    
    return driver

def handle_cookie_consent(driver):
    """Handle cookie consent dialog if present"""
    logger.info("Looking for cookie consent dialog...")
    try:
        # Wait for cookie dialog to appear (max 1 second)
        time.sleep(1)
        
        # Try multiple selector approaches to find accept button
        accept_buttons = driver.find_elements(By.XPATH, "//button[contains(., 'accept') or contains(., 'Accept') or .//span[contains(., 'accept') or contains(., 'Accept')]]")
        
        if not accept_buttons:
            accept_buttons = driver.find_elements(By.CSS_SELECTOR, "button[id*='consent' i], button[class*='consent' i]")
        
        if accept_buttons:
            logger.info("Cookie consent dialog found, clicking accept...")
            accept_buttons[0].click()
            time.sleep(0.5)  # Brief pause after clicking
        else:
            logger.info("No cookie consent dialog detected")
            
    except Exception as e:
        logger.error(f"Error handling cookie dialog: {e}")

def wait_for_page_load(driver, max_wait=10):
    """Wait for page to load - simplified and faster version"""
    logger.info("Waiting for page to load...")
    
    # First wait for document.readyState to be complete
    try:
        WebDriverWait(driver, max_wait).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        logger.info("Page reached 'complete' state")
    except Exception as e:
        logger.warning(f"Page took too long to reach complete state: {e}")
    
    # Single scroll to trigger any lazy-loading elements
    driver.execute_script("window.scrollBy(0, 300);")
    
    # Brief pause for any final AJAX content
    time.sleep(1.5)
    
    # Check if jQuery is active (if present)
    jquery_ready = driver.execute_script("""
        return (typeof jQuery === 'undefined') || 
               (jQuery.active === 0 && jQuery.ready.state === 'complete');
    """)
    
    if not jquery_ready:
        logger.info("Waiting extra time for jQuery requests to complete")
        time.sleep(1)
    
    logger.info("Page load wait completed")

def click_lens_button(driver):
    """Find and click the Google Lens button using multiple strategies"""
    logger.info("Looking for Google Lens button...")
    
    # Try different selector strategies (in order of preference)
    selectors = [
        # Primary selector based on data-attribute
        "[data-base-lens-url='https://lens.google.com']",
    ]
    
    for selector in selectors:
        try:
            logger.info(f"Trying selector: {selector}")
            wait = WebDriverWait(driver, 5)
            lens_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            
            # Move mouse to button before clicking (more human-like)
            action = ActionChains(driver)
            action.move_to_element(lens_button).pause(0.3).perform()
            
            logger.info("Found Google Lens button, clicking...")
            lens_button.click()
            time.sleep(1)
            return True
        except Exception as e:
            logger.debug(f"Selector {selector} failed: {e}")
    
    # If we get here, all selectors failed
    logger.error("Could not find Google Lens button")
    return False

def find_and_click_import_option(driver):
    """Find and click the import option in Google Lens"""
    logger.info("Looking for import option...")
    
    # Wait a moment for Lens page to load
    time.sleep(2)
    
    # Different selectors for the import button/link, ordered by specificity
    import_selectors = [  
        "//span[contains(text(), 'file')]",        # anglais  
        "//span[contains(text(), 'fichier')]",     # français  
        "//span[contains(text(), 'Datei')]",       # allemand  
        "//span[contains(text(), 'archivo')]",     # espagnol  
        "//span[contains(text(), 'ficheiro')]",    # portugais  
        "//span[contains(text(), 'bestand')]",    # néerlandais
        "//span[contains(text(), 'αρχείο')]",     # grec  
    ]
    
    # Try each selector
    for selector in import_selectors:
        try:
            logger.info(f"Trying import selector: {selector}")
            is_xpath = selector.startswith("//")
            by_method = By.XPATH if is_xpath else By.CSS_SELECTOR
            
            # If this is potentially a file input, it might be hidden
            if "input[type='file']" in selector:
                try:
                    # Find even if not visible
                    import_element = driver.find_element(by_method, selector)
                    logger.info("Found file input element")
                    return import_element
                except Exception as e:
                    logger.debug(f"No direct file input found: {e}")
                    continue
                
            # For visible elements
            try:
                wait = WebDriverWait(driver, 3)  # Shorter timeout for faster checking
                import_element = wait.until(EC.element_to_be_clickable((by_method, selector)))
                
                logger.info(f"Found import button: '{import_element.text}', clicking...")
                
                # Move mouse to button before clicking (more human-like)
                action = ActionChains(driver)
                action.move_to_element(import_element).pause(0.2).perform()
                import_element.click()
                
                # Wait for file dialog to appear
                time.sleep(1)
                
                # Try to find the file input that might appear after clicking
                try:
                    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                    logger.info("Found file input after clicking button")
                    return file_input
                except:
                    # Return the clicked element
                    logger.info("No file input found after click, returning clicked element")
                    return import_element
            
            except Exception as e:
                logger.debug(f"Selector {selector} not clickable: {e}")
                continue
                
        except Exception as e:
            logger.debug(f"Import selector {selector} failed: {e}")
    
    # Special handling for last resort - try JavaScript click on any button with "import" or "file" text
    try:
        logger.info("Trying JavaScript approach to find import button...")
        buttons = driver.execute_script("""
            function containsFileOrImport(text) {
                if (!text) return false;
                text = text.toLowerCase();
                return text.includes('file') || 
                       text.includes('fichier') || 
                       text.includes('import') || 
                       text.includes('upload');
            }
            
            // Find all potential buttons
            let potentialButtons = [];
            document.querySelectorAll('[role="button"], button, span').forEach(el => {
                if (containsFileOrImport(el.textContent)) {
                    potentialButtons.push(el);
                }
            });
            
            return potentialButtons;
        """)
        
        if buttons and len(buttons) > 0:
            logger.info(f"Found {len(buttons)} potential import buttons via JavaScript")
            # Try clicking the first one
            action = ActionChains(driver)
            action.move_to_element(buttons[0]).pause(0.2).perform()
            buttons[0].click()
            time.sleep(1)
            
            # Try to find file input after click
            try:
                file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                return file_input
            except:
                return buttons[0]
    
    except Exception as e:
        logger.error(f"JavaScript approach failed: {e}")
    
    logger.error("Could not find import option")
    return None

def upload_image(driver, file_element, image_path):
    """Upload an image file using the provided element"""
    if file_element is None:
        logger.error("No file input element found")
        return False
        
    try:
        # Get absolute path to image
        abs_image_path = os.path.abspath(image_path)
        logger.info(f"Uploading image: {abs_image_path}")
        
        # Verify image file exists and is valid
        if not os.path.exists(abs_image_path):
            logger.error(f"Image file does not exist: {abs_image_path}")
            return False
            
        # Check file size (should be reasonable)
        file_size = os.path.getsize(abs_image_path)
        logger.info(f"Image file size: {file_size} bytes")
        if file_size == 0:
            logger.error("Image file is empty")
            return False
        
        # If it's an input element, use send_keys
        if file_element.tag_name.lower() == 'input' and file_element.get_attribute('type') == 'file':
            file_element.send_keys(abs_image_path)
            logger.info("File upload initiated via input element")
            
            # Wait a bit for upload to process
            time.sleep(2)
            
            # Try to verify upload started by checking if input has value
            try:
                if file_element.get_attribute('value'):
                    logger.info("Upload appears successful - input has value")
                    return True
                else:
                    logger.warning("Upload may have failed - input has no value")
            except:
                logger.debug("Could not check input value")
            
            return True
            
        # Otherwise try to trigger the file dialog and look for input
        else:
            logger.info("Element is not a file input, trying to find one after clicking")
            file_element.click()
            time.sleep(2)  # Increased wait time
            
            try:
                file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                file_input.send_keys(abs_image_path)
                logger.info("File upload initiated after click")
                time.sleep(2)  # Wait for upload processing
                return True
            except Exception as e:
                logger.error(f"Failed to find file input after click: {e}")
                
                # Try alternative selectors for file input
                selectors = [
                    "input[accept*='image']",
                    "input[accept*='*']",
                    "input[type='file']"
                ]
                
                for selector in selectors:
                    try:
                        logger.debug(f"Trying alternative selector: {selector}")
                        alt_input = driver.find_element(By.CSS_SELECTOR, selector)
                        alt_input.send_keys(abs_image_path)
                        logger.info(f"File upload successful with selector: {selector}")
                        time.sleep(2)
                        return True
                    except:
                        continue
                        
                return False
                
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        return False
        
def extract_links_and_descriptions(driver, csv_path):
    """Extract all non-Google links and their descriptions from the page"""
    logger.info("Extracting links and descriptions...")
    
    # Use a raw string for the JavaScript to avoid Python escape sequence warnings
    links_with_desc = driver.execute_script(r"""
        let results = [];
        
        // Get all <a> tags on the page
        let elements = document.getElementsByTagName('a');
        for (let i = 0; i < elements.length; i++) {
            let link = elements[i];
            let href = link.getAttribute('href');
            
            if (href && href.startsWith('http')) {
                let description = '';
                
                // Try to get text directly from the link
                if (link.textContent && link.textContent.trim()) {
                    description = link.textContent.trim();
                }
                // Or from parent element if link has no text
                else if (link.parentElement && link.parentElement.textContent) {
                    description = link.parentElement.textContent.trim();
                }
                
                results.push({
                    url: href,
                    description: description
                });
            }
        }
        
        // Get links from elements that might be clickable but not <a> tags
        elements = document.querySelectorAll('[onclick], [data-url]');
        for (let i = 0; i < elements.length; i++) {
            let el = elements[i];
            let href = null;
            
            // Check onclick attribute
            if (el.hasAttribute('onclick')) {
                let onclick = el.getAttribute('onclick');
                if (onclick && onclick.includes('http')) {
                    let match = onclick.match(/(https?:\/\/[^'"\s]+)/g);
                    if (match) href = match[0];
                }
            }
            
            // Check data-url attribute
            if (!href && el.hasAttribute('data-url')) {
                let dataUrl = el.getAttribute('data-url');
                if (dataUrl && dataUrl.startsWith('http')) {
                    href = dataUrl;
                }
            }
            
            if (href) {
                // Get text from the element
                let description = el.textContent ? el.textContent.trim() : '';
                results.push({
                    url: href,
                    description: description
                });
            }
        }
        
        return results;
    """)
    
    # Filter out Google domains
    filtered_results = [
        item for item in links_with_desc 
        if not any(domain in item['url'] for domain in [
            'google.com', 'gstatic.com', 'googleapis.com', 'chrome.com',
            'google.co', 'googleusercontent.com'
        ])
    ]
    
    logger.info(f"Found {len(filtered_results)} unique external links")
    
    # Write results to CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['URL', 'Description'])  # Header with both columns
        for item in filtered_results:
            writer.writerow([item['url'], item['description']])
    
    logger.info(f"All links saved to {csv_path}")
    return filtered_results

def run_google_lens_search(image_path, csv_path):
    """Run a Google Lens search with the provided image and save results to CSV"""
    driver = setup_anti_detection_driver()
    
    try:
        # Start at Google.com
        url = "https://www.google.com"
        logger.info(f"Opening {url}...")
        driver.get(url)
        
        # Add random delay to mimic human behavior
        import random
        time.sleep(random.uniform(1.0, 2.5))
        
        # Handle cookie consent dialog
        handle_cookie_consent(driver)
        
        # Random delay after cookie handling
        time.sleep(random.uniform(0.5, 1.5))
        
        # Set window size
        driver.set_window_size(1366, 768)
        
        # Wait for page to load completely
        wait_for_page_load(driver)
        
        # Random delay before clicking lens button
        time.sleep(random.uniform(1.0, 2.0))
        
        # Click on Google Lens button
        if not click_lens_button(driver):
            logger.error("Failed to access Google Lens - aborting")
            return False
            
        # Wait for Google Lens interface to load
        wait_for_page_load(driver)
        
        # Random delay before import
        time.sleep(random.uniform(0.8, 1.8))
        
        # Find and click import option
        file_input = find_and_click_import_option(driver)
        
        # Upload image file
        if not upload_image(driver, file_input, image_path):
            logger.error("Failed to upload image - aborting")
            return False
            
        # Wait longer for image to be processed by Google Lens
        logger.info("Waiting for image upload to complete...")
        time.sleep(3)  # Additional wait for upload processing
        
        # Check if upload was successful by looking for error messages
        try:
            # Look for Google's "seems there was no image uploaded" error or similar
            error_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'seems there') or contains(text(), 'no image') or contains(text(), 'upload') or contains(text(), 'error')]")
            if error_elements:
                for element in error_elements:
                    error_text = element.text.lower()
                    if any(phrase in error_text for phrase in ['seems there', 'no image', 'upload failed', 'try again']):
                        logger.error(f"Google Lens upload error detected: {element.text}")
                        return False
        except Exception as e:
            logger.debug(f"Error check failed (this is okay): {e}")
            
        # Wait for search results to load
        logger.info("Waiting for search results...")
        time.sleep(5)  # Initial wait
        wait_for_page_load(driver)
        
        # Extract all links and descriptions
        extract_links_and_descriptions(driver, csv_path)
        return True
        
    except Exception as e:
        logger.error(f"Error in Google Lens search: {e}")
        return False
    finally:
        # Always close the driver
        logger.info("Closing browser...")
        driver.quit()

# Module can be run independently
if __name__ == "__main__":
    # Setup basic logging for standalone use
    logging.basicConfig(level=logging.INFO, 
                       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create argument parser
    parser = argparse.ArgumentParser(description="Run Google Lens image search")
    parser.add_argument("--image", "-i", required=True, help="Path to image file")
    parser.add_argument("--output", "-o", help="Output CSV file path")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create output path if not provided
    if not args.output:
        # Make sure directory exists
        os.makedirs(Config.CSV_DIR, exist_ok=True)
        # Create output path
        args.output = f"{Config.CSV_DIR}/results_{os.path.basename(args.image)}.csv"
    
    # Run search
    logger.info(f"Running Google Lens search on {args.image}")
    success = run_google_lens_search(args.image, args.output)
    
    if success:
        logger.info(f"Success! Results saved to {args.output}")
    else:
        logger.error("Search failed")
        sys.exit(1)