from automation import TaskManager, CommandSequence


def parse_cookie_selectors(file_name):
    """Parse the cookie selectors and return them in data structure.

    The data structure maps FQDNs to a list of CSS selectors.  The empty string
    "" maps to a list of general CSS selectors that apply to many sites."""

    # Maps a domain to a list of selectors.
    filterlist = dict()
    unknown = 0

    with open(file_name) as fd:
        for line in fd:
            # AdBlock's filter rules are complex, but we only care about a
            # subset: element hiding rules.  These rules are denoted by the
            # symbol "##".
            if "##" not in line:
                unknown += 1
                continue
            domains, selectors = line.strip().split("##")

            # Commas denote a list of domains and selectors.
            domains = [s.strip() for s in domains.split(",")]
            selectors = [s.strip() for s in selectors.split(",")]

            for domain in domains:
                for selector in selectors:
                    s = filterlist.get(domain, [])
                    filterlist[domain] = s + [selector]

    if unknown > 0:
        print "%d element weren't element hiding rules" % unknown

    return filterlist

COOKIESELECTOR_DAT = "./cookie-selectors.dat"
selectors = parse_cookie_selectors(COOKIESELECTOR_DAT)

# The list of sites that we wish to crawl
NUM_BROWSERS = 1
sites = ['http://derstandard.at', 'http://tudelft.nl', 'http://ad.nl', 'http://google.nl', 'http://google.com']  

# Loads the manager preference and 3 copies of the default browser dictionaries
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration 
for i in xrange(NUM_BROWSERS):
    browser_params[i]['disable_flash'] = True 
    browser_params[i]['headless'] = True 

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/Desktop/'
manager_params['log_directory'] = '~/Desktop/'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

for site in sites:
    command_sequence = CommandSequence.CommandSequence(site, reset=True)
    command_sequence.get(sleep=0, timeout=60)  # Start by visiting the page
    command_sequence.detect_cookie_banner(selectors, timeout=60)  # Detect cookie banners
    manager.execute_command_sequence(command_sequence)


# Shuts down the browsers and waits for the data to finish logging
manager.close()
