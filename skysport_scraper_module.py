# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 11:14:02 2020

@author: Cédric
"""
def scrap_page(url):
    """
    

    Parameters
    ----------
    url : str
        The url should follow this format : https://www.skysports.com/premier-league-table/<year>

    Returns
    -------
    DataFrame
        Returns a pandas DataFrame containing the page table

    """
    import requests
    try:
        requests.get(url)
    except:
        print("wrong URL, try again with a valid  URL")
        return -1
    
    page = requests.get(url)
    if(page.status_code != 200):
        print("Could not download the page, try again")
    else:
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(page.text, 'html.parser')
        
        league = soup.find('table', class_ = 'standing-table__table')
        league_table = league.find_all('tbody')
        
        league= []
        for league_teams in league_table:
            rows = league_teams.find_all('tr')
            for row in rows:
                team_data = [row.find_all('td', class_ = 'standing-table__cell')[i].text.strip() for i in range(1,10)]
                league_dict= {
                    'Team':team_data[0],
                    'PI':team_data[1],
                    'W':team_data[2],
                    'D':team_data[3],
                    'L':team_data[4],
                    'F':team_data[5],
                    'A':team_data[6],
                    'GD':team_data[7],
                    'Pts':team_data[8]
                }
                league.append(league_dict)
        
        import pandas as pd
        
        df = pd.DataFrame(league)
        df = df[['Team','PI','W','D','L','F','A','GD','Pts']]
        
        return df