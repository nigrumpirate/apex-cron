from bs4 import BeautifulSoup

def extract_tables(html_content):
    """
    Extract data from various HTML tables and return as a JSON string.
    
    Parameters:
    html_content (str): The HTML content containing the table data.
    
    Returns:
    str: A JSON string representing the extracted data from the tables.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    result = []

    # Extracting data from table-case
    case_status = soup.find('h3', class_='text-center text-danger blinkingD')
    # print("Case status is", case_status)

    if case_status != None:
        # print("If block")
        status = case_status.strong.text.strip()
        case_heading = soup.find('h3', class_='text-center text-danger blinkingD').find_next_sibling()
        # print("Case status is", case_heading.text.strip())
        # print(status, "Status")
        result.append({'case_heading' : case_heading.text.strip()})
        result.append({'case-status': status})
    else:
        # print("I am here")
        case_status = soup.find('h3', class_='text-center text-success blinkingP')
        case_heading = case_status.find_next_sibling()
        status = case_status.strong.text.strip()
        # print(status, "Status")
        result.append({'case_heading' : case_heading.text.strip()})
        result.append({'case-status': status})
    
    


    table_case = soup.find('table', class_='table-case')
    if table_case:
        case_data = {}
        rows = table_case.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:
                key = row.find('th').get_text(strip=True)
                value = cells[0].get_text(strip=True)
                case_data[key] = value
            elif len(cells) == 3:
                key = row.find('th').get_text(strip=True)
                value1 = cells[0].get_text(strip=True)
                value2 = cells[1].get_text(strip=True)
                case_data[key] = f"{value1}, {value2}"
        result.append({'table-case': case_data})

    # Extracting data from table-red
    table_red = soup.find('table', class_='table-red')
    if table_red:
        red_data = {}
        rows = table_red.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            key = row.find('th').get_text(strip=True)
            value = cells[0].get_text(strip=True)
            red_data[key] = value
        result.append({'table-red': red_data})

    def clean_info(info):
        advocate_marker = 'Advocate -'
        advocate_start = info.find(advocate_marker)
        print("Advocate Start clean info", advocate_start)
        if advocate_start != -1:
            return info[:advocate_start].strip()
        return info.strip()
    
    def extract_advocate(info):
        advocate_marker = 'Advocate -'
        advocate_start = info.find(advocate_marker)
        print("Advocate Start", advocate_start)

        if advocate_start != -1:
            return info[advocate_start + len(advocate_marker):].strip()
        return ''
    table_adv = soup.find('table', class_='table-adv')
    if table_adv:
        adv_data = []
        rows = table_adv.find_all('tr')[1:]  # Skip header row
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:  # Ensure there are two cells (for Petitioner and Respondent)
                petitioner_info = cells[0].get_text(strip=True)
                respondent_info = cells[1].get_text(strip=True)
                
                # Extracting petitioner's advocate
                petitioner_advocate = extract_advocate(petitioner_info)
                
                # Extracting respondent's advocate
                respondent_advocate = extract_advocate(respondent_info)
                
                # Clean petitioner's and respondent's info
                petitioner_cleaned = clean_info(petitioner_info)
                respondent_cleaned = clean_info(respondent_info)
                
                adv_data.append({
                    'Petitioner': petitioner_cleaned,
                    'petAdvocate': petitioner_advocate,
                    'Respondent': respondent_cleaned,
                    'resAdvocate': respondent_advocate
                })
        
        result.append({'table-adv': adv_data})

    # Extracting data from table-cat
    table_cat = soup.find('table', class_='table-cat')
    if table_cat:
        cat_data = {}
        rows = table_cat.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            key = row.find('th').get_text(strip=True)
            value = cells[0].get_text(strip=True)
            cat_data[key] = value
        result.append({'table-cat': cat_data})

    # Extracting data from table-lower-court
    table_lower_court = soup.find('table', class_='table-lower-court')
    if table_lower_court:
        lower_court_data = {}
        rows = table_lower_court.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                lower_court_data[key] = value
        result.append({'table-lower-court': lower_court_data})

    # Extracting data from table-filing
    table_filing = soup.find('table', class_='table-filing')
    if table_filing:
        filing_data = []
        headers = [th.get_text(strip=True) for th in table_filing.find_all('th')]
        rows = table_filing.find_all('tr')[1:]  # Skip header row
        for row in rows:
            row_dict = {}
            cells = row.find_all('td')
            for i in range(len(headers)):
                row_dict[headers[i]] = cells[i].get_text(strip=True)
            filing_data.append(row_dict)
        result.append({'table-filing': filing_data})

    # Extracting data from table-hist
    table_hist = soup.find('table', class_='table-hist')
    if table_hist:
        hist_data = []
        headers = [th.get_text(strip=True) for th in table_hist.find_all('th')]
        rows = table_hist.find_all('tr')[1:]  # Skip header row
        for row in rows:
            row_dict = {}
            cells = row.find_all('td')
            for i in range(len(headers)):
                row_dict[headers[i]] = cells[i].get_text(strip=True)
            hist_data.append(row_dict)
        result.append({'table-hist': hist_data})

    return result