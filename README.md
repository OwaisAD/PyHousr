# PyHousr

## Table of content

- [Python_eksamen](#Python_eksamen)
  - [Table of content](#table-of-content)
  - [About](#about)
  - [Setup project instructions](#Setup-project-instructions)
  - [Extend project](#Extend-project)
  - [Status](#status)
  - [List of Challenges](#List-of-Challenges)
  - [Other documents](#Other-documents)

## About

Semester project, 4th semester, Python Data Science application using Python, Selenium, Geopy, Pandas, Numpy, Tkinter, Matplotlib, Sklearn.
Models: Linear Regression and Random Forrest Regression.
<br>

## Setup project instructions

1. Install the following packages:
   - selenium
   - pandas
   - numpy
   - customtkinter and tk
   - maplotlib
   - sklearn
   - geopy

Run the following command in the terminal to invoke the GUI

```
python3 UI.py
```

or you might need to use

```
python UI.py
```

If you'd like extend the project with additional cities, then check out the following section.
<br>

## Extend project

If you want to scrape data for additional cities, it is a 2 step process:
First you have to scrape the house links from dingeo.dk. This can be achieved by running the file "link_scraper.py" with the city zipcode as the argument, for example:

```
python3 link_scraper.py 4000
```

This will create a file in the ./data/link_data directory.

Secondly you have to scrape the house data. This can be achieved with the following command using zip_code 4000 as an argument:

```
python3 house_data_scraper.py 4000
```

You may have to create a file in ./data/house_data called:
house_data_4000.csv
and add the following headers: <br>

```
Address,X,Y,Price,Type,Size,Squaremeter price,Energy class,Url
```

If you want the models and UI to include your newly scraped house_data, you have to add the zip code of the city to the lists in each model and UI under the following files:

- ./notebooks/LinearRegression.ipynb
- ./notebooks/RandomTreeRegression.ipynb
- ./gui/UI.py

## Status

In this project, our objective was to create an application that could accurately predict the market price of residences using machine learning. The prediction was based on various parameters such as location, size, energy class and residence type. We successfully achieved what we set out as our goal and our end result is a user interface where users can interact and calculate an estimated price for a residence, in a limited geographical area based on zip codes. The area is open for extension.

To further improve our model, we recognized the need for more comprehensive data. Ideally, accessing an API for data collection instead of relying on web scraping would simplify the process and allow us to incorporate additional features, such as ground/land area, floor count, floor level for appartments, basement (if any), near ocean, near highway, noise level etc.

Overall, we achieved what we set out to do. Our model performs very well, with approximately 90% of the calculated prices falling within 20% margin of the listed prices.

## Other documents

Brainstorming can be found [here](https://docs.google.com/document/d/1BFdvE4-UCWUdEFiJL24s-s-r8a0LO03WU1U8LXW24tU/edit)
