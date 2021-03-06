# SeleniumMultiBrowser


A simplified class wrapper/controller for handling multiple browsers. This can help evading log pattern detection by remote websites. I initially used this to perform a large amount of OSINT collection (50K+ users on LinkedIn) and subsequently enumerating valid accounts against Cloud authentication gateways.

In order to use this class, the prereq below must be met:

    1) The Python Selenium module installed (pip install selenium)
    2) The WebDriver for whichever browser you choose. (Firefox -> geckodriver / Chrome -> chromedriver)
    3) The Browser associated with the WebDriver you'll be using must be installed

## Configs
```config.json```  A key-value hashtable/dictionary.  Valid keys are any of the class properties. The path can be passed upon instantiation. 

See the contents of configs.json for an example.

## Example

See test.py; Firefox's webdriver used (geckodriver). Limited testing was done with the Chrome's WebDriver.  Tested both on Windows and Kali Linux.

## Notes

Right now this class is pretty bare in functionality. 

Short-term plans:

    Allow option for running headless
    Add per-browser proxy configs


If running from a command-line only shell, you'll need to set up a virtual monitor.

```sudo apt-get install xvfb -y
Xvfb :99 -ac &
export DISPLAY=:99```

In order to use this, you'll need to know how to inspect DOM elements by inspecting pages via a web browser's debugger.  
